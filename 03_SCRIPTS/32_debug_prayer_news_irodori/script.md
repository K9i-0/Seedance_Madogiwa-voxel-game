# Debug Prayer News — latest Seedance 2.0 / CapCut package

## Run intent

This run preserves the supplied 15-second comedy-news structure and the supplied production images from the source `31_debug_prayer_news` folder. No local announcer WAV is bundled: Seedance must generate the female-announcer-style Japanese voice for the two supplied lines in Clip 1 and Clip 2. The only pre-generated local spoken audio attached in this run is the confirmed 1.7x Irodori-TTS chant for Clip 3.

Final edit timing is 15.0 seconds: 0.0–4.0 seconds studio, 4.0–9.7 seconds shrine ritual introduction, 9.7–14.2 seconds frontal chant, and 14.2–15.0 seconds statue punchline. Use one-frame hard cuts at 4.0s, 9.7s, and 14.2s. Do not use dissolves.

## Character and production references

All files listed here are physical files in this run folder. The production stills and graphic assets were copied from the supplied source folder. The character and scale references were copied from the canonical project references.

- `character_fukuchan_basic_sheet.png` — Fukuchan pose and costume support reference.
- `Fukuchan_sheet.png` — Fukuchan canonical identity/design reference.
- `height_lineup.png` — relative human scale reference only, never a composition reference.
- `prop_bug_deity_yametaro_statue_production.png` — canonical bug-deity stone statue prop reference.
- `scene_01_studio_start_production.png` — supplied studio production still.
- `scene_03_bug_deity_closeup_production.png` — supplied final statue close-up still.
- `logo_yume_tele_master.png` — supplied Yume Tele logo overlay asset.
- `screen_morning_clock_production.png` — supplied `7:00` clock overlay asset.
- `screen_debug_prayer_lower_third_production.png` — supplied lower-third overlay asset.
- `screen_bug_deity_caption_production.png` — supplied final statue caption overlay asset.

## Dialogue audio (Clip 3 is pre-generated locally; Clip 1 and Clip 2 use Seedance-generated speech)

No local announcer audio is included. Clip 1 and Clip 2 must generate their Japanese female-announcer-style voice inside Seedance from the exact lines specified in their Motion prompts. Clip 3 uses the selected 1.7x Irodori-TTS file as-is.

| File | Clip | Character / group | Voice engine | Line (ja) | Duration |
|---|---:|---|---|---|---:|
| `clip3_line1_chorus.wav` | 3 | Fukuchan-led five-person shrine group | Irodori-TTS, generated from the canonical Fukuchan reference, seed 42, fixed generation seconds 2.34 | 「ギュン謝ギュン謝ギュンギュンでーす！」 | 2.34s |

The pronunciation sent to Irodori-TTS was `ぎゅんしゃ、ぎゅんしゃ、ぎゅんぎゅんでーす！`; “ギュン謝” must be pronounced “ぎゅんしゃ”. The WAV is a single shared chant guide for the simultaneous five-person shout. Do not add five extra synthesized voices.

## Scene ledger (location & time of day across ALL clips)

| Scene state | C1 start | C1 end | C2 start | C2 end | C3 start | C3 end | C4 start | C4 end |
|---|---|---|---|---|---|---|---|---|
| Location | Yume Tele morning-news studio | Yume Tele morning-news studio | Yumemi Shrine worship hall | Yumemi Shrine worship hall | Yumemi Shrine worship hall, frontal altar view | Yumemi Shrine worship hall, frontal altar view | Same Yumemi Shrine altar, statue close-up | Same Yumemi Shrine altar, statue close-up |
| Time of day & light | Bright morning broadcast daylight | Bright morning broadcast daylight | Bright morning daylight through the shrine | Bright morning daylight through the shrine | Bright morning daylight through the shrine | Bright morning daylight through the shrine | Bright morning daylight through the shrine | Bright morning daylight through the shrine |
| Editorial overlays | Supplied Yume Tele logo; add supplied `7:00` clock in CapCut | Same | Add supplied logo, `7:00` clock and lower third in CapCut | Same | Add supplied logo, `7:00` clock and lower third in CapCut | Same until 14.2s | Remove lower third; add supplied statue caption in CapCut | Same until final frame |

