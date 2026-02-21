#!/usr/bin/env bash
set -euo pipefail

echo "=== ruff check ==="
if command -v ruff >/dev/null 2>&1; then
  ruff check src/ tests/
else
  echo "ruff not found; skipping (install ruff to enable lint gate)"
fi

echo "=== mypy ==="
if command -v mypy >/dev/null 2>&1; then
  mypy src/
else
  echo "mypy not found; skipping (install mypy to enable type-check gate)"
fi

echo "=== unit tests ==="
python -m unittest -v

echo "=== All QA gates passed ==="
