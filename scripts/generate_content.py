#!/usr/bin/env python3
from __future__ import annotations
import re, datetime, subprocess
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
    h1 = re.sub(r"<[^>]+>", "", h1).strip()
    return {"title": title or h1, "description": desc}

def parse_date(s: str) -> datetime.date | None:
    try:
        return datetime.date.fromisoformat(s)
    except Exception:
        return None

def git_lastmod_date(path: str) -> datetime.date | None:
    # needs full history => CI must use checkout fetch-depth: 0
    try:
        r = subprocess.run(
            ["git", "log", "-1", "--format=%cI", "--", path],
            capture_output=True,
            text=True,
            check=False,
        )
        iso = (r.stdout or "").strip()
        if not iso:
            return None
        return datetime.date.fromisoformat(iso[:10])
    except Exception:
        return None

def file_mtime_date(p: Path) -> datetime.date | None:
    try:
        ts = p.stat().st_mtime
        return datetime.date.fromtimestamp(ts)
    except Exception:
        return None

def pick_lastmod(updated: datetime.date | None, date: datetime.date | None, path: Path) -> datetime.date:
    return (
        updated
        or date
        or git_lastmod_date(str(path))
        or file_mtime_date(path)
        or datetime.date.today()
    )

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
        slug = p.name  # single source of truth: folder name
        url = f"{SITE_URL}/articles/{slug}/"
        lastmod = pick_lastmod(updated, date, index)

        items.append({
            "dir": p.name,
            "slug": slug,
            "url": url,
            "title": title,
            "description": desc,
            "date": date,
            "updated": updated,
            "index_path": str(index),
            "lastmod": lastmod,
        })

    # sort: date desc, then slug asc
    def sort_key(it):
        d = it["date"] or datetime.date(1970, 1, 1)
        return (-d.toordinal(), it["slug"])
    items.sort(key=sort_key)
    return items

def write_articles_index(items):
    out = Path("articles/index.html")
    if not out.exists():
        return
    html = out.read_text(encoding="utf-8", errors="replace")
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

    base_entries = [
        (f"{SITE_URL}/", Path("index.html")),
        (f"{SITE_URL}/ecosysteme.html", Path("ecosysteme.html")),
        (f"{SITE_URL}/rejoindre.html", Path("rejoindre.html")),
        (f"{SITE_URL}/articles/", Path("articles/index.html")),
    ]

    url_lines = []

    def add_url(loc: str, lastmod: datetime.date | None):
        if lastmod:
            url_lines.append(f"  <url><loc>{loc}</loc><lastmod>{lastmod.isoformat()}</lastmod></url>")
        else:
            url_lines.append(f"  <url><loc>{loc}</loc></url>")

    for loc, path in base_entries:
        lm = pick_lastmod(None, None, path) if path.exists() else datetime.date.today()
        add_url(loc, lm)

    for it in items:
        add_url(it["url"], it.get("lastmod"))

    body = "\n".join(url_lines)
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}\n"
        "</urlset>\n"
    )
    out.write_text(xml, encoding="utf-8")

def main():
    items = collect_articles()
    write_articles_index(items)
    write_sitemap(items)

if __name__ == "__main__":
    main()
