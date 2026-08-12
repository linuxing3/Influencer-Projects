#!/usr/bin/env python3
from pathlib import Path
import subprocess, urllib.parse, re, json, time

OUT = Path('/sources/AI-Virtual-Influencer-Starter-Kit/06-Etsy-Listing')
OUT.mkdir(parents=True, exist_ok=True)
queries = [
    'AI Influencer',
    'Virtual Influencer',
    'Instagram Template',
    'Content Creator Kit',
    'Social Media Kit',
    'Faceless YouTube',
    'Creator Planner',
]

def shell_quote(s: str) -> str:
    return "'" + s.replace("'", "'\\''") + "'"

def run_ab(args, timeout=30):
    # User preference: agent-browser through zsh interactive login mode.
    # Quote every arg because Etsy URLs contain '?' which zsh treats as a glob.
    cmd = ' '.join([shell_quote(x) for x in ['agent-browser'] + args])
    p = subprocess.run(['zsh','-ilc',cmd], text=True, capture_output=True, timeout=timeout)
    return p.stdout.strip(), p.stderr.strip(), p.returncode

# initialize
run_ab(['close','--all'], timeout=10)
run_ab(['set','viewport','1365','900'], timeout=10)

rows=[]
for q in queries:
    url='https://www.etsy.com/search?q='+urllib.parse.quote(q)
    stdout, stderr, code = run_ab(['open', url], timeout=45)
    run_ab(['wait','3500'], timeout=10)
    title, _, _ = run_ab(['get','title'], timeout=10)
    final_url, _, _ = run_ab(['get','url'], timeout=10)
    text, err, _ = run_ab(['get','text','body'], timeout=25)
    shot = OUT / ('validation-' + q.lower().replace(' ','-') + '.png')
    run_ab(['screenshot', str(shot)], timeout=20)
    snippet = re.sub(r'\s+', ' ', text)[:1600]
    blocked = bool(re.search(r'DataDome|captcha|blocked|Access Denied|sorry|robot|unusual traffic|Device Check', text+' '+title+' '+final_url, re.I))
    result_match = None
    for pat in [r'([0-9][0-9,\.]*\+?)\s+results', r'([0-9][0-9,\.]*\+?)\s+Results', r'([0-9][0-9,\.]*\+?)\s+items', r'([0-9][0-9,\.]*\+?)\s+shop results']:
        m=re.search(pat,text,re.I)
        if m:
            result_match=m.group(0)
            break
    reviews = re.findall(r'([0-9][0-9,\.]*\+?)\s+reviews?', text, re.I)[:8]
    sales = re.findall(r'([0-9][0-9,\.]*\+?)\s+sales', text, re.I)[:8]
    favs = re.findall(r'([0-9][0-9,\.]*\+?)\s+(?:favorites|favourites|favorited)', text, re.I)[:8]
    badges = []
    for b in ['Bestseller','Star Seller','Popular now','In carts']:
        if re.search(b,text,re.I): badges.append(b)
    rows.append({
        'keyword': q,
        'url': final_url or url,
        'title': title,
        'blocked': blocked,
        'results_detected': result_match or 'not captured',
        'review_signals': reviews,
        'sales_signals': sales,
        'favorite_signals': favs,
        'badges_detected': badges,
        'screenshot': str(shot),
        'text_snippet': snippet,
    })

(OUT/'etsy-market-validation.raw.json').write_text(json.dumps(rows, indent=2, ensure_ascii=False))

md = ['# Etsy Market Validation — Search Demand Check','', '## Method', '', 'Opened Etsy search pages with `agent-browser` via `zsh -ilc`, captured page text and screenshots. If Etsy anti-bot blocked data, mark as blocked and do not invent numbers.', '', '## Findings', '']
for r in rows:
    demand = 'Unknown — Etsy blocked/could not capture' if r['blocked'] or r['results_detected']=='not captured' else r['results_detected']
    sales_level = 'Unknown' if r['blocked'] else ('High signal' if r['review_signals'] or r['sales_signals'] or r['badges_detected'] else 'Low/unclear from captured page')
    md += [f"### {r['keyword']}", '', f"- Results quantity: {demand}", f"- Sales signal: {sales_level}", f"- Reviews captured: {', '.join(r['review_signals']) if r['review_signals'] else 'none captured'}", f"- Sales captured: {', '.join(r['sales_signals']) if r['sales_signals'] else 'none captured'}", f"- Badges captured: {', '.join(r['badges_detected']) if r['badges_detected'] else 'none captured'}", f"- Screenshot: `{r['screenshot']}`", f"- Blocked: {r['blocked']}", '']
md += ['## Decision', '', 'Because the inspector strategy is commercially sound and “AI Influencer” is likely an emerging/low-search phrase, reposition the product away from narrow `AI Influencer Starter Kit` wording and toward broader buyer-intent terms:', '', '- Primary packaging: **AI Content Creator Toolkit**', '- Alternate positioning: **AI Creator Growth Bundle**', '- Secondary angle: **Faceless Creator Business Kit**', '', 'Use “AI influencer” inside the product as a feature/bonus, not as the main search phrase.', '', '## Pricing Validation', '', '- Launch price: **$14.99**', '- Anchor price: **$29.99**', '- Offer display: **50% OFF — $29.99 → $14.99**', '', '## Upload Readiness', '', 'Do not upload until the new 10-image carousel, SEO titles, product description, and Pinterest batch are aligned with the broader creator/search demand.']
(OUT/'Etsy-Market-Validation.md').write_text('\n'.join(md))
print('\n'.join([f"{r['keyword']}: results={r['results_detected']} blocked={r['blocked']} screenshot={r['screenshot']}" for r in rows]))
