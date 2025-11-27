#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root (script may be run from anywhere)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "[prep_eval] Ensuring eval cache directories exist..."
mkdir -p .evalcache
mkdir -p evals/results

echo "[prep_eval] Optionally checking API health on :8000..."
if curl -sSf http://localhost:8000/health >/dev/null 2>&1; then
  echo "[prep_eval] API is healthy."
else
  echo "[prep_eval] API not healthy yet, waiting up to 30s..."
  for i in {1..30}; do
    if curl -sSf http://localhost:8000/health >/dev/null 2>&1; then
      echo "[prep_eval] API is healthy."
      break
    fi
    sleep 1
  done
fi

echo "[prep_eval] Done."
