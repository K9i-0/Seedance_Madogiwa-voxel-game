#!/bin/zsh
set -euo pipefail

ROOT="/Users/kenji.shimoju/Documents/private/Seedance_Madogiwa"
TMP="/private/tmp/madogiwa_video"
OUT="/private/tmp/09_professional_morning_takosan_15s.mp4"
mkdir -p "$TMP"

for name in narr1 yame1 tako1 tako2 yame2 tako3 narr2; do
  if [[ ! -s "$TMP/$name.aiff" ]]; then
    print -u2 "Missing voice master: $TMP/$name.aiff"
    exit 1
  fi
done

cat > "$TMP/captions.ass" <<'ASS'
[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Narrator,Hiragino Sans W6,48,&H00F3F3F3,&H00FFFFFF,&H00131313,&H99000000,0,0,0,0,100,100,1,0,3,2,0,2,160,160,58,1
Style: Yametaro,Hiragino Sans W6,54,&H00FFFFFF,&H00FFFFFF,&H00131313,&H99000000,0,0,0,0,100,100,0,0,3,2,0,2,120,120,58,1
Style: Takosan,Hiragino Sans W6,54,&H00FFFFFF,&H00FFFFFF,&H00131313,&H99000000,0,0,0,0,100,100,0,0,3,2,0,2,120,120,58,1
Style: Label,Hiragino Sans W6,30,&H00FFFFFF,&H00FFFFFF,&H00131313,&HCC2B2B2B,0,0,0,0,100,100,0,0,3,1,0,1,120,120,134,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:01.78,Narrator,,0,0,0,,プロフェッショナルの朝は、遅い。
Dialogue: 1,0:00:01.90,0:00:05.05,Label,,0,0,0,,インタビュアー・やめ太郎
Dialogue: 0,0:00:01.90,0:00:05.05,Yametaro,,0,0,0,,この時間だと、窓際の席、\N空いてないんやないですか？
Dialogue: 1,0:00:05.17,0:00:07.33,Label,,0,0,0,,たこさん
Dialogue: 0,0:00:05.17,0:00:07.33,Takosan,,0,0,0,,僕がいる場所が、窓際なので。
Dialogue: 1,0:00:07.50,0:00:09.06,Label,,0,0,0,,たこさん
Dialogue: 0,0:00:07.50,0:00:09.06,Takosan,,0,0,0,,ターミナルを開きます。
Dialogue: 1,0:00:09.17,0:00:10.48,Label,,0,0,0,,インタビュアー・やめ太郎
Dialogue: 0,0:00:09.17,0:00:10.48,Yametaro,,0,0,0,,そこから作業を？
Dialogue: 1,0:00:10.58,0:00:12.24,Label,,0,0,0,,たこさん
Dialogue: 0,0:00:10.58,0:00:12.24,Takosan,,0,0,0,,いえ。閉じます。
Dialogue: 0,0:00:12.36,0:00:14.96,Narrator,,0,0,0,,開いて、閉じる。\Nそれが、窓際の流儀。
ASS

ffmpeg -y -hide_banner -loglevel error \
  -f lavfi -i "sine=frequency=110:sample_rate=48000:duration=15" \
  -f lavfi -i "sine=frequency=164.81:sample_rate=48000:duration=15" \
  -f lavfi -i "sine=frequency=220:sample_rate=48000:duration=15" \
  -f lavfi -i "anoisesrc=color=pink:sample_rate=48000:duration=15" \
  -filter_complex "[0:a]volume=0.018[a0];[1:a]volume=0.010[a1];[2:a]volume=0.006[a2];[3:a]lowpass=f=2500,highpass=f=180,volume=0.008[a3];[a0][a1][a2][a3]amix=inputs=4:normalize=0,afade=t=in:st=0:d=0.6,afade=t=out:st=14.2:d=0.8[bgm]" \
  -map "[bgm]" -c:a pcm_s16le "$TMP/bgm.wav"

ffmpeg -y -hide_banner -loglevel error \
  -i "$TMP/narr1.aiff" -i "$TMP/yame1.aiff" -i "$TMP/tako1.aiff" \
  -i "$TMP/tako2.aiff" -i "$TMP/yame2.aiff" -i "$TMP/tako3.aiff" \
  -i "$TMP/narr2.aiff" -i "$TMP/bgm.wav" \
  -filter_complex "\
    [0:a]atempo=1.15,highpass=f=90,lowpass=f=9000,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-18:TP=-2:LRA=7,adelay=0|0[a0];\
    [1:a]atempo=1.18,highpass=f=100,lowpass=f=9500,acompressor=threshold=-20dB:ratio=2.8:attack=4:release=70,loudnorm=I=-18:TP=-2:LRA=7,adelay=1900|1900[a1];\
    [2:a]atempo=1.12,highpass=f=90,lowpass=f=9000,acompressor=threshold=-21dB:ratio=2.6:attack=5:release=80,loudnorm=I=-18:TP=-2:LRA=7,adelay=5170|5170[a2];\
    [3:a]atempo=1.10,highpass=f=90,lowpass=f=9000,acompressor=threshold=-21dB:ratio=2.6:attack=5:release=80,loudnorm=I=-18:TP=-2:LRA=7,adelay=7500|7500[a3];\
    [4:a]atempo=1.08,highpass=f=100,lowpass=f=9500,acompressor=threshold=-20dB:ratio=2.8:attack=4:release=70,loudnorm=I=-18:TP=-2:LRA=7,adelay=9170|9170[a4];\
    [5:a]atempo=1.18,highpass=f=90,lowpass=f=9000,acompressor=threshold=-21dB:ratio=2.6:attack=5:release=80,loudnorm=I=-18:TP=-2:LRA=7,adelay=10580|10580[a5];\
    [6:a]atempo=1.30,highpass=f=90,lowpass=f=9000,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=80,loudnorm=I=-18:TP=-2:LRA=7,adelay=12360|12360[a6];\
    [7:a]volume=0.72[bed];\
    [a0][a1][a2][a3][a4][a5][a6]amix=inputs=7:normalize=0[voice];\
    [bed][voice]amix=inputs=2:weights='3 1':normalize=0,loudnorm=I=-16:TP=-1.5:LRA=7,atrim=0:15[aout]" \
  -map "[aout]" -c:a aac -b:a 256k "$TMP/final_audio.m4a"

ffmpeg -y -hide_banner -loglevel error \
  -loop 1 -t 1.90 -i "$ROOT/03_SCRIPTS/ref_images/09_professional_morning_takosan_clip1_ref.png" \
  -loop 1 -t 5.60 -i "$ROOT/03_SCRIPTS/ref_images/09_professional_morning_takosan_clip2_ref.png" \
  -loop 1 -t 7.50 -i "$ROOT/03_SCRIPTS/ref_images/09_professional_morning_takosan_clip3_ref.png" \
  -i "$TMP/final_audio.m4a" \
  -filter_complex "\
    [0:v]scale=2048:1365,crop=1920:1080,zoompan=z='min(zoom+0.00035,1.025)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=57:s=1920x1080:fps=30,setsar=1[v0];\
    [1:v]scale=2048:1365,crop=1920:1080,zoompan=z='min(zoom+0.00022,1.038)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=168:s=1920x1080:fps=30,setsar=1[v1];\
    [2:v]scale=2048:1365,crop=1920:1080,zoompan=z='min(zoom+0.00018,1.042)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=225:s=1920x1080:fps=30,setsar=1[v2];\
    [v0][v1][v2]concat=n=3:v=1:a=0,eq=contrast=1.05:saturation=0.82:brightness=-0.015,vignette=PI/6[vout]" \
  -map "[vout]" -map 3:a -t 15 -r 30 \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p \
  -c:a copy -movflags +faststart "$OUT"

print "$OUT"
