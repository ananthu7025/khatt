"""Builds site/index.html (the homepage) from home_source.html: shared header, footer and assets, category cards
instead of the full tour grid, and no links to the old site."""
import json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from titles import title_case
from airbnb import AIRBNB, AIRBNB_NOTE
HERE = os.path.dirname(os.path.abspath(__file__))
K = os.path.normpath(os.path.join(HERE, '..', '..'))
t = open(os.path.join(HERE, 'home_source.html')).read()
HEADER = re.sub(r'\{\{CUR_[a-z-]+\}\}', '', open(os.path.join(HERE, 'partials', 'header.html')).read())
FOOTER = open(os.path.join(HERE, 'partials', 'footer.html')).read()

def cut(a, b, new, include_end=True):
    global t
    i = t.index(a); j = t.index(b, i) + (len(b) if include_end else 0)
    t = t[:i] + new + t[j:]
def one(a, b):
    global t
    assert t.count(a) == 1, (t.count(a), a[:80]); t = t.replace(a, b)

t = t.replace('<b>Hotel pickup included</b><span>From any hotel, apartment or cruise terminal in Dubai.</span>', '<b>Hotel pickup on land tours</b><span>From any hotel, apartment or cruise terminal in Dubai. Yacht transfers on request.</span>')
t = t.replace('<h1>Private desert safaris and tours in Dubai</h1>', '<h1>Private Desert Safaris and Tours in Dubai</h1>')
t = t.replace('/home/img/', '/assets/img/').replace('/home/fonts/', '/assets/fonts/')
cut('<header class="top">', '</header>', HEADER.strip())
cut('<footer>', '</footer>', FOOTER.strip().replace('AI-generated illustrations.', 'AI-generated illustrations.' + AIRBNB_NOTE))
one('<a href="https://khattourism.com/cancellation-policy">cancellation policy</a>', '<a href="/cancellation-policy/">cancellation policy</a>')

# categories replace the shortcut strip and the 14-tour grid
cut('<div class="wrap cats">', '<section class="band promise">', '''<section class="band" id="tours">
    <div class="wrap">
      <div class="head"><div>
        <h2>Choose your experience</h2>
        <p>Every tour is private. Pick a category to see its tours, times and prices.</p>
      </div></div>
      <div class="grid cats-grid" id="cats-grid"></div>
    </div>
  </section>

  <section class="band popular" id="popular">
    <div class="wrap">
      <div class="head"><div>
        <h2>Most reviewed on Tripadvisor</h2>
        <p>Our three trips with the most Tripadvisor reviews, all rated 5.0.</p>
      </div></div>
      <div class="grid pop-grid" id="pop-grid"></div>
      <p class="more-tours">Looking for something else? <a href="https://wa.me/971564031600" data-wa="custom_trip">Ask us on WhatsApp</a> and we'll plan it.</p>
    </div>
  </section>

  ''', include_end=False)

# styles: drop the strip and filter rules, add the two grids
t = re.sub(r'/\* category shortcuts \*/.*?(?=section\.band \{)', '', t, flags=re.S)
t = re.sub(r'\.filters[^\n]*\n', '', t)
one('.more-tours { margin-top: 28px; text-align: center; }',
    '.more-tours { margin-top: 28px; text-align: center; }\n.cats-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 26px 20px; }\n.cats-grid .card h3 { font-size: 21px; }\n.cats-grid .card .ph { aspect-ratio: 16 / 10; }\n.pop-grid { grid-template-columns: repeat(3, minmax(0, 1fr)); }\n.popular { padding-top: 0; }\n@media (max-width: 900px) { .cats-grid, .pop-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }\n.card .go { margin-top: 6px; font-weight: 700; font-size: 14.5px; color: var(--red); }')
one('@media (max-width: 560px) {\n  /* phones', '@media (max-width: 560px) {\n  .grid.cats-grid, .grid.pop-grid { grid-template-columns: minmax(0, 1fr); }\n  .grid .card .go { display: none; }\n  /* phones')

