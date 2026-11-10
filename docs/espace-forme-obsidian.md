# Espace et forme 1.1 dans Obsidian

Ce document explique comment Tasogare applique la [spécification Espace et forme 1.1](espace-forme.md) dans Obsidian. Le code fait foi : il se trouve dans `theme.css`, section « Espace et forme » (couche 1), puis dans les rôles et les règles.

## Espacements

Tasogare n'utilise que six marches de l'échelle : 2, 4, 6, 8, 10 et 14 px.

| Rôle Tasogare | Valeur | Spécification | Où |
| --- | --- | --- | --- |
| `--tasogare-inset` | 10 px | `--space-10` | Autour de la carte de note, des onglets, du sélecteur de coffre |
| `--tasogare-ecart-icone` | 10 px | `--space-10` | Entre l'icône et le nom d'une note dans la sidebar |
| `--tasogare-ecart-icone-propriete` | 8 px | `--space-8` | Entre l'icône et le nom d'une propriété |
| `--tasogare-ecart-proprietes` | 2 px | `--space-2` | Entre deux propriétés (`--metadata-gap`) |
| `--tasogare-pas-onglet` | 4 × 10 px | `--space-4`, `--space-10` | Marge intérieure d'un onglet |
| `--tasogare-pas-ligne-nav` | 8 px | `--space-8` | Marge verticale d'une ligne de la sidebar (`--nav-item-padding`, notes et dossiers) et de la fenêtre de réglages |
| `--tasogare-pas-proprietes` | 10 × 14 × 8 px | `--space-10`, `--space-14`, `--space-8` | Marge du bloc de propriétés |
| `--tasogare-pas-propriete` | 4 px | `--space-4` | Marge latérale d'une propriété |
| `--tasogare-pas-selecteur-coffre` | 6 × 10 px | `--space-6`, `--space-10` | Sélecteur de coffre |

## Rythme du texte

| Rôle Tasogare | Valeur | Variable d'Obsidian |
| --- | --- | --- |
| `--tasogare-espace-paragraphe` | 0,9rem | `--p-spacing` |
| `--tasogare-espace-avant-titre` | 3rem | `--heading-spacing` |
| `--tasogare-espace-sous-h2` | 1rem | règle sur `h2` |
| `--tasogare-espace-sous-h3` | 0,75rem | règle sur `h3` |
| `--tasogare-retrait-citation` | 1,5rem | règle sur `.markdown-rendered blockquote` (lecture) |

## Rayons

| Rôle Tasogare | Valeur | Spécification | Variables d'Obsidian et règles |
| --- | ---: | --- | --- |
| `--tasogare-rayon-marque` | 4 px | `--radius-mark` | `--tag-radius`, pastilles, surlignage |
| `--tasogare-rayon-champ` | 6 px | `--radius-control` | `--input-radius`, `--clickable-icon-radius`, `--tooltip-radius`, `--metadata-property-radius` |
| `--tasogare-rayon-bloc` | 10 px | `--radius-block` | `--callout-radius`, `--image-radius`, `--menu-radius`, onglets, lignes de la sidebar, cartes de Bases |
| `--tasogare-rayon-fenetre` | 14 px | `--radius-window` | `--modal-radius`, règle sur `.prompt` |
| `--tasogare-rayon-carte` | 16 px | `--radius-card` | Carte de note, bloc de propriétés, fenêtre de réglages |

Sur macOS, Obsidian redéfinit `--input-radius`, `--clickable-icon-radius` et `--modal-radius` sur `.mod-macos`. Tasogare les reprend sur ordinateur (`body:not(.is-mobile)`) ; le mobile garde ceux d'Obsidian.

Rayon concentrique : la carte intérieure de la fenêtre de réglages prend `16 − 10 = 6 px` quand la fenêtre est intégrée à Obsidian. Dans sa propre fenêtre (Obsidian 1.15), aucune forme ne l'entoure : elle prend le rayon de la carte de note, 16 px.

## Filets et élévation

| Spécification | Dans Tasogare |
| --- | --- |
| `--border-width` | `--tasogare-filet` (1 px) : tags, callouts, fenêtres, menus |
| `--focus-width` | L'anneau de focus d'Obsidian, inchangé |
| Niveau 0, plat | Cadre, carte de note, sidebar, galerie de Bases |
| Niveau 1, posé | `--tasogare-ombre-posee` : cartes du kanban de Bases |
| Niveau 2, flottant | Les ombres d'Obsidian (`--shadow-s`), inchangées |
| Niveau 3, fenêtre | Les ombres d'Obsidian (`--shadow-l`), inchangées |

Les niveaux 2 et 3 restent ceux d'Obsidian pour l'instant : leurs ombres sont noires et non teintées par la palette. Une version suivante pourra les teinter avec `--tasogare-ombre`, après un essai en clair et en sombre.

Tasogare suit le principe « pas de filet dur » : aucun séparateur entre la sidebar, les onglets et la note. Le cadre et l'inset de 10 px séparent les zones.

## Sur téléphone

Sur téléphone et tablette, Tasogare garde la mise en page d'Obsidian :
- la carte de note, l'inset, la barre d'onglets, la fenêtre de réglages, l'invite de commande et le sélecteur de coffre ne changent que sous `body:not(.is-mobile)` ;
- les lignes de la sidebar et le bloc de propriétés passent par les variables d'Obsidian (`--nav-item-*`, `--metadata-*`), qu'Obsidian redéfinit lui-même sur mobile ;
- la croix des pastilles et le lien vers la note du jour restent visibles au toucher : ils ne se cachent jusqu'au survol que sur ordinateur.

Restent sur mobile : les couleurs des palettes, la typographie (titre de note à 26 px sur téléphone), le filet des callouts et le rayon des transclusions. Obsidian gère lui-même les zones sûres, la hauteur de l'écran et le défilement.

## Icônes

| Rôle Tasogare | Valeur | Spécification |
| --- | ---: | --- |
| `--tasogare-taille-icone` | 16 px | `--icon-size` |
| `--tasogare-trait-icone` | 1,75 px | `--icon-stroke` |

## Ce qui change par rapport à Tasogare 1.6

- La marge verticale d'un onglet passe de 3 à 4 px, et celle d'une ligne de la sidebar de 7 à 8 px : les deux valeurs rejoignent l'échelle. Chaque ligne gagne 2 px de hauteur.
- La carte intérieure de la fenêtre de réglages passe d'un rayon de 10 à 6 px, pour être concentrique.
- Le sélecteur de coffre lit un espacement (`--space-6`) au lieu d'un rayon pour sa marge.
