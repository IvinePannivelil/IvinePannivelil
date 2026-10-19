"""Build the supporting profile SVGs. Python standard library only.

The approved raster is embedded unchanged and framed with SVG viewports.
The activity view reuses intensity levels from the supplied saved snapshot;
it does not fetch new data or reinterpret intensity as contribution counts.
"""
from pathlib import Path
from html import escape
from datetime import date, timedelta
import base64
import hashlib
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'profile-polish' / 'assets'
MASTER = ROOT / 'v4/motion-proof/assets/ivine-approved-arms-folded.png'
EXPECTED = 'a9885b2629713ef3048b98fe9ded0b749c080dd06b4e8ac1e6f4fe0220d52101'
INK, MUTED, CYAN, ORANGE = '#f0f6fc', '#a9bacb', '#00d9ff', '#ff7a00'


def text(x, y, value, size=16, color=INK, weight=400, anchor='start', spacing=0):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}">'
            f'{escape(value)}</text>')


def rect(x, y, w, h, fill='#101a27', stroke='#263748', radius=12):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>'


def wrap(w, h, title, description, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(description)}</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}}</style>
{rect(1, 1, w-2, h-2, '#0b111b', '#263748', 18)}
<path d="M24 1 H{w-24}" stroke="{CYAN}" opacity=".5"/>
{body}</svg>'''


def header(label, width, aside=''):
    return text(24, 34, label.upper(), 11, CYAN, 700, spacing=1.6) + (
        text(width-24, 34, aside.upper(), 10, MUTED, 400, 'end', 1) if aside else '')


def portrait(data, x, y, size):
    # Square viewport around the approved face; original source pixels unchanged.
    return f'''<defs><clipPath id="portrait-clip"><circle cx="{x+size/2}" cy="{y+size/2}" r="{size/2}"/></clipPath></defs>
