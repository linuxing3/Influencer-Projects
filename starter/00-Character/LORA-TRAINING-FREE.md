# Luna Rio LoRA Training — Free / Low-Cost Guide

Your training pack is ready:

| Item | Path |
|------|------|
| Images + captions | `00-Character/LunaRio_V1/` (30× `.jpg` + `.txt`) |
| Zip | `00-Character/LunaRio_V1.zip` |
| Trigger word | **`lunario`** |
| Profile | `00-Character/character/lunario.json` |
| fal-style config | `00-Character/LunaRio_V1/config.json` |

**Instance prompt / trigger:** `lunario`  
**Character type:** face + body identity (not style-only)  
**Default steps / rank (profile):** 2000 steps, rank 16

---

## Free options ranked (practical)

| Rank | Service | Cost | GPU | Best for | Catch |
|------|---------|------|-----|----------|-------|
| 1 | **Google Colab Free** | $0 | T4 ~15 GB | Full control, Flux LoRA | Session limits, queue, may need Pro for long runs |
| 2 | **Kaggle Notebooks** | $0 (~30 h GPU/week) | P100/T4 | Longer free runs than Colab Free | Weekly quota, less Flux-tutorial polish |
| 3 | **Tensor.Art / SeaArt** (web trainers) | Free daily credits | Hosted | Zero setup | Watermarks / credit caps; quality varies |
| 4 | **fal.ai** (matches your `config.json`) | ~$2/run (not free) | Hosted | Fastest path; already in your config | Need free promo credits or pay a few dollars |
| 5 | Local (if you have 12 GB+ VRAM) | $0 | Your GPU | Unlimited | Needs setup (Kohya / AI-Toolkit) |

> **Reality check:** True zero-dollar Flux LoRA training is almost always **Colab Free** or **Kaggle**. Hosted “one click” trainers (fal, Civitai trainers, etc.) are cheap but rarely free forever. Start with Colab; use fal only if you have credits or can spend ~$2.

---

## Path A — Google Colab Free (recommended free)

### A1. Prep on your machine (already done)

Confirm:

```bash
# from repo root
ls 00-Character/LunaRio_V1/*.jpg | wc -l   # 30
ls 00-Character/LunaRio_V1/*.txt | wc -l   # 30
ls 00-Character/LunaRio_V1.zip
```

Upload **`LunaRio_V1.zip`** to Google Drive (e.g. `MyDrive/lora/LunaRio_V1.zip`).

### A2. Open a Flux LoRA Colab

Good public options (search Google for latest forks if links move):

1. **Ostris AI-Toolkit** Flux training Colab (popular 2025–2026)
2. **Kohya_ss / sd-scripts** Flux LoRA Colab forks
3. Community notebooks: search *“Flux LoRA train Colab free 2026”*

In Colab:

1. Runtime → Change runtime type → **T4 GPU**
2. Mount Google Drive
3. Unzip dataset:

```python
!mkdir -p /content/dataset
!unzip -o /content/drive/MyDrive/lora/LunaRio_V1.zip -d /content/dataset
# expect: /content/dataset/LunaRio_V1/luna_rio_001.jpg + .txt ...
```

### A3. Training settings (character LoRA)

Use these as a starting point for **30 images / face consistency**:

| Setting | Value | Notes |
|---------|-------|-------|
| Base model | FLUX.1-dev (or notebook default Flux) | Match your later inference stack |
| Trigger | `lunario` | Always in captions (already is) |
| Steps | **800–1500** on free T4 | 2000 may disconnect; try 1000 first |
| Rank (dim) | **16** | Matches your profile |
| Learning rate | **1e-4** to **5e-4** | Profile has 5e-4; start lower if overfit |
| Resolution | 512 or 768 | Free T4: 512 safer |
| Batch size | 1 | Free GPU |
| Repeats | 10–20 | If notebook uses folder repeats |
| Caption mode | Use your `.txt` files | Do **not** auto-recaption away the trigger |

**Important for free GPU:** Prefer **1000 steps** first. If Colab disconnects, you still get a usable LoRA. Retrain longer only if face is weak.

### A4. Download the LoRA

After training finishes, download:

- `lunario.safetensors` (or whatever the notebook names it)

Keep a copy next to the pack:

```text
00-Character/LunaRio_V1/lunario.safetensors   # after you train
```

### A5. Test prompt

```text
lunario, Luna Rio, asian-brazilian virtual influencer, fair skin, long black wavy hair with bangs, dark brown eyes, wearing Argentina fan t-shirt and shorts, sitting on sofa watching tablet, realistic photography
```

Compare face to `lunario_assets.jpg` and pack references.

---

## Path B — Kaggle free GPU

1. Create free Kaggle account → enable phone verification for GPU.
2. New Notebook → Accelerator: **GPU T4 x2** or **P100**.
3. Add `LunaRio_V1.zip` as a Dataset (Upload) or pull from Drive/URL.
4. Install the same AI-Toolkit / Kohya train script used in Colab tutorials.
5. Use the same hyperparameters as Path A.
6. Save output as a Kaggle Dataset or download the `.safetensors`.

**Quota tip:** Kaggle weekly GPU hours often beat Colab Free for one full 1000–2000 step run.

---

