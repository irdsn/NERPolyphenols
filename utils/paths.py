from pathlib import Path

# === ROOT DIRECTORY ===
# Root directory of the project (NERPolyphenols/)
BASE_DIR = Path(__file__).resolve().parent.parent

# === RAW DATA ===
# Directory to store raw article JSONs
RAW_DATA_DIR = BASE_DIR / "datasets" / "raw"

# === TEMPORAL SPLIT DATA (train/val/test) ===
TEMP_DATA_DIR = BASE_DIR / "datasets" / "temp"
TRAIN_DIR = TEMP_DATA_DIR / "train"
VAL_DIR = TEMP_DATA_DIR / "val"
TEST_DIR = TEMP_DATA_DIR / "test"

# === ANNOTATED DATA (Only train and val are labeled) ===
ANNOTATED_DIR = BASE_DIR / "datasets" / "annotated"
ANNOTATED_TRAIN_DIR = ANNOTATED_DIR / "train"
ANNOTATED_VAL_DIR = ANNOTATED_DIR / "val"

# === ENTITY EXTRACTION PIPELINE ===
ENTITIES_DIR = BASE_DIR / "entities"
DEFINED_ENTITIES_DIR = ENTITIES_DIR / "defined"       # Static entity lists
EXTRACTED_ENTITIES_DIR = ENTITIES_DIR / "extracted"   # Auto-tagged documents (5983 total)
ENTITY_DICTIONARY_DIR = ENTITIES_DIR / "dictionary"   # Final JSON dictionary
ENTITY_DICTIONARY_PATH = ENTITY_DICTIONARY_DIR / "entity_dictionary.json"

# === DOCS ===
# Directory to store logs or query tracking
DOCS_DIR = BASE_DIR / "docs"

# === Ensure all required directories exist ===
for path in [
    RAW_DATA_DIR,
    TRAIN_DIR, VAL_DIR, TEST_DIR,
    ANNOTATED_TRAIN_DIR, ANNOTATED_VAL_DIR,
    DEFINED_ENTITIES_DIR, EXTRACTED_ENTITIES_DIR, ENTITY_DICTIONARY_DIR,
    DOCS_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)
