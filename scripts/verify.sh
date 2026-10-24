#!/usr/bin/env bash
set -euo pipefail

python3 -m compileall -q backend
python3 -m pytest -q backend/tests
cd frontend
npm run typecheck
npm run test -- --run
npm run build
