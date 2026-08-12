from pathlib import Path
import subprocess, zipfile, shutil

ROOT = Path('/sources/AI-Virtual-Influencer-Starter-Kit')
ETSY = ROOT / '06-Etsy-Listing' / 'v2-gpt-image2-style'
PINT = ROOT / '07-Pinterest' / 'v2-gpt-image2-style'
PKG = ROOT / '08-Launch-Package'
SELLER_V2 = PKG / 'Seller-Upload-Kit-V2-GPT-Image2-Style'
for p in [ETSY, PINT, SELLER_V2 / '01-Etsy-Listing-Images', SELLER_V2 / '02-Pinterest-Pins', SELLER_V2 / '03-Listing-Copy', SELLER_V2 / '04-Upload-Checklist']:
    p.mkdir(parents=True, exist_ok=True)

EW, EH = 2700, 2025
PW, PH = 1000, 1500

CSS = """
.h1{font-family:Arial Black,Arial,sans-serif;font-weight:900;letter-spacing:-5px;fill:#fff}
.h1p{font-family:Arial Black,Arial,sans-serif;font-weight:900;letter-spacing:-5px;fill:#a855f7}
.h2{font-family:Arial,Helvetica,sans-serif;font-weight:900;fill:#fff}
.purple{font-family:Arial,Helvetica,sans-serif;font-weight:900;fill:#a855f7}
.body{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#e5e7eb}
.muted{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#94a3b8}
.yellow{font-family:Arial Black,Arial,sans-serif;font-weight:900;fill:#facc15}
.dark{font-family:Arial Black,Arial,sans-serif;font-weight:900;fill:#0b1020}
.small{font-family:Arial,Helvetica,sans-serif;font-weight:800;fill:#f8fafc}
"""

def defs():
    return '''<defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#050816"/><stop offset="52%" stop-color="#111827"/><stop offset="100%" stop-color="#220844"/></linearGradient>
    <radialGradient id="glow" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#a855f7" stop-opacity="0.75"/><stop offset="100%" stop-color="#a855f7" stop-opacity="0"/></radialGradient>
    <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#1f2937"/><stop offset="100%" stop-color="#060914"/></linearGradient>
    <linearGradient id="paper" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#ffffff"/><stop offset="100%" stop-color="#e5e7eb"/></linearGradient>
    <filter id="shadow" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="0" dy="28" stdDeviation="28" flood-color="#000" flood-opacity="0.50"/></filter>
    <filter id="neon" x="-40%" y="-40%" width="180%" height="180%"><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#a855f7" flood-opacity="0.85"/></filter>
    <filter id="blur"><feGaussianBlur stdDeviation="55"/></filter>
    </defs>'''

def esc(s):
    return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def bg(w,h):
    return f'''<rect width="100%" height="100%" fill="url(#bg)"/>
    <circle cx="{w*0.78}" cy="{h*0.28}" r="{w*0.22}" fill="url(#glow)" filter="url(#blur)" opacity="0.9"/>
    <circle cx="{w*0.22}" cy="{h*0.88}" r="{w*0.18}" fill="#a855f7" filter="url(#blur)" opacity="0.22"/>
    <path d="M0,{h*0.86} C{w*0.3},{h*0.75} {w*0.55},{h*0.95} {w},{h*0.78} L{w},{h} L0,{h} Z" fill="#0b1020" opacity="0.78"/>
    '''

def topbar(text, w=EW):
    return f'<rect x="0" y="0" width="{w}" height="92" fill="#020617"/><text x="90" y="60" class="small" font-size="34">{esc(text)}</text>'

def feature_box(x,y,w,h,items,bonus=None):
    rows=[]
    for i,it in enumerate(items):
        yy=y+92+i*72
        rows.append(f'<text x="{x+60}" y="{yy}" class="purple" font-size="42">✓</text><text x="{x+115}" y="{yy}" class="body" font-size="42">{esc(it)}</text>')
    if bonus:
        yy=y+92+len(items)*72+15
        rows.append(f'<rect x="{x+48}" y="{yy-50}" width="{w-96}" height="68" rx="20" fill="#2e1065" stroke="#a855f7" stroke-width="2"/><text x="{x+76}" y="{yy-5}" class="purple" font-size="36">BONUS: {esc(bonus)}</text>')
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="34" fill="#050816" stroke="#312e81" stroke-width="3" opacity="0.96" filter="url(#shadow)"/>' + ''.join(rows)

