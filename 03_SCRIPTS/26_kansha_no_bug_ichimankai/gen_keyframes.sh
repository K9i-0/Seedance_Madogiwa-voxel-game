#!/bin/bash
# Generate all 15 keyframes for run 26_kansha_no_bug_ichimankai.
# Resumable: any frame whose PNG already exists is skipped, so this same script
# is reused for interruptions AND for the step-6 partial regeneration.
# Chain order matters — each frame is seeded from the previous one.
set -uo pipefail

RUN="$(cd "$(dirname "$0")" && pwd)"
REPO="$(cd "$RUN/../.." && pwd)"
DT=$REPO/.claude/skills/local-video/dt_generate.sh
STITCH="python3 $REPO/.claude/skills/local-video/stitch_refs.py"
SIZE=${SIZE:-1024x576}
export DT_STEPS=${DT_STEPS:-20}

cd "$RUN" || exit 1

# ---- reusable prompt blocks (kept identical across every frame) ----
STYLE="Photorealistic live-action-style cinematic still: a real high-rise Tokyo office interior, true-to-life materials, real daylight, shallow depth of field, real camera optics. Every human character is rendered as a REAL PHOTOGRAPHED PERSON. Yametaro ALONE is rendered as a soft matte 3D chibi toy figure — smooth matte vinyl-toy surfaces, thick dark outline, oversized head, roughly 90 cm tall — standing physically inside that real space and lit by the same real light. NOT flat 2D anime, NOT cartoon lineart, NOT a drawing, NOT a painting. Single still frame, one coherent scene, no text overlay, no sheet-style panels, no labels, no watermark, no readable letters anywhere in frame."

NGY="Yametaro is ALWAYS WEARING SMALL ROUND glasses with THIN WHITE / PALE SILVER rims — the frames are white, NOT black, NOT dark, NOT thick — and the glasses do NOT disappear. He keeps his oversized head, black bowl-cut hair with a pointed widow's peak, pink blush cheeks, purple patterned shirt and black trousers; his design never shifts toward a realistic human. Yametaro wears NO lanyard, NO name tag, NO badge and NO black jacket or coat — only his purple patterned shirt and black trousers; none of Fukuchan's clothing ever appears on Yametaro."

# Constant prop/set facts appended to EVERY frame prompt. These three were all
# violated in the first attempt at ch1_start (mug drawn full of beer, only two cans,
# a black office chair instead of the cardboard-box seat), and because every frame is
# seeded from the previous one, a miss here propagates through the whole chain.
PROPS="There is exactly ONE drinking vessel in the entire frame: a single EMPTY clear glass beer mug with a handle, holding NO beer, NO liquid, NO froth and NO foam head. There is NO second glass, NO tumbler, NO cup and NO bottle anywhere, and NO liquid of any kind is visible anywhere in the frame; nobody drinks, lifts or pours anything. Exactly THREE empty aluminium cans lie on the desk: two crushed and lying on their sides plus one upright — three cans in total, never more and never fewer. Yametaro sits on a seat behind the corrugated cardboard desk with a stack of cardboard boxes beside him. The desk is plain corrugated cardboard."

NGF="Fukuchan is an ADULT MAN WITH NORMAL REALISTIC HUMAN BODY PROPORTIONS: slim, tall, 48 years old, with a NORMAL-SIZED adult head, tidy black hair, a loose black long coat over a white graphic T-shirt, black trousers, white sneakers and a lanyard name tag round his neck, smiling warmly. Fukuchan is emphatically NOT a chibi character, NOT a toy figure and NOT a doll: his head is NORMAL adult size (roughly one seventh of his height), he does NOT have an oversized head, he does NOT wear round glasses, and he does NOT have pink blush cheeks. SCALE IS CRITICAL: Fukuchan is MUCH TALLER than the tiny Yametaro — standing side by side, the whole of Yametaro only reaches up to Fukuchan's hip, and Fukuchan's head is far smaller than Yametaro's huge head. The two characters must never look the same size and must never look like the same kind of creature."

SET="The Window-Side Tribe area on a high floor of a Tokyo office: a floor-to-ceiling glass curtain wall on frame right with Tokyo Tower visible outside, a corrugated cardboard desk, and a stack of cardboard boxes used as a chair behind it. On the desk, left to right: three crushed empty cans, an EMPTY glass beer mug, an OPEN laptop whose lid stays at a constant ~100 degrees with its hinge on the REAR edge away from camera, and a thick paper spec booklet. A plain navy noren and a red paper lantern hang on the back wall. All signage carries only abstract brush-like marks with NO readable letters. The window wall has no hinge, handle or latch."