# data: categories and the most-reviewed trips instead of every tour
data = json.loads(re.search(r'<script type="application/json" id="home-data">(.*?)</script>', t, re.S).group(1))
data.pop('tours'); data.pop('categories')
data['airbnb'] = AIRBNB
data['categories'] = [
  {"id": "desert", "name": "Desert safari Dubai", "url": "/desert-safari-dubai/", "photo": "/assets/img/land-cruisers-sunset-800.jpg", "line": "Evening, kids-friendly, candlelight dinner and morning safaris in your own Land Cruiser.", "count": "4 safaris", "note": "Hotel pickup included", "from": 400, "unit": "per Land Cruiser"},
  {"id": "yacht", "name": "Private yacht rental", "url": "/yacht-rental-dubai/", "photo": "/assets/img/yacht-marina-800.jpg", "line": "Dubai Marina, Atlantis and Burj Al Arab from your own boat, with captain and crew.", "count": "1 to 4 hours", "note": "Captain and crew included", "from": 800, "unit": "per hour"},
  {"id": "abudhabi-safari", "name": "Abu Dhabi desert safari", "url": "/abu-dhabi-desert-safari/", "photo": "/assets/img/abu-dhabi-land-cruiser.jpg", "line": "Evening safaris with dinner and fire shows, and kids-friendly mornings with a camel farm.", "count": "4 safaris", "note": "Pickup in Abu Dhabi", "from": 500, "unit": "per Land Cruiser"},
  {"id": "buggy", "name": "Dune buggy and quad bike", "url": "/dune-buggy-dubai/", "photo": "/assets/img/dune-buggy.jpg", "line": "Drive a Polaris or Can-Am buggy, or ride your own quad, behind a lead guide.", "count": "3 rides", "note": "Hotel pickup included", "from": 350, "unit": ""},
  {"id": "abudhabi-city", "name": "Abu Dhabi city tour", "url": "/abu-dhabi-city-tour/", "photo": "/assets/img/grand-mosque.jpg", "line": "The Sheikh Zayed Grand Mosque, Emirates Palace and Heritage Village with a private guide.", "count": "2 tours", "note": "Pickup from Dubai or Abu Dhabi", "from": 110, "unit": ""},
  {"id": "city", "name": "Dubai city tour and dinner cruise", "url": "/dubai-city-tour/", "photo": "/assets/img/abra-creek-800.jpg", "line": "Old Dubai, the souks and an abra ride by day, a dhow dinner cruise by night.", "count": "3 tours", "note": "Hotel pickup on city tours", "from": 120, "unit": ""}
]
data['popular'] = [
  {"id": "private-evening", "name": "Private evening desert safari", "url": "/desert-safari-dubai/?safari=private-evening", "photo": "/assets/img/land-cruisers-sunset-800.jpg", "line": "Dune bashing, a camel ride and a belly dance show at sunset.", "duration": "6 hours", "rating": [5.0, 218], "from": 750, "unit": "per Land Cruiser"},
  {"id": "kids-evening", "name": "Kids-friendly desert safari", "url": "/desert-safari-dubai/?safari=kids-evening", "photo": "/assets/img/mother-and-child.jpg", "line": "Planned around small children, with baby seats on request.", "duration": "6 hours", "rating": [5.0, 74], "from": 750, "unit": "per Land Cruiser"},
  {"id": "ad-kids-morning", "name": "Abu Dhabi kids-friendly morning safari", "url": "/abu-dhabi-desert-safari/?safari=ad-kids-morning", "photo": "/assets/img/abu-dhabi-family.jpg", "line": "A camel farm, dune bashing and sandboarding, back before the heat.", "duration": "4 hours", "rating": [5.0, 48], "from": 500, "unit": "per Land Cruiser"}
]
for c in data['categories'] + data['popular']:
    c['name'] = title_case(c['name'])
