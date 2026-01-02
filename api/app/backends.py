import main
import os
import httpx

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")


def model_backend(prompt: str, policy: str | None = None) -> str:
    if main.violates_policy(prompt):
        return "I can’t assist with that."

    try:
        r = httpx.post(
            f"{OLLAMA_BASE_URL}/api/generate",
            json={"model": OLLAMA_MODEL, "prompt": prompt},
            timeout=60.0,
        )
        r.raise_for_status()
    except Exception as e:
        return f"[backend-error] {e}"

    return r.json().get("response", "")
