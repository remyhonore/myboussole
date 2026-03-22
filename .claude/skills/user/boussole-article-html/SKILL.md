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

## 0bis. Audit obligatoire avant toute modification d'article existant

Avant de modifier un article déjà déployé (correction, ajout de section, update front matter, fix CSS…) :

1. Fetcher l'article live : web_fetch https://www.myboussole.fr/articles/[slug]/
2. Vérifier avant de toucher au code :
   - H1 présent et cohérent avec le titre front matter
   - Image hero accessible (pas de 404)
   - Canonical présent et correct
   - Aucun placeholder visible ("TODO", "à compléter", "lorem")
   - Footer 2 lignes présent (copyright + disclaimer éducatif)
   - Noms de médicaments = marché France uniquement (ANSM/Vidal)
3. Documenter les anomalies dans le chat avant de commencer
4. Corriger les anomalies dans le même commit que la modification demandée

**Principe :** toute session qui touche un article repart avec cet article dans un état meilleur qu'avant — jamais neutre, jamais dégradé.

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
level: "[debutant|intermediaire|expert]"
tags: ["Tag1", "Tag2"]
author: "Dr Rémy Honoré"
image: "/articles/[slug]/[nom-image-hero].jpg"
--- -->
```

**Règle déploiement :** Ne jamais utiliser `draft: true` dans un article poussé sur le repo. Le brouillon reste dans Notion (base 09). Quand un article est déployé sur le repo, il est déployé complet en une seule opération : article finalisé + sitemap + maillage entrant. Pas d'état intermédiaire "draft en ligne".

> Format étendu supporté : `"AAAA-MM-JJTHH:MM"` — utiliser si deux articles sont publiés le même jour pour contrôler l'ordre d'affichage dans le listing (`generate_content.py` trie par datetime, commit 1ff5c38).

### 2b. Vocabulaire contrôlé — tags autorisés

**Niveaux de lecture — champ `level` obligatoire**

Ajouter `level:` dans le front matter de chaque article, après `readingTime:`.

| Valeur | Label affiché | Profil |
|---|---|---|
| `"debutant"` | Grand public | Pas de bagage scientifique, vulgarisation pure |
| `"intermediaire"` | Public averti | Familier du sujet, comprend SNA/MPE/pacing |
| `"expert"` | Public expert | Professionnel de santé, mécanismes moléculaires |

Fallback si absent : `"intermediaire"` (géré par `generate_content.py`).
Règle : tout article déployé sans `level` s'affiche automatiquement en "Public averti".

### Vocabulaire par niveau de lecture — règle obligatoire

Le niveau déclaré dans le front matter conditionne le vocabulaire autorisé dans tout l'article, y compris l'encadré PharmD.

**Grand public (`debutant`) — termes interdits sans reformulation :**
- Noms de cytokines bruts : RANTES, TNF-α, IL-6, IFN-γ → reformuler : "molécules pro-inflammatoires (protéines de signalisation du système immunitaire)"
- Dysfonction mitochondriale → "perturbation de la production d'énergie cellulaire"
- Activation immunitaire de faible grade → "inflammation de faible intensité"
- Dysautonomie → expliquer à la 1ère occurrence : "dérèglement du système nerveux autonome"
- Acronymes non définis dès la 1ère occurrence (PEM, POTS, HRV, SAM, RMSSD…)
- Maximum 1 mécanisme moléculaire par section — le reste en langage courant

**Public averti (`intermediaire`) :**
- Termes courants du domaine acceptés sans définition (SNA, PEM, HRV, pacing, dysautonomie)
- Cytokines majeures acceptées une fois si clés pour le propos ("TNF-α, une cytokine pro-inflammatoire")
- Mécanismes scientifiques si la phrase reste lisible — cascades complexes résumées

**Public expert (`expert`) :**
- Vocabulaire scientifique complet sans restriction
- Mécanismes moléculaires détaillés attendus
- Sources : niveau élevé obligatoire (méta-analyses, RCT, cohortes contrôlées)

**Règle encadré PharmD :** l'encadré peut dépasser d'un niveau le reste de l'article — jamais de 2 niveaux d'écart. Article `debutant` → encadré accessible. Article `intermediaire` → vocabulaire scientifique standard. Article `expert` → moléculaire autorisé.

**Check obligatoire avant déploiement :** relire l'encadré PharmD avec le `level` du front matter en tête. Si un passage dépasse le niveau déclaré → simplifier OU changer le `level`.

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

**Liens externes — règle absolue :**
Tout lien `target="_blank"` doit avoir `rel="noopener noreferrer"` (pas seulement `rel="noopener"`).
Appliquer à : tous les liens sources PubMed, tous les boutons de partage (Facebook, LinkedIn, copier), toute URL externe.

**Schema.org JSON-LD (3 types dans un seul `<script>`) :**
- `Article` (headline, datePublished, dateModified, author, publisher, wordCount, inLanguage: "fr", mainEntityOfPage pointant vers l'URL canonique)
- `BreadcrumbList` (3 niveaux : Accueil > Articles > titre)
- `FAQPage` (si FAQ présente — reprendre les Q/R exactes)

**Exemple de bloc Article complet :**
```json
{
  "@type": "Article",
  "headline": "[titre]",
  "datePublished": "AAAA-MM-JJ",
  "dateModified": "AAAA-MM-JJ",
  "author": { "@type": "Person", "name": "Dr Rémy Honoré" },
  "publisher": { "@type": "Organization", "name": "myBoussole" },
  "wordCount": 2500,
  "inLanguage": "fr",
  "mainEntityOfPage": { "@type": "WebPage", "@id": "https://www.myboussole.fr/articles/[slug]/" }
}
```

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
1.  Skip link : <a href="#main-content" class="skip-link">Aller au contenu principal</a>
2.  H1 (mots-clés identiques au <title>)
3.  Chapeau (lead) — 2-3 phrases max
4.  Bloc synthesis grille 2×2 — voir §6b — OBLIGATOIRE
5.  Sommaire ancré (si article ≥ 6 min)
6.  Glossaire bilingue en accordéon — voir §6a — APRÈS le sommaire ← [20/03/2026]
7.  Image hero (positionnée après le glossaire)
8.  Corps de l'article (H2 avec id= pour ancres)
9.  Micro-CTA Boussole (inline, avant le CTA principal)
10. Bloc résumé épistémique — voir §6c — OBLIGATOIRE ← [21/03/2026]
11. FAQ (éléments <details>/<summary>)
12. CTA Boussole principal
13. Boutons de partage (3 boutons : Facebook · LinkedIn · Copier le lien) ← [20/03/2026]
14. Sources (liste numérotée)
15. Footer article
```

