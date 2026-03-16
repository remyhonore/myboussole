---
name: boussole-article-html
description: "Créer ou modifier un article HTML pour myboussole.fr. Utilise ce skill pour toute demande impliquant un article du site myboussole.fr (rédaction, mise en page, correction, audit SEO, ajout de section). Déclenche dès que l'utilisateur mentionne article, myboussole.fr, écrire un post sur le site, HTML article, déployer un article ou demande de créer du contenu web pour le site. Ce skill garantit le respect du template de référence, du front matter CI, des règles SEO, de la charte éditoriale et du vocabulaire contrôlé — sans aucune exception."
---

# Skill : Article HTML myboussole.fr

Ce skill encode toutes les règles de production d'un article pour myboussole.fr. Chaque règle est le fruit d'un audit réel — ne jamais les court-circuiter même si la demande semble simple.

---

## 0. Avant tout : récupérer le contexte

Avant de rédiger quoi que ce soit :
1. Chercher le sujet dans le Corpus Veille Clinique Notion (page 13) via Notion MCP
2. Vérifier les sources PubMed existantes via PubMed MCP
3. Vérifier la roadmap éditoriale Notion (page 07) pour le statut éditorial du sujet

---

## 1. Template de référence absolu

**Ne jamais créer un article from scratch.** La base est toujours `articles/covid-long-que-faire/index.html` dans le repo `remyhonore/myboussole`.

Structure du fichier (ordre absolu) :
1. Front matter (ligne 1, avant `<!DOCTYPE html>`)
2. `<!DOCTYPE html>` + `<head>` complet
3. Skip link accessibilité (première ligne du `<body>`)
4. `<header class="site-header">` — copie exacte
5. `<main id="main-content" class="article-wrapper"><div class="article-card">`
6. Contenu article
7. `</div></main>`
8. `<footer>` article
9. Scripts en fin de `<body>`

---

## 2. Front matter — obligatoire pour le CI

**Placer avant `<!DOCTYPE html>`, ligne 1 absolue du fichier.**
Sans ce bloc → l'article n'apparaît PAS dans `/articles/`.

```html
<!-- ---
title: "[titre article — aligné sur le H1]"
description: "[120-155 caractères — reprend le lead]"
slug: "[slug-kebab-case]"
date: "AAAA-MM-JJ"
readingTime: "X min"
tags: ["Tag1", "Tag2"]
author: "Dr Rémy Honoré"
image: "/articles/[slug]/[nom-image-hero].jpg"
--- -->
```

---

## 3. `<head>` — balises obligatoires

```html
<title>[50-62 caractères — intention de recherche]</title>
<meta name="description" content="[120-155 car.]">
<link rel="canonical" href="https://www.myboussole.fr/articles/[slug]/">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
```

**Open Graph (obligatoire) :**
```html
<meta property="og:title" content="[titre]">
<meta property="og:description" content="[description]">
<meta property="og:url" content="https://www.myboussole.fr/articles/[slug]/">
<meta property="og:type" content="article">
<meta property="og:image" content="https://www.myboussole.fr/articles/[slug]/[image-hero].jpg">
<meta name="twitter:card" content="summary_large_image">
```

**Schema.org JSON-LD (3 types dans un seul `<script>`) :**
- `Article` (headline, datePublished, dateModified, author, publisher)
- `BreadcrumbList` (3 niveaux : Accueil > Articles > titre)
- `FAQPage` (si FAQ présente — reprendre les Q/R exactes)

**Typographie :**
```html
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&display=swap" rel="stylesheet">
```

---

## 4. Header — copier-coller exact

