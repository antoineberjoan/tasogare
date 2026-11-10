# Couleur 1.0 dans Obsidian

Ce document explique comment Tasogare applique la [spécification Couleur 1.0](couleur.md) dans Obsidian. Le code fait foi : il se trouve dans `theme.css`, sections « Palette » (couche 1) et « Couleurs » (couche 2).

## Les trois noms d'une même couleur

Une couleur passe par trois noms. La spécification parle en anglais, pour servir d'autres projets. Tasogare nomme ses emplacements en français. Obsidian lit ses propres variables.

| Spécification | Emplacement Tasogare | Variables d'Obsidian |
| --- | --- | --- |
| `frame` | `--tasogare-cadre` | `--background-secondary`, `--background-secondary-alt` |
| `surface` | `--tasogare-carte` | `--background-primary`, `--background-primary-alt` |
| `sunken` | `--tasogare-creux` | `--code-background`, `--table-header-background` |
| `veil` + parts | `--tasogare-voile` | `--background-modifier-hover`, `--background-modifier-border`, `--background-modifier-border-hover` |
| `shadow` | `--tasogare-ombre` | `--bases-kanban-card-shadow`, par le rôle `--tasogare-ombre-posee` |
| `rule-table` | `--tasogare-filet-tableau` | `--table-border-color` |
| `rule-strong` | `--tasogare-filet-fort` | `--hr-color`, `--blockquote-border-color` |
| `ink` | `--tasogare-encre` | `--text-normal` |
| `ink-muted` | `--tasogare-encre-moyenne` | `--text-muted` |
| `ink-faint` | `--tasogare-encre-pale` | `--text-faint` |
| `accent` | `--tasogare-accent` | `--text-accent`, et `--accent-h/s/l` pour les teintes calculées par Obsidian |
| `accent-hover` | `--tasogare-accent-survol` | `--text-accent-hover` |
| `action` | `--tasogare-action` | `--interactive-accent` |
| `action-hover` | `--tasogare-action-survol` | `--interactive-accent-hover` |
| `on-action` | `--tasogare-sur-action` | `--text-on-accent` |
| `check` | `--tasogare-coche` | `--checkbox-color` |
| `on-check` | `--tasogare-coche-marque` | `--checkbox-marker-color` |
| `highlight` | `--tasogare-surlignage` | `--text-highlight-bg` |
| `selection` | `--tasogare-selection` | `--text-selection` |
| `search` | `--tasogare-recherche` | `--search-result-background` |
| `red` à `pink` | `--tasogare-rouge` à `--tasogare-rose` | `--color-red` à `--color-pink` (callouts, code, graphe) |

Les parts de transparence s'appellent `--tasogare-part-*` dans le thème.

Chaque couleur nommée d'une palette (Cabine rouge, Matcha vif, Bleu cobalt…) s'écrit une seule fois, dans le bloc « Couleurs sources des palettes » de `theme.css`. Les emplacements la lisent par son nom (`var(--tasogare-matcha-vif)`) ; seules les nuances dérivées s'écrivent à leur emplacement. Les tableaux ci-dessous montrent les valeurs résolues.

## Choisir une palette

Le plugin communautaire **Style Settings** ajoute une liste « Palette » dans Réglages → Style Settings → Tasogare. Il pose une classe sur la page : `tasogare-graphite`, `tasogare-crepuscule`, `tasogare-gres`, `tasogare-the`, `tasogare-lac`, `tasogare-porte` ou `tasogare-galet`. Sans le plugin, aucune classe n'est posée et Graphite s'applique : ses blocs n'ont pas de classe, et les autres palettes en héritent.

## Vérifier les contrastes

```bash
python3 outils/palettes.py
```

L'outil lit les palettes dans `theme.css`, applique les seuils de la spécification et s'arrête en erreur si un seuil échoue. Pour changer l'accent d'une palette, change sa couleur source dans `theme.css`, puis lance `python3 outils/palettes.py --accord` : les trois nombres `--tasogare-accent-h/s/l`, que le CSS ne sait pas calculer, se réécrivent depuis l'accent. Les tableaux ci-dessous viennent de la même commande, avec `--markdown`.

## Les palettes

<!-- Généré par `python3 outils/palettes.py --markdown`. Ne pas modifier à la main. -->

### Graphite

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#f2f2f7` | `#1c1c1e` |
| `carte` | `#ffffff` | `#2c2c2e` |
| `creux` | `#f2f2f7` | `#242426` |
| `encre` | `#1c1c1e` | `#f5f5f7` |
| `encre-moyenne` | `#636366` | `#aeaeb2` |
| `encre-pale` | `#8e8e93` | `#8e8e93` |
| `accent` | `#0066cc` | `#4da3ff` |
| `accent-survol` | `#0050a8` | `#7bbcff` |
| `action` | `#0071e3` | `#0071e3` |
| `action-survol` | `#0062c4` | `#0062c4` |
| `sur-action` | `#ffffff` | `#ffffff` |
| `coche` | `#0071e3` | `#4da3ff` |
| `coche-marque` | `#ffffff` | `#1c1c1e` |
| `surlignage` | `#ffd60a` | `#ffd60a` |
| `selection` | `#4da3ff` | `#0071e3` |
| `recherche` | `#ffd60a` | `#ffd60a` |
| `rouge` | `#d70015` | `#ff6961` |
| `orange` | `#c93400` | `#ff9f0a` |
| `jaune` | `#946c00` | `#ffd60a` |
| `vert` | `#248a3d` | `#32d74b` |
| `cyan` | `#0a7ea4` | `#64d2ff` |
| `bleu` | `#0066cc` | `#4da3ff` |
| `violet` | `#8944ab` | `#bf5af2` |
| `rose` | `#d30f45` | `#ff6482` |