**CSS obligatoire :**
```css
.section-label { font-size: 14px; font-weight: 700; color: var(--ink); margin-bottom: 12px; }
.cta-title { font-size: 20px; font-weight: 800; margin-bottom: 12px; color: #fff; }
```

---

## 6a. Glossaire bilingue — accordéon discret

**Règle :** Le glossaire est placé dans un `<details>` fermé par défaut, **après le sommaire** (pas avant). Le lecteur expert passe, le lecteur débutant ouvre.

**Position :** après le sommaire (§5), avant l'image hero (§7). ← [20/03/2026]

**CSS obligatoire :**
```css
.glossaire-accordion { margin-bottom: 20px; }
.glossaire-accordion summary {
  font-size: 13px; font-weight: 700; color: var(--forest);
  cursor: pointer; list-style: none; display: flex;
  align-items: center; gap: 8px; padding: 10px 16px;
  background: rgba(45,106,79,0.05); border-radius: 8px;
  border: 1px solid rgba(45,106,79,0.15);
}
.glossaire-accordion summary::after { content: "+"; font-size: 16px; margin-left: auto; }
.glossaire-accordion[open] summary::after { content: "−"; }
.glossaire-accordion .glossaire-bilingue {
  background: rgba(110,135,125,0.07); border-radius: 0 0 8px 8px;
  padding: 14px 18px; margin-top: -1px;
  border: 1px solid rgba(45,106,79,0.15); border-top: none;
}
.glossaire-bilingue ul { padding-left: 18px; margin: 0; }
.glossaire-bilingue li { font-size: 14px; margin-bottom: 4px; color: var(--ink); }
```

