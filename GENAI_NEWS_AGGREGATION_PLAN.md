# GenAI News Aggregation and Summarization System

## Project Definition

Build a Python backend that automatically collects current news from reliable web sources, removes duplicate or irrelevant articles, categorizes the remaining news, and produces concise AI-generated summaries.

The system will use LangChain for document processing, retrieval, prompt orchestration, and LLM integration. It will not use LangGraph. The frontend will be added later.

The backend should return structured, categorized news data that a React dashboard can consume through REST APIs.

## Core Problem

News is published continuously across many sources, making it difficult to quickly find relevant, reliable updates without reading repetitive articles. The system should consolidate articles from selected sources, identify important stories, group similar coverage, and generate short factual summaries with source links.

## Main Features

- Collect articles from configured RSS feeds, news APIs, or approved websites.
- Extract title, source, URL, publication time, category, and full article text.
- Remove duplicate or near-duplicate articles.
- Filter articles by selected topics, keywords, language, and recency.
- Categorize news into Technology, Business, Sports, Politics, Science, Entertainment, and other categories.
- Generate a concise summary for each story using an LLM.
- Preserve source URLs so every summary is traceable.
- Store articles, embeddings, summaries, and metadata in a database/vector store.
- Expose REST endpoints for latest news, news by category, semantic search, and article details.

## Proposed LangChain-Only Architecture

```text
News Sources
    ↓
Loader / RSS / API Collector
    ↓
Text Cleaning + Metadata Extraction
    ↓
Duplicate Detection + Relevance Filtering
    ↓
Embeddings + AstraDB Vector Store
    ↓
Topic Categorization
    ↓
LangChain Summarization Chain
    ↓
Structured JSON Output
    ↓
FastAPI REST API
    ↓
React Frontend Later
```

## Development Plan

### Phase 1 — Project Foundation

- Create a clean backend structure.
- Configure `.env` for API keys.
- Set up FastAPI.
- Define article data models.
- Add logging and error handling.

Expected output: a running API with a health-check endpoint.

### Phase 2 — News Collection

- Start with RSS feeds because they are simple and reliable.
- Add selected sources, for example BBC, Reuters, The Verge, TechCrunch, or Google News RSS.
- Extract title, URL, source, published date, short description, and article text.
- Store raw collected articles.

Expected output: `POST /news/collect` fetches and returns raw articles.

### Phase 3 — Processing and Filtering

- Clean HTML and normalize article text.
- Filter articles by time range, such as the last 24 hours.
- Remove exact duplicate URLs.
- Detect near-duplicate stories using embeddings and similarity search.
- Keep only relevant articles based on selected topics.

Expected output: clean, unique, relevant article records.

### Phase 4 — AstraDB Vector Search

- Generate Mistral embeddings for article content.
- Store articles and metadata in AstraDB.
- Use metadata such as `source`, `category`, `published_at`, and `url`.
- Add semantic search, for example: "latest AI regulation news."

Expected output: `GET /news/search?q=AI+regulation` returns semantically relevant articles.

### Phase 5 — LangChain Summarization and Categorization

- Use a Groq-hosted LLM through LangChain.
- Categorize each article.
- Generate a short factual summary.
- Return structured output.

```json
{
  "title": "Example AI News",
  "category": "Technology",
  "summary": "A short factual summary of the article.",
  "source": "Reuters",
  "url": "https://example.com/article",
  "published_at": "2026-09-18T10:30:00Z"
}
```

Expected output: summarized, categorized articles with traceable sources.

### Phase 6 — REST API

Create endpoints such as:

```text
GET /health
POST /news/collect
GET /news/latest
GET /news/category/{category}
GET /news/search?q=...
GET /news/{article_id}
```

Expected output: a backend ready for a future React dashboard.

### Phase 7 — Scaling and Automation

- Run collection on a schedule.
- Cache summaries to avoid repeated LLM calls.
- Add rate limiting and retries for news sources and LLM APIs.
- Track failures and collection history.
- Add source-quality rules.
- Deploy the API and database configuration securely.

## Starting Point

Begin with Phase 1 and Phase 2: FastAPI plus RSS-based news collection. This provides real news data before adding embeddings, AstraDB, and summarization.
