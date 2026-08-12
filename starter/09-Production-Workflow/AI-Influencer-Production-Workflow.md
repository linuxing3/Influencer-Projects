---
title: "AI Influencer Production Workflow"
subtitle: "From Character to Consistent Instagram Content"
author: "AI Virtual Influencer Starter Kit"
geometry: margin=0.75in
fontsize: 11pt
---

\newpage

# AI Influencer Production Workflow

## From Character to Consistent Instagram Content

This document is the master production system for the starter kit. It connects character setup, content ideas, calendars, image generation, Canva polish, Instagram publishing, and weekly review into one repeatable loop.

**Primary platform:** Instagram (feed, Reels, Stories)  
**Secondary:** X and TikTok / YouTube Shorts (repurpose only after the Instagram loop works)

**What you will run:**

- A one-time setup phase
- A weekly batch production phase
- A light daily publish + engage phase
- A weekly / monthly performance review

Treat your AI influencer like a media brand. Consistency beats volume.

\newpage

# 1 — Workflow Map

```text
Character Bible
      ↓
Visual Identity + Base Prompt
      ↓
(Optional) Reference pack / LoRA via prepare_pack.py
      ↓
Content Pillars
      ↓
Idea Bank  (03-Content-Ideas)
      ↓
Calendar   (04-Calendar — 7-day / 30-day / weekly)
      ↓
Batch image generation  (02-Prompts)
      ↓
Quality gate  (face · hands · lighting · outfit · voice)
      ↓
Canva polish  (05-Canva)
      ↓
Captions + hashtags  (02-Prompts bonuses)
      ↓
Instagram publish
      ↓
Engagement window
      ↓
Weekly performance review → next calendar
```

## Folder roles

| Folder | Role |
|--------|------|
| `01-Workbook` | Concept, niche, character, pillars, monetization worksheets |
| `00-Character` | Visual pack, captions for training / reference consistency |
| `02-Prompts` | Image prompts + caption / hook / X templates |
| `03-Content-Ideas` | Idea bank, formulas, custom idea worksheet |
| `04-Calendar` | Launch plan, 30-day grid, weekly batch planner |
| `05-Canva` | Sizes, design system, layout briefs |
| `09-Ops` | Operator SOPs, publish QA, repurpose matrix |

\newpage

# 2 — Tool Stack (Defaults)

You can swap tools. Keep **one tool per step** so the system stays simple.

| Step | Default tool type | Examples |
|------|-------------------|----------|
| Text / planning | Chat LLM | ChatGPT, Claude, Gemini |
| Image generation | Image AI | Midjourney, Flux, Leonardo, DALL·E, etc. |
| Design / resize | Canva | Free or Pro |
| Primary publish | Instagram app or scheduler | Meta Business Suite, Later, etc. |
| Optional LoRA pack | Local script | `00-Character/character/prepare_pack.py` |

## Base character prompt (reuse every time)

```text
A realistic AI influencer named [Name], [Age] years old, from [Country],
with [hair], [eyes], [skin tone], [style], [personality],
consistent facial identity, Instagram lifestyle photography, natural lighting.
```

Save this in a note titled **Base Prompt**. Paste it into every image generation session.

\newpage

# 3 — Phase A: One-Time Setup (Day 1–2)

Complete these once before you batch content.

## A1. Character bible

Use `01-Workbook` worksheets:

- Influencer concept
- Niche selection
- Character profile
- Visual identity
- Content pillars
- Platform plan (Instagram primary)

**Lock these fields:** name, age range, face description, hair, eyes, skin, style, personality, brand colors (3–5), niche, caption voice.

## A2. Visual references

1. Generate 10–20 test images with the base prompt.
2. Keep the best 3–5 as **face references**.
3. Optionally prepare a training pack with `00-Character/character/prepare_pack.py` (see `09-Ops/prepare-pack-usage.md`).

## A3. Account skeleton (Instagram)

- [ ] Username available and on-brand
- [ ] Profile photo (clear face, consistent look)
- [ ] Bio with niche + personality in one line
- [ ] Link (Linktree, Beacons, site, or first offer)
- [ ] Highlights plan (About, Looks, Tips, Travel, etc.)

