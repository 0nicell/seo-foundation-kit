# Prompt library

The prompts behind the ncell.ie v2 work, cleaned up and made portable. Replace
anything in `[BRACKETS]`.

Two rules that make all of these work better:

1. **Give it the real data.** Paste actual GSC exports, actual HTML, actual
   robots.txt. Prompts that describe a site produce advice about a genre of
   site. Prompts that contain a site produce advice about that site.
2. **Make it diagnose before it prescribes.** Left alone, an LLM will hand you a
   generic SEO checklist. Force the diagnosis step and the checklist becomes
   specific.

---

## 1. Baseline read

```
Here is a Google Search Console export for [SITE] — 28 days, queries and pages.

[PASTE CSV OR TABLE]

Tell me:
1. What is search demand actually asking for here, in the users' words — not
   what the site is positioned as?
2. Which pages are near-misses: real impressions, ~zero clicks, position 10-60?
   Rank them by how cheap they'd be to move.
3. Where is the gap between what the site sells and what people search for?

Do not give me an action plan yet. Just tell me what the data says.
```

## 2. Indexing diagnosis — run this before anything else

```
[SITE] has these pages in Google Search Console:
[PASTE PAGES REPORT WITH INDEX STATUS]

Here is the homepage HTML:
[PASTE]

And robots.txt:
[PASTE]

For each non-indexed page, tell me which of these is the actual cause:
- Orphaned (not linked from any indexed page)
- Blocked (robots.txt, noindex, canonical pointing elsewhere)
- Thin or duplicative (Google crawled it and declined)
- Simply too new

Be specific about which one and why. If a status is actually healthy and needs
no action, say so plainly instead of inventing work.
```

> This is the prompt that found the ncell.ie orphan problem. Three pages sat in
> "Discovered — currently not indexed"; the homepage footer linked to none of
> the 22 standalone pages. Every other diagnosis was wrong.

## 3. Crawl-path check

```
Here is the homepage HTML for [SITE]:
[PASTE]

And the full list of URLs in sitemap.xml:
[PASTE]

Which sitemap URLs cannot be reached by following links from this homepage?
List the orphans. Then propose a footer link structure, grouped into logical
sections, that reaches every one of them without looking like a link dump.
```

## 4. Technical foundation build

```
Build the technical SEO foundation for [SITE], a [BUSINESS TYPE] in
[LOCATION] serving [AUDIENCE].

Produce, as files I can drop in:
1. robots.txt — allow standard crawlers and AI crawlers (GPTBot, ClaudeBot,
   PerplexityBot, Google-Extended), sitemap reference
2. sitemap.xml for these URLs: [LIST]
3. JSON-LD for: LocalBusiness on the homepage, Service on each service page,
   FAQPage where there's real Q&A, BreadcrumbList for nested pages
4. llms.txt
5. Title + meta description for every page

Constraints: one URL convention throughout ([.html | pretty]); every canonical
absolute and self-referencing; no invented facts — if you need an address,
phone number or opening hours, ask me rather than making one up.
```

## 5. Landing page architecture

```
[SITE] is a [BUSINESS TYPE] in [LOCATION].

Search demand looks like this: [PASTE TOP QUERIES]

Design a landing page architecture:
1. The [service] × [location] grid worth building, ranked by
   demand-to-difficulty
2. A second layer of [customer type] × [location] pages
3. For each page: URL, H1, target phrase, the one thing that makes it not a
   template
4. The internal linking pattern connecting them to each other and to the
   homepage

Kill any page that would be a near-duplicate of another. I want pages that each
earn their place, not a matrix.
```

## 6. Single page brief

```
Write the brief for [URL], targeting "[PHRASE]".

Context: [BUSINESS], [LOCATION], [WHAT MAKES IT DIFFERENT]

I want:
- H1 and section headings
- What genuinely local or specific content goes in each section — real place
  names, real clients, real work
- The proof elements and where they sit
- Title + meta description
- Internal links: up to parent, sideways to siblings
- The JSON-LD block

No filler sections. If a section wouldn't be read, don't include it.
```

## 7. Competitor teardown

```
[COMPETITOR URL] outranks [MY URL] for "[PHRASE]".

Here is their page: [PASTE HTML OR TEXT]
Here is mine: [PASTE]

What do they have that I don't — structurally, not stylistically? Separate:
1. Things I can fix on the page this week
2. Things that come from authority or history and will take months
3. Things that don't matter and I should ignore

Be blunt about which of my assumptions are wrong.
```

## 8. Post-change review

```
[TIME] ago I changed [WHAT] on [SITE].

Before: [GSC NUMBERS]
After: [GSC NUMBERS]

Did it work? Distinguish real movement from noise and from normal seasonal
drift. If the sample is too small to conclude anything, say that instead of
finding a pattern in it. What should I change next, and what should I leave
alone?
```

---

## Anti-patterns

Prompts that consistently produced worthless output:

- **"How do I improve my SEO?"** — returns the same checklist every time.
- **Describing the site instead of pasting it.** You get advice about a category.
- **Asking for fixes before diagnosis.** It will find something to fix whether or not it's the problem.
- **Asking for a keyword list with no demand data.** It invents plausible keywords with no relationship to what anyone types.
- **Batching five changes and then asking what worked.** No prompt can recover that.
