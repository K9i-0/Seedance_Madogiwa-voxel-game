# fix_list.md — keyframe verification round 1

Verification: Qwen3-VL 8b (`qwen3-vl:8b`) via `verify_frame.py`, one checklist per frame built from
`script.md`'s Prop state ledger, Fixture layout and NG-change rules, plus a direct read of each
image by Claude. **The VLM verdict alone was not sufficient** — see D1.

Decision: **regenerate the 13 frames from `ch2_end` onward.** `ch1_start` and `ch1_end` are kept.

---

## D1 — Fukuchan rendered as a chibi clone of Yametaro, at the wrong scale  ★ most serious

| | |
|---|---|
| **Frames** | `ch5_end`, `ch6_end`, `ch7_end`, `ch8_start`, `ch8_end`, `ch9_start`, `ch9_end`, `ch10_end`, `ch11_end` |
| **Problem** | Fukuchan is drawn as a chibi figure with an oversized head, small round white glasses, black bowl-cut hair and pink blush cheeks — visually the same creature as Yametaro, and roughly the SAME HEIGHT. Canon: he is a slim, tall adult man, and Yametaro's whole body should only reach his hip (`height_lineup.png`). In `ch6_end` Yametaro has additionally acquired Fukuchan's **lanyard** and a black jacket. |
| **Root cause** | **Our error.** `ch5_end`, `ch8_start` and `ch11_end` were generated from a stitched canvas containing Fukuchan's *photographic* model sheet. The skill explicitly warns against this: a character appearing mid-run should be introduced by **text description**, because stitching a sheet of a different visual register causes style mixing. The model resolved the photo-vs-chibi conflict by making him chibi. |
| **Detection** | **Missed by the VLM** — it passed "Fukuchan … black long coat and lanyard" and even "far taller than Yametaro". Caught by Claude opening `ch6_end` directly. This is exactly why the skill requires reading the images and not trusting `VERDICT:` lines. |
| **Fix** | Stop stitching Fukuchan's sheet (all three stitch points removed). Introduce and maintain him by text: explicit ADULT NORMAL HUMAN PROPORTIONS, normal-sized head (~1/7 of height), no round glasses, no blush cheeks, "NOT a chibi character, NOT a toy figure, NOT a doll", plus an explicit scale clause in every frame ("Yametaro only reaches Fukuchan's hip"). Added anti-contamination: Yametaro wears NO lanyard, name tag or jacket. |
| **Downstream** | All 9 frames regenerate. |

## D2 — Beer mug refills itself, then disappears, then refills

| | |
|---|---|
| **Frames** | `ch3_end` (beer), `ch4_end` (mug absent), `ch5_start` (mug absent), `ch6_end` (beer + foam), `ch7_end` (beer + foam) |
| **Problem** | The Prop state ledger says the mug is **EMPTY in all 15 columns** and that nobody ever drinks or pours. Actual chain: empty (ch1–ch2) → full → gone → full. A mug changing state with no on-screen action is the precise continuity break the skill warns about, and H3 would faithfully interpolate the nonsense. |
| **Contributing cause** | `ch2_end` introduced a **second drinking vessel** (a tall tumbler holding liquid) that is not in the ledger at all. From then on the chain had two vessels to confuse, and the "empty mug" instruction attached to the wrong one. |
| **Fix** | Global prop rule rewritten to "exactly ONE drinking vessel in the entire frame … NO second glass, NO tumbler, NO cup, NO bottle, and NO liquid of any kind visible anywhere". |
| **Downstream** | `ch3_end` onward regenerate. |

## D3 — `ch2_end` overexposed, washing out canonical colours

| | |
|---|---|
| **Frames** | `ch2_end` (and inherited by everything after it) |
| **Problem** | Yametaro's hair reads light brown and his shirt reads pink. The VLM flagged this as a design violation; on inspection the cause is exposure, not design — the frame is blown out. Either way the canonical black hair / purple shirt are not legible, which matters because this frame seeds the rest of the chain. |
| **Root cause** | **Our script direction.** The C2 prompt asked for a "blazing golden shaft", and the model delivered a blown-out frame. |
| **Fix** | Softened to "gentle golden afternoon light", plus an explicit exposure guard: "correctly exposed and NOT washed out, NOT blown out … hair stays clearly BLACK, shirt stays clearly PURPLE, colours stay saturated". `script.md`'s C2 wording needs the same softening so the Motion prompt does not re-request a blowout. |

