# DESIGN SYSTEM — myboussole.fr
> Source de vérité unique pour tous les styles visuels du site.
> **Claude Code doit lire ce fichier avant toute modification CSS ou HTML.**
> Si un composant demandé n'y est pas défini → signaler à Rémy plutôt qu'improviser.

---

## 1. Variables CSS (`:root`)

```css
:root {
  /* Fonds */
  --paper:   #F3F0E8;       /* fond cards, sections alternées */
  --paper2:  #F8F6F0;       /* fond global par défaut */

  /* Texte */
  --ink:     #06172D;       /* texte principal */
  --muted:   rgba(6,23,45,.72);   /* texte secondaire */
  --muted2:  rgba(6,23,45,.58);   /* texte tertiaire, footer */

  /* Couleurs d'accent */
  --sage:       #6E877D;    /* vert sauge — accents doux */
  --terracotta: #C97A61;    /* terracotta — highlights chauds */
  --lavender:   #C9B9D9;    /* lavande — fond dégradé gauche */
  --rose:       #E8B7C8;    /* rose — fond dégradé droite */

  /* Bordures */
  --border:     rgba(6,23,45,.12);
  --borderSoft: rgba(6,23,45,.08);

  /* Ombres */
  --shadow:     0 22px 60px rgba(6,23,45,.16);
  --shadowSoft: 0 14px 34px rgba(6,23,45,.11);

  /* Forme */
  --radius:  22px;
  --radius2: 28px;

  /* Espacement */
  --pad: clamp(18px, 3.2vw, 34px);
  --max: 1160px;            /* max-width conteneur */

  /* Typographie */
  --serif: ui-serif, Georgia, "Times New Roman", Times, serif;
  --sans:  ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;

  /* Aliases couleurs (compatibilité) */
  --color-border:   #e9ecef;
  --color-text:     #1a1a2e;
  --color-accent:   #2d6a4f;    /* vert primaire — boutons, liens actifs */
  --color-accent-2: #1b4332;    /* vert foncé — hover */
}
```

---

## 2. Fond de page (body background)

Dégradé radial 4 couches — identique sur toutes les pages :

```css
body {
  background:
    radial-gradient(950px 620px at 14% 0%,   rgba(201,185,217,.45), transparent 60%),
    radial-gradient(920px 620px at 86% 8%,   rgba(232,183,200,.40), transparent 62%),
    radial-gradient(1200px 700px at 55% 115%, rgba(110,135,125,.26), transparent 60%),
    linear-gradient(#F8F6F0, #F3F0E8);
}
```

---

## 3. Header (`.site-header`)

```css
.site-header {
  background: rgba(248,246,240,0.85) !important;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  border-bottom: 1px solid rgba(6,23,45,0.06);
  position: sticky;
  top: 0;
  z-index: 100;
}
```

**Logo :** `myboussole` (texte + icône boussole) — PAS "Boussole" seul.
**Nav :** Articles · Écosystème
**CTA :** bouton `.btn-primary` → "Essayer Boussole"

---

## 4. Boutons

### Bouton primaire (`.btn.btn-primary`)
```css
.btn-primary {
  background: #2d6a4f;      /* --color-accent */
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  font-family: var(--sans);
  padding: 8px 18px;
  border-radius: 8px;
  border: none;
  text-decoration: none;
}
.btn-primary:hover {
  background: #1b4332;      /* --color-accent-2 */
}
```

### Lien secondaire (`.btn:not(.btn-primary)`)
```css
.btn:not(.btn-primary) {
  background: transparent;
  color: #2d6a4f;             /* --color-accent */
  font-size: 16px;
  font-weight: 600;
  font-family: var(--sans);
  text-decoration: underline;
  text-decoration-color: rgba(45,106,79,0.4);
  text-underline-offset: 3px;
  padding: 0;
  border: none;
  border-radius: 0;
}
```

> ⚠️ Règle globale — s'applique à TOUS les `.btn` sans `.btn-primary`, partout sur le site.
> Ne pas restreindre à `.hero .btn:not(.btn-primary)`.

---

## 5. Typographie

| Élément | Font | Taille | Poids | Couleur |
|---------|------|--------|-------|---------|
| `h1` | `--serif` | `clamp(42px, 6vw, 72px)` | 780 | `--ink` |
| `h2` | `--serif` | `~32px` | 700 | `--ink` |
| `h3` | `--sans` | `16px` | 700 | `--ink` |
| body | `--sans` | `16px` | 400 | `--ink` |
| footer | `--sans` | `~13px` | 400 | `--muted2` |
| tags/labels | `--sans` | `12-13px` | 600 | contextuel |

---

## 6. Cards (`.article-card`, `.mockup`, cards génériques)

```css
.article-card, .card {
  background: #ffffff;
  border-radius: var(--radius2);   /* 28px */
  box-shadow: var(--shadowSoft);   /* 0 14px 34px rgba(6,23,45,.11) */
  padding: clamp(24px, 3vw, 40px);
  border: 1px solid var(--borderSoft);
}

.mockup {
  background: transparent;         /* PAS de background blanc */
  border-radius: 26px;
  border: 1px solid rgba(0,0,0,0.08);
  box-shadow: rgba(0,0,0,.12) 0px 18px 60px;
  overflow: hidden;
}
```

---

## 7. Footer

```css
footer {
  color: var(--muted2);       /* rgba(6,23,45,.58) */
  font-size: 13px;
  background: transparent;
  border-top: 1px solid var(--border);
}
```

Contenu : `© 2026 Boussole — micronutriment.fr` + liens Confidentialité · Écosystème · Rejoindre

---

## 8. Pages et leur spécificité

| Page | Particularité CSS |
|------|-------------------|
| `index.html` | Hero avec `.hero-visual .mockup` — background transparent obligatoire |
| `articles/index.html` | Listing simple, fond dégradé standard |
| `articles/*/index.html` | `.article-card` wrappant le contenu, fond dégradé |
| `ecosysteme.html` | Fond dégradé standard |
| `rejoindre.html` | Pas de back-nav secondaire — supprimée |

---

## 9. Règles d'intervention pour Claude Code

1. **Toujours lire ce fichier avant** toute modification CSS/HTML sur ce repo.
2. **Ne jamais improviser** une valeur de couleur, taille ou ombre — utiliser les variables ci-dessus.
3. **Toujours appliquer les règles de boutons de façon globale** (pas scoped à `.hero`).
4. **Si un composant est absent** de ce design system → demander à Rémy avant de créer un nouveau style.
5. **Après chaque correction CSS** : vérifier que le style est cohérent sur TOUTES les pages concernées, pas seulement la page modifiée.
6. **Ne pas ajouter `!important`** sauf pour `.site-header background` (exception documentée).

---

*Dernière mise à jour : 07/03/2026 — extrait depuis les valeurs CSS calculées en production.*
