"""Integration-ish test for `python -m hello --version`.

Runs the module as Python would do from the CLI.
"""

from __future__ import annotations

import os
import subprocess
import sys
import unittest

sys.path.insert(0, "src")

from hello import get_version  # noqa: E402


class TestModuleInvocation(unittest.TestCase):
    def test_python_m_hello_version(self) -> None:
        env = os.environ.copy()
        # Ensure the in-repo src/ is importable when running `python -m hello`.
        env["PYTHONPATH"] = os.pathsep.join(["src", env.get("PYTHONPATH", "")]).strip(
            os.pathsep
        )

        proc = subprocess.run(
            [sys.executable, "-m", "hello", "--version"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )

        self.assertEqual(proc.stdout, f"{get_version()}\n")
        self.assertEqual(proc.stderr, "")


if __name__ == "__main__":
    unittest.main()
