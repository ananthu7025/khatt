# Khat Tourism: new website

`site/` is the whole website: static HTML with no framework, sharing one header, one footer and one `assets/` folder.

| Page | Path | Tours |
|---|---|---|
| Homepage | `/` | 6 category cards, 3 most-reviewed trips, reviews, FAQ |
| Desert safari Dubai | `/desert-safari-dubai/` | Private evening, kids-friendly, candlelight dinner for two, morning |
| Yacht rental | `/yacht-rental-dubai/` | 1-hour Marina, 2-hour Palm and Atlantis, 3-hour Burj Al Arab, 4-hour with swim stop. Includes the route map, drawn from OpenStreetMap coastline data. |
| Abu Dhabi desert safari | `/abu-dhabi-desert-safari/` | Private evening, kids-friendly evening, kids-friendly morning, private morning |
| Abu Dhabi city tour | `/abu-dhabi-city-tour/` | Full-day city tour, Grand Mosque tour |
| Dune buggy and quad | `/dune-buggy-dubai/` | Dune buggy, quad bike, morning safari with quad |
| Dubai city tour | `/dubai-city-tour/` | Half day, full day, dhow dinner cruise |
| Cancellation policy | `/cancellation-policy/` | Khat's own terms |

**Links:** no page links to the old khattourism.com site. The only mentions are each page's canonical tag and structured data, which hold the address the page will have once it goes live there.

**Deep links:** a tour page opens on a specific tour when given its id, for example `/desert-safari-dubai/?safari=kids-evening` or `/abu-dhabi-desert-safari/?safari=ad-kids-morning`. Use these for Google Ads sitelinks.

**Booking on phones (GetYourGuide-style):** a bar at the bottom shows the chosen tour's price and a "Check availability" button. That button, or tapping a tour, opens a booking sheet with three steps:
1. date and guests
2. choose the option: pickup or start time, free-cancellation date, "pay on the day" and price
3. review, add the pickup hotel, and send the request on WhatsApp with every detail filled in

Desktop keeps the booking card beside the page. The sheet sends `open_booking`, `check_availability` and `select_option` to the dataLayer, so the booking funnel shows in GA4.

**Tour photos:** the chosen tour shows a strip of its own photos, and each one opens that tour's photo viewer. The lists are `OPTION_PHOTOS` in `build.py`, with Khat's real photos first.

**Reviews follow the tour:** the featured reviews are a Tripadvisor shortlist, explained in `review-shortlist.md`. Each has a `tours` list in `build.py`. A page takes turns between its tours' reviews, and choosing a tour moves its reviews to the front.

**Airbnb:** the homepage and the Dubai desert safari page say "Also rated 4.96 from 55 reviews on Airbnb Experiences", as text with no Airbnb logo, plus a trademark note in the footer. Update the numbers in `_build/site/airbnb.py`.

**Lighthouse (mobile, local):**

| Page | Performance | Accessibility, best practices, SEO |
|---|---|---|
| Homepage | 95 | 100 |
| Category pages | 94 to 99 | 100 |
| Yacht page | 91 | 100 |
| Cancellation policy | 100 | 100 |

## Preview

```sh
cd site && python3 -m http.server 8080      # http://127.0.0.1:8080/
```

## Editing and rebuilding

The pages are generated. Edit the sources in `_build/`, then rebuild:

```sh
cd _build/site && python3 build.py && python3 make_home.py && python3 policy.py
```

| File | What it controls |
|---|---|
| `_build/site/build.py` | All six tour pages: titles, photos, tours, prices, includes, day plans, FAQ. One entry per page in `PAGES`. |
| `_build/site/yacht_page.py` | The yacht page entry, including its "Where you'll go" route map. |
| `_build/site/yacht-chart/` | The map. `chart.py` turns the OpenStreetMap coastline (`osm-coastline.json`) into land shapes and routes, and fails if a route crosses land; then `python3 chart_svg.py chart.json chart.svg.html`. |
| `_build/site/airbnb.py` | The Airbnb rating line and footer note. |
| `_build/site/template.html` | The shared layout of those pages (made once from the desert safari page). |
| `_build/site/partials/` | The header and footer used on every page. |
| `_build/site/home_source.html` + `make_home.py` | The homepage; category cards and most-reviewed trips are in `make_home.py`. |
| `_build/site/policy.py` | The cancellation policy page. |
| `_build/_archive/` | Earlier versions, including the first standalone yacht page. Not used. |

## Style rules

- **Title Case for tour names and page headings (H1)**, for example "Private Evening Desert Safari" and "Candlelight Dinner for Two". Short joining words stay lowercase: and, for, with, of, the, in, from.
  - `_build/site/titles.py` applies this automatically to tour names, category names, breadcrumbs and review labels. New tours follow the rule without extra work.
- **Sentence case for everything else:** section headings ("Which safari is right for you?"), buttons, navigation, and body text.
- **Ratings** always appear as two matching boxes, Tripadvisor and Google, each with logo, name, score and review count.
- **Two buttons together** share one width on desktop and stack at full width on phones.

