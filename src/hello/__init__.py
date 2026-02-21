"""hello-openclaw: a minimal CLI that greets you by name."""

from __future__ import annotations

import argparse
import sys
import tomllib
from pathlib import Path


def _project_root() -> Path:
    # src/hello/__init__.py -> src/hello -> src -> repo root
    return Path(__file__).resolve().parents[2]


def get_version() -> str:
    """Return the project version as defined in pyproject.toml."""
    pyproject_path = _project_root() / "pyproject.toml"
    with pyproject_path.open("rb") as f:
        data = tomllib.load(f)

    version = data.get("project", {}).get("version")
    if not isinstance(version, str) or not version.strip():
        raise RuntimeError("Could not read [project].version from pyproject.toml")

    return version


def greet(name: str, uppercase: bool = False) -> str:
    """Return a greeting for the given name."""
    greeting = f"Olá, {name}!"
    return greeting.upper() if uppercase else greeting


def main(argv: list[str] | None = None) -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Greet someone by name.")
    parser.add_argument("name", nargs="?", help="Name to greet")
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Print greeting in uppercase",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit",
    )
    args = parser.parse_args(argv)

    if args.version:
        print(get_version())
        return

    if args.name is None:
        parser.error("the following arguments are required: name")

    print(greet(args.name, uppercase=args.uppercase))


__all__ = ["greet", "get_version", "main"]
