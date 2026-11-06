# Typographie 1.1 dans Obsidian

Ce document explique comment Tasogare applique la [spécification Typographie 1.1](typographie.md) dans Obsidian. Le code fait foi : il se trouve dans `theme.css`, sections « Échelle typographique » (couche 1) et « Typographie » (couche 2). Ce document ne recopie pas le CSS, pour garder une seule source.

## L'idée

Obsidian n'utilise pas de classes `.type-*`. Il lit ses propres variables : `--h1-size`, `--tab-font-size`, `--line-height-normal`, etc. Tasogare remplit donc ces variables avec l'échelle de la spécification.

## La base : 1rem = ton réglage de taille de police

Obsidian écrit le réglage **Apparence → Taille de police** à deux endroits : dans `--font-text-size` (taille du texte des notes) et dans la taille racine de la page (donc `1rem`). Un thème ne peut pas changer `--font-text-size` : Obsidian l'écrase avec ton réglage.

Tasogare exprime donc chaque rôle comme un **rapport** au texte courant de la spécification (15 px) :

- le contenu des notes lit ce rapport en `em` : il suit le texte qui l'entoure (dans une note, un callout, la sidebar) ;
- l'interface lit ce rapport en `rem` : elle suit ton réglage.

**Règle la taille de police sur 15** pour obtenir les valeurs exactes de la spécification. À 16, toute l'échelle grandit de 16/15, sans changer ses proportions.

## Correspondance des rôles

| Élément d'Obsidian | Variables d'Obsidian | Rôle | Valeur à 15 px |
| --- | --- | --- | --- |
| Texte des notes | `--line-height-normal` | `body` | 15 px, interligne 1,75 |
| Titre de note et h1 | `--inline-title-*`, `--h1-*` | `title` | 28 / 500, −0,02em |
| Titre sur téléphone | idem, sous `.is-phone` | `title` | 26 / 500 |
| h2 | `--h2-*` | `section` | 19 / 500, −0,01em |
| h3 | `--h3-*` | `subheading` | 16 / 500, −0,01em |
| h4 | `--h4-*` | `heading` | 15 / 500 |
| h5 | `--h5-*` | `label` | 14 / 500, −0,01em |
| h6 | `--h6-*` | `overline` | 12 / 500, +0,05em |
| Gras | `--bold-modifier` | `emphasis` | 600 (400 + 200) |
| Code | `--code-size` | `code` | 13 px |
| Tags | `--tag-size` | `tag` | 12 px |
| Tableaux de note | `--table-text-size` | `small` | 13 px |
| Propriétés | `--metadata-label-font-size`, `--metadata-input-font-size` | `small` | 13 px |
| Onglets | `--tab-font-size`, `--tab-font-weight` | `label` | 14 / 500 |
| Fichiers et dossiers | `--nav-item-size` | `small` | 13 px |
| Nom du coffre | `--vault-profile-font-*` | `label` | 14 / 500, −0,01em |
| Titres de la fenêtre de réglages | `--setting-group-heading-weight` | `heading` | graisse 500 |
| Barre d'état | `--status-bar-font-size` | `micro` | 11,52 px |
| Infobulles | `--tooltip-font-size`, et une règle pour l'approche | `caption` | 13 px, +0,01em |
| Fil d'Ariane | `--file-header-font-size` (valeur d'Obsidian : `--font-ui-small`) | `small` | 13 px |
| Tableaux de Bases | `--bases-table-font-size` | `small` | 13 px |
| Petites tailles de l'interface | `--font-ui-smaller` à `--font-ui-large` | `tag`, `small`, `body`, `section` | 12, 13, 15, 19 px |

L'approche des titres passe par `--h1-letter-spacing` à `--h6-letter-spacing`. Obsidian écrit en dur celle du titre de note (`.inline-title`) : une seule règle lui rend l'approche du h1.

## Ce qui n'a pas d'équivalent

`hero`, `figure`, `lede` et `wordmark` n'ont pas d'élément dans Obsidian. Ils restent dans la spécification. On pourra les relier plus tard à des classes de note (`cssclasses`), par exemple pour un tableau de bord.

Le nom du coffre prend `label` plutôt que `wordmark` : à 17 / 600, il pesait trop dans la sidebar.

## Ce qui change par rapport à Tasogare 1.6

- Le titre passe de 30 à 28 px, et son approche de −0,04em à −0,02em.
- Le h2 passe de la graisse 550 à 500, et son approche de −0,02em à −0,01em.
- Les onglets passent à 14 / 500 (rôle `label`) ; l'onglet actif se distingue par sa couleur.
- La taille optique d'Inter redevient automatique (`font-optical-sizing: auto`, le comportement par défaut) au lieu d'être forcée à 32. Un titre de 28 px reste proche du dessin « Display » ; un h2 de 19 px prend un dessin plus proche du texte.
- La police est appelée `"Inter"`, le nom sous lequel Obsidian 1.15 l'embarque. L'ancien nom `"Inter Variable"` ne fonctionnait que si Inter était installée sur l'ordinateur.
