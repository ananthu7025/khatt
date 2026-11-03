# Khat Tourism (khattourism.com): Website, Speed, UX & SEO Audit

*Checked 28 Oct 2026. Site: Laravel (PHP 8.3) on Hostinger, about 22 tours, 1 package and 27 blog posts (64 URLs in the sitemap).*

## The short version

The site looks premium and already has a lot of content (27 blog posts, FAQs, detailed tour pages). But three problems are costing money on Google Ads right now:

1. **Tour pages are slow.** The ads most likely send people to these pages, and the server takes about 2.5–3 seconds to build each one. In real Chrome on fast broadband, nothing appeared on screen for **6.5 seconds**. Google's target is under 2.5 seconds, and on a phone with 4G it will be slower still.
2. **Conversion tracking is probably undercounting.** Analytics and Tag Manager are deliberately delayed until the visitor scrolls or taps, or about 3.5 seconds pass. On a slow page, many ad visitors leave before tracking even starts. I found no Google Ads conversion tag on the site, and WhatsApp clicks (the main way people contact them) don't appear to be tracked as conversions.
3. **The trust signals look fake.** Tour pages show "5.0 ★ (0)", which means zero reviews, and every tour card says "5.0 Rating". Meanwhile the hidden search data claims 4.9 stars from 280 reviews. The footer's Facebook, Instagram and Twitter icons link nowhere, and there is no link to their Google reviews.

SEO is at an early stage. The content is there, but technical bugs stop Google from using it well. For example, the **homepage's title in Google is a single tour's name**, and the structured data on every tour and blog page is broken by a coding bug.

---

## 1. Speed

| What I measured | Result | Target |
|---|---|---|
| Tour page: server build time (Hostinger header `x-hcdn-upstream-rt`) | **2.4 s** | < 0.5 s |
| Tour page: time to first byte (TTFB) | 2.8–3.0 s with curl, **4.3 s in Chrome** | < 0.8 s |
| Tour page: first content and largest image visible (Chrome, desktop broadband) | **6.5 s** | < 2.5 s |
| Other pages (home, blog, about): server time | about 0.3 s, total about 1.0–1.3 s | fine |
| Homepage: total download | **8.9 MB, 59 images, none lazy-loaded** | < 2 MB |
| Tour page (Chrome) | 35 requests, 1.9 MB, 13 third-party domains | — |

All 22 tour pages took 3.5–4.6 s to return their HTML, compared with about 1 s for every other page. So the problem is in the tour-page code, not the hosting.

**Fixes, in order of impact:**

1. **Find out why tour pages take 2.4 s to build.** This is almost certainly slow or repeated database queries. Install Laravel Debugbar or Telescope locally and look at the query count on a tour page. Then cache the result with `Cache::remember()` for the tour data, reviews, related tours and FAQs. On its own, this should take tour pages from about 3 s to under 0.5 s.
2. **Turn on page caching.** Every page is sent with `cache-control: no-cache, private` plus a session cookie, so Hostinger's CDN can never cache the HTML (`x-hcdn-cache-status: DYNAMIC`). Public pages like tours and blog posts don't need a session for anonymous visitors.
3. **Compress the images.** Seven tour photos are stored as **PNG files of 450–880 KB each** (1200×675). In WebP format they would be about 80–120 KB, so roughly 5 MB could be cut from the homepage alone.
   - Add `loading="lazy"` to every image below the first screen. Right now the carousels download every slide straight away.
   - Serve smaller images to phones (`srcset`).
4. **Trim the page code.** The site loads 3 font families × 6 weights each, and the Google Fonts and Font Awesome stylesheets are each loaded twice. The second copy is render-blocking, which cancels out the async trick used for the first. It also loads 5 different code libraries (jsDelivr, cdnjs, unpkg and others), GSAP plus ScrollTrigger plus AOS for animations, and the Google Translate widget. Keep 1–2 font families and self-host the CSS.
5. Run **pagespeed.web.dev** on a tour URL. I couldn't run Lighthouse myself because Hostinger's bot protection returned **403 Forbidden** to it. If PageSpeed Insights also gets a 403, relax the Hostinger security setting, or Google's own tools can't measure the site. (AdsBot-Google did get through when I tested, which is good.)

## 2. Google Ads tracking

What I found in the page code and the Tag Manager container (GTM-542BQV7F):

