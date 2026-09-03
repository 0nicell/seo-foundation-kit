# Case study — rebuilding ncell.ie's SEO foundation (v2)

The site: [ncell.ie](https://ncell.ie), a one-person web design studio in
Dungarvan, Co. Waterford, Ireland. Originally positioned exclusively for
nightlife and events clients.

Everything below is what actually happened, in order.

---

## 1. Where it started

A Google Search Console baseline, 28 days to **14 July 2026**, URL-prefix
property `https://ncell.ie/`:

| Metric | Value |
|---|---|
| Clicks | 14 |
| Impressions | 111 |
| CTR | 12.6% |
| Average position | 50.8 |

Position ~50 means page five. Nobody scrolls to page five. The 12.6% CTR is a
vanity number — it is high only because the handful of impressions were
brand-name searches by people already looking for the studio.

Indexing status of the 10 pages GSC knew about:

- 5 indexed
- 3 **Discovered — currently not indexed**
- 1 **Crawled — currently not indexed**
- 1 Alternate page with proper canonical

Top query: `web design waterford` — 12 impressions, **0 clicks**.
Biggest near-miss page: `/web-designer-waterford` — 40 impressions, 0 clicks, ~position 50.
Second: `/web-designer-dungarvan` — 18 impressions, 0 clicks.
The homepage alone drove 12 of 43 total clicks.

The demand was local and generic — *Waterford web design* — not the nightlife
niche the site was built around. That mismatch shaped everything after.

## 2. Competitor analysis

Benchmark: `craigmurray.ie`, a local competitor ranking for the exact terms
ncell.ie was losing. What he had that ncell.ie did not:

- Location pages that read like they were written for a human in that town
- Visible personal identity — a face, a name, a story (E-E-A-T signals)
- Internal linking that actually connected the site together

## 3. What got built (the v2 technical foundation)

- **JSON-LD structured data on every page** — LocalBusiness, Service, FAQPage, BreadcrumbList
- **`robots.txt` with explicit AI-crawler allowlisting** — GPTBot, ClaudeBot, PerplexityBot and friends, allowed on purpose
- **`sitemap.xml` with hreflang**, listing all 23 pages
- **`llms.txt`** — a plain-text site summary for LLM crawlers
- **Canonical strategy** to resolve `.html` vs pretty-URL duplicates

Templates for all of the above are in this repo.

## 4. The discovery that mattered

Three pages sat in **"Discovered — currently not indexed"** for weeks. The
standard advice is "improve content quality" or "build authority". Both wrong here.

The actual cause: **the homepage linked to none of the 22 standalone pages.**
The footer contained only `#services`, `#faq`, a WhatsApp link and Instagram.
Every service page, location page and blog post was an orphan — reachable only
by the sitemap, which Google treats as a hint, not a promise.

Fix: a 22-link footer sitemap grouped into Services / Areas / Studio / Guides.

Two other findings from the same pass, both worth knowing:

- **"Alternate page with proper canonical" is not a bug.** The `.html` and
  pretty-URL versions were canonicalising correctly. It was already healthy.
- **"Crawled — currently not indexed"** was one genuinely thin page
  (`blog-countdown.html`). Google crawled it, judged it not worth an index slot,
  and was right.

`robots.txt` was open and fine the whole time. The sitemap was complete the
whole time. The problem was never the thing the tooling pointed at.

## 5. Difficulties

**The niche was wrong for the demand.** The site was built for nightlife and
events. Search demand in Waterford is for "web design" generically. Nightlife
intent exists but the volume is tiny. Resolution: keep the niche as
positioning, broaden the pricing tiers and page copy to any business, and
build business-type × location landing pages (café, barber, trades, shop,
salon, gym) to meet the demand that actually exists.

**URL inconsistency.** Some pages ended `.html`, some did not. This generated
duplicate-URL noise in GSC and made canonicals harder to reason about than they
needed to be. Pick one convention on day one.

**Diagnosing the wrong layer first.** Considerable time went into keyword
targeting and page copy while the pages in question were structurally
unreachable. The lesson is in `GUIDE.md`: run the crawl-path check *before* any
content work.

**The deploy blocker.** The host is Netlify (project `ncell-design`). Netlify
credits ran out mid-project, so the completed v2 edits could not be deployed.
Worse, un-deployed edits are not retrievable through the Netlify API — only the
live deploy is exposed. Anything not in a Git repo or on local disk was
stranded. **Lesson: never let the only copy of your work live in a hosting
provider's UI.**

**Measurement lag.** GSC does not respond quickly. Fixes made in one week do
not show as index-status changes for one to several more. This makes it easy to
change five things at once and learn nothing about which one worked.

## 6. Timeline

| | |
|---|---|
| First recorded SEO session | 12 July 2026 |
| GSC baseline captured | 14 July 2026 |
| Orphan-page root cause found + v2 foundation built | mid-July 2026 |
| Latest session | 3 September 2026 |
| **Calendar span** | **~8 weeks** |
| **Active working weeks** | _`<!-- Oisín: fill in — this is the one number the working notes don't record -->`_ |

Calendar span is not effort. The work happened in bursts between client
projects, and a large share of the elapsed time was waiting on Google to
recrawl rather than doing anything.

## 7. What was staged but not shipped

Built and verified, blocked on the Netlify deploy:

- Homepage hero replaced with a Three.js holographic wireframe globe
- Showcase carousel expanded 6 → 8 cards
- Pricing tier descriptions broadened from events-only to any business (prices unchanged)
- A new standalone project page
- The 22-link internal footer sitemap

## 8. What I'd do differently

1. **Check the crawl path before anything else.** One question — *is every page reachable by clicking from the homepage?* — would have saved the most time of anything in this project.
2. **Keep the site in Git from commit one.** The stranded-edits problem was self-inflicted and entirely avoidable.
3. **Pick a URL convention on day one** and never mix.
4. **Change one thing at a time** once GSC is the feedback loop, or accept that you will not know what worked.
5. **Let the search demand pick the pages**, not the brand positioning. Position however you like; build pages for what people actually type.
