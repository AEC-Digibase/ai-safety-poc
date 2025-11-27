from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, Iterable, List


# Map suite name -> list of numeric scores
ScoresBySuite = DefaultDict[str, List[float]]


def load_scores(path: str) -> ScoresBySuite:
    """Load per-suite scores from a JSONL results file."""
    scores: ScoresBySuite = defaultdict(list)

    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            row = json.loads(line)

            suite_name = str(row["suite"])
            score_value = float(row["score"])

            scores[suite_name].append(score_value)

    return scores


def pct(values: Iterable[float]) -> str:
    """Return percentage string for a collection of scores."""
    total = 0.0
    count = 0

    for v in values:
        total += v
        count += 1

    denom = max(1, count)
    return f"{100 * total / denom:.1f}%"


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/summarize.py <results.jsonl>")

    path = sys.argv[1]
    scores = load_scores(path)

    lines: List[str] = ["# Eval Summary\n"]
    for suite_name, values in scores.items():
        lines.append(f"- {suite_name}: {pct(values)}")

    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)

    out_path = docs_dir / "eval-summary.md"
    out_path.write_text("\n".join(lines))

    print(str(out_path))


if __name__ == "__main__":
    main()
