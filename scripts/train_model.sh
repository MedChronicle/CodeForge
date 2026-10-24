#!/usr/bin/env bash
set -euo pipefail
python -m backend.ml.train
python -m backend.ml.evaluate