def ebook(x,y,w,h,title='AI CREATOR KIT',sub='Prompt Pack'):
    return f'''<g filter="url(#shadow)">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="url(#paper)"/>
    <rect x="{x+28}" y="{y+28}" width="{w-56}" height="{h-56}" rx="20" fill="#111827"/>
    <circle cx="{x+w*0.72}" cy="{y+h*0.22}" r="{w*0.20}" fill="#a855f7" opacity="0.55" filter="url(#neon)"/>
    <text x="{x+56}" y="{y+130}" class="h1p" font-size="54">AI</text>
    <text x="{x+56}" y="{y+195}" class="h2" font-size="54">CREATOR</text>
    <text x="{x+56}" y="{y+260}" class="h2" font-size="54">KIT</text>
    <text x="{x+56}" y="{y+335}" class="body" font-size="26">{esc(sub)}</text>
    <rect x="{x+56}" y="{y+h-140}" width="{w-112}" height="54" rx="27" fill="#a855f7"/>
    <text x="{x+92}" y="{y+h-105}" class="small" font-size="24">DIGITAL DOWNLOAD</text>
    </g>'''

def phone(x,y,w,h):
    return f'''<g filter="url(#shadow)">
    <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="58" fill="#020617" stroke="#475569" stroke-width="8"/>
    <rect x="{x+32}" y="{y+70}" width="{w-64}" height="{h-120}" rx="34" fill="#0f172a"/>
    <text x="{x+58}" y="{y+145}" class="small" font-size="28">Creator Dashboard</text>
    <rect x="{x+58}" y="{y+190}" width="{w-116}" height="70" rx="18" fill="#2e1065"/>
    <text x="{x+82}" y="{y+235}" class="purple" font-size="28">100 AI Prompts</text>
    <rect x="{x+58}" y="{y+292}" width="{w-116}" height="45" rx="14" fill="#1e293b"/>
    <rect x="{x+58}" y="{y+362}" width="{w-170}" height="45" rx="14" fill="#1e293b"/>
    <rect x="{x+58}" y="{y+432}" width="{w-135}" height="45" rx="14" fill="#1e293b"/>
    <rect x="{x+58}" y="{y+540}" width="{w-116}" height="120" rx="22" fill="#a855f7" opacity="0.86"/>
    <text x="{x+88}" y="{y+612}" class="small" font-size="34">Plan → Post</text>
    </g>'''

def floating_card(x,y,w,h,title,body='',color='#a855f7'):
    return f'''<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#111827" stroke="{color}" stroke-width="3"/>
    <text x="{x+34}" y="{y+60}" class="small" font-size="30">{esc(title)}</text>
    <text x="{x+34}" y="{y+108}" class="muted" font-size="22">{esc(body)}</text></g>'''

def price_bar(w=EW,h=EH):
    return f'''<rect x="0" y="{h-155}" width="{w}" height="155" fill="#020617"/>
    <rect x="90" y="{h-118}" width="420" height="82" rx="41" fill="#facc15"/>
    <text x="140" y="{h-64}" class="dark" font-size="36">50% OFF TODAY</text>
    <text x="650" y="{h-60}" class="yellow" font-size="72">$14.99</text>
    <text x="940" y="{h-64}" class="muted" font-size="38">$29.99</text>
    <line x1="936" y1="{h-76}" x2="1080" y2="{h-96}" stroke="#94a3b8" stroke-width="5"/>
    <circle cx="{w-190}" cy="{h-78}" r="55" fill="#172554" stroke="#a855f7" stroke-width="4"/>
    <text x="{w-238}" y="{h-68}" class="small" font-size="26">INSTANT</text>'''

def write_svg(path, body, w, h):
    data=f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><style>{CSS}</style>{defs()}{body}</svg>'
    path.write_text(data)
    png=path.with_suffix('.png')
    subprocess.run(['rsvg-convert','-w',str(w),'-h',str(h),str(path),'-o',str(png)], check=True)
    return png

