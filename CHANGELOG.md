# Journal des versions

## 1.9.0

### Refonte

- Crépuscule japonais, une palette claire et sombre inspirée du lac Ashi et de son torii.

- Grille fine entre les colonnes des Bases et des tableaux Markdown. Propriétés alignées sur une colonne commune et bouton d’ajout visible.

- Tableaux de Bases séparés du panneau par une marge intérieure ; en-têtes teintés, libellés contrastés et filets de tableau de la palette. Contrôles natifs conservés.

- Règles de composants réécrites à partir des variables et contrôles natifs d’Obsidian. Palettes et échelle typographique conservées.
- Une seule source CSS, sans compilation, JavaScript d’affichage ni fragment supplémentaire. Sélecteurs limités à leur composant et règles distinctes pour le bureau.
- Cadre et panneau droit avec le même inset ; rôle de hauteur commun aux barres d’onglets, séparé des contrôles de note. Onglets empilés conservés.
- Menu natif du coffre aligné sous son bouton. Badge des rétroliens translucide au survol, avec un fond opaque lorsque la transparence est réduite. La barre d’état suit le volet actif dans une vue scindée.
- Aide, réglages et repli sur la ligne du sélecteur de coffre. L’extension facultative Interface romā ajoute le tiroir de lecture et une sélection multiple des éléments visibles.
- Marges latérales élargies dans la navigation gauche. Le tiroir d’Interface romā s’insère dans la carte active et laisse le panneau du graphe local accessible à côté.
- Quand la navigation est repliée, l’inset gauche du cadre principal reprend le même fond que les autres bords. La navigation ouverte a davantage de marge au bord gauche.
- Les icônes d’Obsidian dans les barres d’onglets utilisent la même surface de survol. Le tiroir de lecture reçoit un léger retrait et reprend la couleur d’accent sur ses quatre bords.
- Les libellés d’onglet, les dossiers et les notes à la racine de la navigation gauche partagent le même alignement. Les sous-dossiers gardent leur retrait.
- En mode clair, le fond commun du cadre et des panneaux latéraux se distingue davantage des cartes. Les onglets de navigation ont des zones de survol plus amples.
- Propriétés natives éditables et repliables, avec ajout accessible au clavier. Les autres actions d’édition restent visibles.
- Pages larges via `cssclasses: [wide]`, sans calcul de translation des Bases. Tableaux et cartes conservent les contrôles natifs.
- Suppression des survols artificiels des icônes, des remplacements SVG des fichiers et des réglages géométriques des fenêtres.
- Contrôles de source renforcés et un test d’interface autonome : données temporaires, parité Minimal, préservation des notes, palettes et dispositions.

## 1.8.0

### Nouveautés

- Palette **Graphite**, par défaut : des gris neutres (cadre `#F2F2F7`, carte blanche, encre `#1C1C1E`) et un seul bleu pour l'accent. Clair et sombre, avec les seuils de contraste WCAG AA. Les six autres palettes restent au choix dans Style Settings.
- Sidebar : les icônes des notes et des dossiers viennent de Hugeicons (licence MIT, trait de 1,5). Un dossier ouvert montre un dossier ouvert.
- Sidebar : la ligne active devient une pastille posée (fond de la carte, ombre de niveau 1), comme l'onglet actif.
- Sidebar : un trait guide les enfants d'un dossier. La racine du coffre n'a ni trait ni retrait.

### Corrections

- Les boutons de sidebar repliée se centrent sur la rangée d'onglets, et leur fond de survol est carré au lieu d'un rectangle plat.
- Toutes les icônes ont le même survol : un carré centré sur l'icône, de côté « icône + 6 px de chaque côté », donc 28 px (`--tasogare-taille-bouton-icone`, qui suit `--tasogare-taille-icone`). Avant, les fonds mesuraient 28 × 14, 28 × 16 ou 28 × 24 px selon l'endroit. Ordinateur seulement.

### Changements