**HTML template :**
```html
<details class="glossaire-accordion">
  <summary>📖 Termes de référence</summary>
  <div class="glossaire-bilingue">
    <ul>
      <li>Terme français (SIGLE FR) = English term (EN)</li>
      <li>Terme français (SIGLE FR) = English term (EN)</li>
    </ul>
  </div>
</details>
```

**Ce qui est interdit :**
- ❌ Glossaire en bloc ouvert (ancien style `.glossaire-bilingue` direct)
- ❌ Glossaire placé entre le lead et le synthesis (ancienne position — abandonnée 20/03/2026)
- ❌ Titre du glossaire en `<h3>` ou `<h2>`

---

## 6b. Bloc synthesis — grille 2×2 éditorial

**Règle :** Tout article doit avoir un bloc synthesis. Jamais de liste à puces sur fond vert monochrome.

**Position :** entre le lead (§3) et le sommaire (§5).

**CSS obligatoire :**
```css
.article-synthesis {
  background: rgba(45,106,79,0.06);
  border: 1px solid rgba(45,106,79,0.18);
  border-radius: 14px; padding: 22px 24px; margin-bottom: 36px;
}
.synthesis-label {
  font-size: 12px; font-weight: 800; color: var(--forest);
  text-transform: uppercase; letter-spacing: .1em; margin-bottom: 16px;
}
.synthesis-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
@media (max-width: 560px) { .synthesis-grid { grid-template-columns: 1fr; } }
.synthesis-card {
  display: flex; gap: 12px; align-items: flex-start;
  background: #fff; border-radius: 10px; padding: 14px 16px;
  box-shadow: 0 1px 6px rgba(6,23,45,0.06);
}
.synthesis-icon { font-size: 20px; line-height: 1; flex-shrink: 0; margin-top: 1px; }
.synthesis-card-title { font-size: 14px; font-weight: 700; color: var(--navy); margin-bottom: 5px; }
.synthesis-card-text { font-size: 13px; color: var(--muted); line-height: 1.55; margin: 0; }
```

**HTML template :**
```html
<div class="article-synthesis">
  <p class="synthesis-label">⚡ L'essentiel en 4 points</p>
  <div class="synthesis-grid">
    <div class="synthesis-card">
      <span class="synthesis-icon">🔬</span>
      <div>
        <p class="synthesis-card-title">[Titre 2-4 mots]</p>
        <p class="synthesis-card-text">[1-2 phrases. Niveau de preuve proportionnel.]</p>
      </div>
    </div>
    <div class="synthesis-card">
      <span class="synthesis-icon">📊</span>
      <div>
        <p class="synthesis-card-title">[Titre 2-4 mots]</p>
        <p class="synthesis-card-text">[1-2 phrases.]</p>
      </div>
    </div>
    <div class="synthesis-card">
      <span class="synthesis-icon">💡</span>
      <div>
        <p class="synthesis-card-title">[Titre 2-4 mots]</p>
        <p class="synthesis-card-text">[1-2 phrases.]</p>
      </div>
    </div>
    <div class="synthesis-card">
      <span class="synthesis-icon">🧭</span>
      <div>
        <p class="synthesis-card-title">[Titre 2-4 mots]</p>
        <p class="synthesis-card-text">[1-2 phrases.]</p>
      </div>
    </div>
  </div>
</div>
```

