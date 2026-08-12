import os
from dotenv import load_dotenv

load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai").lower()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
FURIOSA_BASE_URL = os.getenv("FURIOSA_BASE_URL", "http://localhost:8000/v1")
FURIOSA_API_KEY = os.getenv("FURIOSA_API_KEY", "EMPTY")
FURIOSA_MODEL = os.getenv("FURIOSA_MODEL", "EMPTY")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OPENAI_COMPATIBLE_BASE_URL = os.getenv("OPENAI_COMPATIBLE_BASE_URL", "")
OPENAI_COMPATIBLE_API_KEY = os.getenv("OPENAI_COMPATIBLE_API_KEY", "")
MOCK_LLM = os.getenv("MOCK_LLM", "true").lower() == "true"
