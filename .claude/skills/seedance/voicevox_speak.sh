#!/bin/bash
# VOICEVOXローカルエンジンでセリフ音声(wav)を1つ生成する
# 使い方: voicevox_speak.sh "セリフテキスト" 出力ファイル.wav スタイルID [話速speedScale]
# スタイルIDはキャラごとに 02_CHARACTERS/VOICE_CAST.md（正典）で指定されたものを使う。
# エンジン未起動なら自動起動する（VOICEVOX_ENGINE_DIR、既定: ~/voicevox_engine/macos-arm64）。
set -eu

TEXT="${1:?セリフテキストを指定してください}"
OUT="${2:?出力wavパスを指定してください}"
SPEAKER="${3:?スタイルIDを指定してください（02_CHARACTERS/VOICE_CAST.md参照）}"
SPEED="${4:-1.0}"
HOST="${VOICEVOX_HOST:-http://127.0.0.1:50021}"
ENGINE_DIR="${VOICEVOX_ENGINE_DIR:-$HOME/voicevox_engine/macos-arm64}"

if ! curl -sf "$HOST/version" >/dev/null; then
  if [ ! -x "$ENGINE_DIR/run" ]; then
    echo "ERROR: VOICEVOXエンジンが起動しておらず、$ENGINE_DIR/run も見つかりません。" >&2
    echo "VOICEVOX/voicevox_engine のmacOSビルドを設置するか、VOICEVOX_ENGINE_DIRを設定してください。" >&2
    exit 1
  fi
  echo "エンジンを起動します..." >&2
  (cd "$ENGINE_DIR" && nohup ./run --host 127.0.0.1 --port 50021 > "$ENGINE_DIR/../engine.log" 2>&1 &)
  for _ in $(seq 1 60); do
    curl -sf "$HOST/version" >/dev/null && break
    sleep 1
  done
  curl -sf "$HOST/version" >/dev/null || { echo "ERROR: エンジンの起動に失敗しました（$ENGINE_DIR/../engine.log 参照）" >&2; exit 1; }
fi

QUERY=$(curl -s -X POST "$HOST/audio_query" --get \
  --data-urlencode "text=$TEXT" --data-urlencode "speaker=$SPEAKER")
QUERY=$(printf '%s' "$QUERY" | python3 -c "
import json, sys
q = json.load(sys.stdin)
q['speedScale'] = float('$SPEED')
print(json.dumps(q))
")
printf '%s' "$QUERY" | curl -s -X POST "$HOST/synthesis?speaker=$SPEAKER" \
  -H "Content-Type: application/json" -d @- -o "$OUT"

# wavとして妥当かの簡易チェック（失敗時はエラーJSONが書かれている）
head -c 4 "$OUT" | grep -q RIFF || { echo "ERROR: 合成に失敗しました: $(cat "$OUT")" >&2; rm -f "$OUT"; exit 1; }
DUR=$(python3 -c "
import wave
w = wave.open('$OUT')
print(f'{w.getnframes()/w.getframerate():.2f}')
")
echo "OK: $OUT (${DUR}s, style=$SPEAKER, speed=$SPEED)"
