from pathlib import Path
import subprocess
import textwrap

ROOT = Path('/sources/AI-Virtual-Influencer-Starter-Kit')
ETSY = ROOT / '06-Etsy-Listing'
PINT = ROOT / '07-Pinterest'
ETSY.mkdir(parents=True, exist_ok=True)
PINT.mkdir(parents=True, exist_ok=True)

EW, EH = 2700, 2025
PW, PH = 1000, 1500

CSS = """
.title{font-family:Arial,Helvetica,sans-serif;font-weight:900;letter-spacing:-2px;fill:#fff}
.titleDark{font-family:Arial,Helvetica,sans-serif;font-weight:900;letter-spacing:-1.5px;fill:#111827}
.sub{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#f8fafc}
.muted{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#475569}
.small{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#cbd5e1}
.micro{font-family:Arial,Helvetica,sans-serif;font-weight:600;fill:#64748b}
.badge{font-family:Arial,Helvetica,sans-serif;font-weight:900;fill:#0f172a}
.white{font-family:Arial,Helvetica,sans-serif;font-weight:900;fill:#fff}
"""

def defs():
    return '''
    <defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#080817"/>
        <stop offset="45%" stop-color="#43208d"/>
        <stop offset="100%" stop-color="#fb7a21"/>
      </linearGradient>
      <linearGradient id="cream" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#fff7ed"/>
        <stop offset="100%" stop-color="#f8fafc"/>
      </linearGradient>
      <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1">
        <stop offset="0%" stop-color="#ffffff"/>
        <stop offset="100%" stop-color="#f1f5f9"/>
      </linearGradient>
      <filter id="shadow" x="-20%" y="-20%" width="150%" height="150%">
        <feDropShadow dx="0" dy="22" stdDeviation="24" flood-color="#000" flood-opacity="0.28"/>
      </filter>
      <filter id="soft" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="50"/></filter>
    </defs>
    '''

