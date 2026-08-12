from pathlib import Path
import subprocess, zipfile, shutil

ROOT = Path('/sources/AI-Virtual-Influencer-Starter-Kit')
ETSY = ROOT / '06-Etsy-Listing' / 'v3-reference-grid-style'
PINT = ROOT / '07-Pinterest' / 'v3-reference-grid-style'
PKG = ROOT / '08-Launch-Package'
SELLER = PKG / 'Seller-Upload-Kit-V3-Reference-Grid-Style'
for p in [ETSY, PINT, SELLER/'01-Etsy-Listing-Images', SELLER/'02-Pinterest-Pins', SELLER/'03-Listing-Copy', SELLER/'04-Upload-Checklist']:
    p.mkdir(parents=True, exist_ok=True)

EW, EH = 2700, 2025
PW, PH = 1000, 1500

CSS = """
.h1{font-family:Arial Black,Arial,sans-serif;font-weight:900;letter-spacing:-5px;fill:#fff}
.ai{font-family:Arial Black,Arial,sans-serif;font-weight:900;letter-spacing:-5px;fill:#b45cff}
.h2{font-family:Arial Black,Arial,sans-serif;font-weight:900;fill:#fff}
.body{font-family:Arial,Helvetica,sans-serif;font-weight:800;fill:#eef2ff}
.muted{font-family:Arial,Helvetica,sans-serif;font-weight:700;fill:#a5b4fc}
.purple{font-family:Arial Black,Arial,sans-serif;font-weight:900;fill:#b45cff}
.orange{font-family:Arial Black,Arial,sans-serif;font-weight:900;fill:#ffb703}
.dark{font-family:Arial Black,Arial,sans-serif;font-weight:900;fill:#080816}
.small{font-family:Arial,Helvetica,sans-serif;font-weight:900;fill:#fff}
"""

def esc(s):
    return str(s).replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')

def defs():
    return '''<defs>
      <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#03030b"/><stop offset="0.42" stop-color="#0b1025"/><stop offset="1" stop-color="#2b075e"/></linearGradient>
      <radialGradient id="violet" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#b45cff" stop-opacity=".9"/><stop offset="1" stop-color="#b45cff" stop-opacity="0"/></radialGradient>
      <linearGradient id="sunset" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7c3aed"/><stop offset=".55" stop-color="#f97316"/><stop offset="1" stop-color="#111827"/></linearGradient>
      <linearGradient id="panel" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#17122d"/><stop offset="1" stop-color="#050713"/></linearGradient>
      <filter id="shadow" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="0" dy="24" stdDeviation="26" flood-color="#000" flood-opacity=".58"/></filter>
      <filter id="glow" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="42"/></filter>
      <filter id="neon" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="10" flood-color="#b45cff" flood-opacity=".9"/></filter>
    </defs>'''

def bg(w,h):
    return f'''<rect width="100%" height="100%" fill="url(#bg)"/>
      <circle cx="{w*.74}" cy="{h*.25}" r="{w*.26}" fill="url(#violet)" filter="url(#glow)" opacity=".88"/>
      <circle cx="{w*.13}" cy="{h*.83}" r="{w*.22}" fill="#7c3aed" filter="url(#glow)" opacity=".32"/>
      <path d="M0,{h*.86} C{w*.23},{h*.76} {w*.55},{h*.96} {w},{h*.78} L{w},{h} L0,{h}Z" fill="#050713" opacity=".78"/>'''

def top_offer(w, price='$14.99'):
    return f'''<rect x="70" y="54" width="720" height="68" rx="34" fill="#0a0a18" stroke="#7c3aed" stroke-width="2"/>
      <text x="108" y="99" class="small" font-size="28">DIGITAL DOWNLOAD  |  LAUNCH OFFER </text>
      <text x="665" y="99" class="orange" font-size="30">{price}</text>'''

