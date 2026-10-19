"""Reproducible SVG composition. Python 3 standard library only.

The approved raster is immutable. SVG clipping assigns DIFFERENT visible
regions to head and body. Only the head group receives the idle transform.
This is a conservative 2D rig, not a fully articulated character.
"""
from pathlib import Path
import base64
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SOURCE = ASSETS / 'ivine-approved-arms-folded.png'

# Source coordinates: 1024 x 1536. Follow the rear hair and neck closely so
# the source's blue background is not carried into the character cutout.
# Head includes beard/neck; body overlaps the bottom neck for tiny rotations.
HEAD = ('M 379,91 C 377,69 394,48 418,42 C 441,31 465,34 479,39 '
        'C 505,26 533,36 546,41 C 567,44 586,59 588,81 '
        'C 591,99 581,120 575,140 Q 580,147 577,167 '
        'C 574,188 565,199 558,206 Q 563,216 557,226 '
        'L 557,242 L 550,275 L 527,305 Q 503,323 478,312 '
        'L 441,290 L 435,267 C 421,254 420,239 415,224 '
        'L 408,191 L 407,151 L 398,124 Q 384,112 379,91 Z')
BODY = ('M 440,285 Q 479,308 510,308 L 551,267 '
        'Q 563,271 577,281 L 615,301 Q 653,311 681,331 '
        'Q 714,355 719,396 L 721,450 Q 715,483 690,518 '
        'L 679,563 L 680,628 L 684,701 L 686,758 '
        'L 695,802 L 714,873 L 717,934 L 728,998 L 739,1059 '
        'L 753,1125 L 768,1184 L 781,1248 L 801,1294 '
        'L 799,1320 L 791,1362 Q 812,1386 806,1427 '
        'L 793,1472 Q 777,1501 741,1504 L 691,1502 '
        'Q 665,1496 651,1482 L 650,1454 L 660,1415 L 680,1370 '
        'L 684,1326 L 666,1296 L 649,1238 L 626,1184 '
        'L 605,1122 L 584,1054 L 560,998 L 533,943 '
        'L 511,900 L 506,961 L 512,1025 L 522,1088 '
        'L 536,1146 L 544,1197 L 550,1249 L 557,1299 '
        'L 553,1330 L 545,1350 Q 551,1371 547,1409 '
        'L 541,1432 Q 523,1448 480,1452 L 403,1446 '
        'L 332,1438 Q 306,1434 304,1417 L 309,1392 '
        'Q 327,1371 368,1359 L 417,1329 L 419,1316 '
        'L 402,1290 L 396,1258 L 399,1228 L 392,1194 '
        'L 383,1142 L 374,1094 L 366,1036 L 359,983 '
        'L 352,936 L 342,894 L 343,840 L 349,801 L 347,778 '
        'L 319,760 L 314,742 L 327,690 L 341,638 L 357,587 '
        'Q 320,586 300,567 L 283,536 Q 272,515 274,490 '
        'L 286,448 L 295,403 Q 303,366 323,345 '
        'Q 356,324 399,310 L 440,285 Z')

def artwork_defs(data):
    return f'''<defs>
      <image id="approved-art" x="0" y="0" width="1024" height="1536" href="data:image/png;base64,{data}"/>
      <clipPath id="head-region" clipPathUnits="userSpaceOnUse"><path d="{HEAD}"/></clipPath>
      <clipPath id="body-region" clipPathUnits="userSpaceOnUse"><path d="{BODY}"/></clipPath>
      <filter id="hair-rim-tone" x="0" y="0" width="1024" height="1536" filterUnits="userSpaceOnUse" color-interpolation-filters="sRGB">
        <feColorMatrix type="saturate" values=".12"/>
        <feComponentTransfer><feFuncR type="linear" slope=".8"/><feFuncG type="linear" slope=".8"/><feFuncB type="linear" slope=".8"/></feComponentTransfer>
      </filter>
      <linearGradient id="hair-rim-fade" gradientUnits="userSpaceOnUse" x1="514" y1="0" x2="580" y2="0">
        <stop offset="0" stop-color="black"/><stop offset=".52" stop-color="#666"/><stop offset="1" stop-color="#eee"/>
      </linearGradient>
      <mask id="hair-rim-mask" maskUnits="userSpaceOnUse" x="500" y="20" width="104" height="124">
        <path d="M505 26 Q550 24 588 57 L600 100 L578 143 L567 135 L553 113 Q553 83 535 61 L505 45 Z" fill="url(#hair-rim-fade)"/>
      </mask>
    </defs>'''

def rig(layer='both'):
    body = '''<g id="body" clip-path="url(#body-region)"><use href="#approved-art"/></g>'''
    # Local SVG colour treatment only on the blue rear-hair rim; the original
    # raster, face, beard, clothing, body and motion transforms are unchanged.
    head = '''<g id="head-pivot" class="head-idle"><g id="head" clip-path="url(#head-region)"><use href="#approved-art"/><use href="#approved-art" filter="url(#hair-rim-tone)" mask="url(#hair-rim-mask)"/></g></g>'''
    # A neck-sized underlap is behind both raster regions, never on the face.
    underlap = '<path id="neck-underlap" d="M445 281 Q489 305 550 274 L535 315 L482 326 L443 303 Z" fill="#734a3b"/>'
    return (underlap + body + head) if layer == 'both' else (head if layer == 'head' else body)

