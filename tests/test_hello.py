"""Tests for hello-openclaw CLI."""

from __future__ import annotations

import sys

import pytest

sys.path.insert(0, "src")

from hello import greet, main


def test_greet_basic() -> None:
    assert greet("João") == "Olá, João!"


def test_greet_ascii_name() -> None:
    assert greet("World") == "Olá, World!"


def test_main_prints_greeting(capsys: pytest.CaptureFixture[str]) -> None:
    main(["Maria"])
    captured = capsys.readouterr()
    assert captured.out.strip() == "Olá, Maria!"
