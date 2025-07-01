##################################################################################################
#                                        IO HELPER FUNCTIONS                                     #
#                                                                                                #
# Utility functions for saving JSON outputs and logging performed queries across API clients.    #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import json
import re
from datetime import datetime
from typing import Dict, Any

##################################################################################################
#                              FUNCTION: SANITIZE FILENAME FROM TITLE                            #
##################################################################################################

def sanitize_title(title: str) -> str:
    """
    Sanitizes a title string to create a safe filename.

    Removes characters that are unsafe for filenames and replaces spaces with underscores.

    Args:
        title (str): The article title.

    Returns:
        str: Sanitized filename string.
    """
    title = re.sub(r'[^\w\s-]', '', title)          # Remove special characters
    title = re.sub(r'\s+', '_', title.strip())      # Replace whitespace with underscores
    return title[:100]                              # Limit length to avoid long filenames

##################################################################################################
#                               FUNCTION: SAVE ARTICLE TO JSON FILE                              #
##################################################################################################

def save_article_json(article: Dict[str, Any], output_dir: str) -> str:
    """
    Saves an article's metadata as a JSON file in the specified directory.

    Creates the filename using the article source and a sanitized version of the title.
    Skips saving if a file with the same name already exists.

    Args:
        article (Dict[str, Any]): Article metadata dictionary.
        output_dir (str): Directory to save the file.

    Returns:
        str: Path to the saved file or empty string if skipped.
    """
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{article['source']} - {sanitize_title(article['title'])}.json"
    filepath = os.path.join(output_dir, filename)

    if os.path.exists(filepath):
        return ""

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(article, f, indent=2, ensure_ascii=False)
    return filepath

##################################################################################################
#                             FUNCTION: REGISTER QUERY IN LOG FILE                               #
##################################################################################################

def log_query(source: str, query: str, log_path: str):
    """
    Appends a record of the performed query to a text file.

    Each entry includes source, query, and UTC timestamp.

    Args:
        source (str): API source (e.g. PubMed).
        query (str): Search keyword used.
        log_path (str): File path for logging queries.
    """
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.utcnow().isoformat()
    entry = f"{source} | {query} | {timestamp}\n"

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(entry)