gen() { # gen <out> <seed> <input|none> <<<prompt
  local out=$1 seed=$2 img=$3
  if [ -f "$out" ]; then echo "SKIP (exists): $out"; return 0; fi
  echo "### GENERATING $out (seed=$seed, from=$img, steps=$DT_STEPS) $(date +%H:%M:%S)"
  # ABORT the whole run on the first failure. The chain is strictly sequential —
  # each frame is the seed for the next — so continuing past a failure just
  # produces a cascade of "input image not found" and hides the real error.
  if ! "$DT" "$out" "$img" "$seed" "$SIZE"; then
    echo "### FATAL: generation failed for $out — aborting the chain $(date +%H:%M:%S)" >&2
    exit 1
  fi
  if [ ! -f "$out" ]; then
    echo "### FATAL: $DT returned success but $out does not exist — aborting $(date +%H:%M:%S)" >&2
    exit 1
  fi
  echo "### DONE $out $(date +%H:%M:%S)"
}

# ---------- reference canvases (generation intermediates, not H3 inputs) ----------
[ -f ref_canvas_ch1_start.png ] || $STITCH ref_canvas_ch1_start.png Yametaro_sheet.png --size 2048x1152

# ================= C1 =================
gen ch1_start.png 42 ref_canvas_ch1_start.png <<EOF
The input image is a character model sheet of Yametaro — an identity/design reference ONLY, NOT a composition reference. Using exactly that character, create the FIRST-FRAME still of a video shot. $SET Yametaro sits on the stack of cardboard boxes behind the cardboard desk, slumped forward and deflated, shoulders dropped, both small hands limp on the desktop, looking down at the OPEN paper spec booklet lying flat with its pages up. His mouth is CLOSED in a small flat line. The laptop screen is completely DARK and switched off. The glass beer mug is EMPTY. There are exactly three crushed empty cans. A cardboard tray beside the laptop is EMPTY. Soft morning daylight. $NGY $PROPS $STYLE
EOF

gen ch1_end.png 43 ch1_start.png <<EOF
This is the start frame of a video shot. Keep the SAME character, the same photographic rendering style, the same framing, the same lighting and the same location — change ONLY what the motion changes. Create the LAST-FRAME still: Yametaro now sits bolt upright on the stack of cardboard boxes, both small palms pressed flat together in front of his chest in a serene prayer, eyes closed, with a small calm smile. His mouth stays CLOSED. Everything else on the desk is EXACTLY unchanged: the paper spec booklet is still OPEN and flat with its pages up, the laptop screen is still completely DARK, the glass beer mug is still EMPTY, there are still exactly three crushed cans, and the cardboard tray is still EMPTY. The laptop lid stays OPEN at the same ~100 degrees with its hinge on the REAR edge. Soft morning daylight, unchanged. $NGY $PROPS $STYLE
EOF

# ================= C2 =================
gen ch2_end.png 44 ch1_end.png <<EOF
This is the start frame of a video shot. Keep the SAME character, rendering style, framing and location — change ONLY the light. Create the LAST-FRAME still: Yametaro holds the exact same pose, palms pressed flat together in front of his chest, eyes closed, serene small smile, mouth CLOSED. The daylight through the floor-to-ceiling window has warmed into a gentle golden afternoon light that rakes softly across the cardboard desk and puts a warm rim-light on his oversized head, and a faint golden glow gathers between his pressed palms. The image is correctly exposed and NOT washed out, NOT blown out and NOT overexposed: Yametaro's hair stays clearly BLACK, his shirt stays clearly PURPLE, and all colours stay saturated and true. Every prop is EXACTLY unchanged: the paper spec booklet is still OPEN and flat, the laptop screen is still completely DARK, the glass beer mug is still EMPTY, exactly three crushed cans, the cardboard tray still EMPTY, the laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. $NGY $PROPS $STYLE
EOF

