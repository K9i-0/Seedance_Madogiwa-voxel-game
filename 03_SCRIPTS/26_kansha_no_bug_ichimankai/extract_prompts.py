#!/usr/bin/env python3
"""Extract each chapter's Motion prompt from script.md into chN_prompt.txt.

script.md stays the single source of truth: the prompts are never retyped or
summarised anywhere else. The skill forbids summarising a Motion prompt at
generation time, so the workflow JSONs are built from these exact extracts.

usage: extract_prompts.py <run_dir>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: extract_prompts.py <run_dir>")
    run = Path(sys.argv[1])
    text = (run / "script.md").read_text(encoding="utf-8")

    sections = list(re.finditer(r"^### H3 inputs \(Chapter (\d+)\)\s*$", text, re.MULTILINE))
    if not sections:
        raise SystemExit("no '### H3 inputs (Chapter N)' sections found")

    written = 0
    for i, m in enumerate(sections):
        n = m.group(1)
        end = sections[i + 1].start() if i + 1 < len(sections) else len(text)
        section = text[m.start():end]
        pm = re.search(r"^- Motion prompt:[ ]?(.*)$", section, re.MULTILINE)
        if not pm:
            raise SystemExit(f"chapter {n}: no Motion prompt line")
        prompt = pm.group(1).strip()
        if len(prompt) < 200:
            raise SystemExit(f"chapter {n}: Motion prompt suspiciously short ({len(prompt)} chars)")
        out = run / f"ch{n}_prompt.txt"
        out.write_text(prompt + "\n", encoding="utf-8")
        print(f"ch{n}_prompt.txt  {len(prompt)} chars")
        written += 1
    print(f"{written} prompts extracted verbatim from script.md")


if __name__ == "__main__":
    main()
