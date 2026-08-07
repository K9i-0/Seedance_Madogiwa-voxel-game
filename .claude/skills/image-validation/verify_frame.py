#!/usr/bin/env python3
"""キーフレーム静止画をローカルVLM（Ollama + Qwen3-VL）で検証する。

フレーム固有のチェックリスト（英語）をstdinで渡すと、画像と突き合わせて
各項目のPASS/FAILと総合判定を返す。総合判定がFAILなら終了コード2。

usage:
  verify_frame.py <image.png> [--model qwen3-vl:32b] <<'EOF'
  <English checklist: numbered items to verify against the image>
  EOF

- モデルは環境変数 OLLAMA_VLM でも差し替え可（デフォルト: qwen3-vl:32b）。
- Ollamaサーバが起動していなければ `ollama serve` をバックグラウンド起動して待つ。
- 判定の最終行に "VERDICT: PASS" / "VERDICT: FAIL" を出させ、それを終了コードに反映する。
  ただしVLMには見落とし・誤検出があるため、最終判断は指摘内容を読んだ上でClaudeが行うこと。
"""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://127.0.0.1:11434")

SYSTEM_INSTRUCTIONS = """You are a meticulous QA inspector for AI-generated video keyframes.
Inspect the attached image against the checklist. For EACH numbered item answer:
  <item number>. PASS or FAIL — <one short sentence of evidence from the image>
Judge only from what is visible. Be strict about design details (glasses shape, masks,
props' fill levels, hinge/handle sides, open/closed mouths, art style).
After all items, output exactly one final line:
  VERDICT: PASS   (only if every item passed)
  VERDICT: FAIL   (if any item failed)
"""


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def ensure_server() -> None:
    for attempt in range(30):
        try:
            urllib.request.urlopen(f"{OLLAMA_URL}/api/tags", timeout=3)
            return
        except (urllib.error.URLError, OSError):
            if attempt == 0:
                print("ollama server not running — starting `ollama serve` ...", file=sys.stderr)
                try:
                    subprocess.Popen(
                        ["ollama", "serve"],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except FileNotFoundError:
                    fail(
                        "ollama is not installed — install it first:\n"
                        "  brew install ollama    (or https://ollama.com/download)\n"
                        "  ollama pull qwen3-vl:32b"
                    )
            time.sleep(1)
    fail("could not reach the ollama server (install: https://ollama.com/download)")


def main() -> None:
    args = [a for a in sys.argv[1:]]
    model = os.environ.get("OLLAMA_VLM", "qwen3-vl:32b")
    if "--model" in args:
        i = args.index("--model")
        if i + 1 >= len(args):
            fail("--model requires a value (e.g. qwen3-vl:32b)")
        model = args[i + 1]
        del args[i : i + 2]
    if len(args) != 1:
        fail("usage: verify_frame.py <image.png> [--model qwen3-vl:32b] <<'EOF' checklist EOF")

    image_path = args[0]
    if not os.path.isfile(image_path):
        fail(f"image not found: {image_path}")

    checklist = sys.stdin.read().strip()
    if not checklist:
        fail("empty checklist on stdin — pass the frame-specific checklist as a heredoc")

    ensure_server()

    with open(image_path, "rb") as fh:
        image_b64 = base64.b64encode(fh.read()).decode("ascii")

    payload = json.dumps(
        {
            "model": model,
            "prompt": f"{SYSTEM_INSTRUCTIONS}\n\nChecklist:\n{checklist}",
            "images": [image_b64],
            "stream": False,
            "options": {"temperature": 0},
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        f"{OLLAMA_URL}/api/generate",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        # 32Bモデルの初回ロードは数分かかることがあるためタイムアウトは長めに取る
        with urllib.request.urlopen(request, timeout=1800) as response:
            body = json.load(response)
    except urllib.error.HTTPError as error:
        detail = error.read().decode("utf-8", "replace")
        if error.code == 404 and "not found" in detail:
            fail(
                f"model '{model}' is not pulled — run: ollama pull {model}\n"
                "(available tags: https://ollama.com/library/qwen3-vl)"
            )
        fail(f"ollama API error {error.code}: {detail}")

    answer = (body.get("response") or "").strip()
    if not answer:
        fail(f"empty response from ollama: {body}")

    print(f"model: {model}")
    print(f"image: {image_path}")
    print(answer)

    if "VERDICT: PASS" not in answer:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
