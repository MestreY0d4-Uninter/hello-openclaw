"""Tests for hello-openclaw CLI.

Uses the stdlib `unittest` module to keep the project dependency-free.
"""

from __future__ import annotations

import io
import sys
import unittest
from contextlib import redirect_stdout

sys.path.insert(0, "src")

from hello import greet, main  # noqa: E402


class TestHello(unittest.TestCase):
    def test_greet_basic(self) -> None:
        self.assertEqual(greet("João"), "Olá, João!")

    def test_greet_ascii_name(self) -> None:
        self.assertEqual(greet("World"), "Olá, World!")

    def test_greet_uppercase(self) -> None:
        self.assertEqual(greet("João", uppercase=True), "OLÁ, JOÃO!")

    def test_main_prints_greeting(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["Maria"])
        self.assertEqual(buf.getvalue().strip(), "Olá, Maria!")

    def test_main_prints_uppercase_greeting(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            main(["--uppercase", "João"])
        self.assertEqual(buf.getvalue().strip(), "OLÁ, JOÃO!")


if __name__ == "__main__":
    unittest.main()
