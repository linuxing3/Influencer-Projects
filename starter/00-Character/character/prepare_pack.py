#!/usr/bin/env python3
"""Prepare a captioned image pack for virtual-influencer LoRA training.

Reads a character profile JSON, renames/converts images to JPEG, and writes
one caption .txt per image (trigger word + base look + action pose).

Usage:
  python character/prepare_pack.py --profile character/lunario.json
  python character/prepare_pack.py --profile character/lunario.json \\
      --input input_images --output LunaRio_V1 --zip
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import zipfile

from PIL import Image

VALID_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def load_profile(path: str) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def collect_images(input_dir: str) -> list[str]:
    files = [
        f
        for f in os.listdir(input_dir)
        if os.path.splitext(f.lower())[1] in VALID_EXTS
    ]
    files.sort()
    return files


def prepare(profile: dict, input_dir: str, output_dir: str, make_zip: bool) -> str:
    prefix = profile.get("file_prefix", profile["id"])
    expected = int(profile.get("expected_count", 30))
    base = profile["base_caption"].rstrip(", ")
    actions = profile.get("action_captions") or [""]

    os.makedirs(output_dir, exist_ok=True)
    images = collect_images(input_dir)
    n = len(images)
    if n == 0:
        sys.exit(f"no images in {input_dir}")
    if n != expected:
        print(f"warning: found {n} images, expected {expected}")

    written = []
    for i, filename in enumerate(images[:expected], start=1):
        src = os.path.join(input_dir, filename)
        jpg_name = f"{prefix}_{i:03d}.jpg"
        txt_name = f"{prefix}_{i:03d}.txt"
        img = Image.open(src).convert("RGB")
        jpg_path = os.path.join(output_dir, jpg_name)
        img.save(jpg_path, quality=95)

        action = actions[i - 1] if i <= len(actions) else ""
        caption = f"{base}, {action}" if action else base
        txt_path = os.path.join(output_dir, txt_name)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(caption)
        written.append((jpg_path, txt_path))

    print(f"prepared {len(written)} image+caption pairs in {output_dir}/")

    zip_path = None
    if make_zip:
        zip_path = output_dir.rstrip(os.sep) + ".zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(output_dir):
                for name in files:
                    full = os.path.join(root, name)
                    zf.write(full, arcname=os.path.relpath(full, os.path.dirname(output_dir)))
        print(f"zipped -> {zip_path}")
    return zip_path or output_dir


def write_fal_config(profile: dict, images_data_url: str | None, out_path: str):
    """Write fal.ai-style Flux LoRA train config from profile."""
    train = dict(profile.get("lora_train") or {})
    cfg = {
        "images_data_url": images_data_url,
        "trigger_word": profile["trigger_word"],
        "disable_captions": False,
        "disable_segmentation_and_captioning": False,
        "learning_rate": train.get("learning_rate", 0.0005),
        "b_up_factor": train.get("b_up_factor", 3.0),
        "create_masks": train.get("create_masks", True),
        "iter_multiplier": train.get("iter_multiplier", 1.0),
        "steps": train.get("steps", 2000),
        "is_style": train.get("is_style", False),
        "is_input_format_already_preprocessed": False,
        "data_archive_format": None,
        "resume_with_lora": None,
        "rank": train.get("rank", 16),
        "debug_preprocessed_images": False,
        "instance_prompt": train.get("instance_prompt", profile["trigger_word"]),
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cfg, f, ensure_ascii=False, indent=2)
    print(f"wrote LoRA train config -> {out_path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--profile", required=True, help="character profile JSON")
    ap.add_argument("--input", default="input_images")
    ap.add_argument("--output", help="override profile output_dir")
    ap.add_argument("--zip", action="store_true", help="also write <output>.zip")
    ap.add_argument(
        "--fal-config",
        default="config.json",
        help="write fal train config here (empty to skip)",
    )
    ap.add_argument(
        "--images-data-url",
        default=None,
        help="remote zip URL for fal train config",
    )
    args = ap.parse_args()

    profile = load_profile(args.profile)
    out = args.output or profile.get("output_dir") or profile["id"]
    prepare(profile, args.input, out, args.zip)
    if args.fal_config:
        write_fal_config(profile, args.images_data_url, args.fal_config)


if __name__ == "__main__":
    main()