def check_list(x,y,items,fs=40,gap=68):
    s=''
    for i,it in enumerate(items):
        yy=y+i*gap
        s += f'<circle cx="{x}" cy="{yy-12}" r="21" fill="#2b075e" stroke="#b45cff" stroke-width="3"/><text x="{x-12}" y="{yy}" class="purple" font-size="31">✓</text><text x="{x+48}" y="{yy}" class="body" font-size="{fs}">{esc(it)}</text>'
    return s

def card(x,y,w,h,title,body='',accent='#b45cff',fs=30):
    lines = body if isinstance(body, list) else ([body] if body else [])
    text = f'<text x="{x+28}" y="{y+55}" class="small" font-size="{fs}">{esc(title)}</text>'
    for i,line in enumerate(lines[:4]):
        text += f'<text x="{x+28}" y="{y+100+i*36}" class="muted" font-size="24">{esc(line)}</text>'
    return f'<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="24" fill="url(#panel)" stroke="{accent}" stroke-width="3"/>{text}</g>'

def book(x,y,w,h,title='AI CREATOR KIT',sub='Launch Your Content Brand Faster'):
    return f'''<g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="#f8fafc"/>
      <rect x="{x+26}" y="{y+26}" width="{w-52}" height="{h-52}" rx="18" fill="#0b1025"/>
      <rect x="{x+50}" y="{y+190}" width="{w-100}" height="{h-300}" rx="20" fill="url(#sunset)"/>
      <circle cx="{x+w*.67}" cy="{y+270}" r="62" fill="#facc15" opacity=".7"/>
      <circle cx="{x+w*.52}" cy="{y+h-190}" r="54" fill="#050713"/><rect x="{x+w*.48}" y="{y+h-145}" width="90" height="135" rx="38" fill="#050713"/>
      <text x="{x+48}" y="{y+90}" class="ai" font-size="42">AI</text><text x="{x+120}" y="{y+90}" class="small" font-size="40">CREATOR KIT</text>
      <text x="{x+48}" y="{y+140}" class="muted" font-size="22">{esc(sub)}</text>
      <rect x="{x+50}" y="{y+h-82}" width="{w-100}" height="48" rx="24" fill="#b45cff"/>
      <text x="{x+96}" y="{y+h-50}" class="small" font-size="22">INSTANT DOWNLOAD</text>
    </g>'''

def laptop(x,y,w,h):
    return f'''<g filter="url(#shadow)">
      <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#0b1025" stroke="#4c1d95" stroke-width="5"/>
      <rect x="{x+35}" y="{y+48}" width="{w-70}" height="{h-95}" rx="18" fill="#111827"/>
      <text x="{x+70}" y="{y+105}" class="small" font-size="26">Creator OS Dashboard</text>
      <rect x="{x+70}" y="{y+145}" width="{w-140}" height="74" rx="16" fill="#2b075e"/><text x="{x+95}" y="{y+192}" class="purple" font-size="26">Today’s Focus: Plan → Create → Post</text>
      <rect x="{x+70}" y="{y+250}" width="{(w-170)/2}" height="116" rx="18" fill="#172554"/><text x="{x+95}" y="{y+315}" class="small" font-size="24">Content Pipeline</text>
      <rect x="{x+95+(w-170)/2}" y="{y+250}" width="{(w-170)/2}" height="116" rx="18" fill="#312e81"/><text x="{x+125+(w-170)/2}" y="{y+315}" class="small" font-size="24">Content Calendar</text>
      <rect x="{x+80}" y="{y+h-10}" width="{w-160}" height="34" rx="17" fill="#0f172a"/>
    </g>'''