# ================= C3 (sheet re-injection) =================
[ -f ref_canvas_ch3_end.png ] || $STITCH ref_canvas_ch3_end.png ch2_end.png Yametaro_sheet.png --size 2048x1152
gen ch3_end.png 45 ref_canvas_ch3_end.png <<EOF
The LEFT panel is the start frame of a video shot — match its framing, lighting, location and photographic rendering style exactly. The RIGHT panel is Yametaro's character model sheet, an identity/design reference ONLY, NOT a composition reference. Create a single LAST-FRAME still of that same shot (one coherent scene, NOT a two-panel image): the paper spec booklet is now CLOSED flat on the cardboard desk, the laptop screen now shows ONE single red error banner — one abstract solid red horizontal bar with absolutely NO readable text or letters on it — and Yametaro is bowing his oversized head low over his pressed-together palms in a small apology, eyes squeezed shut, mouth CLOSED. The glass beer mug is still EMPTY, there are still exactly three crushed cans, and the cardboard tray is still EMPTY. The laptop lid stays OPEN at ~100 degrees with its hinge on the REAR edge. Gentle warm golden daylight, correctly exposed and never washed out. $NGY $PROPS $STYLE
EOF

# ================= C4 =================
gen ch4_end.png 46 ch3_end.png <<EOF
This is the start frame of a video shot. Keep the SAME character, rendering style, framing and location. Create the LAST-FRAME still: the daylight has changed to a deep orange dusk and Tokyo Tower is lit up outside the window. Yametaro has collapsed face-down onto the cardboard desk, one cheek resting on the CLOSED paper spec booklet, both arms dangling limp at his sides, fast asleep with a tiny contented smile, mouth CLOSED. His small round white-rimmed glasses are still on his face even though he is face-down. The laptop screen still shows exactly ONE single red error banner — one abstract solid red horizontal bar with NO readable text — glowing in the dimmer room. The paper spec booklet is still CLOSED. The glass beer mug is still EMPTY, exactly three crushed cans, cardboard tray still EMPTY, laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. He is happily exhausted, comedic, never gloomy. $NGY $PROPS $STYLE
EOF

# ================= C5 (hard cut: 2-year time skip, slightly wider) =================
gen ch5_start.png 47 ch4_end.png <<EOF
This is a frame from the previous shot of the same video. Keep the SAME character, the same photographic rendering style, the same set and the same props, but this is a NEW shot two years later: pull the camera back slightly so the mid-background floor on frame left is visible, and change the light to bright midday daylight. Create the FIRST-FRAME still of that new shot: Yametaro sits upright on the stack of cardboard boxes with both small palms pressed flat together in front of his chest, eyes closed, just finishing a prayer, mouth CLOSED. The paper spec booklet on the desk is still CLOSED and now carries a thin film of dust. The laptop screen still shows exactly ONE single red error banner — one abstract solid red horizontal bar with NO readable text. The glass beer mug is still EMPTY, exactly three crushed cans, the cardboard tray still EMPTY, the laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. No other person is in the room yet. $NGY $PROPS $STYLE
EOF

# ================= C5 end (Fukuchan's first appearance — both sheets re-injected) =================
[ -f ref_canvas_ch5_end.png ] || $STITCH ref_canvas_ch5_end.png ch5_start.png Yametaro_sheet.png --size 2048x1152
gen ch5_end.png 48 ref_canvas_ch5_end.png <<EOF
The LEFT panel is the start frame of a video shot — match its framing, lighting, location and rendering style exactly. The RIGHT panel is Yametaro's character model sheet, an identity/design reference ONLY, NOT a composition reference. Create a single LAST-FRAME still of that same shot (one coherent scene, NOT a two-panel image): Yametaro has opened his eyes and tipped his oversized head back to look up and out through the window, small round eyes wide, eyebrows raised, mouth CLOSED in a puzzled flat line. Standing a few steps behind him in the mid-background on frame left is a SECOND, COMPLETELY DIFFERENT character: Fukuchan, a tall adult man with normal human proportions, drawn in EXACTLY the same rendering style as the rest of the image but at realistic adult scale, smiling warmly and watching, holding a smartphone with a completely DARK screen down at his side, mouth CLOSED. Every prop is unchanged: the paper spec booklet still CLOSED and dusty, the laptop screen still showing exactly ONE abstract solid red horizontal bar with NO readable text, the glass beer mug still EMPTY, exactly three crushed cans, the cardboard tray still EMPTY, the laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. Bright midday light. $NGY $NGF $PROPS $STYLE
EOF