The hard cuts are intentional location/composition changes. Time of day never changes: every clip is bright morning daylight, never night, dusk, or a dark horror scene.

## Prop state ledger

| Prop / state | C1 start | C1 end | C2 start | C2 end | C3 start | C3 end | C4 start | C4 end |
|---|---|---|---|---|---|---|---|---|
| Studio desk, papers and anchor hands | Present, papers flat, hands resting | Same | Out of shot after hard cut | Out of shot | Out of shot | Out of shot | Out of shot | Out of shot |
| Bug-deity stone statue | Not in studio shot | Not in studio shot | One gray stone statue, stationary on altar | One identical gray stone statue, stationary on altar | One identical gray stone statue, stationary behind group | Same | One identical gray stone statue, stationary in close-up | Same |
| Fukuchan state | Not in shot | Not in shot | Kneeling in priest robe, hands on thighs | Standing, fists rising toward cheeks | Standing, fists touching both cheeks | Same pose; mouth closes after chant | Out of shot | Out of shot |
| Four assistants | Not in shot | Not in shot | Kneeling, hands on thighs | Standing 0.2s behind Fukuchan, fists rising | Standing, fists touching both cheeks | Same pose; mouth closes after chant | Out of shot | Out of shot |
| Yume Tele logo | Small supplied logo visible | Same | Small supplied logo overlay | Same | Same | Same | Remove unless needed by editor | Same |
| `7:00` clock | Supplied overlay added in CapCut | Same | Supplied overlay added in CapCut | Same | Same | Same | Remove unless needed by editor | Same |
| Lower third | OFF | OFF | ON from 4.0s | ON through 14.2s | ON | OFF at 14.2s | OFF | OFF |
| Statue caption | OFF | OFF | OFF | OFF | OFF | OFF | ON from 14.2s | ON until 15.0s |

No prop state may reset during a clip. The statue never moves, blinks, speaks, glows, changes material, or becomes a living character.

## Fixture layout

No hinged doors, windows, drawers, switches, handles, or other moving fixtures are visible in this run. The shrine beams and altar hardware remain fixed.

## Clip 1 — studio anchor with Seedance-generated announcer voice (0.0–4.0s)

### First frame

Use `clip1_start.png`: the supplied Yume Tele morning-news studio still. The Japanese female anchor is centered in a chest-up locked shot, wearing a navy jacket and white blouse, with both hands resting on the desk and her mouth closed.

### Last frame

Use `clip1_end.png`, the same still. Hold the same framing, daylight, face, hands, desk papers and background. The local announcer WAV is intentionally absent; the final voice is generated by Seedance from the Motion prompt.

### Prop states

The desk and papers remain flat and unchanged; the anchor's hands remain on the desk; the supplied Yume Tele logo remains fixed; the supplied `7:00` clock is added later in CapCut.

### CapCut inputs (Clip 1)

- Start frame (Frame A): `clip1_start.png`
- End frame (Frame B): `clip1_end.png`
- Reference images:
  - `@Image1 = scene_01_studio_start_production.png` → supplied studio identity and lighting reference, not a composition override.
- Audio: Seedance-generated voice (no local audio file; generated inside Seedance).
- Overlay asset: `screen_morning_clock_production.png` → add as a CapCut overlay for the exact `7:00` clock; do not ask Seedance to render it.
- Motion prompt:

```text
Required attached reference files: @Image1 = scene_01_studio_start_production.png — supplied Yume Tele morning-news studio reference, identity/lighting/layout only, NOT a composition reference. This reference attachment is REQUIRED and must remain attached for this generation. Start EXACTLY on Frame A and end EXACTLY on Frame B. Create a 4.0-second locked chest-up studio shot in BRIGHT MORNING BROADCAST DAYLIGHT. The Japanese female anchor stays centered behind the desk with both hands resting on the papers and reads the exact Japanese line 「エンジニアの強い味方です」 from approximately 0.4s to 3.4s. Seedance must generate one calm, clear, neutral Japanese female morning-news announcer-style voice for this line; do not use a local announcer WAV, do not use the silent timing placeholder as dialogue, and do not generate any second voice. Lip-sync only the visible anchor to the generated line: her mouth moves only while the line is spoken, stays CLOSED before the line and after it ends. Keep the supplied studio, sea-window background, navy jacket, white blouse, desk, papers and supplied Yume Tele logo stable. No camera movement, no zoom, no pan, no new gestures, no extra people. The Japanese line is AUDIO ONLY and must NOT appear as subtitles or captions. Do NOT render any on-screen text — no subtitles, no captions, no lettering, no Japanese characters; the only visible source graphic may be the supplied Yume Tele logo already present in the reference. The supplied 7:00 clock will be added later in CapCut. The video must contain no newly generated text, no watermark, and no spontaneous graphics. It is DAYTIME, NOT night; keep the bright morning light unchanged.
```

Duration: 4.0s / Aspect: 16:9.

## Clip 2 — shrine ritual introduction with Seedance-generated announcer VO (4.0–9.7s)

### First frame

Use `clip2_start.png`: the supplied right-front three-quarter shrine view. One gray stone bug-deity statue stands on the altar at screen-left. Fukuchan and four assistants kneel in the worship hall. Fukuchan wears the white-and-gold “ギュンギュン” patterned priest robe, deep purple hakama, lanyard and name tag; the four assistants wear plain white robes and pale gray hakama. All five mouths are closed.

### Last frame

Use `clip2_end.png`: the same shrine and right-front daylight view after the group has stood. Fukuchan leads; the four assistants follow slightly behind. All five are standing and lifting inward-facing fists toward their cheeks, just before the frontal hard cut. The statue remains identical and stationary.

### Prop states

The single gray stone statue remains fixed on the left altar. Fukuchan and the assistants transition visibly from kneeling with hands on thighs to standing with fists rising; there are exactly five adults throughout. The lower third is a CapCut overlay from 4.0s to 14.2s, not Seedance-generated text. The announcer line is off-screen audio generated by Seedance, not spoken by any shrine character.

### CapCut inputs (Clip 2)

- Start frame (Frame A): `clip2_start.png`
- End frame (Frame B): `clip2_end.png`
- Reference images:
  - `@Image1 = Fukuchan_sheet.png` → Fukuchan canonical model sheet, identity/design reference only, NOT a composition reference.
  - `@Image2 = character_fukuchan_basic_sheet.png` → Fukuchan pose/costume support reference, identity/design reference only, NOT a composition reference.
  - `@Image3 = prop_bug_deity_yametaro_statue_production.png` → exact stone statue prop reference, NOT a composition reference.
  - `@Image4 = height_lineup.png` → relative human scale reference only, NOT a composition reference.
  - `@Image5 = logo_yume_tele_master.png` → supplied logo overlay reference, use later in CapCut only.
  - `@Image6 = screen_morning_clock_production.png` → supplied `7:00` overlay reference, use later in CapCut only.
  - `@Image7 = screen_debug_prayer_lower_third_production.png` → supplied lower-third overlay, use later in CapCut only.
- Audio: Seedance-generated voice (no local audio file; generated inside Seedance).
- Motion prompt:

```text
Required attached reference files: @Image1 = Fukuchan_sheet.png — Fukuchan canonical model sheet, identity/design reference only, NOT a composition reference; @Image2 = character_fukuchan_basic_sheet.png — Fukuchan pose and costume support reference, identity/design reference only, NOT a composition reference; @Image3 = prop_bug_deity_yametaro_statue_production.png — the exact gray stone bug-deity statue, prop identity reference only, NOT a composition reference; @Image4 = height_lineup.png — relative body-size reference only, NOT a composition reference; @Image5 = logo_yume_tele_master.png — supplied overlay reference, not to be redrawn; @Image6 = screen_morning_clock_production.png — supplied clock overlay reference, not to be redrawn; @Image7 = screen_debug_prayer_lower_third_production.png — supplied lower-third overlay reference, not to be redrawn. These reference attachments are REQUIRED inputs and must remain attached for this generation. Start EXACTLY on Frame A and end EXACTLY on Frame B. Create a continuous 5.7-second shrine ritual shot in BRIGHT MORNING DAYLIGHT, NOT night. Begin with Fukuchan and exactly four adult assistants kneeling in the supplied right-front three-quarter Yumemi Shrine worship hall, the single gray stone bug-deity statue on the screen-left altar. Fukuchan — the slim stylish black-haired man in the supplied white-and-gold patterned priest robe with deep purple hakama, lanyard and name tag — looks toward the statue, bows once from the waist, returns upright, then leads the visible transition from kneeling with hands on thighs to standing. The four assistants follow 0.2 seconds later. By Frame B all five stand in the same right-front composition, closed mouths, both small inward-facing fists rising toward their cheeks. Seedance must generate one calm, clear, neutral Japanese female morning-news announcer-style off-screen voice reading the exact line 「こちらの神社では、デバッグ祈願が受けられます。」 from approximately 4.4s to 9.3s. Do not use a local announcer WAV, do not use the silent timing placeholder as dialogue, and do not generate any second voice. This line is AUDIO ONLY and must NOT appear as subtitles or captions. The five shrine staff do NOT speak and their mouths stay CLOSED throughout this off-screen narration. Keep exactly five adults, the same clothing, the same statue, the same shrine beams, the same camera side and bright morning light. Keep the statue completely still and never make it blink, speak, glow, transform, duplicate or become alive. The supplied Yume Tele logo, 7:00 clock and lower third will be composited later in CapCut; do not render new text. Do NOT render any on-screen text — no subtitles, no captions, no lettering, no Japanese characters, no spontaneous logos and no watermark. The only later-added text is the supplied CapCut overlay artwork. Preserve the clean hard-cut handoff to the frontal chant clip at 9.7 seconds. It is DAYTIME, NOT night; keep natural bright morning light throughout.
```

Duration: 5.7s / Aspect: 16:9.

## Clip 3 — frontal five-person chant (9.7–14.2s)

### First frame

Use `clip3_start.png`: the supplied frontal eye-level symmetric composition. Exactly five adults stand in front of the altar, Fukuchan centered, four assistants symmetrically arranged, one statue behind them. All ten hands are small inward-facing fists with the index-finger sides touching the corresponding cheeks. All mouths are closed at the first frame.

### Last frame

Use `clip3_end.png`: the same frontal composition and pose for the silent hold after the chant. The chant audio lasts 2.34 seconds inside the 4.5-second clip. All five mouths close immediately after the attached audio ends and the group holds the pose until the hard cut at 14.2s.

### Prop states

The statue, five-person arrangement, costumes, fists, cheek contact, feet and camera remain unchanged. Only the mouths open during the attached chant and close when the WAV ends; no hand opens, no fist leaves the cheek, and no extra person appears.

### CapCut inputs (Clip 3)

- Start frame (Frame A): `clip3_start.png`
- End frame (Frame B): `clip3_end.png`
- Reference images:
  - `@Image1 = Fukuchan_sheet.png` → Fukuchan canonical identity/design reference only, NOT a composition reference.
  - `@Image2 = character_fukuchan_basic_sheet.png` → Fukuchan pose/costume support reference, NOT a composition reference.
  - `@Image3 = prop_bug_deity_yametaro_statue_production.png` → exact statue prop reference, NOT a composition reference.
  - `@Image4 = height_lineup.png` → relative scale reference only, NOT a composition reference.
  - `@Image5 = logo_yume_tele_master.png` → supplied logo overlay reference, use later in CapCut only.
  - `@Image6 = screen_morning_clock_production.png` → supplied clock overlay reference, use later in CapCut only.
  - `@Image7 = screen_debug_prayer_lower_third_production.png` → supplied lower-third overlay, use later in CapCut only.
- Audio: `clip3_line1_chorus.wav` as `@Audio1` — attach to Seedance as input; pre-generated Irodori-TTS 1.7x chant, 2.34s, use AS-IS as the only spoken audio track.
- Motion prompt:

