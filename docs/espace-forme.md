# Espace et forme

Version : **1.1**. Décision : **5 novembre 2026**.

Cette spécification définit les espacements, les rayons, les filets, l'élévation (les ombres) et les icônes d'une interface. Elle ne définit ni les couleurs, ni la typographie, ni le mouvement. Les couleurs des filets et des ombres viennent de la spécification Couleur.

Les règles sur les surfaces et le téléphone viennent des skills `apple-design` et `mobile-native` d'Emil Kowalski (licence MIT, © 2026 Emil Kowalski, <https://github.com/emilkowalski/skill>), traduites et adaptées. Les règles de hiérarchie, d'alignement et de densité s'inspirent d'Interface Craft (Josh Puckett), reformulées.

## Principes

1. **Une échelle, pas des valeurs au cas par cas.** Un espacement prend une marche de l'échelle. Une valeur hors échelle doit dire pourquoi, en commentaire.
2. **Deux familles d'espace.** L'espace d'**interface** est en pixels : il entoure les contrôles. Le **rythme du texte** est en `rem` ou `em` : il suit la taille du texte.
3. **Le rayon grandit avec la surface.** Une petite marque a un petit rayon ; une grande carte, un grand rayon.
4. **Rayons concentriques.** Une forme posée dans une autre, avec une marge, prend le rayon extérieur moins la marge. Sinon, les coins ne sont pas parallèles.
5. **Peu d'élévation.** La plupart des surfaces sont plates. Une ombre dit qu'un objet flotte au-dessus des autres ; elle ne décore pas.
6. **Une ombre semi-transparente plutôt qu'un trait épais.** Un filet d'un pixel suffit pour séparer ; l'ombre dit la hauteur.
7. **Mêmes rayons, mêmes traits, même traitement d'un bout à l'autre.** La cohérence distingue une interface réfléchie d'une interface bâclée.
8. **Pas de filet dur sous une barre fixe.** Là où le contenu passe sous une barre qui flotte, un léger fondu suffit ; ailleurs, l'espace sépare mieux qu'un trait.
9. **Peu de niveaux, nettement distincts.** L'œil sait où aller en premier. Deux espacements trop proches ne disent rien : on saute une marche de l'échelle pour marquer un changement de niveau.
10. **Peu de lignes d'alignement.** Chaque élément s'aligne sur une ligne déjà présente. Quand le calcul tombe faux à l'œil (une icône dans une pastille, une icône à côté d'un texte), on corrige d'un ou deux pixels, et on écrit la correction en commentaire.
11. **Retirer tant que le sens reste.** Un filet, une marge, une ombre qui ne servent pas le sens partent. Moins, mais mieux.

## Échelle d'espace d'interface

Des pas de 2 px jusqu'à 16, puis des pas plus larges.

| Jeton | Valeur | Usage type |
| --- | ---: | --- |
| `--space-2` | 2 px | Entre deux lignes d'une liste serrée |
| `--space-4` | 4 px | Marge intérieure d'une pastille, d'une ligne |
| `--space-6` | 6 px | Marge verticale d'un petit bouton |
| `--space-8` | 8 px | Écart entre une icône et son libellé ; ligne de liste |
| `--space-10` | 10 px | Marge d'un cadre autour d'une carte |
| `--space-12` | 12 px | Marge intérieure d'un menu |
| `--space-14` | 14 px | Marge latérale d'un bloc de propriétés |
| `--space-16` | 16 px | Marge intérieure d'une carte |
| `--space-24` | 24 px | Entre deux groupes |
| `--space-32` | 32 px | Marge d'une page étroite |
| `--space-48` | 48 px | Entre deux sections |
| `--space-64` | 64 px | Marge d'une page large |

## Rythme du texte

Ces espaces suivent la taille du texte. Ils sont en `rem`, ou en `em` quand ils doivent suivre le texte qui les entoure.

| Jeton | Valeur | Usage |
| --- | ---: | --- |
| `--rhythm-paragraph` | 0,9rem | Entre deux paragraphes |
| `--rhythm-before-heading` | 3rem | Au-dessus d'un titre |
| `--rhythm-after-section` | 1rem | Sous un titre de section |
| `--rhythm-after-subheading` | 0,75rem | Sous un sous-titre |
| `--rhythm-indent` | 1,5rem | Retrait d'une citation |

## Rayons

| Jeton | Valeur | Usage |
| --- | ---: | --- |
| `--radius-mark` | 4 px | Tag, surlignage, pastille |
| `--radius-control` | 6 px | Champ, icône cliquable |
| `--radius-block` | 10 px | Ligne de liste, onglet, callout, image, menu, petite carte |
| `--radius-window` | 14 px | Fenêtre, invite |
| `--radius-card` | 16 px | Grande carte, panneau |

Rayon concentrique : `calc(var(--radius-card) - var(--space-10))`, pour une carte posée dans un panneau avec une marge de 10 px.

## Filets

| Jeton | Valeur | Usage |
| --- | ---: | --- |
| `--border-width` | 1 px | Tout filet : séparation, contour de fenêtre, de callout, de tag |
| `--focus-width` | 2 px | L'anneau de focus au clavier, jamais retiré |

La couleur d'un filet vient de `--color-rule` (repos) et `--color-rule-hover` (survol).

