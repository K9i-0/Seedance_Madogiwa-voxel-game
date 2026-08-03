# Seedance: Yotan's Dress-Code Interview

Total duration: 12 seconds (2 clips)
Aspect ratio: 16:9
Genre: cheerful office interview comedy
Setting: a clean, bright interview room at Accidenchua Inc., with a hallway entrance door, an interview table, two chairs, and a second side door.

## Character references

- Sobaya: `Sobaya_sheet.png` (bundled physical file; required CapCut attachment)
- Yotan: `Yotan_sheet.png` (bundled physical file; required CapCut attachment)
- Relative scale: `height_lineup.png` (bundled physical file; required for Clip 2)

## Dialogue audio (all voices pre-generated locally — Seedance must NOT generate any voice)

| File | Clip | Character | Voice (engine) | Line (ja) | Duration |
|---|---:|---|---|---|---:|
| `clip1_line1_sobaya.wav` | 1 | Sobaya | Irodori-TTS (`Sobaya_voice.wav`, seed 42) + required monsterize | 「何その金髪と革ジャン。弊社はドレスコード厳しいよ？」 | 4.48s |
| `clip2_line1_yotan.wav` | 2 | Yotan | Irodori-TTS (`Yotan_voice.wav`, seed 100) | 「いや誰が言うとんねん」 | 1.96s |

## Prop state ledger

| Prop | C1 start | C1 end = C2 start | C2 end |
|---|---|---|---|
| Yotan's electric guitar | Securely slung across his body; one hand holds the neck | Same guitar and strap position; hand still holds the neck | Unchanged; one hand holds the neck while the free hand points |
| Sobaya's oversized clear beer mug | Off-screen, upright in Sobaya's hand, HALF-FULL | Off-screen, upright in Sobaya's hand, HALF-FULL | Visible, upright in Sobaya's hand, HALF-FULL |
| Hallway entrance door | Half-open | Closed after Yotan enters | Remains closed |
| Interview-room side door | Closed | Closed | Open after Sobaya enters through it |

Logical check: the entrance and side-door transitions occur visibly. No liquid level changes. Nobody drinks or pours. Yotan's guitar and Sobaya's mask and mug remain mandatory design elements.

## Fixture layout (constant across ALL clips — hinges and handles never move)

| Fixture | Hinge side (from camera) | Handle | Opens |
|---|---|---|---|
| Hallway entrance door (back wall) | LEFT edge | silver lever handle on the RIGHT edge (the edge opposite the hinges), mid-height | inward into the room, swinging toward camera-left |
| Interview-room side door (right wall) | RIGHT edge | silver lever handle on the LEFT edge (the edge opposite the hinges), mid-height | inward into the room, swinging toward camera-right |

Every keyframe prompt and Motion prompt that shows a door must repeat this layout, including when the door is fully closed. Handles never disappear, never move to the hinge side, and are never duplicated.

## Clip 1 — The unseen dress-code warning

Duration: 7 seconds
Speaker: Sobaya only, entirely off-screen
Audio: `clip1_line1_sobaya.wav`

### First frame

A medium-wide view from inside the spotless interview room toward the hallway entrance. Yotan — the slim 170cm 40-year-old rocker with shoulder-length blond hair, round sunglasses and a black leather biker jacket, holding an electric guitar — is halfway through the half-open door. The entrance door is hinged on its LEFT edge and swung inward toward camera-left; its silver lever handle sits at mid-height on the free RIGHT edge (opposite the hinges). His required guitar is securely slung across his body and one hand holds its neck. His mouth is CLOSED. Sobaya is not visible. The room's side door is closed, with its silver lever handle at mid-height on its LEFT edge (hinge on the RIGHT edge). No text.

### Last frame

The same room, framing, and lighting. Yotan now stands fully inside beside the interview table. The entrance door has closed behind him; its silver lever handle is clearly visible at mid-height on the RIGHT edge of the closed door (hinges on the LEFT edge) — the handle has NOT disappeared and has NOT moved to the hinge side. His guitar and clothing are unchanged. He turns toward the still-closed side door (lever handle on its LEFT edge) with confused disbelief, mouth CLOSED. Sobaya remains completely off-screen.

### Prop states

- Guitar: securely slung, one hand on neck → unchanged.
- Beer mug: off-screen, upright, HALF-FULL → unchanged; no drinking or pouring.
- Entrance door: half-open → visibly closes after Yotan enters. Hinged on its LEFT edge, silver lever handle on the RIGHT edge (opposite the hinges) at mid-height; the handle stays on that edge through the whole swing and remains visible when the door is fully closed.
- Side door: closed → remains closed. Lever handle on its LEFT edge (hinge on the RIGHT edge) throughout.

