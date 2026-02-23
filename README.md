# hello-openclaw

Bot/CLI minimal em Python para testar o pipeline OpenClaw/DevClaw.

## Pré-requisitos

- Python 3.11+
- (Para o bot) um token via **@BotFather** no Telegram

## Como obter o token do bot (Telegram)

1. No Telegram, fale com **@BotFather**
2. Execute `/newbot` e siga as instruções
3. Copie o token gerado e exporte como variável de ambiente:

```bash
export TELEGRAM_BOT_TOKEN="<seu_token_aqui>"
```

## Rodar localmente (long polling)

Instale a dependência do bot:

```bash
python -m pip install -U python-telegram-bot
```

Execute:

```bash
PYTHONPATH=src python -m telegram_bot
```

### Comandos e mensagens

- `/hello <nome>` → responde com saudação personalizada no idioma do usuário
- `/hello` (sem nome) → usa o nome do perfil do Telegram (fallback)
- Mensagens com **exatamente** `oi` ou `olá` (trim + case-insensitive) → responde com saudação

O idioma é escolhido por `language_code` do Telegram (prefix match):

- `pt*` → `pt-BR`
- `en*` → `en-US`
- `es*` → `es-ES`
- caso contrário → `en-US`

As strings visíveis ao usuário passam por gettext e reutilizam os catálogos em `src/locales/`.

## CLI (opcional)

```bash
python src/hello.py João
# Olá, João!

python src/hello.py --uppercase João
# OLÁ, JOÃO!

# Override locale (supported: pt-BR, en-US, es-ES)
python src/hello.py --locale en-US João
# Hello, João!
```

## Docker

Build:

```bash
docker build -t hello-openclaw:local .
```

Run:

```bash
docker run --rm -e TELEGRAM_BOT_TOKEN="$TELEGRAM_BOT_TOKEN" hello-openclaw:local
```

## QA

```bash
bash scripts/qa.sh
```
