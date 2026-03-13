#!/usr/bin/env python3
from __future__ import annotations
import re, datetime, subprocess
from pathlib import Path
from html import escape

# ── SVG FALLBACKS miniatures listing ──────────────────────────
FALLBACK_SVGS = {
    "Mécanisme biologique": '<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="10" fill="#EEF2F8"/><circle cx="40" cy="40" r="7" fill="#2d6a4f"/><ellipse cx="40" cy="40" rx="26" ry="10" fill="none" stroke="#4A7AB5" stroke-width="1.8" opacity="0.7"/><ellipse cx="40" cy="40" rx="26" ry="10" fill="none" stroke="#4A7AB5" stroke-width="1.8" opacity="0.7" transform="rotate(60 40 40)"/><ellipse cx="40" cy="40" rx="26" ry="10" fill="none" stroke="#4A7AB5" stroke-width="1.8" opacity="0.7" transform="rotate(120 40 40)"/><circle cx="66" cy="40" r="3" fill="#6A9AD5"/><circle cx="27" cy="54" r="3" fill="#6A9AD5"/><circle cx="27" cy="26" r="3" fill="#6A9AD5"/></svg>',
    "Vécu patient": '<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="10" fill="#FAF0F0"/><circle cx="40" cy="26" r="10" fill="#C08090" opacity="0.85"/><path d="M22 62 Q22 44 40 44 Q58 44 58 62" fill="#C08090" opacity="0.75"/><path d="M16 70 Q22 64 28 70 Q34 76 40 70 Q46 64 52 70 Q58 76 64 70" fill="none" stroke="#E07080" stroke-width="2" opacity="0.6"/></svg>',
    "Pratique / Ressource": '<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="10" fill="#EEF4F0"/><circle cx="40" cy="40" r="24" fill="none" stroke="#2d6a4f" stroke-width="2" opacity="0.5"/><circle cx="40" cy="40" r="3" fill="#2d6a4f"/><polygon points="40,18 37,40 43,40" fill="#2d6a4f"/><polygon points="40,62 37,40 43,40" fill="#A0B0A8"/><text x="40" y="13" text-anchor="middle" font-size="7" fill="#2d6a4f" font-family="sans-serif" font-weight="700">N</text></svg>',
    "Intersectionnel": '<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="10" fill="#F2EEF8"/><circle cx="32" cy="40" r="20" fill="#9080C0" opacity="0.35"/><circle cx="48" cy="40" r="20" fill="#4A7AB5" opacity="0.35"/><path d="M40 22 Q54 30 54 40 Q54 50 40 58 Q26 50 26 40 Q26 30 40 22 Z" fill="#7060A8" opacity="0.3"/></svg>',
    "Bingo / Liste": '<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="10" fill="#F8F4EE"/><rect x="16" y="20" width="10" height="10" rx="2" fill="none" stroke="#2d6a4f" stroke-width="1.8"/><path d="M18 25 L21 28 L26 22" stroke="#2d6a4f" stroke-width="1.8" fill="none" stroke-linecap="round"/><line x1="32" y1="25" x2="64" y2="25" stroke="#06172D" stroke-width="2" opacity="0.4"/><rect x="16" y="36" width="10" height="10" rx="2" fill="none" stroke="#2d6a4f" stroke-width="1.8"/><path d="M18 41 L21 44 L26 38" stroke="#2d6a4f" stroke-width="1.8" fill="none" stroke-linecap="round"/><line x1="32" y1="41" x2="64" y2="41" stroke="#06172D" stroke-width="2" opacity="0.4"/><rect x="16" y="52" width="10" height="10" rx="2" fill="none" stroke="#A0A0A0" stroke-width="1.5"/><line x1="32" y1="57" x2="55" y2="57" stroke="#06172D" stroke-width="2" opacity="0.25"/></svg>',
    "default": '<svg viewBox="0 0 80 80" xmlns="http://www.w3.org/2000/svg"><rect width="80" height="80" rx="10" fill="#FAF8F4"/><circle cx="40" cy="40" r="26" fill="none" stroke="#2d6a4f" stroke-width="2" opacity="0.4"/><circle cx="40" cy="40" r="4" fill="#2d6a4f"/><polygon points="40,16 37,40 43,40" fill="#2d6a4f"/><polygon points="40,64 37,40 43,40" fill="#B0C0B8"/><polygon points="16,40 40,37 40,43" fill="#B0C0B8"/><polygon points="64,40 40,37 40,43" fill="#2d6a4f" opacity="0.6"/></svg>',
}

TAG_TO_ANGLE = {
    "histamine": "Mécanisme biologique", "mcas": "Mécanisme biologique",
    "methylation": "Mécanisme biologique", "cortisol": "Mécanisme biologique",
    "thyroide": "Mécanisme biologique", "système nerveux": "Mécanisme biologique",
    "axe hpa": "Mécanisme biologique", "orexine": "Mécanisme biologique",
    "mécanisme": "Mécanisme biologique", "biologie": "Mécanisme biologique",
    "fibromyalgie": "Vécu patient", "covid long": "Vécu patient",
    "fatigue chronique": "Vécu patient", "réveil fatigué": "Vécu patient",
    "brouillard mental": "Vécu patient", "dysautonomie": "Vécu patient",
    "pem": "Vécu patient", "pots": "Vécu patient",
    "pacing": "Pratique / Ressource", "sommeil": "Pratique / Ressource",
    "supplémentation": "Pratique / Ressource", "guide": "Pratique / Ressource",
    "ressource": "Pratique / Ressource",
}

