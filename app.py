# -------------------------------------------------
# app/main.py
# -------------------------------------------------
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.research import research_news

app = FastAPI(title="GenAI News Research Assistant")


class ResearchRequest(BaseModel):
    query: str = Field(..., min_length=3, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/news/research")
def news_research(request: ResearchRequest):
    try:
        return research_news(request.query)
    except Exception as err:               # pragma: no cover
        raise HTTPException(status_code=502, detail=str(err)) from err


# -------------------------------------------------
# **Bootstrap block** – lets you run `python3 app/main.py`
# -------------------------------------------------
if __name__ == "__main__":
    import os

    # Render (and many PaaS) expose the port via the $PORT env var.
    # If it is not set (e.g. when you run locally), fall back to 8000.
    port = int(os.getenv("PORT", "8000"))

    # Bind to 0.0.0.0 so external traffic can reach the server.
    # `log_level="info"` gives you nice startup logs.
    import uvicorn

    uvicorn.run(
        "app.main:app",          # module path + FastAPI instance
        host="0.0.0.0",
        port=port,
        log_level="info",
    )