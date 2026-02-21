"""hello-openclaw: a minimal CLI that greets you by name."""

from __future__ import annotations

import argparse
import sys


def greet(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Olá, {name}!"


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Greet someone by name.")
    parser.add_argument("name", help="Name to greet")
    args = parser.parse_args(argv)

    print(greet(args.name))


if __name__ == "__main__":
    main()