## Path C — fal.ai (recommended hosted; ~$2)

Ready-made script in this repo:

| File | Role |
|------|------|
| `00-Character/train_fal_lora.py` | Upload zip → train → download LoRA |
| `00-Character/LunaRio_V1.zip` | Dataset |
| `00-Character/.venv/` | Local Python env with `fal-client` |

### C1. Get an API key

1. Sign up / log in: https://fal.ai  
2. Create a key: https://fal.ai/dashboard/keys  
3. Check balance / free credits on the dashboard  

### C2. Run training (one command)

From repo root:

```bash
export FAL_KEY="fal_xxxxxxxx"   # paste your key (do not commit it)

cd 00-Character
source .venv/bin/activate      # or: .venv/bin/python ...

python train_fal_lora.py
# first run defaults to 1000 steps (cheaper)

# optional:
python train_fal_lora.py --steps 1500
python train_fal_lora.py --steps 2000
```

What the script does:

1. Uploads `LunaRio_V1.zip` to fal storage  
2. Calls `fal-ai/flux-lora-fast-training` with trigger **`lunario`**, masks on, captions from `.txt`  
3. Saves:
   - `LunaRio_V1/lunario.safetensors`
   - `LunaRio_V1/fal_train_result.json`
   - updates `LunaRio_V1/config.json` with the job URL/result  

### C3. UI alternative (no script)

1. Open https://fal.ai/models/fal-ai/flux-lora-fast-training  
2. Upload the zip (or a public URL)  
3. Trigger word: `lunario`  
4. Steps: `1000`  
5. Create masks: on  
6. Train → download weights  

Portrait-focused alternative endpoint: `fal-ai/flux-lora-portrait-trainer`  
(`python train_fal_lora.py --endpoint fal-ai/flux-lora-portrait-trainer`)

**Approx cost:** often ~$2 per fast training run (confirm on fal pricing page).

---

## Path D — Web trainers with free credits (easiest UI)

If you want zero code:

1. **Tensor.Art** — train LoRA with free daily credits (check Flux availability).
2. **SeaArt** — similar free-credit trainers.
3. **Civitai** — on-site trainers / partners when available.

Steps common to all:

1. Upload 15–30 of your `luna_rio_*.jpg` (and captions if supported).
2. Set trigger: `lunario`
3. Train as **character / person** not style.
4. Download `.safetensors` when done.

Quality and commercial license differ by site — read each ToS.

---

## Dataset tips (you already did most of this)

Your pack is strong for free training:

- ✅ 30 images with pose variety  
- ✅ Matching `.txt` captions with trigger first  
- ✅ Same face / outfit identity  
- ✅ Clean studio + a few lifestyle shots  

Optional improvements before a second train:

1. Drop any image where face drifts.  
2. Cap lifestyle shots at ~20% of the set (studio identity first).  
3. Keep trigger **`lunario`** at the start of every caption.  
4. Avoid recaptioning that removes `lunario`.

---

## After training — use the LoRA

| Place | How |
|-------|-----|
| fal image gen | Attach LoRA URL + prompt starting with `lunario` |
| ComfyUI | Load FLUX + LoRA loader → strength 0.7–1.0 |
| Forge / WebUI Flux forks | Add LoRA, weight ~0.8 |
| This kit’s content flow | Generate stills → quality gate → Canva → Instagram |

**Strength guide:** start **0.8**. Too high = overfit (same pose/outfit only). Too low = face drifts.

---

## Suggested order for you (Luna Rio)

1. **Today (free):** Upload `LunaRio_V1.zip` to Drive → Colab Free → train **1000 steps**, rank **16**, trigger **`lunario`**.  
2. **Test:** 5 prompts (studio portrait, Argentina fan outfit, beach, coffee shop, selfie).  
3. **If face weak:** retrain 1500–2000 steps on Kaggle (more GPU hours).  
4. **If you get fal credits / $2:** use Path C with existing `config.json` for speed.

---

## Checklist

- [ ] `LunaRio_V1.zip` uploaded to Drive / trainer  
- [ ] Trigger word set to `lunario`  
- [ ] Captions enabled (your `.txt` files)  
- [ ] Character mode (not style-only)  
- [ ] Steps 1000 first on free GPU  
- [ ] Download `.safetensors`  
- [ ] Test 5 prompts; adjust strength  
- [ ] Archive LoRA next to pack for the production workflow  

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Colab disconnect mid-train | Lower steps to 800–1000; save checkpoints if notebook supports it |
| Face not consistent | More studio angles; raise steps; check trigger in every caption |
| Only wears Brazil outfit | Captions overfit outfit — add more varied outfit captions next train or lower LoRA strength + prompt hard for new clothes |
| OOM on T4 | Resolution 512, batch 1, rank 8–16 |
| Blurry results | Inference model mismatch; use same Flux base you trained against |

---

## Related files in this repo

- `00-Character/character/prepare_pack.py` — rebuild zip/captions from a profile  
- `00-Character/character/lunario.json` — source of truth for captions + train hyperparams  
- `09-Ops/prepare-pack-usage.md` — how to prepare packs  
- `09-Ops/PRODUCTION-SOP.md` — weekly content after LoRA works  

You do **not** need to re-generate images to start training. Use `LunaRio_V1.zip` as-is.