def phone(x,y,w,h):
    return f'''<g filter="url(#shadow)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="42" fill="#030712" stroke="#64748b" stroke-width="6"/>
      <rect x="{x+25}" y="{y+58}" width="{w-50}" height="{h-92}" rx="28" fill="#111827"/>
      <text x="{x+45}" y="{y+120}" class="small" font-size="22">Social Post</text>
      <rect x="{x+45}" y="{y+155}" width="{w-90}" height="108" rx="18" fill="#2b075e"/><text x="{x+64}" y="{y+215}" class="purple" font-size="24">Hook + Caption</text>
      <rect x="{x+45}" y="{y+295}" width="{w-90}" height="30" rx="12" fill="#334155"/><rect x="{x+45}" y="{y+345}" width="{w-130}" height="30" rx="12" fill="#334155"/>
    </g>'''

def price_bar(w=EW,h=EH):
    return f'''<rect x="0" y="{h-170}" width="{w}" height="170" fill="#070716"/>
      <rect x="88" y="{h-132}" width="420" height="88" rx="44" fill="#b45cff" filter="url(#neon)"/><text x="142" y="{h-74}" class="small" font-size="38">50% OFF TODAY</text>
      <text x="650" y="{h-62}" class="orange" font-size="76">$14.99</text><text x="940" y="{h-68}" class="muted" font-size="38">$29.99</text><line x1="936" y1="{h-82}" x2="1084" y2="{h-104}" stroke="#a5b4fc" stroke-width="5"/>
      <rect x="{w-620}" y="{h-126}" width="505" height="78" rx="39" fill="#0b1025" stroke="#facc15" stroke-width="3"/><text x="{w-582}" y="{h-75}" class="orange" font-size="30">7-DAY MONEY BACK GUARANTEE ★★★★★</text>'''

def benefit_row(y):
    benefits=['Instant Download','Beginner Friendly','Lifetime Access','Commercial Use','Works with AI Tools','Bonus Templates']
    s=''
    for i,b in enumerate(benefits):
        x=120+i*415
        s += f'<rect x="{x}" y="{y}" width="350" height="95" rx="28" fill="#0b1025" stroke="#4c1d95" stroke-width="2"/><text x="{x+25}" y="{y+58}" class="small" font-size="27">✓ {esc(b)}</text>'
    return s

def write_svg(path, body, w, h):
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><style>{CSS}</style>{defs()}{body}</svg>'
    path.write_text(svg)
    png = path.with_suffix('.png')
    subprocess.run(['rsvg-convert','-w',str(w),'-h',str(h),str(path),'-o',str(png)], check=True)
    return png

items=['100 AI Prompts','50 X (Twitter) Templates','30 YouTube Hooks','30 Instagram Captions','Workbook & Planner','BONUS: Notion Dashboard']
slides=[]
slides.append(('etsy-v3-01-main-value.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="88" y="270" class="ai" font-size="150">AI</text><text x="286" y="270" class="h1" font-size="150"> CREATOR KIT</text>'+
    '<text x="96" y="380" class="h2" font-size="62">Launch Your Content Brand <tspan fill="#b45cff">Faster</tspan></text>'+
    '<text x="98" y="465" class="body" font-size="36">Everything You Need to Create, Grow &amp; Monetize Your Faceless Content Brand</text>'+
    check_list(128,620,items,41,76)+book(1060,380,480,660)+laptop(1290,1085,760,430)+phone(2090,830,330,565)+
    card(1760,360,620,170,'100 AI Prompts',['Selfie prompts','Travel prompts','Brand prompts'])+card(1800,570,580,150,'30 YouTube Hooks',['Short-form video ideas'])+card(1565,760,490,145,'50 X Templates',['Authority post frameworks'])+benefit_row(1695)+price_bar()))
slides.append(('etsy-v3-02-whats-inside.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="h1" font-size="118">WHAT’S INSIDE</text><text x="96" y="380" class="body" font-size="42">A complete starter stack for AI-assisted content creation</text>'+
    card(120,520,760,250,'1. 100 AI Prompts',['Selfie, lifestyle, travel, brand scenes'])+card(970,520,760,250,'2. 50 X Templates',['Hooks, threads, authority posts'])+card(1820,520,760,250,'3. 30 YouTube Hooks',['Shorts, Reels and TikTok ideas'])+
    card(120,860,760,250,'4. 30 Instagram Captions',['Lifestyle, creator and motivation captions'])+card(970,860,760,250,'5. Workbook & Planner',['Niche, offer, workflow and calendar'])+card(1820,860,760,250,'6. Bonus Dashboard',['Notion-style content operating system'])+
    book(420,1215,330,430,'Workbook','Planner')+book(890,1215,330,430,'Prompts','100 ideas')+book(1360,1215,330,430,'X Posts','50 templates')+book(1830,1215,330,430,'Hooks','30 video hooks')+price_bar()))
