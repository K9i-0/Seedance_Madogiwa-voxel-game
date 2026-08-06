#!/bin/bash
# Assemble run 26 into final.mp4 per script.md's assembly section.
# Narration chapters keep their generated ambient bed and get the narration mixed over it;
# dialogue chapters (8, 9) DISCARD the generated audio and use the local wav alone, because
# H3's embedded audio is not the source of truth — the Irodori-TTS wavs are.
#
# OFFSETS_MS below are per-chapter speech onsets. They must be set by WATCHING each
# generated chapter and finding the frame where the speaker's mouth starts moving
# (dialogue) or the beat the line describes (narration). The placeholder 0 values are
# NOT correct by default — assembly is not finished until these are checked.
set -uo pipefail
RUN="$(cd "$(dirname "$0")" && pwd)"
FF=$(command -v ffmpeg || echo /opt/homebrew/bin/ffmpeg)
FP=$(command -v ffprobe || echo /opt/homebrew/bin/ffprobe)
cd "$RUN" || exit 1

declare -A OFFSETS_MS=(
  [1]=0 [2]=0 [3]=0 [4]=0 [5]=0 [6]=0 [7]=0 [8]=0 [9]=0 [10]=0 [11]=0
)
DIALOGUE_CHAPTERS="8 9"

wav_for() { case $1 in 8) echo ch8_line1_fukuchan.wav;; 9) echo ch9_line1_yametaro.wav;; *) echo "ch$1_nar1.wav";; esac; }

for n in 1 2 3 4 5 6 7 8 9 10 11; do
  vid="ch$n.mp4"; wav=$(wav_for $n); out="ch${n}_final.mp4"; off=${OFFSETS_MS[$n]}
  if [ ! -f "$vid" ]; then echo "MISSING $vid — generate it first"; continue; fi
  if [ ! -f "$wav" ]; then echo "MISSING $wav"; continue; fi
  if echo "$DIALOGUE_CHAPTERS" | grep -qw "$n"; then
    # dialogue: local wav ONLY, generated audio discarded
    $FF -y -v error -i "$vid" -i "$wav" \
      -filter_complex "[1:a]adelay=${off}|${off},apad[a]" \
      -map 0:v -map "[a]" -c:v copy -shortest "$out" && echo "ch$n (dialogue, wav only, +${off}ms) -> $out"
  else
    # narration: mix over the generated ambient bed
    $FF -y -v error -i "$vid" -i "$wav" \
      -filter_complex "[1:a]adelay=${off}|${off},apad[n];[0:a][n]amix=inputs=2:duration=first:dropout_transition=0[a]" \
      -map 0:v -map "[a]" -c:v copy "$out" && echo "ch$n (narration mixed, +${off}ms) -> $out"
  fi
done

: > concat.txt
for n in 1 2 3 4 5 6 7 8 9 10 11; do
  [ -f "ch${n}_final.mp4" ] && echo "file 'ch${n}_final.mp4'" >> concat.txt
done
missing=$(( 11 - $(wc -l < concat.txt) ))
[ "$missing" -gt 0 ] && echo "WARNING: $missing chapter(s) missing — concat will be incomplete"

$FF -y -v error -f concat -safe 0 -i concat.txt -c copy final_draft.mp4 && echo "-> final_draft.mp4"

# Burned-in 究極奥義 title over chapter 11 (never rendered via keyframes/H3 — generated text garbles).
C11_START=$(python3 - <<'PY'
import subprocess
tot=0.0
for n in range(1,11):
    try:
        d=subprocess.run(["$FP","-v","error","-show_entries","format=duration",
                          "-of","csv=p=0",f"ch{n}_final.mp4"],capture_output=True,text=True).stdout.strip()
        tot+=float(d)
    except Exception: pass
print(f"{tot:.2f}")
PY
)
echo "chapter 11 starts at ${C11_START}s"
FONT='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc'
$FF -y -v error -i final_draft.mp4 -vf \
"drawtext=fontfile='$FONT':text='究極奥義':fontsize=44:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h*0.62:enable='between(t,$C11_START+1,$C11_START+9)',drawtext=fontfile='$FONT':text='何もしてないのに壊れた':fontsize=64:fontcolor=white:borderw=4:bordercolor=black:x=(w-tw)/2:y=h*0.70:enable='between(t,$C11_START+2,$C11_START+9)'" \
 -c:a copy final.mp4 && echo "-> final.mp4"

$FP -v error -show_entries format=duration,size -show_entries stream=width,height,codec_name -of default=noprint_wrappers=1 final.mp4
echo "NOTE: watch final.mp4 end-to-end and confirm cuts, sync, no doubled dialogue, ~86.6s total."