- There is a GA4 property (G-8D7DBPNTPB) with custom events `BOOKING`, `FINALLEADFORMSUBMISSION` and `ads_conversion_submit_lead_form`. GA4 is linked to Google Ads.
- **There is no Google Ads conversion tag (AW-…)** on the site or in GTM. Ads must be relying on imported GA4 events, if anything.
- **GTM and GA4 are only loaded after the first scroll or tap, or about 3.5 s of idle time.** Combined with a 4–6 s load, anyone who bounces is never recorded. Expect Ads to show many more clicks than GA4 shows sessions.
- GA4 is loaded twice, once directly and once via GTM's Google tag with the same ID. Check for double-counted page views.
- **WhatsApp is the main call to action** (the floating button, "WhatsApp Concierge", "WhatsApp Booking" and the quotation form all go to WhatsApp). I saw no conversion set up for WhatsApp clicks.
- **There is no tap-to-call phone link anywhere on the site** (no `tel:` link).

**Fixes:**

1. Load GTM normally in the `<head>`, without the delay. It is async and barely affects speed.
2. In GTM, add the Google Ads Conversion Linker plus Google Ads conversion tags for:
   - **Booking submitted.** Pass the booking value in AED, so Ads can optimise for revenue.
   - **WhatsApp click.** Use a click trigger on links containing `wa.me`.
   - **Phone click**, once a call button exists.
3. Turn on **Enhanced Conversions**. The booking form already collects email and phone.
4. In Google Ads, set only real leads and bookings as *Primary* conversions, not generic `form_submit` or page-view events.

## 3. Customer experience (mobile)

Mobile screenshots are in `/var/folders/7_/bmsqjq2d3470y9t7441r3_p00000gn/T/claude-chrome-screenshots-7vCjll/`.

- **About a third of the phone screen is covered by fixed bars:**
  - header: 88 px
  - sticky price bar: 78 px
  - app-style bottom menu (Home / Tours / Packages / Bookings / Profile): 70 px
  - floating WhatsApp bubble: 58 px

  A tourist coming from an ad doesn't need "Bookings / Profile" or "Login / Register". On tour pages, keep just one sticky bar: **"AED 750 · Book now · WhatsApp"**.
- **The floating WhatsApp bubble covers content.** It sits over the tour title on tour pages and directly on top of the "WhatsApp Concierge" button on the homepage.
- **The booking form is near the bottom of a very long page.** On mobile it starts about 9,700 px down a 14,000 px page. The sticky "Book Now" button helps.
- **The form has 12 fields**, including coupon, payment method and a 3-mode pickup picker. Cut the first step to **date, guests, name and WhatsApp number**, and collect the hotel and pickup details afterwards on WhatsApp.
- **Their best trust point is hidden.** They accept **Cash on Tour**, which is a big deal for first-time visitors. Put "No prepayment needed · Pay on the day" and the cancellation terms right next to the Book button.
- **Show real reviews.** Remove "5.0 ★ (0)" and "5.0 Rating" from tours that have no reviews. Instead, show the real Google rating and review count, with a link to the Google Business Profile. The "Google Reviews & Trust" testimonials on the homepage don't link to Google, so visitors can't verify them.
- **Explain the price.** AED 750 for a private evening safari sits next to much cheaper shared safaris in the same search results. Say clearly above the fold why private is worth it: own 4x4, no strangers, flexible pickup, private camp setup.
- **The homepage search box isn't needed.** With about 22 tours, the category, location, date and duration filters are an extra step. Use 4–6 big category tiles instead (Desert Safari, Abu Dhabi, Buggy & Quad, Yacht, City Tours).
- Small text and buttons: 41 text elements under 12 px, and 20 buttons or links smaller than 32 px.
- Footer social icons (Facebook, Instagram, Twitter) link to `#`.

## 4. SEO

### Bugs to fix first