<circle cx="{x+size/2}" cy="{y+size/2}" r="{size/2+4}" fill="#152333" stroke="{CYAN}" stroke-opacity=".5"/>
<g clip-path="url(#portrait-clip)"><svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="330 0 330 330">
<image x="0" y="0" width="1024" height="1536" href="data:image/png;base64,{data}"/>
</svg></g>'''


PROFILE = [
    ('EDUCATION', 'B.Tech · AI & Data Science', 'Kerala Technological University'),
    ('PORTFOLIO', '4 selected projects', 'Vision · RAG · IIoT · Wearables'),
    ('INTERESTS IN AI', 'CV · RAG · Time series', 'Visual, sensor and tabular data'),
    ('HOW I WORK', 'Evaluate. Explain. Improve.', 'Data quality · Useful applications'),
]


def profile(data, mobile=False):
    w, h = (390, 558) if mobile else (960, 276)
    body = header('Profile at a glance', w, '' if mobile else 'AI / ML / DATA')
    if mobile:
        body += portrait(data, 28, 62, 90)
        body += text(140, 101, 'IVINE P SABU', 21, weight=700)
        body += text(140, 128, 'AI ENGINEER', 12, CYAN, 700, spacing=1)
    else:
        body += portrait(data, 56, 64, 116)
        body += text(114, 218, 'IVINE P SABU', 18, weight=700, anchor='middle')
        body += text(114, 241, 'AI ENGINEER', 11, CYAN, 700, 'middle', 1)
    for i, (label, value, sub) in enumerate(PROFILE):
        x = 20 if mobile else 242 + (i % 2)*350
        y = 174+i*92 if mobile else 64+(i//2)*100
        width, height = (350, 80) if mobile else (332, 88)
        body += rect(x, y, width, height)
        body += text(x+15, y+22, label, 10, MUTED, 700, spacing=1)
        body += text(x+15, y+46, value, 17 if mobile else 18, weight=700)
        body += text(x+15, y+66, sub, 12, MUTED)
    return wrap(w, h, 'Profile at a glance', 'The approved Ivine portrait, education, project areas and working approach.', body)


TOOLS = [
    ('AI & MACHINE LEARNING', 'Python · PyTorch · scikit-learn', 'YOLOv8 · Model evaluation', 'Experiments and model evaluation'),
    ('DATA SCIENCE', 'Pandas · NumPy · SQL', 'EDA · Time-series analysis', 'Explore, clean and interpret data'),
    ('APPLIED AI & GENAI', 'FastAPI · Pinecone', 'RAG · Intent routing', 'Retrieval and agent workflows'),
    ('COMPUTER VISION', 'OpenCV · ByteTrack', 'ONNX Runtime · YOLOv8', 'Tracking, counting and diagnostics'),
    ('SOFTWARE', 'Git · Docker · PyTest', 'React · Next.js', 'APIs, interfaces and automated checks'),
    ('EDGE & DATA SYSTEMS', 'ESP32 · BLE · Flutter', 'InfluxDB · Node-RED · C++', 'Wearables, telemetry and integration'),
]


def tools_panel(mobile=False):
    w,h = (390, 918) if mobile else (960, 382)
    body = header('Tools I use', w, '' if mobile else 'Grouped by workflow')
    for i,(label,a,b,note) in enumerate(TOOLS):
        x = 20 if mobile else 20+(i%3)*312
        y = 60+i*140 if mobile else 60+(i//3)*154
        cw,ch = (350,128) if mobile else (296,138)
        body += rect(x,y,cw,ch)
        body += f'<path d="M{x+16} {y} H{x+60}" stroke="{ORANGE if i==2 else CYAN}"/>'
        body += text(x+16,y+27,label,11,CYAN,700,spacing=.7)
        body += text(x+16,y+56,a,16)
        body += text(x+16,y+80,b,15)
        # The descriptive line has a dedicated smaller size, not a badge claim.
        body += text(x+16,y+108,note,11.5,MUTED)
    return wrap(w,h,'Tools I use','Six groups of tools used across the selected projects and current work.',body)


def interests(mobile=False):
    w,h = (390,354) if mobile else (960,232)
    body=header('Beyond code',w)
    if mobile:
        body += text(24,79,'Machines, roads & stories.',23,weight=700)
        body += text(24,111,'Cars · Bikes',16,MUTED)
        body += text(24,140,'Anime · Movies · Travel',16,MUTED)
        body += f'<path d="M24 174 H366" stroke="#263748"/>'
        body += text(24,210,'A LONGER-TERM CURIOSITY',10,ORANGE,700,spacing=1)
        body += text(24,247,'Where machine learning',21,weight=700)
        body += text(24,277,'meets perception',21,weight=700)
        body += text(24,307,'and automotive systems.',21,weight=700)
    else:
        body += text(24,83,'Machines, roads & stories.',26,weight=700)
        body += text(24,122,'Cars · Bikes',17,MUTED)
        body += text(24,152,'Anime · Movies · Travel',17,MUTED)
        body += f'<path d="M496 62 V202" stroke="#263748"/>'
        body += text(532,83,'A LONGER-TERM CURIOSITY',10,ORANGE,700,spacing=1)
        body += text(532,117,'Where machine learning',21,weight=700)
        body += text(532,147,'meets perception and',21,weight=700)
        body += text(532,177,'automotive systems.',21,weight=700)
        body += text(24,202,'Curiosity beyond the screen.',12,MUTED)
    return wrap(w,h,'Beyond code','Cars, bikes, anime, movies and travel. An interest in machine learning and automotive systems.',body)


def main():
    raw=MASTER.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest != EXPECTED:raise ValueError('Approved master checksum mismatch; stopping.')
    data=base64.b64encode(raw).decode('ascii');OUT.mkdir(parents=True,exist_ok=True)
    for mobile in (False,True):
        suffix='mobile' if mobile else 'desktop'
        for name,svg in [('profile',profile(data,mobile)),('tools',tools_panel(mobile)),('interests',interests(mobile))]:
            ET.fromstring(svg)
            (OUT/f'{name}-{suffix}.svg').write_text(svg,encoding='utf-8')
    footer=wrap(960,76,'Better models. Real impact.','Better models. Real impact.',
                text(480,45,'BETTER MODELS. REAL IMPACT.',15,CYAN,700,'middle',2))
    (OUT/'footer.svg').write_text(footer,encoding='utf-8')
    (OUT/'footer-mobile.svg').write_text(wrap(390,64,'Better models. Real impact.',
        'Better models. Real impact.',text(195,38,'BETTER MODELS. REAL IMPACT.',12.5,CYAN,700,'middle',1)),encoding='utf-8')
    (ROOT/'profile-polish/asset-manifest.json').write_text(json.dumps({
        'approved_source_sha256':digest,'portrait_method':'SVG framing of unchanged full PNG',
        'generated_assets':[
            'profile-desktop.svg', 'profile-mobile.svg',
            'tools-desktop.svg', 'tools-mobile.svg',
            'interests-desktop.svg', 'interests-mobile.svg',
            'footer.svg', 'footer-mobile.svg'
        ],
        'github_render_verified':False
    },indent=2)+'\n',encoding='utf-8')
    print('Built 8 supporting SVGs. Approved source checksum verified.')


if __name__=='__main__':main()
