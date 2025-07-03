##################################################################################################
#                                        PUBMED API CLIENT                                       #
#                                                                                                #
# This script provides functionality to search and fetch scientific articles from PubMed.        #
# It exposes a client class that retrieves structured metadata for local processing.             #
##################################################################################################

##################################################################################################
#                                            IMPORTS                                             #
##################################################################################################

import requests
from typing import List, Dict
from bs4 import BeautifulSoup
from dateutil import parser

##################################################################################################
#                                        IMPLEMENTATION                                          #
##################################################################################################

def extract_pubmed_date(article) -> str:
    """
    Extracts the publication date from a PubMed article element.

    Tries multiple XML paths to find the most reliable publication date available.
    Falls back to different sources if the primary path is missing.

    Args:
        article: A BeautifulSoup-parsed PubMedArticle XML element.

    Returns:
        str: Formatted publication date or empty string if not found.
    """
    try:
        if article.MedlineCitation.Article.ArticleDate:
            y = article.MedlineCitation.Article.ArticleDate.Year.get_text()
            m = article.MedlineCitation.Article.ArticleDate.Month.get_text()
            d = article.MedlineCitation.Article.ArticleDate.Day.get_text()
            return f"{y}-{m.zfill(2)}-{d.zfill(2)}"
    except Exception:
        pass

    try:
        completed = article.MedlineCitation.DateCompleted
        y = completed.Year.get_text()
        m = completed.Month.get_text()
        return f"{y}-{m.zfill(2)}-01"
    except Exception:
        pass

    try:
        date_str = article.MedlineCitation.Article.Journal.JournalIssue.PubDate.MedlineDate.get_text()
        dt = parser.parse(date_str, fuzzy=True)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    return ""

class PubMedClient:
    """
    Client for interacting with the PubMed API to search and retrieve scientific articles.

    This client provides methods to perform keyword-based searches and extract metadata
    including title, abstract, journal, DOI, and publication date.
    """

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    FETCH_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

    def search(self, query: str, max_results: int = 10) -> List[str]:
        """
        Searches the PubMed database and returns article IDs matching the query.

        Args:
            query (str): Free-text search query.
            max_results (int): Maximum number of article IDs to retrieve.

        Returns:
            List[str]: List of PubMed article IDs.
        """
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "pub+date"
        }

        response = requests.get(self.BASE_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])[:max_results]
        return []

    def fetch_details(self, ids: List[str], query: str) -> List[Dict]:
        """
        Fetches metadata for each article ID using the PubMed fetch API.

        Args:
            ids (List[str]): List of PubMed article identifiers.
            query (str): The original search query.

        Returns:
            List[Dict]: List of metadata dictionaries (only for articles with abstract).
        """
        if not ids:
            return []

        params = {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "xml"
        }

        response = requests.get(self.FETCH_URL, params=params)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "xml")
        articles = []

        for article in soup.find_all("PubmedArticle"):
            title = article.Article.ArticleTitle.get_text(strip=True) if article.Article.ArticleTitle else None
            abstract = article.Article.Abstract.AbstractText.get_text(strip=True) if article.Article.Abstract else None
            journal = article.Article.Journal.Title.get_text(strip=True) if article.Article.Journal and article.Article.Journal.Title else None
            doi_tag = article.find("ELocationID", {"EIdType": "doi"})
            doi = doi_tag.get_text(strip=True) if doi_tag else None
            pub_date = extract_pubmed_date(article)

            # Skip articles without abstract or title
            if not abstract or not title:
                continue

            articles.append({
                "source": "PubMed",
                "query": query,
                "title": title,
                "abstract": abstract,
                "publication_date": pub_date,
                "journal": journal,
                "doi": doi
            })

        return articles
