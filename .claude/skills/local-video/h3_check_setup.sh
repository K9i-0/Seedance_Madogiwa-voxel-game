#!/bin/bash
# ローカル動画制作（MiniMax H3）ワークフローの導入状態チェック。
# 未導入コンポーネントごとに、公式ドキュメントに基づく導入手順を表示する。
#
# usage: .claude/skills/local-video/h3_check_setup.sh
#
# 環境変数:
#   COMFYUI_DIR   ComfyUIの設置場所（デフォルト: ~/ComfyUI）
#   OLLAMA_VLM    画像検証に使うVLMモデル（デフォルト: qwen3-vl:32b）
set -uo pipefail

COMFYUI_DIR="${COMFYUI_DIR:-$HOME/ComfyUI}"
OLLAMA_VLM="${OLLAMA_VLM:-qwen3-vl:32b}"
MISSING=0

section() { printf '\n== %s ==\n' "$1"; }
ok()      { printf 'OK:      %s\n' "$1"; }
missing() { printf 'MISSING: %s\n' "$1"; MISSING=1; }

section "ComfyUI (MiniMax H3 実行基盤)"
if [ -f "$COMFYUI_DIR/main.py" ]; then
  ok "ComfyUI at $COMFYUI_DIR"
else
  missing "ComfyUI が $COMFYUI_DIR にありません"
  cat <<'MSG'
  導入手順（公式: https://docs.comfy.org/ を必ず確認すること）:
    git clone https://github.com/comfyanonymous/ComfyUI ~/ComfyUI
    cd ~/ComfyUI && pip3 install -r requirements.txt
  （既存インストールがある場合は v0.30.0 以上へ更新する。
   別の場所に置く場合は COMFYUI_DIR で指定する）
MSG
fi

section "MiniMax H3 モデルファイル"
for f in \
  "diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors" \
  "diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors" \
  "vae/minimax_h3_video_vae_fp16.safetensors" \
  "vae/minimax_h3_audio_vae_fp32.safetensors"; do
  if [ -f "$COMFYUI_DIR/models/$f" ]; then
    ok "$f"
  else
    missing "$COMFYUI_DIR/models/$f"
  fi
done
if ls "$COMFYUI_DIR/models/text_encoders/"qwen3vl_32b_minimax_h3_*.safetensors >/dev/null 2>&1; then
  ok "text encoder: $(ls "$COMFYUI_DIR/models/text_encoders/" | grep '^qwen3vl_32b_minimax_h3_' | tr '\n' ' ')"
else
  missing "text encoder (qwen3vl_32b_minimax_h3_*.safetensors)"
fi
if [ "$MISSING" -ne 0 ]; then
  cat <<'MSG'
  モデル取得（公式チュートリアル: https://docs.comfy.org/tutorials/video/minimax/minimax-h3 、
  配布元: https://huggingface.co/Comfy-Org/MiniMax-H3 。数十GBあるので開始前にユーザーへ確認する）:
    hf download Comfy-Org/MiniMax-H3 \
      --include "diffusion_models/minimax_h3_fl2va_pruned_int8_convrot.safetensors" \
                "diffusion_models/minimax_h3_ref2va_pruned_int8_convrot.safetensors" \
                "vae/*" \
      --local-dir ~/ComfyUI/models
  テキストエンコーダは Apple Silicon では NVFP4 版ではなく INT8/bf16 版を選ぶこと
  （https://huggingface.co/Comfy-Org/MiniMax-H3/tree/main/text_encoders で最新のファイル名を確認）。
MSG
fi

section "APIワークフローJSON（初回にComfyUIからExport (API)で保存）"
for wf in h3_i2v_api.json h3_r2v_api.json; do
  if [ -f "$(dirname "$0")/workflows/$wf" ]; then
    ok "workflows/$wf"
  else
    missing "workflows/$wf — ComfyUIで公式テンプレート(MiniMax H3 I2V/R2V)を開き Export (API) で保存する"
  fi
done

section "Ollama + Qwen3-VL（キーフレーム画像の検証）"
if command -v ollama >/dev/null 2>&1; then
  ok "ollama CLI"
  if ollama list 2>/dev/null | grep -q "^${OLLAMA_VLM%%:*}"; then
    ok "model ${OLLAMA_VLM%%:*}* is pulled"
  else
    missing "VLMモデル ${OLLAMA_VLM} が未取得"
    echo "  取得: ollama pull ${OLLAMA_VLM}"
    echo "  （タグは https://ollama.com/library/qwen3-vl で確認。メモリの少ないマシンは qwen3-vl:8b）"
  fi
else
  missing "ollama が未導入"
  cat <<'MSG'
  導入手順（公式: https://ollama.com/download ）:
    brew install ollama
    ollama pull qwen3-vl:32b   # 64GB未満のマシンは qwen3-vl:8b
MSG
fi

section "draw-things-cli + Qwen Image Edit 2511（キーフレーム生成）"
if command -v draw-things-cli >/dev/null 2>&1; then
  ok "draw-things-cli"
  if draw-things-cli models list --downloaded-only 2>/dev/null | grep -q "qwen_image_edit_2511_q6p"; then
    ok "model qwen_image_edit_2511_q6p.ckpt"
  else
    missing "モデル qwen_image_edit_2511_q6p.ckpt（取得: draw-things-cli models ensure --model qwen_image_edit_2511_q6p.ckpt）"
  fi
else
  missing "draw-things-cli（導入: brew install drawthingsai/draw-things/draw-things-cli）"
fi

section "音声合成（Irodori-TTS / VOICEVOX）"
[ -d "$HOME/irodori_tts" ] && ok "~/irodori_tts" || missing "~/irodori_tts（https://github.com/Aratako/Irodori-TTS の手順で導入）"
[ -d "$HOME/voicevox_engine" ] && ok "~/voicevox_engine" || missing "~/voicevox_engine（VOICEVOXヘッドレスエンジン）"

section "ffmpeg（結合・パディング・クレジット焼き込み）"
command -v ffmpeg >/dev/null 2>&1 && ok "ffmpeg" || missing "ffmpeg（導入: brew install ffmpeg）"

echo
if [ "$MISSING" -ne 0 ]; then
  echo "RESULT: 未導入のコンポーネントがあります。上記の手順と公式ドキュメントに従って導入してから作業を開始してください。"
  exit 1
fi
echo "RESULT: すべて導入済みです。"