def svg_escape(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def text_lines(x,y,lines,size=58,klass='muted',gap=82):
    return ''.join(f'<text x="{x}" y="{y+i*gap}" class="{klass}" font-size="{size}">{svg_escape(line)}</text>' for i,line in enumerate(lines))

def pdf_mock(x,y,w,h,title,sub='',accent='#fb7a21'):
    sub_txt = f'<text x="{x+44}" y="{y+310}" class="micro" font-size="30">{svg_escape(sub)}</text>' if sub else ''
    return f'''
    <g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="28" fill="url(#paper)"/>
      <rect x="{x}" y="{y}" width="{w}" height="125" rx="28" fill="{accent}"/>
      <rect x="{x}" y="{y+92}" width="{w}" height="45" fill="{accent}"/>
      <text x="{x+44}" y="{y+78}" class="white" font-size="38">PDF</text>
      <text x="{x+44}" y="{y+210}" class="titleDark" font-size="44">{svg_escape(title)}</text>
      {sub_txt}
      <rect x="{x+44}" y="{y+360}" width="{w-88}" height="16" rx="8" fill="#e5e7eb"/>
      <rect x="{x+44}" y="{y+405}" width="{w-150}" height="16" rx="8" fill="#e5e7eb"/>
      <rect x="{x+44}" y="{y+450}" width="{w-115}" height="16" rx="8" fill="#e5e7eb"/>
      <circle cx="{x+w-88}" cy="{y+h-78}" r="44" fill="{accent}" opacity="0.9"/>
    </g>'''

def notion_mock(x,y,w,h):
    rows=''.join(f'<rect x="{x+55}" y="{y+190+i*70}" width="{w-110}" height="34" rx="12" fill="{c}" opacity="0.9"/>' for i,c in enumerate(['#e2e8f0','#fed7aa','#ddd6fe','#e2e8f0','#c7d2fe','#e2e8f0']))
    return f'''
    <g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="32" fill="#ffffff"/>
      <rect x="{x}" y="{y}" width="{w}" height="95" rx="32" fill="#111827"/>
      <circle cx="{x+58}" cy="{y+48}" r="13" fill="#fb7185"/><circle cx="{x+100}" cy="{y+48}" r="13" fill="#fbbf24"/><circle cx="{x+142}" cy="{y+48}" r="13" fill="#34d399"/>
      <text x="{x+55}" y="{y+150}" class="titleDark" font-size="42">Creator Planner</text>
      {rows}
    </g>'''

def write_svg(path, body, w=EW, h=EH):
    data=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><style>{CSS}</style>{defs()}{body}</svg>'
    path.write_text(data)
    png=path.with_suffix('.png')
    subprocess.run(['rsvg-convert','-w',str(w),'-h',str(h),str(path),'-o',str(png)], check=True)
    return png

etsy_specs = []

# 1 value display
body=f'''
<rect width="100%" height="100%" fill="url(#bg)"/>
<circle cx="2320" cy="250" r="380" fill="#fb923c" opacity="0.34" filter="url(#soft)"/>
<text x="145" y="210" class="small" font-size="46">DIGITAL DOWNLOAD • LAUNCH OFFER $14.99</text>
<text x="145" y="405" class="title" font-size="132">AI CREATOR KIT</text>
<text x="150" y="520" class="sub" font-size="56">Launch Your Content Brand Faster</text>
<rect x="145" y="690" width="1040" height="600" rx="46" fill="#fff" opacity="0.96"/>
{text_lines(215,815,['✓ 100 AI Prompts','✓ 50 X Templates','✓ 30 YouTube Hooks','✓ 30 Instagram Captions','✓ Workbook'],54,'muted',96)}
{pdf_mock(1510,360,570,720,'Prompt Pack','100 AI prompts','#fb7a21')}
{pdf_mock(1840,680,570,720,'Workbook','creator planner','#7c3aed')}
{notion_mock(1330,1030,740,520)}
<rect x="145" y="1590" width="720" height="115" rx="58" fill="#fb7a21"/>
<text x="218" y="1665" class="white" font-size="48">50% OFF TODAY</text>
'''
etsy_specs.append(('etsy-new-01-main-value.svg',body))

# 2 table of contents
body=f'''
<rect width="100%" height="100%" fill="#f8fafc"/>
<rect x="0" y="0" width="2700" height="330" fill="#111827"/>
<text x="145" y="145" class="title" font-size="96">Everything Included</text>
<text x="150" y="245" class="small" font-size="42">A practical content system for creators, freelancers, coaches, and AI users</text>
{pdf_mock(145,480,440,540,'Workbook','planning','#7c3aed')}
{pdf_mock(645,480,440,540,'100 Prompts','AI content','#fb7a21')}
{pdf_mock(1145,480,440,540,'50 X Posts','templates','#0ea5e9')}
{pdf_mock(1645,480,440,540,'30 Hooks','YouTube','#14b8a6')}
{pdf_mock(2145,480,440,540,'30 Captions','Instagram','#ec4899')}
<rect x="145" y="1200" width="2410" height="520" rx="50" fill="#ffffff" filter="url(#shadow)"/>
{text_lines(235,1330,['Workbook • Content Strategy • Niche & Persona Worksheets','Prompt Pack • Selfies • Travel • Lifestyle • Brand Posts','Templates • X Posts • YouTube Hooks • Instagram Captions'],48,'muted',115)}
'''
etsy_specs.append(('etsy-new-02-contents.svg',body))

# 3 prompt example
body=f'''
<rect width="100%" height="100%" fill="url(#cream)"/>
<text x="145" y="210" class="titleDark" font-size="106">Prompt Example</text>
<text x="150" y="315" class="muted" font-size="46">Copy, customize, and generate faster</text>
<rect x="145" y="470" width="2410" height="860" rx="52" fill="#111827" filter="url(#shadow)"/>
<text x="240" y="610" class="small" font-size="42">AI PROMPT TEMPLATE</text>
{text_lines(240,740,['Create a realistic lifestyle photo of [character name],','a [niche] content creator, sitting in a modern coffee shop,','natural morning light, premium editorial style,','consistent face, detailed outfit, social media ready.'],48,'sub',90)}
<rect x="145" y="1510" width="850" height="115" rx="58" fill="#fb7a21"/>
<text x="225" y="1585" class="white" font-size="48">100 PROMPTS INCLUDED</text>
'''
etsy_specs.append(('etsy-new-03-prompt-example.svg',body))

# 4 youtube hook
body=f'''
<rect width="100%" height="100%" fill="#0f172a"/>
<circle cx="2350" cy="1550" r="520" fill="#dc2626" opacity="0.25" filter="url(#soft)"/>
<text x="145" y="220" class="title" font-size="108">YouTube Hook Examples</text>
<text x="150" y="325" class="small" font-size="46">Short-form hooks for Reels, Shorts, and TikTok</text>
<rect x="145" y="510" width="2410" height="930" rx="52" fill="#ffffff"/>
{text_lines(245,675,['“I built an AI content brand in 7 days.”','“Nobody talks about this AI creator workflow.”','“Steal this prompt system for your next 30 posts.”','“This is how faceless creators plan content faster.”'],58,'muted',150)}
<rect x="145" y="1620" width="790" height="115" rx="58" fill="#dc2626"/>
<text x="225" y="1695" class="white" font-size="48">30 HOOKS INCLUDED</text>
'''
etsy_specs.append(('etsy-new-04-youtube-hooks.svg',body))

# 5 X template
body=f'''
<rect width="100%" height="100%" fill="#f8fafc"/>
<text x="145" y="220" class="titleDark" font-size="108">X Post Templates</text>
<text x="150" y="325" class="muted" font-size="46">Content frameworks for authority, growth, and engagement</text>
<rect x="145" y="505" width="2410" height="900" rx="52" fill="#111827" filter="url(#shadow)"/>
{text_lines(245,670,['I spent [timeframe] testing [AI/content workflow].','Here are [number] things nobody tells you:', '1. [Lesson]', '2. [Lesson]', '3. [Lesson]', 'Save this if you are building a creator brand.'],50,'sub',105)}
<rect x="145" y="1605" width="820" height="115" rx="58" fill="#111827"/>
<text x="225" y="1680" class="white" font-size="48">50 X TEMPLATES</text>
'''
etsy_specs.append(('etsy-new-05-x-templates.svg',body))

# 6 instagram captions
body=f'''
<rect width="100%" height="100%" fill="url(#bg)"/>
<text x="145" y="220" class="title" font-size="108">Instagram Captions</text>
<text x="150" y="325" class="small" font-size="46">Lifestyle, creator, travel, and motivation captions</text>
<rect x="200" y="520" width="690" height="880" rx="58" fill="#ffffff" filter="url(#shadow)"/>
<rect x="970" y="520" width="690" height="880" rx="58" fill="#ffffff" filter="url(#shadow)"/>
<rect x="1740" y="520" width="690" height="880" rx="58" fill="#ffffff" filter="url(#shadow)"/>
{text_lines(270,690,['Somewhere','between work','and adventure.'],48,'muted',86)}
{text_lines(1040,690,['Building','quietly,','posting','consistently.'],48,'muted',86)}
{text_lines(1810,690,['A little','more signal,','a little','less noise.'],48,'muted',86)}
<rect x="145" y="1610" width="930" height="115" rx="58" fill="#ec4899"/>
<text x="225" y="1685" class="white" font-size="48">30 CAPTIONS INCLUDED</text>
'''
etsy_specs.append(('etsy-new-06-instagram-captions.svg',body))

# 7 workflow
body=f'''
<rect width="100%" height="100%" fill="#fff7ed"/>
<text x="145" y="220" class="titleDark" font-size="108">Simple Creator Workflow</text>
<text x="150" y="325" class="muted" font-size="46">Turn prompts into content, audience, and income experiments</text>
{''.join([f'<rect x="{225+i*615}" y="690" width="430" height="250" rx="48" fill="{c}" filter="url(#shadow)"/><text x="{300+i*615}" y="845" class="white" font-size="56">{t}</text>' for i,(t,c) in enumerate([('Prompt','#7c3aed'),('Content','#fb7a21'),('Audience','#0ea5e9'),('Income','#16a34a')])])}
{''.join([f'<text x="{700+i*615}" y="850" class="titleDark" font-size="80">↓</text>' for i in range(3)])}
<rect x="145" y="1240" width="2410" height="300" rx="52" fill="#ffffff"/>
<text x="245" y="1380" class="muted" font-size="56">Plan once. Generate faster. Post consistently.</text>
'''
etsy_specs.append(('etsy-new-07-workflow.svg',body))

# 8 for whom
body=f'''
<rect width="100%" height="100%" fill="#0f172a"/>
<text x="145" y="220" class="title" font-size="112">Who It’s For</text>
<text x="150" y="325" class="small" font-size="46">A starter kit for people building a content brand with AI</text>
{''.join([f'<rect x="{210+(i%2)*1180}" y="{560+(i//2)*360}" width="980" height="240" rx="50" fill="#ffffff"/><text x="{300+(i%2)*1180}" y="{710+(i//2)*360}" class="titleDark" font-size="62">✓ {t}</text>' for i,t in enumerate(['Creators','Freelancers','AI Users','Coaches','Influencers','Digital Sellers'])])}
'''
etsy_specs.append(('etsy-new-08-who-for.svg',body))

# 9 bonus
body=f'''
<rect width="100%" height="100%" fill="url(#bg)"/>
<text x="145" y="220" class="title" font-size="112">Bonus Stack</text>
<text x="150" y="325" class="small" font-size="46">More than a workbook — a usable content bundle</text>
{pdf_mock(210,560,650,780,'50 X Templates','growth posts','#111827')}
{pdf_mock(1010,560,650,780,'30 YouTube Hooks','short-form ideas','#dc2626')}
{pdf_mock(1810,560,650,780,'30 IG Captions','ready captions','#ec4899')}
<rect x="145" y="1580" width="1020" height="115" rx="58" fill="#ffffff"/>
<text x="225" y="1655" class="titleDark" font-size="48">INCLUDED WITH THE BUNDLE</text>
'''
etsy_specs.append(('etsy-new-09-bonus.svg',body))

# 10 FAQ
body=f'''
<rect width="100%" height="100%" fill="#f8fafc"/>
<text x="145" y="220" class="titleDark" font-size="112">FAQ</text>
<text x="150" y="325" class="muted" font-size="46">Before you download</text>
<rect x="145" y="510" width="2410" height="1120" rx="52" fill="#ffffff" filter="url(#shadow)"/>
{text_lines(245,660,['Is this physical?  No — instant digital download.','Do I need design skills?  No — beginner friendly.','Can I customize it?  Yes — copy and edit the prompts.','Does it guarantee income?  No — it gives you a creation system.','What files are included?  PDF workbook, prompts, hooks, templates, captions.'],45,'muted',165)}
<rect x="145" y="1760" width="900" height="115" rx="58" fill="#fb7a21"/>
<text x="225" y="1835" class="white" font-size="48">READY TO DOWNLOAD</text>
'''
etsy_specs.append(('etsy-new-10-faq.svg',body))

# Generate Etsy
outs=[]
for fname, body in etsy_specs:
    outs.append(write_svg(ETSY/fname, body, EW, EH))

# Pinterest 20 pins
pin_angles = [
('AI Content Creator Toolkit','100 AI prompts + workbook','Launch your content brand faster'),
('100 AI Prompts for Creators','Selfies, hooks, captions, posts','Copy, customize, create'),
('Faceless Creator Business Kit','No camera required','Build a creator brand with AI'),
('Content Creator Kit for Beginners','Prompts + templates + planner','Start posting consistently'),
('YouTube Growth Bundle','30 short-form hooks included','Never start from blank again'),
('Social Media Templates','X posts + Instagram captions','Create faster with AI'),
('Creator Business Planner','Plan your niche and content system','Workbook included'),
('AI Prompt Pack','Lifestyle, brand, travel, video','100 copy-paste prompts'),
('Instagram Caption Kit','30 captions for creator brands','Post faster this week'),
('X Post Template Pack','50 viral-style frameworks','Build authority with content'),
('Launch Your Content Brand','AI workflow for beginners','Prompt → Content → Audience'),
('AI Tools for Creators','Prompt systems and content ideas','Make content less chaotic'),
('Digital Product for Creators','Instant PDF download','Creator kit for AI users'),
('Faceless Content Ideas','For coaches and freelancers','Use AI to plan content'),
('AI Creator Growth Bundle','Prompts, hooks, captions','One bundle, faster workflow'),
('Build an AI Content Brand','Beginner-friendly system','PDF toolkit included'),
('Creator Templates Bundle','Social media + AI prompts','Download and start today'),
('Content Workflow Kit','Plan, prompt, post','Simple creator system'),
('AI Side Hustle Toolkit','Content brand starter files','For digital creators'),
('Social Media Creator Planner','Workbook + prompt pack','Create consistently'),
]
for idx,(title,sub,foot) in enumerate(pin_angles,1):
    words = title.split(' ')
    # line break title roughly
    if len(words) > 4:
        lines = [' '.join(words[:3]), ' '.join(words[3:])]
    else:
        lines = [' '.join(words[:2]), ' '.join(words[2:])] if len(words)>2 else [title]
    txt=''.join(f'<text x="70" y="{230+i*96}" class="title" font-size="78">{svg_escape(line)}</text>' for i,line in enumerate(lines) if line)
    body=f'''
    <rect width="100%" height="100%" fill="url(#bg)"/>
    <circle cx="850" cy="160" r="260" fill="#fb923c" opacity="0.32" filter="url(#soft)"/>
    {txt}
    <text x="72" y="{260+len(lines)*96}" class="small" font-size="34">{svg_escape(sub)}</text>
    <rect x="70" y="{325+len(lines)*96}" width="860" height="105" rx="36" fill="#ffffff" opacity="0.96"/>
    <text x="115" y="{392+len(lines)*96}" class="titleDark" font-size="34">{svg_escape(foot)}</text>
    {pdf_mock(150,760,700,480,'AI Creator Kit','PDF bundle','#fb7a21')}
    <rect x="70" y="1325" width="540" height="78" rx="39" fill="#ffffff" opacity="0.95"/>
    <text x="115" y="1377" class="titleDark" font-size="30">Instant Digital Download</text>
    '''
    outs.append(write_svg(PINT/f'pinterest-new-{idx:02d}.svg', body, PW, PH))

print('\n'.join(map(str, outs)))