### Motion

Yotan takes two relaxed steps inside and the entrance door swings shut. An unseen Sobaya speaks from behind the closed side door. Yotan pauses and slowly turns toward the voice, listening silently with his mouth CLOSED. Do not reveal Sobaya in this clip.

### CapCut inputs (Clip 1)

- Start frame (Frame A): `clip1_start.png`
- End frame (Frame B): `clip1_end.png`
- Reference images:
  - @Image1 = `Sobaya_sheet.png` → Sobaya — the hulking 180cm/100kg muscular gray-skinned man whose face is always covered by a white mask with red markings, wearing a white T-shirt and holding a large beer mug. Identity/design reference only, NOT composition.
  - @Image2 = `Yotan_sheet.png` → Yotan — the slim 170cm 40-year-old rocker with shoulder-length blond hair, round sunglasses and a black leather biker jacket, holding an electric guitar. Identity/design reference only, NOT composition.
- Audio: `clip1_line1_sobaya.wav` (@Audio1 — off-screen Sobaya) — attach to Seedance and use AS-IS.
- Duration: 7s / Aspect: 16:9
- Motion prompt:

```text
Required attached reference files: @Image1 = Sobaya_sheet.png — Sobaya's character model sheet, identity/design reference only, NOT a composition reference; @Image2 = Yotan_sheet.png — Yotan's character model sheet, identity/design reference only, NOT a composition reference. These reference attachments are REQUIRED inputs and must remain attached for this generation.
Create a cheerful Japanese office-interview comedy shot moving exactly from Frame A to Frame B. Keep the clean interview room, framing, lighting, identities and props consistent. Yotan (@Image2, Yotan — the slim 170cm 40-year-old rocker with shoulder-length blond hair, round sunglasses and a black leather biker jacket, holding an electric guitar) takes two relaxed steps through the half-open entrance. His required electric guitar stays securely slung across his body and one hand stays on its neck. The entrance door visibly swings closed behind him. The entrance door is hinged on its LEFT edge and its silver lever handle sits at mid-height on the RIGHT edge (the edge opposite the hinges); the hinges and handle stay fixed to those same edges throughout the swing, and once the door is fully closed the handle stays clearly visible on the RIGHT edge — the handle does NOT disappear, does NOT move to the hinge side, and is NOT duplicated. The room's side door stays CLOSED, keeping its silver lever handle at mid-height on its LEFT edge (hinge on the RIGHT edge). Sobaya (@Image1, Sobaya — the hulking 180cm/100kg muscular gray-skinned man whose face is always covered by a white mask with red markings, wearing a white T-shirt and holding a large beer mug) remains completely OFF-SCREEN for the entire clip. ONLY off-screen Sobaya speaks “何その金髪と革ジャン。弊社はドレスコード厳しいよ？” using @Audio1 AS-IS. Because Sobaya is off-screen, no visible mouth lip-syncs to @Audio1. Yotan does NOT speak — his mouth stays CLOSED; he pauses, turns toward the unseen voice, and reacts with confused disbelief. Sobaya's off-screen mug stays upright and HALF-FULL. No drinking, pouring, or liquid change. Use the attached audio AS-IS; do NOT generate any voice — no synthesized speech, narration, or doubled dialogue. The reference sheets' labels must NOT appear. No subtitles, text, logos, watermarks, extra people, extra dialogue, bullying, humiliation, harassment, sadness, injury, or dark mood.
```

## Clip 2 — The reveal and retort

Duration: 5 seconds
Speaker: Yotan only
Audio: `clip2_line1_yotan.wav`

### First frame

Use `clip1_end.png` unchanged. Yotan faces the closed side door with confused disbelief and a CLOSED mouth. The entrance door is closed, its silver lever handle visible at mid-height on its RIGHT edge (hinges on the LEFT edge). The side door's lever handle is on its LEFT edge. Sobaya remains off-screen. All prop states exactly match Clip 1's last frame.

### Last frame

The same framing and room. The side door is open: hinged on its RIGHT edge, it has swung inward into the room toward camera-right, and its silver lever handle is still at mid-height on the free LEFT edge of the panel. The entrance door stays closed with its lever handle visible on its RIGHT edge. Sobaya — the hulking 180cm/100kg muscular gray-skinned man whose face is always covered by a white mask with red markings, wearing a white T-shirt and holding a large beer mug — stands proudly inside. His required mask fully covers his face and his required oversized mug is upright and HALF-FULL. Yotan points at him with his free hand while his other hand holds the guitar neck. Yotan's mouth is OPEN mid-retort. Both remain friendly and comedic.

### Prop states

