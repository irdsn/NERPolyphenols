##################################################################################################
#                                      PATHS CONFIGURATION                                       #
#                                                                                                #
# This module centralizes all relevant filesystem paths for the local pipeline of the project.   #
# It ensures a single source of truth for directory structures across all scripts (extraction,   #
# annotation, processing, etc.), fostering modularity and maintainability.                       #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

from pathlib import Path

##################################################################################################
#                                        CONFIGURATION                                           #
##################################################################################################

# Root directory of the project (NERPolyphenols/)
BASE_DIR = Path(__file__).resolve().parent.parent


# Raw abstracts downloaded from PubMed (5983 total)
RAW_DATA_DIR = BASE_DIR / "datasets" / "raw"

# Output from annotation tools like Doccano (manual or semi-auto)
DOCCANO_DIR = BASE_DIR / "datasets" / "doccano"

# Final dataset processed and tokenized for training/validation/test
PROCESSED_DATA_DIR = BASE_DIR / "datasets" / "processed"

# Local script used to fetch all PubMed abstracts (placed in datasets/)
FETCH_SCRIPT_PATH = BASE_DIR / "datasets" / "fetch_all_abstracts.py"


# Main entity pipeline folder
ENTITIES_DIR = BASE_DIR / "entities"

# Predefined entity lists (e.g., known polyphenols, foods, symptoms)
DEFINED_ENTITIES_DIR = ENTITIES_DIR / "defined"

# Auto-tagged abstracts with extracted entities (from spaCy + dictionaries)
EXTRACTED_ENTITIES_DIR = ENTITIES_DIR / "extracted"

# Dictionary of all extracted and cleaned entities with frequency count
ENTITY_DICTIONARY_DIR = ENTITIES_DIR / "dictionary"
ENTITY_DICTIONARY_PATH = ENTITY_DICTIONARY_DIR / "entities_dict_raw.json"


# Central log directory for tracking queries, extraction results, etc.
LOGS_DIR = BASE_DIR / "logs"

# Specific logs
API_QUERIES_LOG = LOGS_DIR / "api_queries.txt"
RAW_DICT_LOG = LOGS_DIR / "raw_dict_log.txt"


# Folder where trained models are saved (e.g., BiLSTM .h5 or .pt)
MODELS_DIR = BASE_DIR / "models"

# Folder to store notebooks and exported training code (e.g., TFM.py)
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
TFM_SCRIPT_PATH = NOTEBOOKS_DIR / "TFM.py"

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

for path in [
    RAW_DATA_DIR,
    DOCCANO_DIR,
    PROCESSED_DATA_DIR,
    DEFINED_ENTITIES_DIR,
    EXTRACTED_ENTITIES_DIR,
    ENTITY_DICTIONARY_DIR,
    LOGS_DIR,
    MODELS_DIR,
    NOTEBOOKS_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)
