# Fix list — image validation (2026-08-07)

Scope: all 3 keyframes of this run (`clip1_start`, `clip1_end`, `clip2_end`). Method:
`/image-validation` — per-frame checklists built from `script.md`'s Prop state ledger and Fixture
layout, VLM pass with `qwen3-vl:8b` (`validation/results/`), then a direct read of every frame by
Claude, then a timeline cross-check.

VLM summary: **3 PASS / 0 FAIL.** Claude's direct read agrees on every blocking item. Two minor
deviations the VLM passed over are logged below; neither blocks generation.

## Blocking defects

**None.** This run's keyframes are consistent enough to hand to CapCut.

## Minor deviations (no regeneration required)

| # | File | Aspect | Observation | Recommendation |
|---|---|---|---|---|
| 1 | `clip2_end` | Prop ledger | The ledger says "one hand holds the neck while the free hand points". Yotan's pointing hand is correct, but his other hand rests on the guitar **body/pickups**, not the neck. The guitar itself is still slung and secure. | Do not regenerate. Reword the C2 ledger cell and Motion prompt to "his other hand stays on the guitar" so H3/Seedance is not asked to move the hand back to the neck mid-clip. |
| 2 | all 3 frames | Style | The keyframe generation prompts in `script.md` say "Polished anime illustration", but the frames are **photorealistic** (they inherit the photographic character sheets). All three frames match each other, so nothing is broken — but regenerating any frame with the prompt as written would produce a different style and break the set. | Update the three keyframe prompts in `script.md` to describe the actual established look before any frame is ever regenerated. |
| 3 | `clip1_start`, `clip1_end`, `clip2_end` | NG element | Yotan's sunglasses read slightly angular/cat-eye against the canonical round frames in `Yotan_sheet.png`. Consistent across all three frames. | Watch item only. Add "SMALL ROUND sunglasses — NOT angular, NOT cat-eye" to any future regeneration prompt. |

## Timeline cross-check (Claude, no VLM)

- **Fixture layout — PASS, all three frames.** Entrance door: hinges on the LEFT edge, silver lever
  handle at mid-height on the RIGHT edge, **and the handle stays visible after the door finishes
  closing** in `clip1_end` — the exact failure mode the Fixture layout table exists to prevent.
  Side door: hinges on the RIGHT edge, handle on the LEFT edge, correct in the closed state
  (`clip1_start`, `clip1_end`) and still on the LEFT edge of the panel once it swings open
  (`clip2_end`). No handle moved, disappeared or duplicated anywhere.
- **Prop continuity — PASS.** Entrance door half-open → closed, with C1's Motion prompt showing the
  swing. Side door closed → open, with C2 showing Sobaya entering through it. The guitar stays
  slung in all three frames. The beer mug appears only at the reveal, upright and half-full, with
  nobody drinking or pouring — matching every ledger cell.
- **Vessel count — PASS.** Exactly one beer mug in `clip2_end`; no stray second glass anywhere.
- **Lighting / time of day — PASS.** Warm, even interior light, identical across all three frames.
  No day-to-night jump. (This run has no windows and no `## Scene ledger` section, so there is no
  time-of-day cell to check against — see below.)
- **Speaker mouths — PASS.** `clip1_start` and `clip1_end`: Yotan's mouth CLOSED (Sobaya speaks
  off-screen, so no visible mouth should move). `clip2_end`: Yotan's mouth OPEN mid-retort, Sobaya
  masked with no mouth. The lip-sync signal is unambiguous in every frame.
- **Character design — PASS.** Sobaya's white mask with red markings fully covers his face, white
  T-shirt, gray muscular build, oversized mug — all match `Sobaya_sheet.png`. He is clearly taller
  and broader than Yotan. Yotan's blond hair, leather biker jacket and guitar match `Yotan_sheet.png`.
  No cross-character contamination.
- **Shared boundary — PASS.** Clip 2's Frame A reuses `clip1_end.png` as a single file; there is no
  separate `clip2_start.png` to drift.

## Script-level finding

`script.md` has **no `## Scene ledger` section**. The `/seedance` skill requires one and
`validate_run_bundle.py` machine-checks for it. This run is a single windowless interior shot at a
constant time of day, so nothing is visually wrong — but the section is missing and the Motion
prompts carry no time-of-day phrase, which is what normally stops Seedance from re-deciding the
lighting per clip.
