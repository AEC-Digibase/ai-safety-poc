#!/usr/bin/env bash
cd ./api/app
set -euo pipefail
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1