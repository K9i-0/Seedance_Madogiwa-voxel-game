#!/usr/bin/env python3
"""Build an LTX-2.5 API-format workflow JSON for one chapter (first/last-frame i2v).

Wiring is taken from ComfyUI's official LTX-2.3 FLF2V blueprint and Lightricks'
LTX-2.5 single-stage distilled example workflow, converted to API format and
parameterized. Single-stage distilled only (8 steps, cfg=1, euler_ancestral,
manual sigmas) — the dev model and the two-stage upscaler pipeline are out of
scope for chapter generation.

LTX-2.5 has no wav-driven lip-sync input (H3のR2V相当は無い) — dialogue chapters
stay on MiniMax H3. Use this for I2V (no-dialogue) chapters. Audio is always
generated jointly from the prompt's Soundscape/Music description.

usage:
  build_ltx25_workflow.py --out ch1_workflow.json --prompt-file p.txt \
      --frames 121 --first ch1_start.png --last ch1_end.png [--width 1344 --height 768]
  # --last を省くと開始フレームのみの条件付けになる
"""
from __future__ import annotations

import argparse
import json

# Only one quantized variant exists for LTX-2.5 (comfy-int8-convrot) and it runs on
# both Ada (L4) and Ampere (A100) — no per-GPU weight switching, unlike H3.
TRANSFORMER = "ltx-2.5-22b-distilled-transformer-comfy-int8-convrot.safetensors"
ENCODER = "gemma4-12b-with-proj-ltx-2.5-comfy-int8-convrot.safetensors"
VIDEO_VAE = "ltx-2.5-video-vae-bf16.safetensors"
AUDIO_VAE = "ltx-2.5-audio-vae-bf16.safetensors"

# Distilled 8-step schedule from the official single-stage workflow.
DISTILLED_SIGMAS = "1.0, 0.99375, 0.9875, 0.98125, 0.975, 0.909375, 0.725, 0.421875, 0.0"