slides.append(('etsy-v3-03-prompt-pack-preview.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="ai" font-size="112">100 AI PROMPTS</text><text x="96" y="380" class="body" font-size="42">No more blank-page content planning</text>'+
    card(130,520,2440,800,'Prompt Preview',['Create a realistic lifestyle photo of [creator name], a [niche] creator,','modern coffee shop, premium editorial light, consistent face,','social-media-ready framing, cinematic purple/orange color grade.'], '#b45cff',42)+
    card(270,1390,610,170,'Selfie Prompts',['Personal-brand image ideas'])+card(1045,1390,610,170,'Travel Prompts',['Location-based content scenes'])+card(1820,1390,610,170,'Brand Prompts',['Creator offer visuals'])+price_bar()))
slides.append(('etsy-v3-04-template-previews.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="h1" font-size="112">TEMPLATES THAT SELL THE IDEA</text><text x="96" y="380" class="body" font-size="42">X posts, hooks and captions buyers can use immediately</text>'+
    card(130,540,760,560,'50 X Templates',['I spent [timeframe] testing [workflow].','Here are [number] lessons nobody tells you:','1. [Lesson]  2. [Lesson]  3. [Lesson]'])+
    card(970,540,760,560,'30 YouTube Hooks',['“I built an AI content brand in 7 days.”','“Steal this prompt system for 30 posts.”','“Nobody talks about this AI workflow.”'])+
    card(1810,540,760,560,'30 IG Captions',['Somewhere between work and adventure.','Building quietly, posting consistently.','More signal. Less noise. More creation.'])+laptop(680,1230,880,430)+phone(1670,1180,300,480)+price_bar()))
slides.append(('etsy-v3-05-dashboard-workbook.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="ai" font-size="108">WORKBOOK + DASHBOARD</text><text x="96" y="380" class="body" font-size="42">Turn scattered ideas into a repeatable content system</text>'+
    laptop(185,555,1050,610)+book(1430,500,450,660,'AI CREATOR','Workbook')+phone(2030,610,330,565)+
    card(260,1270,620,170,'Plan Your Niche',['Audience, pillars, offer angle'])+card(1040,1270,620,170,'Build Your Pipeline',['Idea → Draft → Publish'])+card(1820,1270,620,170,'Track Consistency',['Today’s focus + calendar'])+price_bar()))
slides.append(('etsy-v3-06-who-for.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="h1" font-size="118">PERFECT FOR</text><text x="96" y="380" class="body" font-size="42">Creators building faster with AI tools</text>'+
    check_list(170,590,['Faceless creators','Freelancers','Coaches','Digital product sellers','AI tool beginners','Influencers testing new niches'],54,105)+
    book(1450,500,500,690)+card(2010,665,450,190,'No Camera?',['Use prompts to create a','faceless brand workflow'])+card(2010,920,450,190,'No Strategy?',['Use the planner to map','repeatable content'])+price_bar()))
slides.append(('etsy-v3-07-offer-stack.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="ai" font-size="112">VALUE STACK</text><text x="96" y="380" class="body" font-size="42">Make the offer feel bigger than a simple PDF</text>'+
    book(150,540,390,520,'Prompt Pack','100 prompts')+book(650,540,390,520,'X Templates','50 posts')+book(1150,540,390,520,'Hooks','30 ideas')+book(1650,540,390,520,'Captions','30 captions')+book(2150,540,390,520,'Workbook','Planner')+
    card(370,1210,1960,230,'BONUS: Notion Dashboard Style Planner',['Organize content ideas, content calendar, publishing focus and experiment tracking.'],'#facc15',44)+benefit_row(1530)+price_bar()))
