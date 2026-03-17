---
name: boussole-visual-identity
description: Charte visuelle officielle de Boussole / myboussole.fr. Applique systématiquement la palette, la typographie, les formats et la philosophie "Meridian Quiet" à tous les assets visuels. Déclenche dès que l'utilisateur mentionne "design", "logo", "visuel", "couverture", "identité", "charte", "asset", "illustration", "hero", "bannière", "post FB", "couleur", "police", "font", "PNG", "PDF", "canva", ou demande la création de tout contenu visuel pour Boussole, myboussole.fr, ou les réseaux sociaux. Utiliser également pour tous les artifacts HTML/CSS qui doivent respecter l'identité de la marque. Ne jamais créer de visuels Boussole sans ce skill.
---

# Boussole Visual Identity — "Meridian Quiet"

## Philosophie de la marque

**Mouvement : Meridian Quiet**

Boussole s'adresse à des personnes qui naviguent dans l'incertain — fatigue chronique, Covid long, fibromyalgie. L'identité visuelle traduit cela : orientation calme, précision scientifique, chaleur humaine. Pas une marque "startup santé" générique. Pas de dégradés violets, pas d'icônes plates colorées. Un langage visuel qui dit : *quelqu'un a réfléchi à ça sérieusement*.

Le symbole central est la **rose des vents** — navigation, orientation, corps dans le temps. Jamais décoratif, toujours porteur de sens.

---

## Palette officielle

| Token | Hex | Usage |
|---|---|---|
| `--color-primary` | `#2d6a4f` | Vert forêt — couleur primaire unique app + vitrine (ADR-2026-027) |
| `--color-navy` | `#06172D` | Navy — fond sombre, texte principal sur fond clair |
| `--color-cream` | `#F8F5EE` | Crème — fond clair principal |
| `--color-green-mid` | `#3E8260` | Vert intermédiaire — accents secondaires |
| `--color-green-light` | `#B4D2BE` | Vert clair — textes sur fond sombre, détails fins |
| `--color-white` | `#FFFFFF` | Blanc pur — uniquement pour contraste maximum |

**Règle d'or palette :**
- Fond primaire app = navy `#06172D`
- Fond primaire vitrine = crème `#F8F5EE`
- Jamais de gradient décoratif
- Jamais de couleur hors palette sans validation

---

## Typographie

| Rôle | Police | Style | Usage |
|---|---|---|---|
| Wordmark / Display | `Instrument Serif` | Regular / Italic | Logo, titres héros, accroches |
| Labels / UI | `Jura` | Light / Medium | Sous-titres, annotations, taglines |
| Corps texte | `Instrument Sans` | Regular / Bold | Texte courant, UI app |
| Mono technique | `DM Mono` | Regular | Données chiffrées, codes |

**Règles typo :**
- Wordmark "boussole" : toujours en minuscules, Instrument Serif
- Jamais Inter, Roboto, Arial comme choix primaire
- Hiérarchie : Display grande + labels petits whisper — éviter le milieu mou

---

## Formats des assets

| Asset | Dimensions | Fond | Notes |
|---|---|---|---|
| Logo principal | 1200×1200 px | Crème `#F8F5EE` | Version claire |
| Logo alternatif | 800×800 px | Navy `#06172D` | Version sombre |
| Favicon / icône app | 512×512 px | Vert `#2d6a4f` | Rose des vents seule |
| Couverture Facebook | 1640×624 px | Navy | Compass + wordmark + tagline |
| Photo profil Facebook | 800×800 px | Navy | Compass + "boussole" |
| Bannière LinkedIn | 1584×396 px | Navy | Compass + Dr Rémy Honoré + rôle |
| Hero article | 1200×630 px | Variable | OG image + article header |
| Post carré FB | 1080×1080 px | Variable | Contenu éducatif |
| Story / Reel | 1080×1920 px | Navy | Format vertical |

---

## Symbole — Rose des vents

Le symbole Boussole est une **rose des vents géométrique à 4 branches cardinales** :

- **N** (nord) : branche dominante, plus longue, couleur crème/blanc — direction principale
- **S / E / O** : branches secondaires, plus courtes, vert `#2d6a4f` ou `#3E8260`
- Branches diagonales optionnelles : fines, vertes, pour les versions détaillées
- Cercles concentrices : 2-3 anneaux fins, espacés, verts
- Tirets graduués sur le cercle extérieur (comme un cadran)
- Point central : disque vert `#2d6a4f` + dot crème au centre

**Ce qu'il ne faut PAS faire :**
- Boussole émoji seul 🧭 comme logo (trop générique)
- Compass plat style icône flatdesign
- Rose des vents trop ornementale / baroque

---

## Textures de fond

Deux textures caractéristiques de l'identité Meridian Quiet :

**1. Isocontours** : lignes horizontales ondulées légères, comme une carte topographique. Opacité 5-15%. Couleur `#2d6a4f`.

**2. Grille de points** : grid régulière de petits dots. Opacité 8-20%. Couleur `#2d6a4f`.

Ces textures s'utilisent toujours en fond subtil — jamais en premier plan.

---

## Taglines officielles

- **Principale** : "Suivre pour comprendre. Comprendre pour aller mieux."
- **Courte** : "Votre boussole santé"
- **Technique** : "Privacy-first · Local · Gratuit"
- **URL** : `myboussole.fr` / `app.myboussole.fr`

---

## Règles d'usage

### ✅ À faire
- Rose des vents comme ancre visuelle centrale
- Espace négatif généreux — le silence fait partie du design
- Typographie légère (Jura Light) pour les sous-titres
- Tons navy/crème comme combo de base

### ❌ À éviter
- Gradients dégradés violet/rose/orange (cliché santé)
- Icônes stock médicales (stéthoscope, croix rouge, pilules)
- Photos de personnes souriantes en blanc
- Polices sans personnalité (Inter, Roboto, Arial)
- Plus de 3 couleurs par composition
- Texte centré partout — varier les alignements

---

## Workflow création visuel

### Avec le skill `canvas-design` (PNG/PDF)
1. Charger ce skill (boussole-visual-identity)
2. Charger le skill `canvas-design`
3. Briefer avec : format cible + palette ci-dessus + textures isocontours + typographie Instrument Serif/Jura

### Avec Python/PIL (assets programmatiques)
- Fonts disponibles dans `/mnt/skills/examples/canvas-design/canvas-fonts/`
- Clés : `InstrumentSerif-Regular.ttf`, `Jura-Light.ttf`, `InstrumentSans-Regular.ttf`, `DMMono-Regular.ttf`
- Résolution : 300 dpi pour print, 96 dpi pour web

### Avec Canva MCP
- Pas de brand kit configuré actuellement
- Briefer explicitement avec hex codes et typographie
- Quota limité — prioriser logo + couverture FB

### Pour artifacts HTML/CSS
```css
:root {
  --color-primary: #2d6a4f;
  --color-navy: #06172D;
  --color-cream: #F8F5EE;
  --color-green-mid: #3E8260;
  --color-green-light: #B4D2BE;
  --font-display: 'Instrument Serif', Georgia, serif;
  --font-ui: 'Jura', system-ui, sans-serif;
  --font-body: 'Instrument Sans', system-ui, sans-serif;
}
```

---

## Nomenclature stricte (rappel)
- **Boussole** = version freemium actuelle (app.myboussole.fr)
- **Boussole+** = version premium future
- **myBoussole** = marque globale / vitrine
- **Dr Rémy Honoré** = identité personnelle (LinkedIn, profil perso)

Ne jamais confondre dans les communications visuelles.
