"""HTTP helpers for the OpenAI-compatible Furiosa-LLM server."""

import time
from typing import Any

import requests


def health(base_url: str, timeout: float = 5.0) -> dict[str, Any]:
    started = time.perf_counter()
    response = requests.get(f"{base_url.rstrip('/')}/version", timeout=timeout)
    response.raise_for_status()
    return {"status": "ok", "latency_ms": round((time.perf_counter() - started) * 1000, 2), "data": response.json()}


def chat(base_url: str, model: str, prompt: str, api_key: str = "EMPTY", timeout: float = 120.0) -> dict[str, Any]:
    started = time.perf_counter()
    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0, "stream": False},
        timeout=timeout,
    )
    response.raise_for_status()
    return {"latency_ms": round((time.perf_counter() - started) * 1000, 2), "response": response.json()}