- Guitar: same position → unchanged while Yotan points with his free hand.
- Beer mug: off-screen, upright, HALF-FULL → visible, upright, HALF-FULL; no drinking or pouring.
- Entrance door: closed → remains closed; its lever handle stays visible on its RIGHT edge (hinges on the LEFT edge).
- Side door: closed → visibly opens as Sobaya enters. Hinged on its RIGHT edge, lever handle on the LEFT edge (opposite the hinges) at mid-height; the hinges and handle stay fixed to those same edges throughout the swing — the handle never disappears or moves.

### Motion

After a half-beat, the side door opens and Sobaya steps in with absurd authority while keeping his mug upright. Yotan reacts, points at Sobaya, and delivers the retort with sharp Kansai-comedy timing. Sobaya remains silent.

### CapCut inputs (Clip 2)

- Start frame (Frame A): `clip1_end.png` (shared boundary; do not regenerate)
- End frame (Frame B): `clip2_end.png`
- Reference images:
  - @Image1 = `Sobaya_sheet.png` → Sobaya — the hulking 180cm/100kg muscular gray-skinned man whose face is always covered by a white mask with red markings, wearing a white T-shirt and holding a large beer mug. Identity/design reference only, NOT composition.
  - @Image2 = `Yotan_sheet.png` → Yotan — the slim 170cm 40-year-old rocker with shoulder-length blond hair, round sunglasses and a black leather biker jacket, holding an electric guitar. Identity/design reference only, NOT composition.
  - @Image3 = `height_lineup.png` → relative body scale only, NOT composition; Sobaya is taller and much broader.
- Audio: `clip2_line1_yotan.wav` (@Audio1 — Yotan) — attach to Seedance and use AS-IS.
- Duration: 5s / Aspect: 16:9
- Motion prompt:

```text
Required attached reference files: @Image1 = Sobaya_sheet.png — Sobaya's character model sheet, identity/design reference only, NOT a composition reference; @Image2 = Yotan_sheet.png — Yotan's character model sheet, identity/design reference only, NOT a composition reference; @Image3 = height_lineup.png — relative height/scale reference only, NOT a composition reference. These reference attachments are REQUIRED inputs and must remain attached for this generation.
Continue seamlessly from Frame A to Frame B in the identical clean interview room. After a short comedic half-beat, the closed side door visibly opens and Sobaya (@Image1, Sobaya — the hulking 180cm/100kg muscular gray-skinned man whose face is always covered by a white mask with red markings, wearing a white T-shirt and holding a large beer mug) steps proudly into view. The side door is hinged on its RIGHT edge and its silver lever handle sits at mid-height on the LEFT edge (the edge opposite the hinges); it swings open inward into the room toward camera-right, and the hinges and handle stay fixed to those same edges throughout the swing — the handle does NOT disappear, does NOT move to the hinge side, and is NOT duplicated. The closed entrance door keeps its silver lever handle clearly visible at mid-height on its RIGHT edge (hinges on the LEFT edge). Preserve his required full white mask with red markings, white short-sleeve T-shirt, muscular gray body, and required oversized clear beer mug. The mug is upright and HALF-FULL when revealed and remains HALF-FULL; Sobaya does NOT drink or pour. Yotan (@Image2, Yotan — the slim 170cm 40-year-old rocker with shoulder-length blond hair, round sunglasses and a black leather biker jacket, holding an electric guitar) holds a stunned beat, then points at Sobaya with his free hand while his other hand keeps holding his required guitar's neck. ONLY Yotan speaks “いや誰が言うとんねん,” lip-syncing naturally to @Audio1 with sharp Kansai-comedy timing. Sobaya does NOT speak; his mask remains fixed and he stands confidently. @Image3 controls relative scale only. Both are friendly and amused. Use @Audio1 AS-IS; do NOT generate any voice — no synthesized speech, narration, or doubled dialogue. The reference sheets' labels must NOT appear. No subtitles, text, logos, watermarks, extra people, extra dialogue, missing mask, missing guitar, missing mug, drinking, pouring, bullying, humiliation, harassment, sadness, injury, or dark mood.
```

## Keyframe generation prompts

### `clip1_start.png`

```text
Required input images: Image 1 = Sobaya_sheet.png — Sobaya's bundled character model sheet, identity/design reference only; Image 2 = Yotan_sheet.png — Yotan's bundled character model sheet, identity/design reference only. Create the FIRST-FRAME still of a 16:9 cheerful office-interview comedy. View from inside a spotless interview room toward a half-open hallway entrance. The entrance door is hinged on its LEFT edge and swung inward toward camera-left; its silver lever handle sits at mid-height on the free RIGHT edge (the edge opposite the hinges). Yotan from Image 2 is halfway through the door. Preserve his shoulder-length blond hair, round sunglasses, black leather biker jacket, and required electric guitar, securely slung with one hand on its neck. His mouth is FULLY CLOSED. Include a simple table, two chairs, and a second CLOSED side door on the right wall whose silver lever handle sits at mid-height on its LEFT edge (hinge on the RIGHT edge). Sobaya is completely off-screen. Polished anime illustration, warm clean lighting, no text, labels, subtitles, logos, or watermark.
```