**Règles de rédaction :**
- Titres : 2-4 mots, affirmatifs, sans verbe conjugué
- Texte : 1-2 phrases max, formulation proportionnelle au niveau de preuve (§11b)
- Icônes selon sujet : 🔬 mécanisme · 📊 données · 💡 point clinique · 🧭 pratique · ⚡ signal · 🧬 biologie · 💊 pharmacologie · 📡 SNA · 🔋 énergie
- Les 4 cartes doivent couvrir 4 angles distincts : mécanisme / données / clinique / pratique
- Ne jamais copier les mêmes 4 cartes sur deux articles différents

**Ce qui est interdit :**
- ❌ `background: var(--forest)` sur `.article-synthesis` (ancien style vert plein)
- ❌ `<ul class="synthesis-list">` avec `<li>` blancs sur fond vert
- ❌ Plus de 2 phrases par carte
- ❌ Titres de carte en `<h2>` ou `<h3>` — toujours `<p class="synthesis-card-title">`

---

## 6c. Bloc résumé épistémique — OBLIGATOIRE en fin d'article ← [20/03/2026]

**Règle :** Tout article doit se terminer (avant le CTA) par un bloc distinguant ce qui est établi de ce qui reste spéculatif. Objectif : rigueur scientifique visible, déculpabilisation du lecteur, transparence sur les limites.

**Position :** après le corps de l'article et le micro-CTA (§9), avant la FAQ (§11). ← [21/03/2026]

**CSS obligatoire :**
```css
.article-epistemic {
  background: rgba(6,23,45,0.04);
  border: 1px solid rgba(6,23,45,0.10);
  border-radius: 12px; padding: 22px 26px; margin: 36px 0;
}
.epistemic-label {
  font-size: 13px; font-weight: 800; text-transform: uppercase;
  letter-spacing: .08em; color: var(--navy); margin-bottom: 12px;
}
```

**HTML template :**
```html
<div class="article-epistemic">
  <p class="epistemic-label">🧩 Ce que l'on sait — et ce que l'on ne sait pas encore</p>
  <p>[Paragraphe 1 — ce qui est documenté : données, associations, preuves existantes avec niveau de preuve.]</p>
  <p>[Paragraphe 2 — ce qui reste spéculatif ou non encore validé en RCT : mécanismes incertains, interventions préliminaires, limites de la littérature disponible.]</p>
</div>
```

**Règles de rédaction :**
- Toujours 2 paragraphes distincts : "ce qu'on sait" / "ce qui reste spéculatif"
- Ne jamais écrire de faux équilibre — si les données sont solides, le dire
- Niveau de preuve dans ce bloc ≤ niveau affiché dans le corps de l'article
- Ne jamais terminer par une promesse ou un CTA implicite

---

## 6d. Boutons de partage — 3 boutons obligatoires ← [20/03/2026]

**Règle :** 3 boutons systématiques : Facebook · LinkedIn · Copier le lien.

**Position :** après les sources (§14), avant le footer (§15).

**CSS obligatoire :**
```css
.share-block { display: flex; gap: 12px; align-items: center; margin: 28px 0; flex-wrap: wrap; }
.share-label { font-size: 14px; font-weight: 600; color: var(--muted); }
.share-btn { display: inline-flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 600; text-decoration: none; transition: opacity .15s; }
.share-btn:hover { opacity: 0.85; }
.share-fb { background: #1877f2; color: #fff; }
.share-li { background: #0a66c2; color: #fff; }
.share-copy { background: rgba(6,23,45,0.07); color: var(--ink); border: 1px solid rgba(6,23,45,0.15); cursor: pointer; font-family: inherit; }
.share-copy:hover { background: rgba(6,23,45,0.12); }
.share-copy.copied { background: var(--forest); color: #fff; border-color: var(--forest); }
```

