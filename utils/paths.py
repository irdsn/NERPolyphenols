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

# Central log directory for tracking queries, extraction results, etc.
LOGS_DIR = BASE_DIR / "logs"

# Specific logs
API_QUERIES_LOG = LOGS_DIR / "api_queries.txt"

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

for path in [
    RAW_DATA_DIR,
    DOCCANO_DIR,
    PROCESSED_DATA_DIR,
    LOGS_DIR,
]:
    path.mkdir(parents=True, exist_ok=True)