### `clip1_end.png` (also Clip 2 Frame A)

```text
Required input images: Image 1 = clip1_start.png — previous frame and composition lock; Image 2 = Sobaya_sheet.png — Sobaya's bundled character model sheet, identity/design reference only; Image 3 = Yotan_sheet.png — Yotan's bundled character model sheet, identity/design reference only. Create the LAST-FRAME still of the same shot. Preserve Image 1's exact room, art style, framing, lighting, and Yotan identity. Yotan now stands fully inside beside the table. The entrance door is fully closed: it is hinged on its LEFT edge and its silver lever handle is clearly visible at mid-height on the RIGHT edge of the closed door (the edge opposite the hinges) — the handle must NOT be on the left/hinge side and must NOT be missing. His clothes, guitar, strap, and hand on its neck are unchanged. He turns toward the still-CLOSED side door (silver lever handle at mid-height on its LEFT edge, hinge on the RIGHT edge) with confused disbelief and his mouth FULLY CLOSED. Sobaya remains completely off-screen. No text, labels, subtitles, logos, or watermark.
```

### `clip2_end.png`

```text
Required input images: Image 1 = clip1_end.png — previous frame and composition lock; Image 2 = Sobaya_sheet.png — Sobaya's bundled character model sheet, identity/design reference only; Image 3 = Yotan_sheet.png — Yotan's bundled character model sheet, identity/design reference only; Image 4 = height_lineup.png — bundled relative scale reference only. Create the LAST-FRAME still of the continuous shot. Preserve Image 1's exact room, art style, framing, lighting, and Yotan identity. The side door is OPEN: hinged on its RIGHT edge, it has swung inward into the room toward camera-right, and its silver lever handle is still at mid-height on the free LEFT edge of the panel — the handle must NOT be missing or on the hinge side. The entrance door stays fully closed with its silver lever handle visible at mid-height on its RIGHT edge (hinges on the LEFT edge). Sobaya from Image 2 stands proudly inside, preserving his required full white mask with red markings, white short-sleeve T-shirt, muscular gray body, and oversized clear beer mug. The upright mug is HALF-FULL; no drinking. Yotan points at Sobaya with his free hand while his other hand holds his unchanged guitar neck. Yotan's mouth is OPEN mid-retort. Sobaya is taller and broader. Friendly comedy, no text, labels, subtitles, logos, or watermark.
```

## Generation & assembly protocol (REQUIRED — read before generating anything in CapCut)

### Step 1 — Pilot clip first (batch generation is FORBIDDEN until the pilot passes)
Generate ONLY Clip 1, then verify ALL of the following before touching any other clip:
- [ ] The dialogue audio in the output is the attached wav AS-IS (no synthesized voice, no doubled voices)
- [ ] The CORRECT character lip-syncs to each line (the speaker named in the prompt moves their mouth; every non-speaker's mouth stays closed)
- [ ] Motion, poses and prop states match the Motion prompt and the Prop state ledger
- [ ] Door hardware follows the Fixture layout table in EVERY frame: hinges and lever handles stay on their specified edges, and the handle stays visible after the entrance door finishes closing (it never disappears, jumps to the hinge side, or duplicates)
- [ ] The clip duration equals the Duration specified in the CapCut inputs table (NOT the ~8s default)
If any check fails, fix the inputs/prompt and regenerate Clip 1 until all pass.
Only then generate the remaining clips, and re-run at least the audio + duration checks on every clip.

### Step 2 — Prompts are verbatim
Paste each clip's Motion prompt into CapCut EXACTLY as written in this file.
Do NOT summarize, shorten, or paraphrase it. If it seems too long, do not compress it —
go back to the script and split the clip instead.

### Step 3 — Final audio track (assembly)
The audio embedded in the generated clips is NOT the final audio, even when the wav was
attached at generation time. When assembling the final video on the CapCut timeline:
1. Mute (or delete) the audio embedded in every generated clip.
2. Lay the original wav files from the Dialogue audio table onto the timeline as the
   final dialogue track, aligned to each character's lip movements.
3. Play back the full timeline before export and confirm every line sounds exactly like
   the local VOICEVOX / Irodori-TTS takes (the source wavs are the single source of truth).

## Credits

No VOICEVOX voices are used. No VOICEVOX on-screen credit is required.
