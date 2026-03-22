---
name: boussole-audit-vitrine
description: Auditer myboussole.fr. Déclenche sur audit, vérifier le site, listing articles, check vitrine, SEO, post-déploiement.
---

# Skill — Audit vitrine myboussole.fr

## Déclenchement automatique
- Avant tout git push impliquant un article → Phase 1 (bloquante)
- ~2 min après git push confirmé → Phase 3 (automatique)
- Demande explicite → Phase 1 + 2 + 3

## Phase 1 — Gate pré-déploiement (bloquante)
NEW_SLUG="<slug>"
grep -c "$NEW_SLUG" ~/Projects/myboussole/articles/index.html  # doit être >= 1
grep -c "$NEW_SLUG" ~/Projects/myboussole/sitemap.xml          # doit être >= 1

Checks HTML obligatoires :
- H1 unique (grep -c '<h1' index.html = 1)
- rel="canonical" présent
- meta description présente
- og:title, og:description, og:url présents
- img sans alt = 0
- Pas de placeholder (lorem ipsum, TODO, à compléter)
- Image hero déclarée et fichier présent

Tout check rouge = corriger avant de commiter.

## Phase 2 — Audit complet
Diff croisé 4 colonnes : Local / Listing / Sitemap / Live
Rapport tableau : Slug | Local | Listing | Sitemap | Live| HTML | Images | Notes

## Phase 3 — Checklist post-déploiement
1. HTTP 200 live
2. Position listing (slug en position 1)
3. Sitemap live (slug présent)
4. Images live (toutes HTTP 200)
5. Canonical live correct
6. Pas de placeholder dans le texte fetché
7. OG tags présents et non vides

## Règles de conformité

### Taxonomie tags (17 tags — source de vérité : listing live)
```
Alimentation | Biologie | Dysautonomie | Enfant | Épigénétique | Histamine | Hormones | Inflammation | Médicaments | Microbiote | Mitochondries | Neuromédiateurs | Pacing | Pharmacologie | SNA | Sommeil | Suppléments
```

**Règle absolue** : ne jamais inventer un tag. Si le contenu d'un article ne correspond à aucun tag de cette liste → choisir le plus proche parmi les 17. Si vraiment aucun ne convient → signaler à Rémy pour décision d'ajout de tag, mais ne pas en créer un nouveau sans validation explicite.

Tout `data-tags` hors liste dans `articles/index.html` = anomalie 🟠.

Vérification systématique : avant tout commit → `grep -o 'data-tags="[^"]*"' articles/index.html | sort -u` → comparer avec la liste ci-dessus.

### Architecture listing articles/index.html (depuis 22/03/2026)
Structure :

- Accordéon "Par où commencer" — ouvert par défaut (`id="acc-body"`), chevron `id="acc-chev"`
- Onglets thématiques `.tab-btn` (`data-tab`) : `tous` | `meca` | `agir` | `nut`
- Filtre niveau `.lvl-btn` (`data-level`) : `tous` | `debutant` | `intermediaire` | `expert`
- Barre résultats : `#results-count` + `#active-chips` (chips supprimables)
- Liste `#articles-list` générée par CI `generate_content.py`
- Pagination `#pagination` (10/page, `PER_PAGE = 10`)
- Section `#section-recents` (visible si `tab=tous`, `level=tous`, `search` vide)

Attributs sur chaque `.article-item` générés par CI :

- `data-tags="{Tag1},{Tag2}"` — tags taxonomie
- `data-level="{debutant|intermediaire|expert}"` — fallback `"intermediaire"` si absent
- `data-date="{YYYY-MM-DD}"` — extrait du front matter

Mapping slug→onglet : `const TAB_MAP` dans `articles/index.html`

- `meca` : mécanismes biologiques (pathophysiologie, biomarqueurs, mécanismes)
- `agir` : agir au quotidien (stratégies pratiques, symptômes)
- `nut`  : alimentation & micronutrition (nutriments, suppléments alimentaires)
- Tout slug absent du TAB_MAP → fallback `'meca'`

Niveaux de lecture :

- `debutant` → "Grand public" (badge vert `#eaf3de` / `#3b6d11`)
- `intermediaire` → "Public averti" (badge bleu `#e6f1fb` / `#185fa5`) — fallback
- `expert` → "Public expert" (badge orange `#faeeda` / `#854f0b`)

Badge "Nouveau" : calculé JS côté client, < 14 jours depuis `data-date`, rose `#fbeaf0` / `#993556`

Checks audit spécifiques à cette architecture :

- Tout nouvel article doit figurer dans `TAB_MAP` (sinon fallback `'meca'` silencieux)
- `data-level` doit être l'un des 3 valeurs valides
- `data-date` doit être au format `YYYY-MM-DD` (premier 10 chars du champ `date` front matter)
- `draft: true` dans front matter = exclusion CI → invisible listing jusqu'à suppression