for r in data['reviews']:
    r['about'] = title_case(r['about'])
cut('<script type="application/json" id="home-data">', '</script>', '<script type="application/json" id="home-data">\n' + json.dumps(data, ensure_ascii=False, indent=1) + '\n</script>')
one('  tours:    one card each. "price" is the From price shown on the tour\'s page on khattourism.com; "unit" is shown only\n            where it is confirmed. "rating" is the Tripadvisor rating of the matching product listing.',
    '  categories: one card per tour page. "from" is the lowest price on that page; "unit" is shown only where it is confirmed.\n  popular:    the trips with the most Tripadvisor reviews; "rating" is from the matching Tripadvisor listing.')

# script: render the two grids instead of the filterable tour grid
i = t.index('  // ── tours grid with filters ──'); j = t.index('  // ── tracking:')
t = t[:i] + '''  // ── categories and the most-reviewed trips ──
  function card(c, kind, pos) {
    var ph = c.photo
      ? '<div class="ph"><img src="' + c.photo + '" alt="" loading="lazy" width="640" height="480"></div>'
      : '<div class="ph sea"><svg viewBox="0 0 400 170" role="img" aria-label="Drawing of a motor yacht"><use href="#boat-profile"/></svg></div>';
    var rate = c.rating ? '<div class="rate"><img src="/assets/img/logos/tripadvisor-mark.svg" alt="Tripadvisor" width="18" height="18"><b>' + c.rating[0].toFixed(1) + '</b><span>(' + fmt.format(c.rating[1]) + ' reviews)</span></div>' : '';
    var meta = kind === 'category' ? '<span>' + esc(c.count) + '</span><span>' + esc(c.note) + '</span>' : '<span>' + esc(c.duration) + '</span><span>Hotel pickup</span>';
    return '<a class="card" href="' + c.url + '" data-kind="' + kind + '" data-pos="' + pos + '">' + ph +
      '<div class="body"><h3>' + esc(c.name) + '</h3><p>' + esc(c.line) + '</p><div class="meta">' + meta + '</div>' + rate +
      '<div class="price">From <b class="num">' + money(c.from) + '</b>' + (c.unit ? ' ' + esc(c.unit) : '') + '</div>' +
      (kind === 'category' ? '<span class="go">See the tours</span>' : '') + '</div></a>';
  }
  $('cats-grid').innerHTML = data.categories.map(function (c, i) { return card(c, 'category', i + 1); }).join('');
  $('pop-grid').innerHTML = data.popular.map(function (c, i) { return card(c, 'popular', i + 1); }).join('');

''' + t[j:]
one("    var card = e.target.closest('a.card');\n    if (card) { var t = data.tours[card.dataset.pos - 1]; track('select_item', { item_id: t.id, item_name: t.name, item_category: t.cat, price: t.price, currency: data.currency, index: Number(card.dataset.pos) }); return; }",
    "    var card = e.target.closest('a.card');\n    if (card) { var list = card.dataset.kind === 'category' ? data.categories : data.popular, t = list[card.dataset.pos - 1]; track('select_item', { item_list_name: card.dataset.kind, item_id: t.id, item_name: t.name, price: t.from, currency: data.currency, index: Number(card.dataset.pos) }); return; }")

left = sorted(set(re.findall(r'href="(https://khattourism\.com[^"]*)"', t)))
for m in re.finditer(r'<script type="application/(?:ld\+)?json"[^>]*>(.*?)</script>', t, re.S): json.loads(m.group(1))
os.makedirs(os.path.join(K, 'site'), exist_ok=True)
open(os.path.join(K, 'site', 'index.html'), 'w').write(t)
print('site/index.html', len(t), 'bytes; khattourism.com hrefs:', left, '; leftover /home/:', '/home/' in t, '; leftover filter code:', 'filters' in t)