- La carte intérieure de la fenêtre de réglages, ouverte dans sa propre fenêtre, prend le rayon de la carte de note (16 px). Dans une fenêtre intégrée, elle garde le rayon concentrique (6 px).
- Crépuscule alpin n'est plus la palette de base : elle devient une palette à classe (`tasogare-crepuscule`), comme les cinq autres. Sans Style Settings, c'est Graphite qui s'applique.
- `outils/palettes.py` lit la palette de base dans la constante `BASE`.
- Les six autres palettes n'écrivent plus aucune couleur dans leurs emplacements : leurs 155 nuances dérivées sont des couleurs sources nommées (`<palette>-<emplacement>-<mode>`), comme celles de Graphite. Les couleurs résolues sont identiques à celles de 1.7.0.
- `outils/palettes.py --accord` réécrit `--tasogare-accent-h/s/l` depuis l'accent de chaque palette : changer une couleur source suffit.
- La gouttière de la flèche des dossiers (`--tasogare-gouttiere-nav`) et les parts des filets sombres (`--tasogare-part-filet-tableau`, `--tasogare-part-filet-fort`) ont chacune une seule source.

## 1.7.0

### Nouveautés

- Six palettes, chacune en clair et en sombre, une par famille de couleur : Crépuscule alpin (par défaut), Grès rosé, Thé vert, Lac profond, Porte bleue et Galet noir. Le choix se fait avec le plugin Style Settings ; sans lui, Crépuscule alpin s'applique.
- Typographie 1.1 : titre 28 / 500, h2 19 / 500, texte avec un interligne de 1,75. L'échelle suit le réglage de taille de police d'Obsidian.
- Design system documenté dans `docs/` : couleur, typographie, espace et forme, mouvement.
- `outils/palettes.py` vérifie les contrastes de chaque palette (WCAG AA).
- Bases : titres de cartes et de kanban plus légers, liens de la vue liste sans soulignement.
- Fenêtre de réglages : chaque groupe devient une carte du cadre, comme le bloc de propriétés ; la navigation de gauche reprend les lignes de la sidebar.

### Corrections

- La police Inter embarquée par Obsidian est enfin utilisée (elle s'appelle « Inter », pas « Inter Variable »).
- Les callouts `tip`, `summary` et `important` prennent le cyan de la palette.
- Les rayons des champs, des icônes et des fenêtres s'appliquent aussi sur macOS.
- Les icônes par clé de propriété s'affichent en entier (Obsidian 1.15 réduisait leur dessin à 4 px).
- La barre de défilement mesure 11 px comme prévu, et l'onglet actif garde sa pastille au survol.
- Le nom du coffre passe à 14 / 500 (rôle `label`) : à 17 / 600, il pesait trop dans la sidebar.
- Style Settings : plus de filet courbe sous les titres de section ; les titres de la fenêtre de réglages passent à la graisse 500.
- Les surlignages de couleur d'Obsidian (bleu, vert…) gardent leur couleur.
- Choisir une couleur d'accent dans les réglages d'Obsidian ne rend plus le texte des boutons illisible.
- Les dossiers de la sidebar ont la même hauteur que les notes.
- Les pastilles de liste des propriétés ont une marge intérieure ; une propriété texte tient sur une ligne.
- Le titre de note reçoit bien son approche (−0,02em) ; les h1 à h6 passent par les variables d'Obsidian.
- La barre d'onglets a le même inset au-dessus et au-dessous, et la première pastille s'aligne sur la carte.
- Le retrait des citations s'applique en lecture.
- Le bloc de propriétés replié garde son titre, pour pouvoir le rouvrir.
- Dans les sous-pages des réglages, la barre de titre prend la couleur de la carte : plus de bande du cadre en haut.
- La fenêtre de réglages, ouverte dans sa propre fenêtre, n'a plus de coins clairs sous la barre du haut.
- Sur téléphone et tablette, la mise en page d'Obsidian est respectée ; la croix des pastilles reste visible au toucher.
- Une Base intégrée dans un callout, un aperçu ou un canvas garde la largeur d'Obsidian.

### Changements

- Aucun `!important` : un snippet peut maintenant modifier n'importe quelle règle du thème.
- Chaque couleur nommée d'une palette s'écrit une seule fois dans `theme.css`.
- Les icônes par clé de propriété deviennent un snippet facultatif : `snippets/tasogare-icones-proprietes.css`.
- Retrait du script `lier-coffre.sh`.
- Version minimale d'Obsidian : 1.15.0, la version testée.
- `outils/verifier.py` contrôle variables, couleurs, contrastes, tableaux de la doc et journal, à chaque envoi et à chaque pull request.
