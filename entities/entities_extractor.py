##################################################################################################
#                               ENTITY EXTRACTION FROM ABSTRACTS                                #
#                                                                                                #
# This script processes abstracts from PubMed and extracts candidate entities using heuristics  #
# based on predefined lexicons. The output is stored in JSON format for downstream use.         #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import json
from collections import defaultdict
from tqdm import tqdm
import spacy

from defined.polyphenols import KNOWN_POLYPHENOLS
from defined.foods import KNOWN_FOODS
from defined.symptoms import KNOWN_SYMPTOMS
from utils.paths import RAW_DATA_DIR, EXTRACTED_ENTITIES_DIR
from utils.logs_config import logger

##################################################################################################
#                                         CONFIGURATION                                           #
##################################################################################################

try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("✅ Loaded spaCy model: en_core_web_sm")
except Exception:
    nlp = spacy.load("en_core_sci_sm")
    logger.warning("⚠️ Fallback to spaCy model: en_core_sci_sm")

##################################################################################################
#                                     ENTITY EXTRACTION LOGIC                                    #
##################################################################################################

def extract_entities(text: str) -> dict:
    """
    Extract candidate entities from the input text using known lexicons
    and noun chunking from spaCy.

    Args:
        text (str): Input abstract text.

    Returns:
        dict: Dictionary with keys 'POLYPHENOL', 'FOOD', 'SYMPTOM' and extracted terms.
    """
    doc = nlp(text)
    candidates = defaultdict(set)

    for chunk in doc.noun_chunks:
        span = chunk.text.lower().strip()
        if any(term in span for term in KNOWN_POLYPHENOLS):
            candidates['POLYPHENOL'].add(span)
        elif any(term in span for term in KNOWN_FOODS):
            candidates['FOOD'].add(span)
        elif any(term in span for term in KNOWN_SYMPTOMS):
            candidates['SYMPTOM'].add(span)

    return {k: sorted(list(v)) for k, v in candidates.items()}

##################################################################################################
#                                         MAIN EXECUTION                                         #
##################################################################################################

def main():
    """
    Process all raw abstracts and extract entity candidates.
    Saves the enriched documents to the extracted/ directory.
    """
    file_list = sorted([f for f in RAW_DATA_DIR.iterdir() if f.suffix == ".json"])
    logger.info(f"📁 Input directory: {RAW_DATA_DIR}")
    logger.info(f"📂 Output directory: {EXTRACTED_ENTITIES_DIR}")
    logger.info(f"📄 Documents to process: {len(file_list)}")

    for path in tqdm(file_list, desc="🔍 Extracting entities"):
        with open(path, 'r', encoding='utf-8') as f:
            doc = json.load(f)

        abstract = doc.get("abstract", "")
        doc["entities"] = extract_entities(abstract)

        out_path = EXTRACTED_ENTITIES_DIR / path.name
        with open(out_path, 'w', encoding='utf-8') as out_f:
            json.dump(doc, out_f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Extraction complete: {len(file_list)} documents processed.")

##################################################################################################
#                                         SCRIPT ENTRYPOINT                                      #
##################################################################################################

if __name__ == "__main__":
    main()
