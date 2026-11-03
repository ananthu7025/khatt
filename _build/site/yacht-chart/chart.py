"""Builds the Dubai-coast chart geometry from OpenStreetMap coastline data (osm-coastline.json, natural=coastline ways
around Dubai Marina, Palm Jumeirah and Burj Al Arab, fetched from Overpass). Map data © OpenStreetMap contributors, ODbL.
Projection: x=(lon-55.08)*9060, y=(25.16-lat)*10000 (north up; 90 units = 1 km). Writes chart.json for chart_svg.py,
and fails if a route crosses land."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
def P(lat, lon): return ((lon - 55.08) * 9060, (25.16 - lat) * 10000)

# ── coastline: stitch the ways into rings (islands) and one long open chain (the mainland) ──
ways = json.load(open(os.path.join(HERE, 'osm-coastline.json')))['elements']
by_first = {}
for w in ways: by_first.setdefault(w['nodes'][0], []).append(w)
ends = {w['nodes'][-1] for w in ways}
used, chains = set(), []
for w in sorted(ways, key=lambda w: w['nodes'][0] in ends):   # chain heads (nothing leads into them) first
    if w['id'] in used: continue
    used.add(w['id']); nodes = list(w['nodes']); pts = [(g['lat'], g['lon']) for g in w['geometry']]
    while nodes[0] != nodes[-1]:
        nxt = [v for v in by_first.get(nodes[-1], []) if v['id'] not in used]
        if not nxt: break
        used.add(nxt[0]['id']); nodes += nxt[0]['nodes'][1:]; pts += [(g['lat'], g['lon']) for g in nxt[0]['geometry']][1:]
    chains.append((nodes[0] == nodes[-1], [P(*p) for p in pts]))
mainland = [c for closed, c in chains if not closed]
assert len(mainland) == 1, 'expected one open mainland chain, got %d' % len(mainland)
mainland = mainland[0]
# OSM keeps land on the left of a coastline, so this chain runs north-east to south-west with the land to its south-east:
# close it round that side, far outside the chart
mainland += [(mainland[-1][0], 2600), (2600, 2600), (2600, mainland[0][1])]
islands = [c for closed, c in chains if closed and max(x for x, y in c) > -300 and min(y for x, y in c) < 1400]
polys = [mainland] + islands

def dp(pts, tol):
    """Douglas-Peucker simplification."""
    if len(pts) < 3: return pts
    (x1, y1), (x2, y2) = pts[0], pts[-1]; L = math.hypot(x2 - x1, y2 - y1) or 1e-9
    i, dmax = 0, 0
    for k in range(1, len(pts) - 1):
        d = abs((x2 - x1) * (y1 - pts[k][1]) - (x1 - pts[k][0]) * (y2 - y1)) / L
        if d > dmax: i, dmax = k, d
    return dp(pts[:i + 1], tol)[:-1] + dp(pts[i:], tol) if dmax > tol else [pts[0], pts[-1]]
def ring(pts, tol=0.7):
    # a closed ring starts and ends on the same point, so split it at its farthest point before simplifying
    k = max(range(len(pts)), key=lambda i: math.hypot(pts[i][0] - pts[0][0], pts[i][1] - pts[0][1]))
    pts = dp(pts[:k + 1], tol)[:-1] + dp(pts[k:], tol)
    return 'M' + ' '.join('%.1f,%.1f' % p for p in pts) + 'Z'
land = ' '.join(ring(p) for p in polys)

def inside(x, y, poly):
    c = False
    for (x1, y1), (x2, y2) in zip(poly, poly[1:] + poly[:1]):
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1): c = not c
    return c
def on_land(x, y): return any(inside(x, y, p) for p in polys)

# ── smooth curves ──
def cr_pts(pts, closed=False, t=0.5, steps=12):
    """Points along a Catmull-Rom curve, and the same curve as SVG cubic path data."""
    p = [pts[-1]] + pts + pts[:2] if closed else [pts[0]] + pts + [pts[-1]]
    d = 'M%.0f,%.0f' % p[1]; out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        c1 = (p1[0] + (p2[0] - p0[0]) * t / 3, p1[1] + (p2[1] - p0[1]) * t / 3)
        c2 = (p2[0] - (p3[0] - p1[0]) * t / 3, p2[1] - (p3[1] - p1[1]) * t / 3)
        d += ' C%.0f,%.0f %.0f,%.0f %.0f,%.0f' % (c1 + c2 + p2)
        for s in range(steps):
            u = s / steps; a, b, c, e = (1 - u) ** 3, 3 * u * (1 - u) ** 2, 3 * u * u * (1 - u), u ** 3
            out.append((a * p1[0] + b * c1[0] + c * c2[0] + e * p2[0], a * p1[1] + b * c1[1] + c * c2[1] + e * p2[1]))
    return d + (' Z' if closed else ''), out

# ── depth lines: offsets of a smoothed beach line (decoration; drawn under the land) ──
beach = [(150, 1110), (261, 996), (330, 930), (420, 850), (500, 730), (560, 660), (652, 580), (716, 501), (774, 437), (831, 372), (896, 294), (946, 229), (980, 160), (1050, 40), (1150, -120)]
def offset(pts, dist):
    out = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(i - 1, 0)]; b = pts[min(i + 1, len(pts) - 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy)
        out.append((x + dy / L * dist, y - dx / L * dist))    # seaward (north-west) normal
    return out
contours = [cr_pts(offset(beach, d))[0] for d in (60, 150, 290, 460)]

# ── routes. Boats leave down the Marina canal and out of its south mouth, past Ain Dubai on Bluewaters
# (the canal path came from a shortest water path over the OSM land mask). Past that, each route is a loop in open water
# so the way back shows too. Every route is checked against the land below.
EXIT = [(541, 822), (535, 822), (527, 830), (467, 897), (450, 898), (422, 889), (406, 871), (408, 843), (422, 829), (422, 756), (392, 726)]
LOOP1 = [(360, 712), (318, 730), (300, 775), (310, 815), (335, 830), (328, 790), (345, 752), (375, 733)]
SOUTH_OUT = [(345, 705), (290, 715), (240, 690), (215, 640), (218, 560), (228, 480), (232, 400), (240, 330), (262, 280)]   # up the outside of the crescent to Atlantis
WEST_BACK = [(205, 330), (192, 420), (190, 520), (192, 610), (205, 690), (250, 738), (310, 742), (360, 725)]
NORTH_OUT = [(290, 235), (340, 185), (420, 155), (500, 145), (570, 150), (640, 175), (700, 215), (760, 238), (840, 232), (900, 205), (915, 165)]
NORTH_BACK = [(890, 135), (800, 160), (700, 160), (620, 125), (500, 105), (400, 115), (310, 150), (250, 210), (215, 290)]
r1 = EXIT + LOOP1 + EXIT[::-1]
r2 = EXIT + SOUTH_OUT + WEST_BACK + EXIT[::-1]
r3 = EXIT + SOUTH_OUT + NORTH_OUT + NORTH_BACK + WEST_BACK + EXIT[::-1]
routes = {}
for name, pts in (('r1', r1), ('r2', r2), ('r3', r3)):
    d, samples = cr_pts(pts)
    bad = [(round(x), round(y)) for x, y in samples if on_land(x, y)]
    if bad: raise SystemExit('%s crosses land at %s' % (name, bad[:6]))
    routes[name] = d
routes['r4'] = routes['r3']

pins = {'marina': EXIT[0], 'ain': P(25.0797, 55.1226), 'atlantis': P(25.1304, 55.1171), 'burj': P(25.1412, 55.1853), 'anchor': (800, 236)}
json.dump(dict(land=land, contours=contours, pins=pins, **routes), open(os.path.join(HERE, 'chart.json'), 'w'), indent=1)
print('land', len(land), 'bytes;', len(islands), 'islands; pins', {k: tuple(round(v) for v in p) for k, p in pins.items()},
      '; atlantis on land:', on_land(*pins['atlantis']), '; burj on land:', on_land(*pins['burj']))
