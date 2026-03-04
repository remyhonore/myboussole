# Plan — 10 changements max (ordonnés par impact)

1) Unifier canonical + og:url (1 seule occurrence) sur **toutes** les pages, domaine www + chemin exact.  
2) Corriger `og:image` / `twitter:image` (domaine cohérent).  
3) Remplacer tous les liens Cloudflare email-protection par des `mailto:` fonctionnels.  
4) Sécuriser le reveal : fallback sans `IntersectionObserver` + respect `prefers-reduced-motion`.  
5) Menu mobile : `aria-label` toggle + focus sur 1er lien + restauration du focus + fermeture si focus sort.  
6) Skip link : rendre `<main id="contenu">` focusable (`tabindex="-1"`).  
7) Harmoniser le libellé du CTA primaire (“Essayer la bêta”).  
8) Remplacer “privacy-first” par “confidentialité d’abord”.  
9) Ajouter `meta color-scheme` (light).  
10) Nettoyer le ZIP : retirer `.DS_Store` et dossiers parasites.

