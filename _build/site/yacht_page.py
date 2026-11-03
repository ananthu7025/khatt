"""The yacht rental page: the shared detail-page layout plus its own "Where you'll go" route map.
Imported by build.py. The map comes from yacht-chart/: chart.py turns the OpenStreetMap coastline into chart.json,
then chart_svg.py writes chart.svg.html."""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CHART_SVG = open(os.path.join(HERE, 'yacht-chart', 'chart.svg.html')).read()
CHART_CSS = open(os.path.join(HERE, 'yacht-chart', 'chart.css')).read()

# the map's own colours, and a square card in the content column instead of the old full-height hero
CHART_CSS = """
:root { --sea: #d7ebf2; --contour: #a9cedb; --land: #f1e6c6; --land-edge: #d6c48f; --chart-serif: "Iowan Old Style", "Palatino Linotype", Palatino, Georgia, serif; }
""" + CHART_CSS.replace('.chart-card { align-self: stretch; position: relative;', '.chart-card { position: relative; aspect-ratio: 1 / 1;').replace(' min-height: 620px;', '') \
    .replace('@media (max-width: 900px) { .chart-card { min-height: 0; aspect-ratio: 4 / 5; } }', '')
# the route note sits over the land at the bottom right; on phones it goes under the map so it never hides the Marina
CHART_CSS += """
.chart-wrap { position: relative; }
.chart-foot { position: absolute; right: 0; bottom: 0; }
@media (max-width: 520px) {
  .chart-card { aspect-ratio: 5 / 6; }
  .chart-foot { position: static; padding: 10px 0 0; }
}
"""

HOURS = ''.join('<input type="radio" name="hours" id="h%d" value="%d"%s><label for="h%d">%d %s</label>'
                % (h, h, ' checked' if h == 2 else '', h, h, 'hour' if h == 1 else 'hours') for h in (1, 2, 3, 4))

EXTRA = '''      <section class="block" id="route">
        <h2 class="sec">Where you'll go</h2>
        <p class="sec-sub">The route grows with the time you book. Tap a length to see it.</p>
        <div class="chart-wrap">
          <div class="chart-card" id="chart" data-hours="2">
            %s
            <div class="chart-top">
              <fieldset class="hours"><legend>How long on the water</legend>%s</fieldset>
            </div>
          </div>
          <div class="chart-foot">
            <p class="route-note" aria-live="polite"><b id="route-title">2 hours on the water</b><span id="route-stops">Dubai Marina, JBR, Ain Dubai, the Palm and Atlantis</span></p>
            <p class="chart-disclaimer">Typical route. The captain sets the day's course with the weather and Coast Guard rules.</p>
          </div>
        </div>
        <p class="chart-credit">Map data © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors.</p>
      </section>
''' % (CHART_SVG, HOURS)

EXTRA_JS = '''<script>
/* route map: shows the route for the chosen cruise, and its hour tabs choose that cruise */
(function () {
  var STOPS = {
    1: 'Dubai Marina, JBR and Ain Dubai',
    2: 'Dubai Marina, JBR, Ain Dubai, the Palm and Atlantis',
    3: 'Everything in 2 hours, plus Burj Al Arab',
    4: 'The full route to Burj Al Arab, with time to anchor and swim'
  };
  var chart = document.getElementById('chart');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var current = 2, seen = false;
  function showRoute(h, animate) {
    current = h;
    chart.setAttribute('data-hours', h);
    document.querySelectorAll('.route').forEach(function (p) {
      var on = p.getAttribute('data-hours') === String(h);
      p.classList.toggle('on', on);
      if (!on) return;
      var len = p.getTotalLength();
      p.classList.remove('draw');
      p.style.strokeDasharray = len;
      p.style.strokeDashoffset = animate && !reduce ? len : 0;
      if (animate && !reduce) { p.getBoundingClientRect(); p.classList.add('draw'); p.style.strokeDashoffset = 0; }
    });
    document.getElementById('route-title').textContent = h + (h === 1 ? ' hour' : ' hours') + ' on the water';
    document.getElementById('route-stops').textContent = STOPS[h];
  }
  document.querySelectorAll('input[name="hours"]').forEach(function (r) {
    r.addEventListener('change', function () {
      var el = document.querySelector('.opt[data-id="yacht-' + r.value + 'h"]');
      if (el) el.click();
    });
  });
  window.onChoose = function (o) {
    if (!o.hours) return;
    var r = document.getElementById('h' + o.hours);
    if (r) r.checked = true;
    showRoute(o.hours, seen);
  };
  // draw the route in the first time the map scrolls into view
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (en, obs) {
      if (!en[0].isIntersecting) return;
      seen = true; obs.disconnect(); showRoute(current, true);
    }, { threshold: 0.35 }).observe(chart);
  } else { seen = true; }
})();
</script>'''

INCLUDES = ["Private yacht with captain and crew", "Soft drinks, water and ice", "Bluetooth sound system", "Life jackets for adults and children", "Sun deck"]
EXCLUDES = ["Food and catering (we can arrange it)", "Hotel transfers (on request)", "Tips for the crew"]
PER_HOUR = 800   # Khat's published yacht price, read as per hour: confirm with Khat


def cruise(h, cid, name, tag, photo, blurb, chips, swim=False):
    return {"id": cid, "name": name, "tag": tag, "photo": photo, "blurb": blurb, "chips": chips, "hours": h,
            "group": "cruise", "duration": "%d %s" % (h, "hour" if h == 1 else "hours"), "pickup": "", "where": "Boarding at Dubai Marina",
            "private": PER_HOUR * h, "unit": "for the whole boat",
            "includes": INCLUDES + (["A swim stop"] if swim else []), "excludes": EXCLUDES}


