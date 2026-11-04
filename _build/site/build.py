"""Builds the Khat Tourism tour-category pages into ../../site/<slug>/index.html.

Every category page shares template.html (made from the desert safari page by make_template.py), the header and
footer in partials/, and the assets in site/assets/. Page content lives in PAGES below.

    python3 build.py
"""
import html, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from titles import title_case
from airbnb import AIRBNB, AIRBNB_NOTE   # pages with "airbnb": True show it

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.normpath(os.path.join(HERE, '..', '..', 'site'))
TEMPLATE = open(os.path.join(HERE, 'template.html'), encoding='utf-8').read()
HEADER = open(os.path.join(HERE, 'partials', 'header.html'), encoding='utf-8').read()
FOOTER = open(os.path.join(HERE, 'partials', 'footer.html'), encoding='utf-8').read()

FOOTER_CSS = """footer.site-foot { padding-block: 44px 120px; font-size: 14.5px; color: var(--ink-2); border-top: 1px solid var(--line); }
footer.site-foot .cols { display: grid; grid-template-columns: 1.3fr repeat(3, minmax(0, 1fr)); gap: 28px; }
footer.site-foot h3 { margin: 0 0 10px; font: 700 15px var(--display); color: var(--ink); }
footer.site-foot ul { list-style: none; margin: 0; padding: 0; display: grid; gap: 6px; }
footer.site-foot a { text-decoration: none; }
footer.site-foot a:hover { text-decoration: underline; }
footer.site-foot .brand img { height: 48px; width: auto; margin-bottom: 10px; }
footer.site-foot .legal { margin-top: 32px; padding-top: 18px; border-top: 1px solid var(--line); display: flex; flex-wrap: wrap; gap: 8px 20px; justify-content: space-between; }
@media (max-width: 860px) { footer.site-foot .cols { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (min-width: 1041px) { footer.site-foot { padding-bottom: 44px; } }
/* galleries with two photos: a large one and a tall one beside it */
.gallery.g2 { grid-template-columns: 1.7fr 1fr; }
.gallery.g2 .hero-shot { grid-column: 1; }
.gallery.g2 .side-shot { grid-column: 2; }"""

RATINGS = {
    "tripadvisor": {"score": 5.0, "count": 1396, "bars": [["Excellent", 1355], ["Good", 34], ["Average", 4], ["Poor", 0], ["Terrible", 3]],
                    "url": "https://www.tripadvisor.com/Attraction_Review-g295424-d10898020-Reviews-Khat_Tours_and_Safaris-Dubai_Emirate_of_Dubai.html"},
    "google": {"score": 5.0, "count": 113, "bars": [["5 stars", 111], ["4 stars", 0], ["3 stars", 2], ["2 stars", 0], ["1 star", 0]],
               "url": "https://maps.google.com/?cid=10514996801509726899"},
}
MENTIONS = ["Friendly drivers", "Kids and babies", "Quad biking", "Sunset photos", "Private dinners", "Abu Dhabi trips"]
G_URL = RATINGS["google"]["url"]
# Featured reviews, shortlisted from Khat's Tripadvisor tour listings on 1 Nov 2026. All are 5 stars.
# "tours" says which tours a review is about (empty = the company in general); each page shows its own tours' reviews first.
# Paste a short excerpt (one or two sentences) into "text" for each; until then the card links to the full review.
# Left out on purpose: a 1-star review about being asked for cash after being told card was fine (Lizzy P, Oct 2026),
# a 3-star one about child seats on the Abu Dhabi kids morning safari (Silke, Feb 2026), and a 5-star one titled "crazy driver".
def ta(g, d, r, slug):
    return "https://www.tripadvisor.com/ShowUserReviews-%s-%s-r%s-%s.html" % (g, d, r, slug)
KIDS = ("g295424", "d19881866", "Kids_Friendly_Desert_Safari_or_Kids_Friendly_Desert_Tours-Dubai_Emirate_of_Dubai")
DESERT = ("g295424", "d18935556", "Dubai_Desert_Safari-Dubai_Emirate_of_Dubai")
EVENING = ("g295424", "d15209402", "Exclusive_Evening_Desert_Safari-Dubai_Emirate_of_Dubai")
MORNING = ("g295424", "d21196862", "Dubai_Kids_Friendly_Morning_Safari_Private_Car-Dubai_Emirate_of_Dubai")
AD_KIDS_EVE = ("g295424", "d25338184", "Abu_Dhabi_Kids_Friendly_Evening_Desert_Safari-Dubai_Emirate_of_Dubai")
AD_KIDS_AM = ("g294013", "d26368707", "Abu_Dhabi_Kids_Friendly_Morning_Desert_Safari-Abu_Dhabi_Emirate_of_Abu_Dhabi")
AD_AM = ("g294013", "d20322522", "Abu_Dhabi_morning_desert_safari_Private_car-Abu_Dhabi_Emirate_of_Abu_Dhabi")
KHAT = ("g295424", "d10898020", "Khat_Tours_and_Safaris-Dubai_Emirate_of_Dubai")
def rv(author, date, trip, about, tours, listing, rid, why):
    g, d, slug = listing
    return {"source": "tripadvisor", "author": author, "tours": tours, "from": trip, "date": date, "about": about, "rating": 5,
            "text": "", "why": why, "url": ta(g, d, rid, slug)}
