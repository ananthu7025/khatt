# Homepage: Khat Tourism

A static homepage in the same design system as `/desert-safari-dubai/` and `/yacht-rental-dubai/`.

Lighthouse, tested locally:

| | Performance | Accessibility | Best practices | SEO | Largest element shown in |
|---|---|---|---|---|---|
| Mobile | 94 | 100 | 100 | 100 | 3.1 s |
| Desktop | 100 | 100 | 100 | 100 | 0.6 s |

**Preview all three pages together** by serving the whole `khat/` folder:
`python3 -m http.server 8767`, then open http://127.0.0.1:8767/home/

## What's on it, top to bottom

1. **Header:** logo, links to Desert safari, Yacht, Abu Dhabi, Buggy and quad, Reviews, the phone number and a WhatsApp button.
2. **Hero:**
   - "Private desert safaris and tours in Dubai"
   - one line on what's included (own Land Cruiser, hotel pickup, free cancellation)
   - two buttons: "Plan my trip on WhatsApp" and "See all tours"
   - the Tripadvisor and Google ratings
   - a photo collage with a "Rated 5.0, 1,509 reviews" badge
3. **Category shortcuts:** Desert safaris, On the water, Abu Dhabi, Buggy and quad, City tours, All tours, each with a "from" price. Tapping one filters the tour grid.
4. **"Pick your trip":** 14 tour cards with filter chips. Each card has a photo, category, name, one line, duration, the Tripadvisor rating where a matching listing exists, and the From price. On phones they become compact rows with a small photo on the left.
5. **"Why travellers book with Khat":** private only, hotel pickup, free cancellation, families welcome.
6. **Reviews:** the same module as the safari page.
7. **"Booking takes a minute":** three steps.
8. **FAQ.**
9. **Final call to action** (crimson band) and the footer with every tour linked.
10. **Mobile:** a "From AED 110 / Plan my trip" bar appears once the hero buttons scroll away.

## Editing

Tours, ratings and featured reviews all live in the `home-data` block at the top of `<body>`.

**Tour cards**
- **Desert safaris** link to `/desert-safari-dubai/?safari=<id>`, which opens that safari already selected. Use the same links as Google Ads sitelinks.
- **The yacht** links to `/yacht-rental-dubai/`.
- **Every other tour** links to its existing page on khattourism.com.

**Prices** are the From prices on each tour's page. The `unit` (per Land Cruiser, per couple, per hour) is shown only where it's confirmed. Fill it in for:
- Abu Dhabi city tour (AED 150)
- Grand Mosque tour (AED 110)
- Dune buggy (AED 450)
- Quad bike (AED 350)
- Dinner cruise (AED 180)
- Dubai city tour (AED 120)
- Layover safari (AED 500)

If those are per person, the "only private tours" promise needs checking for them. The half-day city tour's page even lists an "air-conditioned coached transfer".

**Tripadvisor ratings** on cards come from Khat's matching product listings on Tripadvisor:

| Homepage card | Tripadvisor listing | Rating |
|---|---|---|
| Private evening desert safari | Exclusive Evening Desert Safari | 5.0 (218) |
| Kids-friendly desert safari | Kids Friendly Desert Safari | 5.0 (74) |
| Abu Dhabi kids-friendly morning safari | Abu Dhabi Kids Friendly Morning Desert Safari | 5.0 (48) |

The other tours have no separate Tripadvisor listing, so they show no rating.

**Photos** come from Khat's tour pages:
- Abu Dhabi skyline, Grand Mosque, Burj Al Arab and the dhow cruise look like stock images. Swap in Khat's own when possible.
- The yacht card uses the line drawing until there are real boat photos.

## Deploy as the homepage

- Upload this folder to Laravel's `public/home/`. Assets use absolute `/home/...` paths, so the folder must sit at `/home/`.
- Point the homepage route at the file: `Route::get('/', fn () => response()->file(public_path('home/index.html')));`. Or paste the HTML into the home Blade view.
- Keep `/desert-safari-dubai/` and `/yacht-rental-dubai/` deployed alongside it; the cards link there.

## Tracking (GTM-542BQV7F)

| Event | Fires on | Parameters |
|---|---|---|
| `whatsapp_lead` | any WhatsApp button | `cta` (where on the page) |
| `call_click` | any phone link | |
| `select_item` | a tour card is clicked | `item_id`, `item_name`, `item_category`, `price`, `index` |
| `tour_filter` | a category or filter is chosen | `category` |

Mark `whatsapp_lead` and `call_click` as Google Ads conversions. `select_item` is a standard GA4 ecommerce event; it shows which tours get attention from the homepage.