# Etsy 10 images
slides=[]
items=['100 AI Prompts','50 X Templates','30 YouTube Hooks','30 Instagram Captions','Workbook & Planner']
slides.append(('etsy-v2-01-main-value.svg', bg(EW,EH)+topbar('DIGITAL DOWNLOAD  |  LAUNCH OFFER $14.99')+
    '<text x="95" y="295" class="h1p" font-size="150">AI</text><text x="290" y="295" class="h1" font-size="150"> CREATOR KIT</text>'+
    '<text x="100" y="430" class="h2" font-size="64">Launch Your Content Brand <tspan fill="#a855f7">Faster</tspan></text>'+
    '<text x="100" y="520" class="body" font-size="39">Everything You Need to Create, Grow &amp; Monetize Your Faceless Content Brand</text>'+
    feature_box(95,650,990,590,items,'Notion Dashboard')+ebook(1350,360,470,650,'AI CREATOR KIT','Workbook')+phone(1950,430,440,780)+floating_card(1210,1060,520,155,'Prompt Pack','100 copy-paste AI prompts')+floating_card(1780,1240,510,155,'Creator Planner','workflow + content system')+price_bar()))
slides.append(('etsy-v2-02-contents.svg', bg(EW,EH)+topbar('WHAT IS INSIDE THE AI CREATOR KIT')+'<text x="95" y="285" class="h1" font-size="118">Everything Included</text><text x="100" y="390" class="body" font-size="42">Five ready-to-use files for content creators and AI users</text>'+ebook(120,560,410,530,'Workbook','plan your brand')+ebook(620,560,410,530,'100 Prompts','AI content')+ebook(1120,560,410,530,'X Posts','50 templates')+ebook(1620,560,410,530,'Hooks','30 video hooks')+ebook(2120,560,410,530,'Captions','30 captions')+feature_box(250,1260,2200,350,['Workbook + planner pages','100 prompts + templates + hooks + captions','Built for creators, freelancers, coaches and AI users'],None)+price_bar()))
slides.append(('etsy-v2-03-prompt-example.svg', bg(EW,EH)+topbar('PROMPT EXAMPLE')+'<text x="95" y="285" class="h1p" font-size="110">100 AI PROMPTS</text><text x="100" y="390" class="body" font-size="44">Copy, customize, and create faster</text><rect x="150" y="560" width="2400" height="820" rx="42" fill="#050816" stroke="#a855f7" stroke-width="4" filter="url(#shadow)"/><text x="240" y="690" class="purple" font-size="42">PROMPT TEMPLATE</text><text x="240" y="805" class="body" font-size="48">Create a realistic lifestyle photo of [creator name],</text><text x="240" y="900" class="body" font-size="48">a [niche] content creator, modern coffee shop,</text><text x="240" y="995" class="body" font-size="48">premium editorial light, consistent face,</text><text x="240" y="1090" class="body" font-size="48">social-media-ready composition.</text>'+floating_card(1820,1190,520,145,'Use for','AI images + content ideas')+price_bar()))
slides.append(('etsy-v2-04-youtube-hooks.svg', bg(EW,EH)+topbar('YOUTUBE HOOK EXAMPLES')+'<text x="95" y="285" class="h1" font-size="108">30 YouTube Hooks</text><text x="100" y="390" class="body" font-size="44">Short-form hooks for Shorts, Reels and TikTok</text><rect x="160" y="560" width="2380" height="820" rx="42" fill="#050816" stroke="#ef4444" stroke-width="4" filter="url(#shadow)"/><text x="250" y="720" class="body" font-size="58">“I built an AI content brand in 7 days.”</text><text x="250" y="860" class="body" font-size="58">“Steal this prompt system for 30 posts.”</text><text x="250" y="1000" class="body" font-size="58">“Nobody talks about this AI workflow.”</text><text x="250" y="1140" class="body" font-size="58">“Here’s how faceless creators plan content.”</text>'+price_bar()))
slides.append(('etsy-v2-05-x-templates.svg', bg(EW,EH)+topbar('X / TWITTER POST TEMPLATES')+'<text x="95" y="285" class="h1p" font-size="108">50 X TEMPLATES</text><text x="100" y="390" class="body" font-size="44">Reusable frameworks for authority and engagement</text><rect x="170" y="560" width="2360" height="820" rx="42" fill="#050816" stroke="#60a5fa" stroke-width="4" filter="url(#shadow)"/><text x="260" y="710" class="body" font-size="52">I spent [timeframe] testing [workflow].</text><text x="260" y="830" class="body" font-size="52">Here are [number] things nobody tells you:</text><text x="260" y="950" class="body" font-size="52">1. [Lesson]   2. [Lesson]   3. [Lesson]</text><text x="260" y="1070" class="body" font-size="52">Save this if you are building a creator brand.</text>'+price_bar()))
slides.append(('etsy-v2-06-instagram-captions.svg', bg(EW,EH)+topbar('INSTAGRAM CAPTION EXAMPLES')+'<text x="95" y="285" class="h1" font-size="104">30 Instagram Captions</text><text x="100" y="390" class="body" font-size="44">Lifestyle, creator, travel and motivation captions</text>'+floating_card(170,580,690,370,'Caption 01','Somewhere between work and adventure.')+floating_card(1000,580,690,370,'Caption 02','Building quietly, posting consistently.')+floating_card(1830,580,690,370,'Caption 03','More signal. Less noise. More creation.')+ebook(1130,1110,430,520,'Captions','30 IG captions')+price_bar()))
slides.append(('etsy-v2-07-workflow.svg', bg(EW,EH)+topbar('CREATOR WORKFLOW')+'<text x="95" y="285" class="h1p" font-size="108">PROMPT → CONTENT → AUDIENCE</text><text x="100" y="390" class="body" font-size="44">A simple workflow for creator growth experiments</text><rect x="220" y="650" width="440" height="220" rx="42" fill="#a855f7" filter="url(#neon)"/><text x="315" y="785" class="small" font-size="58">Prompt</text><text x="740" y="790" class="h1p" font-size="82">↓</text><rect x="890" y="650" width="440" height="220" rx="42" fill="#2563eb"/><text x="985" y="785" class="small" font-size="58">Content</text><text x="1410" y="790" class="h1p" font-size="82">↓</text><rect x="1560" y="650" width="440" height="220" rx="42" fill="#7c3aed"/><text x="1648" y="785" class="small" font-size="58">Audience</text><text x="2080" y="790" class="h1p" font-size="82">↓</text><rect x="2230" y="650" width="360" height="220" rx="42" fill="#facc15"/><text x="2305" y="785" class="dark" font-size="58">Income</text><text x="400" y="1120" class="body" font-size="56">Plan once. Generate faster. Post consistently.</text>'+price_bar()))
slides.append(('etsy-v2-08-who-for.svg', bg(EW,EH)+topbar('WHO IT IS FOR')+'<text x="95" y="285" class="h1" font-size="112">Perfect For</text><text x="100" y="390" class="body" font-size="44">People building content brands with AI</text>'+feature_box(170,560,1040,620,['Creators','Freelancers','AI Users','Coaches','Influencers','Digital Sellers'],None)+phone(1600,500,480,820)+floating_card(2040,850,470,160,'No camera?','Build a faceless brand')+price_bar()))
slides.append(('etsy-v2-09-bonus.svg', bg(EW,EH)+topbar('BONUS VALUE STACK')+'<text x="95" y="285" class="h1p" font-size="112">BONUS INCLUDED</text><text x="100" y="390" class="body" font-size="44">More than a workbook — a complete creator bundle</text>'+ebook(250,560,520,660,'X Templates','50 posts')+ebook(1080,560,520,660,'YouTube Hooks','30 hooks')+ebook(1910,560,520,660,'IG Captions','30 captions')+floating_card(780,1330,1120,150,'Bonus: Notion Dashboard Style Planner','Use the structure to organize your content workflow')+price_bar()))
slides.append(('etsy-v2-10-faq.svg', bg(EW,EH)+topbar('FAQ + INSTANT DOWNLOAD')+'<text x="95" y="285" class="h1" font-size="112">Before You Buy</text><rect x="160" y="470" width="2380" height="900" rx="42" fill="#050816" stroke="#312e81" stroke-width="4" filter="url(#shadow)"/><text x="260" y="610" class="body" font-size="50">Is this physical?  No — instant digital download.</text><text x="260" y="750" class="body" font-size="50">Do I need design skills?  No — beginner friendly.</text><text x="260" y="890" class="body" font-size="50">Can I customize it?  Yes — copy and edit prompts.</text><text x="260" y="1030" class="body" font-size="50">Does it guarantee income?  No — it gives a system.</text><text x="260" y="1170" class="body" font-size="50">What files?  Workbook, prompts, hooks, templates, captions.</text>'+price_bar()))