FAM, FRIENDS, COUPLE = "Travelled with family", "Travelled with friends", "Travelled as a couple"
REVIEWS = [
    # Dubai, kids-friendly
    rv("Rita T", "Feb 2026", FAM, "Kids-friendly desert safari", ["kids-evening"], KIDS, "1049830458", "Two small children: child seats and a booster provided; guide Mohamed"),
    rv("Claire H", "Feb 2026", FAM, "Kids-friendly desert safari", ["kids-evening"], KIDS, "1049300392", "Infant and toddler: prompt hotel pickup, car seats ready"),
    rv("Stéphanie L", "Feb 2026", FAM, "Dubai desert safari", ["kids-evening", "private-evening"], DESERT, "1051067462", "Safe driver (Mani), great with the kids, taught them sandboarding"),
    rv("Prevlen R", "Aug 2026", FAM, "Kids-friendly desert safari", ["kids-evening"], KIDS, "1073496212", "Recent, short: excellent on all fronts, brilliant guide"),
    rv("Soner B", "Nov 2025", FAM, "Kids-friendly desert safari", ["kids-evening"], KIDS, "1038874009", "With a child: dunes, sandboarding, camp, camels, falcon photos"),
    # Dubai, private evening
    rv("AtHomeWithTheHappyHousewife", "Sep 2026", FAM, "Dubai desert safari", ["private-evening"], DESERT, "1078722684", "Guide Safs; sunset photos; good vegetarian food"),
    rv("Kofi S", "Apr 2024", COUPLE, "Exclusive evening desert safari", ["private-evening", "romantic-dinner"], EVENING, "945655273", "Couple: very responsive, delivered everything as discussed"),
    rv("NiccoleWilson", "Dec 2023", FAM, "Exclusive evening desert safari", ["private-evening"], EVENING, "931344272", "Went above and beyond: hotel pickup, lots of photos"),
    # Dubai, morning
    rv("Chris C", "Apr 2025", FAM, "Kids-friendly morning safari", ["private-morning", "kids-evening"], MORNING, "1001921708", "Driver confirmed pickup the day before, arrived early; booster seat"),
    rv("Markus W", "Apr 2025", FAM, "Kids-friendly morning safari", ["private-morning"], MORNING, "1004750616", "Children aged 4 and 1½; hotel pickup; needs looked after"),
    rv("shrirang K", "Dec 2024", FAM, "Kids-friendly morning safari", ["private-morning"], MORNING, "984840645", "Kids had fun; very safe and informative"),
    # Abu Dhabi
    rv("AO’C", "Oct 2026", FAM, "Kids-friendly evening safari, Abu Dhabi", ["ad-kids-evening", "ad-private-evening"], AD_KIDS_EVE, "1082855849", "Picked up at 2:30 by driver Jay"),
    rv("Aaron A", "Feb 2026", FAM, "Kids-friendly morning safari, Abu Dhabi", ["ad-kids-morning", "ad-kids-evening"], AD_KIDS_AM, "1049879861", "Booster seat provided for a five-year-old"),
    rv("Kellan W", "Feb 2026", FAM, "Kids-friendly morning safari, Abu Dhabi", ["ad-kids-morning"], AD_KIDS_AM, "1050053399", "Well organised and safe from start to finish"),
    rv("Iris L", "Feb 2026", FAM, "Kids-friendly morning safari, Abu Dhabi", ["ad-kids-morning"], AD_KIDS_AM, "1050900658", "A two-year-old had fun; cool sand in the morning"),
    rv("Nadia T", "Apr 2026", FAM, "Morning desert safari, Abu Dhabi", ["ad-private-morning"], AD_AM, "1056880041", "Family of five: worth every dirham; dune bashing and camel farm"),
    rv("Meander297547", "Jan 2026", FAM, "Morning desert safari, Abu Dhabi", ["ad-private-morning", "ad-kids-morning"], AD_AM, "1045771352", "Car seat for the toddler; camel ride and sandboarding"),
    rv("Radu I", "Dec 2025", FAM, "Morning desert safari, Abu Dhabi", ["ad-private-morning"], AD_AM, "1043124733", "Camel ride with the kids, time at the camp"),
    # Quad, city tours (older: Khat has no separate Tripadvisor listing for these)
    rv("Viktoria H", "Jan 2023", FRIENDS, "Desert safari with quad biking", ["quad-bike", "morning-quad"], KHAT, "875035984", "Dune bashing, quad biking, camels and sandboarding"),
    rv("Pankaj Tiwari", "Oct 2022", FRIENDS, "Desert safari with quad biking", ["quad-bike", "morning-quad"], KHAT, "867573039", "Really enjoyed the safari and the quad biking"),
    rv("Taras T", "Mar 2021", FRIENDS, "Desert safari with quad biking", ["quad-bike"], KHAT, "784243931", "Quad bikes, dunes, camp: everything perfect"),
    rv("Nawaf A", "Nov 2022", FRIENDS, "Dubai city tour", ["dubai-full", "dubai-half"], KHAT, "867320235", "Excellent Dubai city tour"),
    rv("Dawn C", "Nov 2022", COUPLE, "Dubai city tour", ["dubai-full"], KHAT, "868846911", "Guide Anjay for a day in Dubai"),
    rv("Basu", "Dec 2019", FAM, "Half-day Dubai city tour", ["dubai-half"], KHAT, "733808170", "Half-day city tour"),
    rv("Delia C", "Apr 2023", FRIENDS, "Abu Dhabi city tour and Grand Mosque", ["grand-mosque", "ad-city"], KHAT, "885776842", "Grand Mosque visit"),
    # Google, about the company in general
    {"source": "google", "author": "Yolanda Jackson", "tours": [], "from": "Google Local Guide", "date": "2026", "about": "Desert safari", "rating": 5, "text": "", "url": G_URL},
    {"source": "google", "author": "Elliot Hasoon", "tours": [], "from": "Google reviewer", "date": "2026", "about": "Desert safari", "rating": 5, "text": "", "url": G_URL},
    {"source": "google", "author": "Danny Hasoon", "tours": [], "from": "Google reviewer", "date": "2026", "about": "Desert safari", "rating": 5, "text": "", "url": G_URL},
]

ICON = {
    "cancel": '<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M3 9h18M8 2v4M16 2v4"/><path d="m9 15 2 2 4-4"/>',
    "pickup": '<path d="M3 17h18M5 17l1.5-6h11L19 17"/><circle cx="7.5" cy="19" r="1.5"/><circle cx="16.5" cy="19" r="1.5"/><path d="M8 11l1-4h6l1 4"/>',
    "time": '<circle cx="12" cy="13" r="8"/><path d="M12 9v4l2.5 2.5M9 2h6"/>',
    "family": '<circle cx="9" cy="7" r="3"/><circle cx="17" cy="10" r="2"/><path d="M3 21c0-4 3-6 6-6s6 2 6 6M14 21c0-2.5 1.5-4 3-4s3 1.5 3 4"/>',
    "pay": '<rect x="2" y="6" width="20" height="13" rx="2"/><path d="M2 10h20M6 15h4"/>',
    "licence": '<path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><path d="M4 22v-7"/>',
    "guide": '<circle cx="12" cy="7" r="4"/><path d="M4 21c1-4 4-6 8-6s7 2 8 6"/>',
    "shield": '<path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/><path d="m9 12 2 2 4-4"/>',
}
CANCEL = ("cancel", "Free cancellation", "Up to 48 hours before pickup for a full refund.")
PAY = ("pay", "Pay your way", "Card, bank transfer, PayPal or cash on the day.")
WEATHER_TIP = "If a sandstorm, heavy rain or a government weather warning stops the trip, you can move it to another day or get a full refund."
REFUND_TIP = 'Refunds go back to the way you paid within 3 to 5 working days. See the <a href="/cancellation-policy/">cancellation policy</a>.'
FAQ_PAY = ("When do I pay?", "Confirm on WhatsApp, then pay by card, bank transfer, PayPal or cash on the day.")
FAQ_PRIVATE = ("Will we share the car with other people?", "No. Every tour is private: your own vehicle and driver or guide, for your group only.")

RELATED = {
    "desert-safari-dubai": ("/desert-safari-dubai/", "land-cruisers-sunset-800.jpg", "Desert safari Dubai", "Evening, kids-friendly, candlelight dinner and morning safaris"),
    "yacht-rental-dubai": ("/yacht-rental-dubai/", "yacht-marina-800.jpg", "Private yacht rental", "Marina, Atlantis and Burj Al Arab from the water"),
    "abu-dhabi-desert-safari": ("/abu-dhabi-desert-safari/", "abu-dhabi-land-cruiser.jpg", "Abu Dhabi desert safari", "Evening, morning and kids-friendly safaris"),
    "abu-dhabi-city-tour": ("/abu-dhabi-city-tour/", "grand-mosque.jpg", "Abu Dhabi city tour", "The Grand Mosque, Heritage Village and the Corniche"),
    "dune-buggy-dubai": ("/dune-buggy-dubai/", "dune-buggy.jpg", "Dune buggy and quad", "Drive the red dunes yourself, with a lead guide"),
    "dubai-city-tour": ("/dubai-city-tour/", "abra-creek-800.jpg", "Dubai city tour", "Souks, the abra and an evening dhow cruise"),
}