```text
Required attached reference files: @Image1 = Fukuchan_sheet.png — Fukuchan canonical identity/design reference only, NOT a composition reference; @Image2 = character_fukuchan_basic_sheet.png — Fukuchan pose/costume support reference only, NOT a composition reference; @Image3 = prop_bug_deity_yametaro_statue_production.png — exact gray stone bug-deity statue prop reference only, NOT a composition reference; @Image4 = height_lineup.png — relative body-size reference only, NOT a composition reference; @Image5 = logo_yume_tele_master.png — supplied overlay reference, not to be redrawn; @Image6 = screen_morning_clock_production.png — supplied clock overlay reference, not to be redrawn; @Image7 = screen_debug_prayer_lower_third_production.png — supplied lower-third overlay reference, not to be redrawn. These reference attachments are REQUIRED inputs and must remain attached for this generation. @Audio1 = clip3_line1_chorus.wav is REQUIRED and must remain attached. Start EXACTLY on Frame A and end EXACTLY on Frame B. Create a 4.5-second fixed frontal eye-level symmetric shot in BRIGHT MORNING DAYLIGHT, NOT night. Keep exactly five adult shrine staff in the supplied arrangement: Fukuchan — the slim stylish black-haired man in the white-and-gold patterned priest robe and deep purple hakama — centered, with four assistants in plain white robes and pale gray hakama symmetrically arranged around him. The single gray stone bug-deity statue remains stationary behind the group. All five keep both small inward-facing fists pressed to the corresponding cheeks; palms never face camera, fingers never spread, and fists never leave the cheeks. ONLY the five visible shrine staff perform the same simultaneous chant, using @Audio1 AS-IS: 「ギュン謝ギュン謝ギュンギュンでーす！」. Treat @Audio1 as the complete spoken audio; do not generate any additional voice, synthesized speech, narration, crowd layer, or doubled dialogue. All five mouths move together ONLY while @Audio1 is playing; the chant begins almost immediately, ends at 2.34 seconds, and every mouth stays CLOSED for the rest of the clip. Keep the feet planted, camera fixed, statue motionless, composition symmetric, and all five bodies visible from face to sandals. The supplied Yume Tele logo, 7:00 clock and lower third will be composited later in CapCut; do not redraw them in Seedance. Do NOT render any on-screen text — no subtitles, no captions, no lettering, no Japanese characters, no spontaneous graphics and no watermark. The only Japanese words in this prompt are spoken through the attached audio and must not appear as text. Preserve the serious deadpan delivery and the harmless visual joke. End on the exact supplied Frame B, then hard-cut to the statue close-up at 14.2 seconds. It is DAYTIME, NOT night; keep bright natural morning light throughout.
```

Duration: 4.5s / Aspect: 16:9.

## Clip 4 — statue punchline (14.2–15.0s final use)

### First frame

Use `clip4_start.png`: the supplied 50–70mm close-up of the same single gray stone bug-deity statue on the same altar, placed to the right with calm negative space at lower left.

### Last frame

Use `clip4_end.png`, the same still. Generate a 4.0-second hold-capable clip, then trim the final timeline to the first 0.8 seconds so the complete video ends at exactly 15.0 seconds.

### Prop states

The statue remains completely motionless and identical. No people, no voice, no glow, no transformation. The supplied statue caption is composited in CapCut only from 14.2s to 15.0s.

### CapCut inputs (Clip 4)

- Start frame (Frame A): `clip4_start.png`
- End frame (Frame B): `clip4_end.png`
- Reference images:
  - `@Image1 = prop_bug_deity_yametaro_statue_production.png` → exact statue identity/prop reference only, NOT a composition reference.
  - `@Image2 = scene_03_bug_deity_closeup_production.png` → supplied shrine close-up lighting and altar reference, NOT a composition reference.
  - `@Image3 = screen_bug_deity_caption_production.png` → supplied caption overlay reference, use later in CapCut only.
- Audio: Seedance-generated ambience only; no local audio file, no voice, narration, or caption readout.
- Overlay asset: `screen_bug_deity_caption_production.png` → add in CapCut from 14.2s to 15.0s at lower left. Keep the exact supplied text and modest size; do not ask Seedance to render it.
- Motion prompt:

