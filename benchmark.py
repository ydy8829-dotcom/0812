"""Run the same prompt against an OpenAI-compatible endpoint."""

import argparse
import json
import time

import requests


def run_once(base_url: str, model: str, prompt: str, api_key: str) -> dict:
    started = time.perf_counter()
    response = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": [{"role": "user", "content": prompt}], "temperature": 0},
        timeout=180,
    )
    response.raise_for_status()
    usage = response.json().get("usage", {})
    return {"latency_ms": round((time.perf_counter() - started) * 1000, 2), "prompt_tokens": usage.get("prompt_tokens"), "completion_tokens": usage.get("completion_tokens"), "total_tokens": usage.get("total_tokens")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="furiosa")
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="EMPTY")
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    prompt = "Create a concise three-step plan for preparing a technical interview."
    results = [run_once(args.base_url, args.model, prompt, args.api_key) for _ in range(args.runs)]
    output = {"provider": args.provider, "model": args.model, "runs": results, "avg_latency_ms": round(sum(x["latency_ms"] for x in results) / len(results), 2)}
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
