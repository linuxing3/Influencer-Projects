# Operator Production SOP

Weekly runbook for operating an AI influencer. Human-in-the-loop: **do not auto-publish** without review.

**Primary channel:** Instagram  
**Secondary:** X, TikTok / Shorts via repurpose matrix  
**Buyer-facing twin:** `09-Production-Workflow/AI-Influencer-Production-Workflow.md`

---

## Cadence Overview

| When | Block | Duration |
|------|-------|----------|
| Monday (or fixed batch day) | Plan + generate + Canva + captions | 2–4 hours |
| Assigned publish days | Post + engage | 15–25 min each |
| Sunday / Monday | Performance review | 20–30 min |
| Monthly | Idea bank refresh + offer test | 1 hour |

---

## Monday — Weekly Batch

### 1. Load context (10 min)

- [ ] Open character base prompt
- [ ] Open `04-Calendar/Weekly-Batch-Planner.md` (new copy for this week)
- [ ] Skim last week’s performance notes
- [ ] Confirm pillars and promo limit (≤ 20%)

### 2. Select ideas (20–30 min)

- [ ] Pick 5–9 ideas from idea bank
- [ ] Assign formats (F / C / R / S)
- [ ] Mark promo rows
- [ ] Assign publish days

### 3. Generate visuals (45–90 min)

- [ ] Paste base prompt every generation
- [ ] Use `02-Prompts` or custom prompts
- [ ] Save winners only under `ops-media/week-YYYY-MM-DD/01-raw`
- [ ] Promote keepers to `02-approved`

### 4. Quality gate (15–20 min)

- [ ] Run `quality-gate.md` on every asset
- [ ] Reject face drift, bad hands, artifacts
- [ ] Crop or regenerate rather than “sticker fix”

### 5. Canva (30–45 min)

- [ ] Apply correct sizes (`05-Canva`)
- [ ] Export to `03-canva` → `04-ready`
- [ ] Match design system checklist

### 6. Captions (20–30 min)

- [ ] Voice locked to character
- [ ] CTA set
- [ ] Hashtags prepared
- [ ] Optional first comment

### 7. Stage

- [ ] One folder per post or clear naming: `YYYY-MM-DD_pillar_fmt.ext`
- [ ] Caption text file or sheet row paired
- [ ] Schedule times written on weekly planner

**Stop condition:** nothing goes live Monday unless it was already planned. Prefer staging over rushing.

---

## Publish Days

For each post:

1. Open `instagram-publish-checklist.md`
2. Upload from `04-ready` only
3. Engage 10–15 minutes after post
4. Story cross-post (optional but recommended)
5. Log post URL / ID in performance sheet

If something fails QA at the last minute: **skip and replace later**. Do not ship broken face consistency.

---

## Sunday / Monday — Review

1. Complete `performance-review.md`
2. Tag top 3 and bottom 2 posts
3. Add 3–5 ideas from comments/DMs to idea bank
4. Book next batch block
5. Adjust cadence if burnout or under-posting

---

## Monthly Operator Tasks

- [ ] Refresh 10 ideas
- [ ] Audit 80/20 promo ratio
- [ ] Update bio if positioning sharpened
- [ ] One monetization experiment (affiliate, product, pitch)
- [ ] Optional: rebuild reference pack via `prepare-pack-usage.md`

---

## Folder Convention (recommended)

```text
ops-media/
  week-2026-07-07/
    01-raw/
    02-approved/
    03-canva/
    04-ready/
    captions.md
    notes.md
```

---

## Escalation / Failure Modes

| Symptom | Action |
|---------|--------|
| Face inconsistency | Tighten base prompt; use refs; fewer outfit extremes |
| Missed publish days | Lower target count; protect batch block |
| Zero engagement | More Reels; clearer niche in first 3 grid posts |
| Promo fatigue | Cut promo for 2 weeks; value-only |

---

## Related Docs

| Doc | Use |
|-----|-----|
| `quality-gate.md` | Pre-publish QA |
| `instagram-publish-checklist.md` | Go-live steps |
| `repurpose-matrix.md` | Secondary channels |
| `performance-review.md` | Weekly metrics |
| `prepare-pack-usage.md` | LoRA / reference pack |
| `character-profile.template.json` | New character schema |
