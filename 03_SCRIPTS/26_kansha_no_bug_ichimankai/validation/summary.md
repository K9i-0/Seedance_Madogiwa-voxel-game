# Image validation summary (single-image VLM pass)

- Model: `qwen3-vl:8b`
- Per-item evidence: `validation/results/<image>.txt`
- NOTE: VLM verdicts are advisory — Claude must read every result (PASS included)
  and run the timeline cross-check (SKILL.md steps 4-5) before concluding.

| Image | Verdict |
|-------|---------|
| ch1_end.png | FAIL |
| ch1_start.png | PASS |
| ch2_end.png | FAIL |
| ch3_end.png | FAIL |
| ch4_end.png | FAIL |