1. **The homepage title and description are a tour's.** Google sees the homepage as *"Private Dubai desert safari with private dinner - Dubai |... | KHAT TOURISM LLC"*, and the homepage also carries that tour's schema. Give it its own title, for example *"Private Desert Safari Dubai & Abu Dhabi Tours | Khat Tourism"*, with its own description.
2. **Structured data is broken on every tour and blog page.** Blade (Laravel's template engine) treats `"@context"` inside the JSON-LD as a Blade directive, so **raw PHP code ends up in the page source**. As a result, the `TouristTrip`, `Offer` and `FAQPage` schema can't be read on any tour page (6 broken blocks per tour page, 3 per blog post).
   - Fix: write `@@context` in the Blade file, or build the JSON-LD with `json_encode()` in PHP.
   - Then check a tour page in Google's Rich Results Test.
3. **The schema points to pages that don't exist.** The `Product` schema URLs use `www.` and a `best-…` slug, for example `/tours/best-dubai-private-evening-desert-safari-dubai-khat-tourism`, which returns **404**.
   - The schema also claims `aggregateRating 4.9 / 280 reviews` while the page shows 0 reviews. Google treats that mismatch as spammy markup.
   - Use only real, visible review counts.
4. **The site is duplicated on www and non-www.** `www.khattourism.com` and `khattourism.com` both load normally, and each one's canonical tag points to itself, so Google sees two copies of the site. Also, `robots.txt` points to the www sitemap, but the sitemap lists non-www URLs.
   - Fix: add a 301 redirect from www to non-www in Hostinger.
   - Update `robots.txt` to match.
5. **Category pages can't rank.** `/tours?category=desert-safari`, `?category=yacht-marina` and the other category pages all have the same title and a canonical pointing back to `/tours`.
   - These should be real pages with their own content: `/desert-safari-dubai`, `/abu-dhabi-desert-safari`, `/dune-buggy-dubai`, `/yacht-rental-dubai`, `/dubai-city-tour`.
   - These are the high-volume searches, and the same pages make better Ads landing pages.
6. **The title template is messy:**
   - Blog titles are cut off mid-word with "...", for example *"Private Morning Desert Safari With Quad Bike - Dubai | Kh..."*.
   - One blog title literally starts with *"SEO Title:"*.
   - Tour titles repeat the brand twice (*"…- Dubai | Khat Tourism - Book Dubai Tour | KHAT TOURISM LLC"*), and the on-page H1 includes *"- Dubai | Khat Tourism"*.
   - Fix: make titles `{Tour name} | Khat Tourism`, kept under 60 characters, with no "...".
7. **The sitemap `lastmod` is always "right now"**, so Google learns to ignore it. Use each page's real last-updated date.

### Off-site signals (where most of the next gains are)

- **Google Business Profile:** this matters most for "desert safari near me" and for the Map Pack.
  - Make sure it's claimed and set to the *Tour operator* category, with photos, opening hours and the website link.
  - Ask every guest for a review via a WhatsApp message after the tour.
  - Link the website to it.
- **Their listings are scattered:**
  - Trustpilot has **0 reviews**.
  - A Magpie tour listing uses the name "Khat Tours and Safaris".
  - Directory sites (vymaps, wiuwi) list the Al Dhaffra Building, Damascus St, Al Qusais address.
  - The website says "since 1996" while other listings say "10+ years".

  Use one name, address and phone number everywhere, and one story.
- The organisation schema's `sameAs` link is a **WhatsApp group invite**. Replace it with their Instagram, Facebook, TripAdvisor and Google Business Profile URLs.
- Get listed and reviewed on **TripAdvisor, GetYourGuide and Viator**. Tourists check these, and AI assistants cite them.

### What's already good

- 27 blog posts covering real tourist questions (what to wear, morning vs evening, layover safari, Global Village).
- One H1 per page, alt text on every image, HTTPS, a proper 404 page, and Gzip compression.
- The sitemap exists and lists every tour and blog post, `robots.txt` allows crawling, and the Search Console verification tag is in place.

## 5. Google Ads: quick wins

- Send each ad group to the **matching tour page**, not the homepage. The homepage has the wrong title and is the heaviest page.
- Landing-page speed is part of **Quality Score**. Fixing tour-page speed lowers cost per click.
- Add **call, location (linked to the Google Business Profile), price and sitelink assets**, with the sitelinks pointing to the main tour pages.
- Once WhatsApp and booking conversions are tracked properly, switch bidding to *Maximise conversions*, then *Target CPA*.
- I haven't seen their Ads account. With read access, the next step would be an audit of the search terms, wasted spend and keyword-to-landing-page match.

## Priority checklist

| # | Fix | Effort | Impact |
|---|---|---|---|
| 1 | Cache or fix the slow tour-page queries (2.4 s → < 0.5 s) | 1–2 days dev | Very high |
| 2 | Convert PNGs to WebP and lazy-load images | half a day | High |
| 3 | Load GTM normally and add Ads conversions (booking, WhatsApp, call) | half a day | Very high |
| 4 | Add a tap-to-call button and remove "5.0 (0)" ratings | 1 hour | High |
| 5 | Fix the homepage title and the `@@context` schema bug | 1 hour | High |
| 6 | 301 redirect www → non-www and fix robots.txt | 15 min | Medium |
| 7 | Simplify the mobile layout (one sticky bar, shorter form, "Pay on tour" message) | 1–2 days | High |
| 8 | Turn categories into real landing pages | 2–3 days | High (SEO and Ads) |
| 9 | Google Business Profile, review collection, consistent listings | ongoing | High |
| 10 | Clean up title templates and sitemap dates | 1–2 hours | Medium |
