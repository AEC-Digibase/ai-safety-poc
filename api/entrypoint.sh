#!/usr/bin/env bash
set -euo pipefail

# Ensure eval cache directories exist inside the container
mkdir -p /app/.evalcache
mkdir -p /app/evals/results

echo "[entrypoint] Prepared .evalcache and evals/results"

# Hand off to the original API runner
exec bash /app/api/run.sh