PAGES = [
  # ── Dubai desert safari (the original page, rebuilt from the shared template) ──
  {
    "slug": "desert-safari-dubai", "crumb": "Desert safari Dubai", "airbnb": True,
    "title": "Desert Safari Dubai: Private Tours with Hotel Pickup | Khat Tourism",
    "desc": "Book a private desert safari in Dubai with hotel pickup: evening safari, kids-friendly safari, candlelight dinner for two and morning safari. Rated 5.0 from 1,509 reviews. Free cancellation.",
    "h1": "Desert Safari Dubai: Private Tours with Hotel Pickup",
    "sub": "Dune bashing, camel rides and dinner in the dunes. A licensed driver collects you from your hotel in a Land Cruiser and brings you back.",
    "hero": "land-cruisers-sunset.jpg",
    "gallery": [("land-cruisers-sunset.jpg", "Two Khat Land Cruisers parked on a dune at sunset"), ("family-watching-dunes.jpg", "A family watching the sun go down over the dunes"),
                ("private-dinner-setup.jpg", "A private dinner table set on a carpet in the dunes"), ("quad-bikes-dunes.jpg", "Guests riding quad bikes across the sand")],
    "photos": [("land-cruiser-daytime.jpg", "A Land Cruiser dune bashing in the morning"), ("camel-morning.jpg", "A camel in the desert"), ("couple-on-dune.jpg", "A couple sitting on a dune at sunset"),
               ("camp-dinner-night.jpg", "A lantern-lit dinner in the desert at night"), ("mother-and-child.jpg", "A mother holding her son in the dunes"), ("land-cruiser-dusk.jpg", "A Land Cruiser in the dunes at dusk")],
    "facts": [CANCEL, ("pickup", "Hotel pickup included", "From any hotel, apartment or cruise terminal in Dubai."), ("time", "3 to 6 hours", "Mornings are shorter, evenings run through dinner."),
              ("family", "Made for families", "Baby seats and boosters on request, and drivers used to small children."), PAY, ("licence", "Licensed safari drivers", "Every driver holds a desert safari licence.")],
    "opt_title": "Which safari is right for you?", "opt_sub": "Four ways to see the desert. Pick one to see the price for your group.",
    "default": "private-evening",
    "options": [
      {"id": "private-evening", "name": "Private evening safari", "tag": "For groups and friends", "hot": "Most reviewed", "photo": "land-cruisers-sunset-800.jpg",
       "blurb": "Just your group and the driver in a Land Cruiser, out to the red dunes for sunset.", "chips": ["Red dune bashing", "Camel ride", "Belly dance show"],
       "group": "evening", "duration": "6 hours", "pickup": "3:00–3:30 PM", "private": 850, "unit": "per Land Cruiser",
       "includes": ["Hotel pickup and drop-off", "Red dune bashing", "Camel ride", "Arabic coffee and dates", "Unlimited soft drinks", "Shisha corner", "Belly dance show"],
       "excludes": ["Private VIP table at the camp", "Quad bike"]},
      {"id": "kids-evening", "name": "Kids-friendly safari", "tag": "For families", "photo": "mother-and-child.jpg",
       "blurb": "Planned around small children, with baby seats on request and drivers used to little ones.", "chips": ["Baby seats and boosters", "Sandboarding", "Live shows"],
       "group": "evening", "duration": "6 hours", "pickup": "2:30–3:00 PM", "private": 850, "unit": "per Land Cruiser",
       "includes": ["Hotel pickup and drop-off", "Baby seats and boosters on request", "Sandboarding", "Live entertainment shows", "Soft drinks and water"],
       "excludes": ["Quad bikes (available to rent)", "Falcon photos", "Alcoholic drinks"]},
      {"id": "romantic-dinner", "name": "Candlelight dinner for two", "tag": "For couples", "photo": "camp-dinner-night.jpg",
       "blurb": "A sunset drive, then a table set just for the two of you among the dunes.", "chips": ["Private dinner setup", "Sunset views", "Desert photos"],
       "group": "evening", "duration": "6 hours", "pickup": "Around 2:00 PM", "private": 1500, "unit": "per couple",
       "includes": ["Private pickup and drop-off", "Dune bashing", "Sunset views", "Private dinner setup in the dunes", "Sandboarding", "Desert photography"],
       "excludes": ["Quad bike", "Dune buggy"]},
      {"id": "private-morning", "name": "Morning safari", "tag": "For hot days and early risers", "photo": "land-cruiser-daytime.jpg",
       "blurb": "Out early while the dunes are cool, and back at your hotel by late morning.", "chips": ["Dune bashing", "Sandboarding", "Camel ride"],
       "group": "morning", "duration": "3 hours", "pickup": "7:30–8:00 AM", "private": 500, "unit": "per Land Cruiser",
       "includes": ["Hotel pickup and drop-off", "Dune bashing", "Sandboarding", "Camel ride"], "excludes": ["Breakfast", "Quad bikes"]},
    ],
    "day": {
      "evening": ["How the evening goes", [["Hotel pickup", "Your driver collects you in a Land Cruiser."], ["Dune bashing", "A roller-coaster drive over the red dunes."], ["Sunset photo stop", "Time on the dunes as the sun goes down."],
                  ["Camel ride and sandboarding", "At the camp, or on the dunes on private trips."], ["Dinner and shows", "Arabic coffee, dates and dinner. Shows depend on the safari you pick."], ["Drop-off", "Back at your hotel around six hours after pickup."]]],
      "morning": ["How the morning goes", [["Early hotel pickup", "Beat the heat with a morning start."], ["Dune bashing", "The dunes are quieter and cooler in the morning."], ["Sandboarding and a camel ride", "Then a few photo stops on the way back."], ["Drop-off", "Back at your hotel by late morning."]]],
    },
    "know": ["Dune bashing is bumpy. Tell us when you book if anyone is pregnant or has back, neck or heart problems, and we'll plan the trip around them.",
             "Wear light, loose clothes and closed shoes. Bring sunglasses, and a light layer for winter evenings.", WEATHER_TIP, REFUND_TIP],
    "faq": [("Which desert safari should I book?", "Pick the private evening safari to have the Land Cruiser to yourselves, the kids-friendly safari if you're bringing babies or young children, the candlelight dinner for a couple's evening, or the morning safari to avoid the afternoon heat."),
            FAQ_PRIVATE, ("Can we bring a baby or toddler?", "Yes. Ask for a baby seat or booster when you book, and tell us your children's ages so the driver can keep the dune bashing gentle."),
            ("Where do you pick up from?", "Any hotel, hotel apartment or cruise terminal in Dubai."),
            ("Can we add a quad bike or dune buggy?", "Yes, on most trips. Quad bikes and buggies are paid extras. Ask in your WhatsApp message and we'll add the price to your quote."), FAQ_PAY],
    "related": ["abu-dhabi-desert-safari", "dune-buggy-dubai", "yacht-rental-dubai"], "related_sub": "Pair your safari with a day on the water or a faster ride through the dunes.",
  },
  # ── Abu Dhabi desert safari ──
  {
    "slug": "abu-dhabi-desert-safari", "crumb": "Abu Dhabi desert safari",
    "title": "Abu Dhabi Desert Safari: Private Tours with Hotel Pickup | Khat Tourism",
    "desc": "Private desert safaris in Abu Dhabi with hotel pickup: evening safari with BBQ dinner and fire show, kids-friendly safaris with a camel farm visit, and morning safaris. Free cancellation.",
    "h1": "Abu Dhabi Desert Safari: Private Tours with Hotel Pickup",
    "sub": "Dune bashing, camel rides and dinner under the stars, in your own Land Cruiser. We pick you up from your hotel or home in Abu Dhabi.",
    "hero": "abu-dhabi-land-cruiser.jpg",
    "gallery": [("abu-dhabi-land-cruiser.jpg", "A Khat Land Cruiser dune bashing in golden sand"), ("abu-dhabi-family.jpg", "A mother and daughter in the dunes"),
                ("kids-camel-abu-dhabi.jpg", "Children riding a camel"), ("abu-dhabi-dune-bashing.jpg", "A Land Cruiser crossing the dunes")],
    "photos": [("camp-dinner-night.jpg", "A lantern-lit dinner in the desert at night"), ("land-cruiser-daytime.jpg", "A Land Cruiser dune bashing in the morning")],
    "facts": [CANCEL, ("pickup", "Pickup in Abu Dhabi", "From your hotel, home or chosen spot in Abu Dhabi."), ("time", "4 to 6 hours", "Mornings are shorter, evenings run through dinner."),
              ("family", "Made for families", "Baby seats on request and a camel farm visit on the kids' trips."), PAY, ("licence", "Licensed safari drivers", "Every driver holds a desert safari licence.")],
    "opt_title": "Which Abu Dhabi safari is right for you?", "opt_sub": "Four private safaris. Pick one to see the price for your group.",
    "default": "ad-private-evening",
    "options": [
      {"id": "ad-private-evening", "name": "Private evening safari", "tag": "For groups and friends", "photo": "abu-dhabi-land-cruiser.jpg",
       "blurb": "Dune bashing, sandboarding and a camel ride, then a BBQ dinner with live dance and fire shows.", "chips": ["BBQ dinner", "Fire show", "Camel ride"],
       "group": "evening", "duration": "6 hours", "pickup": "Flexible, in Abu Dhabi", "private": 950, "unit": "per Land Cruiser",
       "includes": ["Pickup and drop-off in a Land Cruiser", "Licensed safari driver", "Dune bashing and sandboarding", "Camel ride", "Unlimited water and soft drinks", "Arabian BBQ dinner, vegetarian or not", "Live dance and fire shows"],
       "excludes": ["Quad bike or dune buggy (optional)", "Alcoholic drinks (sold at the bar)", "Souvenir photos", "Tips"]},
      {"id": "ad-kids-evening", "name": "Kids-friendly evening safari", "tag": "For families", "photo": "kids-camel-abu-dhabi.jpg",
       "blurb": "A camel farm visit, sunset photos and a BBQ dinner with shows, timed around your children.", "chips": ["Camel farm", "BBQ dinner", "Live shows"],
       "group": "evening", "duration": "6 hours", "pickup": "Flexible, around your children", "private": 950, "unit": "per Land Cruiser",
       "includes": ["Pickup and drop-off", "Dune bashing", "Camel farm visit", "Desert photo stop", "Camel ride", "Henna painting", "Sunset photography", "Water and soft drinks", "BBQ dinner", "Live entertainment"],
       "excludes": ["Quad bikes"]},
      {"id": "ad-kids-morning", "name": "Kids-friendly morning safari", "tag": "For families with small children", "hot": "Most reviewed", "photo": "abu-dhabi-family.jpg",
       "blurb": "A gentle morning out: a camel farm, dune bashing and sandboarding, back before the heat.", "chips": ["Camel farm", "Sandboarding", "Camel ride"],
       "group": "morning", "duration": "4 hours", "pickup": "Flexible", "private": 500, "unit": "per Land Cruiser",
       "includes": ["Pickup and drop-off", "Camel farm visit", "Dune bashing", "Desert photo stop", "Camel ride", "Sandboarding"], "excludes": ["Quad bike rides"]},
      {"id": "ad-private-morning", "name": "Private morning safari", "tag": "For hot days and early risers", "photo": "land-cruiser-daytime.jpg",
       "blurb": "Out at 7:30 AM for dune bashing, sandboarding and a camel ride in the cool of the morning.", "chips": ["Dune bashing", "Sandboarding", "Baby seats on request"],
       "group": "morning", "duration": "4 hours", "pickup": "7:30 AM", "private": 500, "unit": "per Land Cruiser",
       "includes": ["Private pickup and drop-off in Abu Dhabi", "Your own Land Cruiser", "Dune bashing", "Desert photo stop", "Camel ride", "Sandboarding", "Bottled water", "Baby seats on request"],
       "excludes": ["Quad bike or buggy"]},
    ],
    "day": {
      "evening": ["How the evening goes", [["Pickup in Abu Dhabi", "Your driver collects you in a Land Cruiser."], ["Dune bashing and sandboarding", "Out into the dunes beyond the city."], ["Sunset photo stop", "Time on the dunes as the sun goes down."],
                  ["Camel ride", "On the kids' safari, with a visit to a camel farm."], ["Dinner and shows", "A BBQ dinner with live entertainment at the camp."], ["Drop-off", "Back home around six hours after pickup."]]],
      "morning": ["How the morning goes", [["Morning pickup", "Your driver collects you in Abu Dhabi."], ["Camel farm or dune bashing", "Depending on the safari you pick."], ["Sandboarding and a camel ride", "With photo stops in the dunes."], ["Drop-off", "Back before the midday heat."]]],
    },
    "know": ["Dune bashing is bumpy. Tell us when you book if anyone is pregnant or has back, neck or heart problems.",
             "Tell us your children's ages and whether you need a baby seat, and we'll set the pace around them.", "Staying in Dubai? Ask us on WhatsApp about pickup from Dubai.", WEATHER_TIP],
    "faq": [FAQ_PRIVATE, ("Where do you pick up from?", "From your hotel, home or a spot you choose in Abu Dhabi. If you're staying in Dubai, ask us on WhatsApp about pickup from Dubai."),
            ("Is the kids-friendly safari safe for babies?", "Yes. Ask for a baby seat when you book and tell us your children's ages, and the driver plans the dune bashing around them."),
            ("Is dinner vegetarian-friendly?", "Yes. The Arabian BBQ dinner on the private evening safari has vegetarian and non-vegetarian dishes."), FAQ_PAY],
    "related": ["abu-dhabi-city-tour", "desert-safari-dubai", "dune-buggy-dubai"], "related_sub": "Add a day in the city, or try a safari in Dubai.",
  },
  # ── Abu Dhabi city tour ──
  {
    "slug": "abu-dhabi-city-tour", "crumb": "Abu Dhabi city tour",
    "title": "Abu Dhabi City Tour from Dubai: Grand Mosque & Private Guide | Khat Tourism",
    "desc": "Private Abu Dhabi city tour from Dubai or Abu Dhabi with a licensed guide: Sheikh Zayed Grand Mosque, Emirates Palace, Heritage Village and the Corniche. Free cancellation.",
    "h1": "Abu Dhabi City Tour from Dubai with a Private Guide",
    "sub": "The Sheikh Zayed Grand Mosque, Emirates Palace and the Heritage Village, with a licensed guide and pickup from Dubai or Abu Dhabi.",
    "hero": "grand-mosque.jpg",
    "gallery": [("grand-mosque.jpg", "Sheikh Zayed Grand Mosque at dusk"), ("abu-dhabi-skyline.jpg", "The Abu Dhabi skyline from the water")],
    "photos": [],
    "facts": [CANCEL, ("pickup", "Pickup from Dubai or Abu Dhabi", "We collect you from your hotel in either city."), ("guide", "Licensed guide", "A professional guide stays with you all day."),
              ("time", "4 or 8 hours", "A Grand Mosque visit or a full day in the city."), PAY, ("shield", "Mosque entry included", "On the full-day tour, with the Heritage Village.")],
    "opt_title": "Which tour is right for you?", "opt_sub": "Two ways to see Abu Dhabi. Pick one to see the price.",
    "default": "ad-city",
    "options": [
      {"id": "ad-city", "name": "Full-day Abu Dhabi city tour", "tag": "For seeing the city", "photo": "abu-dhabi-skyline.jpg",
       "blurb": "The Grand Mosque, Emirates Palace, the Heritage Village and a drive along the Corniche.", "chips": ["Grand Mosque", "Heritage Village", "Emirates Palace"],
       "group": "adcity", "duration": "8 hours", "pickup": "9:00 AM, from Dubai or Abu Dhabi", "private": 850, "unit": "starting price",
       "includes": ["Pickup from Dubai or Abu Dhabi", "Licensed guide", "Sheikh Zayed Grand Mosque", "Heritage Village entry", "Emirates Palace photo stop", "Corniche drive", "Dates market", "Ferrari World photo stop"],
       "excludes": ["Lunch", "Ferrari World tickets"]},
      {"id": "grand-mosque", "name": "Grand Mosque tour", "tag": "For a half-day visit", "photo": "grand-mosque.jpg",
       "blurb": "A guided visit to the Sheikh Zayed Grand Mosque, with private transfers there and back.", "chips": ["Licensed guide", "Private transfer", "Half day"],
       "group": "mosque", "duration": "4 hours", "pickup": "8:00 AM", "private": 600, "unit": "starting price",
       "includes": ["Private transfer", "Professional guide", "Bottled water"], "excludes": ["Meals"]},
    ],
    "day": {
      "adcity": ["How the day goes", [["Morning pickup", "From your hotel in Dubai or Abu Dhabi at 9:00 AM."], ["Sheikh Zayed Grand Mosque", "A guided visit inside the mosque."], ["Emirates Palace", "A photo stop outside the palace."],
                 ["Heritage Village and dates market", "A look at life in the Emirates before oil."], ["Corniche and Ferrari World", "A drive along the waterfront and a photo stop."], ["Drop-off", "Back at your hotel in the evening."]]],
      "mosque": ["How the visit goes", [["Morning pickup", "From your hotel at 8:00 AM."], ["Drive to the mosque", "Your guide introduces the mosque on the way."], ["Guided visit", "Time inside the Sheikh Zayed Grand Mosque."], ["Drop-off", "Back at your hotel around four hours after pickup."]]],
    },
    "know": ["The Grand Mosque has a dress code: cover your arms and legs, and women cover their hair.", "Lunch isn't included.", WEATHER_TIP, REFUND_TIP],
    "faq": [FAQ_PRIVATE, ("Can you pick us up in Dubai?", "Yes. The full-day tour picks up from Dubai or Abu Dhabi."),
            ("What should we wear to the mosque?", "Cover your arms and legs. Women also cover their hair."), ("Is lunch included?", "No. Lunch and Ferrari World tickets are extra."), FAQ_PAY],
    "related": ["abu-dhabi-desert-safari", "dubai-city-tour", "desert-safari-dubai"], "related_sub": "End the day in the dunes, or see Dubai too.",
  },
  # ── Dune buggy and quad bike ──
  {
    "slug": "dune-buggy-dubai", "crumb": "Dune buggy and quad bike",
    "title": "Dune Buggy & Quad Bike Tours in Dubai with Hotel Pickup | Khat Tourism",
    "desc": "Drive a Polaris or Can-Am dune buggy or ride your own quad bike in Dubai's red dunes, with a lead guide, safety gear and hotel pickup. Free cancellation.",
    "h1": "Dune Buggy & Quad Bike Tours in Dubai with Hotel Pickup",
    "sub": "Drive the red dunes yourself behind a lead guide, with helmets, goggles and pickup from your hotel included.",
    "hero": "dune-buggy.jpg",
    "gallery": [("dune-buggy.jpg", "A dune buggy throwing up red sand"), ("quad-bikes-dunes.jpg", "Riders on quad bikes in the dunes"),
                ("land-cruiser-daytime.jpg", "A Land Cruiser dune bashing in the morning"), ("camel-morning.jpg", "A camel in the desert")],
    "photos": [],
    "facts": [CANCEL, ("pickup", "Hotel pickup included", "From any hotel or residence in Dubai."), ("guide", "Lead guide on every ride", "With a safety vehicle and mechanic on quad tours."),
              ("shield", "Safety gear included", "Helmet and goggles, plus a full safety briefing."), ("time", "About 3 hours", "Including pickup and drop-off."), PAY],
    "opt_title": "Which ride is right for you?", "opt_sub": "Three ways to drive the dunes. Pick one to see the price.",
    "default": "dune-buggy",
    "options": [
      {"id": "dune-buggy", "name": "Dune buggy tour", "tag": "For thrill seekers", "photo": "dune-buggy.jpg",
       "blurb": "Drive a Polaris or Can-Am buggy yourself through the red dunes, behind a lead guide.", "chips": ["Self-drive", "Polaris or Can-Am", "Lead guide"],
       "group": "ride", "duration": "3 hours", "pickup": "At a time that suits you", "private": 750, "unit": "starting price",
       "includes": ["Hotel pickup and drop-off", "Full safety briefing", "Helmet and goggles", "Experienced lead guide", "Water and energy drinks"], "excludes": ["Souvenirs and photos", "Tips"]},
      {"id": "quad-bike", "name": "Quad bike tour", "tag": "For riding your own quad", "photo": "quad-bikes-dunes.jpg",
       "blurb": "An hour on your own quad bike with a lead guide, a mechanic and a safety vehicle.", "chips": ["1 hour on a quad", "Safety gear", "Sandboarding"],
       "group": "ride", "duration": "3 hours", "pickup": "8:00 AM or 3:00 PM", "private": 450, "unit": "starting price",
       "includes": ["Private pickup and drop-off", "Full safety briefing", "Helmet, goggles and harness", "Experienced lead guide", "Mechanic and safety vehicle", "1 hour quad ride", "Cold water"],
       "excludes": ["Tips for the instructors"]},
      {"id": "morning-quad", "name": "Morning safari with quad bike", "tag": "For a bit of everything", "photo": "land-cruiser-daytime.jpg",
       "blurb": "A morning in the dunes in your own Land Cruiser, with a quad bike ride before the heat.", "chips": ["Quad bike ride", "Land Cruiser", "Morning start"],
       "group": "morning", "duration": "4 hours", "pickup": "Flexible", "private": 700, "unit": "per Land Cruiser",
       "includes": ["Hotel pickup and drop-off", "Quad bike ride", "Safety gear and helmet", "Water and soft drinks"], "excludes": ["Souvenirs and photos", "Tips"]},
    ],
    "day": {
      "ride": ["How the ride goes", [["Hotel pickup", "Your driver collects you and drives you out to the dunes."], ["Safety briefing", "Helmets, goggles and a run-through of the controls."], ["Into the dunes", "Follow your lead guide across the red sand."], ["Photo stop", "Time for photos on top of the dunes."], ["Drop-off", "Back at your hotel around three hours after pickup."]]],
      "morning": ["How the morning goes", [["Morning pickup", "In your own Land Cruiser."], ["Quad bike ride", "Ride the dunes behind a guide."], ["Photo stops", "In the soft morning light."], ["Drop-off", "Back before the midday heat."]]],
    },
    "know": ["Wear closed shoes and clothes you don't mind getting sandy. Sunglasses help in the wind.", "Tell us when you book if anyone is pregnant or has back or neck problems.", WEATHER_TIP, REFUND_TIP],
    "faq": [FAQ_PRIVATE, ("Do I drive the buggy myself?", "Yes. You drive a Polaris or Can-Am buggy yourself, following a lead guide."),
            ("Is safety gear included?", "Yes. Helmets and goggles are included, and every ride starts with a safety briefing."),
            ("What times can we go?", "Quad bike tours run at 8:00 AM and 3:00 PM. Buggy tours can be booked at a time that suits you."), FAQ_PAY],
    "related": ["desert-safari-dubai", "abu-dhabi-desert-safari", "yacht-rental-dubai"], "related_sub": "Slow things down with a desert dinner or a day on the water.",
  },
  # ── Dubai city tour and dinner cruise ──
  {
    "slug": "dubai-city-tour", "crumb": "Dubai city tour",
    "title": "Dubai City Tour with Private Guide & Hotel Pickup | Khat Tourism",
    "desc": "Private Dubai city tours with a licensed guide: Old Dubai, the gold and spice souks, an abra ride and photo stops at the Dubai Frame and Museum of the Future. Plus a dhow dinner cruise.",
    "h1": "Dubai City Tour with a Private Guide and Hotel Pickup",
    "sub": "Old Dubai, the gold and spice souks and an abra across the creek, with a licensed guide. Add a dhow dinner cruise for the evening.",
    "hero": "abra-creek.jpg",
    "gallery": [("abra-creek.jpg", "An abra crossing Dubai Creek in front of Old Dubai"), ("al-fahidi.jpg", "A guide showing a family the wind towers of Al Fahidi"),
                ("spice-souk.jpg", "Spices and dried flowers in the spice souk"), ("dhow-marina-night.jpg", "A lit-up dhow dinner cruise in Dubai Marina at night")],
    "photos": [("burj-al-arab.jpg", "Burj Al Arab at sunset")],
    "facts": [CANCEL, ("pickup", "Hotel pickup included", "From any hotel in Dubai."), ("guide", "Licensed guide", "An English-speaking guide on every city tour."),
              ("time", "3 to 8 hours", "A half day, a full day or an evening cruise."), PAY, ("shield", "Abra ticket included", "The water taxi across Dubai Creek.")],
    "opt_title": "Which tour is right for you?", "opt_sub": "Three ways to see Dubai. Pick one to see the price.",
    "default": "dubai-half",
    "options": [
      {"id": "dubai-half", "name": "Half-day Dubai city tour", "tag": "For a first look at Dubai", "photo": "abra-creek-800.jpg",
       "blurb": "Old Dubai, the spice and gold souks and an abra ride, with photo stops at the Frame and Burj Al Arab.", "chips": ["Gold and spice souks", "Abra ride", "Photo stops"],
       "group": "half", "duration": "5 hours", "pickup": "9:00 AM", "private": 120, "unit": "starting price",
       "includes": ["English-speaking guide", "Air-conditioned transfer", "Abra ticket", "Photo stops at the Dubai Frame, Museum of the Future, Burj Khalifa and Burj Al Arab"],
       "excludes": ["Lunch", "Burj Khalifa tickets"]},
      {"id": "dubai-full", "name": "Full-day Dubai city tour", "tag": "For seeing it all", "photo": "al-fahidi.jpg",
       "blurb": "Old Dubai and Al Fahidi, the souks and the abra, plus a Monorail ride along the Palm.", "chips": ["Monorail ride", "Al Fahidi", "Souks and abra"],
       "group": "full", "duration": "8 hours", "pickup": "8:00 AM", "private": 220, "unit": "starting price",
       "includes": ["Hotel pickup and drop-off", "Licensed tour guide", "Monorail ticket", "Old Dubai, the spice and gold souks", "Bottled water"],
       "excludes": ["Lunch", "Burj Khalifa tickets"]},
      {"id": "dinner-cruise", "name": "Dhow dinner cruise", "tag": "For an evening out", "photo": "dhow-marina-night.jpg",
       "blurb": "A welcome drink, BBQ dinner and a Tanoura show on a traditional dhow, with Marina views.", "chips": ["BBQ dinner", "Tanoura show", "Marina views"],
       "group": "cruise", "duration": "3 hours", "pickup": "Boarding from 7:45 PM", "private": 180, "unit": "starting price",
       "includes": ["Welcome drink", "BBQ dinner", "Soft drinks and water", "Tanoura show", "Hotel transfer (on request)"], "excludes": ["Alcoholic drinks"]},
    ],
    "day": {
      "half": ["How the morning goes", [["Hotel pickup", "At 9:00 AM with your guide."], ["Old Dubai and the souks", "The spice and gold souks on foot."], ["Abra across the creek", "A short ride on a traditional water taxi."], ["Photo stops", "The Dubai Frame, Museum of the Future, Burj Khalifa and Burj Al Arab."], ["Drop-off", "Back at your hotel around five hours after pickup."]]],
      "full": ["How the day goes", [["Hotel pickup", "At 8:00 AM with your guide."], ["Old Dubai and Al Fahidi", "The historic quarter and the souks."], ["Abra and the creek", "Across Dubai Creek by water taxi."], ["Monorail along the Palm", "With photo stops at Dubai's landmarks."], ["Drop-off", "Back at your hotel in the evening."]]],
      "cruise": ["How the evening goes", [["Boarding", "From 7:45 PM, with hotel transfer on request."], ["Welcome drink", "As the dhow sets off."], ["Dinner and the Tanoura show", "A BBQ dinner while you cruise."], ["Back on shore", "About three hours later."]]],
    },
    "know": ["Wear comfortable shoes for the souks, and bring a hat for the midday sun.", "Lunch and Burj Khalifa tickets aren't included on the city tours.", WEATHER_TIP, REFUND_TIP],
    "faq": [FAQ_PRIVATE, ("Is the abra ride included?", "Yes. The abra ticket across Dubai Creek is included on the city tours."),
            ("Do you go up the Burj Khalifa?", "Not on the tour. We stop for photos outside, and tickets to the top are extra."),
            ("Can we do the city tour and dinner cruise on the same day?", "Yes. Take the half-day tour in the morning and the dhow cruise in the evening. Ask on WhatsApp and we'll plan it."), FAQ_PAY],
    "related": ["desert-safari-dubai", "yacht-rental-dubai", "abu-dhabi-city-tour"], "related_sub": "End the day in the desert or out on the water.",
  },
]