slides.append(('etsy-v3-08-instant-download.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="h1" font-size="112">INSTANT DIGITAL DOWNLOAD</text><text x="96" y="380" class="body" font-size="42">No shipping. No subscription. Start using it after purchase.</text>'+
    card(180,600,660,360,'1. Buy on Etsy',['Download the ZIP files from your Etsy account'])+card(1020,600,660,360,'2. Open the PDFs',['Read the workbook and copy templates'])+card(1860,600,660,360,'3. Create Content',['Use prompts, hooks and captions in your workflow'])+
    laptop(350,1120,900,430)+phone(1445,1060,315,520)+book(1900,1040,360,500,'AI KIT','PDF Bundle')+price_bar()))
slides.append(('etsy-v3-09-guarantee-faq.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="285" class="ai" font-size="112">FAQ + GUARANTEE</text><text x="96" y="380" class="body" font-size="42">Clear buying confidence for digital-product shoppers</text>'+
    card(150,540,2400,760,'Before You Buy',['Is this physical? No — instant digital download.','Do I need design skills? No — beginner friendly.','Can I customize it? Yes — copy and edit the prompts/templates.','Does it guarantee income? No — it gives a planning system.'],'#b45cff',44)+
    card(430,1390,760,170,'7-Day Money Back',['Buyer-friendly confidence badge'],'#facc15')+card(1510,1390,760,170,'One-Time Payment',['No subscription required'],'#facc15')+price_bar()))
slides.append(('etsy-v3-10-carousel-overview.svg', bg(EW,EH)+top_offer(EW)+
    '<text x="92" y="260" class="h1" font-size="100">AI CREATOR GROWTH BUNDLE</text><text x="96" y="345" class="body" font-size="38">Prompts, templates, hooks, captions and planner for content creators</text>'+
    card(115,455,470,265,'01 Main Offer',['High-converting cover image'])+card(625,455,470,265,'02 What’s Inside',['Six-part bundle overview'])+card(1135,455,470,265,'03 Prompts',['100 AI prompt preview'])+card(1645,455,470,265,'04 Templates',['X, YouTube, IG examples'])+card(2155,455,430,265,'05 Planner',['Dashboard + workbook'])+
    card(115,805,470,265,'06 Who For',['Buyer personas'])+card(625,805,470,265,'07 Value Stack',['Bundle value perception'])+card(1135,805,470,265,'08 Download',['Instant digital product'])+card(1645,805,470,265,'09 FAQ',['Guarantee + disclaimers'])+card(2155,805,430,265,'10 Overview',['Upload-ready carousel'])+
    book(620,1235,360,470)+laptop(1110,1285,760,360)+price_bar()))

outs=[]
for name, body in slides:
    outs.append(write_svg(ETSY/name, body, EW, EH))