## Élévation

| Niveau | Objet | Ombre |
| --- | --- | --- |
| 0, plat | Cadre, carte de lecture, sidebar | aucune |
| 1, posé | Carte qu'on peut déplacer (kanban) | `0 1px 2px` |
| 2, flottant | Menu, popover, infobulle | `0 1px 2px` puis `0 8px 24px` |
| 3, fenêtre | Fenêtre modale, invite | `0 2px 8px` puis `0 24px 64px` |

Chaque ombre mélange `--color-shadow`. Plus la surface est grande, plus elle paraît épaisse : son ombre est plus profonde que celle d'une pastille. Une fenêtre modale s'accompagne d'un voile qui assombrit l'arrière-plan ; un panneau parallèle, non. Les niveaux 2 et 3 sont des valeurs de départ, à régler sur un vrai écran.

## Icônes

| Jeton | Valeur | Usage |
| --- | ---: | --- |
| `--icon-size` | 16 px | Icône d'interface |
| `--icon-stroke` | 1,75 px | Épaisseur du trait (icônes Lucide) |
| `--icon-gap` | 8 px | Écart entre une icône et son libellé |

## Sur téléphone

Chaque règle corrige un défaut précis. L'appliquer là où le défaut existe, pas partout par habitude.

| Défaut | Règle |
| --- | --- |
| Contenu coupé par l'encoche | `viewport-fit=cover`, puis des marges `--safe-top`, `--safe-bottom`, etc. sur les en-têtes, les barres et les feuilles |
| Hauteur fausse (barre d'adresse) | `100dvh` pour une coque d'application, `100svh` pour un écran d'accueil ; jamais `100vh` |
| Tirer pour rafraîchir vole le défilement | `overscroll-behavior: none` sur la racine, `contain` sur les zones qui défilent |
| Appui long qui sélectionne un libellé | `user-select: none` sur les contrôles seulement ; le contenu reste sélectionnable |
| Zoom à l'entrée dans un champ | Texte des champs à 16 px au moins (voir Typographie, `.type-field`) |

- Tester selon la capacité (`hover`, `pointer`, `env()`, `dvh`), jamais selon l'appareil ou la largeur d'écran.
- Ne jamais bloquer le zoom.
- Valider sur un vrai téléphone, de préférence ancien, clavier ouvert et en paysage.

## Validation avant adoption

- Aucune marge ni rayon écrit en chiffres hors des primitives.
- Chaque valeur hors échelle a un commentaire qui dit pourquoi.
- Les coins imbriqués sont concentriques.
- L'anneau de focus reste visible au clavier.
- Le rendu est vérifié sur ordinateur et sur un vrai téléphone.

## Changements depuis la version 1.0

- **Sources** : ajout des skills `apple-design` et `mobile-native` d'Emil Kowalski.
- **Principes ajoutés** : la cohérence des rayons et des traits, l'absence de filet dur sous une barre fixe, la hiérarchie par l'espace, la correction optique de l'alignement, la densité.
- **Élévation** : une grande surface paraît plus épaisse ; une fenêtre modale s'accompagne d'un voile.
- **Nouvelle section** : « Sur téléphone », avec les jetons de zone sûre `--safe-*`.

## CSS complet prêt à enregistrer

```css
/*
 * Espace et forme, version 1.1, choisie par Antoine le 5 novembre 2026.
 * Les primitives portent les valeurs ; les consommateurs lisent les jetons nommés.
 * Les couleurs des filets et des ombres viennent de la spécification Couleur (--color-rule, --color-shadow).
 */
:root {
  /* Échelle d'espace d'interface */
  --space-2: 2px;
  --space-4: 4px;
  --space-6: 6px;
  --space-8: 8px;
  --space-10: 10px;
  --space-12: 12px;
  --space-14: 14px;
  --space-16: 16px;
  --space-24: 24px;
  --space-32: 32px;
  --space-48: 48px;
  --space-64: 64px;

  /* Rythme du texte */
  --rhythm-paragraph: 0.9rem;
  --rhythm-before-heading: 3rem;
  --rhythm-after-section: 1rem;
  --rhythm-after-subheading: 0.75rem;
  --rhythm-indent: 1.5rem;

  /* Rayons */
  --radius-mark: 4px;
  --radius-control: 6px;
  --radius-block: 10px;
  --radius-window: 14px;
  --radius-card: 16px;

  /* Filets */
  --border-width: 1px;
  --focus-width: 2px;

  /* Élévation : la forme ici, la couleur dans --color-shadow */
  --elevation-1: 0 1px 2px var(--color-shadow);
  --elevation-2: 0 1px 2px var(--color-shadow), 0 8px 24px var(--color-shadow);
  --elevation-3: 0 2px 8px var(--color-shadow), 0 24px 64px var(--color-shadow);

  /* Icônes */
  --icon-size: 16px;
  --icon-stroke: 1.75px;
  --icon-gap: var(--space-8);

  /* Zones sûres du téléphone (encoche, barre d'accueil) ; 0 ailleurs. */
  --safe-top: env(safe-area-inset-top, 0px);
  --safe-right: env(safe-area-inset-right, 0px);
  --safe-bottom: env(safe-area-inset-bottom, 0px);
  --safe-left: env(safe-area-inset-left, 0px);
}
```
