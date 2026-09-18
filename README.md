# GenAI News Research Assistant

This backend searches recent news with Tavily, loads article pages, removes duplicate titles, and uses Groq through LangChain to produce a source-backed answer.

## Required `.env` values

```env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

Optional:

```env
GROQ_MODEL=openai/gpt-oss-20b
```

## Run the API

```bash
conda activate ai-rag-project
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for the interactive API documentation.

## Test the API

```bash
curl -X POST http://127.0.0.1:8000/news/research \
  -H "Content-Type: application/json" \
  -d '{"query":"What are the latest developments in AI agents?"}'
```
