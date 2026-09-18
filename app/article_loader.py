import re

from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document


def load_articles(search_results: list[dict]) -> list[Document]:
    """Load article pages and keep usable text."""
    articles = []

    for result in search_results:
        try:
            loader = WebBaseLoader(web_paths=(result["url"],))
            docs = loader.load()

            if docs and len(docs[0].page_content) > 300:
                docs[0].page_content = re.sub(r"\s+", " ", docs[0].page_content).strip()
                docs[0].metadata.update(result)
                articles.append(docs[0])
        except Exception as error:
            print(f"Could not load {result['url']}: {error}")

    return articles