```text
Required attached reference files: @Image1 = prop_bug_deity_yametaro_statue_production.png — exact gray stone bug-deity statue identity reference only, NOT a composition reference; @Image2 = scene_03_bug_deity_closeup_production.png — supplied shrine close-up lighting and altar reference, NOT a composition reference; @Image3 = screen_bug_deity_caption_production.png — supplied caption overlay reference, not to be redrawn. These reference attachments are REQUIRED inputs and must remain attached for this generation. Start EXACTLY on Frame A and end EXACTLY on Frame B. Create a quiet 4.0-second fixed 50–70mm shrine close-up in BRIGHT MORNING DAYLIGHT, NOT night. Show only the same one gray stone statue on the same altar, placed to the right with lower-left negative space. The statue must remain completely motionless: no blinking, no speaking, no glowing, no breathing, no transformation, no living skin, no camera zoom, no pan, no focus pull, no extra people, no additional statue. The supplied Japanese caption will be composited later in CapCut for only the first 0.8 seconds of the final timeline. Do NOT render any on-screen text — no subtitles, no captions, no lettering, no Japanese characters, no spontaneous graphics and no watermark. No voice, no narration, no synthesized speech and no caption readout. Keep the same bright morning light and shrine altar until the end. It is DAYTIME, NOT night.
```

Generation duration: 4.0s / final timeline use: first 0.8s / Aspect: 16:9.

## Generation & assembly protocol (REQUIRED — read before generating anything in CapCut)

### Step 1 — Pilot clip first (batch generation is FORBIDDEN until the pilot passes)

Generate ONLY Clip 1, then verify ALL of the following before touching any other clip:

- [ ] Clip 1 contains exactly one Seedance-generated Japanese female announcer-style voice reading 「エンジニアの強い味方です」; there is no doubled voice and no local silent guide audible in the final result.
- [ ] The anchor is the only visible speaker, and her mouth moves only during the generated line and stays closed before and after it.
- [ ] Motion, poses, desk and paper states match the Motion prompt and the Prop state ledger.
- [ ] Location, time of day and lighting match the Scene ledger in EVERY frame — bright morning daylight, no day-to-night jump.
- [ ] NO unrequested on-screen text appears — no spontaneous subtitles, captions, Japanese lettering, or watermark.
- [ ] The clip duration equals the specified 4.0s, not the CapCut default.

If any check fails, fix the inputs/prompt and regenerate Clip 1 until all pass. Only then generate the remaining clips, and re-run the audio, mouth and duration checks on every clip. For Clip 3, confirm that the attached `clip3_line1_chorus.wav` is used AS-IS with no doubled or synthesized voice, that all five mouths move only during its 2.34 seconds, and that every mouth closes afterward.

### Step 2 — Prompts are verbatim

Paste each clip's Motion prompt into CapCut EXACTLY as written in this file. Do NOT summarize, shorten or paraphrase it. If it seems too long, split the clip rather than compressing away the state, identity, daylight, audio or text constraints.

### Step 3 — Final audio track (assembly)

The audio embedded in generated clips must be checked before final assembly. When assembling the final video on the CapCut timeline:

1. For Clip 1 and Clip 2, keep the Seedance-generated announcer voice only after verifying the exact Japanese lines, correct female announcer style, no doubled voice and correct lip-sync/off-screen binding. No local announcer WAV is attached or audible.
2. Mute or delete any embedded generated audio from Clip 3, then add `clip3_line1_chorus.wav` as the final dialogue track in Clip 3, aligned to the visible five-person mouth movement.
3. Use only restrained studio/shrine ambience; do not add music, drum hits, bells, applause, laughter or a caption readout.
4. Trim Clip 4 to 0.8s in the final timeline. Confirm the total edit is exactly 15.0s.
5. Play the full timeline before export and confirm that Clip 1 and Clip 2 contain the two generated announcer lines and Clip 3 contains the local Irodori-TTS chant.

## Credits

No VOICEVOX voice is used in the final video. The temporary female reference used during the abandoned announcer test was removed from this run and must not be attached to CapCut. No VOICEVOX on-screen credit is required.
