##################################################################################################
#                                      ENTITY DICTIONARY BUILDER                                 #
#                                                                                                #
# This script processes all auto-tagged JSON abstracts from the entity extraction pipeline,      #
# sanitizes the extracted entities, and generates a global dictionary grouped by entity type.    #
# It also creates a human-readable log with top entities per category for manual inspection.     #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import json
import re
from collections import Counter
from datetime import datetime

from utils.paths import EXTRACTED_ENTITIES_DIR, ENTITY_DICTIONARY_PATH, RAW_DICT_LOG

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

ENTITY_LABELS = ["polyphenol", "food", "symptom"]

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def sanitize_entity(entity: str) -> str:
    """
    Cleans and standardizes an entity string for consistency across the dataset.

    - Converts to lowercase.
    - Strips leading/trailing spaces.
    - Removes trailing punctuation.
    - Collapses multiple spaces into one.

    Args:
        entity (str): Raw entity text.

    Returns:
        str: Sanitized entity string or empty string if invalid.
    """
    entity = entity.strip().lower()
    entity = re.sub(r'\s+', ' ', entity)
    entity = re.sub(r'[.,;:!?()"\']+$', '', entity)
    return entity if len(entity) > 1 else ""


def write_log(entity_dict: dict, total_files: int) -> None:
    """
    Writes a summary log of the generated entity dictionary.

    Includes counts of total and unique entities per label, and the top 10 entities
    per category with their frequencies.

    Args:
        entity_dict (dict): Dictionary with entity frequencies per type.
        total_files (int): Number of processed JSON files.
    """
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(RAW_DICT_LOG, "w", encoding="utf-8") as log_file:
        log_file.write("📘 Entity Dictionary Generation Log\n")
        log_file.write(f"🕒 Date: {now}\n")
        log_file.write(f"📄 Files processed: {total_files}\n\n")

        total_entities = {label: sum(counter.values()) for label, counter in entity_dict.items()}

        for label in ENTITY_LABELS:
            log_file.write(f"== {label.upper()} ==\n")
            log_file.write(f" - Total entities found: {total_entities[label]}\n")
            log_file.write(f" - Unique entities: {len(entity_dict[label])}\n")
            log_file.write(" - Top 10 most frequent:\n")
            for ent, count in entity_dict[label].most_common(10):
                log_file.write(f"    • {ent} : {count}\n")
            log_file.write("\n")

    print(f"📝 Log written to: {RAW_DICT_LOG}")


def generate_entity_dictionary() -> None:
    """
    Generates a frequency-based dictionary of all extracted entities.

    It processes each file in `entities/extracted/`, sanitizes entity strings,
    and updates counters per entity type. Results are saved as a consolidated JSON
    and a human-readable log.
    """
    entity_dict = {label: Counter() for label in ENTITY_LABELS}
    files = list(EXTRACTED_ENTITIES_DIR.glob("*.json"))

    print(f"🔍 Processing {len(files)} extracted entity files...")

    for file_path in files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                doc = json.load(f)

            entities_by_type = doc.get("entities", {})

            for raw_label, raw_entities in entities_by_type.items():
                label = raw_label.strip().lower()
                if label not in entity_dict:
                    continue

                for raw_text in raw_entities:
                    text = sanitize_entity(raw_text)
                    if text:
                        entity_dict[label][text] += 1

        except (json.JSONDecodeError, IOError, AttributeError) as e:
            print(f"⚠️ Error reading {file_path.name}: {e}")

    # Save dictionary as JSON
    output_dict = {label: dict(counter) for label, counter in entity_dict.items()}
    ENTITY_DICTIONARY_PATH.parent.mkdir(parents=True, exist_ok=True)

    with open(ENTITY_DICTIONARY_PATH, "w", encoding="utf-8") as out_file:
        json.dump(output_dict, out_file, indent=2, ensure_ascii=False)

    print(f"\n✅ Dictionary saved to: {ENTITY_DICTIONARY_PATH}")
    for label in ENTITY_LABELS:
        print(f" - {label}: {len(entity_dict[label])} unique entities")

    # Save log
    write_log(entity_dict, total_files=len(files))

##################################################################################################
#                                         SCRIPT ENTRYPOINT                                      #
##################################################################################################

if __name__ == "__main__":
    generate_entity_dictionary()
