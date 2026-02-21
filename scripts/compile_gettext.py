"""Compile .po files into .mo files (minimal msgfmt).

Keeps the project dependency-free (no GNU gettext required).

Usage:
  python scripts/compile_gettext.py
"""

from __future__ import annotations

import ast
import os
import struct
from pathlib import Path


def read_po(path: Path) -> dict[str, str]:
    messages: dict[str, str] = {}

    msgid_parts: list[str] = []
    msgstr_parts: list[str] = []
    state: str | None = None

    def flush() -> None:
        nonlocal msgid_parts, msgstr_parts, state
        if not msgid_parts and not msgstr_parts:
            return
        msgid = "".join(msgid_parts)
        msgstr = "".join(msgstr_parts)
        # keep header (msgid == "") so gettext knows the charset, plural forms, etc.
        messages[msgid] = msgstr
        msgid_parts = []
        msgstr_parts = []
        state = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("msgid "):
            flush()
            state = "msgid"
            msgid_parts.append(ast.literal_eval(line[len("msgid ") :]))
            continue
        if line.startswith("msgstr "):
            state = "msgstr"
            msgstr_parts.append(ast.literal_eval(line[len("msgstr ") :]))
            continue
        if line.startswith('"') and state == "msgid":
            msgid_parts.append(ast.literal_eval(line))
            continue
        if line.startswith('"') and state == "msgstr":
            msgstr_parts.append(ast.literal_eval(line))
            continue

    flush()
    return messages


def write_mo(messages: dict[str, str], outpath: Path) -> None:
    # Based on the GNU gettext .mo file format.
    items = sorted(messages.items())

    ids = b"\x00".join(k.encode("utf-8") for k, _ in items) + b"\x00"
    strs = b"\x00".join(v.encode("utf-8") for _, v in items) + b"\x00"

    keystart = 7 * 4
    valuestart = keystart + len(items) * 8
    id_offset = valuestart + len(items) * 8
    str_offset = id_offset + len(ids)

    koffsets: list[tuple[int, int]] = []
    voffsets: list[tuple[int, int]] = []

    offset = 0
    for k, _v in items:
        b = k.encode("utf-8")
        koffsets.append((len(b), id_offset + offset))
        offset += len(b) + 1

    offset = 0
    for _k, v in items:
        b = v.encode("utf-8")
        voffsets.append((len(b), str_offset + offset))
        offset += len(b) + 1

    output = []
    # magic, version, nstrings, orig_tab_offset, trans_tab_offset, hash size, hash offset
    output.append(struct.pack("Iiiiiii", 0x950412DE, 0, len(items), keystart, valuestart, 0, 0))

    for length, off in koffsets:
        output.append(struct.pack("ii", length, off))
    for length, off in voffsets:
        output.append(struct.pack("ii", length, off))

    output.append(ids)
    output.append(strs)

    outpath.write_bytes(b"".join(output))


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    locales_dir = repo_root / "src" / "locales"

    for po in locales_dir.rglob("*.po"):
        messages = read_po(po)
        mo = po.with_suffix(".mo")
        write_mo(messages, mo)
        print(f"Compiled {po.relative_to(repo_root)} -> {mo.relative_to(repo_root)}")


if __name__ == "__main__":
    main()
