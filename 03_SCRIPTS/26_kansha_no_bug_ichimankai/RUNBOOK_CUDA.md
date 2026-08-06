# RUNBOOK — generating this video's chapters on a CUDA machine

This run's script, voices and keyframes were all produced locally on a Mac (M1 Pro, 32GB).
**The MiniMax H3 video-generation step could not run there**, so this directory is a complete,
portable input bundle: copy it to a CUDA box and run the 11 chapter workflows.

## Why the video step moved to CUDA

All four H3 weight variants were tested in ComfyUI on Apple Silicon (MPS). None can run:

| Variant | Size | Result on MPS |
|---|---|---|
| `*_pruned_int8_convrot` | 21 GB | `NotImplementedError: aten::_int_mm` — no MPS kernel; ComfyUI's `comfy_kitchen` int8 path has no fallback |
| `*_pruned_fp8_scaled` | 21 GB | `RuntimeError: Undefined type Float8_e4m3fn` — MPS has no float8 dtype |
| `qwen3vl_32b_..._nvfp4_awq` | 16 GB | NVIDIA-only quantization |
| `*_pruned_bf16` | 40 GB | Loads (MPS-native) then `MPS backend out of memory: allocated 41.80 GiB, max allowed 42.43 GiB` — and that was at MINIMUM settings (90 frames, 640x384, 2 steps) |

Both models always loaded successfully, so this was never purely a capacity problem — the two
quantized formats that fit in memory cannot execute on MPS, and the one format that executes
does not fit. On CUDA all of these work normally.

Note the text encoder was fine even on the Mac, because ComfyUI places it on **CPU**, where
`aten::_int_mm` does exist. Only the transformer failed.

## What is in this bundle

| Files | What they are |
|---|---|
| `script.md` | The canonical script: 11 chapters, 86.6s, prop-state ledger, fixture layout, dialogue-audio table, per-chapter H3 inputs, generation protocol, assembly recipe, credits |
| `ch*_workflow.json` | 11 ready-to-run ComfyUI **API-format** workflows, one per chapter |
| `ch*_prompt.txt` | Each chapter's Motion prompt, extracted verbatim from `script.md` |
| `ch*_start.png` / `ch*_end.png` | 15 keyframes (1024x576) — H3 upscales these to its 1344x768 canvas |
| `ch*_nar1.wav`, `ch8_line1_fukuchan.wav`, `ch9_line1_yametaro.wav` | 11 Irodori-TTS voice takes |
| `Yametaro_sheet.png`, `Fukuchan_sheet.png`, `height_lineup.png` | Identity/scale references (R2V chapters only) |
| `ref_canvas_*.png` | Keyframe-generation intermediates. **NOT H3 inputs** — ignore them |
| `build_h3_workflow.py`, `extract_prompts.py`, `h3_run.py`, `assemble.sh` | Tooling to rebuild workflows and assemble the final cut |

