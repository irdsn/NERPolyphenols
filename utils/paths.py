from pathlib import Path

# Base directory of the project (NERPolyphenols root)
BASE_DIR = Path(__file__).resolve().parent.parent

# Directory to store raw article JSONs
RAW_DATA_DIR = BASE_DIR / "datasets" / "raw"

# Directory to store logs or query tracking
DOCS_DIR = BASE_DIR / "docs"

# Ensure directories exist
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