## A4. Content system

- [ ] 3–5 content pillars chosen
- [ ] 20–30 ideas pulled from `03-Content-Ideas` or written on the Idea Bank worksheet
- [ ] 7-day launch calendar filled (`04-Calendar`)
- [ ] Canva brand kit started (`05-Canva`)

\newpage

# 4 — Phase B: Weekly Batch (2–4 hours)

Do this once per week. Do **not** create posts one-by-one every day if you can batch.

## B1. Plan (30–45 min)

1. Open `04-Calendar/Weekly-Batch-Planner.md`.
2. Pick 7–12 ideas from the idea bank (mix pillars).
3. Mark formats: feed photo · carousel · Reel · Story.
4. Apply **80% lifestyle / 20% soft promo**.

## B2. Generate images (45–90 min)

1. Use prompts from `02-Prompts/100-AI-Influencer-Prompts.md`.
2. Always prepend the base character prompt.
3. Generate in batches of 3–5 scenes.
4. Save winners only. Delete weak outputs immediately.

## B3. Quality gate (15–20 min)

Before Canva or posting, check:

- [ ] Face matches references
- [ ] Hair / eyes / skin consistent
- [ ] Hands acceptable (or cropped)
- [ ] Lighting matches brand
- [ ] Outfit fits niche
- [ ] Background makes sense
- [ ] No random text, logos, or extra limbs
- [ ] Image sharp enough for mobile

Full checklist: `09-Ops/quality-gate.md`.

## B4. Canva polish (30–45 min)

1. Resize to Instagram specs (`05-Canva/Instagram-Size-Specs.md`).
2. Add overlays only when needed (quotes, tips, carousel numbers).
3. Keep safe margins; do not cover the face with text.
4. Export PNG or high-quality JPG.

## B5. Captions (20–30 min)

1. Match character voice (warm, bold, educational, etc.).
2. Use `02-Prompts/Bonus-30-Instagram-Captions.md` as starters.
3. One idea per caption. Soft CTA when promo.
4. Prepare 5–15 hashtags (niche + mid-size, not only mega tags).

## B6. Stage for publish

- Folder structure suggestion: `week-YYYY-MM-DD / 01-raw · 02-approved · 03-canva · 04-ready`
- Name files: `YYYY-MM-DD_pillar_format.ext`

\newpage

# 5 — Phase C: Daily Publish + Engage (15–25 min)

## Publish (Instagram first)

1. Post from the ready folder.
2. Use `09-Ops/instagram-publish-checklist.md`.
3. Alternate feed and Reels so the grid does not look random.
4. Cross-post a Story: still + sticker or poll.

## Engagement window (10–15 min after post)

- Reply to early comments
- Like / reply to relevant niche accounts
- Save questions as future content ideas

## Secondary channels (optional same day)

Only after Instagram is consistent:

- X: shorter text take or hook (`Bonus-50-Viral-X-Post-Templates`)
- TikTok / Shorts: repurpose Reels with a new hook (`Bonus-30-YouTube-Hooks`)

See `09-Ops/repurpose-matrix.md`.

\newpage

# 6 — Phase D: Review Loop

## Weekly (Sunday or Monday)

Use `09-Ops/performance-review.md`:

- Top 3 posts (reach, saves, follows, comments)
- Best pillar this week
- Worst format to pause or improve
- 3 ideas for next week from comments / DMs

## Monthly

- Refresh 10 ideas into the idea bank
- Update bio or highlights if niche sharpened
- Test one monetization move (affiliate, digital product, brand pitch list)

\newpage

# 7 — Content Rules

## 80 / 20 mix

| Type | Share | Purpose |
|------|-------|---------|
| Lifestyle / value | ~80% | Trust, recognition, saves |
| Soft promo | ~20% | Offers, affiliates, products, collabs |

## Content pillars (pick 3–5)

Examples (customize):

1. Daily life / aesthetic
2. Niche moments (travel, fashion, fitness, AI…)
3. Tips and recommendations
4. Behind the scenes / process
5. Soft product or affiliate

## Consistency (non-negotiable)

Keep stable:

