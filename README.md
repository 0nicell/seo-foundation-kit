# SEO Foundation Kit

A technical-SEO starter kit for small business websites — the templates, prompts and
diagnostic method behind the v2 rebuild of [ncell.ie](https://ncell.ie).

Built by [@0nicell](https://github.com/0nicell) with Claude. Part of a public
learning journey: everything here is what actually shipped, including the parts
that went wrong.

---

## What's in here

| File | What it is |
|---|---|
| `GUIDE.md` | The playbook. Five phases, in order, from zero to indexed. |
| `CASE-STUDY.md` | The real ncell.ie v2 build — numbers, mistakes, timeline. |
| `PROMPTS.md` | The prompt library. Copy-paste into Claude. |
| `SKILL.md` | A Claude skill. Drop it in `~/.claude/skills/seo-foundation-kit/`. |
| `seo-audit.py` | Single-file auditor. Points at a URL, prints what's broken. |
| `robots.txt` | Template with AI-crawler allowlisting. |
| `llms.txt` | Template for the emerging LLM-readable site summary convention. |
| `schema-*.json` | JSON-LD blocks: LocalBusiness, Service, FAQPage, BreadcrumbList. |

## The short version

Most small-business sites do not have an SEO problem. They have an
**indexing** problem wearing an SEO costume. Before touching keywords, answer:

1. Does Google know the page exists? (internal links, sitemap)
2. Can Google crawl it? (robots.txt, canonicals)
3. Does Google think it's worth keeping? (thin content, duplicates)

The ncell.ie audit found 22 standalone pages linked from **nowhere** on the
homepage. Every keyword hour before that discovery was wasted. `GUIDE.md`
phase 2 exists so nobody repeats it.

## Quick start

```bash
python3 seo-audit.py https://example.com
```

No dependencies beyond the standard library plus `requests`.

## Status

Working notes, not a finished product. Opening issues with corrections is
welcome — especially on the schema templates.

## Licence

MIT.
