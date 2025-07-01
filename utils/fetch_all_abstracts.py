##################################################################################################
#                                FETCH ABSTRACTS FROM PUBMED API                                #
#                                                                                                #
# This script fetches scientific articles from PubMed based on a user-defined query.            #
# It stores article metadata as JSON files and logs executed queries to file.                   #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import os
import sys

# Add project root to Python path for relative imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.logs_config import logger
from api_clients.pubmed_client import PubMedClient
from utils.io_helpers import save_article_json, log_query
from utils.paths import RAW_DATA_DIR, DOCS_DIR

# Full path for the query log file
QUERIES_LOG = DOCS_DIR / "api_queries.txt"

##################################################################################################
#                                       MAIN FETCH FUNCTION                                      #
##################################################################################################

def fetch_all(query: str, max_results: int = 250):
    """
    Fetches up to `max_results` PubMed articles containing both title and abstract.

    Retrieves a large pool of article IDs and processes them in batches to avoid API overload.
    Stops once the desired number of valid articles is reached. Each result is saved as a
    separate JSON file. Skips duplicates based on filename matching.

    Args:
        query (str): Search term to submit to PubMed.
        max_results (int): Maximum number of valid articles to fetch.
    """

    logger.info(f"🚀 Starting full fetch for query: '{query}'")
    logger.info("🌐 Querying PubMed...")

    pubmed = PubMedClient()
    all_ids = pubmed.search(query, max_results=1000)  # recupera muchos IDs

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
        saved_path = save_article_json(article, RAW_DATA_DIR)
        if saved_path:
            logger.info(f"✅ Saved: {os.path.basename(saved_path)}")
        else:
            logger.info("📄 Article already exists. Skipped.")

    log_query("PubMed", query, QUERIES_LOG)


##################################################################################################
#                                         SCRIPT ENTRYPOINT                                      #
##################################################################################################

if __name__ == "__main__":
    query = input("🔎 Enter your search term (e.g., polyphenols): ").strip()
    if query:
        fetch_all(query=query)
    else:
        print("⚠️ No search term provided.")