outs=[]
for name, body in slides:
    outs.append(write_svg(ETSY/name, body, EW, EH))

# Pinterest 20 pins same style
pin_titles = [
('AI CREATOR KIT','Launch your content brand faster'),('100 AI PROMPTS','Copy, customize, create'),('FACELESS CREATOR KIT','No camera required'),('CONTENT CREATOR TOOLKIT','For beginners using AI'),('YOUTUBE HOOKS','30 short-form ideas'),('SOCIAL MEDIA TEMPLATES','X + Instagram + YouTube'),('CREATOR PLANNER','Plan your brand workflow'),('AI PROMPT PACK','100 copy-paste prompts'),('INSTAGRAM CAPTIONS','Post faster this week'),('X POST TEMPLATES','50 creator frameworks'),('LAUNCH YOUR CONTENT BRAND','Prompt to audience'),('AI TOOLS FOR CREATORS','Create without blank pages'),('DIGITAL PRODUCT FOR CREATORS','Instant PDF download'),('FACELESS CONTENT IDEAS','AI-assisted workflow'),('AI CREATOR GROWTH BUNDLE','Prompts, hooks, captions'),('BUILD AN AI CONTENT BRAND','Beginner-friendly system'),('CREATOR TEMPLATES BUNDLE','Plan, write, post'),('CONTENT WORKFLOW KIT','Prompt → Content → Audience'),('AI SIDE HUSTLE TOOLKIT','Creator brand starter'),('SOCIAL MEDIA PLANNER','Workbook + prompt pack')]
for i,(title,sub) in enumerate(pin_titles,1):
    words=title.split(' ')
    if len(words)>=4: lines=[' '.join(words[:2]), ' '.join(words[2:])]
    elif len(words)==3: lines=[words[0], ' '.join(words[1:])]
    else: lines=[title]
    y0=190
    t=''.join(f'<text x="70" y="{y0+j*90}" class="h1{"p" if j==0 else ""}" font-size="74">{esc(line)}</text>' for j,line in enumerate(lines))
    body=bg(PW,PH)+topbar('DIGITAL DOWNLOAD',PW)+t+f'<text x="72" y="{y0+len(lines)*90+28}" class="body" font-size="32">{esc(sub)}</text>'+feature_box(70,520,860,365,['100 AI Prompts','50 X Templates','30 YouTube Hooks','30 IG Captions'],None)+ebook(165,960,300,360,'AI KIT','PDF')+phone(565,910,270,430)+f'<rect x="70" y="1385" width="360" height="70" rx="35" fill="#facc15"/><text x="112" y="1431" class="dark" font-size="28">GET THE KIT</text>'
    outs.append(write_svg(PINT/f'pinterest-v2-{i:02d}.svg', body, PW, PH))