- Face shape and features
- Hair color and usual style
- Eye color and skin tone
- Age range
- Overall fashion vibe
- Caption voice
- Niche promise

Change freely:

- Locations
- Outfits within style
- Props and activities
- Formats (photo vs Reel)

\newpage

# 8 — Instagram-First Rules

## Formats

| Format | Best for |
|--------|----------|
| Feed 4:5 photo | Grid identity, lifestyle |
| Carousel | Tips, outfit details, story beats |
| Reel 9:16 | Discovery, trends, hooks |
| Story 9:16 | Daily presence, polls, links |

## Cadence (beginner defaults)

See full guide: `04-Calendar/Instagram-Posting-Cadence.md`.

- **Launch week:** 1 post/day (mix feed + Reel)
- **Steady state:** 4–7 feed/Reels per week + Stories most days
- Prefer consistency over daily burnout

## Grid rhythm

Alternate light/dark or calm/busy so the profile looks intentional. Avoid three hard-promo posts in a row.

\newpage

# 9 — Monetization Insertion Points

Do not wait for 100k followers. Insert soft monetization after 2–4 weeks of consistent posting.

| Slot | Calendar use |
|------|----------------|
| Soft mention | 1 post per week (product in scene, no hard sell) |
| Direct promo | 1 post every 1–2 weeks |
| Story swipe / link | After value posts |
| Affiliate in bio | Always available, rarely shouted |

Workbook Page 10 and the monetization worksheet define offers. The calendar marks promo days with a **P** flag.

\newpage

# 10 — 60-Minute First Run

Use this if you want progress today.

| Minutes | Action |
|---------|--------|
| 0–10 | Fill name, niche, 3 pillars (workbook concept page) |
| 10–20 | Write base character prompt |
| 20–35 | Generate 5 images; keep best 2 |
| 35–45 | Pick 3 ideas from `03-Content-Ideas` |
| 45–55 | Write 3 captions; resize 1 image in Canva |
| 55–60 | Draft bio + username list |

Tomorrow: finish the 7-day launch calendar and post the first image.

\newpage

# 11 — Quality Gate (Quick Card)

Print or pin this.

**Visual**

- [ ] Same face as references
- [ ] Hands OK or cropped
- [ ] Lighting on-brand
- [ ] Outfit + niche fit
- [ ] No glitches / weird text

**Copy**

- [ ] Sounds like the character
- [ ] One clear idea
- [ ] CTA matches post type (none / soft / promo)
- [ ] Hashtags relevant

**Platform**

- [ ] Correct aspect ratio
- [ ] Alt text written
- [ ] First comment ready (optional)
- [ ] Story cross-post planned

Full version: `09-Ops/quality-gate.md`.

\newpage

# 12 — Common Failure Modes

| Problem | Fix |
|---------|-----|
| Face changes every post | Lock base prompt; use references; fewer style changes |
| Account feels random | Fewer pillars; stick to calendar |
| Burnout | Weekly batch; fewer daily decisions |
| No growth | More Reels; stronger hooks; niche clarity |
| No income | Add 20% soft promo; clear offer in bio |
| Over-designed Canva | Less text; let the photo lead |

\newpage

# 13 — Start Checklist

- [ ] Read this workflow once
- [ ] Complete workbook character + niche pages
- [ ] Save base prompt
- [ ] Build 20+ ideas (`03-Content-Ideas`)
- [ ] Fill 7-day calendar (`04-Calendar`)
- [ ] Generate first image batch
- [ ] Pass quality gate
- [ ] Polish in Canva (`05-Canva`)
- [ ] Publish first 3 Instagram posts
- [ ] Schedule weekly batch time
- [ ] Run first performance review after 7 days

**Launch goal:** publish before you feel ready. Improve with real feedback.

---

## Next documents

| Need | Open |
|------|------|
| Ideas | `03-Content-Ideas/` |
| Schedule | `04-Calendar/` |
| Design | `05-Canva/` |
| Operator weekly run | `09-Ops/PRODUCTION-SOP.md` |
| Prompts & captions | `02-Prompts/` |
| Concept worksheets | `01-Workbook/` |
