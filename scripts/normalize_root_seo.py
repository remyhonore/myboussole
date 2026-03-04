#!/usr/bin/env python3
import re
from pathlib import Path

BASE = "https://www.myboussole.fr"
DEFAULT_OG_IMAGE = f"{BASE}/assets/og-default.jpg"

PAGES = [
    ("index.html", f"{BASE}/", "Boussole — Suivi simple (fatigue chronique, Covid long, fibromyalgie)", "Un suivi santé simple et privacy-first : énergie, sommeil, confort, clarté mentale. Articles et outil Boussole.", "website"),
    ("ecosysteme.html", f"{BASE}/ecosysteme.html", "Écosystème Boussole", "Découvrir l’écosystème Boussole : outils, ressources et parcours.", "article"),
    ("rejoindre.html", f"{BASE}/rejoindre.html", "Rejoindre Boussole", "Accéder à l’app et aux ressources Boussole.", "article"),
]

def upsert_in_head(html: str, pattern: str, replacement: str) -> str:
    if re.search(pattern, html, flags=re.IGNORECASE):
        return re.sub(pattern, replacement, html, flags=re.IGNORECASE)
    if not re.search(r"</head>", html, flags=re.IGNORECASE):
        raise RuntimeError("No </head> found; cannot insert SEO tags safely.")
    return re.sub(r"</head>", replacement + "\n</head>", html, count=1, flags=re.IGNORECASE)

def ensure_tags(path: Path, canonical: str, title: str, desc: str, og_image: str, og_type: str) -> bool:
    html = path.read_text(encoding="utf-8", errors="replace")
    new = html

    # canonical + og:url
    new = upsert_in_head(new, r'<link[^>]*rel=["\']canonical["\'][^>]*>', f'<link rel="canonical" href="{canonical}" />')
    new = upsert_in_head(new, r'<meta[^>]*property=["\']og:url["\'][^>]*>', f'<meta property="og:url" content="{canonical}" />')

    # og basics
    new = upsert_in_head(new, r'<meta[^>]*property=["\']og:type["\'][^>]*>', f'<meta property="og:type" content="{og_type}" />')
    new = upsert_in_head(new, r'<meta[^>]*property=["\']og:title["\'][^>]*>', f'<meta property="og:title" content="{title}" />')
    new = upsert_in_head(new, r'<meta[^>]*property=["\']og:description["\'][^>]*>', f'<meta property="og:description" content="{desc}" />')
    new = upsert_in_head(new, r'<meta[^>]*property=["\']og:image["\'][^>]*>', f'<meta property="og:image" content="{og_image}" />')

    # twitter (simple)
    new = upsert_in_head(new, r'<meta[^>]*name=["\']twitter:card["\'][^>]*>', '<meta name="twitter:card" content="summary_large_image" />')
    new = upsert_in_head(new, r'<meta[^>]*name=["\']twitter:title["\'][^>]*>', f'<meta name="twitter:title" content="{title}" />')
    new = upsert_in_head(new, r'<meta[^>]*name=["\']twitter:description["\'][^>]*>', f'<meta name="twitter:description" content="{desc}" />')
    new = upsert_in_head(new, r'<meta[^>]*name=["\']twitter:image["\'][^>]*>', f'<meta name="twitter:image" content="{og_image}" />')

    if new != html:
        path.write_text(new, encoding="utf-8")
        return True
    return False

def main():
    changed = 0
    for filename, canonical, title, desc, og_type in PAGES:
        p = Path(filename)
        if not p.exists():
            continue
        if ensure_tags(p, canonical, title, desc, DEFAULT_OG_IMAGE, og_type):
            changed += 1
    print(f"normalize_root_seo: changed {changed} file(s)")

if __name__ == "__main__":
    main()
