import os
from fastapi import APIRouter
from pydantic import BaseModel

from app.cache import redis_client

# LangChain
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

router = APIRouter(prefix="/ai", tags=["ai"])

# Expostos em nível de módulo para facilitar mocking nos testes
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "nokey")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

llm = ChatOpenAI(api_key=OPENAI_API_KEY, model=OPENAI_MODEL, temperature=0)
prompt = ChatPromptTemplate.from_template("Responda de forma objetiva e correta: {q}")
chain = prompt | llm  # permite monkeypatch no teste

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    cached: bool

@router.post("/ask", response_model=AskResponse)
def ask_ai(payload: AskRequest):
    q = payload.question.strip()
    cache_key = f"ai:{q}"
    cached = redis_client.get(cache_key)
    if cached:
        return AskResponse(answer=cached, cached=True)

    # Chamada ao LLM (ou mock em testes)
    result = chain.invoke({"q": q})
    answer = getattr(result, "content", str(result))

    redis_client.set(cache_key, answer, ex=60)  # cache 60s
    return AskResponse(answer=answer, cached=False)
