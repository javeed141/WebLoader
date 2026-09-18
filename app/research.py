from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.article_loader import load_articles
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.deduplicator import remove_duplicates
from app.search import search_news


def research_news(query: str) -> dict:
    """Search, read, deduplicate, summarize, and cite recent news."""
    search_results = search_news(query)
    articles = remove_duplicates(load_articles(search_results))

    if not articles:
        return {
            "answer": "No usable articles were found. Try a broader question.",
            "sources": [],
        }

    context = "\n\n".join(
        f"Title: {article.metadata['title']}\n"
        f"Source: {article.metadata['source']}\n"
        f"URL: {article.metadata['url']}\n"
        f"Content: {article.page_content[:5000]}"
        for article in articles
    )

    prompt = ChatPromptTemplate.from_template("""
Answer the question using only the news articles in the context.
Keep the answer concise and factual. Do not make unsupported claims.

<context>
{context}
</context>

Question: {question}
""")

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=0,
    )
    response = llm.invoke(prompt.format(context=context, question=query))

    return {
        "answer": response.content,
        "sources": [
            {
                "title": article.metadata["title"],
                "source": article.metadata["source"],
                "url": article.metadata["url"],
                "published_at": article.metadata["published_at"],
            }
            for article in articles
        ],
    }
