#!/usr/bin/env python3
"""
seo-audit.py — single-file technical SEO auditor.

Answers the three questions that matter before any content work:
  1. Can Google reach every page? (orphan detection)
  2. Is anything blocking it?     (robots.txt, noindex, canonicals)
  3. Is the page-level foundation there? (title, meta, h1, JSON-LD)

Usage:
    python3 seo-audit.py https://example.com
    python3 seo-audit.py https://example.com --orphans
    python3 seo-audit.py https://example.com --max-pages 100

Requires: requests
"""

import argparse
import json
import re
import sys
import time
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse, urldefrag
from urllib.robotparser import RobotFileParser

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

UA = "seo-foundation-kit/1.0 (+https://github.com/0nicell/seo-foundation-kit)"
G, Y, R, DIM, B, X = "\033[32m", "\033[33m", "\033[31m", "\033[2m", "\033[1m", "\033[0m"


class PageParser(HTMLParser):
    """Pulls the handful of things that actually matter out of a page."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.jsonld = [], []
        self.title, self.description, self.canonical, self.robots_meta = None, None, None, None
        self.h1s = []
        self._in_title = self._in_h1 = self._in_ld = False
        self._buf = ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "a" and a.get("href"):
            rel = (a.get("rel") or "").lower()
            self.links.append((a["href"], "nofollow" in rel))
        elif tag == "title":
            self._in_title, self._buf = True, ""
        elif tag == "h1":
            self._in_h1, self._buf = True, ""
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            if name == "description":
                self.description = a.get("content", "")
            elif name == "robots":
                self.robots_meta = (a.get("content") or "").lower()
        elif tag == "link" and (a.get("rel") or "").lower() == "canonical":
            self.canonical = a.get("href")
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in_ld, self._buf = True, ""

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self.title, self._in_title = self._buf.strip(), False
        elif tag == "h1" and self._in_h1:
            self.h1s.append(self._buf.strip())
            self._in_h1 = False
        elif tag == "script" and self._in_ld:
            self.jsonld.append(self._buf.strip())
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title or self._in_h1 or self._in_ld:
            self._buf += data


def normalise(url):
    url, _ = urldefrag(url)
    return url.rstrip("/") or url


def same_host(a, b):
    return urlparse(a).netloc.replace("www.", "") == urlparse(b).netloc.replace("www.", "")


def fetch(session, url, timeout=12):
    try:
        r = session.get(url, timeout=timeout, allow_redirects=True)
        return r
    except requests.RequestException as e:
        print(f"  {R}fetch failed{X} {url} — {e}")
        return None


def get_sitemap_urls(session, base):
    """Read sitemap.xml, following a sitemap index one level."""
    found, queue, seen = set(), [urljoin(base, "/sitemap.xml")], set()
    while queue:
        sm = queue.pop()
        if sm in seen:
            continue
        seen.add(sm)
        r = fetch(session, sm)
        if not r or r.status_code != 200:
            continue
        locs = re.findall(r"<loc>\s*(.*?)\s*</loc>", r.text, re.I | re.S)
        if "<sitemapindex" in r.text[:2000].lower():
            queue.extend(locs[:50])
        else:
            found.update(normalise(u) for u in locs)
    return found


def crawl(session, base, max_pages):
    """Follow links from the homepage only. This is the crawl path Google sees."""
    start = normalise(base)
    seen, queue, pages = {start}, [start], {}
    while queue and len(pages) < max_pages:
        url = queue.pop(0)
        r = fetch(session, url)
        if not r:
            continue
        final = normalise(r.url)
        ctype = r.headers.get("content-type", "")
        if "html" not in ctype:
            continue
        p = PageParser()
        try:
            p.feed(r.text)
        except Exception:
            pass
        pages[final] = {"status": r.status_code, "parser": p, "redirected": final != url}
        for href, nofollow in p.links:
            if nofollow:
                continue
            nxt = normalise(urljoin(final, href))
            if not nxt.startswith("http") or not same_host(nxt, base):
                continue
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
        time.sleep(0.15)
    return pages


def audit_page(url, info):
    """Return a list of (severity, message) for one page."""
    out, p = [], info["parser"]
    if info["status"] >= 400:
        out.append(("err", f"HTTP {info['status']}"))
        return out
    if p.robots_meta and "noindex" in p.robots_meta:
        out.append(("err", "meta robots noindex — this page cannot rank"))
    if not p.title:
        out.append(("err", "no <title>"))
    elif len(p.title) > 65:
        out.append(("warn", f"title {len(p.title)} chars (will truncate ~60)"))
    elif len(p.title) < 15:
        out.append(("warn", f"title very short ({len(p.title)} chars)"))
    if not p.description:
        out.append(("warn", "no meta description"))
    elif len(p.description) > 165:
        out.append(("warn", f"meta description {len(p.description)} chars (truncates ~155)"))
    if not p.canonical:
        out.append(("warn", "no canonical tag"))
    else:
        if not p.canonical.startswith("http"):
            out.append(("warn", "canonical is relative — use an absolute URL"))
        elif normalise(p.canonical) != url:
            out.append(("info", f"canonical points elsewhere → {p.canonical}"))
    if len(p.h1s) == 0:
        out.append(("warn", "no <h1>"))
    elif len(p.h1s) > 1:
        out.append(("info", f"{len(p.h1s)} <h1> tags"))
    if not p.jsonld:
        out.append(("warn", "no JSON-LD structured data"))
    else:
        for block in p.jsonld:
            try:
                json.loads(block)
            except json.JSONDecodeError as e:
                out.append(("err", f"JSON-LD is invalid and will be ignored: {e}"))
    return out


def main():
    ap = argparse.ArgumentParser(description="Technical SEO audit")
    ap.add_argument("url")
    ap.add_argument("--max-pages", type=int, default=60)
    ap.add_argument("--orphans", action="store_true", help="only run the orphan check")
    args = ap.parse_args()

    base = args.url if args.url.startswith("http") else "https://" + args.url
    session = requests.Session()
    session.headers["User-Agent"] = UA

    print(f"\n{B}SEO audit — {base}{X}\n")

    # robots.txt
    rp, robots_url = RobotFileParser(), urljoin(base, "/robots.txt")
    r = fetch(session, robots_url)
    if r and r.status_code == 200:
        rp.parse(r.text.splitlines())
        has_sitemap = "sitemap:" in r.text.lower()
        print(f"{G}✓{X} robots.txt found"
              + ("" if has_sitemap else f"  {Y}(no Sitemap: line){X}"))
        ai = [b for b in ("GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended")
              if b.lower() in r.text.lower()]
        print(f"  {DIM}AI crawlers mentioned: {', '.join(ai) if ai else 'none'}{X}")
    else:
        print(f"{Y}!{X} no robots.txt")

    # sitemap
    sitemap = get_sitemap_urls(session, base)
    print(f"{G if sitemap else Y}{'✓' if sitemap else '!'}{X} sitemap.xml — {len(sitemap)} URLs")

    # crawl
    print(f"\n{DIM}crawling from the homepage…{X}")
    pages = crawl(session, base, args.max_pages)
    reachable = set(pages)
    print(f"{G}✓{X} {len(reachable)} pages reachable by following links\n")

    # --- the orphan check: the whole point of this script ---
    def variants(u):
        return {u, u + ".html", u[:-5] if u.endswith(".html") else u}

    orphans, mismatched = set(), set()
    for _u in sitemap:
        if _u in reachable:
            continue
        (mismatched if variants(_u) & reachable else orphans).add(_u)
    print(f"{B}Crawl path{X}")
    if mismatched:
        print(f"  {Y}{len(mismatched)} URL-form mismatch(es){X} — sitemap and internal links disagree on .html vs pretty URLs")
        print(f"  {DIM}Not orphans. Pick one convention and make sitemap, links and canonicals agree.{X}")
        for _u in sorted(mismatched)[:5]:
            print(f"    {Y}·{X} {_u}")
        if len(mismatched) > 5:
            print(f"    {DIM}… and {len(mismatched) - 5} more{X}")
        print()
    if not sitemap:
        print(f"  {Y}no sitemap to compare against{X}")
    elif orphans:
        print(f"  {R}{len(orphans)} orphaned page(s){X} — in sitemap.xml, but not reachable")
        print(f"  {DIM}These are your 'Discovered — currently not indexed' pages.{X}")
        print(f"  {DIM}Fix: link to them from a page that IS indexed.{X}\n")
        for u in sorted(orphans):
            print(f"    {R}·{X} {u}")
    else:
        print(f"  {G}✓ no orphans — every sitemap URL is reachable from the homepage{X}")

    unlisted = {u for u in reachable if not (variants(u) & sitemap)}
    if sitemap and unlisted:
        print(f"\n  {Y}{len(unlisted)} reachable page(s) missing from sitemap.xml{X}")
        for u in sorted(unlisted)[:15]:
            print(f"    {Y}·{X} {u}")

    if args.orphans:
        print()
        return

    # --- page-level ---
    print(f"\n{B}Pages{X}")
    totals = {"err": 0, "warn": 0}
    for url in sorted(pages):
        issues = audit_page(url, pages[url])
        errs = [i for i in issues if i[0] == "err"]
        warns = [i for i in issues if i[0] == "warn"]
        totals["err"] += len(errs)
        totals["warn"] += len(warns)
        if not issues:
            print(f"  {G}✓{X} {url}")
            continue
        mark = f"{R}✗{X}" if errs else f"{Y}!{X}"
        print(f"  {mark} {url}")
        for sev, msg in issues:
            c = R if sev == "err" else (Y if sev == "warn" else DIM)
            print(f"      {c}{msg}{X}")

    # --- duplicate titles ---
    titles = {}
    for url, info in pages.items():
        t = info["parser"].title
        if t:
            titles.setdefault(t, []).append(url)
    dupes = {t: u for t, u in titles.items() if len(u) > 1}
    if dupes:
        print(f"\n{B}Duplicate titles{X}")
        for t, urls in dupes.items():
            print(f"  {Y}“{t}”{X} on {len(urls)} pages")

    print(f"\n{B}Summary{X}")
    print(f"  {len(pages)} pages crawled · {R}{totals['err']} errors{X} · {Y}{totals['warn']} warnings{X}"
          + (f" · {R}{len(orphans)} orphans{X}" if sitemap and orphans else ""))
    print(f"\n  {DIM}Fix orphans and errors first. Warnings second. Content last.{X}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\ninterrupted")
