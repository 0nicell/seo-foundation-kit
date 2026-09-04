# SEO Foundation Kit

**A technical SEO starter kit for small business websites.**

Most small business sites don't have an SEO problem. They have an **indexing** problem wearing an SEO costume — Google either doesn't know the pages exist, can't crawl them, or doesn't think they're worth keeping.

This kit is the guide, prompts, templates and audit script behind the v2 rebuild of [ncell.ie](https://ncell.ie). Everything here is what actually shipped, including the parts that went wrong.

Python · MIT licensed · by [@0nicell](https://github.com/0nicell), built with Claude

---

## Start here

Before touching a single keyword, answer three questions about any page:

1. **Does Google know it exists?** — is it linked from anywhere, is it in the sitemap
2. **Can Google crawl it?** — robots.txt, canonical tags
3. **Does Google think it's worth keeping?** — thin content, duplicates

The ncell.ie audit found 22 pages linked from **nowhere** on the homepage. Every hour spent on keywords before that discovery was wasted. Phase 2 of the guide exists so nobody repeats it.

---

## Run the audit

```bash
python3 seo-audit.py https://example.com
```

Point it at a URL and it prints what's broken. The only dependency beyond the standard library is `requests`.

Useful options:

```bash
python3 seo-audit.py https://example.com --orphans          # only check for orphan pages
python3 seo-audit.py https://example.com --max-pages 200    # crawl further (default: 60)
```

---

## What's in the kit

| File | What it is |
|---|---|
| [`GUIDE.md`](GUIDE.md) | The playbook — five phases, in order, from zero to indexed |
| [`PROMPTS.md`](PROMPTS.md) | Eight prompts to copy and paste into Claude, plus the anti-patterns to avoid |
| [`CASE-STUDY.md`](CASE-STUDY.md) | The real ncell.ie v2 build — numbers, mistakes, timeline |
| [`SKILL.md`](SKILL.md) | A Claude skill. Drop it in `~/.claude/skills/seo-foundation-kit/` |
| [`seo-audit.py`](seo-audit.py) | The auditor. One file, points at a URL, prints what's broken |
| [`robots.txt`](robots.txt) | Template, including which AI crawlers to allow |
| [`llms.txt`](llms.txt) | Template for the new convention of writing a site summary for LLMs |
| `schema-*.json` | Ready-made JSON-LD blocks: LocalBusiness, Service, FAQPage, BreadcrumbList |

---

## The five phases

The guide works through them in this order, and the order is the point.

1. **Baseline** — measure where you actually are before changing anything
2. **Indexing** — can each page be reached and will Google keep it
3. **Technical foundation** — robots, sitemap, canonicals, structured data
4. **Landing page architecture** — what pages should exist and how they link
5. **Local SEO and measurement** — maps, reviews, and knowing whether any of it worked

Skipping to phase 3 because it feels like the technical bit is the most common way to waste a month.

---

## Install as a Claude skill

```bash
git clone https://github.com/0nicell/seo-foundation-kit.git ~/.claude/skills/seo-foundation-kit
```

Then ask Claude to use it:

```
Use the seo-foundation-kit skill. Audit example.com, starting with the indexing
diagnosis, and tell me what to fix first.
```

---

## Status

Working notes, not a finished product. Corrections are welcome — especially on the schema templates.

## Licence

MIT — see [LICENSE](LICENSE).
