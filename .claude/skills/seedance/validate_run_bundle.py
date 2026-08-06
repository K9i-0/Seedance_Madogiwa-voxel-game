#!/usr/bin/env python3
"""Validate that a Seedance run is a portable, self-contained CapCut input bundle."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def fail(messages: list[str]) -> None:
    for message in messages:
        print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    if len(sys.argv) != 2:
        fail(["usage: validate_run_bundle.py 03_SCRIPTS/<NN>_<slug>"])

    run_dir = Path(sys.argv[1])
    script_path = run_dir / "script.md"
    errors: list[str] = []

    if not run_dir.is_dir():
        fail([f"run directory does not exist: {run_dir}"])
    if not script_path.is_file():
        fail([f"missing script.md: {script_path}"])

    text = script_path.read_text(encoding="utf-8")
    if re.search(r"(?:\.\./)+02_CHARACTERS/", text):
        errors.append("script.md references 02_CHARACTERS outside the run; copy references into the run and use basenames")

    if re.search(r"^##.*\bScene ledger\b", text, re.MULTILINE | re.IGNORECASE) is None:
        errors.append(
            "script.md lacks a '## Scene ledger' section "
            "(location & time-of-day ledger across all clips; prevents unexplained day/night jumps)"
        )

    sections = list(re.finditer(r"^### CapCut inputs \(Clip (\d+)\)\s*$", text, re.MULTILINE))
    if not sections:
        errors.append("no '### CapCut inputs (Clip N)' sections found")

    for index, match in enumerate(sections):
        clip = match.group(1)
        end = sections[index + 1].start() if index + 1 < len(sections) else len(text)
        section = text[match.start():end]
        prompt_marker = section.find("- Motion prompt:")

        if prompt_marker < 0:
            errors.append(f"Clip {clip}: missing Motion prompt")
            prompt = ""
            input_table = section
        else:
            prompt = section[prompt_marker:]
            input_table = section[:prompt_marker]

        mappings = re.findall(r"@Image(\d+)\s*=\s*`([^`]+\.png)`", input_table)
        if mappings and "Required attached reference files:" not in prompt:
            errors.append(f"Clip {clip}: Motion prompt lacks 'Required attached reference files:'")

        if prompt and "on-screen text" not in prompt.lower():
            errors.append(
                f"Clip {clip}: Motion prompt lacks the no-on-screen-text instruction "
                '(e.g. "do NOT render any on-screen text — no subtitles, no captions, no lettering, no Japanese characters")'
            )

        time_of_day = re.compile(
            r"\b(daylight|daytime|midday|noon|morning|afternoon|dusk|sunset|golden hour|evening|night|nighttime)\b",
            re.IGNORECASE,
        )
        if prompt and time_of_day.search(prompt) is None:
            errors.append(
                f"Clip {clip}: Motion prompt lacks a time-of-day/lighting phrase from the Scene ledger "
                '(e.g. "bright midday daylight" — without it the model defaults to the location\'s typical '
                "time of day and the video can jump from day to night)"
            )

        for slot, filename in mappings:
            if Path(filename).name != filename:
                errors.append(f"Clip {clip}: @Image{slot} must use a bundled basename, not path: {filename}")
                continue
            bundled = run_dir / filename
            if not bundled.is_file():
                errors.append(f"Clip {clip}: missing bundled reference file: {filename}")
            elif bundled.is_symlink():
                errors.append(f"Clip {clip}: reference must be a physical file, not symlink: {filename}")
            if f"@Image{slot} = {filename}" not in prompt:
                errors.append(f"Clip {clip}: Motion prompt does not redeclare '@Image{slot} = {filename}'")

        for label in ("Start frame (Frame A)", "End frame (Frame B)", "Audio"):
            declaration = re.search(rf"^- {re.escape(label)}:\s*`([^`\n]+)`", input_table, re.MULTILINE)
            if declaration is None:
                errors.append(f"Clip {clip}: missing {label} file declaration")
                continue
            filename = declaration.group(1)
            if Path(filename).name != filename:
                errors.append(f"Clip {clip}: {label} must use a bundled basename, not path: {filename}")
            elif not (run_dir / filename).is_file():
                errors.append(f"Clip {clip}: missing {label} file: {filename}")

    if errors:
        fail(errors)
    print(f"OK: portable Seedance bundle validated: {run_dir}")


if __name__ == "__main__":
    main()
