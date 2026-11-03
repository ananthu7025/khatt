import json,sys
g=json.load(open(sys.argv[1])); p=g['pins']
def pt(k): return p[k][0],p[k][1]
mx,my=pt('marina'); ax,ay=pt('ain'); tx,ty=pt('atlantis'); bx,by=pt('burj'); nx,ny=pt('anchor')
sound=[(300,640,'6'),(360,470,'9'),(250,330,'14'),(470,150,'17'),(640,170,'12'),(760,170,'11'),(210,540,'16'),(560,620,'5'),(860,160,'8'),(410,690,'7')]
svg=f'''<svg class="chart-svg" viewBox="180 40 990 960" preserveAspectRatio="xMidYMid meet" role="img" aria-labelledby="chart-title chart-desc">
  <title id="chart-title">Typical yacht routes from Dubai Marina</title>
  <desc id="chart-desc">A map of the Dubai coast showing how far a private charter usually goes in one, two, three or four hours.</desc>
  <rect class="sea" x="0" y="-100" width="1400" height="1300"/>
  <g class="contours">{''.join(f'<path d="{c}"/>' for c in g['contours'])}</g>
  <g class="soundings" aria-hidden="true">{''.join(f'<text x="{x}" y="{y}">{t}</text>' for x,y,t in sound)}</g>
  <path class="land" d="{g['land']}"/>
  <g class="palm" aria-hidden="true">
    <path class="palm-edge" d="{g['crescent']}"/><path class="palm-edge" d="{g['trunk']}"/><path class="palm-edge frond" d="{' '.join(g['fronds'])}"/>
    <path class="palm-fill" d="{g['crescent']}"/><path class="palm-fill" d="{g['trunk']}"/><path class="palm-fill frond" d="{' '.join(g['fronds'])}"/>
  </g>
  <ellipse class="land islet" cx="368" cy="796" rx="36" ry="19" transform="rotate(-38 368 796)"/>
  <circle class="land islet" cx="{bx:.0f}" cy="{by:.0f}" r="11"/>
  <g class="routes">
    <path class="route" data-hours="1" d="{g['r1']}"/>
    <path class="route" data-hours="2" d="{g['r2']}"/>
    <path class="route" data-hours="3" d="{g['r3']}"/>
    <path class="route" data-hours="4" d="{g['r4']}"/>
  </g>
  <g class="marks" aria-hidden="true">
    <g class="mark" transform="translate({ax-6:.0f} {ay-2:.0f})"><circle r="15" class="wheel"/><path class="wheel" d="M-15,0H15M0,-15V15M-10.6,-10.6L10.6,10.6M-10.6,10.6L10.6,-10.6"/></g>
    <g class="mark" transform="translate({bx:.0f} {by-2:.0f})"><path class="sail" d="M-3,8 L-3,-26 C9,-20 14,-6 9,8 Z"/></g>
    <g class="mark" transform="translate({tx:.0f} {ty-6:.0f})"><path class="atl" d="M-16,10 V-6 H-7 V4 C-7,-6 7,-6 7,4 V-6 H16 V10 Z"/></g>
    <g class="mark anchor" data-min-hours="4" transform="translate({nx} {ny})"><circle r="15"/><path d="M0,-8V8M-6,-4H6M-8,2C-7,8 7,8 8,2" /></g>
    <g class="dock" transform="translate({mx} {my})"><circle r="11"/><circle r="4.5" class="dot"/></g>
  </g>
  <g class="labels" aria-hidden="true">
    <text x="{mx+20}" y="{my+30}" class="lbl lbl-strong">Dubai Marina</text>
    <text x="482" y="884" class="lbl">JBR</text>
    <text x="{ax-50}" y="{ay-34}" class="lbl" text-anchor="end">Ain Dubai</text>
    <text x="{tx-22:.0f}" y="{ty-40:.0f}" class="lbl" text-anchor="end"><tspan x="{tx-22:.0f}">Atlantis</tspan><tspan x="{tx-22:.0f}" dy="24">The Palm</tspan></text>
    <text x="{bx+16:.0f}" y="{by+34:.0f}" class="lbl">Burj Al Arab</text>
    <text x="520" y="476" class="lbl land-lbl" transform="rotate(43 520 476)">Palm Jumeirah</text>
    <text x="430" y="128" class="lbl water-lbl">Arabian Gulf</text>
    <text x="{nx+22}" y="{ny+30}" class="lbl anchor-lbl" data-min-hours="4">Swim stop</text>
  </g>
  <text x="900" y="640" class="lbl city-lbl">Dubai</text>
  <g class="scale" transform="translate(890 800)" aria-hidden="true"><path d="M0,0H90M0,-6V6M90,-6V6"/><text x="45" y="-12" text-anchor="middle">1 km</text></g>
</svg>'''
open(sys.argv[2],'w').write(svg); print(len(svg),'bytes')