### Crépuscule alpin

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#edecf5` | `#1f2a3a` |
| `carte` | `#ffffff` | `#293546` |
| `creux` | `#edecf5` | `#232e3e` |
| `encre` | `#4a4e5c` | `#e6e4ef` |
| `encre-moyenne` | `#666976` | `#b9b3d6` |
| `encre-pale` | `#8b8e99` | `#9d99b8` |
| `accent` | `#9e2b25` | `#e8a3b4` |
| `accent-survol` | `#7e211d` | `#f2c0cd` |
| `action` | `#9e2b25` | `#6e6ba8` |
| `action-survol` | `#7e211d` | `#5e5b96` |
| `sur-action` | `#ffffff` | `#ffffff` |
| `coche` | `#6e6ba8` | `#e8a3b4` |
| `coche-marque` | `#ffffff` | `#1f2a3a` |
| `surlignage` | `#f4c66a` | `#f4c66a` |
| `selection` | `#b9b3d6` | `#6e6ba8` |
| `recherche` | `#e8a3b4` | `#e8a3b4` |
| `rouge` | `#9e2b25` | `#e06e64` |
| `orange` | `#c46e28` | `#eca064` |
| `jaune` | `#b0801e` | `#f4c66a` |
| `vert` | `#4f7a5a` | `#a8cfa0` |
| `cyan` | `#3d7a80` | `#8cc8c8` |
| `bleu` | `#4a6096` | `#8ca0dc` |
| `violet` | `#6e6ba8` | `#b9b3d6` |
| `rose` | `#be627c` | `#e8a3b4` |

### Grès rosé

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#e6e2da` | `#2f2925` |
| `carte` | `#faf8f4` | `#3f3832` |
| `creux` | `#e6e2da` | `#383029` |
| `encre` | `#3f3832` | `#e6e2da` |
| `encre-moyenne` | `#675e56` | `#b4aea2` |
| `encre-pale` | `#958b81` | `#9a9085` |
| `accent` | `#7a5443` | `#d3a790` |
| `accent-survol` | `#5f3f31` | `#e2c0ae` |
| `action` | `#7a5443` | `#b98a72` |
| `action-survol` | `#5f3f31` | `#cfa28b` |
| `sur-action` | `#ffffff` | `#2a2420` |
| `coche` | `#8c7e5e` | `#b98a72` |
| `coche-marque` | `#ffffff` | `#2a2420` |
| `surlignage` | `#b98a72` | `#b98a72` |
| `selection` | `#b98a72` | `#8c7e5e` |
| `recherche` | `#8c7e5e` | `#b98a72` |
| `rouge` | `#a2483a` | `#e0907e` |
| `orange` | `#a8622e` | `#e3a774` |
| `jaune` | `#8f7533` | `#d9c08a` |
| `vert` | `#8c7e5e` | `#b7ad86` |
| `cyan` | `#4a7a76` | `#8fc0b8` |
| `bleu` | `#4f6a8a` | `#9ab2d0` |
| `violet` | `#7a6290` | `#c0aad6` |
| `rose` | `#a85d6c` | `#e0a3b2` |

### Thé vert

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#e9e6dc` | `#2a2622` |
| `carte` | `#fbfaf6` | `#35302b` |
| `creux` | `#e9e6dc` | `#2f2b27` |
| `encre` | `#4a4f55` | `#e9e6dc` |
| `encre-moyenne` | `#69665f` | `#bdb7aa` |
| `encre-pale` | `#8f8b82` | `#a29c90` |
| `accent` | `#636e27` | `#8db33a` |
| `accent-survol` | `#4c551d` | `#a9c962` |
| `action` | `#6e7a2c` | `#8db33a` |
| `action-survol` | `#4c551d` | `#a9c962` |
| `sur-action` | `#ffffff` | `#2a2622` |
| `coche` | `#5b3a24` | `#8db33a` |
| `coche-marque` | `#ffffff` | `#2a2622` |
| `surlignage` | `#c2a25a` | `#c2a25a` |
| `selection` | `#8db33a` | `#8db33a` |
| `recherche` | `#c2a25a` | `#c2a25a` |
| `rouge` | `#a5402f` | `#e07a62` |
| `orange` | `#a85f26` | `#e0a060` |
| `jaune` | `#8f7330` | `#c2a25a` |
| `vert` | `#5f6c22` | `#8db33a` |
| `cyan` | `#3c766c` | `#7fc0b2` |
| `bleu` | `#46658a` | `#8fadd0` |
| `violet` | `#6c5a8c` | `#b3a3d6` |
| `rose` | `#a2506a` | `#e09ab0` |

