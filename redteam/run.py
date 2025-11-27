import json
import time
from pathlib import Path
from typing import TypedDict, List

import httpx
import yaml

API = "http://localhost:8000/generate"


class RedteamRow(TypedDict):
    prompt: str
    output: str


def main() -> None:
    with open("redteam/session-001.yaml", "r") as f:
        sess = yaml.safe_load(f)

    rows: List[RedteamRow] = []

    with httpx.Client(timeout=30.0) as client:
        for item in sess["items"]:
            prompt_text: str = item["prompt"]["text"]  # adjust if your YAML uses a different shape
            resp = client.post(API, json={"prompt": prompt_text})
            resp.raise_for_status()
            output_text: str = resp.json()["output"]
            rows.append({"prompt": prompt_text, "output": output_text})

    Path("docs").mkdir(exist_ok=True)
    fn = f"docs/redteam-rt001-{int(time.time())}.jsonl"

    with open(fn, "w") as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")

    print(fn)


if __name__ == "__main__":
    main()
