# Desert safari detail page: Khat Tourism

A static page laid out like a GetYourGuide product page. Tested locally with Lighthouse:

| | Performance | Accessibility | Best practices | SEO | Largest element shown in |
|---|---|---|---|---|---|
| Mobile | 94 | 100 | 100 | 100 | 3.1 s |
| Desktop | 100 | 100 | 100 | 100 | 0.6 s |

Everything that changes lives in the `safari-data` block at the top of `<body>`.

## Heading

**"Desert Safari Dubai: Private Tours with Hotel Pickup"**
- **"Desert Safari Dubai"** is how people actually search. "desert safari dubai" gets 40,500 searches a month in the UAE, more than any other safari term. Matching the ad keyword word for word helps Quality Score.
- **"Private Tours"** is Khat's selling point. VIP, premium and private searches cost less to win than the general term.
- **"with Hotel Pickup"** makes it clear this is a trip they're picked up for, not a drive they make themselves.

The page title, meta description and Open Graph tags use the same wording.

## Safari options

"Which safari is right for you?" shows four rows, each clearly different:

| Option | Tag | Price |
|---|---|---|
| Private evening safari | For groups and friends, marked "Most reviewed" | AED 750 per Land Cruiser |
| Kids-friendly safari | For families | AED 750 per Land Cruiser |
| Candlelight dinner for two | For couples | AED 1,500 per couple |
| Morning safari | For hot days and early risers | AED 400 per Land Cruiser |

Each row in `options` has:
- `photo`: the small picture on the left
- `tag`: who the trip is for
- `hot`: an optional red badge
- `blurb`: one line
- `chips`: three selling points

Prices and the included/excluded lists come from each tour's page on khattourism.com. Choosing a row updates the booking card, "How the day goes" and "What's included".

Khat's other safaris aren't shown: the BBQ dinner safari, the morning safari with quad bike, the kids-friendly morning safari and the layover safari. To add one, copy a row into `options` and fill in its details from its tour page.

## Reviews and logos

**Official logo files** are in `img/logos/`, downloaded from each platform's own servers:
- `tripadvisor-lockup.svg` and `tripadvisor-mark.svg` from `static.tacdn.com`
- `google-g.png` from `gstatic.com`

Check both platforms' brand rules before launch:
- Tripadvisor: Management Center, under marketing tools
- Google: the Business Profile marketing kit at marketingkit.withgoogle.com

**Ratings**, read off both platforms on 31 Oct 2026:

| | Score | Reviews | Breakdown |
|---|---|---|---|
| Tripadvisor | 5.0 | 1,396 | 1,355 / 34 / 4 / 0 / 3, from excellent to terrible |
| Google | 5.0 | 113 | 111 five-star, 2 three-star |

The section heading adds both counts together: "Rated 5.0 from 1,509 reviews". Update `ratings` monthly.

**Featured reviews** (`reviews`) are real reviews: three from Tripadvisor and three from Google. Each has the reviewer, the date and a link.
- Paste the excerpt you want to show into `"text"`. The card turns into a quote, with the platform logo, rating, reviewer and a "Read on Tripadvisor" or "Read on Google" link.
- Keep excerpts short and word-for-word, and always keep the link.
- Until text is added, each card shows a link to the full review.
- The Google reviews all link to the business's reviews page. Replace `date` (currently "2026") with the month shown on Google.

**Don't add review stars to the structured data.** Google doesn't allow ratings taken from other sites in your own markup, so the JSON-LD has offers and FAQ but no `aggregateRating`.

## Check before launch

**Prices.** These are copied from each tour page on khattourism.com. Khat only runs private tours, so `private` is the price per Land Cruiser (or per couple for the candlelight dinner). The page has no shared option. Some don't add up:
- The BBQ dinner safari is AED 200 per person or AED 560 private, yet the private safari without dinner is AED 750.
- Google's booking links show different prices: private morning AED 600 (website AED 400) and kids-friendly morning AED 250 (website AED 500).
- One product, private safari with private dinner, shows AED 150 per person and isn't on this page.

Pick one price per product and use it everywhere.

**Other gaps:**
- **Capacity:** how many guests fit in one private Land Cruiser? Add it to the FAQ.
- **Children's prices:** the booking system has AED 0 for children on every tour, so the page asks for them on WhatsApp.
- **Photos:** they come from Khat's own tour pages. Confirm Khat owns them, and add more of the branded Land Cruisers shown on Tripadvisor.
- **"Most reviewed" badge:** the private evening safari has the most Tripadvisor reviews (218).

## Deploy

Upload this folder to Laravel's `public/desert-safari-dubai/`. The page is then live at https://khattourism.com/desert-safari-dubai/ (keep the trailing slash).

"Book and pay online" goes to each option's existing tour page, which has the card-payment form.

## Tracking (GTM-542BQV7F)

| Event | Fires on | Parameters |
|---|---|---|
| `whatsapp_lead` | any WhatsApp button | `safari`, `transfer`, `adults`, `children`, `value`, `currency` |
| `book_online_click` | "Book and pay online" | same as above |
| `call_click` | any phone link | same as above |

In GTM, create a Custom Event trigger for each and attach a Google Ads conversion tag to it.
