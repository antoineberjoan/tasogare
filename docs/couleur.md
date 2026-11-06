# Couleur

Version : **1.0**. Décision : **5 novembre 2026**.

Cette spécification définit la **structure** des couleurs d'une interface : des emplacements, des règles de contraste et une façon d'ajouter une palette. Elle ne choisit pas les couleurs d'un projet. Les valeurs du bloc CSS en bas sont un exemple (Crépuscule Alpin), à remplacer.

## Principes

1. **Une palette remplit des emplacements.** Le reste de l'interface lit seulement les emplacements. Changer de palette ne touche aucune règle.
2. **Un emplacement a un usage, écrit à côté de lui.** Un même usage lit toujours le même emplacement.
3. **Une seule couleur d'accent, avec un rôle.** Elle marque le titre et les liens. Une deuxième couleur, l'action, marque ce qu'on clique (boutons, cases).
4. **Le contraste se vérifie par un outil, pas à l'œil.** Une palette qui échoue un seuil ne part pas.
5. **Les transparences se calculent depuis un emplacement.** Un survol ou un filet mélange une couleur de la palette avec du transparent (`color-mix`). Aucune couleur `rgba` écrite à la main.
6. **Chaque palette existe en clair et en sombre.** Les deux modes remplissent les mêmes emplacements.

## Les emplacements

| Emplacement | Usage |
| --- | --- |
| `frame` | Le cadre : le fond autour des cartes, la sidebar |
| `surface` | La carte : le fond de lecture |
| `sunken` | Le creux : blocs de code, en-têtes de tableau |
| `veil` | La teinte des survols et des filets, mélangée à du transparent |
| `shadow` | La teinte des ombres |
| `rule-table` | Les filets d'un tableau |
| `rule-strong` | Les filets visibles : ligne horizontale, bord de citation |
| `ink` | Le texte courant |
| `ink-muted` | Le texte secondaire |
| `ink-faint` | Le texte discret et le décor ; jamais un libellé important |
| `accent` | Le titre, les liens |
| `accent-hover` | Un lien survolé |
| `action` | Un bouton principal |
| `action-hover` | Un bouton principal survolé |
| `on-action` | Le texte posé sur `action` |
| `check` | Une case cochée |
| `on-check` | La marque dans la case cochée |
| `highlight` | Le surlignage |
| `selection` | Le texte sélectionné |
| `search` | Un résultat de recherche |
| `red` à `pink` | Huit couleurs de signal : rouge, orange, jaune, vert, cyan, bleu, violet, rose |

## Les parts de transparence

Les survols, les filets et les surlignages mélangent un emplacement avec du transparent. La part dépend du mode : un fond sombre demande souvent une part plus forte.

| Part | Mélange | Clair | Sombre |
| --- | --- | ---: | ---: |
| `hover` | `veil` | 5 % | 7 % |
| `rule` | `veil` | 8 % | 6 % |
| `rule-hover` | `veil` | 16 % | 12 % |
| `shadow` | `shadow` | 8 % | 50 % |
| `highlight` | `highlight` | 42 % | 30 % |
| `selection` | `selection` | 55 % | 45 % |
| `search` | `search` | 18 % | 10 % |

Une palette peut changer une part quand sa couleur est plus forte. Par exemple, une sélection verte vive descend à 30 %.

## Seuils de contraste

Les seuils suivent les WCAG 2.x (niveau AA, plus un seuil plus haut pour le texte courant).

| Texte | Fond | Minimum |
| --- | --- | ---: |
| `ink` | `surface` | 7:1 |
| `ink` | `frame` | 4,5:1 |
| `ink-muted` | `frame` et `surface` | 4,5:1 |
| `ink-faint` | `surface` | 3:1 |
| `accent`, `accent-hover` | `surface` | 4,5:1 |
| `on-action` | `action`, `action-hover` | 4,5:1 |
| `on-check` | `check` | 3:1 |
| `check` | `surface` | 3:1 |
| chaque signal | `surface` | 3:1 |

Quand une couleur de la palette échoue un seuil, la palette garde son nom et sa teinte, mais l'emplacement reçoit une version assombrie (en clair) ou éclaircie (en sombre). Note-le à côté de la valeur : « Bouée rouge, assombrie pour le texte ».

## Ajouter une palette

1. Nommer la palette et ses couleurs, avec la photo ou l'objet qui l'inspire.
2. Choisir `frame`, `surface` et `ink` pour chaque mode. Ce sont eux qui donnent l'ambiance.
3. Choisir `accent`, puis `action`. Vérifier qu'ils sont distincts de `ink`.
4. Dériver les nuances manquantes (survols, texte secondaire, signaux) depuis les couleurs de la palette.
5. Lancer l'outil de contraste. Corriger chaque échec.
6. Regarder la palette sur un vrai écran, en clair et en sombre, avec une note complète.

## Validation avant adoption

- L'outil de contraste passe sans échec, pour chaque palette et chaque mode.
- Aucune règle ne lit une couleur de palette directement : seulement des emplacements.
- Aucune valeur `rgba` ou hexadécimale hors des blocs de palette.
- Le rendu est vérifié sur un vrai écran, en clair et en sombre.

## CSS complet prêt à enregistrer

L'exemple suit la palette Crépuscule alpin. Une autre palette se déclare avec une classe sur la racine (`.palette-galet`) et redéfinit seulement ce qui change.

