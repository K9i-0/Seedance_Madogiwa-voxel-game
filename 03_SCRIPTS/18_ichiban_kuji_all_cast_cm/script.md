# Video Commercial: "Ichiban Kuji Madogiwa-zoku Monogatari — All-Cast Grand Launch"

## Format

- Length: 30 seconds
- Structure: 5 clips x 6 seconds
- Aspect ratio: 16:9
- Genre: spectacular ensemble product commercial / cheerful office slice-of-life comedy
- Visual style: polished high-end live-action-meets-anime commercial, warm navy-and-gold izakaya palette, energetic concert lighting, crisp product silhouettes, harmless cartoon spectacle
- Product reference: `product_ichiban_kuji_ref.png`
- Product facts shown in the supplied artwork: launch begins September 5, 2026; suggested retail price is JPY 790 per draw including 10% tax; sales end when stock runs out.
- Output design: every clip uses fixed first and last frames for CapCut / Seedance 2.0 first-last-frame generation.

## Story summary

Sobaya pulls open the navy curtain of the Window-Side Tribe's standing bar and unveils the new "一番くじ 窓際族物語" display. Yumemin rings the opening with a BONK while Takosan silently guards the plush-prize shelf. Tokun, Yotan, Fukuchan, and Yametaro rush in like an absurd commercial band and show off the figure, plush, cushion, acrylic stands, mugs, charms, and stickers. Yametaro nervously draws one ticket, discovers that every prize feels like a win, and celebrates with the others. A large remote screen descends and Okayaman gives his official astonished approval. The commercial ends with the seven featured members plus remote Okayaman in one lavish navy-and-gold hero tableau around the prize lineup and the release information. This is a real cheerful promotional event, not a dream.

## Character and design invariants

- Sobaya: tall muscular adult man. His white full-face mask, short-sleeve T-shirt, and giant glass beer mug are mandatory and clearly visible.
- Takosan: black hooded robe, white face, black round eyes, octopus tentacles, and two human arms. The robe and tentacles never change.
- Tokun: slightly chubby adult man in an aloha shirt and straw hat, always carrying his ukulele.
- Yotan: slim blond adult man in black leather rock clothing and sunglasses, always carrying his guitar.
- Fukuchan: stylish black-haired adult man with a neck badge and SPONSOR strap. His Gyun-Gyun pose uses both hands against his cheeks.
- Yametaro: stylized adult man in a purple shirt and round glasses. His exact character design never changes.
- Okayaman: medium-length black hair, moustache and beard, black hooded jacket, gentle smile. He appears only through a large remote screen.
- Yumemin: flying blue round baku-like mascot with black dot eyes, small ears, white rear body, flexible nose, and wooden BONK mallet. Yumemin speaks no words and only makes a short cry.
- Everyone is visibly delighted. No bullying, coercion, dangerous drinking, injury, realistic destruction, gloomy mood, or workplace abuse.

## Product and graphic invariants

- Treat `product_ichiban_kuji_ref.png` as the authoritative product-art reference, not as a character identity reference.
- Preserve the navy, warm gold, red-lantern, Tokyo-night, and standing-bar visual language.
- Show the recognizable prize categories: Sobaya large figure, Takosan plush, Yumemin BONK cushion, five acrylic stands, four phrase mugs, six acrylic charms, seven sticker designs, and the Okayaman remote-drama Last One prize.
- Do not ask the image or video model to reproduce small Japanese typography exactly. Composite the supplied product artwork or editor-built typography in post for exact wording, date, price, prize labels, and legal text.
- On generated frames, use clean blank navy-and-gold sign panels where exact text will be composited later.

## Prop state ledger

