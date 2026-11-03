# Yacht rental landing page: Khat Tourism

A single static page with no framework: about 57 KB of HTML, 88 KB of fonts and the logo. Tested locally with Lighthouse, it scores 100 for performance, accessibility, best practices and SEO on both mobile and desktop. On mobile, the largest element appears in 1.9 s (Khat's current tour pages take about 6.5 s).

## Fill in before launch

Everything below lives in the `charter-data` block near the top of `<body>` in `index.html`.

1. **Price.** Khat's current yacht page says "AED 800" with a duration of "3 Hours", but doesn't say whether that's per hour or per trip. The page assumes **AED 800 per hour**. Correct `pricePerHour` and the `"price": "800"` in the JSON-LD at the top of the file.
2. **The boat.** Fill in its name, length, maximum guests and cabins. Remove `"sample": true` when the details are real; that also removes the yellow "Sample details" badge. To add more boats, add more entries to `boats`. The booking card uses the first one.
3. **Photos.** Add real photos of the actual boat, about 1600×1000 in WebP or JPG. Put them in `img/` and set `"photo": "img/boat-name.webp"`. Until then the card shows a line drawing.
   - Don't reuse the "FAVOR" superyacht photo from the current tour page. It's a stock photo of a different boat.
4. **Departure point.** The page says Dubai Marina, and the FAQ says "Dubai Marina or Dubai Harbour", both taken from Khat's current page. Confirm which applies.
5. **Add-ons.** Only catering and hotel transfer are listed, because those are the only ones on Khat's current page. Add others (cake, decorations, a jet ski) to `addons` only if Khat can actually supply them.
6. **Payment.** "How booking works" lists card, bank transfer, PayPal and cash, copied from Khat's booking form. Confirm that cash is accepted for yachts.

## Deploy (Hostinger / Laravel)

1. Upload this folder to `public/yacht-rental-dubai/`. The page is then live at **https://khattourism.com/yacht-rental-dubai/**.
   - Keep the trailing slash. The fonts and images use relative paths, so the page only works at the folder URL.
2. Add the URL to `sitemap.xml`.

Because the page is a static file, Hostinger's CDN can cache it, so it stays fast. Khat's tour pages can't be cached this way.

## Tracking (GTM-542BQV7F, already on the page)

GTM loads straight away instead of waiting for the first scroll, so ad visitors who leave quickly are still counted. The page sends two `dataLayer` events:

| Event | Fires on | Parameters |
|---|---|---|
| `whatsapp_lead` | any WhatsApp button | `cta`, `hours`, `guests`, `occasion`, `value`, `currency` |
| `call_click` | any phone link | `cta`, `value`, `currency` |

In GTM:
1. Create a Custom Event trigger for each of the two events.
2. Attach a Google Ads conversion tag to each. Set value to a Data Layer Variable for `value` and currency to `AED`.
3. Optionally, add GA4 event tags to the same triggers.
4. Publish.

Then in Google Ads, set both as **primary** conversions.

## Google Ads

Use **https://khattourism.com/yacht-rental-dubai/** as the final URL. The keyword list is in `../landing-page-niches.md`.
