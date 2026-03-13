# CLAUDE.md — myboussole (vitrine)

Généré le 13/03/2026. Source de vérité : Boussole OS Notion.

---

## Identité du repo

- **Repo** : `github.com/remyhonore/myboussole`
- **Dev local** : `~/Projects/myboussole`
- **Déploiement** : Vercel auto-deploy sur `git push origin main`
- **URL prod** : `https://www.myboussole.fr`
- **Relation** : vitrine uniquement — l'app est dans le repo `remyhonore/boussole` (`app.myboussole.fr`)

---

## Architecture du repo

```
/
├── index.html                  # Page d'accueil vitrine
├── articles/
│   ├── index.html              # Listing articles — GÉNÉRÉ PAR CI (ne pas modifier manuellement)
│   ├── covid-long-que-faire/
│   │   └── index.html          # Template de référence absolu pour tout nouvel article
│   ├── brouillard-mental-covid-long/
│   ├── pacing-covid-long/
│   ├── reveil-fatigue-causes/
│   └── [slug]/
│       └── index.html
├── ecosysteme.html
├── rejoindre.html
├── confidentialite.html
├── sitemap.xml                 # À mettre à jour manuellement après chaque nouvel article
├── generate_content.py         # CI script — régénère articles/index.html depuis les front matters
└── CLAUDE.md                   # Ce fichier
```

---

## Règle CI — source de vérité articles

`articles/index.html` est **entièrement généré** par `generate_content.py` à chaque `git push`.

> ⚠️ Ne jamais modifier `articles/index.html` manuellement. Toute correction manuelle sera écrasée au prochain push.

**Source de vérité = front matter HTML de chaque article** (bloc commentaire avant `<!DOCTYPE html>`).

### Front matter obligatoire (ligne 1 absolue de chaque article) :

```html
<!-- ---
title: "Titre réel de l'article"
description: "Description 120-155 caractères"
slug: "slug-kebab-case"
date: "AAAA-MM-JJ"
readingTime: "X min"
tags: ["Tag1", "Tag2"]
author: "Dr Rémy Honoré"
image: "/articles/[slug]/[image-hero].jpg"
--- -->
```

**Règles front matter :**
- `title` : jamais de placeholder — doit être le titre réel
- `description` : jamais de placeholder — 120-155 caractères
- `slug` : jamais de placeholder — kebab-case, correspond au nom du dossier
- `tags` : séparateur virgule `,` — jamais espace seul (provoque un split incorrect en CI)
- Sans ce bloc → l'article n'apparaît PAS dans le listing `/articles/`

---

## Template de référence absolu

**Tout nouvel article doit copier** `articles/covid-long-que-faire/index.html` comme base.
Ne jamais créer from scratch.

### Structure obligatoire d'un article :

1. Front matter (avant `<!DOCTYPE html>`)
2. `<head>` avec balises SEO complètes (title, meta description, canonical, OG, Twitter Card, Schema.org JSON-LD)
3. Skip link accessibilité : `<a href="#main-content" class="skip-link">Aller au contenu principal</a>`
4. Header vitrine (copie exacte — voir section Header)
5. `<main id="main-content" class="article-wrapper"><div class="article-card">…</div></main>`
6. Footer : `© 2026 myBoussole · Dr Rémy Honoré, Docteur en pharmacie et nutrithérapeute`

### Background body (dégradé lavande — obligatoire) :

```css
body {
  background:
    radial-gradient(950px 620px at 14% 0%, rgba(201,185,217,.45), transparent 60%),
    radial-gradient(920px 620px at 86% 8%, rgba(232,183,200,.40), transparent 62%),
    radial-gradient(1200px 700px at 55% 115%, rgba(110,135,125,.26), transparent 60%),
    linear-gradient(180deg, #F8F6F0, #F3F0E8);
}
.article-wrapper { max-width: 800px; margin: 0 auto; padding: 48px 24px 80px; }
.article-card { background: rgba(255,255,255,.92); border-radius: 22px; box-shadow: 0 22px 60px rgba(0,0,0,.12); padding: clamp(28px, 4vw, 48px); }
```

---

## Header vitrine — copie exacte obligatoire

Ne jamais recréer manuellement. Copier depuis le template de référence.

### CSS (dans `<style>`) :