def get_fallback_svg(tags_list):
    for tag in (tags_list or []):
        tag_lower = tag.lower().strip()
        for key, angle in TAG_TO_ANGLE.items():
            if key in tag_lower:
                return FALLBACK_SVGS.get(angle, FALLBACK_SVGS["default"])
    return FALLBACK_SVGS["default"]
# ──────────────────────────────────────────────────────────────

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

def extract_hero_image(html: str, slug: str, fm: dict) -> str:
    """Extract a thumbnail URL: front matter image > og:image > first <img src> in content."""
    # 1. Front matter image field
    fm_image = fm.get("image", "")
    if fm_image:
        if fm_image.startswith("http"):
            return fm_image
        return f"{SITE_URL}/articles/{slug}/{fm_image}"
    # 2. og:image meta tag (both attribute orders)
    for pat in [
        r'<meta\s[^>]*property=["\']og:image["\']\s[^>]*content=["\'](.*?)["\']',
        r'<meta\s[^>]*content=["\'](.*?)["\']\s[^>]*property=["\']og:image["\']',
    ]:
        m = re.search(pat, html, flags=re.I | re.S)
        if m:
            url = m.group(1).strip()
            if url:
                return url
    # 3. First <img src> in content (skip data: URIs)
    m = re.search(r'<img\b[^>]*\bsrc=["\']((?!data:)[^"\']+)["\']', html, flags=re.I | re.S)
    if m:
        src = m.group(1).strip()
        if src:
            if src.startswith("http"):
                return src
            return f"{SITE_URL}/articles/{slug}/{src}"
    return ""


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
        import json as _json
        tags_raw = fm.get("tags", "[]")
        try:
            tags = _json.loads(tags_raw) if isinstance(tags_raw, str) else list(tags_raw)
        except Exception:
            tags = []
        url = f"{SITE_URL}/articles/{slug}/"
        lastmod = pick_lastmod(updated, date, index)

        if title == "Titre de l'article" or slug == "mon-article":
            continue

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
            "tags": tags,
            "read_time": fm.get("read_time", ""),
            "image": extract_hero_image(html, slug, fm),
        })

    # sort: date desc, then slug asc
    def sort_key(it):
        d = it["date"] or datetime.date(1970, 1, 1)
        return (-d.toordinal(), it["slug"])
    items.sort(key=sort_key)
    return items

MONTHS_FR = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"]

def format_date_fr(d: datetime.date | None) -> str:
    if not d:
        return ""
    return f"{d.day} {MONTHS_FR[d.month - 1]} {d.year}"

def write_articles_index(items):
    out = Path("articles/index.html")
    if not out.exists():
        return
    html = out.read_text(encoding="utf-8", errors="replace")
    list_pattern = r'(<div id="articles-list"[^>]*>)(.*?)(</div>)(?=\s*<div id="empty-state")'
    m = re.search(list_pattern, html, flags=re.S|re.I)
    if not m:
        return
    cards = []
    for item in items:
        tags = item.get("tags", [])
        tags_attr = ",".join(tags)
        # show max 2 tags in UI
        tag_spans = "".join(f'<span class="article-tag">{escape(t)}</span>' for t in tags[:2])
        date_fr = format_date_fr(item["date"])
        read_time = item.get("read_time", "")
        image = item.get("image", "")
        tags = item.get("tags", [])
        is_image = image and any(image.lower().endswith(ext) for ext in ('.jpg', '.jpeg', '.png', '.webp', '.gif'))
        if is_image:
            thumb_html = f'        <img class="article-thumb" src="{escape(image)}" alt="" loading="lazy" aria-hidden="true" />\n'
        else:
            svg = get_fallback_svg(tags)
            thumb_html = f'        <div class="article-thumb article-thumb-svg" aria-hidden="true">{svg}</div>\n'
        cards.append(
            f'      <a href="{SITE_URL}/articles/{escape(item["slug"])}/" class="article-item" data-tags="{tags_attr}">\n'
            f'        <div>\n'
            f'          <div class="article-tags-row">{tag_spans}</div>\n'
            f'          <div class="article-title">{escape(item["title"])}</div>\n'
            f'        </div>\n'
            f'        <div class="article-meta"><span class="article-date">{escape(date_fr)}</span>'
            + (f'<span class="article-readtime">{escape(read_time)}</span>' if read_time else "")
            + f'</div>\n'
            + thumb_html
            + f'      </a>'
        )
    inner = "\n" + "\n".join(cards) + "\n    "
    new_html = html[:m.start()] + m.group(1) + inner + m.group(3) + html[m.end():]
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
