"""Writes chart.svg.html from chart.json (made by chart.py). Usage: python3 chart_svg.py chart.json chart.svg.html"""
import json, sys
g = json.load(open(sys.argv[1])); p = g['pins']
def pt(k): return round(p[k][0]), round(p[k][1])
mx, my = pt('marina'); ax, ay = pt('ain'); tx, ty = pt('atlantis'); bx, by = pt('burj'); nx, ny = pt('anchor')
svg = f'''<svg class="chart-svg" viewBox="120 -30 960 960" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Typical yacht routes from Dubai Marina</title>
  <desc id="chart-desc">A map of the Dubai coast and Palm Jumeirah showing how far a private charter usually goes in one, two, three or four hours.</desc>
  <rect class="sea" x="-300" y="-500" width="1800" height="1900"/>
  <defs>
    <radialGradient id="palm-fade"><stop offset="0.8" stop-color="#000"/><stop offset="1" stop-color="#fff"/></radialGradient>
    <mask id="open-sea"><rect x="-300" y="-500" width="1800" height="1900" fill="#fff"/><circle cx="468" cy="410" r="300" fill="url(#palm-fade)"/></mask>
  </defs>
  <g class="contours" mask="url(#open-sea)">{''.join(f'<path d="{c}"/>' for c in g['contours'])}</g>
  <path class="land" d="{g['land']}"/>
  <g class="routes">
    <path class="route" data-hours="1" d="{g['r1']}"/>
    <path class="route" data-hours="2" d="{g['r2']}"/>
    <path class="route" data-hours="3" d="{g['r3']}"/>
    <path class="route" data-hours="4" d="{g['r4']}"/>
  </g>
  <g class="marks" aria-hidden="true">
    <g class="mark" transform="translate({ax - 6} {ay - 2})"><circle r="15" class="wheel"/><path class="wheel" d="M-15,0H15M0,-15V15M-10.6,-10.6L10.6,10.6M-10.6,10.6L10.6,-10.6"/></g>
    <g class="mark" transform="translate({bx} {by - 2})"><path class="sail" d="M-3,8 L-3,-26 C9,-20 14,-6 9,8 Z"/></g>
    <g class="mark" transform="translate({tx} {ty - 6})"><path class="atl" d="M-16,10 V-6 H-7 V4 C-7,-6 7,-6 7,4 V-6 H16 V10 Z"/></g>
    <g class="mark anchor" data-min-hours="4" transform="translate({nx} {ny})"><circle r="15"/><path d="M0,-8V8M-6,-4H6M-8,2C-7,8 7,8 8,2" /></g>
    <g class="dock" transform="translate({mx} {my})"><circle r="11"/><circle r="4.5" class="dot"/></g>
  </g>
  <g class="labels" aria-hidden="true">
    <text x="{mx + 18}" y="{my + 20}" class="lbl lbl-strong"><tspan x="{mx + 18}">Dubai</tspan><tspan x="{mx + 18}" dy="1.1em">Marina</tspan></text>
    <text x="505" y="786" class="lbl" text-anchor="middle">JBR</text>
    <text x="{ax - 38}" y="{ay + 68}" class="lbl" text-anchor="middle">Ain Dubai</text>
    <text x="{tx + 18}" y="{ty + 4}" class="lbl">Atlantis</text>
    <text x="{bx + 30}" y="{by + 44}" class="lbl" text-anchor="middle"><tspan x="{bx + 30}">Burj</tspan><tspan x="{bx + 30}" dy="1.1em">Al Arab</tspan></text>
    <text x="572" y="502" class="lbl land-lbl" text-anchor="middle" transform="rotate(46 572 502)">Palm Jumeirah</text>
    <text x="700" y="60" class="lbl water-lbl">Arabian Gulf</text>
    <text x="{nx - 22}" y="{ny + 34}" class="lbl anchor-lbl" data-min-hours="4" text-anchor="end">Swim stop</text>
  </g>
  <text x="790" y="640" class="lbl city-lbl">Dubai</text>
  <g class="scale" transform="translate(880 470)" aria-hidden="true"><path d="M0,0H90M0,-6V6M90,-6V6"/><text x="45" y="-12" text-anchor="middle">1 km</text></g>
</svg>'''
open(sys.argv[2], 'w').write(svg); print(len(svg), 'bytes')