# ================= C6 =================
gen ch6_end.png 49 ch5_end.png <<EOF
This is the start frame of a video shot. Keep the SAME two characters, rendering style, location and lighting; the camera has pushed in slightly toward the laptop. Create the LAST-FRAME still: the laptop screen is now a FULL WALL of stacked red error bars filling the entire screen — all abstract solid red horizontal bars with absolutely NO readable text, letters or code — and the cardboard tray beside the laptop has become a tall, overflowing stack of paper inquiry slips. Yametaro sits with both small hands resting in his lap, having touched nothing, blinking at the screen with mild confusion, mouth CLOSED. Fukuchan still stands in the mid-background, smiling warmly, still holding his smartphone with a completely DARK screen, mouth CLOSED. The paper spec booklet is still CLOSED and dusty, the glass beer mug still EMPTY, exactly three crushed cans, the laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. Bright midday light. Nobody is angry or in trouble; deadpan comedy. $NGY $NGF $PROPS $STYLE
EOF

# ================= C7 (sheet re-injection) =================
[ -f ref_canvas_ch7_end.png ] || $STITCH ref_canvas_ch7_end.png ch6_end.png Yametaro_sheet.png --size 2048x1152
gen ch7_end.png 50 ref_canvas_ch7_end.png <<EOF
The LEFT panel is the start frame of a video shot — match its framing, lighting, location and photographic rendering style exactly. The RIGHT panel is Yametaro's character model sheet, an identity/design reference ONLY, NOT a composition reference. Create a single LAST-FRAME still of that same shot (one coherent scene, NOT a two-panel image): Yametaro's pressed-together palms are sinking slowly down toward his lap after a finished prayer, his eyes now open, mouth CLOSED. The keyboard directly in front of him is perfectly still, completely untouched, carrying a light film of dust with not one key depressed. The laptop screen keeps its FULL WALL of stacked abstract solid red horizontal bars with NO readable text, scrolled one notch further. Fukuchan is still standing in the mid-background, smiling warmly, holding his smartphone with a completely DARK screen, mouth CLOSED. The paper spec booklet is still CLOSED and dusty, the cardboard tray still holds its tall stack of paper slips, the glass beer mug is still EMPTY, exactly three crushed cans, the laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. Bright midday light. $NGY $NGF $PROPS $STYLE
EOF

# ================= C8 (hard cut: new two-shot for dialogue; Fukuchan sheet re-injected) =================
gen ch8_start.png 51 ch7_end.png <<EOF
This is a frame from the previous shot of the same video — keep its two characters, props, lighting, location and rendering style exactly, including Fukuchan's normal adult proportions and his much greater height. Create the FIRST-FRAME still of a NEW camera setup: a static two-shot from slightly beside and behind the cardboard desk. Fukuchan stands on frame left, crouched slightly down toward the desk with his warm friendly smile, his MOUTH CLEARLY OPEN mid-sentence as he speaks, holding his smartphone with a completely DARK screen in one hand. Yametaro sits small on frame right with both hands in his lap, looking up at Fukuchan, his MOUTH FIRMLY CLOSED because he is only listening. Every prop is unchanged: the laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet is CLOSED and dusty, the glass beer mug is EMPTY, exactly three crushed cans, the laptop lid OPEN at ~100 degrees with its hinge on the REAR edge. Bright midday light. A friendly, curious question between colleagues — no accusation, no anger. $NGY $NGF $PROPS $STYLE
EOF

gen ch8_end.png 52 ch8_start.png <<EOF
This is the start frame of a video shot. Keep the SAME two characters, framing, rendering style, lighting, location and every prop — change ONLY what the motion changes. Create the LAST-FRAME still: Fukuchan is finishing his question, still leaning in toward the desk, his head tilted with friendly curiosity, his mouth JUST CLOSING on the last syllable. Yametaro's mouth is still FIRMLY CLOSED and his small round eyes are now wide. Every prop is EXACTLY unchanged: the laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet is CLOSED and dusty, the glass beer mug is EMPTY, exactly three crushed cans, Fukuchan's smartphone screen is still completely DARK, the laptop lid still OPEN at ~100 degrees with its hinge on the REAR edge. Bright midday light. $NGY $NGF $PROPS $STYLE
EOF

# ================= C9 (hard cut: close single for the punchline) =================
gen ch9_start.png 53 ch8_end.png <<EOF
This is a frame from the previous shot of the same video. Keep the SAME characters, props, lighting, location and photographic rendering style, but this is a NEW camera setup: a static CLOSE SINGLE on Yametaro, framed low and looking slightly up at him, with Fukuchan's black coat and lanyard only just visible and completely out of focus at the frame edge. Create the FIRST-FRAME still of that new shot: Yametaro has brought both small palms flat together in front of his chest again, wearing a completely serene, gentle, innocent expression, his MOUTH CLEARLY OPEN mid-word because he is the one speaking now. Fukuchan, out of focus at the frame edge, has his mouth CLOSED. Behind Yametaro and softly out of focus, the laptop screen still glows with its FULL WALL of abstract solid red horizontal bars with NO readable text. Bright midday light. He is sincerely serene, not smug. $NGY $NGF $PROPS $STYLE
EOF

