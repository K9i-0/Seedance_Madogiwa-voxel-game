#!/usr/bin/env python3
"""ランディレクトリ内のキーフレームを一括でVLM検証するバッチドライバ。

事前に <run_dir>/validation/checklists/<画像名（拡張子なし）>.txt として
フレーム固有チェックリスト（英語）を置いておくと、同名の画像を
verify_frame.py（Ollama + Qwen3-VL）で名前順に検証し、
  - <run_dir>/validation/results/<画像名>.txt  … 項目ごとのPASS/FAIL＋根拠
  - <run_dir>/validation/summary.md           … 全フレームの一覧表
を書き出す。

usage:
  verify_run.py <run_dir> [--model qwen3-vl:8b]

- 画像は <run_dir>/<画像名>.png（無ければ .jpg / .jpeg）を探す。
- モデルは --model または環境変数 OLLAMA_VLM で指定（verify_frame.py に渡る）。
- 1枚あたり数十秒〜数分かかるため、呼び出し側は必ずバックグラウンドで実行する。
- FAILが1枚でもあれば（全チェックリスト消化後に）終了コード2。
  ただしVLMには見落とし・誤検出があるため、最終判断はresultsを読んだClaudeが行う。
"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg")
VERIFY_FRAME = Path(__file__).resolve().parent / "verify_frame.py"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def find_image(run_dir: Path, stem: str) -> Path | None:
    for suffix in IMAGE_SUFFIXES:
        candidate = run_dir / f"{stem}{suffix}"
        if candidate.is_file():
            return candidate
    return None


def main() -> None:
    args = sys.argv[1:]
    model_args: list[str] = []
    if "--model" in args:
        i = args.index("--model")
        if i + 1 >= len(args):
            fail("--model requires a value (e.g. qwen3-vl:8b)")
        model_args = ["--model", args[i + 1]]
        del args[i : i + 2]
    if len(args) != 1:
        fail("usage: verify_run.py <run_dir> [--model qwen3-vl:8b]")

    run_dir = Path(args[0])
    if not run_dir.is_dir():
        fail(f"run directory not found: {run_dir}")

    checklist_dir = run_dir / "validation" / "checklists"
    checklists = sorted(checklist_dir.glob("*.txt"))
    if not checklists:
        fail(
            f"no checklists found in {checklist_dir}/ — write one English checklist per frame "
            "as validation/checklists/<image-stem>.txt first (see SKILL.md step 2)"
        )

    results_dir = run_dir / "validation" / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    rows: list[tuple[str, str]] = []  # (image name, verdict)
    for index, checklist_path in enumerate(checklists, start=1):
        stem = checklist_path.stem
        image = find_image(run_dir, stem)
        if image is None:
            print(f"[{index}/{len(checklists)}] {stem}: MISSING (no image for checklist)", flush=True)
            rows.append((stem, "MISSING"))
            continue

        print(f"[{index}/{len(checklists)}] verifying {image.name} ...", flush=True)
        checklist = checklist_path.read_text(encoding="utf-8")
        proc = subprocess.run(
            [sys.executable, str(VERIFY_FRAME), str(image), *model_args],
            input=checklist,
            capture_output=True,
            text=True,
        )
        output = proc.stdout
        if proc.stderr.strip():
            output += f"\n--- stderr ---\n{proc.stderr}"
        (results_dir / f"{image.name}.txt").write_text(output, encoding="utf-8")

        if proc.returncode == 0:
            verdict = "PASS"
        elif proc.returncode == 2:
            verdict = "FAIL"
        else:
            verdict = "ERROR"
        print(f"[{index}/{len(checklists)}] {image.name}: {verdict}", flush=True)
        rows.append((image.name, verdict))

    model_label = model_args[1] if model_args else os.environ.get("OLLAMA_VLM", "qwen3-vl:32b")
    lines = [
        "# Image validation summary (single-image VLM pass)",
        "",
        f"- Model: `{model_label}`",
        "- Per-item evidence: `validation/results/<image>.txt`",
        "- NOTE: VLM verdicts are advisory — Claude must read every result (PASS included)",
        "  and run the timeline cross-check (SKILL.md steps 4-5) before concluding.",
        "",
        "| Image | Verdict |",
        "|-------|---------|",
    ]
    lines += [f"| {name} | {verdict} |" for name, verdict in rows]
    (run_dir / "validation" / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    counts = {v: sum(1 for _, verdict in rows if verdict == v) for v in ("PASS", "FAIL", "ERROR", "MISSING")}
    print(
        f"done: {counts['PASS']} PASS / {counts['FAIL']} FAIL / "
        f"{counts['ERROR']} ERROR / {counts['MISSING']} MISSING "
        f"-> {run_dir / 'validation' / 'summary.md'}",
        flush=True,
    )
    if counts["FAIL"] or counts["ERROR"] or counts["MISSING"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
