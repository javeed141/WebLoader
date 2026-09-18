from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.research import research_news

app = FastAPI(title="GenAI News Research Assistant")


class ResearchRequest(BaseModel):
    query: str = Field(min_length=3, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/news/research")
def news_research(request: ResearchRequest):
    try:
        return research_news(request.query)
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