[ -f ref_canvas_ch9_end.png ] || $STITCH ref_canvas_ch9_end.png ch9_start.png Yametaro_sheet.png --size 2048x1152
gen ch9_end.png 54 ref_canvas_ch9_end.png <<EOF
The LEFT panel is the start frame of a video shot — match its close framing, lighting, location and photographic rendering style exactly. The RIGHT panel is Yametaro's character model sheet, an identity/design reference ONLY, NOT a composition reference. Create a single LAST-FRAME still of that same shot (one coherent scene, NOT a two-panel image): Yametaro holds the same serene pose with both palms pressed flat together in front of his chest, his mouth JUST CLOSING on the last syllable, eyes softly shut, the picture of innocence. Fukuchan stays out of focus at the frame edge with his mouth CLOSED. Behind Yametaro and softly out of focus, the laptop screen still glows with its FULL WALL of abstract solid red horizontal bars with NO readable text. Bright midday light. $NGY $NGF $PROPS $STYLE
EOF

# ================= C10 =================
gen ch10_end.png 55 ch9_end.png <<EOF
This is the start frame of a video shot. Keep the SAME characters, rendering style, location and lighting; the focus has racked and the camera panned slightly onto the smartphone in Fukuchan's hand. Create the LAST-FRAME still: Fukuchan's smartphone is now in sharp focus and its screen is packed edge to edge with a dense stack of rectangular notification cards — all abstract grey-and-red rounded rectangles with absolutely NO readable text, letters, names or logos. Fukuchan looks down at the phone with delighted, completely unbothered surprise, eyebrows raised, mouth CLOSED. Yametaro is still serene in the softly out-of-focus background with both palms pressed together and his eyes softly shut, mouth CLOSED. Every other prop is unchanged: the laptop screen keeps its FULL WALL of abstract solid red horizontal bars with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet is CLOSED and dusty, the glass beer mug is EMPTY, exactly three crushed cans, the laptop lid OPEN at ~100 degrees with its hinge on the REAR edge. Nobody panics and nobody is in trouble; everyone stays cheerful. $NGY $NGF $PROPS $STYLE
EOF

# ================= C11 (wide ending; both sheets re-injected) =================
[ -f ref_canvas_ch11_end.png ] || $STITCH ref_canvas_ch11_end.png ch10_end.png Yametaro_sheet.png --size 2048x1152
gen ch11_end.png 56 ref_canvas_ch11_end.png <<EOF
The LEFT panel is a frame from a video shot — keep its two characters, props, location and rendering style exactly, including Fukuchan's normal adult proportions and his much greater height. The RIGHT panel is Yametaro's character model sheet, an identity/design reference ONLY, NOT a composition reference. Create a single LAST-FRAME still (one coherent scene, NOT a two-panel image) of a WIDE shot of the whole Window-Side Tribe office area, Tokyo Tower visible through the floor-to-ceiling window behind. Yametaro is still seated on the stack of cardboard boxes with both small palms pressed flat together in a serene, unbroken prayer, eyes closed, mouth CLOSED, a soft warm glow gathering gently around him in the midday shaft of light. Fukuchan has crouched down beside him and holds his smartphone out at arm's length to take one cheerful selfie of the two of them, grinning warmly, mouth CLOSED; even crouching he is clearly much bigger than the little figure. His phone screen keeps its dense stack of abstract grey-and-red notification cards with NO readable text. The laptop's FULL WALL of abstract solid red horizontal bars glows on the cardboard desk beside them with NO readable text, the cardboard tray keeps its tall stack of paper slips, the paper spec booklet is CLOSED and dusty, the glass beer mug is EMPTY, exactly three crushed cans, the laptop lid OPEN at ~100 degrees with its hinge on the REAR edge. Warm, funny, affectionate ending — two colleagues smiling together, nobody blamed, no gloom. $NGY $NGF $PROPS $STYLE
EOF

echo "=== ALL KEYFRAMES DONE $(date +%H:%M:%S) ==="
ls -la "$RUN"/ch*.png
