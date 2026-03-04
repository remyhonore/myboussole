# Audit — site Boussole (priorité index.html)

Date : 04/03/2026  
Périmètre : index.html (prioritaire), ecosysteme.html, rejoindre.html, /assets

## P0 — Bloquants / à corriger en premier

1) **Canonical / OG URL incohérents (www vs non-www + doublons)**
- Symptôme : plusieurs `<link rel="canonical">`, plusieurs `og:url`, valeurs différentes selon les pages.
- Cause probable : copier-coller de head + migration de domaine.
- Fix recommandé :
  - Garder **1 canonical** par page (URL exacte de la page).
  - Garder **1 og:url** par page, aligné sur le canonical.
  - Aligner aussi `og:image` / `twitter:image` sur le même domaine.

2) **Liens “contact” cassés (Cloudflare email-protection)**
- Symptôme : bouton “Prendre contact / Candidater …” pointe vers `/cdn-cgi/l/email-protection…` (ne fonctionne pas hors Cloudflare).
- Cause probable : export d’un site derrière Cloudflare.
- Fix recommandé :
  - Remplacer par `mailto:` (même adresse, sujet pré-rempli).
  - Garder une formulation sobre (pas d’injonction).

3) **Animation “reveal” : risque de contenu invisible**
- Symptôme : si `IntersectionObserver` est indisponible (ou JS bloqué), éléments `.reveal` peuvent rester invisibles (opacity 0).
- Cause probable : reveal CSS dépendant d’un JS sans fallback.
- Fix recommandé :
  - Fallback : si pas d’IO ou si `prefers-reduced-motion`, afficher immédiatement (ajout `.in` ou override CSS).

## P1 — Impact fort (UX / accessibilité / clarté)

4) **Menu mobile : état ARIA incomplet**
- Symptôme : le bouton conserve le label “Ouvrir le menu” même quand le menu est ouvert ; focus non guidé.
- Cause probable : gestion minimale du toggle.
- Fix recommandé :
  - Toggle `aria-label` (Ouvrir/Fermer).
  - Au clic : focus sur le 1er lien ; à la fermeture : restaurer le focus.
  - Fermer aussi si le focus sort du menu (clavier).

5) **Skip link : ancre non focusable**
- Symptôme : “Aller au contenu” scrolle mais ne place pas le focus sur la zone principale (selon navigateur/lecteur d’écran).
- Cause probable : `main` non focusable.
- Fix recommandé :
  - Ajouter `tabindex="-1"` à `<main id="contenu">`.

6) **Cohérence microcopy CTA**
- Symptôme : “Essayer” (topbar/menu) vs “Essayer la bêta” (hero) → friction cognitive.
- Cause probable : variantes de libellés.
- Fix recommandé :
  - Unifier le libellé du CTA primaire partout.

7) **Jargon résiduel (“privacy-first”)**
- Symptôme : terme anglais dans une page grand public.
- Cause probable : vocabulaire produit.
- Fix recommandé :
  - Remplacer par “confidentialité d’abord” (même sens, plus clair).

## P2 — Optimisations (qualité / partage / propreté)

8) **Meta “color-scheme” absent**
- Symptôme : certains UA peuvent optimiser différemment le rendu si non déclaré.
- Cause probable : omission.
- Fix recommandé :
  - Ajouter `<meta name="color-scheme" content="light">`.

9) **OG/Twitter incomplets sur pages secondaires**
- Symptôme : partage social moins propre sur ecosysteme/rejoindre.
- Cause probable : head minimal.
- Fix recommandé :
  - Ajouter OG/Twitter basiques (title/description/image) cohérents.

10) **Fichiers parasites**
- Symptôme : `.DS_Store` dans /assets.
- Cause probable : export macOS.
- Fix recommandé :
  - Supprimer du ZIP déployé (propreté + micro-gain perf).

