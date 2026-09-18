# uvicorn app.main:app --reload
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

from app.research import research_news

app = FastAPI(title="GenAI News Research Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://rag-react-fronted-beige.vercel.app",
    ],
    allow_origin_regex=r"https://rag-react-fronted(?:-[a-z0-9-]+)?\.vercel\.app",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

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
