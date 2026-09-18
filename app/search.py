from urllib.parse import urlparse

from langchain_tavily import TavilySearch

from app.config import TOP_K


def search_news(query: str) -> list[dict]:
    """Return recent news results from Tavily."""
    search = TavilySearch(
        topic="news",
        time_range="week",
        search_depth="basic",
        max_results=TOP_K,
    )
    results = search.invoke({"query": query})["results"]

    for result in results:
        result["source"] = urlparse(result["url"]).netloc
        result["published_at"] = result.get("published_date", "Not provided")

    return results