**CSS dans `<style>` :**
```css
.site-header { background: rgba(248,246,240,0.85); backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px); border-bottom: 1px solid rgba(6,23,45,0.06); position: sticky; top: 0; z-index: 100; }
.topbar { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; max-width: 1100px; margin: 0 auto; padding: 0 24px; height: 60px; }
.topbar-logo { grid-column: 1; font-weight: 700; font-size: 18px; color: var(--forest); text-decoration: none; }
.topbar-nav { grid-column: 2; display: flex; gap: 32px; }
.topbar-nav a { color: var(--ink); text-decoration: none; font-size: 15px; font-weight: 500; opacity: 0.8; transition: opacity .15s; }
.topbar-nav a:hover { opacity: 1; }
.topbar-cta { grid-column: 3; display: flex; justify-content: flex-end; }
.btn-primary { background: var(--forest); color: #fff; padding: 8px 18px; border-radius: 8px; font-size: 14px; font-weight: 600; text-decoration: none; transition: background .15s; }
.btn-primary:hover { background: var(--forest-dark); }
.mobile-menu-btn { display: none; background: none; border: none; cursor: pointer; padding: 4px; }
@media (max-width: 640px) { .topbar-nav, .topbar-cta { display: none; } .mobile-menu-btn { display: flex; grid-column: 3; justify-self: end; } }
.mobile-nav { display: none; flex-direction: column; background: rgba(248,246,240,0.98); border-bottom: 1px solid rgba(6,23,45,0.08); padding: 12px 24px 16px; gap: 12px; }
.mobile-nav.open { display: flex; }
.mobile-nav a { font-size: 15px; font-weight: 500; color: var(--ink); text-decoration: none; padding: 6px 0; }
```

**HTML dans `<body>` :**
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

## 5. Layout — background + card

**Background body :**
```css
body {
  background:
    radial-gradient(950px 620px at 14% 0%, rgba(201,185,217,.45), transparent 60%),
    radial-gradient(920px 620px at 86% 8%, rgba(232,183,200,.40), transparent 62%),
    radial-gradient(1200px 700px at 55% 115%, rgba(110,135,125,.26), transparent 60%),
    linear-gradient(180deg, #F8F6F0, #F3F0E8);
}
```

**Wrapper + card :**
```html
<main id="main-content" class="article-wrapper">
  <div class="article-card">
    <!-- contenu -->
  </div>
</main>
```
```css
.article-wrapper { max-width: 800px; margin: 0 auto; padding: 48px 24px 80px; }
.article-card { background: rgba(255,255,255,.92); border-radius: 22px; box-shadow: 0 22px 60px rgba(0,0,0,.12); padding: clamp(28px, 4vw, 48px); }
```

---

## 6. Structure du contenu — ordre canonique

```
1. Skip link : <a href="#main-content" class="skip-link">Aller au contenu principal</a>
2. H1 (mots-clés identiques au <title>)
3. Chapeau (lead) — 2-3 phrases max
4. Encadré glossaire bilingue (si termes FR/EN — voir §9)
5. Sommaire ancré (si article ≥ 6 min)
6. Image hero
7. Corps de l'article (H2 avec id= pour ancres)
8. Micro-CTA Boussole (inline, avant le CTA principal)
9. FAQ (éléments <details>/<summary>)
10. CTA Boussole principal
11. Boutons de partage
12. Sources (liste numérotée)
13. Footer article
```

---

## 7. Règles illustrations

**Image hero :** JPEG, ratio 1.91:1 (1200×630px), < 200 Ko. Ideogram ou Canva. `loading="eager"` + `fetchpriority="high"`.

**CSS image hero (règle figée 14/03/2026) :**
```css
.hero-img { width: 100%; max-height: 340px; border-radius: 14px; margin: 28px 0 32px; display: block; object-fit: cover; object-position: center; }
```
⚠️ Ne jamais utiliser `aspect-ratio` seul sans `max-height`. Ne jamais mettre de `height` fixe. Issue du bug article SNA (image en plein écran).

**Illustrations internes :** SVG inline (priorité 1) ou BioRender (priorité 2). **Jamais d'image IA (Ideogram, DALL-E) dans le corps de l'article.** Jamais de stock photos.

Chaque grande section mécaniste doit avoir au moins 1 illustration interne. Articles sans visuels = non publiables.

---

## 8. Sources — format obligatoire

**Appel dans le texte :**
```html
<sup><a href="#source-N" aria-label="Source N">[N]</a></sup>
```

**Liste en bas de page :**
```html
<ol class="sources-list">
  <li id="source-1">Auteur et al. <em>Titre</em>. Journal. Année. <a href="https://pubmed.ncbi.nlm.nih.gov/PMID/" target="_blank" rel="noopener">Auteur et al., Année — PubMed</a></li>
</ol>
```

Chaque `[N]` dans le texte → entrée `id="source-N"` dans la liste. Sources HAS/NICE/OMS → lien direct officiel.

---

## 9. Règles terminologiques

