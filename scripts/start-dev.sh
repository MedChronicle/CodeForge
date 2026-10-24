#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -x ".venv/bin/uvicorn" ]]; then
  printf '%s\n' "Missing .venv/bin/uvicorn. Run: python3.12 -m venv .venv && .venv/bin/pip install -r backend/requirements.txt" >&2
  exit 1
fi

if [[ ! -d "frontend/node_modules" ]]; then
  printf '%s\n' "Missing frontend/node_modules. Run: cd frontend && npm install" >&2
  exit 1
fi

if [[ ! -f ".env" ]]; then
  cp .env.example .env
fi

if [[ ! -f "algoforge.db" ]]; then
  .venv/bin/python -m backend.seed.seed_data
fi

if [[ ! -f "backend/ml/artifacts/skill_estimator.joblib" ]]; then
  .venv/bin/python -m backend.ml.train
fi

cleanup() {
  kill "$API_PID" "$FRONTEND_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

.venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload > /tmp/algoforge-api.log 2>&1 &
API_PID=$!

(cd frontend && npm run dev -- --host 127.0.0.1) > /tmp/algoforge-frontend.log 2>&1 &
FRONTEND_PID=$!

sleep 2
printf '%s\n' "AlgoForge API: http://127.0.0.1:8000"
printf '%s\n' "AlgoForge frontend: see /tmp/algoforge-frontend.log for the selected Vite URL"
printf '%s\n' "Press Ctrl+C to stop both servers."

wait "$API_PID" "$FRONTEND_PID"
