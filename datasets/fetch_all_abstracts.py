##################################################################################################
#                                FETCH ABSTRACTS FROM PUBMED API                                 #
#                                                                                                #
# This script fetches scientific articles from PubMed based on a user-defined query.             #
# It stores article metadata as JSON files and logs executed queries to file.                    #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import sys
from pathlib import Path

# Add project root to Python path for relative imports
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.logs_config import logger
from utils.io_helpers import save_article_json, log_query
from utils.paths import RAW_DATA_DIR
from api_clients.pubmed_client import PubMedClient

##################################################################################################
#                                       MAIN FETCH FUNCTION                                      #
##################################################################################################

def fetch_all(query: str, max_results: int = 250) -> None:
    """
    Fetches PubMed articles for a given query and stores them as JSON files.

    Fetches article IDs in batches and collects metadata until reaching
    the `max_results` limit. Each valid article (with abstract) is saved
    to disk, and the query is logged for traceability.

    Args:
        query (str): Search term to submit to PubMed.
        max_results (int): Maximum number of articles to store locally.
    """
    logger.info(f"🚀 Starting full fetch for query: '{query}'")
    logger.info("🌐 Querying PubMed...")

    pubmed = PubMedClient()
    all_ids = pubmed.search(query, max_results=1000)

    valid_articles = []
    batch_size = 100
    for i in range(0, len(all_ids), batch_size):
        batch_ids = all_ids[i:i + batch_size]
        articles = pubmed.fetch_details(batch_ids, query)

        for article in articles:
            valid_articles.append(article)
            if len(valid_articles) >= max_results:
                break
        if len(valid_articles) >= max_results:
            break

    for article in valid_articles:
        save_article_json(article, RAW_DATA_DIR)

    log_query("PubMed", query)

##################################################################################################
#                                         SCRIPT ENTRYPOINT                                      #
##################################################################################################

if __name__ == "__main__":
    query = input("🔎 Enter your search term (e.g., polyphenols): ").strip()
    if query:
        fetch_all(query=query)
    else:
        print("⚠️ No search term provided.")
