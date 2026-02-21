# hello-openclaw

Minimal Python CLI for testing the OpenClaw/DevClaw pipeline end-to-end.

## Usage

```bash
python src/hello.py João
# Olá, João!

python src/hello.py --uppercase João
# OLÁ, JOÃO!

# Override locale (supported: pt-BR, en-US, es-ES)
python src/hello.py --locale en-US João
# Hello, João!
```

## QA

```bash
bash scripts/qa.sh
```
