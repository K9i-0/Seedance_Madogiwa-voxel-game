# 感謝のバグ仕込み一万回 — Ten Thousand Bugs of Gratitude

Local full-offline production (MiniMax H3 via ComfyUI). Total length 86.6s, 16:9, native 768p.

Chapter durations below are final: every one was re-fitted to H3's 17k+5-frame grid (24fps) **after** the
wavs existed, so each chapter is long enough to hold its actual narration/dialogue take.

- Source story: user-supplied (a Baki-style "感謝の正拳突き" parody set in the Window-Side Tribe area).
- Story Formula check: Yametaro starts something strange (a 10,000-rep gratitude bug-planting ritual) → a colleague gets pulled in (Fukuchan) → a small commotion (100 incident notifications) → everyone ends up smiling.
- Tone guard: this is harmless slapstick. NO black-company depiction, NO bullying, NO power harassment, NO depressive arc, NO gore. Yametaro is always cheerful/serene about his own nonsense — never pitiful, never tragic. Nobody is scolded, blamed, or punished; nobody suffers.
- Mode split: **every narration chapter is I2V** (strict first/last-frame anchoring, no audio input — narration is laid over the video with ffmpeg during assembly). **Only the two on-screen dialogue chapters are R2V**, because R2V is the only mode that accepts audio for lip-sync.

## Character references (bundled in this directory)

- `Yametaro_sheet.png` — Yametaro's character model sheet (turnaround + NG-element close-ups). Identity/design reference only, NOT a composition reference.
- `Fukuchan_sheet.png` — Fukuchan's character model sheet (turnaround, expressions, outfit details). Identity/design reference only, NOT a composition reference.
- `height_lineup.png` — height/scale reference for relative body sizes. NOT a composition reference.

Canonical identity phrases (use verbatim, never paraphrase per chapter):

- **Yametaro** — the tiny chibi cartoon middle-aged man with an oversized head, black bowl-cut hair, small round white glasses, pink blush cheeks and a purple shirt (much shorter than every human character).
- **Fukuchan** — the slim, stylish 170cm 48-year-old black-haired man in a loose black long coat over a white graphic T-shirt, with a lanyard name tag, always smiling warmly.

Scale: Yametaro is roughly 90 cm tall — the top of his head reaches only to Fukuchan's hip.

## Style block (append VERBATIM to the end of EVERY keyframe generation prompt)

> Photorealistic live-action-style cinematic still: a real high-rise Tokyo office interior, true-to-life materials, real daylight, shallow depth of field, real camera optics. Every human character is rendered as a REAL PHOTOGRAPHED PERSON. Yametaro ALONE is rendered as a soft matte 3D chibi toy figure — smooth matte vinyl-toy surfaces, thick dark outline, oversized head, roughly 90 cm tall — standing physically inside that real space and lit by the same real light. NOT flat 2D anime, NOT cartoon lineart, NOT a drawing, NOT a painting. Single still frame, one coherent scene, no text overlay, no sheet-style panels, no labels, no watermark, no readable letters anywhere in frame.

Rationale (do not change mid-run): the established look of this IP is a photorealistic live-action space in which the photographic members and the matte 3D chibi Yametaro coexist. Never write `anime style` or `cartoon style` into a keyframe prompt for this run.

## NG-change elements (restate in EVERY frame prompt, positive + negative form)

- Yametaro **always wears SMALL ROUND WHITE-RIMMED glasses** — NOT rectangular, NOT thick dark-rimmed, and the glasses do NOT disappear in any frame.
- Yametaro keeps his **oversized head, black bowl-cut hair with a pointed widow's peak, pink blush cheeks, purple patterned shirt and black trousers** — the design never shifts toward a realistic human.
- Fukuchan keeps his **loose black long coat over a white graphic T-shirt, white sneakers, and the lanyard name tag** — NOT a suit, NOT a plain shirt; the lanyard does NOT disappear.
- Fukuchan's canonical **"ギュンギュン" pose** (both palms pressed to his own cheeks) is his and only his; Yametaro never does it.

## Set (constant across all chapters)

The Window-Side Tribe area on a high floor of Accidenture Inc. A floor-to-ceiling glass curtain wall on frame right with Tokyo Tower visible outside. Yametaro's DIY workstation on frame left-of-centre: a corrugated **cardboard desk**, and the **"Aaronchure"** chair behind it (a stack of cardboard boxes used as a seat). On the desk, left to right: three crushed empty cans, an EMPTY glass beer mug, an OPEN laptop, and a thick paper spec booklet (仕様書). A plain navy noren hangs on the back wall with a red paper lantern beside it. All cardboard signage and the noren carry only abstract brush-like marks — **no readable letters anywhere**.

### Known deviation — Yametaro's seat