### Lac profond

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#eeeae2` | `#132a2b` |
| `carte` | `#fbfaf7` | `#1a3536` |
| `creux` | `#eeeae2` | `#163031` |
| `encre` | `#2d3a3b` | `#eeeae2` |
| `encre-moyenne` | `#655f55` | `#a6b8b3` |
| `encre-pale` | `#7e9590` | `#8fa5a0` |
| `accent` | `#2f7672` | `#7cc4bd` |
| `accent-survol` | `#245c59` | `#a3d8d2` |
| `action` | `#1f5a5c` | `#2f7672` |
| `action-survol` | `#174547` | `#286662` |
| `sur-action` | `#ffffff` | `#ffffff` |
| `coche` | `#3e8a86` | `#3e8a86` |
| `coche-marque` | `#ffffff` | `#ffffff` |
| `surlignage` | `#c8ae7e` | `#c8ae7e` |
| `selection` | `#3e8a86` | `#3e8a86` |
| `recherche` | `#d2452b` | `#d2452b` |
| `rouge` | `#b83a22` | `#ef7a60` |
| `orange` | `#b0601f` | `#e8a05e` |
| `jaune` | `#8c7238` | `#c8ae7e` |
| `vert` | `#4c7a52` | `#9cc79a` |
| `cyan` | `#2f7672` | `#7cc4bd` |
| `bleu` | `#2f5f8a` | `#8db4dc` |
| `violet` | `#675d8e` | `#b4aadb` |
| `rose` | `#a84d6c` | `#e99ab4` |

### Porte bleue

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#f6eed6` | `#13213f` |
| `carte` | `#fffcf3` | `#1b2b50` |
| `creux` | `#f6eed6` | `#172647` |
| `encre` | `#13213f` | `#f0e3be` |
| `encre-moyenne` | `#565e75` | `#c3c0b4` |
| `encre-pale` | `#8a8f9f` | `#9aa0b5` |
| `accent` | `#2347a8` | `#8ca6ec` |
| `accent-survol` | `#1a3683` | `#b0c3f2` |
| `action` | `#2347a8` | `#e6be3a` |
| `action-survol` | `#1a3683` | `#efd06e` |
| `sur-action` | `#ffffff` | `#13213f` |
| `coche` | `#c2287a` | `#e6be3a` |
| `coche-marque` | `#ffffff` | `#13213f` |
| `surlignage` | `#e6be3a` | `#e6be3a` |
| `selection` | `#2347a8` | `#2347a8` |
| `recherche` | `#c2287a` | `#c2287a` |
| `rouge` | `#b0302a` | `#ec7a6e` |
| `orange` | `#c0663e` | `#e39a6e` |
| `jaune` | `#957514` | `#e6be3a` |
| `vert` | `#5e8b4a` | `#9cc488` |
| `cyan` | `#2a7f86` | `#7cc8cc` |
| `bleu` | `#2347a8` | `#8ca6ec` |
| `violet` | `#6a4aa8` | `#b7a0ec` |
| `rose` | `#c2287a` | `#ec86b8` |

### Galet noir

| Emplacement | Clair | Sombre |
| --- | --- | --- |
| `cadre` | `#eeebe5` | `#1f1e1c` |
| `carte` | `#fbfaf8` | `#2b2a27` |
| `creux` | `#eeebe5` | `#252422` |
| `encre` | `#2b2a27` | `#eeebe5` |
| `encre-moyenne` | `#5f5b53` | `#c9c4ba` |
| `encre-pale` | `#8e8a80` | `#9b978d` |
| `accent` | `#5f5c43` | `#b3a68f` |
| `accent-survol` | `#45432f` | `#c9bfa9` |
| `action` | `#2b2a27` | `#c9c4ba` |
| `action-survol` | `#5f5b53` | `#eeebe5` |
| `sur-action` | `#ffffff` | `#2b2a27` |
| `coche` | `#2b2a27` | `#b3a68f` |
| `coche-marque` | `#ffffff` | `#2b2a27` |
| `surlignage` | `#b3a68f` | `#b3a68f` |
| `selection` | `#8e8a80` | `#8e8a80` |
| `recherche` | `#7d7a5e` | `#b3a68f` |
| `rouge` | `#9c4a3e` | `#d79a8a` |
| `orange` | `#9a6233` | `#d8ad80` |
| `jaune` | `#86733a` | `#d6c48f` |
| `vert` | `#7d7a5e` | `#aeb08a` |
| `cyan` | `#4f7470` | `#9cc0b8` |
| `bleu` | `#50667f` | `#a5b6cb` |
| `violet` | `#6d6082` | `#bdb0cf` |
| `rose` | `#96596a` | `#d6a7b3` |

