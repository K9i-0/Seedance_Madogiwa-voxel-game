#!/bin/bash
# そば屋のセリフwavにモンスターボイス加工をかける（正典エフェクト。VOICE_CAST.md参照）
# 使い方: sobaya_monsterize.sh 入力.wav [出力.wav]
#   出力を省略すると入力ファイルを上書き（in-place）する。
# 加工内容: ピッチ5半音下げ（尺は維持）＋70Hzトレモロでうなり系のザラつきを追加。
# そば屋のセリフは irodori_speak.sh で生成した後、必ずこのスクリプトを通したwavを成果物にする。
set -eu

IN="${1:?入力wavを指定してください}"
OUT="${2:-$IN}"

[ -f "$IN" ] || { echo "ERROR: 入力wavが見つかりません: $IN" >&2; exit 1; }
command -v ffmpeg >/dev/null || { echo "ERROR: ffmpegが必要です（brew install ffmpeg）" >&2; exit 1; }
command -v ffprobe >/dev/null || { echo "ERROR: ffprobeが必要です（brew install ffmpeg）" >&2; exit 1; }

SR=$(ffprobe -v error -select_streams a:0 -show_entries stream=sample_rate -of csv=p=0 "$IN")
[ -n "$SR" ] && [ "$SR" -gt 0 ] || { echo "ERROR: サンプルレートを取得できません: $IN" >&2; exit 1; }

# ピッチ比 0.7492 = 2^(-5/12)（5半音下げ）。asetrateで下げ、atempo=1/0.7492で尺を元に戻す。
TMP=$(mktemp -t sobaya_monster).wav
ffmpeg -y -v error -i "$IN" \
  -af "asetrate=${SR}*0.7492,aresample=${SR},atempo=1.3348,tremolo=f=70:d=0.5,dynaudnorm" \
  -sample_fmt s16 "$TMP"
mv "$TMP" "$OUT"

DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$OUT")
echo "OK: $OUT (${DUR%.*}s台, monsterized: -5半音+うなり)"