NEGATIVE = (
    "blurry, out of focus, overexposed, underexposed, low contrast, washed out colors, "
    "excessive noise, grainy texture, flickering, distorted proportions, deformed facial "
    "features, extra limbs, disfigured hands, jittery movement, awkward pauses, unnatural "
    "transitions, color banding, cartoonish rendering, watermark, text overlay, AI artifacts, "
    "distorted voice, robotic voice, echo, off-sync audio"
)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--frames", type=int, required=True)
    ap.add_argument("--width", type=int, default=1344)
    ap.add_argument("--height", type=int, default=768)
    ap.add_argument("--fps", type=float, default=24.0)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--prefix", default="video/LTX25")
    ap.add_argument("--first", required=True)
    ap.add_argument("--last")
    ap.add_argument("--guide-strength", type=float, default=0.7)
    ap.add_argument("--img-compression", type=int, default=18)
    ap.add_argument("--negative", default=NEGATIVE)
    ap.add_argument("--transformer", default=TRANSFORMER)
    ap.add_argument("--encoder", default=ENCODER)
    a = ap.parse_args()

    if (a.frames - 1) % 8 != 0:
        near = (a.frames - 1) // 8 * 8 + 1
        raise SystemExit(
            f"--frames {a.frames} is not on LTX's 8k+1 grid (e.g. 97, 121, 145, 193) "
            f"— nearest: {near} or {near + 8}. H3の17k+5グリッドとは違うので注意")
    if a.width % 32 or a.height % 32:
        raise SystemExit(f"--width/--height must be multiples of 32 (got {a.width}x{a.height})")

    prompt = open(a.prompt_file, encoding="utf-8").read().strip()

    g: dict[str, dict] = {
        "1": {"class_type": "VAELoader", "inputs": {"vae_name": VIDEO_VAE}},
        "2": {"class_type": "VAELoader", "inputs": {"vae_name": AUDIO_VAE}},
        "3": {"class_type": "UNETLoader", "inputs": {
            "unet_name": a.transformer, "weight_dtype": "default"}},
        "4": {"class_type": "CLIPLoader", "inputs": {
            "clip_name": a.encoder, "type": "ltxv", "device": "default"}},
        "5": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 0], "text": prompt}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 0], "text": a.negative}},
        "7": {"class_type": "LTXVConditioning", "inputs": {
            "positive": ["5", 0], "negative": ["6", 0], "frame_rate": a.fps}},
        "8": {"class_type": "EmptyLTXVLatentVideo", "inputs": {
            "width": a.width, "height": a.height, "length": a.frames, "batch_size": 1}},
        "9": {"class_type": "LoadImage", "inputs": {"image": a.first}},
        "10": {"class_type": "LTXVPreprocess", "inputs": {
            "image": ["9", 0], "img_compression": a.img_compression}},
        # AddGuide scales/crops the image to the latent size internally (bilinear,
        # center crop) — keyframes only need to match the aspect ratio.
        "11": {"class_type": "LTXVAddGuide", "inputs": {
            "positive": ["7", 0], "negative": ["7", 1], "vae": ["1", 0],
            "latent": ["8", 0], "image": ["10", 0],
            "frame_idx": 0, "strength": a.guide_strength}},
    }
    tail = "11"  # last AddGuide in the chain
    if a.last:
        g["12"] = {"class_type": "LoadImage", "inputs": {"image": a.last}}
        g["13"] = {"class_type": "LTXVPreprocess", "inputs": {
            "image": ["12", 0], "img_compression": a.img_compression}}
        g["14"] = {"class_type": "LTXVAddGuide", "inputs": {
            "positive": ["11", 0], "negative": ["11", 1], "vae": ["1", 0],
            "latent": ["11", 2], "image": ["13", 0],
            "frame_idx": -1, "strength": a.guide_strength}}
        tail = "14"

    g.update({
        "15": {"class_type": "LTXVEmptyLatentAudio", "inputs": {
            "frames_number": a.frames, "frame_rate": a.fps, "batch_size": 1,
            "audio_vae": ["2", 0]}},
        "16": {"class_type": "LTXVConcatAVLatent", "inputs": {
            "video_latent": [tail, 2], "audio_latent": ["15", 0]}},
        "17": {"class_type": "CFGGuider", "inputs": {
            "model": ["3", 0], "positive": [tail, 0], "negative": [tail, 1], "cfg": 1.0}},
        "18": {"class_type": "KSamplerSelect", "inputs": {"sampler_name": "euler_ancestral"}},
        "19": {"class_type": "ManualSigmas", "inputs": {"sigmas": DISTILLED_SIGMAS}},
        "20": {"class_type": "RandomNoise", "inputs": {"noise_seed": a.seed}},
        "21": {"class_type": "SamplerCustomAdvanced", "inputs": {
            "noise": ["20", 0], "guider": ["17", 0], "sampler": ["18", 0],
            "sigmas": ["19", 0], "latent_image": ["16", 0]}},
        # Slot 1 = denoised output, per the official blueprint.
        "22": {"class_type": "LTXVSeparateAVLatent", "inputs": {"av_latent": ["21", 1]}},
        # Guide latents are appended to the video latent — crop them before decode.
        "23": {"class_type": "LTXVCropGuides", "inputs": {
            "positive": [tail, 0], "negative": [tail, 1], "latent": ["22", 0]}},
        "24": {"class_type": "VAEDecodeTiled", "inputs": {
            "samples": ["23", 2], "vae": ["1", 0],
            "tile_size": 512, "overlap": 64, "temporal_size": 64, "temporal_overlap": 8}},
        "25": {"class_type": "LTXVAudioVAEDecode", "inputs": {
            "samples": ["22", 1], "audio_vae": ["2", 0]}},
        "26": {"class_type": "CreateVideo", "inputs": {
            "images": ["24", 0], "audio": ["25", 0], "fps": a.fps, "bit_depth": 8}},
        "27": {"class_type": "SaveVideo", "inputs": {
            "video": ["26", 0], "filename_prefix": a.prefix, "format": "auto", "codec": "auto"}},
    })

    with open(a.out, "w", encoding="utf-8") as fh:
        json.dump(g, fh, ensure_ascii=False, indent=2)

    secs = a.frames / a.fps
    print(f"wrote {a.out}: {a.width}x{a.height} {a.frames}f ({secs:.3f}s @{a.fps:g}fps) "
          f"seed={a.seed} distilled 8-step")
    print(f"  first_frame = {a.first}")
    print(f"  last_frame  = {a.last or '(none — first-frame only)'}")


if __name__ == "__main__":
    main()
