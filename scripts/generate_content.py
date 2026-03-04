#!/usr/bin/env python3
from __future__ import annotations
import os, re, datetime
from pathlib import Path
from html import escape

SITE_URL = "https://www.myboussole.fr"
ARTICLES_DIR = Path("articles")
EXCLUDE_DIRS = {"_template"}

def parse_front_matter(html: str) -> dict:
    """
    Front matter in HTML comment:
    <!--
    ---
    key: "value"
    ---
    -->
    """
    m = re.search(r"<!--\s*---(.*?)---\s*-->", html, flags=re.S)
    if not m:
        return {}
    block = m.group(1)
    out = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        out[k] = v
    return out

def parse_html_meta(html: str) -> dict:
    def find(pattern: str):
        m = re.search(pattern, html, flags=re.I|re.S)
        return m.group(1).strip() if m else ""
    title = find(r"<title>(.*?)</title>")
    desc = find(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']')
    h1 = find(r"<h1[^>]*>(.*?)</h1>")
    # strip tags in h1 if any
    h1 = re.sub(r"<[^>]+>", "", h1).strip()
    return {
        "title": title or h1,
        "description": desc,
    }

def parse_date(s: str) -> datetime.date | None:
    try:
        return datetime.date.fromisoformat(s)
    except Exception:
        return None

def collect_articles():
    items = []
    if not ARTICLES_DIR.exists():
        return items
    for p in sorted(ARTICLES_DIR.iterdir()):
        if not p.is_dir():
            continue
        if p.name in EXCLUDE_DIRS:
            continue
        index = p / "index.html"
        if not index.exists():
            continue
        html = index.read_text(encoding="utf-8", errors="replace")
        fm = parse_front_matter(html)
        meta = parse_html_meta(html)
        title = fm.get("title") or meta.get("title") or p.name
        desc = fm.get("description") or meta.get("description") or ""
        date = parse_date(fm.get("date", "")) or None
        updated = parse_date(fm.get("updated", "")) or None
        slug = fm.get("slug") or p.name
        url = f"{SITE_URL}/articles/{slug}/"
        items.append({
            "dir": p.name,
            "slug": slug,
            "url": url,
            "title": title,
            "description": desc,
            "date": date,
            "updated": updated,
        })
    # sort: date desc, then slug asc
    def sort_key(it):
        d = it["date"] or datetime.date(1970,1,1)
        return (-d.toordinal(), it["slug"])
    items.sort(key=sort_key)
    return items

def write_articles_index(items):
    out = Path("articles/index.html")
    if not out.exists():
        return
    html = out.read_text(encoding="utf-8", errors="replace")
    # Replace UL content between markers
    ul_pattern = r'(<ul>\s*)(.*?)(\s*</ul>)'
    m = re.search(ul_pattern, html, flags=re.S|re.I)
    if not m:
        return
    li = []
    for it in items:
        date = it["date"].isoformat() if it["date"] else ""
        meta = f' <span class="meta">— {escape(date)}</span>' if date else ""
        li.append(f'<li><a href="/articles/{escape(it["slug"])}/">{escape(it["title"])}</a>{meta}</li>')
    new_ul = m.group(1) + "\n        " + "\n        ".join(li) + "\n      " + m.group(3)
    new_html = html[:m.start()] + new_ul + html[m.end():]
    out.write_text(new_html, encoding="utf-8")

def write_sitemap(items):
    out = Path("sitemap.xml")
    # base urls
    urls = [
        f"{SITE_URL}/",
        f"{SITE_URL}/ecosysteme.html",
        f"{SITE_URL}/rejoindre.html",
        f"{SITE_URL}/articles/",
    ]
    for it in items:
        urls.append(it["url"])
    body = "\n".join([f"  <url><loc>{u}</loc></url>" for u in urls])
    xml = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{body}\n</urlset>\n'
    out.write_text(xml, encoding="utf-8")

def main():
    items = collect_articles()
    write_articles_index(items)
    write_sitemap(items)

if __name__ == "__main__":
    main()
