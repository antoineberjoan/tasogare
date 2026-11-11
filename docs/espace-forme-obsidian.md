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
| `--tasogare-rayon-bloc` | 10 px | `--radius-block` | `--callout-radius`, `--image-radius`, `--menu-radius`, onglets, lignes de la sidebar, cartes de Bases, tableaux Markdown et de Bases |
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
| Niveau 1, posé | `--tasogare-ombre-posee` : cartes du kanban de Bases, tableaux Markdown et de Bases |
| Niveau 2, flottant | Les ombres d'Obsidian (`--shadow-s`), inchangées |
| Niveau 3, fenêtre | Les ombres d'Obsidian (`--shadow-l`), inchangées |

Les niveaux 2 et 3 restent ceux d'Obsidian pour l'instant : leurs ombres sont noires et non teintées par la palette. Une version suivante pourra les teinter avec `--tasogare-ombre`, après un essai en clair et en sombre.

Tasogare suit le principe « pas de filet dur » : aucun séparateur entre la sidebar, les onglets et la note. Le cadre et l'inset de 10 px séparent les zones.

## Tableaux

Un tableau forme une surface groupée dans la note : fond de la carte, contour `--background-modifier-border`, rayon de bloc et ombre posée. Ce traitement est commun aux tableaux Markdown en lecture et en aperçu actif, et au conteneur des tableaux de Bases. Les sept palettes fournissent les couleurs, en clair comme en sombre.

Les cellules Markdown gardent des séparations horizontales, sans quadrillage vertical. Leur marge intérieure lit `--tasogare-espace-8` et `--tasogare-espace-14` ; `--tasogare-rayon-cellule-tableau` calcule une seule fois le rayon du bloc moins l’épaisseur du contour, au niveau du tableau pour suivre les réglages locaux. Les chiffres utilisent des figures tabulaires et l’alignement reste celui écrit dans la note. Les lignes de Bases conservent leur hauteur et leur fonctionnement natifs.

Les filets lisent les variables natives `--table-border-width`, `--table-header-border-width` et `--table-row-last-border-width`. Les sélecteurs restent assez légers pour laisser les états de sélection et les réglages de ces variables prendre le dessus. Cette séparation entre paramètres communs et règles ciblées rejoint l’approche de [Minimal](https://github.com/kepano/obsidian-minimal/blob/master/src/scss/content/tables.scss) ; Tasogare conserve ses propres jetons et surfaces.

Le thème n’ajoute aucun masquage du contenu débordant ni aucune largeur minimale : Obsidian garde le défilement, les poignées et les outils d’édition. Aucun fragment propre à un coffre n’est nécessaire.

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
| `--tasogare-taille-bouton-icone` | 28 px (16 + 2 × 6) | côté du fond de survol d'une icône ; suit `--tasogare-taille-icone` |

Le survol d'une icône est un carré de côté « icône + 6 px de chaque côté » (28 px aujourd'hui), centré sur l'icône, le même pour toutes (icônes cliquables, boutons de la sidebar, ruban, onglets de la sidebar). Obsidian cale la boîte d'une icône sur `--header-height`, que Tasogare fixe à 30 px : cette boîte mesure alors 28 × 14 ou 28 × 16 px. Le thème dessine donc le fond avec `::after`, sans dépendre de la boîte. Sur mobile, le survol d'Obsidian reste.

## Ce qui change par rapport à Tasogare 1.6

- La marge verticale d'un onglet passe de 3 à 4 px, et celle d'une ligne de la sidebar de 7 à 8 px : les deux valeurs rejoignent l'échelle. Chaque ligne gagne 2 px de hauteur.
- La carte intérieure de la fenêtre de réglages passe d'un rayon de 10 à 6 px, pour être concentrique.
- Le sélecteur de coffre lit un espacement (`--space-6`) au lieu d'un rayon pour sa marge.