import yacht_page
PAGES.append(yacht_page.page(CANCEL, PAY, WEATHER_TIP, REFUND_TIP, FAQ_PAY))


def esc(s):
    return html.escape(s, quote=True)


def header(slug):
    h = HEADER
    for m in re.findall(r'\{\{CUR_([a-z-]+)\}\}', HEADER):
        h = h.replace('{{CUR_%s}}' % m, ' aria-current="page"' if m == slug else '')
    return h


def gallery(p):
    imgs = p['gallery']
    total = len(imgs) + len(p['photos'])
    cls = 'gallery' if len(imgs) >= 4 else 'gallery g2'
    out = ['<div class="%s">' % cls]
    (src, alt) = imgs[0]
    small = src.replace('.jpg', '-800.jpg')
    srcset = (' srcset="/assets/img/%s 800w, /assets/img/%s 1200w" sizes="(max-width: 760px) 86vw, 50vw"' % (small, src)) if os.path.exists(os.path.join(SITE, 'assets', 'img', small)) else ''
    out.append('    <figure class="hero-shot"><img src="/assets/img/%s"%s alt="%s" width="1200" height="675" fetchpriority="high"></figure>' % (src, srcset, esc(alt)))
    (src, alt) = imgs[1]
    out.append('    <figure class="side-shot"><img src="/assets/img/%s" alt="%s" width="800" height="450" loading="lazy"></figure>' % (src, esc(alt)))
    for src, alt in imgs[2:4]:
        out.append('    <figure><img src="/assets/img/%s" alt="%s" width="800" height="450" loading="lazy"></figure>' % (src, esc(alt)))
    out.append('    <button type="button" class="all-photos" id="open-photos">Show all %d photos</button>' % total)
    out.append('  </div>')
    return '\n'.join(out)