## D4 — "three crushed cans" — NOT a defect, our checklist was wrong

| | |
|---|---|
| **Frames** | 8 frames reported FAIL on this item |
| **Finding** | The images consistently contain **three cans: two crushed on their sides plus one upright**. The ledger only ever required "exactly 3". Our verification checklist demanded three *crushed* cans, which is stricter than the ledger and stricter than the prompts. |
| **Fix** | No regeneration for this reason. The prop rule now states the achievable, already-consistent arrangement ("two crushed and lying on their sides plus one upright — three in total"), and the ledger row in `script.md` is reworded to match. Consistency across frames — which is what interpolation cares about — was never actually broken. |

## D5 — Cosmetic, accepted without regeneration

- `ch6_end`: the paper inquiry slips sit on top of a box rather than in a tray. Reads correctly as a growing pile; ledger intent satisfied.
- `ch4_end`: VLM reported "no booklet". Yametaro is lying face-down **on** the closed booklet, so it is occluded by design.
- Yametaro's seat is a black office chair, not the Aaronchure box stack — a pre-existing accepted deviation, see "Known deviation" in `script.md`. Two attempts failed to move the model off this prior, so the prop rule now says "a seat … with a stack of cardboard boxes beside him" rather than fighting it.

---

## Note on verification coverage

Frames `ch8_end`, `ch9_start`, `ch9_end`, `ch10_end` and `ch11_end` were **never verified in round 1**.
They returned `ERROR: image not found`, because the round-1 files were archived to
`round1_rejected/` while the VLM pass was still working through the list — our sequencing mistake,
not a tool failure.

This does not change the plan: all five are downstream of `ch5_end` and therefore inherit **D1** and
**D2** unconditionally, and all five were already slated for regeneration. Their round-1 verdicts
could only have added detail, never removed a frame from the fix list. All five ARE covered by the
round-2 verification below, so no frame ships unverified.

Lesson applied: the round-2 pass runs to completion **before** any file is moved or deleted.

## Regeneration plan (chain order, upstream first)

Discard and rebuild, in order — each frame seeds the next, so order is not optional:

`ch2_end` → `ch3_end` → `ch4_end` → `ch5_start` → `ch5_end` → `ch6_end` → `ch7_end` →
`ch8_start` → `ch8_end` → `ch9_start` → `ch9_end` → `ch10_end` → `ch11_end`

Kept: `ch1_start`, `ch1_end` (only D4, which is not a defect).
Also discarded: `ref_canvas_ch5_end.png`, `ref_canvas_ch7_end.png`, `ref_canvas_ch9_end.png`,
`ref_canvas_ch11_end.png` (rebuilt without Fukuchan's sheet), and `ref_canvas_ch8_start.png`
(no longer used — `ch8_start` now seeds directly from `ch7_end`).

Yametaro's sheet re-injection is retained at `ch3_end`, `ch5_end`, `ch7_end`, `ch9_end`, `ch11_end`
— his design held up well across the first pass, so that mechanism is working.

## Round 2 re-verification (after regeneration)

Re-check every regenerated frame, and add these two checks that round 1 lacked, since they are the
defects the first checklist failed to catch:

1. Fukuchan has NORMAL ADULT PROPORTIONS — normal-sized head, no oversized head, no round glasses,
   no blush cheeks — and is NOT the same kind of figure as Yametaro.
2. Fukuchan is MUCH TALLER than Yametaro: Yametaro reaches only about Fukuchan's hip. Ask the model
   to state the approximate height ratio rather than answer yes/no.
3. Exactly ONE drinking vessel in frame, and it is empty.

Claude must open every regenerated two-character frame directly. Round 1 proved the VLM can pass a
frame in which the single most important character is drawn as the wrong kind of creature.
