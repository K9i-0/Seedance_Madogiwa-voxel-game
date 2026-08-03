#!/bin/bash
# Irodori-TTS（ゼロショットボイスクローン）でセリフ音声(wav)を1つ生成する
# 使い方: irodori_speak.sh "セリフテキスト" 出力ファイル.wav 参照音声.wav [シード値]
# 参照音声はキャラごとに 02_CHARACTERS/VOICE_CAST.md（正典）で指定された <キャラ>_voice.wav を使う。
# 事前学習は不要（毎回の合成時に参照音声を渡すゼロショット方式）。
# Irodori-TTS本体の設置場所は IRODORI_TTS_DIR（既定: ~/irodori_tts）。
set -eu

TEXT="${1:?セリフテキストを指定してください}"
OUT="${2:?出力wavパスを指定してください}"
REF="${3:?参照音声wavを指定してください（02_CHARACTERS/VOICE_CAST.md参照）}"
SEED="${4:-}"
TTS_DIR="${IRODORI_TTS_DIR:-$HOME/irodori_tts}"

[ -f "$REF" ] || { echo "ERROR: 参照音声が見つかりません: $REF" >&2; exit 1; }
if [ ! -f "$TTS_DIR/infer.py" ]; then
  echo "ERROR: Irodori-TTSが見つかりません: $TTS_DIR" >&2
  echo "セットアップ: git clone https://github.com/Aratako/Irodori-TTS.git ~/irodori_tts && cd ~/irodori_tts && uv sync --extra cpu" >&2
  exit 1
fi

# 出力先を絶対パスにする（infer.pyはTTS_DIRで実行するため）
case "$OUT" in
  /*) : ;;
  *) OUT="$PWD/$OUT" ;;
esac
case "$REF" in
  /*) : ;;
  *) REF="$PWD/$REF" ;;
esac

SEED_ARGS=()
[ -n "$SEED" ] && SEED_ARGS=(--seed "$SEED")

(cd "$TTS_DIR" && uv run --no-sync python infer.py \
  --hf-checkpoint Aratako/Irodori-TTS-500M-v3 \
  --text "$TEXT" \
  --ref-wav "$REF" \
  --output-wav "$OUT" \
  "${SEED_ARGS[@]}" >&2)

head -c 4 "$OUT" | grep -q RIFF || { echo "ERROR: 合成に失敗しました（上のログ参照）" >&2; rm -f "$OUT"; exit 1; }

# 前後の無音をトリムする（先頭~0.1s・末尾~0.2sだけ残す）。
# 長い無音はSeedance添付時に口パクの開始位置を狂わせる（リップシンクずれの原因）。
if command -v ffmpeg >/dev/null 2>&1; then
  TMP="${OUT%.wav}.trim.wav"
  ffmpeg -y -v error -i "$OUT" -af "silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.1,areverse,silenceremove=start_periods=1:start_threshold=-40dB:start_silence=0.2,areverse" "$TMP" \
    && mv "$TMP" "$OUT" || { rm -f "$TMP"; echo "WARN: 無音トリムに失敗したため未トリムのまま出力します" >&2; }
else
  echo "WARN: ffmpegが無いため無音トリムをスキップしました（Seedanceでリップシンクがずれやすくなります）" >&2
fi

DUR=$(python3 -c "
import wave
w = wave.open('$OUT')
print(f'{w.getnframes()/w.getframerate():.2f}')
")
echo "OK: $OUT (${DUR}s, ref=$(basename "$REF")${SEED:+, seed=$SEED})"