**HTML template :**
```html
<div class="share-block">
  <span class="share-label">Partager :</span>
  <a href="https://www.facebook.com/sharer/sharer.php?u=https://www.myboussole.fr/articles/[slug]/"
     class="share-btn share-fb" target="_blank" rel="noopener noreferrer">Facebook</a>
  <a href="https://www.linkedin.com/sharing/share-offsite/?url=https://www.myboussole.fr/articles/[slug]/"
     class="share-btn share-li" target="_blank" rel="noopener noreferrer">LinkedIn</a>
  <button class="share-btn share-copy" id="copy-btn" onclick="copyArticleLink()" aria-label="Copier le lien de l'article">
    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"
         stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <rect x="9" y="9" width="13" height="13" rx="2"/>
      <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
    </svg>
    <span id="copy-label">Copier le lien</span>
  </button>
</div>
```

**JS obligatoire (dans `<script>` en fin de `<body>`) :**
```javascript
function copyArticleLink() {
  const btn = document.getElementById('copy-btn');
  const label = document.getElementById('copy-label');
  const url = 'https://www.myboussole.fr/articles/[slug]/';
  navigator.clipboard.writeText(url).then(() => {
    btn.classList.add('copied');
    label.textContent = 'Lien copié !';
    setTimeout(() => { btn.classList.remove('copied'); label.textContent = 'Copier le lien'; }, 2000);
  }).catch(() => {
    const el = document.createElement('textarea');
    el.value = url; el.style.position = 'fixed'; el.style.opacity = '0';
    document.body.appendChild(el); el.select(); document.execCommand('copy');
    document.body.removeChild(el);
    btn.classList.add('copied'); label.textContent = 'Lien copié !';
    setTimeout(() => { btn.classList.remove('copied'); label.textContent = 'Copier le lien'; }, 2000);
  });
}
```

**⚠️ Remplacer `[slug]` dans l'URL du bouton Copier ET dans la fonction JS.**

---

## 7. Règles illustrations

