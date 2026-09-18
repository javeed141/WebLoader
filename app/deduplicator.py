from langchain_core.documents import Document


def remove_duplicates(articles: list[Document]) -> list[Document]:
    """Remove articles with the same normalized title."""
    unique_articles = []
    seen_titles = set()

    for article in articles:
        title = article.metadata["title"].lower().strip()

        if title not in seen_titles:
            unique_articles.append(article)
            seen_titles.add(title)

    return unique_articles