The keyframes render Yametaro on a **black office chair**, not seated on the Aaronchure
cardboard-box stack, and the box stack appears beside/behind him instead. Qwen Image Edit
kept drawing an office chair even with explicit negative prompting ("NO normal office chair,
NO leather chair, NO swivel chair anywhere in the frame") across two attempts.

Accepted rather than fought, because it is set dressing — not an NG-change element, not a
prop-state transition and not a physics violation. The Motion prompts above were reworded to
match the actual anchor frames ("his chair"), so H3 is never asked to morph the seat between
a keyframe and its prompt. The cardboard boxes, cardboard desk, noren and lantern still carry
the Window-Side Tribe read.

## Prop state ledger (single source of truth — each column is ONE shared keyframe)

Columns are keyframe boundaries. Where a chapter's end and the next chapter's start share a column, they are literally the same PNG file.

| Prop | C1 start | C1 end = C2 start | C2 end = C3 start | C3 end = C4 start | C4 end | C5 start (hard cut) | C5 end = C6 start | C6 end = C7 start | C7 end | C8 start (hard cut) | C8 end | C9 start (hard cut) | C9 end = C10 start | C10 end = C11 start | C11 end |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Spec booklet (仕様書) | OPEN flat, pages up | OPEN flat | OPEN flat | CLOSED | CLOSED | CLOSED, thin film of dust | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty | CLOSED, dusty |
| Laptop screen | DARK (asleep) | DARK | DARK | ONE red error banner | ONE red error banner | ONE red error banner | ONE red error banner | FULL WALL of red error bars | FULL WALL of red bars | FULL WALL of red bars | FULL WALL of red bars | FULL WALL of red bars | FULL WALL of red bars | FULL WALL of red bars | FULL WALL of red bars |
| Laptop lid | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° | OPEN ~100° |
| Beer mug | EMPTY, on desk | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY |
| Empty cans (2 crushed + 1 upright) | exactly 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 |
| Paper inquiry slips (cardboard tray) | EMPTY tray | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | EMPTY | TALL overflowing stack | TALL stack | TALL stack | TALL stack | TALL stack | TALL stack | TALL stack | TALL stack |
| Fukuchan's phone | (Fukuchan absent) | absent | absent | absent | absent | absent | in his hand, screen DARK | screen DARK | screen DARK | screen DARK | screen DARK | screen DARK | screen DARK | FULL of notification cards | FULL of notification cards |
| Daylight | soft morning | soft morning | gentle golden afternoon light | warm golden | deep orange dusk | bright midday | bright midday | bright midday | bright midday | bright midday | bright midday | bright midday | bright midday | bright midday | bright midday |

Ledger logic check (left to right):

- The booklet goes OPEN → CLOSED exactly once, at the C3 end column, and C3's Motion prompt shows him closing it on screen.
- The screen goes DARK → ONE red banner inside C3 (he types, it breaks — shown on screen), then ONE → FULL WALL inside C6 (the bars cascade by themselves — shown on screen). No other transitions.
- The inquiry-slip tray goes EMPTY → TALL inside C6, shown on screen as slips piling up by themselves.
- Fukuchan's phone goes DARK → FULL of notifications inside C10, shown on screen as cards flooding in.
- The dust on the booklet and Fukuchan's arrival both land across the **C4 end → C5 start hard cut**, which is an explicit two-year time skip stated by the narration ("二年が過ぎたころ"). No prop is silently reset: the booklet stays CLOSED, the mug stays EMPTY, the can count stays 3, and the screen keeps the same single red banner across that cut.
- The beer mug is EMPTY in every column and nobody ever drinks, pours, or lifts it. The can count never changes.

## Fixture layout (constant across ALL chapters — hinges and handles never move)

| Fixture | Hinge side (from camera) | Handle | Opens |
|---|---|---|---|
| Yametaro's laptop | hinge runs along the REAR edge of the base (the far side from camera); the lid tilts away from camera toward the window | no handle or latch of any kind | stays OPEN at a constant ~100° in every single frame — it never closes, never changes angle, and the hinge never moves to the front edge |
| Window wall (frame right) | none — a fixed floor-to-ceiling glass curtain wall | none | never opens; there is no openable sash, no hinge and no handle on it |

The laptop's hinge stays on the rear edge and its lid angle stays identical in every frame of every chapter. The window wall has no hardware at all — do not add a handle, latch or hinge to it in any frame.

## Dialogue audio (all voices pre-generated locally — H3 must NOT generate any voice)

Voice casting per `02_CHARACTERS/VOICE_CAST.md`. **No VOICEVOX voice is used in this run** — every voice is Irodori-TTS, so no on-screen VOICEVOX credit is required (see Credits).

| File | Chapter | Character | Voice (engine) | Line (ja) | Duration |
|---|---|---|---|---|---|
| `ch1_nar1.wav` | 1 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | やめ太郎、43歳。己のエンジニア人生に限界を感じ、悩みに悩み抜いた結果、やめ太郎がたどり着いたのは、感謝であった。 | 11.12s |
| `ch2_nar1.wav` | 2 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | 一日一万回。感謝のバグ仕込み。 | 4.19s |
| `ch3_nar1.wav` | 3 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | 祈る。仕様書を閉じる。実装する。壊す。謝る。 | 6.79s |
| `ch4_nar1.wav` | 4 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | この一連の動作を一回として、完了までに当初は十八時間を要した。 | 5.58s |
| `ch5_nar1.wav` | 5 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | 二年が過ぎたころ、異変が起きた。一万回のバグ仕込みを終えても、日が暮れていない。 | 6.51s |
| `ch6_nar1.wav` | 6 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | 増えていたのは、エラーログと問い合わせ、そして誰にも再現できない不具合だけ。バグを作る速度が、レビューを置き去りにした。 | 10.32s |
| `ch7_nar1.wav` | 7 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | タイピングの音は消えた。ただ祈りを終えた瞬間、本番環境のどこかが静かに壊れている。 | 8.00s |
| `ch8_line1_fukuchan.wav` | 8 | Fukuchan | Irodori-TTS (ref: Fukuchan_voice.wav, seed 42) | やめ太郎さん……今、何をしていたんですか？ | 4.24s |
| `ch9_line1_yametaro.wav` | 9 | Yametaro | Irodori-TTS (ref: Yametaro_voice.wav, seed 7) | 何もしてへんで | 2.00s (padded from 1.22s) |
| `ch10_nar1.wav` | 10 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | その直後、Slackに障害通知が百件流れた。 | 4.36s |
| `ch11_nar1.wav` | 11 | Narrator | Irodori-TTS (ref: Narrator_voice.wav, seed 100) | 後にこの技は、畏怖を込めてこう呼ばれる。究極奥義、何もしてないのに壊れた。なお、本人は現在も原因究明のため祈り続けている。 | 12.67s |

- Durations above are the generator's reported post-trim lengths (measured, not estimated). H3 requires every attached audio file to be **at least 2.0s**; `ch9_line1_yametaro.wav` came out at 1.22s and was padded at the END only (never the head) with `apad=whole_dur=2.0`.
- **Chapter 9 lip-sync caveat:** the skill's rule is that real speech should not fall below ~60% of a chapter's length. Chapter 9's real speech is 1.22s against a 3.75s chapter (33%), because 90 frames is the SMALLEST duration H3's 17k+5 grid allows — the chapter cannot be made shorter. The Motion prompt therefore leans hard on the timing constraint ("begins the line almost immediately… his mouth moves ONLY while <Audio 1> is playing; once the line ends his mouth stays CLOSED"). **Check this chapter's lip-flap specifically during the pilot pass**; if the mouth keeps moving through the trailing silence, the fix is to re-record the line with a slower delivery (a longer real take), not to shorten the chapter.
- Only chapters 8 and 9 attach audio to the generator. Every narration wav is laid over the finished video with ffmpeg at assembly time and is never attached to H3.

## Keyframe inventory (15 distinct PNGs; shared boundaries reuse the same file)

| File | Role |
|---|---|
| `ch1_start.png` | C1 first frame |
| `ch1_end.png` | C1 last frame = C2 first frame |
| `ch2_end.png` | C2 last frame = C3 first frame |
| `ch3_end.png` | C3 last frame = C4 first frame |
| `ch4_end.png` | C4 last frame |
| `ch5_start.png` | C5 first frame (hard cut — two-year time skip, new shot) |
| `ch5_end.png` | C5 last frame = C6 first frame |
| `ch6_end.png` | C6 last frame = C7 first frame |
| `ch7_end.png` | C7 last frame |
| `ch8_start.png` | C8 first frame (hard cut — new two-shot camera for the dialogue) |
| `ch8_end.png` | C8 last frame |
| `ch9_start.png` | C9 first frame (hard cut — new close single for the punchline) |
| `ch9_end.png` | C9 last frame = C10 first frame |
| `ch10_end.png` | C10 last frame = C11 first frame |
| `ch11_end.png` | C11 last frame |

Generation chain order (each frame is seeded from the previous one; never generate a frame from scratch): `ch1_start` (from a stitched sheet canvas) → `ch1_end` → `ch2_end` → `ch3_end` → `ch4_end` → `ch5_start` (new shot, seeded from `ch4_end`) → `ch5_end` → `ch6_end` → `ch7_end` → `ch8_start` (new camera, seeded from `ch7_end`) → `ch8_end` → `ch9_start` (new camera, seeded from `ch8_end`) → `ch9_end` → `ch10_end` → `ch11_end`.

Because Yametaro appears in all 15 frames, **re-inject `Yametaro_sheet.png` via a stitched reference canvas every 3rd frame** (`ch3_end`, `ch5_end`, `ch7_end`, `ch9_end`, `ch11_end`) to pull his design back before it drifts. Fukuchan's sheet is re-injected at `ch5_end` (his first appearance) and `ch8_start`.

Seeds used are recorded in the Keyframe generation log at the bottom of this file.

---

## Chapter 1 — "…what he arrived at was gratitude."

- Shot: static medium shot, camera at Yametaro's eye level, cardboard desk in the near foreground, window and Tokyo Tower on frame right. Soft morning light.
- First frame: Yametaro sits on his chair behind the cardboard desk, with the Aaronchure cardboard-box stack beside him, slumped forward and deflated, shoulders dropped, both small hands limp on the desktop, looking down at the OPEN spec booklet with a small flat mouth. Laptop lid OPEN ~100°, screen DARK. EMPTY beer mug and exactly 3 crushed cans on the desk. Cardboard tray EMPTY.
- Last frame: Yametaro sits bolt upright, palms pressed flat together in front of his chest in a serene prayer, eyes closed, a small calm smile. Everything else on the desk is unchanged (booklet still OPEN, screen still DARK).
- Prop states: spec booklet OPEN → OPEN. Laptop screen DARK → DARK. Mug EMPTY → EMPTY. Cans 3 → 3.

### H3 inputs (Chapter 1)
- Mode: I2V
- First frame: `ch1_start.png`
- Last frame: `ch1_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. In one continuous static medium shot in a real high-rise Tokyo office, the tiny matte 3D chibi figure Yametaro — oversized head, black bowl-cut hair, SMALL ROUND WHITE-RIMMED glasses, pink blush cheeks, purple patterned shirt — begins slumped forward and deflated over the cardboard desk, staring down at the OPEN paper spec booklet. Over the shot he slowly draws his shoulders back, straightens up on the stack of cardboard boxes he is sitting on, and brings both small hands up to press his palms flat together in front of his chest in a calm prayer, closing his eyes into a serene little smile by the final frame. His glasses stay SMALL, ROUND and WHITE-RIMMED for every frame — NOT rectangular, NOT thick dark-rimmed — and the glasses do NOT disappear. His mouth stays CLOSED the entire time: no speech, no lip movement, no narration, ambient room tone only. The spec booklet stays OPEN and flat on the desk and is NOT touched, NOT closed and NOT moved in this chapter. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera, and its screen stays completely DARK — it does not light up. The EMPTY glass beer mug stays EMPTY and untouched on the desk and nobody drinks, lifts or pours anything; exactly three crushed empty cans stay where they are and their number does not change; the cardboard tray stays EMPTY. The window wall on frame right has no hinge, handle or latch. Soft morning light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no captions, no watermark anywhere in frame. Nobody is scolded or blamed; the mood is gentle and comedic, never gloomy or pitiful.
- Duration: 12s requested (grid-rounded to 294 frames = 12.250s at 24fps) / Aspect: 16:9 (native 768p — output rounds to 1344x768)
- Narration laid over at assembly: `ch1_nar1.wav`

---

## Chapter 2 — "Ten thousand a day."

- Shot: same framing as C1, an almost imperceptible push in. The morning light ramps up into a gentle golden afternoon light through the window.
- First frame: identical to `ch1_end.png` — Yametaro upright, palms together, eyes closed, serene.
- Last frame: same pose held exactly, but the light has ramped to a gentle golden afternoon light raking across the desk, a warm rim-light on his oversized head and a faint golden glow between his pressed palms.
- Prop states: everything unchanged. Only the light changes.

### H3 inputs (Chapter 2)
- Mode: I2V
- First frame: `ch1_end.png`
- Last frame: `ch2_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous shot with an almost imperceptible slow push toward the tiny matte 3D chibi figure Yametaro, who holds his palms pressed flat together in front of his chest in a completely still prayer, eyes closed, with a serene little smile. He does NOT change pose, does NOT lower his hands and does NOT move from his chair. His mouth stays CLOSED throughout: no speech, no lip movement, no narration, ambient room tone only. The only thing that changes is the light: the soft morning daylight coming through the floor-to-ceiling window warms into a gentle golden afternoon light that rakes softly across the cardboard desk and puts a warm rim-light on his oversized head, correctly exposed and never blown out (his hair stays clearly BLACK and his shirt clearly PURPLE), and a faint golden glow gathers between his pressed palms by the final frame. His glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. The paper spec booklet stays OPEN and flat and is NOT touched. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera, and its screen stays completely DARK. The EMPTY beer mug stays EMPTY and untouched, nobody drinks or pours anything, exactly three empty cans (two crushed, one upright) stay unchanged, and the cardboard tray stays EMPTY. The window wall has no hinge, handle or latch. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no captions, no watermark anywhere in frame.
- Duration: 5s requested (grid-rounded to 124 frames = 5.167s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch2_nar1.wav`

---

## Chapter 3 — The ritual: pray, close the spec, implement, break, apologise.

- Shot: same framing, static. The full five-step ritual performed once, briskly and comically.
- First frame: identical to `ch2_end.png` — palms together, golden light, booklet OPEN, screen DARK.
- Last frame: the spec booklet is CLOSED flat on the desk, the laptop screen shows ONE red error banner (an abstract red bar, no readable text), and Yametaro is bowing his head over his pressed palms in a small apology, eyes squeezed shut.
- Prop states: spec booklet OPEN → **CLOSED** (he closes it on screen). Laptop screen DARK → **ONE red error banner** (he types and it breaks on screen). Mug EMPTY → EMPTY. Cans 3 → 3. Tray EMPTY → EMPTY.

### H3 inputs (Chapter 3)
- Mode: I2V
- First frame: `ch2_end.png`
- Last frame: `ch3_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous static shot in which the tiny matte 3D chibi figure Yametaro performs a brisk five-beat comic ritual exactly once. Beat one: he holds his palms pressed together in prayer and gives one small nod. Beat two: he opens his palms, reaches across the cardboard desk with both small hands and CLOSES the OPEN paper spec booklet flat without reading a single page — the booklet clearly starts OPEN and is CLOSED by his own visible hand movement, and it stays CLOSED for the rest of the shot. Beat three: he turns to the OPEN laptop and hammers the keyboard rapidly with both tiny hands for about a second. Beat four: the completely DARK laptop screen flashes once and settles into ONE single red error banner — an abstract solid red horizontal bar with absolutely NO readable text or letters on it. Beat five: he instantly presses his palms flat together again and bows his oversized head low over them in a small apology, squeezing his eyes shut, holding that bow on the final frame. His mouth stays CLOSED the whole time: no speech, no lip movement, no narration, ambient room tone and keyboard clatter only. His glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear or slip off during the bow; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera — the lid never closes and never changes angle even while he types. The EMPTY glass beer mug stays EMPTY and untouched, nobody drinks, lifts or pours anything, exactly three empty cans (two crushed, one upright) stay unchanged, and the cardboard tray stays EMPTY. The window wall has no hinge, handle or latch. Gentle warm golden daylight holds steady, correctly exposed. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. The apology is a light comic bow — nobody is scolded, blamed or punished, and the mood stays cheerful.
- Duration: 7s requested (grid-rounded to 175 frames = 7.292s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch3_nar1.wav`

---

## Chapter 4 — Eighteen hours per rep, then sleep.

- Shot: same framing, static, but the daylight time-lapses from warm gold down to deep orange dusk.
- First frame: identical to `ch3_end.png` — booklet CLOSED, ONE red banner, Yametaro bowing over pressed palms.
- Last frame: deep orange dusk, Tokyo Tower lit outside. Yametaro has collapsed face-down onto the cardboard desk, one cheek resting on the CLOSED booklet, arms dangling limp at his sides, fast asleep with a tiny contented smile. The single red error banner glows in the dimmer room.
- Prop states: everything holds. Booklet CLOSED → CLOSED. Screen ONE red banner → ONE red banner. Mug EMPTY → EMPTY. Cans 3 → 3. Tray EMPTY → EMPTY. Light: warm gold → deep orange dusk.

### H3 inputs (Chapter 4)
- Mode: I2V
- First frame: `ch3_end.png`
- Last frame: `ch4_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous static shot that time-lapses a single working day. The tiny matte 3D chibi figure Yametaro repeats his short ritual — press palms together, one nod, a quick burst of typing on the OPEN laptop, then a small bow over his pressed palms — in fast rhythmic loops, several times, with light motion blur on his small hands to sell the repetition. At the same time the daylight through the floor-to-ceiling window sweeps continuously from gentle golden afternoon light, through warm afternoon, into a deep orange dusk, and Tokyo Tower lights up outside. In the final beats his loops slow, wobble, and he pitches forward and lands face-down on the cardboard desk, one cheek on the CLOSED paper spec booklet, arms hanging limp at his sides, fast asleep with a tiny contented smile on the last frame. His mouth stays CLOSED the whole time: no speech, no lip movement, no narration, ambient room tone and keyboard clatter only. His glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they stay on his face even when he lands face-down; they do NOT disappear. His black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. The paper spec booklet stays CLOSED for the entire shot and is never reopened. The laptop screen keeps exactly ONE single red error banner — an abstract solid red horizontal bar with NO readable text — and it does not multiply or change in this chapter. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera; it never closes even when he collapses. The EMPTY glass beer mug stays EMPTY and untouched, nobody drinks, lifts or pours anything, exactly three empty cans (two crushed, one upright) stay unchanged, and the cardboard tray stays EMPTY. The window wall has no hinge, handle or latch. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. He is happily exhausted, not suffering — comedic, never gloomy, and nobody is overworked by anyone else; this is entirely his own hobby.
- Duration: 6.5s requested (grid-rounded to 158 frames = 6.583s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch4_nar1.wav`

---

## Chapter 5 — Two years later: the sun hasn't moved.

**Hard cut.** `ch5_start.png` is a NEW frame (a two-year time skip and a slightly wider camera), so it is generated from `ch4_end.png` as a seed rather than shared with it. Prop states carry across the cut unchanged except for the dust, which the narration explains.

- Shot: same set, camera pulled back slightly so the mid-background floor is visible on frame left. Bright midday light.
- First frame: bright midday. Yametaro sits upright on his chair, palms pressed flat together, eyes closed, just finishing a prayer. The CLOSED spec booklet now carries a thin film of dust. ONE red error banner on the screen. No Fukuchan yet.
- Last frame: Yametaro has opened his eyes and tipped his oversized head back to look up and out of the window, small round eyes wide, eyebrows raised, mouth closed in a puzzled flat line — the sun is still high. Behind him in the mid-background, Fukuchan has walked into frame and stands a few steps away, smiling warmly, holding a smartphone with a DARK screen at his side, mouth CLOSED.
- Prop states: booklet CLOSED+dusty → CLOSED+dusty. Screen ONE red banner → ONE red banner. Mug EMPTY → EMPTY. Cans 3 → 3. Tray EMPTY → EMPTY. Fukuchan's phone: absent → in hand, screen DARK.

### H3 inputs (Chapter 5)
- Mode: I2V
- First frame: `ch5_start.png`
- Last frame: `ch5_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous shot in bright midday light. The tiny matte 3D chibi figure Yametaro sits upright in his chair with his palms pressed flat together, finishing a prayer; he opens his small round eyes, then slowly tips his oversized head back and looks up and out through the floor-to-ceiling window with his eyebrows raised in genuine puzzlement, because the sun is still high in the sky. He holds that puzzled upward look on the final frame. His mouth stays CLOSED the entire time: no speech, no lip movement, no narration, ambient room tone only. Meanwhile, in the mid-background on frame left, Fukuchan — the slim, stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag — an ADULT MAN WITH NORMAL HUMAN PROPORTIONS and a normal-sized head, NOT a chibi figure and NOT a toy, and MUCH TALLER than Yametaro, whose whole body only reaches Fukuchan's hip — walks calmly into frame, stops a few steps behind Yametaro and stands there smiling warmly, holding a smartphone with a completely DARK screen down at his side. Fukuchan does NOT speak: his mouth stays CLOSED and he only watches. Fukuchan keeps his loose black long coat, white graphic T-shirt, white sneakers and lanyard name tag — NOT a suit, and the lanyard does NOT disappear. Fukuchan is rendered as a real photographed person and is far taller than Yametaro, whose head only reaches Fukuchan's hip. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. The paper spec booklet stays CLOSED with its thin film of dust and is never opened or touched. The laptop screen keeps exactly ONE single red error banner — an abstract solid red horizontal bar with NO readable text — and does not multiply in this chapter. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The EMPTY glass beer mug stays EMPTY and untouched, nobody drinks, lifts or pours anything, exactly three empty cans (two crushed, one upright) stay unchanged, and the cardboard tray stays EMPTY. The window wall has no hinge, handle or latch. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no captions, no watermark anywhere in frame. Friendly, curious, comedic mood.
- Duration: 7s requested (grid-rounded to 175 frames = 7.292s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch5_nar1.wav`

---

## Chapter 6 — Only the error logs and the inquiries grew.

- Shot: slow push from the wide two-figure framing in toward the laptop screen and the cardboard tray beside it.
- First frame: identical to `ch5_end.png`.
- Last frame: the laptop screen is a FULL WALL of cascading red error bars (abstract, no readable text), and the cardboard tray beside the laptop has become a tall, overflowing stack of paper inquiry slips. Yametaro sits with both hands resting in his lap, having touched nothing, blinking at the screen. Fukuchan still stands in the mid-background, smiling, phone screen still DARK, mouth CLOSED.
- Prop states: screen ONE red banner → **FULL WALL of red bars** (the bars cascade on their own, on screen). Tray EMPTY → **TALL overflowing stack** (slips pile up by themselves, on screen). Booklet CLOSED+dusty → unchanged. Mug EMPTY → EMPTY. Cans 3 → 3. Fukuchan's phone DARK → DARK.

### H3 inputs (Chapter 6)
- Mode: I2V
- First frame: `ch5_end.png`
- Last frame: `ch6_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous shot with a slow, steady camera push from the wide framing in toward the OPEN laptop and the cardboard tray beside it. Two things multiply entirely by themselves, with nobody touching anything: first, the single red error banner on the laptop screen cascades and multiplies downward into a FULL WALL of stacked red error bars that fills the whole screen — all of them abstract solid red horizontal bars with absolutely NO readable text, letters or code; second, the EMPTY cardboard tray beside the laptop fills up as paper inquiry slips drop into it one after another until it is a tall, overflowing stack by the final frame. The tiny matte 3D chibi figure Yametaro does NOT touch the keyboard, the tray or the slips: he keeps both small hands resting in his lap the entire shot and simply blinks at the screen with mild confusion. His mouth stays CLOSED the whole time: no speech, no lip movement, no narration, ambient room tone only. In the mid-background Fukuchan — the slim, stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag — an ADULT MAN WITH NORMAL HUMAN PROPORTIONS and a normal-sized head, NOT a chibi figure and NOT a toy, and MUCH TALLER than Yametaro, whose whole body only reaches Fukuchan's hip — stays where he is, smiling warmly and watching, still holding his smartphone with a completely DARK screen; Fukuchan does NOT speak, his mouth stays CLOSED, and his phone screen does NOT light up in this chapter. Fukuchan keeps the loose black long coat, white graphic T-shirt, white sneakers and lanyard name tag — NOT a suit, and the lanyard does NOT disappear. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. The paper spec booklet stays CLOSED and dusty and is never opened. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The EMPTY glass beer mug stays EMPTY and untouched, nobody drinks, lifts or pours anything, and exactly three empty cans (two crushed, one upright) stay unchanged. The window wall has no hinge, handle or latch. Bright midday light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. Nobody is angry, blamed or in trouble — the tone is deadpan comedy.
- Duration: 11.5s requested (grid-rounded to 277 frames = 11.542s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch6_nar1.wav`

---

## Chapter 7 — The typing sound is gone.

- Shot: starts tight on the laptop and Yametaro's hands, then eases back slightly to include his face.
- First frame: identical to `ch6_end.png`.
- Last frame: Yametaro's palms are pressed together in a finished prayer and lowering toward his lap; the keyboard directly in front of him is perfectly still and carries a light film of dust, not one key depressed; the red wall on the screen has scrolled one notch further on its own. Fukuchan is still in the mid-background, smiling, phone DARK, mouth CLOSED.
- Prop states: everything holds. Screen FULL WALL → FULL WALL (scrolled one notch). Tray TALL → TALL. Booklet CLOSED+dusty → unchanged. Mug EMPTY → EMPTY. Cans 3 → 3.

### H3 inputs (Chapter 7)
- Mode: I2V
- First frame: `ch6_end.png`
- Last frame: `ch7_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous shot that eases back slightly from the laptop to include the face of the tiny matte 3D chibi figure Yametaro. He presses his palms flat together in front of his chest, holds one short still prayer with his eyes closed, then opens his eyes and lets his pressed hands sink slowly toward his lap by the final frame. The keyboard directly in front of him stays completely untouched and motionless for the entire shot, carrying a light film of dust — not one key is pressed, not one finger touches it, and there is NO typing sound at all, only quiet room tone. Exactly once, and entirely on its own with nobody touching anything, the FULL WALL of red error bars on the laptop screen scrolls one notch further down; every bar stays an abstract solid red horizontal shape with absolutely NO readable text, letters or code. His mouth stays CLOSED the whole time: no speech, no lip movement, no narration. In the mid-background Fukuchan — the slim, stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag — an ADULT MAN WITH NORMAL HUMAN PROPORTIONS and a normal-sized head, NOT a chibi figure and NOT a toy, and MUCH TALLER than Yametaro, whose whole body only reaches Fukuchan's hip — stays where he is, smiling warmly and watching, still holding his smartphone with a completely DARK screen; Fukuchan does NOT speak, his mouth stays CLOSED, and his phone screen does NOT light up in this chapter. Fukuchan keeps the loose black long coat, white graphic T-shirt, white sneakers and lanyard name tag — NOT a suit, and the lanyard does NOT disappear. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. The paper spec booklet stays CLOSED and dusty; the cardboard tray keeps its tall stack of paper slips and does not empty. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The EMPTY glass beer mug stays EMPTY and untouched, nobody drinks, lifts or pours anything, and exactly three empty cans (two crushed, one upright) stay unchanged. The window wall has no hinge, handle or latch. Bright midday light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. Calm, eerie-but-friendly comedy; nobody is upset or blamed.
- Duration: 8.5s requested (grid-rounded to 209 frames = 8.708s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch7_nar1.wav`

---

## Chapter 8 — Fukuchan asks. (dialogue, R2V)

**Hard cut** to a new two-shot camera, so `ch8_start.png` is a new frame seeded from `ch7_end.png`. Because this is a dialogue chapter, the speaker's mouth is drawn OPEN and the non-speaker's mouth CLOSED in **both** keyframes.

- Shot: static two-shot from slightly behind and beside the desk — Fukuchan standing on frame left leaning down toward the desk, Yametaro seated small on frame right.
- First frame: Fukuchan is crouched slightly toward Yametaro with his warm smile, mouth clearly OPEN mid-sentence, phone screen DARK in one hand. Yametaro is seated with his hands in his lap, mouth CLOSED, looking up at him.
- Last frame: Fukuchan finishing the question, still leaning in, mouth just closing, head tilted with friendly curiosity. Yametaro's mouth still CLOSED, eyes now wide.
- Line (lip-sync only — the voice comes from the attached pre-generated audio, NOT generated): Fukuchan: 「やめ太郎さん……今、何をしていたんですか？」
- Prop states: all unchanged from C7 end. Screen FULL WALL. Tray TALL. Booklet CLOSED+dusty. Mug EMPTY. Cans 3. Fukuchan's phone DARK.

### H3 inputs (Chapter 8)
- Mode: R2V
- Images (connection order = <Picture N> tags; max 9):
  - <Picture 1> = `ch8_start.png` — start keyframe; the video's FIRST frame
  - <Picture 2> = `ch8_end.png` — end keyframe; the video's LAST frame
  - <Picture 3> = `Fukuchan_sheet.png` — Fukuchan's character model sheet, identity/design reference only, NOT a composition reference
  - <Picture 4> = `Yametaro_sheet.png` — Yametaro's character model sheet, identity/design reference only, NOT a composition reference
  - <Picture 5> = `height_lineup.png` — height/scale reference for relative body sizes, NOT a composition reference
- Audio (max 3 files, each 2-15s, 15s total; attach in speaking order):
  - <Audio 1> = `ch8_line1_fukuchan.wav` — spoken by Fukuchan, use AS-IS as the dialogue audio
- Total input files: 6 / 12
- Motion prompt: Required attached input files: <Picture 1> = ch8_start.png — start keyframe, the video's FIRST frame; <Picture 2> = ch8_end.png — end keyframe, the video's LAST frame; <Picture 3> = Fukuchan_sheet.png — Fukuchan's character model sheet, identity/design reference only, NOT a composition reference; <Picture 4> = Yametaro_sheet.png — Yametaro's character model sheet, identity/design reference only, NOT a composition reference; <Picture 5> = height_lineup.png — height/scale reference for relative body sizes, NOT a composition reference; <Audio 1> = ch8_line1_fukuchan.wav — Fukuchan's spoken line. These attachments are REQUIRED inputs and must remain attached for this generation. The video starts EXACTLY on <Picture 1> and ends EXACTLY on <Picture 2>. One continuous static two-shot in a real high-rise Tokyo office: Fukuchan (<Picture 3>, the slim stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag) stands on frame left, leaning down toward the cardboard desk with a warm friendly smile, and Yametaro (<Picture 4>, the tiny matte 3D chibi figure with an oversized head, black bowl-cut hair, SMALL ROUND WHITE-RIMMED glasses, pink blush cheeks and a purple patterned shirt) sits small on frame right with both hands in his lap, looking up at him. ONLY Fukuchan speaks, lip-syncing to <Audio 1> — he begins the line almost immediately and his mouth moves ONLY while <Audio 1> is playing; once the line ends his mouth stays CLOSED for the rest of the chapter. As he asks, he tilts his head with gentle curiosity and makes one small open-palmed gesture toward the laptop. Yametaro does NOT speak — his mouth stays CLOSED for the entire chapter, he only listens and widens his small round eyes. Use <Audio 1> AS-IS as the dialogue audio and do NOT generate any voice — no synthesized speech, no narration, no second voice. The two do not overlap and there is only ever one voice. Fukuchan keeps the loose black long coat, white graphic T-shirt, white sneakers and lanyard name tag — NOT a suit — and the lanyard does NOT disappear; he never presses his palms to his own cheeks in this chapter. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear. Per <Picture 5>, Fukuchan is far taller than Yametaro: Yametaro's head only reaches Fukuchan's hip. The reference sheets' text labels must NOT appear in the video. Every prop stays exactly as it is: the laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet stays CLOSED and dusty, the EMPTY glass beer mug stays EMPTY and untouched with nobody drinking, lifting or pouring anything, exactly three empty cans (two crushed, one upright) stay unchanged, and Fukuchan's smartphone screen stays completely DARK. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The window wall has no hinge, handle or latch. Bright midday light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Fukuchan as a real photographed person and Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. This is a friendly, curious question between colleagues — no accusation, no blame, no anger, no interrogation.
- Duration: 5s requested (grid-rounded to 124 frames = 5.167s at 24fps) / Aspect: 16:9 (native 768p — output rounds to 1344x768)

---

## Chapter 9 — "I didn't do anything." (dialogue, R2V — the punchline)

**Hard cut** to a close single on Yametaro, so `ch9_start.png` is a new frame seeded from `ch8_end.png`. Speaker's mouth OPEN, non-speaker's CLOSED in both keyframes.

- Shot: static close single on Yametaro, low angle looking slightly up at him; Fukuchan's coat and lanyard are just visible, out of focus, at the frame edge.
- First frame: Yametaro has brought his palms flat together again in front of his chest, wearing a completely serene, gentle expression, mouth clearly OPEN mid-word.
- Last frame: same serene pose held, mouth just closing on the last syllable, eyes softly shut, the picture of innocence.
- Line (lip-sync only — the voice comes from the attached pre-generated audio, NOT generated): Yametaro: 「何もしてへんで」
- Prop states: all unchanged. Screen FULL WALL (visible out of focus). Tray TALL. Booklet CLOSED+dusty. Mug EMPTY. Cans 3. Fukuchan's phone DARK.

### H3 inputs (Chapter 9)
- Mode: R2V
- Images (connection order = <Picture N> tags; max 9):
  - <Picture 1> = `ch9_start.png` — start keyframe; the video's FIRST frame
  - <Picture 2> = `ch9_end.png` — end keyframe; the video's LAST frame
  - <Picture 3> = `Yametaro_sheet.png` — Yametaro's character model sheet, identity/design reference only, NOT a composition reference
  - <Picture 4> = `Fukuchan_sheet.png` — Fukuchan's character model sheet, identity/design reference only, NOT a composition reference
  - <Picture 5> = `height_lineup.png` — height/scale reference for relative body sizes, NOT a composition reference
- Audio (max 3 files, each 2-15s, 15s total; attach in speaking order):
  - <Audio 1> = `ch9_line1_yametaro.wav` — spoken by Yametaro, use AS-IS as the dialogue audio
- Total input files: 6 / 12
- Motion prompt: Required attached input files: <Picture 1> = ch9_start.png — start keyframe, the video's FIRST frame; <Picture 2> = ch9_end.png — end keyframe, the video's LAST frame; <Picture 3> = Yametaro_sheet.png — Yametaro's character model sheet, identity/design reference only, NOT a composition reference; <Picture 4> = Fukuchan_sheet.png — Fukuchan's character model sheet, identity/design reference only, NOT a composition reference; <Picture 5> = height_lineup.png — height/scale reference for relative body sizes, NOT a composition reference; <Audio 1> = ch9_line1_yametaro.wav — Yametaro's spoken line. These attachments are REQUIRED inputs and must remain attached for this generation. The video starts EXACTLY on <Picture 1> and ends EXACTLY on <Picture 2>. One continuous static close single in a real high-rise Tokyo office, framed low and looking slightly up at Yametaro (<Picture 3>, the tiny matte 3D chibi figure with an oversized head, black bowl-cut hair, SMALL ROUND WHITE-RIMMED glasses, pink blush cheeks and a purple patterned shirt), who holds both small palms pressed flat together in front of his chest with a completely serene, gentle, innocent expression. ONLY Yametaro speaks, lip-syncing to <Audio 1> — he begins the line almost immediately and his mouth moves ONLY while <Audio 1> is playing; once the line ends his mouth stays CLOSED for the rest of the chapter and his eyes settle softly shut. He keeps the pressed-palm pose throughout and does not stand up or turn away. Fukuchan (<Picture 4>, the slim stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag) is only partly visible and out of focus at the frame edge, and he does NOT speak — his mouth stays CLOSED and he does not move into focus. Use <Audio 1> AS-IS as the dialogue audio and do NOT generate any voice — no synthesized speech, no narration, no second voice. There is only ever one voice. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. Per <Picture 5>, Yametaro is far shorter than Fukuchan. The reference sheets' text labels must NOT appear in the video. Every prop stays exactly as it is: the out-of-focus laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet stays CLOSED and dusty, the EMPTY glass beer mug stays EMPTY and untouched with nobody drinking, lifting or pouring anything, exactly three empty cans (two crushed, one upright) stay unchanged, and Fukuchan's smartphone screen stays completely DARK. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The window wall has no hinge, handle or latch. Bright midday light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no captions, no watermark anywhere in frame. He is sincerely serene, not smug and not lying maliciously — the joke is that he genuinely believes it. Nobody is blamed or angry.
- Duration: 3.75s requested (grid-rounded to 90 frames = 3.750s at 24fps) / Aspect: 16:9 (native 768p — output rounds to 1344x768)

---

## Chapter 10 — A hundred incident notifications.

- Shot: same close-ish framing, then a quick rack of focus / small pan onto Fukuchan's phone.
- First frame: identical to `ch9_end.png` — Yametaro serene, palms together, eyes softly shut.
- Last frame: Fukuchan's smartphone, now in sharp focus, its screen packed edge to edge with a dense stack of rectangular notification cards (abstract grey-and-red blocks, no readable text). Fukuchan is looking down at it with delighted, unbothered surprise, eyebrows up, mouth CLOSED. Yametaro is still serene in the soft background.
- Prop states: Fukuchan's phone DARK → **FULL of notification cards** (they flood in on screen). Everything else unchanged.

### H3 inputs (Chapter 10)
- Mode: I2V
- First frame: `ch9_end.png`
- Last frame: `ch10_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous shot that begins on the serene tiny matte 3D chibi figure Yametaro with his palms pressed flat together and his eyes softly shut, then racks focus and pans slightly onto the smartphone in Fukuchan's hand. Yametaro does NOT move from his serene pressed-palm pose and his mouth stays CLOSED throughout. The smartphone screen starts completely DARK and then, entirely on its own, floods with a dense stack of rectangular notification cards that pile in rapidly one after another until they pack the screen edge to edge — all of them abstract grey-and-red rounded rectangles with absolutely NO readable text, letters, names or logos on them. Fukuchan — the slim, stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag — an ADULT MAN WITH NORMAL HUMAN PROPORTIONS and a normal-sized head, NOT a chibi figure and NOT a toy, and MUCH TALLER than Yametaro, whose whole body only reaches Fukuchan's hip — looks down at the phone with delighted, completely unbothered surprise, eyebrows raised; his mouth stays CLOSED and he does NOT speak. There is no speech, no lip movement and no narration in this chapter: only quiet room tone and a rapid flurry of soft notification chimes. Fukuchan keeps the loose black long coat, white graphic T-shirt, white sneakers and lanyard name tag — NOT a suit — and the lanyard does NOT disappear. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear. Every other prop stays exactly as it is: the laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet stays CLOSED and dusty, the EMPTY glass beer mug stays EMPTY and untouched with nobody drinking, lifting or pouring anything, and exactly three empty cans (two crushed, one upright) stay unchanged. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The window wall has no hinge, handle or latch. Bright midday light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Fukuchan as a real photographed person and Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. Nobody panics, nobody is scolded and nobody is in trouble — everyone stays cheerful and amused.
- Duration: 5s requested (grid-rounded to 124 frames = 5.167s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch10_nar1.wav`

---

## Chapter 11 — The ultimate secret technique, and he is still praying.

- Shot: one long, slow pull-back from the two of them out to a wide of the whole Window-Side Tribe area, Tokyo Tower in the window.
- First frame: identical to `ch10_end.png`.
- Last frame: a wide shot of the whole area. Yametaro is still seated in his chair with his palms pressed together, serene and glowing faintly in the midday shaft. Fukuchan has crouched down beside him, holding his phone out at arm's length to take a cheerful selfie with the two of them, both smiling, mouths CLOSED. The laptop's red wall glows on the desk beside them. Tokyo Tower stands in the window behind.
- Prop states: everything holds. Phone FULL of notification cards → same (now held out for the selfie). Screen FULL WALL. Tray TALL. Booklet CLOSED+dusty. Mug EMPTY. Cans 3.
- Ending check (Story Formula step 4): the final frame is two colleagues smiling together. Nobody is punished, nothing is grim.

### H3 inputs (Chapter 11)
- Mode: I2V
- First frame: `ch10_end.png`
- Last frame: `ch11_end.png`
- Motion prompt: The video starts EXACTLY on the first frame and ends EXACTLY on the last frame. One continuous, slow, steady camera pull-back from the close framing all the way out to a wide shot of the whole Window-Side Tribe office area, with Tokyo Tower visible through the floor-to-ceiling window. The tiny matte 3D chibi figure Yametaro stays seated in his chair with both small palms pressed flat together in a serene, unbroken prayer for the entire shot — he does NOT stand up, does NOT lower his hands and does NOT open his eyes, and a soft warm glow gathers gently around him in the midday shaft of light. His mouth stays CLOSED the whole time: no speech, no lip movement, no narration, only quiet room tone. As the camera widens, Fukuchan — the slim, stylish 170cm black-haired man in a loose black long coat over a white graphic T-shirt with a lanyard name tag — an ADULT MAN WITH NORMAL HUMAN PROPORTIONS and a normal-sized head, NOT a chibi figure and NOT a toy, and MUCH TALLER than Yametaro, whose whole body only reaches Fukuchan's hip — crouches down beside the little figure, holds his smartphone out at arm's length and takes one cheerful selfie of the two of them, grinning warmly; his mouth stays CLOSED and he does NOT speak. Fukuchan keeps the loose black long coat, white graphic T-shirt, white sneakers and lanyard name tag — NOT a suit — and the lanyard does NOT disappear. Yametaro's glasses stay SMALL, ROUND and WHITE-RIMMED in every frame — NOT rectangular, NOT thick dark-rimmed — and they do NOT disappear; his black bowl-cut hair, pink blush cheeks and purple patterned shirt stay exactly as they are. Yametaro is far shorter than Fukuchan; even crouching, Fukuchan is clearly bigger than the little figure. Every prop stays exactly as it is: Fukuchan's phone screen keeps its dense stack of abstract grey-and-red notification cards with NO readable text, the laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet stays CLOSED and dusty, the EMPTY glass beer mug stays EMPTY and untouched with nobody drinking, lifting or pouring anything, and exactly three empty cans (two crushed, one upright) stay unchanged. The laptop lid stays OPEN at a constant ~100° with its hinge on the REAR edge away from camera. The window wall has no hinge, handle or latch. Bright midday light holds steady. Photorealistic live-action-style cinematic scene, real office materials and real daylight, with Fukuchan as a real photographed person and Yametaro alone rendered as a soft matte 3D chibi toy figure lit by that same real light — NOT flat 2D anime, NOT cartoon lineart. No readable text, no letters, no code, no captions, no watermark anywhere in frame. Warm, funny, affectionate ending — two colleagues smiling together, nobody blamed, nobody punished, no gloom.
- Duration: 13.5s requested (grid-rounded to 328 frames = 13.667s at 24fps) / Aspect: 16:9 (native 768p)
- Narration laid over at assembly: `ch11_nar1.wav`

---

## Generation & assembly protocol (REQUIRED — read before generating any chapter)

### Step 1 — Pilot chapter first (batch generation is FORBIDDEN until the pilot passes)
Generate ONLY Chapter 8 (the first dialogue chapter), then verify ALL of the following:
- [ ] The dialogue in the output is driven by the attached wav (correct voice, no synthesized/doubled voice)
- [ ] The CORRECT character lip-syncs (Fukuchan's mouth moves only while <Audio 1> plays; Yametaro's mouth stays closed the whole chapter)
- [ ] The video starts/ends on (or acceptably close to) `ch8_start.png` / `ch8_end.png` — check R2V frame anchoring
- [ ] Motion, poses, prop states and fixture hardware match the Motion prompt, the Prop state ledger and the Fixture layout table
- [ ] Character identity and NG-change elements survive H3 generation (compare against `Fukuchan_sheet.png` / `Yametaro_sheet.png`: Yametaro's small round white-rimmed glasses present and round, Fukuchan's coat and lanyard present)
- [ ] Duration matches the H3 inputs table (remember the 17k+5-frame grid rounding)
If any check fails, fix the workflow inputs/prompt and regenerate the pilot until all pass.
Only then generate the remaining chapters, and re-run at least the audio + duration checks on each.

### Step 2 — Prompts are verbatim
Copy each chapter's Motion prompt into the workflow JSON EXACTLY as written here. Do NOT
summarize or shorten. If it seems too long, go back to the script and split the chapter.

### Step 3 — Final audio track (assembly)
The audio embedded in generated chapters is NOT the final dialogue audio. During assembly:
1. For every dialogue chapter (8 and 9), strip the embedded audio and lay the original wavs from the
   Dialogue audio table over the video, aligned to the frame where the speaker's mouth starts moving.
2. Narration chapters (1-7, 10, 11) are I2V and were generated with no audio input: keep their
   generated ambient audio if it is usable, and lay the matching narration wav over it with `amix`,
   confirming the narration is not doubled.
3. Play back the assembled video before delivery and confirm every line is the local
   Irodori-TTS take (the source wavs are the single source of truth).

### Step 4 — Burned-in title text (ffmpeg only — never via keyframes or H3)
The "究極奥義 / 何もしてないのに壊れた" title card is burned in with ffmpeg `drawtext` over Chapter 11,
because generated text in keyframes comes out garbled. Command in the Assembly section below.

## Assembly (ffmpeg)

Per-chapter audio. Narration chapters (`N` = 1,2,3,4,5,6,7,10,11) — mix the narration over the generated ambient bed, with `<offset_ms>` chosen so the line lands on the beat it describes:

```bash
ffmpeg -y -i chN.mp4 -i chN_nar1.wav -filter_complex "[1:a]adelay=<offset_ms>|<offset_ms>,apad[n];[0:a][n]amix=inputs=2:duration=first:dropout_transition=0[a]" -map 0:v -map "[a]" -c:v copy chN_final.mp4
```

Dialogue chapters (8 and 9) — discard the embedded audio entirely and use the local wav alone:

```bash
ffmpeg -y -i ch8.mp4 -i ch8_line1_fukuchan.wav -filter_complex "[1:a]adelay=<offset_ms>|<offset_ms>,apad[a]" -map 0:v -map "[a]" -c:v copy -shortest ch8_final.mp4
```

Concatenate all eleven chapters:

```bash
printf "file 'ch1_final.mp4'\nfile 'ch2_final.mp4'\nfile 'ch3_final.mp4'\nfile 'ch4_final.mp4'\nfile 'ch5_final.mp4'\nfile 'ch6_final.mp4'\nfile 'ch7_final.mp4'\nfile 'ch8_final.mp4'\nfile 'ch9_final.mp4'\nfile 'ch10_final.mp4'\nfile 'ch11_final.mp4'\n" > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final_draft.mp4
```

Burn in the title card over Chapter 11 (replace `<ch11_start_sec>` with Chapter 11's start time in the concatenated draft):

```bash
ffmpeg -y -i final_draft.mp4 -vf "drawtext=fontfile='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc':text='究極奥義':fontsize=44:fontcolor=white:borderw=3:bordercolor=black:x=(w-tw)/2:y=h*0.62:enable='between(t,<ch11_start_sec>+1,<ch11_start_sec>+9)',drawtext=fontfile='/System/Library/Fonts/ヒラギノ角ゴシック W6.ttc':text='何もしてないのに壊れた':fontsize=64:fontcolor=white:borderw=4:bordercolor=black:x=(w-tw)/2:y=h*0.70:enable='between(t,<ch11_start_sec>+2,<ch11_start_sec>+9)'" -c:a copy final.mp4
```

Then watch `final.mp4` end to end and check the cuts, the audio sync, that no line is doubled, and the total runtime (86.6s expected).

## Credits

- **No VOICEVOX voice is used in this run.** Every voice (narration, Fukuchan, Yametaro) is Irodori-TTS voice cloning, which carries no on-screen credit obligation, so the mandatory VOICEVOX on-screen credit does not apply here. If a VOICEVOX character is ever added to this run, a `VOICEVOX:<話者名>` on-screen credit MUST be burned in with the ffmpeg `drawtext` recipe above before delivery.
- Irodori-TTS reference audio is the real voice of the actual members. Use stays within the scope each member consented to; if the publication scope changes, confirm with them again.
- Model/tool credits: MiniMax H3 (MiniMax H3 Community License) via ComfyUI; Qwen Image Edit 2511 via draw-things-cli; Qwen3-VL via Ollama; Irodori-TTS (MIT).

## Keyframe generation log

Model: `qwen_image_edit_2511_q6p.ckpt` (fixed for the whole run — never changed mid-run). Resolution 1024x576, 20 steps, ~17 min/frame measured on this M1 Pro / 32GB machine (the skill's 23 s/step figure is for an M4 Max). H3 upscales these to its native 1344x768 canvas.

| File | Seed | Steps | Seeded from | Notes |
|---|---|---|---|---|
| `ch1_start.png` | 42 | 20 | `ref_canvas_ch1_start.png` (Yametaro sheet) | |
| `ch1_end.png` | 43 | 20 | `ch1_start.png` | |
| `ch2_end.png` | 44 | 20 | `ch1_end.png` | |
| `ch3_end.png` | 45 | 20 | `ref_canvas_ch3_end.png` (`ch2_end` + Yametaro sheet) | sheet re-injection |
| `ch4_end.png` | 46 | 20 | `ch3_end.png` | |
| `ch5_start.png` | 47 | 20 | `ch4_end.png` | hard cut, new shot |
| `ch5_end.png` | 48 | 20 | `ref_canvas_ch5_end.png` (`ch5_start` + Yametaro + Fukuchan sheets) | Fukuchan's first appearance |
| `ch6_end.png` | 49 | 20 | `ch5_end.png` | |
| `ch7_end.png` | 50 | 20 | `ref_canvas_ch7_end.png` (`ch6_end` + Yametaro sheet) | sheet re-injection |
| `ch8_start.png` | 51 | 20 | `ref_canvas_ch8_start.png` (`ch7_end` + Fukuchan sheet) | hard cut, new two-shot |
| `ch8_end.png` | 52 | 20 | `ch8_start.png` | |
| `ch9_start.png` | 53 | 20 | `ch8_end.png` | hard cut, close single |
| `ch9_end.png` | 54 | 20 | `ref_canvas_ch9_end.png` (`ch9_start` + Yametaro sheet) | sheet re-injection |
| `ch10_end.png` | 55 | 20 | `ch9_end.png` | |
| `ch11_end.png` | 56 | 20 | `ref_canvas_ch11_end.png` (`ch10_end` + Yametaro + Fukuchan sheets) | sheet re-injection |
