#!/usr/bin/env bash
set -euo pipefail

echo "=== ruff check ==="
ruff check src/ tests/

echo "=== mypy ==="
mypy src/

echo "=== pytest ==="
pytest tests/ -v --tb=short

echo "=== All QA gates passed ==="
