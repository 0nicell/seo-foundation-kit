---
name: seo-foundation-kit
description: Audit and fix technical SEO for a website — diagnose why pages aren't indexed or ranking, build the robots.txt / sitemap / JSON-LD / llms.txt foundation, and design location and service landing pages. Use for "SEO audit", "why isn't my site ranking", "not showing up on Google", "pages not indexed", "improve my SEO", "technical SEO", "structured data", "Search Console", or local SEO work.
---

# SEO Foundation Kit

Diagnose before you prescribe. Most sites that "have an SEO problem" have an
**indexing** problem, and indexing problems have causes that keyword work
cannot touch.

## The rule that matters most

**Never propose content or keyword work until the crawl path is verified.**

Ask, in this order:

1. Is the page reachable by clicking from the homepage? (not "is it in the sitemap")
2. Is anything blocking it — robots.txt, `noindex`, a canonical pointing elsewhere?
3. Did Google crawl it and decline it? (thin, duplicative)

Skipping this is the single most common and most expensive mistake. A real
example: three pages sat in "Discovered — currently not indexed" for weeks.
The cause was that the homepage linked to none of the site's 22 standalone
pages. No amount of content work would have fixed it.

## Phase 1 — Baseline

Ask for a Google Search Console export (28 days, queries + pages + index
status). If the user does not have GSC set up, say so plainly — without it you
are guessing, and you should tell them that rather than producing confident
advice from nothing.

From the export, establish:

- What search demand actually asks for, in users' words — which is often not
  what the site is positioned as
- **Near-misses**: pages with real impressions, ~zero clicks, position 10–60.
  These are the cheapest wins and should lead the recommendations.
- The gap between what the site sells and what people search for

Report what the data says before proposing anything.

## Phase 2 — Diagnose indexing

Run the audit script if available:

```bash
python3 seo-audit.py https://site.com --orphans
```

Otherwise fetch the homepage, `robots.txt` and `sitemap.xml` and compare
sitemap URLs against URLs reachable by following links.

Read GSC statuses literally — they are more precise than they look:

| Status | Actual cause | Fix |
|---|---|---|
| Discovered — currently not indexed | Weak internal linking. Almost always. | Link to it from an indexed page. |
| Crawled — currently not indexed | Google read it and declined. Thin or duplicative. | Improve substantially, merge, or delete. |
| Alternate page with proper canonical | **Healthy. Not a bug.** | Nothing. |
| Duplicate without user-selected canonical | Google chose a canonical, possibly wrong. | Set canonicals explicitly. |

Watch for a **URL-convention mismatch**: the sitemap listing `/page.html` while
internal links point at `/page`. This looks like orphaning in a naive audit but
is a different problem with a different fix — make sitemap, links and canonicals
all use one form.

Say plainly when something is already fine. Do not manufacture work.

## Phase 3 — Technical foundation

Ship these together:

- **robots.txt** — allow standard crawlers; allow AI crawlers (GPTBot,
  ClaudeBot, PerplexityBot, Google-Extended) unless the user wants out of AI
  answers; include the `Sitemap:` line. Never disallow a page you also want
  indexed — Google cannot read a `noindex` on a page it may not crawl.
- **sitemap.xml** — canonical URLs only, real `lastmod`, `hreflang` if
  multi-region. No redirects, no `noindex` pages, no 404s.
- **Canonicals** — absolute, self-referencing, one URL convention throughout.
- **JSON-LD** — `LocalBusiness` (or subtype), `Service` per service page,
  `FAQPage` only where the Q&A is visible on the page, `BreadcrumbList` for
  nested pages. Validate before shipping; invalid JSON-LD is silently ignored,
  and schema that does not match visible content is a policy violation.
- **llms.txt** — plain-text site summary for LLM crawlers.
- **Titles and meta descriptions** — unique per page, ≤60 and ≤155 characters,
  primary term early in the title, description written to earn a click.

**Never invent business facts.** Addresses, phone numbers, opening hours,
prices, client names and review counts must come from the user. Ask.

## Phase 4 — Landing page architecture

Build for what people type, not for what the business wants to sell.

- The grid is `[service] × [location]`, plus a second layer of
  `[customer type] × [location]`
- One page per intent. If two pages would say nearly the same thing, build one.
- Every page needs: an H1 with the target phrase written naturally, something
  genuinely specific (a real place, a real client, real work), proof, one clear
  next action, and internal links up to the parent and across to siblings
- E-E-A-T is evidence, not a formula: a face, a name, a real address, named
  work. For a solo business the person is the authority signal

Refuse to generate a matrix of near-identical template pages. Say why: Google
merges near-duplicates, and a thin page grid dilutes the site.

## Phase 5 — Local and measurement

- **Google Business Profile** is usually the highest-leverage single item for a
  local business, and it is not on their website. Complete profile, right
  category, real photos, service area.
- **NAP consistency** — name, address, phone identical across site, GBP,
  directories, social.
- **Expect lag.** Index status changes take one to several weeks. Tell the user
  this so they do not conclude a fix failed after four days.
- **One change at a time.** With a feedback loop this slow, batching means
  learning nothing. Say so when they want to ship five things at once.

## Reporting

Order every recommendation by cost-to-fix against likely impact:

1. Blocking and indexing problems
2. Near-miss pages (impressions, no clicks, position 10–60)
3. Technical foundation gaps
4. New page architecture
5. Content depth

Be specific about which pages and which lines. "Improve your internal linking"
is not a recommendation; "the footer links to none of your 22 service pages,
add a grouped footer sitemap" is.

## Honesty rules

- If there is no GSC data, say the diagnosis is limited rather than guessing.
- If something is already correct, say so and move on.
- Give ranges and mechanisms for timelines, never promises of positions.
- Never fabricate business details, review counts, or traffic figures.
