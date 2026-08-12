from pathlib import Path
import subprocess
import textwrap

ROOT = Path('/sources/AI-Virtual-Influencer-Starter-Kit')
ETSY = ROOT / '06-Etsy-Listing'
PINT = ROOT / '07-Pinterest'
ETSY.mkdir(parents=True, exist_ok=True)
PINT.mkdir(parents=True, exist_ok=True)

W, H = 3000, 2400
PW, PH = 1000, 1500

CSS = """
.title{font-family:Arial,Helvetica,sans-serif;font-weight:900;letter-spacing:-2px;fill:#fff}
.sub{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#f8fafc}
.small{font-family:Arial,Helvetica,sans-serif;font-weight:600;fill:#cbd5e1}
.dark{font-family:Arial,Helvetica,sans-serif;font-weight:900;fill:#111827}
.muted{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#475569}
.tag{font-family:Arial,Helvetica,sans-serif;font-weight:800;fill:#0f172a}
"""

def bg_defs():
    return '''
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#080816"/>
        <stop offset="45%" stop-color="#4c1d95"/>
        <stop offset="100%" stop-color="#fb923c"/>
      </linearGradient>
      <linearGradient id="card" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="100%" stop-color="#f8fafc"/>
      </linearGradient>
      <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
        <feDropShadow dx="0" dy="28" stdDeviation="28" flood-color="#000" flood-opacity="0.35"/>
      </filter>
      <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
        <feGaussianBlur stdDeviation="45"/>
      </filter>
    </defs>
    '''

def pdf_mock(x,y,w,h,title,accent="#fb923c"):
    return f'''
    <g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="url(#card)"/>
      <rect x="{x}" y="{y}" width="{w}" height="160" rx="34" fill="{accent}"/>
      <rect x="{x}" y="{y+120}" width="{w}" height="70" fill="{accent}"/>
      <text x="{x+48}" y="{y+96}" font-family="Arial" font-size="42" font-weight="900" fill="#fff">PDF</text>
      <text x="{x+48}" y="{y+245}" font-family="Arial" font-size="52" font-weight="900" fill="#111827">{title}</text>
      <rect x="{x+48}" y="{y+310}" width="{w-96}" height="18" rx="9" fill="#e5e7eb"/>
      <rect x="{x+48}" y="{y+355}" width="{w-180}" height="18" rx="9" fill="#e5e7eb"/>
      <rect x="{x+48}" y="{y+400}" width="{w-135}" height="18" rx="9" fill="#e5e7eb"/>
      <circle cx="{x+w-110}" cy="{y+h-100}" r="50" fill="{accent}" opacity="0.9"/>
    </g>'''