def photos(p):
    return '\n'.join('    <img src="/assets/img/%s" alt="%s" loading="lazy">' % (s, esc(a)) for s, a in p['gallery'] + p['photos'])


def facts(p):
    li = []
    for icon, title, text in p['facts']:
        li.append('          <li><div class="ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg></div><div><b>%s</b><span>%s</span></div></li>'
                  % (ICON[icon], esc(title), esc(text)))
    return '<ul class="facts">\n' + '\n'.join(li) + '\n        </ul>'


def related(p):
    out = []
    for slug in p['related']:
        url, img, name, line = RELATED[slug]
        out.append('          <a href="%s"><img src="/assets/img/%s" alt="" loading="lazy" width="800" height="450"><div><b>%s</b><span>%s</span></div></a>' % (url, img, esc(title_case(name)), esc(line)))
    return '\n'.join(out)


# Photos for each tour, shown as a strip under the chosen tour and in its own photo viewer. Khat's real photos come first;
# the rest are AI illustrations made with Higgsfield (see the README).
OPTION_PHOTOS = {
    "private-evening": ["land-cruisers-sunset.jpg", "dune-bashing-khat.jpg", "land-cruiser-dusk.jpg", "camp-dinner-night.jpg"],
    "kids-evening": ["mother-and-child.jpg", "child-booster-seat.jpg", "kids-sandboarding.jpg", "family-watching-dunes.jpg"],
    "romantic-dinner": ["private-dinner-setup.jpg", "couple-on-dune.jpg", "candlelight-dinner-couple.jpg", "candlelight-dinner-table.jpg"],
    "private-morning": ["land-cruiser-daytime.jpg", "sunrise-land-cruiser.jpg", "camel-morning.jpg", "family-morning-dunes.jpg"],
    "ad-private-evening": ["abu-dhabi-land-cruiser.jpg", "abu-dhabi-dune-bashing.jpg", "dune-bashing-khat.jpg", "camp-dinner-night.jpg"],
    "ad-kids-evening": ["kids-camel-abu-dhabi.jpg", "abu-dhabi-family.jpg", "child-booster-seat.jpg", "kids-sandboarding.jpg"],
    "ad-kids-morning": ["abu-dhabi-family.jpg", "kids-camel-abu-dhabi.jpg", "family-morning-dunes.jpg", "kids-sandboarding.jpg"],
    "ad-private-morning": ["land-cruiser-daytime.jpg", "sunrise-land-cruiser.jpg", "camel-morning.jpg"],
    "dune-buggy": ["dune-buggy.jpg", "dune-buggy-action.jpg"],
    "quad-bike": ["quad-bikes-dunes.jpg", "quad-bikes-ridge.jpg"],
    "morning-quad": ["land-cruiser-daytime.jpg", "quad-bikes-ridge.jpg", "sunrise-land-cruiser.jpg", "camel-morning.jpg"],
    "dubai-half": ["abra-creek.jpg", "spice-souk.jpg", "al-fahidi.jpg"],
    "dubai-full": ["al-fahidi.jpg", "abra-creek.jpg", "spice-souk.jpg", "burj-al-arab.jpg"],
    "ad-city": ["abu-dhabi-skyline.jpg", "grand-mosque.jpg"],
    "yacht-1h": ["yacht-ain-dubai.jpg", "yacht-marina.jpg", "yacht-deck.jpg"],
    "yacht-2h": ["yacht-atlantis.jpg", "yacht-proposal.jpg", "yacht-deck.jpg"],
    "yacht-3h": ["yacht-burj.jpg", "yacht-atlantis.jpg", "yacht-family.jpg"],
    "yacht-4h": ["yacht-swim.jpg", "yacht-saloon.jpg", "yacht-burj.jpg"],
}
NEW_ALT = {
    "dune-bashing-khat.jpg": "A Khat Land Cruiser dune bashing over a red dune at sunset",
    "child-booster-seat.jpg": "A child in a booster seat in the back of the car, looking out at the dunes",
    "kids-sandboarding.jpg": "A girl sandboarding down a dune towards her father",
    "candlelight-dinner-couple.jpg": "A couple at a private candlelit table in the desert at dusk",
    "candlelight-dinner-table.jpg": "A candlelit dinner table for two with lanterns and grilled food",
    "sunrise-land-cruiser.jpg": "A family beside a Khat Land Cruiser on a dune at sunrise",
    "family-morning-dunes.jpg": "A family walking along a dune crest in the morning",
    "dune-buggy-action.jpg": "Two riders in a dune buggy throwing up sand on a red dune",
    "quad-bikes-ridge.jpg": "Three quad bikes riding along a dune ridge",
}

