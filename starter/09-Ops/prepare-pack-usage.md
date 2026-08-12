# Prepare Pack Usage

How to build a captioned image pack for **visual consistency** and optional **LoRA training**, using the existing script.

**Script:** `00-Character/character/prepare_pack.py`  
**Example profile:** `00-Character/character/lunario.json`  
**Blank profile:** `09-Ops/character-profile.template.json`

---

## What it does

1. Reads a character profile JSON  
2. Collects images from an input folder  
3. Converts them to JPEG with sequential names  
4. Writes one `.txt` caption per image (`base_caption` + pose/action)  
5. Optionally zips the pack  
6. Optionally writes a fal.ai-style LoRA train config  

---

## 1. Create a profile

Copy the template:

```bash
cp 09-Ops/character-profile.template.json 00-Character/character/my_character.json
```

Edit at minimum:

- `id`, `display_name`, `trigger_word`
- `output_dir`, `file_prefix`
- `expected_count` (default 30)
- `base_caption` (fixed look description)
- `action_captions` (one per training image, same length as count)
- `lora_train` (if you will train)

Keep `base_caption` stable. Vary only `action_captions`.

---

## 2. Gather source images

Put raw generations in a folder (example: `00-Character/input_images/`):

- Prefer the same face, lighting family, and outfit identity
- Mix poses (front, 3/4, profile, actions)
- Aim for `expected_count` images (e.g. 30)

Supported extensions: `.jpg`, `.jpeg`, `.png`, `.webp`

---

## 3. Run the script

From repo root (adjust paths if needed):

```bash
python3 00-Character/character/prepare_pack.py \
  --profile 00-Character/character/my_character.json \
  --input 00-Character/input_images \
  --output 00-Character/MyCharacter_V1 \
  --zip \
  --fal-config 00-Character/MyCharacter_V1/config.json
```

Useful flags:

| Flag | Meaning |
|------|---------|
| `--profile` | Character JSON (required) |
| `--input` | Folder of source images |
| `--output` | Override `output_dir` |
| `--zip` | Also write `output.zip` |
| `--fal-config` | Path for train config JSON (`""` path behavior: pass a real path or edit script default) |
| `--images-data-url` | Remote zip URL embedded in fal config |

Dependency: **Pillow** (`PIL`).

```bash
pip install pillow
```

---

## 4. Outputs

```text
MyCharacter_V1/
  character_name_001.jpg
  character_name_001.txt
  ...
MyCharacter_V1.zip   # if --zip
config.json          # if --fal-config set
```

Each `.txt` looks like:

```text
[base_caption], [action_captions[i]]
```

---

## 5. How this fits production

| Use | When |
|-----|------|
| Reference pack | Weekly: keep best stills as face anchors for img2img / manual QA |
| LoRA train | When one-shot prompts cannot hold identity |
| Buyer product | Optional advanced path — not required for 7-day launch |

Production SOP still applies: generate → quality gate → Canva → Instagram. The pack improves **identity stability**; it does not replace the calendar or captions.

---

## 6. Checklist

- [ ] Profile JSON filled (no leftover bracket placeholders in `base_caption`)
- [ ] Image count ≈ `expected_count`
- [ ] Actions list length ≥ image count used
- [ ] Script completed without empty input error
- [ ] Spot-check 3 caption `.txt` files
- [ ] Store pack outside public buyer zip if it is private IP

---

## 7. Privacy / product note

Character training packs and face references may be **operator assets**. Do not ship private LoRA datasets inside the public Etsy buyer download unless that is an intentional product upgrade.
