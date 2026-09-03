# The Guide

Five phases. Run them in order. Phase 2 is the one everyone skips and the one
that usually holds the answer.

---

## Phase 1 — Baseline before you touch anything

You cannot tell whether you helped if you never wrote down where you started.

Capture from Google Search Console (28-day window):

- Clicks, impressions, CTR, average position
- Every query with impressions, sorted by impressions
- Every page with impressions, sorted by impressions
- The Pages report index-status breakdown

Then write down the single number you are trying to move. "More traffic" is not
a target. "Get `/web-designer-waterford` from position 50 to page one" is.

**The near-miss list is the highest-value thing on the screen.** Pages with
impressions and zero clicks are pages Google already understands and is already
showing — they are just showing them too far down. Those are far cheaper to fix
than pages with no impressions at all.

## Phase 2 — Can the page be reached and kept?

Three questions, in this order. Do not proceed until all three are answered.

**Is the page reachable by clicking from the homepage?**
Not "is it in the sitemap". A sitemap is a hint. Internal links are the signal.
Start at the homepage, follow links only, and list every page you can arrive at.
Anything on the site that never appears is an orphan.

```bash
python3 seo-audit.py https://yoursite.com --orphans
```

**Is anything blocking it?**
`robots.txt` disallow rules, `noindex` meta tags, canonical tags pointing at a
different URL, redirect chains.

**Does Google consider it worth an index slot?**
Read the GSC Pages report literally:

| GSC status | What it actually means | Fix |
|---|---|---|
| Discovered — currently not indexed | Google knows the URL exists but hasn't prioritised crawling it. Almost always weak internal linking. | Link to it from pages that are already indexed. |
| Crawled — currently not indexed | Google read it and decided against it. Usually thin or duplicative. | Make it substantially better, merge it, or delete it. |
| Alternate page with proper canonical | **Working as intended.** Not a bug. | Nothing. |
| Duplicate without user-selected canonical | Google picked a canonical for you and may have picked wrong. | Set canonicals explicitly. |
| Excluded by 'noindex' tag | You told it to. | Check you meant to. |

Fix everything in this phase before writing a single word of new content.

## Phase 3 — The technical foundation

Ship all of it at once; it is a single afternoon.

**`robots.txt`** — allow the crawlers you want, including AI crawlers if you
want to appear in AI answers. Point at the sitemap. Template in this repo.

**`sitemap.xml`** — every canonical URL, correct `lastmod` dates, `hreflang` if
you serve more than one region. No redirects, no `noindex` pages, no 404s.

**Canonical tags** — one canonical per page, absolute URL, self-referencing on
the canonical version. Pick `.html` or pretty URLs and never mix.

**JSON-LD structured data** — the four that earn their place for a small business:

- `LocalBusiness` (or a subtype) on the homepage and contact page
- `Service` on each service page
- `FAQPage` where you genuinely have Q&A
- `BreadcrumbList` on anything nested

Templates in `schema-*.json`. Validate at
[validator.schema.org](https://validator.schema.org) and Google's Rich Results
Test before shipping. Invalid schema is worse than no schema.

**`llms.txt`** — a plain-text summary of what the site is and where the
important pages are, for LLM crawlers. An emerging convention, cheap to add,
no downside.

**Titles and meta descriptions** — unique on every page, primary term near the
front of the title, description written to earn a click rather than to hold
keywords.

## Phase 4 — Landing page architecture

The mistake is building pages around what you want to sell. Build them around
what people type.

**Business type × location.** For a local service business, the grid is
`[what you do] × [where you do it]`, plus a layer of `[customer type] ×
[location]`. A web designer in Waterford: `web design waterford`,
`web designer dungarvan`, then `website for a café in waterford`,
`barber shop website ireland`, and so on.

**One page per intent, and each page must earn its existence.** If two pages
would say nearly the same thing, make one page. Google merges near-duplicates
whether or not you agree.

**Every page needs, at minimum:**
- An H1 containing the target phrase, written naturally
- Something genuinely local or specific — a real place name in a real sentence, a local client, a photo taken there
- Proof: work you did, a result, a name
- One clear next action
- Internal links up to the parent and sideways to two or three siblings

**E-E-A-T is not a formula, it is evidence.** A face, a name, a real address, a
history, work with client names attached. For a one-person studio the person
*is* the authority signal. Hiding is expensive.

## Phase 5 — Local SEO and measurement

**Google Business Profile** is the single highest-leverage item for a local
business, and it sits outside your website entirely. Complete profile, correct
category, real photos, service area, posts. It feeds the map pack, which sits
above the organic results.

**NAP consistency** — name, address, phone identical everywhere: site, GBP,
directories, social. Inconsistency splits your identity across entities.

**Then wait.** Index-status changes take one to several weeks to appear. Use
GSC's URL Inspection → Request Indexing for genuinely new or genuinely changed
pages, but do not spam it; it does not raise the ceiling.

**Change one thing at a time.** With a feedback loop this slow, batching five
changes means learning nothing about which one worked. It is tempting and it is
always a mistake.

---

## The order matters

Phases 1 and 2 are cheap and answer most questions. Phase 3 is a fixed cost you
pay once. Phase 4 is where the ongoing work lives. Phase 5 is where the results
show up, late.

Anyone starting at phase 4 is guessing.