def write_svg(path, body, width=W, height=H):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
    <style>{CSS}</style>{bg_defs()}
    {body}
    </svg>'''
    path.write_text(svg)
    png = path.with_suffix('.png')
    subprocess.run(['rsvg-convert', '-w', str(width), '-h', str(height), str(path), '-o', str(png)], check=True)
    return png

assets = []

# Etsy 1 main
body = f'''
<rect width="100%" height="100%" fill="url(#bg)"/>
<circle cx="2350" cy="350" r="420" fill="#f97316" opacity="0.35" filter="url(#soft)"/>
<circle cx="450" cy="2100" r="520" fill="#7c3aed" opacity="0.45" filter="url(#soft)"/>
<text x="170" y="270" class="small" font-size="48">DIGITAL DOWNLOAD BUNDLE</text>
<text x="170" y="480" class="title" font-size="150">AI Virtual</text>
<text x="170" y="650" class="title" font-size="150">Influencer</text>
<text x="170" y="820" class="title" font-size="150">Starter Kit</text>
<text x="178" y="930" class="sub" font-size="58">Launch your first AI influencer in 7 days</text>
{pdf_mock(1720,360,860,1050,'Workbook','#7c3aed')}
{pdf_mock(1340,760,860,1050,'100 Prompts','#f97316')}
<rect x="170" y="1150" width="1170" height="470" rx="42" fill="#fff" opacity="0.95"/>
<text x="235" y="1260" class="dark" font-size="64">Includes:</text>
<text x="235" y="1360" class="muted" font-size="50">✓ 100 AI Influencer Prompts</text>
<text x="235" y="1440" class="muted" font-size="50">✓ Face Consistency System</text>
<text x="235" y="1520" class="muted" font-size="50">✓ X Templates + Hooks + Captions</text>
<rect x="170" y="1750" width="760" height="120" rx="60" fill="#f97316"/>
<text x="250" y="1830" class="sub" font-size="52">BEGINNER FRIENDLY</text>
<text x="170" y="2135" class="small" font-size="46">PDF WORKBOOK • PROMPTS • SOCIAL TEMPLATES</text>
'''
assets.append(write_svg(ETSY/'etsy-01-main-cover.svg', body))

# Etsy 2 what's inside
body = f'''
<rect width="100%" height="100%" fill="#f8fafc"/>
<rect x="0" y="0" width="3000" height="410" fill="#111827"/>
<text x="150" y="170" class="title" font-size="110">What’s Inside</text>
<text x="150" y="280" class="small" font-size="46">A complete beginner system, not just random prompts</text>
{pdf_mock(170,620,480,610,'Workbook','#7c3aed')}
{pdf_mock(720,620,480,610,'Prompts','#f97316')}
{pdf_mock(1270,620,480,610,'X Posts','#0ea5e9')}
{pdf_mock(1820,620,480,610,'Hooks','#14b8a6')}
{pdf_mock(2370,620,480,610,'Captions','#ec4899')}
<text x="150" y="1510" class="dark" font-size="74">5 PDF files included</text>
<text x="150" y="1640" class="muted" font-size="54">Workbook + 100 Prompts + 50 X Templates</text>
<text x="150" y="1725" class="muted" font-size="54">+ 30 YouTube Hooks + 30 Instagram Captions</text>
<rect x="150" y="1910" width="1250" height="130" rx="65" fill="#111827"/>
<text x="240" y="1996" class="sub" font-size="52">INSTANT DIGITAL DOWNLOAD</text>
'''
assets.append(write_svg(ETSY/'etsy-02-whats-inside.svg', body))

# Etsy 3 prompt categories
cats = ['Selfies','Travel','Coffee Shop','Luxury','Fashion','Holidays','Engagement','Brand Promo','Video Scenes','Face Consistency']
items=''.join([f'<rect x="{150+(i%2)*1330}" y="{520+(i//2)*260}" width="1190" height="170" rx="36" fill="#fff" filter="url(#shadow)"/><text x="{220+(i%2)*1330}" y="{630+(i//2)*260}" class="tag" font-size="58">{i+1}. {c}</text>' for i,c in enumerate(cats)])
body = f'''
<rect width="100%" height="100%" fill="url(#bg)"/>
<text x="150" y="230" class="title" font-size="120">100 Copy-Paste Prompts</text>
<text x="155" y="335" class="small" font-size="48">10 chapters designed for AI influencer content creation</text>
{items}
<text x="150" y="2220" class="small" font-size="52">Use with your favorite AI image or video generator</text>
'''
assets.append(write_svg(ETSY/'etsy-03-prompt-categories.svg', body))

# Etsy 4 buyer transformation
body = f'''
<rect width="100%" height="100%" fill="#0f172a"/>
<circle cx="2600" cy="300" r="500" fill="#f97316" opacity="0.25" filter="url(#soft)"/>
<circle cx="280" cy="2150" r="520" fill="#7c3aed" opacity="0.35" filter="url(#soft)"/>
<text x="160" y="260" class="title" font-size="112">From Blank Page</text>
<text x="160" y="390" class="title" font-size="112">to Content System</text>
<rect x="170" y="620" width="1210" height="1050" rx="60" fill="#fff" opacity="0.95"/>
<text x="250" y="760" class="dark" font-size="68">Before</text>
<text x="250" y="900" class="muted" font-size="54">• No character idea</text>
<text x="250" y="1010" class="muted" font-size="54">• No prompt structure</text>
<text x="250" y="1120" class="muted" font-size="54">• Inconsistent AI face</text>
<text x="250" y="1230" class="muted" font-size="54">• No content plan</text>
<text x="250" y="1340" class="muted" font-size="54">• Random posting</text>
<rect x="1620" y="620" width="1210" height="1050" rx="60" fill="#fff" opacity="0.95"/>
<text x="1700" y="760" class="dark" font-size="68">After</text>
<text x="1700" y="900" class="muted" font-size="54">• Clear AI persona</text>
<text x="1700" y="1010" class="muted" font-size="54">• 100 ready prompts</text>
<text x="1700" y="1120" class="muted" font-size="54">• Consistency prompts</text>
<text x="1700" y="1230" class="muted" font-size="54">• Hooks + captions</text>
<text x="1700" y="1340" class="muted" font-size="54">• 7-day launch plan</text>
<text x="160" y="2050" class="sub" font-size="58">Built for beginners who want to create faster.</text>
'''
assets.append(write_svg(ETSY/'etsy-04-transformation.svg', body))

# Etsy 5 no physical / disclaimer
body = f'''
<rect width="100%" height="100%" fill="#fff7ed"/>
<rect x="150" y="150" width="2700" height="2100" rx="70" fill="#ffffff" filter="url(#shadow)"/>
<text x="270" y="360" class="dark" font-size="105">Important Notes</text>
<text x="270" y="520" class="muted" font-size="58">This is a digital PDF bundle.</text>
<text x="270" y="670" class="muted" font-size="52">✓ No physical item shipped</text>
<text x="270" y="780" class="muted" font-size="52">✓ Instant download after purchase</text>
<text x="270" y="890" class="muted" font-size="52">✓ Beginner-friendly templates</text>
<text x="270" y="1000" class="muted" font-size="52">✓ Editable by copying prompts into your tools</text>
<rect x="270" y="1210" width="2460" height="4" fill="#fed7aa"/>
<text x="270" y="1380" class="dark" font-size="70">Works as a starter system for:</text>
<text x="270" y="1510" class="muted" font-size="52">AI influencers • virtual models • faceless creators</text>
<text x="270" y="1610" class="muted" font-size="52">Instagram • TikTok • X • YouTube Shorts</text>
<text x="270" y="1840" class="muted" font-size="42">Results vary depending on AI tool, model, settings, and your character details.</text>
<rect x="270" y="1980" width="760" height="120" rx="60" fill="#f97316"/>
<text x="350" y="2060" class="sub" font-size="50">DOWNLOAD ONLY</text>
'''
assets.append(write_svg(ETSY/'etsy-05-digital-download.svg', body))

# Pinterest pins
pin_data = [
('pinterest-01-ai-influencer-starter-kit.svg','AI Influencer\nStarter Kit','100 prompts + workbook + captions','Create a faceless content brand faster'),
('pinterest-02-100-prompts.svg','100 AI\nInfluencer\nPrompts','Selfies • Travel • Fashion • Video','Copy, customize, generate content'),
('pinterest-03-faceless-creator.svg','Build a\nFaceless\nCreator Brand','No camera. No design skills.','Start with an AI virtual influencer'),
]
for fname,title,sub,foot in pin_data:
    lines=title.split('\\n')
    text=''.join(f'<text x="70" y="{250+i*115}" class="title" font-size="92">{line}</text>' for i,line in enumerate(lines))
    body=f'''
    <rect width="100%" height="100%" fill="url(#bg)"/>
    <circle cx="820" cy="150" r="260" fill="#f97316" opacity="0.3" filter="url(#soft)"/>
    {text}
    <rect x="70" y="{250+len(lines)*115+30}" width="830" height="150" rx="44" fill="#fff" opacity="0.95"/>
    <text x="110" y="{250+len(lines)*115+120}" class="dark" font-size="38">{sub}</text>
    {pdf_mock(155,820,690,460,'PDF Bundle','#f97316')}
    <text x="70" y="1375" class="small" font-size="38">{foot}</text>
    '''
    assets.append(write_svg(PINT/fname, body, PW, PH))

print('\n'.join(str(a) for a in assets))