def css(animated):
    if not animated:
        return '<style>.head-idle{transform:none}</style>'
    return '''<style>
      .head-idle{transform-box:view-box;transform-origin:493px 292px;animation:headIdle 7s ease-in-out 1.2s infinite}
      .entrance{animation:arrive .8s ease-out both}
      .trace{stroke-dasharray:8 180;animation:trace 6s linear infinite}
      @keyframes arrive{from{opacity:.35;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}
      @keyframes headIdle{0%,20%,100%{transform:rotate(0deg)}45%{transform:rotate(-.65deg)}70%{transform:rotate(.35deg)}}
      @keyframes trace{to{stroke-dashoffset:-188}}
      @media(prefers-reduced-motion:reduce){.head-idle,.entrance,.trace{animation:none!important;transform:none!important;opacity:1!important}}
    </style>'''

def hero(data, mobile=False, animated=True):
    w, h = (390, 650) if mobile else (960, 540)
    text = '''<text x="48" y="76" class="eyebrow">AI / DATA / APPLIED SYSTEMS</text>
      <text x="46" y="166" class="name">IVINE P SABU</text>
      <text x="49" y="207" class="role">AI ENGINEER</text>
      <text x="49" y="249" class="focus">Machine Learning · Data Science · Applied AI</text>
      <text x="49" y="311" class="summary">Building practical intelligent systems</text>
      <text x="49" y="341" class="summary">from real-world data.</text>
      <path d="M50 395 H125 L143 377 H280 L298 395 H450" stroke="#254253" fill="none"/>
      <path class="trace" d="M50 395 H125 L143 377 H280 L298 395 H450" stroke="#00d9ff" fill="none"/>
      <text x="49" y="472" class="caption">BETTER MODELS. REAL IMPACT.</text>'''
    placement = 'translate(590 15) scale(.337)'
    if mobile:
        placement = 'translate(29 225) scale(.265)'
        text = '''<text x="24" y="38" class="eyebrow">AI / DATA / APPLIED SYSTEMS</text>
          <text x="22" y="93" class="name">IVINE P SABU</text>
          <text x="24" y="128" class="role">AI ENGINEER</text>
          <text x="24" y="163" class="focus">Machine Learning · Data Science</text>
          <text x="24" y="187" class="focus">Applied AI</text>
          <text x="24" y="221" class="summary">Intelligent systems. Real-world data.</text>'''
    styles = '''<style>text{font-family:Arial,Helvetica,sans-serif}.eyebrow{font-size:12px;letter-spacing:2px;fill:#79a4b8}.name{font-size:49px;font-weight:700;letter-spacing:-1px;fill:#f0f6fc}.role{font-size:21px;font-weight:700;letter-spacing:3px;fill:#00d9ff}.focus{font-size:15px;fill:#bdcbd5}.summary{font-size:23px;fill:#d4dee6}.caption{font-size:12px;letter-spacing:2px;fill:#a6b4c1}</style>'''
    if mobile:
        styles = styles.replace('font-size:49px','font-size:37px').replace('font-size:23px','font-size:16px').replace('font-size:12px;letter-spacing:2px;fill:#79','font-size:10px;letter-spacing:1.5px;fill:#79')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-labelledby="title desc">
      <title id="title">Ivine P Sabu — AI Engineer</title>
      <desc id="desc">Machine Learning, Data Science and Applied AI. Approved arms-folded character with a subtle head tilt. The face and body come from the unchanged approved artwork.</desc>
      {artwork_defs(data)}{styles}{css(animated)}
      <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="22" fill="#0b111b" stroke="#263748"/>
      <path d="M24 2 H{w-24}" stroke="#00d9ff" opacity=".65"/>
      {text}
      <g id="character-placement" transform="{placement}"><g class="entrance" id="character-entrance">{rig()}</g></g>
    </svg>'''

def layer_svg(data, layer):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1536" width="1024" height="1536"><title>{layer} region of approved character</title>{artwork_defs(data)}{rig(layer)}</svg>'

def main():
    data = base64.b64encode(SOURCE.read_bytes()).decode('ascii')
    for mobile in (False, True):
        for animated in (True, False):
            name = 'hero-' + ('mobile' if mobile else 'desktop') + ('' if animated else '-static') + '.svg'
            (ASSETS / name).write_text(hero(data, mobile, animated), encoding='utf-8')
    for layer in ('head', 'body'):
        (ASSETS / f'{layer}-region.svg').write_text(layer_svg(data, layer), encoding='utf-8')
    (ROOT / 'asset-manifest.json').write_text(json.dumps({
        'approved_source': 'assets/' + SOURCE.name,
        'approved_source_sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
        'source_dimensions': [1024,1536],
        'method': 'Immutable raster with head/body SVG clips, neck underlap and a local SVG rear-hair rim colour treatment',
        'revision': 'Reduced blue halo behind hair; tighter rear-head and neck clip; face and body unfiltered',
        'head_pivot': [493,292], 'idle_rotation_degrees': [-0.65,0.35],
        'idle_period_seconds': 7,
        'scope': 'Arms-folded entrance and head-only idle. No independent arm, blink or breathing claim.',
        'github_render_verified': False
    }, indent=2)+'\n', encoding='utf-8')
    print('Built desktop/mobile motion, static alternatives and separate head/body SVG regions.')

if __name__ == '__main__':
    main()