# Copy into seller V2 kit
for f in sorted(ETSY.glob('etsy-v2-*.png')):
    shutil.copy2(f, SELLER_V2/'01-Etsy-Listing-Images'/f.name)
for f in sorted(PINT.glob('pinterest-v2-*.png')):
    shutil.copy2(f, SELLER_V2/'02-Pinterest-Pins'/f.name)
for src in [ROOT/'06-Etsy-Listing/Etsy-Listing-Copy-Rebranded.md', ROOT/'07-Pinterest/Pinterest-20-Pin-Copy-Rebranded.md']:
    if src.exists(): shutil.copy2(src, SELLER_V2/'03-Listing-Copy'/src.name)
check = SELLER_V2/'04-Upload-Checklist/V2-UPLOAD-CHECKLIST.md'
check.write_text('''# V2 Upload Checklist — GPT Image 2 Reference Style\n\nUse this V2 folder instead of the older orange/purple version.\n\n## Etsy images\n\nUpload 10 images in order: `etsy-v2-01` through `etsy-v2-10`.\n\nAll images are 2700 × 2025.\n\n## Pinterest pins\n\nUse 20 pins: `pinterest-v2-01` through `pinterest-v2-20`.\n\nAll pins are 1000 × 1500.\n\n## Style\n\nHigh-contrast black/navy background, neon purple accent, white typography, yellow offer CTA, right-side product mockups, bottom price bar.\n\n## Buyer ZIP\n\nUse the existing buyer ZIP:\n`AI-Content-Creator-Toolkit-Buyer-Download.zip`\n''')
readme = SELLER_V2/'README-V2.txt'
readme.write_text('Seller Upload Kit V2 — GPT Image 2 reference style. Contains 10 Etsy listing images, 20 Pinterest pins, copy, and checklist. Use this V2 kit for upload.\n')
zip_path = PKG/'AI-Content-Creator-Toolkit-Seller-Upload-Kit-V2-GPT-Image2-Style.zip'
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SELLER_V2.rglob('*')):
        if f.is_file(): z.write(f, f.relative_to(SELLER_V2.parent))
print('\n'.join(map(str, outs)))
print('ZIP', zip_path, zip_path.stat().st_size)
