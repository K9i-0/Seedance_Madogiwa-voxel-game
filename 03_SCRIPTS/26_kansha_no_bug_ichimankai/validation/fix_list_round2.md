# Fix list — image validation round 2 (2026-08-07)

Scope: the 5 keyframes that currently exist in this run (`ch1_start`, `ch1_end`, `ch2_end`,
`ch3_end`, `ch4_end`). Method: `/image-validation` — per-frame checklists built from `script.md`'s
Prop state ledger / Fixture layout / NG-change rules, VLM pass with `qwen3-vl:8b`
(`validation/results/`), then a direct read of every frame by Claude, then a timeline cross-check.

VLM summary: 1 PASS (`ch1_start`) / 4 FAIL. Claude's verdict differs from the VLM on several items
— see the "VLM vs Claude" column.

## Blocking — run is incomplete

**B0. Only 5 of the 15 keyframes in the Keyframe inventory exist.** Missing: `ch5_start`,
`ch5_end`, `ch6_end`, `ch7_end`, `ch8_start`, `ch8_end`, `ch9_start`, `ch9_end`, `ch10_end`,
`ch11_end`. The round-1 fix list called for regenerating everything from `ch2_end` onward; the
chain stopped after `ch4_end`. Chapters 5-11 cannot be generated, and the round-1 defect D1
(Fukuchan drawn as a chibi clone) cannot be re-checked, until those frames exist.

## Defects

| # | File(s) | Aspect | Problem | VLM vs Claude | Fix policy | Downstream impact |
|---|---|---|---|---|---|---|
| 1 | `ch2_end` | Prop ledger | The glass is **FULL of beer with a foam head**. The ledger says the mug is EMPTY in all 15 columns and that nobody ever drinks, pours or lifts it. Round-1 defect D2 has **regressed**. | Both caught it | Regenerate with the one-vessel + no-liquid rule: "exactly ONE drinking vessel … NO liquid of any kind visible anywhere in the frame" | `ch3_end`, `ch4_end` (chained); C2/C3 shared boundary |
| 2 | `ch2_end` | Prop ledger | **FOUR cans** (one upright + three lying). Ledger says exactly 3 (`ch1_start`, `ch3_end`, `ch4_end` all correctly show 1 upright + 2 crushed). | **VLM passed this** — Claude counted 4 | Regenerate; state the achievable configuration ("two crushed lying down plus one upright — three in total, no fourth can") | same as #1 |
| 3 | `ch3_end`, `ch4_end` | Prop ledger | **TWO drinking vessels**: a handled mug (empty) plus a separate tumbler holding liquid. The ledger has exactly one vessel and no liquid anywhere. This is round-1 defect D2's contributing cause repeating. | Both caught it (VLM flagged item 8 on both) | Regenerate with the explicit vessel-count negative prompt | `ch4_end` chains from `ch3_end` |
| 4 | `ch1_start` → `ch1_end` | Continuity (within one chapter) | Yametaro's **seat changes inside Chapter 1**: in `ch1_start` he sits in the black office chair behind the desk; in `ch1_end` he sits on top of a cardboard box, legs dangling, with the chair now empty behind him. The C1 Motion prompt has no action that moves him, and the "Known deviation" note in `script.md` accepts the office chair — not a mid-chapter swap. H3 will invent a climb or morph the seat. | Missed by the VLM in `ch1_start`; it read `ch1_end` item 2 as a framing quibble | Regenerate `ch1_end` from `ch1_start` with the seat explicitly held ("he stays seated in the same chair; the seat under him does NOT change") | `ch2_end`, `ch3_end` inherit the box seat |
| 5 | `ch4_end` | NG element | Yametaro's face has **broken down**: the round glasses are stretched diagonally across the cheek instead of sitting on the eyes, the two lenses sit at different heights, a temple arm floats free into the hair, and the eye/blush features are duplicated and scattered. The glasses are still round, but the face is not intact. | **VLM passed item 3** ("glasses present, not rectangular") — the distortion is what it missed | Regenerate from `ch3_end` + `Yametaro_sheet.png` stitched canvas (the sheet re-injection the log says was skipped for this frame) | none (last frame of the existing chain) |
| 6 | all 5 frames | On-screen text / brand | The red cans carry a **Coca-Cola-style logo and label lettering**. `script.md` requires "no readable letters anywhere in frame", and a real brand mark is also not something to bake into a published video. | VLM flagged it on 4 frames; Claude confirms the marks are brand-evoking even where the letters are garbled | Add to the run's prop rule: "plain unbranded red cans with NO logo, NO lettering, NO barcode" | whole chain |

## Non-defects / accepted

- **Cardboard tray absent.** The VLM reported "no cardboard tray" on four frames. There genuinely is
  no distinct tray — only cardboard boxes. It is harmless while the ledger cell is EMPTY, but C6
  needs the tray to fill with inquiry slips, so **establish a visible empty tray in `ch1_start`**
  or the C6 transition has nothing to grow from. Logged as a script/prop issue, not a frame defect.
- **Vessel type drift** (`ch1_start`/`ch1_end` show a handle-less tumbler; `ch2_end` onward a handled
  mug). Cosmetic on its own, but it is the same mechanism behind #1/#3 — the model keeps
  re-deciding what the vessel is. The one-vessel rule fixes both.
- **Office chair instead of the Aaronchure box stack** — pre-existing accepted deviation, unchanged.
- **`ch4_end` "no booklet"** — occluded by his cheek, as in round 1. Not a defect.
- **Round-1 D3 (blown-out `ch2_end`) is fixed**: hair reads black, shirt reads purple.

## Timeline cross-check (Claude, no VLM)

- **Time of day — PASS.** soft morning (`ch1_start`, `ch1_end`) → gentle golden afternoon (`ch2_end`)
  → warm golden (`ch3_end`) → deep orange dusk with Tokyo Tower lit (`ch4_end`). The progression
  matches the ledger's Daylight row and each step is gradual — no day-to-night jump, and C4's
  Motion prompt does show the time-lapse that justifies the change.
- **Fixture layout — PASS.** The laptop lid stays open at a constant ~100° with its hinge on the
  rear edge in all five frames; the window wall carries no handle, latch or hinge in any frame.
- **Shared boundaries — PASS.** C1 end / C2 start / C3 start are single files, as the inventory
  requires; no duplicate-file drift.
- **Screen states — PASS.** DARK (`ch1_start`, `ch1_end`, `ch2_end`) → ONE red banner (`ch3_end`,
  `ch4_end`), and C3's Motion prompt shows him typing and breaking it on screen.
- **Booklet — PASS.** OPEN → CLOSED exactly once at `ch3_end`, with the closing action on screen.
- **Prop continuity — FAIL** on the mug/can rows only (defects #1-#3 above).

## Script-level finding

`script.md` has **no `## Scene ledger` section**. Time of day lives as a `Daylight` row inside the
Prop state ledger instead. Both the `/seedance` and `/local-video` skills require the separate
section, and `validate_run_bundle.py` machine-checks for it. The content is present and correct —
only the required structure is missing.
