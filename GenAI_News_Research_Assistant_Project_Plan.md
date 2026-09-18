# GenAI News Research Assistant

## 1. Project Goal

Build a simple GenAI-powered news research assistant.

The user asks a natural-language question such as:

- "What is the latest AI news?"
- "What happened with OpenAI recently?"
- "What are the latest developments in AI agents?"
- "Give me the major technology news today."

The Python backend searches the web for recent and relevant news, retrieves the article content, filters duplicate or irrelevant results, and uses an LLM through LangChain to generate a concise factual answer with source links.

The project will be developed **Python-first**. The logic will initially be built and tested in a Jupyter/IPython notebook, then converted into clean Python modules, then exposed through FastAPI, and finally consumed by a React frontend.

---

# 2. Core Idea

```text
User Question
      ↓
Web Search
      ↓
Top K Relevant News Results
      ↓
Article Content Extraction
      ↓
Cleaning + Filtering
      ↓
Duplicate / Similar Article Removal
      ↓
LangChain
      ↓
Groq LLM
      ↓
Concise News Summary
      ↓
Sources + URLs
```

The first version does **not** need to continuously collect every news article on the internet.

It works **on demand**:

> User asks a question → the system searches for relevant recent news → the system summarizes the retrieved information.

---

# 3. Problem Statement

People often need to understand the latest developments around a topic without manually searching through multiple news websites and reading repetitive articles.

This project provides a conversational news research system that searches the web for recent relevant news articles, extracts useful information, removes duplicate or irrelevant results, and uses a Large Language Model to synthesize a concise factual response.

Every response preserves the original article URLs so that users can verify the information.

---

# 4. Example Workflow

### User

```text
What are the latest developments in AI agents?
```

### System

```text
1. Understand the query
2. Create/search for relevant web queries
3. Retrieve top K recent results
4. Collect article URLs and metadata
5. Extract article content
6. Clean the content
7. Remove duplicate/similar articles
8. Send relevant articles to the LLM
9. Generate a concise factual answer
10. Return sources
```

### Example response

```json
{
  "answer": "Several recent developments in AI agents focus on...",
  "key_points": [
    "....",
    "....",
    "...."
  ],
  "sources": [
    {
      "title": "Example article",
      "source": "Example News",
      "url": "https://example.com/article"
    }
  ]
}
```

---

# 5. Technology Stack

## Initial Development

- Python
- Jupyter Notebook / IPython
- Python virtual environment
- LangChain
- Groq
- Web search provider
- Web/article loader

## Backend

- FastAPI
- Pydantic
- Uvicorn

## Vector Search — Later

- Mistral Embeddings
- AstraDB

## Frontend — Later

- React
- Tailwind CSS

---

# 6. Development Philosophy

Build the project in this order:

```text
Python Experiment
       ↓
Working Python Logic
       ↓
Clean Python Modules
       ↓
FastAPI API
       ↓
React Frontend
       ↓
AstraDB / Semantic Search
       ↓
Automation / Production Features
```

Do **not** start by building the React frontend or AstraDB integration.

The first goal is:

> **Make the Python news research pipeline work correctly.**

---

# 7. Project Phases

## Phase 0 — Environment Setup

Create a clean Python environment.

Example:

```bash
python -m venv .venv
```

Activate it and install the initial dependencies.

Initial packages will include the libraries required for:

- LangChain
- Groq
- Web search
- Article/document loading
- Jupyter
- Environment variables

Create:

```text
.env
```

for API keys.

Example:

```env
GROQ_API_KEY=your_key
SEARCH_API_KEY=your_key
```

Never commit `.env` to Git.

---

# 8. Phase 1 — Python Notebook Prototype

This is the **most important first phase**.

Create:

```text
notebooks/
└── news_research.ipynb
```

The notebook will be used to understand and test the entire pipeline.

Do not worry about clean architecture yet.

The objective is simply:

```text
Question
   ↓
Search
   ↓
Articles
   ↓
LLM
   ↓
Answer
```

---

## Phase 1.1 — Test Web Search

