from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

from app.article_loader import load_articles
from app.config import GROQ_API_KEY, GROQ_MODEL
from app.deduplicator import remove_duplicates
from app.search import search_news


async def research_news(query: str) -> dict:
    """Search, read, deduplicate, summarize, and cite recent news."""
    MAX_ARTICLES = 5
    MAX_CHARS_PER_ARTICLE = 1500

    # 1️⃣ Search for recent news
    search_results = search_news(query)
    print(f"[DEBUG] search_results count: {len(search_results)}")

    # 2️⃣ Load articles asynchronously
    loaded = await load_articles(search_results)
    articles = remove_duplicates(loaded)[:MAX_ARTICLES]
    print(f"[DEBUG] usable articles after dedup: {len(articles)}")

    if not articles:
        return {"answer": "No usable articles were found. Try a broader question.", "sources": []}

    # 3️⃣ Build context for the LLM
    context = "\n\n".join(
        f"Title: {article.metadata['title']}\n"
        f"Source: {article.metadata['source']}\n"
        f"URL: {article.metadata['url']}\n"
        f"Content: {article.page_content[:MAX_CHARS_PER_ARTICLE]}"
        for article in articles
    )
    print(f"[DEBUG] context chars: {len(context)}")

    # 4️⃣ Ask the LLM
    prompt = ChatPromptTemplate.from_template("""
You are a careful news research assistant.
Answer the question using only the news articles in the context below.

Requirements:
- Base the answer only on the provided articles.
- Do not invent facts, dates, or claims.
- Write a well-structured answer with a clear summary, the key evidence, and a short conclusion.
- Give a medium-length response, roughly 2-5 paragraphs or a concise but informative structured summary.
- If the articles do not support a clear answer, say that clearly and explain what evidence is missing.
- Mention the main sources and patterns in the reporting when relevant.

<context>
{context}
</context>

Question: {question}
""")

    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name=GROQ_MODEL,
        temperature=0.2,
        max_tokens=500,
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