# the new photos also join each page's "Show all photos" viewer
PAGE_EXTRA_PHOTOS = {
    "desert-safari-dubai": ["dune-bashing-khat.jpg", "kids-sandboarding.jpg", "child-booster-seat.jpg", "candlelight-dinner-couple.jpg",
                            "candlelight-dinner-table.jpg", "sunrise-land-cruiser.jpg", "family-morning-dunes.jpg"],
    "abu-dhabi-desert-safari": ["dune-bashing-khat.jpg", "kids-sandboarding.jpg", "child-booster-seat.jpg", "sunrise-land-cruiser.jpg", "family-morning-dunes.jpg"],
    "dune-buggy-dubai": ["dune-buggy-action.jpg", "quad-bikes-ridge.jpg"],
}


def photo_alt():
    alt = dict(NEW_ALT)
    for q in PAGES:
        for src, a in q['gallery'] + q.get('photos', []):
            alt.setdefault(src, a)
    return alt


def data_block(p):
    opts, alt = [], photo_alt()
    for o in p['options']:
        o = dict(o)
        # list rows show the photo at about 150px, so they get the 400px thumbnail
        thumb = os.path.join(SITE, 'assets', 'img', 'thumbs', o['photo'])
        o['photo'] = '/assets/img/' + ('thumbs/' if os.path.exists(thumb) else '') + o['photo']
        o['name'] = title_case(o['name'])
        o['gallery'] = [{"src": "/assets/img/" + f, "alt": alt[f],
                         "thumb": "/assets/img/" + ("thumbs/" if os.path.exists(os.path.join(SITE, 'assets', 'img', 'thumbs', f)) else "") + f,
                         "row": f.replace('-800', '') == os.path.basename(o['photo']).replace('-800', '')}   # already the row's photo
                        for f in OPTION_PHOTOS.get(o['id'], [])]
        opts.append(o)
    # reviews about this page's tours first; "tours" lists the tour ids a review is about (empty = the company in general)
    ids = {o['id'] for o in p['options']}
    # this page's reviews first, then the general ones; at most 8 in the rail
    # take turns between the page's tours so the first cards cover each of them
    queues = [[r for r in REVIEWS if o['id'] in r['tours']] for o in p['options']]
    mine = []
    while any(queues):
        for q in queues:
            while q and q[0] in mine: q.pop(0)
            if q: mine.append(q.pop(0))
    pool = mine + [r for r in REVIEWS if not r['tours']] + [r for r in REVIEWS if r['tours'] and r not in mine]   # pages without their own reviews borrow the best others
    reviews = [{k: v for k, v in dict(r, about=title_case(r['about'])).items() if k != 'why'} for r in pool[:max(8, len(mine))]]
    d = {"whatsapp": "971564031600", "whatsappGroup": "https://chat.whatsapp.com/DOW0NrXtuJpAb0G1cILkYL?s=cl&p=i&mlu=4&ilr=4&iam=2", "currency": "AED", "defaultOption": p['default'], "ratings": RATINGS, "mentions": MENTIONS, "options": opts, "reviews": reviews}
    if p.get('airbnb'):
        d['airbnb'] = AIRBNB
    return json.dumps(d, ensure_ascii=False, indent=1)