Start with a simple query:

```text
latest AI news
```

Inspect the search results.

For every result, identify:

```text
title
url
source
published_at
description
```

Expected result:

```python
[
    {
        "title": "...",
        "url": "...",
        "source": "...",
        "published_at": "...",
        "description": "..."
    }
]
```

---

## Phase 1.2 — Select Top K Results

Initially use a small value:

```python
TOP_K = 5
```

Pipeline:

```text
Search
  ↓
10 results
  ↓
Select top 5
```

Later, ranking can be improved using:

- publication time
- relevance
- source quality
- semantic similarity

---

## Phase 1.3 — Load Article Content

For each selected URL:

```text
URL
 ↓
Article Loader
 ↓
Article Text
```

Extract:

```text
title
content
source
url
published_at
```

Convert the content into LangChain `Document` objects.

Conceptually:

```python
Document(
    page_content="article text...",
    metadata={
        "title": "...",
        "source": "...",
        "url": "...",
        "published_at": "..."
    }
)
```

---

# 9. Phase 2 — Text Cleaning

Raw web pages contain:

- advertisements
- navigation text
- cookie notices
- unrelated links
- HTML
- repeated content

Clean the article content before sending it to the LLM.

Basic pipeline:

```text
Raw Article
     ↓
HTML / Noise Removal
     ↓
Whitespace Normalization
     ↓
Useful Article Text
```

At this stage, keep the processing simple.

---

# 10. Phase 3 — Filtering

The system should remove articles that are:

- too old
- empty
- obviously irrelevant
- invalid
- duplicate URLs

Example:

```text
Search Results
      ↓
Published recently?
      ↓
Relevant to query?
      ↓
Valid article content?
      ↓
Keep
```

Initially, use a simple recency window such as:

```text
Last 24 hours
```

or

```text
Last 7 days
```

depending on the user's query.

---

# 11. Phase 4 — Duplicate Detection

Different websites may report the same event.

Example:

```text
Reuters:
OpenAI announces ...

TechCrunch:
OpenAI announces ...

The Verge:
OpenAI announces ...
```

These may represent the same underlying story.

The system should avoid producing repetitive summaries.

### Version 1

Use simple techniques:

- duplicate URL detection
- normalized title comparison
- basic text similarity

### Version 2

Use embeddings:

```text
Article A ─┐
Article B ─┼──→ Embeddings → Similarity
Article C ─┘
```

Highly similar articles can be grouped or filtered.

---

# 12. Phase 5 — LangChain + Groq

After search and document processing work correctly, integrate the LLM.

Architecture:

```text
User Query
     +
Relevant Articles
     ↓
LangChain Prompt
     ↓
Groq LLM
     ↓
Structured News Answer
```

The LLM should be instructed to:

- answer only from retrieved information
- stay concise
- avoid unsupported claims
- identify important developments
- mention conflicting information when relevant
- preserve source attribution

---

# 13. Phase 6 — Structured Output

The LLM should return structured data rather than only a text paragraph.

Target structure:

```json
{
  "answer": "Concise synthesized answer.",
  "key_points": [
    "Important point 1",
    "Important point 2",
    "Important point 3"
  ],
  "sources": [
    {
      "title": "Article title",
      "source": "Source name",
      "url": "https://example.com"
    }
  ]
}
```

This structure will make the later React integration much easier.

---

# 14. Phase 7 — Convert Notebook into Python Code

Once the notebook works end-to-end, stop adding features inside the notebook.

Convert the working logic into Python modules.

Suggested structure:

```text
news-aggregator/
│
├── app/
│   ├── __init__.py
│   │
│   ├── config.py
│   │
│   ├── models/
│   │   └── news.py
│   │
│   ├── services/
│   │   ├── search.py
│   │   ├── article_loader.py
│   │   ├── cleaner.py
│   │   ├── deduplicator.py
│   │   └── summarizer.py
│   │
│   └── pipeline.py
│
├── notebooks/
│   └── news_research.ipynb
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

The notebook should then become mainly a place for experimentation/testing.

---

# 15. Phase 8 — Create the News Pipeline

Create one central pipeline.

Conceptually:

```python
def research_news(query: str):
    results = search_news(query)
    articles = load_articles(results)
    articles = clean_articles(articles)
    articles = filter_articles(articles)
    articles = remove_duplicates(articles)

    response = summarize_news(
        query=query,
        articles=articles
    )

    return response
