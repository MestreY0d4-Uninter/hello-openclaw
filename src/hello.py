"""hello-openclaw: a minimal CLI that greets you by name."""

from __future__ import annotations

import argparse
import gettext
import os
from typing import Mapping


DOMAIN = "hello-openclaw"
SUPPORTED_LOCALES: tuple[str, ...] = ("pt-BR", "en-US", "es-ES")


def map_telegram_language_code(language_code: str | None) -> str:
    """Map Telegram `language_code` to a supported locale.

    Uses prefix matching:
    - pt* -> pt-BR
    - en* -> en-US
    - es* -> es-ES
    - otherwise -> en-US (fallback)

    Telegram may send values like: "pt-br", "en", "es-ES".
    """

    if not language_code:
        return "en-US"

    return map_locale(language_code)


def detect_system_locale(env: Mapping[str, str] | None = None) -> str | None:
    """Detect locale from env vars.

    Priority order: LC_ALL > LC_MESSAGES > LANG.

    Returns the raw locale string (e.g. "pt_BR.UTF-8") or None if not set.
    """

    if env is None:
        env = os.environ

    for key in ("LC_ALL", "LC_MESSAGES", "LANG"):
        value = env.get(key)
        if value:
            return value

    return None


def map_locale(raw_locale: str) -> str:
    """Map a raw locale string to a supported locale.

    Uses prefix matching:
    - pt-* -> pt-BR
    - en-* -> en-US
    - es-* -> es-ES
    - otherwise -> en-US (fallback)
    """

    normalized = raw_locale.split(".", 1)[0].strip().lower().replace("_", "-")

    if normalized == "pt" or normalized.startswith("pt-"):
        return "pt-BR"
    if normalized == "en" or normalized.startswith("en-"):
        return "en-US"
    if normalized == "es" or normalized.startswith("es-"):
        return "es-ES"

    return "en-US"


def select_locale(
    *,
    override: str | None,
    env: Mapping[str, str] | None = None,
) -> str:
    """Select the effective locale.

    Rules:
    - If override is provided, it wins.
    - Else if no locale can be detected, default to pt-BR.
    - Else map detected locale via prefix match with fallback en-US.
    """

    if override is not None:
        return override

    raw = detect_system_locale(env)
    if raw is None:
        return "pt-BR"

    return map_locale(raw)


def get_translator(locale: str) -> gettext.NullTranslations:
    """Load gettext translations for the given locale."""

    localedir = os.path.join(os.path.dirname(__file__), "locales")
    return gettext.translation(DOMAIN, localedir=localedir, languages=[locale], fallback=True)


def greet(name: str, uppercase: bool = False, *, locale: str = "pt-BR") -> str:
    """Return a localized greeting for the given name."""

    _ = get_translator(locale).gettext
    greeting = _("Hello, %(name)s!") % {"name": name}
    return greeting.upper() if uppercase else greeting


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""

    # Two-phase parsing: first read --locale (without triggering --help), then build the
    # fully localized parser.
    pre_parser = argparse.ArgumentParser(add_help=False)
    pre_parser.add_argument("--locale", choices=SUPPORTED_LOCALES)
    pre_args, _unknown = pre_parser.parse_known_args(argv)

    locale = select_locale(override=pre_args.locale)

    _ = get_translator(locale).gettext
    parser = argparse.ArgumentParser(description=_("Greet someone by name."))
    parser.add_argument("name", help=_("Name to greet"))
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help=_("Print greeting in uppercase"),
    )
    parser.add_argument(
        "--locale",
        choices=SUPPORTED_LOCALES,
        help=_("Override locale. Supported: %(locales)s")
        % {"locales": ", ".join(SUPPORTED_LOCALES)},
    )

    args = parser.parse_args(argv)
    print(greet(args.name, uppercase=args.uppercase, locale=locale))


if __name__ == "__main__":
    main()
