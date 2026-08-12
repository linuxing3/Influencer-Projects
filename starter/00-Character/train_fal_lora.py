#!/usr/bin/env python3
"""Train Luna Rio Flux LoRA on fal.ai (flux-lora-fast-training).

Requires:
  export FAL_KEY="your_key"   # from https://fal.ai/dashboard/keys

Usage (from repo root):
  python3 00-Character/train_fal_lora.py
  python3 00-Character/train_fal_lora.py --steps 1000
  python3 00-Character/train_fal_lora.py --zip 00-Character/LunaRio_V1.zip --out 00-Character/LunaRio_V1

What it does:
  1. Uploads the training zip to fal storage (public URL for the job)
  2. Submits fal-ai/flux-lora-fast-training
  3. Downloads the .safetensors LoRA + config next to the pack
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEFAULT_ZIP = ROOT / "LunaRio_V1.zip"
DEFAULT_OUT = ROOT / "LunaRio_V1"
DEFAULT_PROFILE = ROOT / "character" / "lunario.json"
ENDPOINT = "fal-ai/flux-lora-fast-training"


def require_fal():
    try:
        import fal_client  # noqa: F401
    except ImportError:
        print(
            "fal_client not installed. Run:\n  uv pip install --system fal-client\n  # or: pip install fal-client",
            file=sys.stderr,
        )
        sys.exit(1)
    if not os.environ.get("FAL_KEY"):
        print(
            "FAL_KEY is not set.\n\n"
            "1. Sign up / log in: https://fal.ai\n"
            "2. Create a key:     https://fal.ai/dashboard/keys\n"
            "3. Export it:\n"
            '     export FAL_KEY="fal_..."\n'
            "4. Re-run this script.\n\n"
            "Pricing is usually ~$2 per fast training run (check fal dashboard).",
            file=sys.stderr,
        )
        sys.exit(1)
    import fal_client

    return fal_client


def load_train_defaults(profile_path: Path) -> dict:
    if not profile_path.exists():
        return {}
    data = json.loads(profile_path.read_text(encoding="utf-8"))
    train = dict(data.get("lora_train") or {})
    return {
        "trigger_word": data.get("trigger_word", "lunario"),
        "instance_prompt": train.get("instance_prompt", data.get("trigger_word", "lunario")),
        "learning_rate": train.get("learning_rate", 0.0005),
        "create_masks": train.get("create_masks", True),
        "steps": train.get("steps", 1000),
        "is_style": train.get("is_style", False),
        "rank": train.get("rank", 16),
    }


def download(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"downloading -> {dest}")
    urllib.request.urlretrieve(url, dest)
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--zip", type=Path, default=DEFAULT_ZIP, help="training zip path")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output directory for LoRA")
    ap.add_argument("--profile", type=Path, default=DEFAULT_PROFILE)
    ap.add_argument("--steps", type=int, default=None, help="override steps (default 1000 for first free-ish run)")
    ap.add_argument("--trigger", default=None, help="override trigger word")
    ap.add_argument(
        "--create-masks",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="face/subject masks (default: true)",
    )
    ap.add_argument(
        "--is-style",
        action="store_true",
        help="style LoRA mode (disables segmentation; not for character)",
    )
    ap.add_argument(
        "--endpoint",
        default=ENDPOINT,
        help="fal endpoint id (default flux-lora-fast-training)",
    )
    args = ap.parse_args()

    fal_client = require_fal()

    if not args.zip.is_file():
        print(f"zip not found: {args.zip}", file=sys.stderr)
        sys.exit(1)

    defaults = load_train_defaults(args.profile)
    steps = args.steps if args.steps is not None else min(int(defaults.get("steps", 1000)), 1000)
    trigger = args.trigger or defaults.get("trigger_word", "lunario")

    print(f"uploading {args.zip} ({args.zip.stat().st_size / 1e6:.1f} MB) to fal storage...")
    images_url = fal_client.upload_file(str(args.zip))
    print(f"images_data_url = {images_url}")

    arguments = {
        "images_data_url": images_url,
        "trigger_word": trigger,
        "create_masks": False if args.is_style else bool(args.create_masks),
        "steps": steps,
        "is_style": bool(args.is_style),
        # keep captions from paired .txt files inside the zip
        "is_input_format_already_preprocessed": False,
    }

    # Optional fields some fal builds accept (ignored if unsupported via API validation)
    # Do not send rank/learning_rate unless the schema supports them — fast-training schema is minimal.

    print("submitting training job:")
    print(json.dumps({**arguments, "endpoint": args.endpoint}, indent=2))
    print("(this may take several minutes; logs stream below)\n")

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress) and getattr(update, "logs", None):
            for log in update.logs:
                msg = log.get("message") if isinstance(log, dict) else getattr(log, "message", None)
                if msg:
                    print(msg)

    result = fal_client.subscribe(
        args.endpoint,
        arguments=arguments,
        with_logs=True,
        on_queue_update=on_queue_update,
    )

    # result may be dict-like
    if hasattr(result, "get"):
        data = result
    else:
        data = dict(result)

    print("\n=== result ===")
    print(json.dumps(data, indent=2, default=str))

    args.out.mkdir(parents=True, exist_ok=True)
    meta_path = args.out / "fal_train_result.json"
    meta_path.write_text(json.dumps(data, indent=2, default=str) + "\n", encoding="utf-8")

    lora_info = data.get("diffusers_lora_file") or {}
    cfg_info = data.get("config_file") or {}
    lora_url = lora_info.get("url") if isinstance(lora_info, dict) else None
    cfg_url = cfg_info.get("url") if isinstance(cfg_info, dict) else None

    saved = []
    if lora_url:
        name = lora_info.get("file_name") or "lunario.safetensors"
        if not str(name).endswith(".safetensors"):
            name = "lunario.safetensors"
        dest = args.out / name
        # prefer stable name for the kit
        dest = args.out / "lunario.safetensors"
        download(lora_url, dest)
        saved.append(dest)
    if cfg_url:
        dest = args.out / "fal_train_config.json"
        download(cfg_url, dest)
        saved.append(dest)

    # update local fal-style config with the used URL
    local_cfg = {
        "images_data_url": images_url,
        "trigger_word": trigger,
        "create_masks": arguments["create_masks"],
        "steps": steps,
        "is_style": arguments["is_style"],
        "is_input_format_already_preprocessed": False,
        "endpoint": args.endpoint,
        "result": data,
    }
    (args.out / "config.json").write_text(json.dumps(local_cfg, indent=2, default=str) + "\n")

    print("\n=== done ===")
    print(f"trigger word: {trigger}")
    print(f"steps:        {steps}")
    for p in saved:
        print(f"saved:        {p}")
    print(f"meta:         {meta_path}")
    print("\nTest prompt:")
    print(
        f"  {trigger}, Luna Rio, asian-brazilian virtual influencer, "
        "long black wavy hair with bangs, dark brown eyes, realistic photography"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
