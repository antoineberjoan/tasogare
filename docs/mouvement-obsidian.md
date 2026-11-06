# Mouvement 1.1 dans Obsidian

Ce document explique comment Tasogare applique la [spécification Mouvement 1.1](mouvement.md) dans Obsidian. Le code fait foi : il se trouve dans `theme.css`, section « Mouvement » (couche 1).

## L'idée : presque rien ne bouge

Obsidian est un outil qu'on ouvre des centaines de fois par jour. Selon le tableau de fréquence de la spécification, la plupart de ses gestes ne doivent pas s'animer : changer d'onglet, parcourir la sidebar, survoler une ligne. Tasogare suit cette règle : il n'ajoute aucune transition aux survols de la sidebar, des onglets et des propriétés.

## Ce qui s'anime

| Élément | Propriété | Durée | Courbe | Pourquoi |
| --- | --- | --- | --- | --- |
| Sélecteur de coffre, au survol | `background-color` | `--tasogare-duree-rapide` (150 ms) | `--tasogare-courbe-survol` (`ease`) | Signaler qu'il s'ouvre ; geste rare |

## Les variables d'animation d'Obsidian

Obsidian expose peu de variables d'animation, et en utilise peu. Tasogare les relie à l'échelle.

| Variable d'Obsidian | Valeur d'Obsidian | Valeur Tasogare | Spécification | Où Obsidian l'utilise |
| --- | --- | --- | --- | --- |
| `--anim-duration-fast` | 140 ms | 150 ms | `--duration-fast` | Icônes cliquables, lien sous une propriété |
| `--anim-motion-swing` | `cubic-bezier(0, .55, .45, 1)` | `cubic-bezier(0.23, 1, 0.32, 1)` | `--ease-out` | Entrée des menus, des suggestions et des aperçus au survol ; glisser-réordonner ; panneau du lecteur PDF |

Tasogare ne relie pas `--anim-duration-moderate` ni `--anim-motion-smooth` : Obsidian 1.15 ne les lit nulle part.

Tasogare ne touche pas à `--anim-motion-jumpy` (une courbe avec rebond) ni à `--anim-motion-spring` : Obsidian ne les utilise pas dans le contenu que le thème habille.

## Réduire les animations

Tasogare n'ajoute que des transitions de couleur ; il change seulement la courbe des animations d'entrée d'Obsidian (menus, suggestions), qui deviennent des décélérations, comme le demande la spécification. Avec la préférence « réduire les animations », c'est Obsidian qui décide de ses propres animations ; le thème n'ajoute pas de règle `prefers-reduced-motion`.

## Source

Les règles et les valeurs viennent d'Emil Kowalski, skills `animate` et `emil-design-eng`, licence MIT, © 2026 Emil Kowalski, <https://github.com/emilkowalski/skill>.