| Prop | C1 start | C1 end = C2 start | C2 end = C3 start | C3 end = C4 start | C4 end = C5 start | C5 end |
|---|---|---|---|---|---|---|
| Navy reveal curtain | CLOSED across the prize stage | FULLY OPEN, tied at both sides | FULLY OPEN, tied at both sides | FULLY OPEN, tied at both sides | FULLY OPEN, tied at both sides | FULLY OPEN, tied at both sides |
| Prize display | Hidden behind curtain | Fully revealed, all items upright and orderly | Fully revealed, all items upright and orderly | Fully revealed, all items upright and orderly | Fully revealed, all items upright and orderly | Fully revealed, all items upright and orderly |
| Lottery draw box | Hidden behind curtain | On the counter, lid CLOSED, ticket stack inside | On the counter, lid CLOSED, ticket stack inside | Lid OPEN; Yametaro holds exactly ONE unfolded ticket; remaining tickets stay inside | Lid OPEN; Yametaro still holds the same ONE ticket | Lid OPEN; Yametaro still holds the same ONE ticket |
| Okayaman remote screen | Raised off-screen, OFF | Raised off-screen, OFF | Raised off-screen, OFF | Descended above the group, OFF | Descended and ON with Okayaman smiling | Descended and ON with Okayaman smiling |
| Sobaya giant beer mug | FULL, upright in left hand, no drinking | FULL, upright in left hand, no drinking | FULL, upright in left hand, no drinking | FULL, upright in left hand, no drinking | FULL, upright in left hand, no drinking | FULL, raised upright in left hand, no drinking |
| Yumemin BONK mallet | Held upright | Taps a small brass opening bell once, then held upright | Held upright | Held upright | Held upright | Raised upright |

## Dialogue audio (all voices pre-generated locally — Seedance must NOT generate any voice)

| File | Clip | Character | Voice (engine) | Line (ja) | Duration |
|---|---:|---|---|---|---:|
| `clip1_line1_sobaya.wav` | 1 | Sobaya | Irodori-TTS (ref: `Sobaya_voice.wav`, seed 44, CPU) | 一番くじ窓際族物語、開幕です！ | 4.36s |
| `clip1_line2_yumemin.wav` | 1 | Yumemin | VOICEVOX:ずんだもん (style 3, speed 1.00) | きゅー！ | 0.69s |
| `clip2_line1_takosan.wav` | 2 | Takosan | VOICEVOX:Voidoll (style 89, speed 1.00) | もちもち。 | 0.84s |
| `clip2_line2_tokun.wav` | 2 | Tokun | VOICEVOX:白上虎太郎 (style 12, speed 1.12) | ウクレレより存在感あるで！ | 1.83s |
| `clip2_line3_yotan.wav` | 2 | Yotan | VOICEVOX:黒沢冴白 (style 100, speed 1.10) | 景品が主役級だぜ！ | 1.87s |
| `clip3_line1_fukuchan.wav` | 3 | Fukuchan | Irodori-TTS (ref: `Fukuchan_voice.wav`, seed 44, CPU) | 推しでギュンギュンでーす！ | 3.00s |
| `clip3_line2_yametaro.wav` | 3 | Yametaro | Irodori-TTS (ref: `Yametaro_voice.wav`, seed 44, CPU) | どうせワイ、全部当たりやん！ | 3.92s |
| `clip4_line1_okayaman.wav` | 4 | Okayaman | VOICEVOX:麒ヶ島宗麟 (style 53, speed 1.08) | おかやまん。豪華すぎて、大変驚いております。 | 3.37s |
| `clip5_line1_sobaya.wav` | 5 | Sobaya | Irodori-TTS (ref: `Sobaya_voice.wav`, seed 45, CPU) | 9月5日より順次発売！なくなり次第終了です！ | 4.44s |

---

## Clip 1: The grand curtain reveal

### Time

0:00-0:06

### First frame

A wide cinematic view inside Sobaya's cozy standing bar in the Window-Side Tribe area at night. Tokyo Tower glows through the office window. A huge closed navy curtain with gold trim covers a prize stage. Sobaya stands front-center with his mandatory white mask, short-sleeve T-shirt, muscular build, and FULL giant beer mug held upright in his left hand. With his right hand, he grips the curtain rope. Yumemin floats beside a small brass bell with the BONK mallet raised. Takosan waits beside the stage, preserving the black robe and all tentacles. The prize display and draw box are hidden.

### Last frame

