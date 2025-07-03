##################################################################################################
#                                      IO HELPER FUNCTIONS                                       #
#                                                                                                #
# Utility functions for saving JSON articles and logging performed queries across API clients.   #
# All outputs are stored in standardized project directories using pathlib.                      #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import json
import re
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

from utils.paths import RAW_DATA_DIR, API_QUERIES_LOG
from utils.logs_config import logger

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def sanitize_title(title: str) -> str:
    """
    Converts an article title into a safe filename format.

    Removes special characters and replaces spaces with underscores,
    truncating the result to a reasonable filename length.

    Args:
        title (str): Raw article title.

    Returns:
        str: Sanitized filename.
    """
    title = re.sub(r'[^\w\s-]', '', title)
    title = re.sub(r'\s+', '_', title.strip())
    return title[:100]


def save_article_json(article: Dict[str, Any], output_dir: Path = RAW_DATA_DIR) -> Path:
    """
    Saves a single article dictionary as a JSON file.

    The filename includes the article source and a sanitized version of its title.
    If a file already exists with the same name, it will not be overwritten.

    Args:
        article (Dict[str, Any]): Metadata and content of the article.
        output_dir (Path): Output directory to save the JSON.

    Returns:
        Path: Full path to the saved file, or None if the file already existed.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    filename = f"{article['source']} - {sanitize_title(article['title'])}.json"
    filepath = output_dir / filename

    if filepath.exists():
        logger.debug(f"Skipping duplicate: {filepath.name}")
        return None

    with filepath.open("w", encoding="utf-8") as f:
        json.dump(article, f, indent=2, ensure_ascii=False)

    logger.info(f"✅ Saved article: {filepath.name}")
    return filepath


def log_query(source: str, query: str, log_path: Path = API_QUERIES_LOG) -> None:
    """
    Appends an API query log entry to the queries log file.

    Includes source name, search query, and UTC timestamp.

    Args:
        source (str): Name of the data source (e.g. PubMed).
        query (str): Search term or keyword used.
        log_path (Path): Path to the log file.
    """
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    entry = f"{source} | {query} | {timestamp}\n"

    with log_path.open("a", encoding="utf-8") as f:
        f.write(entry)

    logger.debug(f"📝 Logged query: [{source}] {query}")