```css
.site-header { background: rgba(248,246,240,0.85); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid rgba(6,23,45,0.06); position: sticky; top: 0; z-index: 100; }
.topbar { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; max-width: 1100px; margin: 0 auto; padding: 0 24px; height: 60px; }
.topbar-logo { grid-column: 1; font-weight: 700; font-size: 18px; color: var(--forest); text-decoration: none; }
.topbar-nav { grid-column: 2; display: flex; gap: 32px; }
.topbar-nav a { color: var(--ink); text-decoration: none; font-size: 15px; font-weight: 500; opacity: 0.8; transition: opacity .15s; }
.topbar-cta { grid-column: 3; display: flex; justify-content: flex-end; }
.btn-primary { background: var(--forest); color: #fff; padding: 8px 18px; border-radius: 8px; font-size: 14px; font-weight: 600; text-decoration: none; }
.mobile-menu-btn { display: none; background: none; border: none; cursor: pointer; padding: 4px; }
@media (max-width: 640px) { .topbar-nav, .topbar-cta { display: none; } .mobile-menu-btn { display: flex; grid-column: 3; justify-self: end; } }
.mobile-nav { display: none; flex-direction: column; background: rgba(248,246,240,0.98); border-bottom: 1px solid rgba(6,23,45,0.08); padding: 12px 24px 16px; gap: 12px; }
.mobile-nav.open { display: flex; }
.mobile-nav a { font-size: 15px; font-weight: 500; color: var(--ink); text-decoration: none; padding: 6px 0; }
```

### HTML (dans `<body>`) :

```html
<header class="site-header">
  <nav class="topbar">
    <a href="https://www.myboussole.fr" class="topbar-logo">🧭 myboussole</a>
    <div class="topbar-nav">
      <a href="https://www.myboussole.fr/articles/">Articles</a>
      <a href="https://www.myboussole.fr/ecosysteme.html">Écosystème</a>
    </div>
    <div class="topbar-cta">
      <a href="https://app.myboussole.fr" class="btn-primary">Essayer Boussole</a>
    </div>
    <button class="mobile-menu-btn" onclick="document.querySelector('.mobile-nav').classList.toggle('open')" aria-label="Menu">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>
    </button>
  </nav>
  <nav class="mobile-nav">
    <a href="https://www.myboussole.fr/articles/">Articles</a>
    <a href="https://www.myboussole.fr/ecosysteme.html">Écosystème</a>
    <a href="https://app.myboussole.fr">Essayer Boussole</a>
  </nav>
</header>
```

---

## Palette couleurs

```css
--forest      : #2d6a4f   /* couleur primaire unique — ADR-2026-027 */
--forest-dark : #1e4d38
--navy        : #06172D
--ink         : #1a2332
--muted       : #6b7280
--surface     : #F8F6F0
```

---

## Typographie

Police unique : **Plus Jakarta Sans** (Google Fonts). Ne jamais substituer par Inter, Roboto ou polices système.

```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
```

Graisses : H1 hero → 800 / letter-spacing -0.03em | Titres articles → 600 | Corps → 400-500

---

## Règles workflow Claude Code

### Règle d'or : 1 prompt = 1 opération = 1 fichier = 1 commit

### Template prompt universel :

```
Fichier cible : [chemin/vers/fichier.html]

Opération : [description courte et précise de l'unique modification]

Lis d'abord le fichier. Repère [élément spécifique à modifier].
Remplace [ancien contenu exact] par [nouveau contenu exact].

Vérifie que [élément attendu] est présent dans le fichier.

Si OK : git add [fichier] && git commit -m "[type]: [description]" && git push origin main
Si KO : affiche ce que tu trouves sans modifier ni pusher.
```

### Règles critiques :
1. **Lire avant de modifier** — toujours lire le fichier cible avant str_replace
2. **Une opération par prompt** — jamais plusieurs corrections dans le même prompt
3. **Vérifier avant pusher** — inclure une étape de vérification dans chaque prompt
4. **git pull --rebase** avant tout push après un conflit
5. **Ne jamais toucher `articles/index.html`** — c'est la CI qui le gère

### Checklist non-régression (à inclure sur tout prompt modifiant articles) :
```
Avant de committer, vérifie :
1. Le front matter est complet (title, description, slug, date, tags, image)
2. Le slug correspond au nom du dossier parent
3. Les tags utilisent la virgule comme séparateur
4. Le header vitrine est le copier-coller exact (grid 3 colonnes)
5. Le background body est le dégradé lavande/rose/sage

Si tous OK → committer et pusher.
Si KO → corriger sans pusher.
```

---

## Après chaque nouvel article

1. Mettre à jour `sitemap.xml` (URL + `lastmod` = date du jour)
2. Google Search Console : Inspection URL → Demander l'indexation
3. Mettre à jour les articles existants pouvant créer du maillage entrant
4. Mettre à jour la roadmap éditoriale Notion (page 07)

---

## Liens utiles

- App Boussole : `https://app.myboussole.fr` (repo `remyhonore/boussole`)
- Boussole OS Notion : page `🧠 Boussole OS — Mémoire IA`
- Guide Prompts Claude Code : page 22 Boussole OS
- Brand rules complètes : page 04 Boussole OS
- Checklist SEO complète : page 04 Boussole OS section "Checklist SEO & technique"