```

The goal is to make the entire system callable from one function.

Example:

```python
result = research_news(
    "What are the latest developments in AI agents?"
)
```

---

# 16. Phase 9 — FastAPI

After the Python pipeline is stable, expose it through FastAPI.

Create:

```text
app/
├── main.py
└── routes/
    └── news.py
```

First endpoint:

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

---

# 17. Main API Endpoint

Create:

```http
POST /news/research
```

Request:

```json
{
  "query": "What are the latest developments in AI agents?"
}
```

Response:

```json
{
  "answer": "Several recent developments...",
  "key_points": [
    "...",
    "...",
    "..."
  ],
  "sources": [
    {
      "title": "...",
      "source": "...",
      "url": "..."
    }
  ]
}
```

FastAPI should only handle:

```text
HTTP request
     ↓
Validation
     ↓
Call research_news()
     ↓
Return JSON
```

The actual AI/news logic should remain in the service layer.

---

# 18. Phase 10 — React Frontend

Only after the FastAPI backend works.

React will provide a simple chatbot interface.

Example:

```text
┌──────────────────────────────────────────────┐
│              News Research AI                │
├──────────────────────────────────────────────┤
│                                              │
│ User: What is happening in AI today?        │
│                                              │
│ AI: Several major developments...            │
│                                              │
│ Key Points                                   │
│ • ...                                        │
│ • ...                                        │
│ • ...                                        │
│                                              │
│ Sources                                      │
│ Reuters                                      │
│ TechCrunch                                   │
│ The Verge                                    │
│                                              │
├──────────────────────────────────────────────┤
│ Ask about current news...              [→]  │
└──────────────────────────────────────────────┘
```

React communicates only with:

```text
React
  ↓
POST /news/research
  ↓
FastAPI
  ↓
Python News Pipeline
```

---

# 19. Phase 11 — AstraDB and Embeddings

Only after the basic system works.

Add:

```text
Article
   ↓
Mistral Embedding
   ↓
AstraDB
```

Store:

```text
article_id
title
content
source
url
published_at
category
summary
embedding
```

This allows semantic retrieval.

For example:

```text
User:
"Show me previous news about AI agents."

        ↓

Query Embedding

        ↓

AstraDB

        ↓

Similar Articles

        ↓

LLM

        ↓

Answer
```

This turns the project into a stronger RAG-style application.

---

# 20. Phase 12 — Better News Retrieval

Once the basic version works, improve retrieval.

Possible improvements:

### Recency

Prefer newer articles.

### Relevance

Prefer articles directly related to the query.

### Source quality

Apply configurable source-quality rules.

### Diversity

Avoid returning five articles that all repeat the same story.

Example:

```text
Top 10 Search Results
        ↓
Relevance
        ↓
Recency
        ↓
Duplicate Detection
        ↓
Source Diversity
        ↓
Final 5 Articles
```

---

# 21. Phase 13 — Automation

Later, add scheduled collection if needed.

For example:

```text
Every 30 minutes
       ↓
Search selected topics
       ↓
Process articles
       ↓
Store in AstraDB
```

This is optional.

The core application should remain capable of answering questions on demand.

---

# 22. API Design

Final API can contain:

```text
GET  /health

POST /news/research

GET  /news/latest

GET  /news/category/{category}

GET  /news/search?q=...