def page(CANCEL, PAY, WEATHER_TIP, REFUND_TIP, FAQ_PAY):
    return {
        "slug": "yacht-rental-dubai", "crumb": "Private yacht rental",
        "title": "Private Yacht Rental in Dubai Marina | Khat Tourism",
        "desc": "Rent a private yacht in Dubai with captain and crew. Cruise from Dubai Marina past JBR, Ain Dubai, Atlantis and Burj Al Arab, from 1 to 4 hours. Free cancellation.",
        "h1": "Private Yacht Rental in Dubai Marina",
        "sub": "Your own yacht, captain and crew from Dubai Marina. Cruise past JBR, Ain Dubai, Atlantis and Burj Al Arab, with a swim stop on longer trips.",
        "hero": "yacht-marina.jpg",
        "gallery": [("yacht-marina.jpg", "A private yacht cruising through Dubai Marina at golden hour"), ("yacht-proposal.jpg", "A couple at the bow of a yacht at sunset"),
                    ("yacht-deck.jpg", "Friends celebrating a birthday on a yacht deck"), ("yacht-swim.jpg", "Friends swimming off the back of an anchored yacht")],
        "photos": [("yacht-atlantis.jpg", "A yacht cruising past Atlantis The Palm"), ("yacht-burj.jpg", "Burj Al Arab seen from a yacht deck"),
                   ("yacht-ain-dubai.jpg", "Ain Dubai lit up at dusk, seen from a yacht"), ("yacht-family.jpg", "A family in life jackets on a yacht deck"),
                   ("yacht-saloon.jpg", "The lounge inside a motor yacht")],
        "facts": [CANCEL, ("guide", "Captain and crew included", "A licensed captain and crew handle the boat and the route."),
                  ("time", "1 to 4 hours", "Pick the length; the route grows with it."), ("pickup", "Boarding at Dubai Marina", "We send the exact pier and a map pin on WhatsApp."),
                  PAY, ("shield", "Life jackets for every size", "For adults and children, plus a first-aid kit on board.")],
        "opt_title": "Which cruise is right for you?", "opt_sub": "Four lengths of charter. The longer you stay out, the further the route goes.",
        "default": "yacht-2h",
        "options": [
            cruise(1, "yacht-1h", "1-hour Marina cruise", "For a quick look", "yacht-ain-dubai.jpg",
                   "Out of Dubai Marina, along JBR and around Ain Dubai on Bluewaters.", ["Dubai Marina", "JBR", "Ain Dubai"]),
            cruise(2, "yacht-2h", "2-hour Palm and Atlantis cruise", "For sunset", "yacht-atlantis.jpg",
                   "Past Ain Dubai and out along the Palm to Atlantis The Palm and back.", ["Ain Dubai", "The Palm", "Atlantis"]),
            cruise(3, "yacht-3h", "3-hour Burj Al Arab cruise", "For the whole coastline", "yacht-burj.jpg",
                   "The full run from the Marina, around the Palm, to Burj Al Arab.", ["Atlantis", "Burj Al Arab", "Swim stop"], swim=True),
            cruise(4, "yacht-4h", "4-hour cruise with swim stop", "For a long, lazy day", "yacht-swim.jpg",
                   "The full route to Burj Al Arab, with time to anchor, swim and eat on board.", ["Burj Al Arab", "Long swim stop", "Time to eat on board"], swim=True),
        ],
        "day": {"cruise": ["How the charter goes", [
            ["Arrive at the marina", "Come 15 to 20 minutes early, with every guest's passport or Emirates ID."],
            ["Safety briefing", "The crew shows you the life jackets and the boat."],
            ["Out on the water", "Your route depends on how long you book. See the map above."],
            ["Swim stop", "On longer charters the captain anchors somewhere calm so you can swim."],
            ["Back at the marina", "At the time you booked."]]]},
        "know": ["UAE Coast Guard rules say everyone on board must carry an original passport or Emirates ID.",
                 "Bring your own food and drinks, or ask us to arrange catering when you book.", WEATHER_TIP, REFUND_TIP],
        "faq": [
            ("How many hours should I book?", "One hour covers Dubai Marina, JBR and Ain Dubai. Two hours adds the Palm and Atlantis, and three reaches Burj Al Arab. Book four if you also want a long swim stop."),
            ("Is the price per person?", "No. The price is for the whole boat with captain and crew."),
            ("How many people can come?", "Tell us your group size on WhatsApp and we'll match the boat. Bigger boats are available for larger groups."),
            ("Where do we board?", "At Dubai Marina or Dubai Harbour, depending on the boat. We send the exact pier and a map pin on WhatsApp after you book."),
            ("Does every guest need ID?", "Yes. UAE Coast Guard rules say everyone on board must carry an original passport or Emirates ID."),
            ("Can we bring food, drinks and music?", "Yes. Bring your own snacks, food and drinks, and connect your phone to the boat's Bluetooth speakers. We can also arrange catering if you ask when you book."),
            ("Is it safe for children?", "Yes. The boat carries life jackets for adults and children, life rings and a first-aid kit, and the captain is licensed."),
            ("Can you pick us up from our hotel?", "Yes. Private hotel transfers are available for an extra fee. Ask for one in your WhatsApp message."),
            ("What if the weather is bad?", "Boats can't leave when the Coast Guard closes the sea. If that happens, you can move your charter to another day or get a full refund."),
            FAQ_PAY],
        "related": ["dubai-city-tour", "desert-safari-dubai", "dune-buggy-dubai"], "related_sub": "Pair your cruise with a desert evening or a day in Old Dubai.",
        "extra": EXTRA, "extra_css": CHART_CSS, "extra_js": EXTRA_JS,
    }
