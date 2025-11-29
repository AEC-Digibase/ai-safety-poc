import httpx
import main

def model_backend(prompt: str, policy: str | None = None) -> str:
    # Keep your existing policy checks
    if main.violates_policy(prompt):
        return "I can’t assist with that."

    try:
        r = httpx.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3:8b", "prompt": prompt},
            timeout=60.0,
        )
        r.raise_for_status()
    except Exception as e:
        return f"[backend-error] {e}"

    # Ollama returns JSON like {"model": "...", "created_at": "...", "response": "..."}
    return r.json().get("response", "")
