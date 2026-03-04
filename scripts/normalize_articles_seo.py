#!/usr/bin/env python3
import re
from pathlib import Path

CANONICAL_BASE = "https://www.myboussole.fr"

def upsert_in_head(html: str, pattern: str, replacement: str) -> str:
    # Replace if exists
    if re.search(pattern, html, flags=re.IGNORECASE):
        return re.sub(pattern, replacement, html, flags=re.IGNORECASE)

    # Insert before </head>
    if not re.search(r"</head>", html, flags=re.IGNORECASE):
        raise RuntimeError("No </head> found; cannot insert SEO tags safely.")
    return re.sub(r"</head>", replacement + "\n</head>", html, count=1, flags=re.IGNORECASE)

def ensure_canonical_and_ogurl(file_path: Path, canonical_url: str) -> bool:
    html = file_path.read_text(encoding="utf-8")

    canonical_tag = f'<link rel="canonical" href="{canonical_url}" />'
    ogurl_tag = f'<meta property="og:url" content="{canonical_url}" />'

    new_html = html
    new_html = upsert_in_head(
        new_html,
        r'<link[^>]*rel=["\']canonical["\'][^>]*>',
        canonical_tag
    )
    new_html = upsert_in_head(
        new_html,
        r'<meta[^>]*property=["\']og:url["\'][^>]*>',
        ogurl_tag
    )

    if new_html != html:
        file_path.write_text(new_html, encoding="utf-8")
        return True
    return False

def main() -> None:
    changed = 0

    # Hub articles
    hub = Path("articles/index.html")
    if hub.exists():
        url = f"{CANONICAL_BASE}/articles/"
        if ensure_canonical_and_ogurl(hub, url):
            changed += 1

    # Each article page: articles/<slug>/index.html (exclude _template)
    for p in sorted(Path("articles").glob("*/index.html")):
        if p.parent.name == "_template":
            continue
        slug = p.parent.name
        url = f"{CANONICAL_BASE}/articles/{slug}/"
        if ensure_canonical_and_ogurl(p, url):
            changed += 1

    print(f"normalize_articles_seo: changed {changed} file(s)")

if __name__ == "__main__":
    main()
