from typing import Type, TypeVar
from config import *
from schemas import IntentResult, ActionItem

T = TypeVar("T")

def get_llm():
    if LLM_PROVIDER == "ollama":
        from langchain_ollama import ChatOllama
        return ChatOllama(model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=0)
    if LLM_PROVIDER == "furiosa":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=FURIOSA_MODEL, api_key=FURIOSA_API_KEY, base_url=FURIOSA_BASE_URL, temperature=0)
    from langchain_openai import ChatOpenAI
    kwargs = {"model": OPENAI_MODEL, "api_key": OPENAI_API_KEY, "temperature": 0}
    if OPENAI_COMPATIBLE_BASE_URL:
        kwargs["base_url"] = OPENAI_COMPATIBLE_BASE_URL
        kwargs["api_key"] = OPENAI_COMPATIBLE_API_KEY or OPENAI_API_KEY
    return ChatOpenAI(**kwargs)

def structured_invoke(prompt: str, schema: Type[T], fallback: T) -> T:
    if MOCK_LLM:
        return fallback
    try:
        return get_llm().with_structured_output(schema).invoke(prompt)
    except Exception:
        return fallback