The camera framing remains continuous but wider and brighter. The navy curtain is fully open and tied at both sides, revealing the complete orderly prize display in navy-and-gold presentation niches. The Sobaya figure, Takosan plush, Yumemin cushion, acrylic stands, mugs, charms, stickers, and Last One laptop-display prop are recognizable by silhouette and arrangement. Tokun, Yotan, Fukuchan, and Yametaro have entered in a jubilant diagonal formation. Sobaya still holds the FULL upright mug without drinking. Yumemin has just tapped the brass bell and holds the mallet upright. The lottery box sits closed on the counter. Okayaman's screen is still off-screen.

### Prop states

- Navy curtain — First: CLOSED. Action: Sobaya pulls the rope and the curtain opens visibly. Last: FULLY OPEN and tied at both sides.
- Prize display — First: physically hidden by the closed curtain. Last: fully revealed, all items upright and orderly; no item moves or vanishes.
- Lottery draw box — First: hidden behind the curtain. Last: visible on the counter with lid CLOSED and tickets inside.
- Sobaya giant beer mug — FULL and upright in his left hand throughout; no sip, spill, pour, or refill.
- Yumemin mallet — First: raised. Action: makes one gentle visible tap on the brass bell. Last: upright in Yumemin's grip.

### Dialogue and sound