## AI-generated photos

Twenty-two photos were made or edited with Higgsfield (GPT Image 2.5, 2K) for scenes Khat had no photos of. The footer says some photos are AI-generated illustrations.

| File | Used on |
|---|---|
| `yacht-marina.jpg` | Homepage yacht card, "Private Yacht Rental" link cards |
| `yacht-deck.jpg`, `yacht-proposal.jpg`, `yacht-swim.jpg` | Yacht page gallery; the swim photo is also on the 4-hour cruise |
| `yacht-atlantis.jpg`, `yacht-burj.jpg`, `yacht-ain-dubai.jpg` | Yacht page gallery and the 2-, 3- and 1-hour cruises |
| `yacht-family.jpg`, `yacht-saloon.jpg` | Yacht page gallery |
| `abra-creek.jpg` | Dubai city tour page, main photo and the half-day tour |
| `al-fahidi.jpg` | Dubai city tour page gallery and the full-day tour |
| `spice-souk.jpg` | Dubai city tour page gallery |
| `dhow-marina-night.jpg` | Dubai city tour page gallery and the dhow dinner cruise |
| `land-cruisers-sunset.jpg`, `abu-dhabi-land-cruiser.jpg` | Khat's own photos with the Khat logo added to the cars. The originals are in `_build/_archive/unbranded-originals/`. |
| `dune-bashing-khat.jpg`, `sunrise-land-cruiser.jpg` | Private evening and morning safaris (Khat-branded car) |
| `child-booster-seat.jpg`, `kids-sandboarding.jpg`, `family-morning-dunes.jpg` | Kids-friendly and morning safaris, Dubai and Abu Dhabi |
| `candlelight-dinner-couple.jpg`, `candlelight-dinner-table.jpg` | Candlelight dinner for two |
| `dune-buggy-action.jpg`, `quad-bikes-ridge.jpg` | Dune buggy and quad tours |

The desert scenes show open desert only, with no city skyline: the safari dunes are far from the city.

The yacht page shows the cruise experience, not a named boat. Once Khat sends photos of their actual yacht, put them first in the yacht page gallery.

List rows use 400px thumbnails from `site/assets/img/thumbs/`. Make one for each new photo (the build uses it automatically when it exists).

## Demo

https://khat-demo.sanjaynediyara.workers.dev (Cloudflare, StartGlobal AI Projects account). The demo copy has no Google Tag Manager, so test clicks never reach Khat's Google Ads, and every page is noindex. To update it:

```sh
cd _build && python3 demo.py && npx wrangler deploy --config demo-wrangler.jsonc
```

## Deploy

Upload the contents of `site/` to the web root (Laravel's `public/`), so that `public/index.html`, `public/assets/` and `public/desert-safari-dubai/` and the other page folders sit side by side. Point the `/` route at `index.html`.

Every page loads Google Tag Manager (GTM-542BQV7F) straight away and sends:
- `whatsapp_lead` on any WhatsApp tap
- `call_click` on any phone link
- `select_item` on homepage cards

Set the first two up as Google Ads conversions in GTM.

## Before going live: what Khat needs to confirm

1. **Prices and units.** Desert and Abu Dhabi safaris are priced per Land Cruiser, the candlelight dinner per couple and the yacht per hour. The buggy (AED 450), quad (350), Abu Dhabi city tour (150), Grand Mosque (110), Dubai city tours (120 and 220) and dinner cruise (180) are shown as "starting price", because their tour pages don't say whether that's per person or per car.
2. **"Only private tours".**
   - The half-day city tour page mentions a "coached transfer".
   - The dhow dinner cruise is usually a shared boat.
   - Confirm both, or reword those two tours.
3. **Yacht price and photos.** The page reads Khat's AED 800 yacht price as per hour (AED 800 to 3,200 for 1 to 4 hours). Confirm this, and send real photos of the boat.
4. **Photos.**
   - The Grand Mosque and Abu Dhabi skyline photos look like stock images.
   - Confirm Khat may use every photo, and add their own where possible.
   - The Dubai city tour and yacht scenes are AI illustrations (see above). Replace them with real photos when there are some.
5. **Review excerpts.** Paste the chosen excerpts into the `text` field of the featured reviews in `build.py` and `make_home.py`, and tag each with the tours it's about. Update the rating counts monthly.
   - Aim for two or three reviews per tour: one each for kids, the candlelight dinner, the morning safari, buggy and quad, the city tours and the yacht.
   - Reviewers' profile photos belong to them and can't be copied from Tripadvisor or Google. For real faces, use guests' own photos with their written permission.
6. **Terms and privacy pages.** Not built yet; they need Khat's own legal text. The footer links only to the cancellation policy.
7. **Airbnb.** Never put this website, the phone number or a direct-booking discount in the Airbnb listing or in messages to Airbnb guests.
8. **Online payment.** Booking is WhatsApp or phone only until a checkout is built for the new site.
