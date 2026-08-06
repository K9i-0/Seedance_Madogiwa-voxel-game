#!/bin/bash
# Build all 11 chapter workflow JSONs from script.md's H3 inputs tables.
# Frame counts are the grid-fitted values recorded in script.md (17k+5 at 24fps).
# Override weights per GPU architecture with H3_ENCODER / H3_UNET_I2V / H3_UNET_R2V.
set -uo pipefail
SP="$(cd "$(dirname "$0")" && pwd)"
RUN=${1:-$SP}
PY=python3
B=$SP/build_h3_workflow.py

ENC=${H3_ENCODER:-qwen3vl_32b_minimax_h3_int8_convrot.safetensors}
UI=${H3_UNET_I2V:-minimax_h3_fl2va_pruned_int8_convrot.safetensors}
UR=${H3_UNET_R2V:-minimax_h3_ref2va_pruned_int8_convrot.safetensors}
W=(--encoder "$ENC" --unet-i2v "$UI" --unet-r2v "$UR")

cd "$RUN" || exit 1
$PY $SP/extract_prompts.py "$RUN" >/dev/null || exit 1

i2v() { # i2v <n> <frames> <first> <last> <seed>
  $PY $B --mode i2v --out "ch$1_workflow.json" --prompt-file "ch$1_prompt.txt" \
    --frames "$2" --first "$3" --last "$4" --seed "$5" --prefix "video/ch$1" "${W[@]}"
}

# chapter frames first_frame        last_frame       seed
i2v 1  294 ch1_start.png  ch1_end.png   1001
i2v 2  124 ch1_end.png    ch2_end.png   1002
i2v 3  175 ch2_end.png    ch3_end.png   1003
i2v 4  158 ch3_end.png    ch4_end.png   1004
i2v 5  175 ch5_start.png  ch5_end.png   1005
i2v 6  277 ch5_end.png    ch6_end.png   1006
i2v 7  209 ch6_end.png    ch7_end.png   1007
i2v 10 124 ch9_end.png    ch10_end.png  1010
i2v 11 328 ch10_end.png   ch11_end.png  1011

# Chapter 8 — Fukuchan speaks. <Picture N> order must match script.md exactly.
$PY $B --mode r2v --out ch8_workflow.json --prompt-file ch8_prompt.txt --frames 124 --seed 1008 \
  --image ch8_start.png --image ch8_end.png --image Fukuchan_sheet.png \
  --image Yametaro_sheet.png --image height_lineup.png \
  --audio ch8_line1_fukuchan.wav --prefix video/ch8 "${W[@]}"

# Chapter 9 — Yametaro's punchline. Yametaro's sheet FIRST here (he is the speaker).
$PY $B --mode r2v --out ch9_workflow.json --prompt-file ch9_prompt.txt --frames 90 --seed 1009 \
  --image ch9_start.png --image ch9_end.png --image Yametaro_sheet.png \
  --image Fukuchan_sheet.png --image height_lineup.png \
  --audio ch9_line1_yametaro.wav --prefix video/ch9 "${W[@]}"

echo
echo "=== 11 workflows written ==="
ls -la ch*_workflow.json | awk '{printf "%6d B  %s\n",$5,$9}'
echo
echo "weights baked in:"
echo "  encoder : $ENC"
echo "  i2v unet: $UI"
echo "  r2v unet: $UR"