def ld(p):
    prices = [o['private'] for o in p['options']]
    graph = [
        {"@type": "TravelAgency", "@id": "https://khattourism.com/#organization", "name": "Khat Tourism LLC", "url": "https://khattourism.com", "telephone": "+971564031600",
         "address": {"@type": "PostalAddress", "addressLocality": "Dubai", "addressCountry": "AE"}, "sameAs": [RATINGS['tripadvisor']['url'], G_URL]},
        {"@type": "TouristTrip", "name": p['h1'], "description": p['desc'], "touristType": ["Families", "Couples", "Friends"], "provider": {"@id": "https://khattourism.com/#organization"},
         "url": "https://khattourism.com/%s/" % p['slug'],
         "offers": {"@type": "AggregateOffer", "priceCurrency": "AED", "lowPrice": str(min(prices)), "highPrice": str(max(prices)), "offerCount": str(len(prices))}},
        {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://khattourism.com/"},
                                                         {"@type": "ListItem", "position": 2, "name": title_case(p['crumb']), "item": "https://khattourism.com/%s/" % p['slug']}]},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in p['faq']]},
    ]
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)


def build(p):
    p = dict(p, photos=p.get('photos', []) + [(f, NEW_ALT[f]) for f in PAGE_EXTRA_PHOTOS.get(p['slug'], [])])
    t = TEMPLATE
    # the old footer rules give way to the shared footer's
    t = re.sub(r'\nfooter[^\n]*', '', t)
    t = t.replace('@media (min-width: 1041px) { footer { padding-bottom: 32px; } }', '')
    t = t.replace('.dock-bar { position: fixed;', FOOTER_CSS + '\n\n.dock-bar { position: fixed;', 1)
    rep = {
        'TITLE': esc(p['title']), 'DESC': esc(p['desc']), 'SLUG': p['slug'], 'HERO': p['hero'], 'LD': ld(p), 'DATA': data_block(p),
        'HEADER': header(p['slug']), 'FOOTER': FOOTER.replace('AI-generated illustrations.', 'AI-generated illustrations.' + AIRBNB_NOTE) if p.get('airbnb') else FOOTER, 'CRUMB': esc(title_case(p['crumb'])), 'H1': esc(p['h1']), 'SUB': esc(p['sub']),
        'GALLERY': gallery(p), 'FACTS': facts(p), 'OPT_TITLE': esc(p['opt_title']), 'OPT_SUB': esc(p['opt_sub']),
        'KNOW': '\n'.join('          <li>%s</li>' % k for k in p['know']),
        'FAQ_HTML': '\n'.join('        <details><summary>%s</summary><p>%s</p></details>' % (esc(q), esc(a)) for q, a in p['faq']),
        'RELATED': related(p), 'RELATED_SUB': esc(p['related_sub']), 'PHOTOS': photos(p),
        'DAY': json.dumps(p['day'], ensure_ascii=False),
        'EXTRA': p.get('extra', ''), 'EXTRA_CSS': p.get('extra_css', ''), 'EXTRA_JS': p.get('extra_js', ''),
    }
    for k, v in rep.items():
        t = t.replace('{{%s}}' % k, v)
    # phones preload the 800px hero when there is one
    small = p['hero'].replace('.jpg', '-800.jpg')
    if os.path.exists(os.path.join(SITE, 'assets', 'img', small)):
        t = t.replace('<link rel="preload" as="image" href="/assets/img/%s" fetchpriority="high">' % p['hero'],
                      '<link rel="preload" as="image" href="/assets/img/%s" imagesrcset="/assets/img/%s 800w, /assets/img/%s 1200w" imagesizes="(max-width: 760px) 86vw, 50vw" fetchpriority="high">' % (p['hero'], small, p['hero']))
    left = re.findall(r'\{\{[A-Z_]+\}\}', t)
    assert not left, (p['slug'], left)
    for m in re.finditer(r'<script type="application/(?:ld\+)?json"[^>]*>(.*?)</script>', t, re.S):
        json.loads(m.group(1))
    os.makedirs(os.path.join(SITE, p['slug']), exist_ok=True)
    open(os.path.join(SITE, p['slug'], 'index.html'), 'w', encoding='utf-8').write(t)
    links = sorted(set(re.findall(r'href="(https://khattourism\.com[^"]*)"', t)))
    print('%-26s %6d bytes  options=%d  links to khattourism.com: %s' % (p['slug'], len(t), len(p['options']), [l for l in links if 'canonical' not in l] or 'none'))


if __name__ == '__main__':
    for page in PAGES:
        build(page)
