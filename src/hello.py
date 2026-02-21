"""hello-openclaw: a minimal CLI that greets you by name."""

from __future__ import annotations

import argparse
import sys


def greet(name: str, uppercase: bool = False) -> str:
    """Return a greeting for the given name."""
    greeting = f"Olá, {name}!"
    return greeting.upper() if uppercase else greeting


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Greet someone by name.")
    parser.add_argument("name", help="Name to greet")
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Print greeting in uppercase",
    )
    args = parser.parse_args(argv)

    print(greet(args.name, uppercase=args.uppercase))


if __name__ == "__main__":
    main()
