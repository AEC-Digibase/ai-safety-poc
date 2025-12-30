#!/usr/bin/env bash
set -euo pipefail

# Ensure eval cache directories exist inside the container
mkdir -p /app/.evalcache
mkdir -p /app/evals/results

echo "[entrypoint] Prepared .evalcache and evals/results"
ls -ltr

# Hand off to the original API runner
exec bash ./api/run.sh