GET  /news/{article_id}
```

But **do not build all endpoints immediately**.

Start with:

```text
GET  /health
POST /news/research
```

Add the others when the data model and storage layer are ready.

---

# 23. Final Architecture

The final system can look like:

```text
                         React
                           │
                           ▼
                        FastAPI
                           │
                           ▼
                    News Researcher
                           │
                ┌──────────┴──────────┐
                │                     │
                ▼                     ▼
          Web Search             AstraDB
                │              Semantic Search
                ▼                     │
        Search Results                │
                │                     │
                ▼                     │
        Article Extraction            │
                │                     │
                ▼                     │
        Cleaning / Filtering          │
                │                     │
                └──────────┬──────────┘
                           ▼
                       LangChain
                           │
                           ▼
                        Groq LLM
                           │
                           ▼
                  Structured Response
                           │
                           ▼
                         React
```

---

# 24. What NOT to Build Initially

Avoid these in the first version:

- Continuous news crawling
- Large-scale scraping
- Complex multi-agent architecture
- LangGraph
- Authentication
- User accounts
- Notifications
- Complex dashboards
- Advanced analytics
- Multiple vector databases
- Complex categorization
- Background workers
- Deployment

First make this work:

```text
Question
   ↓
Search
   ↓
Top K Articles
   ↓
Extract
   ↓
Clean
   ↓
Deduplicate
   ↓
LangChain
   ↓
Groq
   ↓
Answer + Sources
```

---

# 25. Definition of Done — Python Version

The first major milestone is complete when this works inside the notebook:

```python
query = "What are the latest developments in AI agents?"

result = research_news(query)

print(result)
```

And produces:

```text
Answer
───────
A concise factual summary...

Key Points
──────────
• ...
• ...
• ...

Sources
───────
• Article 1 — URL
• Article 2 — URL
• Article 3 — URL
```

At this point:

> **The GenAI part of the project is working.**

Then convert it into clean Python modules.

Then FastAPI.

Then React.

Then AstraDB/semantic retrieval.

---

# 26. Recommended Build Order

Follow this exact order:

```text
STEP 1
Create Python environment
        ↓
STEP 2
Create Jupyter/IPython notebook
        ↓
STEP 3
Test web search
        ↓
STEP 4
Retrieve top K results
        ↓
STEP 5
Load article content
        ↓
STEP 6
Clean article text
        ↓
STEP 7
Filter recent/relevant articles
        ↓
STEP 8
Remove duplicates
        ↓
STEP 9
Connect LangChain + Groq
        ↓
STEP 10
Generate factual summaries
        ↓
STEP 11
Return structured output
        ↓
STEP 12
Convert notebook → Python modules
        ↓
STEP 13
Create FastAPI
        ↓
STEP 14
Expose /news/research
        ↓
STEP 15
Connect React
        ↓
STEP 16
Add embeddings
        ↓
STEP 17
Add AstraDB
        ↓
STEP 18
Add semantic search / RAG
        ↓
STEP 19
Add caching, retries and automation
```

---

# 27. MVP vs Future Version

## MVP

```text
Python
+
LangChain
+
Web Search
+
Article Loader
+
Groq
+
FastAPI
```

Features:

- Ask a news question
- Search recent news
- Retrieve top K articles
- Extract article content
- Remove basic duplicates
- Summarize
- Return sources

## Advanced Version

```text
Python
+
LangChain
+
Groq
+
Web Search
+
Mistral Embeddings
+
AstraDB
+
FastAPI
+
React
```

Additional features:

- Semantic search
- Persistent article storage
- RAG
- Better duplicate detection
- Topic/category filtering
- Search history
- Caching
- Scheduled collection
- Source-quality rules
- Production monitoring

---

# 28. One-Line Project Description

> **A conversational GenAI news research assistant that searches the web for recent articles, retrieves and processes relevant content, and uses LangChain and an LLM to generate concise, source-backed answers to user queries.**

---

# 29. Main Goal for the First Week

Do not worry about the complete application.

Your immediate goal is only:

```text
Jupyter Notebook

User Query
    ↓
Web Search
    ↓
Top 5 Articles
    ↓
Article Content
    ↓
Clean Text
    ↓
LangChain
    ↓
Groq
    ↓
Summary + Sources
```

Once this works reliably, the rest of the project becomes an engineering/refactoring task rather than an unclear AI experiment.
