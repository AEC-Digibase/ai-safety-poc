from fastapi import FastAPI, Request, Response
from pydantic import BaseModel
from typing import Optional
import re, time, uuid
from prometheus_client import Counter, Summary, Gauge, \
CollectorRegistry, generate_latest, CONTENT_TYPE_LATEST

app = FastAPI(title="ai-sut", version="0.1.0")

# --- Metrics ---
PROMPTS_TOTAL = Counter('prompts_total', 'Total prompts')
JAILBREAK_SUCCESS = Counter('jailbreak_success_total', 'Jailbreak success events')
PII_REDACTIONS = Counter('pii_redactions_total', 'PII redactions performed')
LATENCY = Summary('generation_latency_seconds', 'Latency for /generate')

# --- Simple PII scrubber ---
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
SSN_RE = re.compile(r"\b\d{3}-\d{2}-\d{4}\b")
class GenRequest(BaseModel):
    prompt: str
    system: Optional[str] = None
    policy: Optional[str] = None
@app.get("/health")
def health():
    return {"ok": True}
@app.get("/version")
def version():
    return {"version": app.version}
@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
@LATENCY.time()
@app.post("/generate")
async def generate(req: GenRequest):
    PROMPTS_TOTAL.inc()
    # PII scrub in prompt (demo)
    prompt = EMAIL_RE.sub("<EMAIL>", req.prompt)
    new_prompt = SSN_RE.sub("<SSN>", prompt)
    if new_prompt != req.prompt:
        PII_REDACTIONS.inc()
    prompt = new_prompt
    # --- MODEL BACKEND (start with a safe stub) ---
    # Replace this block with a call to a real local model later
    output = safe_stub(prompt, policy=req.policy)
    return {
        "id": str(uuid.uuid4()),
        "model": "stub-0.1",
        "input": prompt,
        "output": output,
    }
# --- A minimal refusal/guardrail policy ---
BANNED = ["how to make a bomb", "how to hack", "ssn", "credit card"]
def violates_policy(text: str) -> bool:
    low = text.lower()
    return any(b in low for b in BANNED)

def safe_stub(prompt: str, policy: str | None = None) -> str:
    if violates_policy(prompt):
        return "I can’t assist with that."
    # echoy stub + light instruction following
    if prompt.strip().endswith("?"):
        return "Here’s a concise, safe answer: (stub)"
    return "Acknowledged. (stub)"