```css
/*
 * Couleur, version 1.0, choisie par Antoine le 5 novembre 2026.
 * Les palettes remplissent les emplacements ; les consommateurs lisent les rôles en bas.
 * Mode sombre : attribut data-theme="dark" sur la racine (à adapter au projet).
 */

/* ---------- Palette d'exemple : Crépuscule alpin, clair ---------- */
:root {
  --palette-frame: #edecf5;          /* Neige lavande */
  --palette-surface: #ffffff;        /* Neige */
  --palette-sunken: #edecf5;
  --palette-veil: #1f2a3a;           /* Sapin nuit */
  --palette-shadow: #1f2a3a;
  --palette-rule-table: #dcd9eb;
  --palette-rule-strong: #b9b3d6;    /* Neige d'ombre */
  --palette-ink: #4a4e5c;            /* Câble acier */
  --palette-ink-muted: #666976;
  --palette-ink-faint: #8b8e99;
  --palette-accent: #9e2b25;         /* Cabine rouge */
  --palette-accent-hover: #7e211d;
  --palette-action: #9e2b25;
  --palette-action-hover: #7e211d;
  --palette-on-action: #ffffff;
  --palette-check: #6e6ba8;          /* Ciel lavande */
  --palette-on-check: #ffffff;
  --palette-highlight: #f4c66a;      /* Lueur */
  --palette-selection: #b9b3d6;
  --palette-search: #e8a3b4;         /* Alpenglow */
  --palette-red: #9e2b25;
  --palette-orange: #c46e28;
  --palette-yellow: #b0801e;
  --palette-green: #4f7a5a;
  --palette-cyan: #3d7a80;
  --palette-blue: #4a6096;
  --palette-purple: #6e6ba8;
  --palette-pink: #be627c;

  --part-hover: 5%;
  --part-rule: 8%;
  --part-rule-hover: 16%;
  --part-shadow: 8%;
  --part-highlight: 42%;
  --part-selection: 55%;
  --part-search: 18%;
}

/* ---------- Palette d'exemple : Crépuscule alpin, sombre ---------- */
:root[data-theme="dark"] {
  --palette-frame: #1f2a3a;          /* Sapin nuit */
  --palette-surface: #293546;
  --palette-sunken: #232e3e;
  --palette-veil: #e6e4ef;
  --palette-shadow: #1f2a3a;
  --palette-rule-table: color-mix(in oklch, #e6e4ef 12%, transparent);
  --palette-rule-strong: color-mix(in oklch, #e6e4ef 14%, transparent);
  --palette-ink: #e6e4ef;
  --palette-ink-muted: #b9b3d6;      /* Neige d'ombre */
  --palette-ink-faint: #9d99b8;
  --palette-accent: #e8a3b4;         /* Alpenglow */
  --palette-accent-hover: #f2c0cd;
  --palette-action: #6e6ba8;         /* Ciel lavande */
  --palette-action-hover: #5e5b96;
  --palette-on-action: #ffffff;
  --palette-check: #e8a3b4;
  --palette-on-check: #1f2a3a;
  --palette-highlight: #f4c66a;
  --palette-selection: #6e6ba8;
  --palette-search: #e8a3b4;
  --palette-red: #e06e64;
  --palette-orange: #eca064;
  --palette-yellow: #f4c66a;
  --palette-green: #a8cfa0;
  --palette-cyan: #8cc8c8;
  --palette-blue: #8ca0dc;
  --palette-purple: #b9b3d6;
  --palette-pink: #e8a3b4;

  --part-hover: 7%;
  --part-rule: 6%;
  --part-rule-hover: 12%;
  --part-shadow: 50%;
  --part-highlight: 30%;
  --part-selection: 45%;
  --part-search: 10%;
}

/* ---------- Rôles : ce que lisent les consommateurs ---------- */
:root,
:root[data-theme="dark"] {
  --color-frame: var(--palette-frame);
  --color-surface: var(--palette-surface);
  --color-sunken: var(--palette-sunken);
  --color-hover: color-mix(in oklch, var(--palette-veil) var(--part-hover), transparent);
  --color-rule: color-mix(in oklch, var(--palette-veil) var(--part-rule), transparent);
  --color-rule-hover: color-mix(in oklch, var(--palette-veil) var(--part-rule-hover), transparent);
  --color-rule-table: var(--palette-rule-table);
  --color-rule-strong: var(--palette-rule-strong);
  --color-shadow: color-mix(in oklch, var(--palette-shadow) var(--part-shadow), transparent);
  --color-ink: var(--palette-ink);
  --color-ink-muted: var(--palette-ink-muted);
  --color-ink-faint: var(--palette-ink-faint);
  --color-accent: var(--palette-accent);
  --color-accent-hover: var(--palette-accent-hover);
  --color-action: var(--palette-action);
  --color-action-hover: var(--palette-action-hover);
  --color-on-action: var(--palette-on-action);
  --color-check: var(--palette-check);
  --color-on-check: var(--palette-on-check);
  --color-highlight: color-mix(in oklch, var(--palette-highlight) var(--part-highlight), transparent);
  --color-selection: color-mix(in oklch, var(--palette-selection) var(--part-selection), transparent);
  --color-search: color-mix(in oklch, var(--palette-search) var(--part-search), transparent);
  --color-red: var(--palette-red);
  --color-orange: var(--palette-orange);
  --color-yellow: var(--palette-yellow);
  --color-green: var(--palette-green);
  --color-cyan: var(--palette-cyan);
  --color-blue: var(--palette-blue);
  --color-purple: var(--palette-purple);
  --color-pink: var(--palette-pink);
}
```