- Sobaya mouths "一番くじ窓際族物語、開幕です！" (lip-sync to `clip1_line1_sobaya.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Yumemin cries "きゅー！" (lip-sync to `clip1_line2_yumemin.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Sound design: dramatic curtain whoosh, one bright BONK-bell chime, cheering, ukulele-and-electric-guitar launch sting. Keep sound effects under the attached dialogue.

### Seedance motion prompt

```text
Use the supplied character references only for identity and design, and use the supplied product artwork only as product-layout and palette reference. Interpolate precisely from Frame A to Frame B in one continuous spectacular commercial shot inside the warm Window-Side Tribe standing bar at night, with Tokyo Tower outside. Sobaya preserves his tall muscular adult build, mandatory white full-face mask, short-sleeve T-shirt, and mandatory giant glass beer mug. His mug remains FULL and upright in his left hand for the entire clip; he does not drink, spill, pour, or refill it. Sobaya pulls the rope with his right hand, visibly opening the CLOSED navy-and-gold curtain until it is FULLY OPEN and tied at both sides, revealing the complete orderly Ichiban Kuji prize display. As the curtain opens, Tokun, Yotan, Fukuchan, and Yametaro rush into their final cheerful formation while preserving every mandatory design element. Yumemin gently taps the brass opening bell exactly once with the BONK mallet and ends holding the mallet upright. Takosan remains mysterious and still beside the plush display, preserving the robe, white face, round eyes, two human arms, and tentacles. Sobaya mouths "一番くじ窓際族物語、開幕です！" in exact sync with the first attached audio. Yumemin mouths only the cry "きゅー！" in exact sync with the second attached audio. Use the attached audio files as the dialogue audio AS-IS and lip-sync to them; do NOT generate any voice, synthesized speech, or narration. Start with a slow heroic push, then accelerate into a bright crane-back reveal. Navy, warm gold, red lanterns, sparkling confetti, cheerful harmless spectacle, polished premium Japanese commercial, 16:9. No readable small text, no random letters, no watermark, no injury, no coercion, no intoxication, no realistic destruction.
```

### CapCut inputs (Clip 1)

- Start frame (Frame A): `clip1_start.png`
- End frame (Frame B): `clip1_end.png`
- Reference images (identity/design lock): `02_CHARACTERS/Sobaya.jpg`, `02_CHARACTERS/Takosan.png`, `02_CHARACTERS/Tokun.jpg`, `02_CHARACTERS/Yotan.jpg`, `02_CHARACTERS/Fukuchan.jpg`, `02_CHARACTERS/Yametaro.jpg`, `02_CHARACTERS/Yumemin.jpg`
- Product reference (layout/palette only): `product_ichiban_kuji_ref.png`
- Audio (attach to Seedance as input): `clip1_line1_sobaya.wav`, `clip1_line2_yumemin.wav` — use these files AS-IS as the dialogue audio track.
- Motion prompt: use the Seedance motion prompt above.
- Duration: 6s
- Aspect: 16:9

---

## Clip 2: Every prize is a headliner

### Time

0:06-0:12

### First frame

This is exactly the same image as Clip 1's last frame. The curtain is open, the entire prize display is orderly, all seven physically present members are in formation, the draw box is closed, and Okayaman's screen is off-screen.

### Last frame

The same stage and prop states remain intact. The group now presents the top prizes in a bold concert pose: Takosan gently hugs the Takosan plush with two human arms while all tentacles remain visible; Tokun points his ukulele toward the Yumemin cushion without letting go of the instrument; Yotan frames the Sobaya figure with the neck of his guitar; Fukuchan and Yametaro react delightedly. No display item has been removed except the Takosan plush, which is visibly held directly in front of its now-empty labeled niche. The lottery box remains closed.

### Prop states

- Prize display — First: all items in niches. Action: Takosan visibly lifts only the Takosan plush from its niche. Last: all other items remain upright; the plush is held directly in front of its empty niche.
- Lottery box — CLOSED throughout; tickets remain inside.
- Instruments, mug, and mallet — held continuously in their established safe states; no drinking or prop disappearance.

### Dialogue and sound

- Takosan mouths "もちもち。" (lip-sync to `clip2_line1_takosan.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Tokun mouths "ウクレレより存在感あるで！" (lip-sync to `clip2_line2_tokun.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Yotan mouths "景品が主役級だぜ！" (lip-sync to `clip2_line3_yotan.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Sound design: plush squeak, happy ukulele flourish, electric-guitar accent, crowd "ooh." Keep effects under the attached dialogue.

### Seedance motion prompt

```text
Continue from the exact fully revealed ensemble frame. Preserve the warm standing-bar location, open tied curtain, navy-and-gold display, all character identities, and every prop state. Takosan uses the two human arms to lift only the Takosan plush from its niche and gently hugs it directly in front of that now-empty niche; every octopus tentacle remains visible and the black hooded robe never changes. Takosan mouths "もちもち。" in sync with the first attached audio. Tokun keeps his mandatory aloha shirt, straw hat, and ukulele; without releasing it, he points the ukulele toward the Yumemin cushion and mouths "ウクレレより存在感あるで！" in sync with the second attached audio. Yotan keeps his blond hair, sunglasses, black leather rock clothing, and guitar; he frames the Sobaya figure with the guitar neck and mouths "景品が主役級だぜ！" in sync with the third attached audio. Fukuchan, Yametaro, Sobaya, and Yumemin react with delighted commercial energy while preserving their mandatory designs. Sobaya's giant mug stays FULL and upright with no drinking. The lottery box remains CLOSED. All other prizes remain upright and do not vanish. Use the three attached audio files AS-IS and lip-sync the correct character to each; do NOT generate any voice, synthesized speech, or narration. Use quick elegant product close-ups connected by a smooth lateral camera move, then settle back into the exact ensemble layout. Premium navy-and-gold commercial lighting, sparkling but readable product silhouettes, 16:9. No small generated text, no random letters, no watermark, no injury, no intoxication.
```

### CapCut inputs (Clip 2)

- Start frame (Frame A): `clip2_start.png` — relative symlink to the exact same file as Clip 1 Frame B (`clip1_end.png`).
- End frame (Frame B): `clip2_end.png`
- Reference images (identity/design lock): `02_CHARACTERS/Sobaya.jpg`, `02_CHARACTERS/Takosan.png`, `02_CHARACTERS/Tokun.jpg`, `02_CHARACTERS/Yotan.jpg`, `02_CHARACTERS/Fukuchan.jpg`, `02_CHARACTERS/Yametaro.jpg`, `02_CHARACTERS/Yumemin.jpg`
- Product reference (layout/palette only): `product_ichiban_kuji_ref.png`
- Audio (attach to Seedance as input): `clip2_line1_takosan.wav`, `clip2_line2_tokun.wav`, `clip2_line3_yotan.wav` — use these files AS-IS in this order.
- Motion prompt: use the Seedance motion prompt above.
- Duration: 6s
- Aspect: 16:9

---

## Clip 3: Yametaro draws a winner

### Time

0:12-0:18

### First frame

This is exactly the same image as Clip 2's last frame. Takosan holds the plush in front of its empty niche. The lottery box is still closed. Everyone else maintains the prize-presentation pose.

### Last frame

The stage remains unchanged. The lottery box lid is now visibly open. Yametaro holds exactly one unfolded ticket toward camera with a blank gold center reserved for editor compositing; the remaining tickets are visible inside the box. Fukuchan performs the full Gyun-Gyun pose beside him. Everyone celebrates. Takosan still holds the same plush, Sobaya keeps his mug upright without drinking, and Okayaman's large screen has descended above the group but remains dark and off.

### Prop states

- Lottery box — First: lid CLOSED, all tickets inside. Action: Yametaro visibly opens the lid, reaches in once, removes one ticket, and unfolds it. Last: lid OPEN, exactly ONE ticket in Yametaro's hand, remaining tickets inside.
- Okayaman screen — First: raised off-screen. Action: descends visibly after the ticket reveal. Last: hanging above the group, OFF.
- Takosan plush — held continuously in front of its empty niche.
- All other prizes, Sobaya's mug, instruments, and mallet — unchanged.

### Dialogue and sound

- Fukuchan mouths "推しでギュンギュンでーす！" from 0.00s to 3.00s (lip-sync to `clip3_line1_fukuchan.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Yametaro mouths "どうせワイ、全部当たりやん！" from 2.00s to 5.92s, deliberately overlapping Fukuchan's final excited second (lip-sync to `clip3_line2_yametaro.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Sound design: box lid click, paper unfolding, heartbeat pause, bright win chime, group cheer, soft mechanical screen descent. Keep effects under dialogue.

### Seedance motion prompt

```text
Continue from the exact prize-presentation frame. Preserve every character identity and every prop state. Yametaro, preserving his exact stylized design, purple shirt, and round glasses, steps to the CLOSED navy lottery box. He visibly opens the lid, reaches inside exactly once, removes exactly ONE ticket while all remaining tickets stay inside, unfolds that same ticket, and presents it toward camera. The ticket has a clean blank gold center for editor compositing, with no generated writing. Yametaro mouths "どうせワイ、全部当たりやん！" from 2.00s to 5.92s with comic resignation turning into a delighted grin, in exact sync with the second attached audio. Fukuchan preserves his stylish clothing, name badge, and SPONSOR strap, places both hands against his cheeks in the mandatory Gyun-Gyun pose, and mouths "推しでギュンギュンでーす！" from 0.00s to 3.00s in exact sync with the first attached audio. The two voices deliberately overlap only from 2.00s to 3.00s as an excited group reaction. At the end, a large remote screen visibly descends from above and stops over the group while remaining completely OFF and dark. Takosan continues holding the same plush. Sobaya's giant mug remains FULL and upright; nobody drinks. Use the attached audio files AS-IS and lip-sync the correct characters; do NOT generate any voice, synthesized speech, or narration. Camera: playful close-up on the hand entering the box, snap focus to the ticket, then fast crane-back for the group celebration and descending screen. Cheerful harmless confetti, premium commercial finish, 16:9. No random text, no watermark, no extra ticket appearing, no disappearing prizes, no injury, no coercion, no intoxication.
```

### CapCut inputs (Clip 3)

- Start frame (Frame A): `clip3_start.png` — relative symlink to the exact same file as Clip 2 Frame B (`clip2_end.png`).
- End frame (Frame B): `clip3_end.png`
- Reference images (identity/design lock): `02_CHARACTERS/Sobaya.jpg`, `02_CHARACTERS/Takosan.png`, `02_CHARACTERS/Tokun.jpg`, `02_CHARACTERS/Yotan.jpg`, `02_CHARACTERS/Fukuchan.jpg`, `02_CHARACTERS/Yametaro.jpg`, `02_CHARACTERS/Yumemin.jpg`
- Product reference (layout/palette only): `product_ichiban_kuji_ref.png`
- Audio (attach to Seedance as input): `clip3_line1_fukuchan.wav`, `clip3_line2_yametaro.wav` — use these files AS-IS as the dialogue audio track.
- Motion prompt: use the Seedance motion prompt above.
- Duration: 6s
- Aspect: 16:9

---

## Clip 4: The Window-Side King's official astonishment

### Time

0:18-0:24

### First frame

This is exactly the same image as Clip 3's last frame. The remote screen hangs above the celebrating group but remains off. Yametaro holds one unfolded ticket, the draw box is open, and all other props preserve their states.

### Last frame

The remote screen is on and displays Okayaman from his remote location, preserving his medium black hair, moustache, beard, black hooded jacket, and gentle smile. The screen is the only new illumination. The group looks upward with delighted anticipation. Every prize and prop remains in the exact prior state.

### Prop states

- Okayaman screen — First: OFF. Action: powers on with a soft scan-line glow. Last: ON, showing Okayaman smiling.
- Yametaro ticket and lottery box — unchanged: exactly one unfolded ticket held; lid open; remaining tickets inside.
- All prizes, Sobaya's mug, instruments, and mallet — unchanged.

### Dialogue and sound

- Okayaman mouths "おかやまん。豪華すぎて、大変驚いております。" (lip-sync to `clip4_line1_okayaman.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Sound design: elegant screen startup tone, tiny ceremonial gong after the line, group delighted murmur. Keep effects under the attached dialogue.

### Seedance motion prompt

```text
Continue from the exact frame with the large hanging remote screen OFF. Preserve all eight featured character designs and every established prop state. The screen powers on visibly with a gentle scan-line glow and reveals Okayaman in remote-video style: medium-length black hair, moustache and beard, black hooded jacket, and an unbroken gentle smile. He remains physically inside the screen and never appears in the room. Okayaman mouths "おかやまん。豪華すぎて、大変驚いております。" in exact sync with the attached audio while keeping calm formal delivery and a gentle smile. The seven members in the room turn their eyes upward with delighted anticipation, then give a synchronized pleased reaction. Yametaro continues holding the same ONE unfolded ticket; the lottery box stays OPEN with remaining tickets inside. Takosan keeps holding the same plush in front of its empty niche. Sobaya's giant mug remains FULL and upright; nobody drinks. Use the attached audio file AS-IS and lip-sync Okayaman to it; do NOT generate any voice, synthesized speech, or narration. Begin with the dark screen dominating the upper frame, let the glow illuminate the navy-and-gold set, then slowly pull back to include the smiling group. Premium cinematic commercial lighting, warm comedy, 16:9. No random text, no watermark, no extra physical Okayaman, no injury, no intoxication.
```

### CapCut inputs (Clip 4)

- Start frame (Frame A): `clip4_start.png` — relative symlink to the exact same file as Clip 3 Frame B (`clip3_end.png`).
- End frame (Frame B): `clip4_end.png`
- Reference images (identity/design lock): `02_CHARACTERS/Okayaman.jpg`, `02_CHARACTERS/Sobaya.jpg`, `02_CHARACTERS/Takosan.png`, `02_CHARACTERS/Tokun.jpg`, `02_CHARACTERS/Yotan.jpg`, `02_CHARACTERS/Fukuchan.jpg`, `02_CHARACTERS/Yametaro.jpg`, `02_CHARACTERS/Yumemin.jpg`
- Product reference (layout/palette only): `product_ichiban_kuji_ref.png`
- Audio (attach to Seedance as input): `clip4_line1_okayaman.wav` — use this file AS-IS as the dialogue audio track.
- Motion prompt: use the Seedance motion prompt above.
- Duration: 6s
- Aspect: 16:9

---

## Clip 5: All-cast release-date finale

### Time

0:24-0:30

### First frame

This is exactly the same image as Clip 4's last frame. Okayaman smiles on the active screen above the complete ensemble. All prize and prop states are preserved.

### Last frame

A majestic wide navy-and-gold final tableau in the same bar. All eight featured members are clearly readable: Okayaman smiles on the screen at top center; Sobaya stands center foreground raising his still-FULL giant mug upright; Takosan holds the plush with tentacles visible; Yumemin raises the BONK mallet beside the cushion; Tokun and Yotan hold their ukulele and guitar in a musical V; Fukuchan performs Gyun-Gyun; Yametaro displays the same one ticket. The complete prize line remains arranged behind them. A clean navy lower-third panel and a clean gold title panel are reserved for exact post-production compositing. Confetti freezes at a triumphant peak. Everyone smiles or shows an equivalent joyful pose.

### Prop states

- Every prize and prop keeps the state from Clip 4.
- Sobaya raises the same FULL mug upright without drinking or spilling.
- No prize, ticket, instrument, mallet, screen, or character appears or disappears.

### Dialogue and sound

- Sobaya mouths "9月5日より順次発売！なくなり次第終了です！" (lip-sync to `clip5_line1_sobaya.wav` — voice comes from the attached pre-generated audio, NOT generated).
- Sound design: full ukulele-and-rock-band fanfare, crowd cheer, camera-flash pops, final bell hit. Keep music and effects under the attached dialogue.

### Seedance motion prompt

```text
Continue from the exact Okayaman approval frame and preserve all character identities, prize positions, and prop states. Build one synchronized all-cast finale without cuts or disappearances. Okayaman remains only on the active screen at top center, smiling gently. Sobaya moves to center foreground and raises the same FULL giant glass beer mug upright without drinking or spilling; his muscular build, mandatory white full-face mask, and short-sleeve T-shirt stay unchanged. He mouths "9月5日より順次発売！なくなり次第終了です！" in exact sync with the attached audio. Takosan holds the same plush with the black robe and every tentacle visible. Yumemin raises the BONK mallet beside the blue cushion. Tokun and Yotan form a musical V with the mandatory ukulele and guitar. Fukuchan performs the mandatory two-hands-to-cheeks Gyun-Gyun pose. Yametaro presents the same ONE unfolded ticket. All prizes remain visible and orderly behind them. Create a clean blank gold title panel and blank navy lower-third panel for exact editor compositing; generate no writing. Confetti and warm sparkles rise to a triumphant peak. Use the attached audio file AS-IS and lip-sync Sobaya to it; do NOT generate any voice, synthesized speech, or narration. Smooth crane-back into a symmetrical premium commercial hero shot, navy and gold palette, Tokyo Tower visible, 16:9. No random text, no watermark, no missing character, no duplicate character, no spill, no intoxication, no injury, no coercion.
```

### CapCut inputs (Clip 5)

- Start frame (Frame A): `clip5_start.png` — relative symlink to the exact same file as Clip 4 Frame B (`clip4_end.png`).
- End frame (Frame B): `clip5_end.png`
- Reference images (identity/design lock): `02_CHARACTERS/Okayaman.jpg`, `02_CHARACTERS/Sobaya.jpg`, `02_CHARACTERS/Takosan.png`, `02_CHARACTERS/Tokun.jpg`, `02_CHARACTERS/Yotan.jpg`, `02_CHARACTERS/Fukuchan.jpg`, `02_CHARACTERS/Yametaro.jpg`, `02_CHARACTERS/Yumemin.jpg`
- Product reference (layout/palette only): `product_ichiban_kuji_ref.png`
- Audio (attach to Seedance as input): `clip5_line1_sobaya.wav` — use this file AS-IS as the dialogue audio track.
- Motion prompt: use the Seedance motion prompt above.
- Duration: 6s
- Aspect: 16:9

## Post-production and assembly notes

- Join the five clips without overlap. Frame B of each clip is the exact Frame A of the next clip.
- Use `product_ichiban_kuji_ref.png` as the authoritative overlay source for product artwork. Do not trust generated Japanese lettering.
- In the final frame, composite the exact title "一番くじ 窓際族物語" into the blank gold panel.
- Composite the exact lower-third: "2026年9月5日(土)より順次発売予定" and "メーカー希望小売価格：1回790円（税10%込）".
- Composite "なくなり次第終了" as a separate red badge.
- If the supplied artwork is an announcement mock-up rather than approved final retail art, replace it with the approved master before publication without changing the animation timing.
- Keep every dialogue file attached to Seedance as the source audio and mute or reject all generated speech.
- Use the product artwork only as an image overlay or product reference; do not animate tiny printed prize labels.
- Finish on smiles, a bright bell hit, and a two-frame hold for readability.

## Publication credits

VOICEVOX:Voidoll / VOICEVOX:白上虎太郎 / VOICEVOX:黒沢冴白 / VOICEVOX:麒ヶ島宗麟 / VOICEVOX:ずんだもん
