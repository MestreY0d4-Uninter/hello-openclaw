FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install runtime dependency for the Telegram bot.
RUN python -m pip install --no-cache-dir -U pip \
    && python -m pip install --no-cache-dir "python-telegram-bot>=21,<22"

COPY src/ ./src/

# Default command: run the Telegram bot via long polling.
ENV PYTHONPATH=/app/src
CMD ["python", "-m", "telegram_bot"]
