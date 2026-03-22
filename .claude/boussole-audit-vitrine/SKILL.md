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

### Taxonomie tags (16 tags — source de vérité : listing live)
```
Alimentation | Biologie | Dysautonomie | Épigénétique | Histamine | Hormones | Inflammation | Médicaments | Microbiote | Mitochondries | Neuromédiateurs | Pacing | Pharmacologie | SNA | Sommeil | Suppléments
```

**Règle absolue** : ne jamais inventer un tag. Si le contenu d'un article ne correspond à aucun tag de cette liste → choisir le plus proche parmi les 16. Si vraiment aucun ne convient → signaler à Rémy pour décision d'ajout de tag, mais ne pas en créer un nouveau sans validation explicite.
