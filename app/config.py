import os

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_MODEL = os.getenv("GROQ_MODEL", "openai/gpt-oss-20b")
TOP_K = 5

# Used by WebBaseLoader while it fetches article pages.
os.environ.setdefault("USER_AGENT", "GenAI-News-Research-Assistant/0.1")
