"""Telegram bot entrypoint for hello-openclaw.

This module is intentionally written so importing it does not require
`python-telegram-bot` to be installed. The dependency is imported only when
`main()` is executed.
"""

from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass

from hello import greet, map_telegram_language_code


LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class EffectiveUser:
    first_name: str | None = None
    full_name: str | None = None
    language_code: str | None = None


def choose_name(command_arg: str | None, user: EffectiveUser) -> str:
    """Pick a display name based on command argument and Telegram profile."""

    if command_arg is not None:
        candidate = command_arg.strip()
        if candidate:
            return candidate

    if user.first_name:
        return user.first_name
    if user.full_name:
        return user.full_name

    # Extremely defensive fallback: Telegram usually provides at least one of them.
    return "there"


def is_greeting_trigger(text: str) -> bool:
    """Return True if message should trigger an automatic greeting."""

    normalized = text.strip().casefold()
    return normalized in {"oi", "olá"}


async def _send_greeting(update: object, context: object, *, name: str) -> None:
    """Send greeting in the same chat, handling API failures gracefully."""

    # Import inside function to keep module importable without dependency.
    from telegram.error import TelegramError  # type: ignore[import-not-found]

    # Duck-typing the objects from python-telegram-bot.
    user_lang = getattr(getattr(update, "effective_user", None), "language_code", None)
    locale = map_telegram_language_code(user_lang)

    text = greet(name, locale=locale)

    try:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    except TelegramError:
        LOGGER.exception("Telegram API error while sending message")


async def hello_command(update: object, context: object) -> None:
    args = getattr(context, "args", [])
    command_arg = " ".join(args) if args else None

    user = getattr(update, "effective_user", None)
    effective = EffectiveUser(
        first_name=getattr(user, "first_name", None),
        full_name=getattr(user, "full_name", None),
        language_code=getattr(user, "language_code", None),
    )

    name = choose_name(command_arg, effective)
    await _send_greeting(update, context, name=name)


async def text_message(update: object, context: object) -> None:
    message = getattr(update, "message", None)
    text = getattr(message, "text", None)
    if not isinstance(text, str):
        return

    if not is_greeting_trigger(text):
        return

    user = getattr(update, "effective_user", None)
    effective = EffectiveUser(
        first_name=getattr(user, "first_name", None),
        full_name=getattr(user, "full_name", None),
        language_code=getattr(user, "language_code", None),
    )
    name = choose_name(None, effective)
    await _send_greeting(update, context, name=name)


def main() -> None:
    """Run the bot using long polling."""

    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN is required")

    logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

    # Import inside main to avoid hard dependency on import.
    from telegram.ext import (  # type: ignore[import-not-found]
        Application,
        CommandHandler,
        MessageHandler,
        filters,
    )

    async def on_error(update: object, context: object) -> None:  # pragma: no cover
        LOGGER.exception("Unhandled error while processing update")

        # Avoid hot-looping on repeated failures; a small backoff helps.
        await asyncio.sleep(1)

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("hello", hello_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_message))
    app.add_error_handler(on_error)

    # python-telegram-bot already implements robust polling with retry.
    app.run_polling(close_loop=False)


if __name__ == "__main__":
    main()
