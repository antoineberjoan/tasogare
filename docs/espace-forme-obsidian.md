# Espace et forme dans Obsidian

La [fondation](espace-forme.md) décrit l’échelle ; `theme.css` définit les valeurs réellement consommées.

## Cadre

L’inset unique de 10 px sépare le cadre des cartes centrales et du panneau droit. Il est porté par le conteneur des cartes : aucune largeur de sidebar n’est nécessaire pour le calculer.

Un onglet mesure 30 px. Sa barre mesure la hauteur de l’onglet plus deux insets, soit 50 px. Ce rôle est local aux barres d’onglets ; les en-têtes et boutons à l’intérieur des notes gardent leur géométrie native. Les onglets empilés gardent leurs en-têtes verticaux.

## Formes

| Rôle    | Rayon | Usage                                        |
| ------- | ----: | -------------------------------------------- |
| Marque  |  4 px | Tags et pastilles                            |
| Champ   |  6 px | Entrées et contrôles                         |
| Bloc    | 10 px | Onglets, cartes de Bases, tableaux, encadrés |
| Fenêtre | 14 px | Menus et fenêtres natives                    |
| Carte   | 16 px | Panneaux centraux et panneau droit           |

Les valeurs passent par les variables natives. Les boutons n’ont pas de pseudo-élément de survol ajouté par le thème. Les fenêtres de réglages gardent la structure d’Obsidian.

## Texte et pages

Une note reste dans sa colonne de lecture de 640 px. La classe native `cssclasses: [wide]` remplace la largeur de lecture par 100 % dans cette note. Une Base intégrée suit alors la largeur de la page, sans translation ni compensation géométrique. Un fichier `.base` ouvert directement garde sa disposition native.

Les propriétés utilisent la largeur intrinsèque de leur champ de clé. La clé occupe au plus la moitié de la rangée et la valeur peut se replier. Les deux-points sont visuels. Ces règles sont limitées au bloc de métadonnées de la note et ne concernent pas les menus de Bases. Le mobile et les moteurs sans `field-sizing: content` gardent l’alignement natif.

## Surfaces

Les tableaux Markdown et de Bases utilisent le fond de la carte, un filet discret, un rayon de bloc et l’ombre posée. Le thème ne fixe ni les colonnes ni le ratio des couvertures. Il ne masque pas les outils d’édition ou le défilement des tableaux.

La barre d’état est masquée par défaut sur ordinateur. Lorsqu’elle est affichée, une ancre CSS la place dans la dernière carte centrale visible ; sa largeur maximale vient de cette carte. Cette règle requiert le moteur de l’Obsidian 1.15 déclaré dans le manifeste. Les sidebars peuvent donc changer de taille sans coordonnée ajoutée au thème.

Les contrastes proviennent des palettes. Les anneaux de focus et les interactions des widgets restent natifs. Le bouton d’ajout de propriété réapparaît au survol ou dès que le bloc reçoit le focus ; les autres actions d’édition ne sont pas masquées par le thème.
