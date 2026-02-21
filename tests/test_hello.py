"""Tests for hello-openclaw CLI.

Uses the stdlib `unittest` module to keep the project dependency-free.
"""

from __future__ import annotations

import io
import os
import sys
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

sys.path.insert(0, "src")

from hello import (
    detect_system_locale,
    greet,
    main,
    map_locale,
    select_locale,
)  # noqa: E402


class TestHello(unittest.TestCase):
    def test_greet_basic_default_pt_br(self) -> None:
        self.assertEqual(greet("João"), "Olá, João!")

    def test_greet_ascii_name_default_pt_br(self) -> None:
        self.assertEqual(greet("World"), "Olá, World!")

    def test_greet_uppercase_default_pt_br(self) -> None:
        self.assertEqual(greet("João", uppercase=True), "OLÁ, JOÃO!")

    def test_greet_in_english(self) -> None:
        self.assertEqual(greet("World", locale="en-US"), "Hello, World!")

    def test_greet_in_spanish(self) -> None:
        self.assertEqual(greet("Mundo", locale="es-ES"), "¡Hola, Mundo!")

    def test_main_prints_greeting(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            with patch.dict(os.environ, {}, clear=True):
                main(["Maria"])
        self.assertEqual(buf.getvalue().strip(), "Olá, Maria!")

    def test_main_prints_uppercase_greeting(self) -> None:
        buf = io.StringIO()
        with redirect_stdout(buf):
            with patch.dict(os.environ, {}, clear=True):
                main(["--uppercase", "João"])
        self.assertEqual(buf.getvalue().strip(), "OLÁ, JOÃO!")

    def test_detect_system_locale_priority(self) -> None:
        env = {"LANG": "es_ES.UTF-8", "LC_MESSAGES": "en_US.UTF-8", "LC_ALL": "pt_BR.UTF-8"}
        self.assertEqual(detect_system_locale(env), "pt_BR.UTF-8")

    def test_map_locale_prefix_and_fallback(self) -> None:
        self.assertEqual(map_locale("pt_BR.UTF-8"), "pt-BR")
        self.assertEqual(map_locale("en_GB.UTF-8"), "en-US")
        self.assertEqual(map_locale("es_ES.UTF-8"), "es-ES")
        self.assertEqual(map_locale("fr_FR.UTF-8"), "en-US")

    def test_select_locale_override_has_priority(self) -> None:
        env = {"LC_ALL": "en_US.UTF-8"}
        self.assertEqual(select_locale(override="pt-BR", env=env), "pt-BR")

    def test_select_locale_default_when_undetectable(self) -> None:
        self.assertEqual(select_locale(override=None, env={}), "pt-BR")

    def test_select_locale_uses_lc_messages_when_lc_all_absent(self) -> None:
        env = {"LC_MESSAGES": "en_US.UTF-8"}
        self.assertEqual(select_locale(override=None, env=env), "en-US")

    def test_select_locale_uses_lang_when_others_absent(self) -> None:
        env = {"LANG": "es_ES.UTF-8"}
        self.assertEqual(select_locale(override=None, env=env), "es-ES")


if __name__ == "__main__":
    unittest.main()