**Image hero :** JPEG, ratio 1.91:1 (1200×630px), < 200 Ko. Ideogram ou Canva. `loading="lazy"` + `decoding="async"`.
(La hero n'est pas au-dessus de la ligne de flottaison sur mobile — eager est contre-productif.)

**CSS image hero (règle figée 14/03/2026) :**
```css
.hero-img { width: 100%; max-height: 340px; border-radius: 14px; margin: 28px 0 32px; display: block; object-fit: cover; object-position: center; }
```
⚠️ Ne jamais utiliser `aspect-ratio` seul sans `max-height`. Ne jamais mettre de `height` fixe. Issue du bug article SNA (image en plein écran).

**Illustrations internes :** SVG inline (priorité 1) ou BioRender (priorité 2). **Jamais d'image IA (Ideogram, DALL-E) dans le corps de l'article.** Jamais de stock photos.

### 7a. Nombre minimum de SVG inline par article ← [21/03/2026]

| Longueur article | Temps de lecture | SVG inline minimum |
|---|---|---|
| < 1 500 mots | ≤ 7 min | 2 |
| 1 500 – 2 500 mots | 8-12 min | 3 |
| > 2 500 mots | ≥ 13 min | 4-5 |

**Règle de couverture :** au moins 1 SVG pour chaque section mécaniste (H2 qui décrit un processus biologique, une cascade, ou un modèle physiopathologique). Les sections pratiques (leviers, examens, FAQ) n'exigent pas de SVG mais peuvent en bénéficier.

**Accessibilité SVG obligatoire — chaque SVG inline doit avoir :**
1. `role="img"` sur l'élément `<svg>`
2. `aria-label="[description courte]"` sur l'élément `<svg>`
3. `<title>` comme **premier enfant** de `<svg>` (contenu identique ou proche de `aria-label`)
4. Une légende `<p class="diagram-caption">` immédiatement sous le `<svg>`

**HTML template SVG :**
```html
<svg role="img" aria-label="[description courte du diagramme]"
     viewBox="0 0 [w] [h]" xmlns="http://www.w3.org/2000/svg">
  <title>[Description courte du diagramme]</title>
  <!-- contenu SVG -->
</svg>
<p class="diagram-caption">[Légende visible — ex : Figure 1. Cascade inflammatoire post-infectieuse]</p>
```

**CSS obligatoire :**
```css
.diagram-caption { font-size: 13px; color: var(--muted); text-align: center; margin: 8px 0 28px; font-style: italic; }
```

**Ce qui est interdit :**
- ❌ SVG sans `role="img"` ni `aria-label`
- ❌ SVG sans `<title>` comme premier enfant
- ❌ SVG sans légende `<p class="diagram-caption">` en dessous
- ❌ Article publié avec moins de SVG que le minimum du tableau ci-dessus
- ❌ Section mécaniste (H2 processus biologique/cascade/physiopathologie) sans SVG

Articles sans le nombre minimum de SVG = non publiables.

---

## 8. Sources — format obligatoire

### 🔴 Règle critique : vérification obligatoire des PMIDs

**Avant toute intégration d'un PMID dans un article, sans exception :**
1. Appeler `PubMed:get_article_metadata` avec le PMID
2. Vérifier que le **titre retourné par PubMed** correspond au **titre affiché dans l'article**
3. Si le titre ne correspond pas → PMID faux → bloquer l'article, ne pas déployer
4. Un PMID faux sur un article publié = erreur de crédibilité grave

**Pourquoi cette règle existe :**
Un audit réel (16/03/2026) a révélé que 5 PMIDs sur 8 dans un article publié pointaient vers des articles sans aucun rapport avec le sujet (physique des matériaux, chirurgie ORL, biologie de la drosophile). Origine : hallucination LLM lors de la rédaction. Les PMIDs existaient dans PubMed — mais ne correspondaient pas aux titres affichés.

**Règle absolue : zéro PMID non vérifié via PubMed MCP dans un article publié.**

---

**Appel dans le texte :**
```html
<sup><a href="#source-N" aria-label="Source N">[N]</a></sup>
```

**Liste en bas de page :**
```html
<ol class="sources-list">
  <li id="source-1">Auteur et al. <em>Titre</em>. Journal. Année. <a href="https://pubmed.ncbi.nlm.nih.gov/PMID/" target="_blank" rel="noopener noreferrer">Auteur et al., Année — PubMed</a></li>
</ol>
```

Chaque `[N]` dans le texte → entrée `id="source-N"` dans la liste. Sources HAS/NICE/OMS → lien direct officiel.

---

## 9. Règles terminologiques

**Encadrés expertise :** titre obligatoire `👁️ L'œil du Docteur en pharmacie` pour tout point pharmacologique ou clinique.

**Glossaire bilingue :** voir §6a pour la position et le template complet (accordéon après le sommaire).
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
     → **Vérification PMID obligatoire** : appeler `PubMed:get_article_metadata` sur chaque PMID et confirmer que le titre retourné = titre affiché dans l'article. Aucune exception. Un PMID non vérifié = article non publiable.
5. **Recommandations** : conformes HAS/NICE ou positionnement médecine fonctionnelle explicité ?

### 11b. Rigueur rédactionnelle — formulations calibrées

Le niveau de preuve doit se refléter dans le vocabulaire. Ne jamais sur-affirmer ni sous-affirmer.

| Niveau | Formulations autorisées | Formulations interdites |
|---|---|---|
| ✅ Solide (méta-analyse, RCT) | "montre que", "est associé à", "réduit significativement" | "prouve définitivement", "guérit" |
| ⚠️ Probable (cohortes, observationnel) | "suggère que", "est cohérent avec", "est associé à" | "démontre", "confirme" |
| 🔄 Spéculatif (mécanisme plausible, in vitro) | "pourrait", "est plausible", "le mécanisme proposé est" | "explique", "cause", "entraîne" |
| ❌ Insuffisant | "on ne peut pas conclure", "les données sont insuffisantes" | toute affirmation directionnelle |

**Règles additionnelles :**
- Association ≠ causalité : ne jamais écrire "X cause Y" sans RCT
- Animal ≠ humain : toujours préciser la population étudiée
- Mécanisme ≠ efficacité clinique : un mécanisme plausible n'est pas une preuve d'effet
- Deep research et Perplexity peuvent fournir de faux PMIDs — toujours vérifier avant intégration

---

## 12. Déploiement — règles obligatoires

Le déploiement se fait EXCLUSIVEMENT via Claude Code.

⚠️ **Source d'un fichier uploadé depuis claude.ai :**
- Toujours `~/Downloads/[nom-du-fichier]` dans le prompt Claude Code
- JAMAIS `/mnt/user-data/uploads/` — ce chemin n'existe pas en local sur le Mac

**Template prompt Claude Code — déploiement fichier uploadé :**

```
Fichier source : ~/Downloads/index.html
Destination : ~/Projects/myboussole/articles/[slug]/index.html

1. Affiche : wc -l ~/Downloads/index.html
2. Compare : diff ~/Downloads/index.html [destination]
3. Copie : cp ~/Downloads/index.html [destination]
4. Vérifie : wc -l [destination] && git -C ~/Projects/myboussole diff --stat
5. git add [destination] && git commit -m "[type]: [description]" && git push origin main
6. Confirme le hash. Si push échoue, affiche la commande de retry.
```

**Workflow déploiement standard :**

```
Bloc 1 — TERMINAL : cd ~/Projects/myboussole && claude
Bloc 2 — CLAUDE CODE : [prompt structuré ci-dessus]
```

**Checklist post-déploiement :**
1. Mettre à jour `sitemap.xml` (URL + `lastmod` = date du jour)
2. Google Search Console : Inspection URL → Demander l'indexation
3. Maillage entrant : min 3 liens internes vers le nouvel article
4. Mettre à jour le statut dans la roadmap éditoriale Notion (page 07)
5. Poster dans le Corpus Articles myboussole.fr Notion (page 09)

---

## 14. Footer article — format obligatoire (figé 14/03/2026)

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

---

## 15. Corrections SEO récurrentes — checklist post-audit

Ces erreurs reviennent à chaque article. Les corriger en amont lors de la rédaction, pas après déploiement.

| Erreur récurrente | Règle |
|---|---|
| H1 → H3 direct (glossaire, sommaire) | Toujours `<p class="section-label">`, jamais `<h3>` sans H2 parent |
| SVG sans ARIA | Chaque `<svg>` doit avoir `role="img"` + `aria-label` + `<title>` premier enfant + `<p class="diagram-caption">` sous le SVG |
| SVG insuffisants | Vérifier le minimum §7a : <1500 mots→2, 1500-2500→3, >2500→4-5. Chaque H2 mécaniste→1 SVG min |
| `rel="noopener"` seul | Toujours `rel="noopener noreferrer"` sur tout `target="_blank"` |
| Schema Article incomplet | Ajouter `wordCount`, `inLanguage`, `mainEntityOfPage` à chaque article |
| `loading="eager"` sur hero | Utiliser `loading="lazy" decoding="async"` |
| H3 dans bloc CTA | Utiliser `<p class="cta-title">` |
| Cohérence sommaire ↔ H2 | Le texte du lien dans le sommaire doit être identique au H2 cible |
| `.site-footer` dans le CSS | Toujours nommer `.article-footer` — le HTML utilise `class="article-footer"`. Vérifier : `grep 'site-footer\|article-footer' articles/{slug}/index.html` |
| `date:` sans heure | Format `"AAAA-MM-JJTHH:MM"` supporté — obligatoire si 2 articles le même jour |
| Bouton copier sans fallback JS | Toujours inclure le `execCommand('copy')` fallback dans `copyArticleLink()` |
| Glossaire avant le sommaire | Depuis 20/03/2026 : glossaire après le sommaire, pas avant |