pin_titles=[
('AI CREATOR KIT','Launch your content brand faster'),('AI CREATOR GROWTH BUNDLE','Prompts, templates, hooks, captions'),('100 AI PROMPTS','Copy, customize, create'),('FACELESS CREATOR KIT','No camera required'),('CONTENT CREATOR TOOLKIT','For beginners using AI'),('YOUTUBE HOOKS','30 short-form ideas'),('SOCIAL MEDIA TEMPLATES','X + Instagram + YouTube'),('CREATOR PLANNER','Plan your brand workflow'),('AI PROMPT PACK','100 copy-paste prompts'),('INSTAGRAM CAPTIONS','Post faster this week'),('X POST TEMPLATES','50 creator frameworks'),('LAUNCH YOUR CONTENT BRAND','Prompt to audience'),('AI TOOLS FOR CREATORS','Create without blank pages'),('DIGITAL PRODUCT FOR CREATORS','Instant PDF download'),('FACELESS CONTENT IDEAS','AI-assisted workflow'),('BUILD AN AI CONTENT BRAND','Beginner-friendly system'),('CREATOR TEMPLATES BUNDLE','Plan, write, post'),('CONTENT WORKFLOW KIT','Prompt → Content → Audience'),('AI SIDE HUSTLE TOOLKIT','Creator brand starter'),('SOCIAL MEDIA PLANNER','Workbook + prompt pack')]
for i,(title,sub) in enumerate(pin_titles,1):
    words=title.split()
    if len(words)>=4:
        lines=[' '.join(words[:2]), ' '.join(words[2:])]
    elif len(words)==3:
        lines=[words[0], ' '.join(words[1:])]
    else:
        lines=[title]
    t=''.join(f'<text x="62" y="{210+j*86}" class="{"ai" if j==0 else "h1"}" font-size="72">{esc(line)}</text>' for j,line in enumerate(lines))
    body=bg(PW,PH)+top_offer(PW)+t+f'<text x="66" y="{235+len(lines)*86}" class="body" font-size="30">{esc(sub)}</text>'+card(65,500,870,320,'Included',['100 AI Prompts','50 X Templates','30 YouTube Hooks','30 IG Captions'],'#b45cff',34)+book(95,895,300,385)+laptop(415,980,455,250)+phone(715,850,190,330)+f'<rect x="65" y="1378" width="410" height="74" rx="37" fill="#b45cff" filter="url(#neon)"/><text x="112" y="1426" class="small" font-size="30">GET THE KIT</text><text x="575" y="1428" class="orange" font-size="44">$14.99</text>'
    outs.append(write_svg(PINT/f'pinterest-v3-{i:02d}.svg', body, PW, PH))

# Copy into seller kit
for f in sorted(ETSY.glob('etsy-v3-*.png')):
    shutil.copy2(f, SELLER/'01-Etsy-Listing-Images'/f.name)
for f in sorted(PINT.glob('pinterest-v3-*.png')):
    shutil.copy2(f, SELLER/'02-Pinterest-Pins'/f.name)
for src in [ROOT/'06-Etsy-Listing/Etsy-Listing-Copy-Rebranded.md', ROOT/'07-Pinterest/Pinterest-20-Pin-Copy-Rebranded.md']:
    if src.exists():
        shutil.copy2(src, SELLER/'03-Listing-Copy'/src.name)
(SELLER/'04-Upload-Checklist/V3-UPLOAD-CHECKLIST.md').write_text('''# V3 Upload Checklist — Reference Grid Style

Use this V3 folder as the strongest current visual set.

## Etsy images
Upload 10 images in order: `etsy-v3-01` through `etsy-v3-10`.

All images are 2700 × 2025.

## Pinterest pins
Use 20 pins: `pinterest-v3-01` through `pinterest-v3-20`.

All pins are 1000 × 1500.

## Style
Dense premium digital-product ad style inspired by the latest reference images: black/navy background, purple neon glow, orange/yellow offer price, product book/laptop/phone mockups, checklist blocks, value-stack cards, bottom discount and guarantee bar.

## Buyer ZIP
Use the existing buyer ZIP:
`AI-Content-Creator-Toolkit-Buyer-Download.zip`
''')
(SELLER/'README-V3.txt').write_text('Seller Upload Kit V3 — Reference Grid Style. Contains 10 Etsy listing images, 20 Pinterest pins, listing copy, and upload checklist. Use this V3 kit for upload.\n')
zip_path = PKG/'AI-Content-Creator-Toolkit-Seller-Upload-Kit-V3-Reference-Grid-Style.zip'
if zip_path.exists():
    zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(SELLER.rglob('*')):
        if f.is_file():
            z.write(f, f.relative_to(SELLER.parent))
print('\n'.join(str(p) for p in outs))
print('ZIP', zip_path, zip_path.stat().st_size)
