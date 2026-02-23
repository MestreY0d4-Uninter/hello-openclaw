#!/usr/bin/env bash
set -euo pipefail

# Local-first QA entrypoint.
# Prefer running via `uv` to avoid depending on system pip/ensurepip.

if command -v uv >/dev/null 2>&1; then
  RUN=(uv run --)
else
  RUN=(python -m)
fi

echo "=== ruff check ==="
"${RUN[@]}" ruff check src/ tests/

echo "=== mypy ==="
"${RUN[@]}" mypy src/

echo "=== unit tests (with coverage >= 80%) ==="
"${RUN[@]}" coverage run -m unittest -v
"${RUN[@]}" coverage report --fail-under=80

echo "=== All QA gates passed ==="