**Encadrés expertise :** titre obligatoire `🔬 L'œil du Docteur en pharmacie` pour tout point pharmacologique ou clinique.

**Glossaire bilingue** (placer après le lead, avant le premier H2) :
```html
<div class="glossaire-bilingue">
  <h3>📖 Termes de référence</h3>
  <ul>
    <li>Terme français (SIGLE FR) = English term (EN)</li>
  </ul>
</div>
```
Corps du texte = terme français seul. Jamais le sigle anglophone seul.

**Noms de médicaments — marché français uniquement**

Toujours utiliser le nom commercial autorisé en France (ANSM / base Vidal). Jamais le nom FDA américain, ni le nom d'un autre pays européen.

| DCI | ❌ Nom étranger | ✅ Nom France |
|---|---|---|
| Escitalopram | Cipralex® (UK/BE), Lexapro® (USA) | Seroplex® |
| Zolpidem | Ambien® (USA) | Stilnox® |
| Vortioxétine | Trintellix® (USA) | Brintellix® |
| Sertraline | Zoloft® (identique FR/USA) | Zoloft® ✅ |
| Alprazolam | Xanax® (identique FR/USA) | Xanax® ✅ |

Règle opérationnelle : avant de nommer un médicament dans un article, vérifier sur base.vidal.fr ou ansm.sante.fr. En cas de doute, utiliser uniquement la DCI sans nom commercial.

**Termes interdits :** "PharmD" seul dans les articles, "Fatigue surrénalienne", "Leaky gut", "Détox", "Terrain" (sans sourçage), "Le Covid long cause X" (causalité).

---

## 10. Vocabulaire contrôlé Ordres

| ❌ À éviter | ✅ À utiliser |
|------------|--------------|
| Patients | Utilisateurs / Personnes |
| Diagnostic / Prescription | Pistes / Données scientifiques |
| Traitement | Approche nutritionnelle / Complément |
| Indication | Contexte d'étude / Niveau de preuve |
| Consulter (nous) | En parler à votre professionnel de santé |
| Protocole (sens thérapeutique) | Programme / Approche |
| PharmD (seul) | Docteur en pharmacie |
| Boussole+ (app actuelle) | Boussole (version freemium) |

**Valeurs chiffrées à ne jamais déformer :**
- 30 jours = fenêtre de données app (jamais 14j)
- 4 métriques : Énergie → Sommeil → Confort physique → Clarté mentale (ordre fixe)

---

## 11. Checklist rigueur scientifique

Avant toute soumission :
1. **Nosologie** : terme reconnu ICD-11 / DSM-5 / société savante ?
2. **Examens** : niveau de recommandation précisé (systématique / selon contexte / non routinier) ?
3. **Causalité** : "signal documenté" vs "association rapportée" vs "mécanisme suspecté" vs "preuve établie" ?
4. **Sources** : toute affirmation mécaniste sourcée (PubMed, guideline) ?
5. **Recommandations** : conformes HAS/NICE ou positionnement médecine fonctionnelle explicité ?

---

## 12. Après déploiement — checklist obligatoire

1. Mettre à jour `sitemap.xml` (URL + `lastmod` = date du jour)
2. Google Search Console : Inspection URL → Demander l'indexation
3. Mettre à jour les articles existants pouvant pointer vers le nouvel article (maillage entrant, min 3 liens internes)
4. Mettre à jour le statut dans la roadmap éditoriale Notion (page 07)
5. Poster dans le Corpus Articles myboussole.fr Notion (page 09)

---

## 13. Footer article — format obligatoire (figé 14/03/2026)

```html
<footer class="article-footer">
  <p>© 2026 <a href="https://www.myboussole.fr">myBoussole</a> · Dr Rémy Honoré, Docteur en pharmacie et nutrithérapeute</p>
  <p class="footer-disclaimer">Information à visée éducative, non substituable à un avis médical individualisé.</p>
</footer>
```

CSS à inclure dans `<style>` :
```css
.footer-disclaimer { font-size: 12px; color: var(--muted); margin-top: 4px; }
```

❌ INTERDIT : footer 1 ligne seule, encadré jaune en footer, `height` fixe sur `.hero-img`
❌ INTERDIT : disclaimer dans un `<div>` coloré — texte simple sous le copyright uniquement