Chapter/mode/duration map (all frame counts sit on H3's 17k+5 grid at 24fps):

| Ch | Mode | Frames | Seconds | Inputs |
|---|---|---|---|---|
| 1 | I2V | 294 | 12.250 | ch1_start → ch1_end |
| 2 | I2V | 124 | 5.167 | ch1_end → ch2_end |
| 3 | I2V | 175 | 7.292 | ch2_end → ch3_end |
| 4 | I2V | 158 | 6.583 | ch3_end → ch4_end |
| 5 | I2V | 175 | 7.292 | ch5_start → ch5_end (hard cut: 2-year skip) |
| 6 | I2V | 277 | 11.542 | ch5_end → ch6_end |
| 7 | I2V | 209 | 8.708 | ch6_end → ch7_end |
| 8 | **R2V** | 124 | 5.167 | 5 images + `ch8_line1_fukuchan.wav` — Fukuchan speaks |
| 9 | **R2V** | 90 | 3.750 | 5 images + `ch9_line1_yametaro.wav` — Yametaro speaks |
| 10 | I2V | 124 | 5.167 | ch9_end → ch10_end |
| 11 | I2V | 328 | 13.667 | ch10_end → ch11_end |

Only chapters 8 and 9 attach audio to the generator (R2V is the only mode that accepts audio,
and lip-sync is the reason). Every narration wav is laid over the finished video with ffmpeg.

## Setup on the CUDA machine

1. **ComfyUI v0.30.0 or newer** (the `MiniMaxH3*` nodes ship in `comfy_extras/nodes_minimax_h3.py`):
   ```
   git clone https://github.com/comfyanonymous/ComfyUI && cd ComfyUI
   python -m venv venv && ./venv/bin/pip install -U pip wheel
   ./venv/bin/pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
   ./venv/bin/pip install -r requirements.txt
   ```
   Confirm the nodes registered: `curl -s localhost:8188/object_info | grep -o MiniMaxH3[A-Za-z]*`

2. **Weights** — from `Comfy-Org/MiniMax-H3`, into `ComfyUI/models/`:

   | File | Destination |
   |---|---|
   | `diffusion_models/minimax_h3_fl2va_pruned_*.safetensors` | `models/diffusion_models/` (I2V chapters) |
   | `diffusion_models/minimax_h3_ref2va_pruned_*.safetensors` | `models/diffusion_models/` (R2V chapters 8, 9) |
   | `text_encoders/qwen3vl_32b_minimax_h3_*.safetensors` | `models/text_encoders/` |
   | `vae/minimax_h3_video_vae_fp16.safetensors` | `models/vae/` |
   | `vae/minimax_h3_audio_vae_fp32.safetensors` | `models/vae/` |

   **Pick the variant for your GPU** — the workflows currently name the INT8 pair:

   | GPU | Recommended |
   |---|---|
   | Blackwell (RTX 50xx, B200) | `nvfp4_awq` encoder + `pruned_fp8_scaled` — fastest, smallest |
   | Ada / Hopper (RTX 40xx, L40S, H100) | `pruned_fp8_scaled` + `int8_convrot` encoder (native fp8) |
   | Ampere (RTX 30xx, A100) | `pruned_int8_convrot` + `int8_convrot` encoder (INT8 tensor cores) — **what the JSONs name now** |
   | Plenty of VRAM (80 GB+) | `pruned_bf16` for maximum quality |

   To switch variants, regenerate rather than hand-editing 11 files:
   ```
   H3_ENCODER=qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors \
   H3_UNET_I2V=minimax_h3_fl2va_pruned_fp8_scaled.safetensors \
   H3_UNET_R2V=minimax_h3_ref2va_pruned_fp8_scaled.safetensors \
   ./gen_all_workflows.sh <this_dir>
   ```
   (or edit node `127` `unet_name` and node `128` `clip_name` in each JSON)

3. **Memory.** The encoder is ~27 GB (INT8) and each transformer ~21 GB (INT8/fp8) or ~40 GB
   (bf16). ComfyUI will offload between them, so a 24 GB card works with enough system RAM, but
   expect swapping. 48 GB+ is comfortable. `--disable-smart-memory` did **not** evict the encoder
   in testing, because it sits on CPU — don't rely on that flag to solve pressure.

4. **Copy the inputs ComfyUI reads** (it only loads from its own `input/` dir):
   ```
   cp *.png *.wav /path/to/ComfyUI/input/
   ```

## Running

Start ComfyUI, then run chapters one at a time:

```
cd ComfyUI && ./venv/bin/python main.py --listen 127.0.0.1 --port 8188
python3 h3_run.py ch8_workflow.json --out ch8.mp4
```

`h3_run.py` submits the graph, polls until completion and downloads the video.

### Pilot first — batch generation is FORBIDDEN until it passes

**Run chapter 8 first** (the first dialogue chapter — lip-sync is the highest-risk thing here),
then check all of:

- [ ] The dialogue is the attached wav (correct voice, no synthesized or doubled voice)
- [ ] **Fukuchan** lip-syncs, and Yametaro's mouth stays closed the whole chapter
- [ ] Mouth motion starts and stops WITH the audio (no lip-flap during silence)
- [ ] The video starts/ends on (or acceptably near) `ch8_start.png` / `ch8_end.png`
- [ ] Prop states match the ledger: beer mug **EMPTY**, exactly 3 crushed cans, spec booklet CLOSED and dusty, laptop lid OPEN ~100° with its hinge on the REAR edge, screen a full wall of abstract red bars with no readable text
- [ ] Yametaro keeps SMALL ROUND WHITE-RIMMED glasses; Fukuchan keeps his black long coat + lanyard
- [ ] Duration is 124 frames / 5.167s
- [ ] No sheet text labels leaked into the video

Then run chapter 9 (the other R2V) and re-check lip-sync, then the nine I2V chapters.

**Chapter 9 needs specific attention:** its real speech is 1.22s in a 3.75s chapter (33%), below
the ~60% guideline, because 90 frames is the smallest H3 allows. If the mouth keeps moving through
the trailing silence, re-record the line with a slower delivery — do not shorten the chapter.

### Prompts are verbatim

Each `ch*_prompt.txt` is already embedded in its JSON. Do **not** summarise or shorten a Motion
prompt; if one seems too long, split the chapter in `script.md` instead.

## Assembly

`assemble.sh` does per-chapter audio, concat, and burns in the 究極奥義 title. Dialogue chapters
(8, 9) discard H3's embedded audio and use the local wav alone; narration chapters mix the
narration over the generated ambient bed.

**Set `OFFSETS_MS` first.** They are all `0` placeholders. Watch each chapter and find the frame
where the speaker's mouth starts moving (dialogue) or the beat the line describes (narration).

```
./assemble.sh     # -> ch*_final.mp4 -> final_draft.mp4 -> final.mp4
```

The 究極奥義 / 何もしてないのに壊れた title is burned in with ffmpeg `drawtext`, never rendered by
H3 or drawn into a keyframe — generated text comes out garbled.

Watch `final.mp4` end to end and confirm cuts, sync, no doubled dialogue, ~86.6s total.

## Credits

No VOICEVOX voice is used in this run (every voice is Irodori-TTS), so the mandatory on-screen
VOICEVOX credit does not apply. If a VOICEVOX character is ever added, burn in
`VOICEVOX:<話者名>` with the `drawtext` recipe in `script.md` before publishing.

Irodori-TTS reference audio is the real voice of actual members — keep use within the scope they
consented to.

## Known caveats — read before debugging

1. **No chapter has ever rendered**, because H3 could not run on the Mac — so treat the first run
   as a bring-up. What HAS been verified, however, is more than structure alone:
   - every node type exists in ComfyUI v0.30.0 and every link resolves
   - R2V stays within 9 images / 3 audio / 12 files; frame counts are on the 17k+5 grid
   - Motion prompts are embedded whole (1,749-3,537 chars, no truncation)
   - an equivalent R2V graph (5 images + 1 audio) was **accepted by ComfyUI's own validator**
     with `node_errors: {}` (see caveat 2)
   - the encoder, both transformers and both VAEs all load successfully (they loaded on the Mac;
     the failures were dtype/operator/allocation, never the graph)

2. **The R2V reference-slot naming IS verified** — this was previously flagged as the likeliest
   bring-up problem, and it has since been tested and cleared. A graph with 5 images + 1 audio,
   addressing the `COMFY_AUTOGROW_V3` slots as `ref_images.ref_image_0..4` and
   `ref_audios.ref_audio_0`, was submitted to a live ComfyUI v0.30.0 `POST /prompt` and came back
   **accepted with `node_errors: {}`**. ComfyUI validates inputs synchronously before executing
   anything, so acceptance confirms the slot names, types and file references are all valid. The
   earlier MPS smoke tests likewise got a 1-image R2V graph past validation and into sampling.

   What remains unverified is therefore only **runtime** behaviour, which no amount of validation
   can establish: whether the output actually lip-syncs to the right character, how closely R2V
   honours the start/end keyframes, and whether prop states survive generation. That is exactly
   what the pilot checklist above is for.

3. The keyframes are 1024x576 and H3 upscales to 1344x768. Regenerating them larger would cost
   ~1.75x more time per frame (~17 min each on the Mac that made them).

4. **Yametaro's seat is a black office chair**, not the Aaronchure cardboard-box stack — the image
   model insisted across attempts. The Motion prompts were reworded to match the keyframes so H3
   is never asked to morph the seat. See "Known deviation" in `script.md`.

5. Chapter 5's start frame is a deliberate **hard cut** (two-year time skip), so `ch4_end.png` and
   `ch5_start.png` are intentionally different images. Same for `ch8_start` and `ch9_start`, which
   are new camera setups for the dialogue. Every other boundary shares one file between chapters.
