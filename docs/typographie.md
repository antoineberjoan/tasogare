# Typographie

Version : **1.1**. Décision : **5 novembre 2026**.

Cette spécification définit une typographie d’interface réutilisable. Elle garde la police du projet. Elle ne définit ni les couleurs, ni les espacements de mise en page, ni les composants.

## Principes

1. **Une seule source de tokens par projet.** Les autres fichiers lisent cette source. Un export est toujours généré depuis elle, jamais maintenu à la main.
2. **Un rôle est un ensemble complet** : famille, taille, graisse, interligne et approche. Choisir un rôle, ne pas recomposer ces propriétés dans chaque écran.
3. **Aucune valeur typographique locale.** Les consommateurs utilisent les rôles ou les classes `.type-*`. Les valeurs brutes vivent seulement dans les primitives.
4. **Garder la police du projet.** Ce fichier n’impose aucun fichier de police ni aucun import externe.
5. **Suivre les préférences de lecture.** Les tailles sont en `rem`. Ne pas fixer la taille racine en pixels. Ne pas bloquer le zoom.
6. **Une seule échelle en clair et en sombre.** Les couleurs et leur contraste dépendent des tokens de couleur du projet.

## Table des styles

Les équivalents en pixels supposent une base de 16 px. Ils aident à lire la table. Ne les recopie pas dans les composants : le CSS complet en bas de ce document fait foi.

| Rôle | Taille (px) | Graisse | Interligne (px) | Approche | Usage |
| --- | ---: | ---: | ---: | --- | --- |
| `hero` | 44 | 600 | 46 | `-0.03em` | Chiffre principal, au plus un par écran |
| `title` | 28 | 500 | 34 | `-0.02em` | Titre de page, un par écran |
| `figure` | 24 | 600 | 28 | `-0.02em` | Chiffre d’une tuile |
| `section` | 19 | 500 | 24 | `-0.01em` | Groupe de contenus, section ou dialogue |
| `wordmark` | 17 | 600 | 20 | `-0.03em` | Nom compact du projet |
| `lede` | 17 | 400 | 28 | `-0.01em` | Introduction éditoriale courte |
| `subheading` | 16 | 500 | 24 | `-0.01em` | Niveau interne d’une section |
| `heading` | 15 | 500 | 20 | `0em` | Titre de carte ou d’élément de liste |
| `body` | 15 | 400 | 26,25 (rapport 1,75) | `0em` | Texte courant |
| `label` | 14 | 500 | 20 | `-0.01em` | Bouton, onglet, libellé ou champ |
| `small` | 13 | 400 | 18 | `0em` | Détail sous un titre |
| `caption` | 13 | 400 | 18 | `0.01em` | Unité, date, axe ou aide de champ |
| `code` | 13 | 400 | 20 | `0em` | Code, avec la famille monospace |
| `overline` | 12 | 500 | 18 | `0.05em` | Surtitre discret, en casse de phrase |
| `tag` | 12 | 400 | 16 | `0em` | Mot court dans une pastille |
| `micro` | 11,52 | 400 | 14 | `0.01em` | Métadonnée compacte, jamais une phrase |

Le texte courant utilise un **rapport** d’interligne (1,75) et non une longueur. L’interligne suit donc la taille du texte, même si un projet change la taille de `body`. Les autres rôles gardent un interligne fixe en `rem`, plus serré, adapté à l’interface.

Sur petit écran, le titre passe à **26 / 500**, avec un interligne de **34 px**. Le seuil est `40rem` et il vit dans ce fichier : une variable CSS ne fonctionne pas dans une condition `@media`.

Un grand panneau peut employer le rôle `section`. Une carte compacte emploie `heading`. Utiliser le même rôle pour le même niveau de contenu dans tout le projet.

## Familles

- `--font-sans` : la famille de l’interface. Par défaut, les polices système.
- `--font-mono` : la famille du code et des valeurs à aligner.
- `--type-optical-sizing` : laisse la police utiliser ses tailles optiques, si elle en a.

Relier les familles aux tokens du projet **après** l’import du fichier :

```css
:root {
  --font-sans: var(--project-font-sans);
  --font-mono: var(--project-font-mono);
}
```

`--project-font-sans` et `--project-font-mono` sont des exemples. Remplace-les par les tokens que le projet déclare vraiment. Ne garde aucune référence vers une variable non définie. Le dessin et les graisses de la police choisie peuvent changer un peu le rendu.

## Utilisation sans framework

Enregistrer le bloc CSS complet de ce document dans `typographie.css`, puis le charger une seule fois :

```html
<link rel="stylesheet" href="typographie.css" />

<main class="type-body">
  <h1 class="type-title">Bilan annuel</h1>
  <h2 class="type-section">Activité</h2>
  <h3 class="type-heading">Premier trimestre</h3>
  <p class="type-caption">Durée totale</p>
  <p class="type-figure">8 h 28</p>
  <p>Un texte avec une <strong class="type-emphasis">information importante</strong>.</p>
</main>
```

La feuille de style n’ajoute aucun reset global ni aucune marge. La mise en page et les composants restent ceux du projet.

### Chiffres, code et emphase

- Les rôles `hero` et `figure` utilisent déjà les chiffres tabulaires : chaque chiffre a la même largeur.
- Ajouter `.type-numeric` aux autres valeurs qui changent et aux colonnes de chiffres.
- Utiliser `.type-code` pour le code. Ce rôle choisit la famille monospace.
- Utiliser `.type-emphasis` pour une emphase à 600. Relier aussi `strong` et `b` à `--type-emphasis-weight` dans le projet.
- Ne pas mettre tous les titres en gras. Leur rôle fixe déjà la hiérarchie.

### Champs et toucher

La classe `.type-field` applique le rôle `label` sur ordinateur. Sur un écran tactile, elle porte le texte à `--touch-input-size` (16 px à la base habituelle). En dessous de 16 px, iOS zoome sur le champ pendant la saisie. Ne pas réduire un titre éditable déjà plus grand. Garder les composants et les cibles tactiles du système de design du projet.

## Tailwind 4 et autres bibliothèques

Le fichier expose aussi les variables natives de Tailwind 4 pour la taille et la graisse, reliées aux rôles. Les composants Tailwind déjà compilés lisent ainsi la même échelle.

Ce CSS reste du CSS standard. Il ne crée pas à lui seul de nouveaux utilitaires Tailwind. Pour écrire `text-heading`, le projet déclare ces noms dans son bloc `@theme`. Les classes `.type-*` fonctionnent directement, sans compilation et dans n’importe quel framework.

## Architecture et règles de contrôle

- **Primitives** : les seules déclarations de valeurs brutes.
- **Rôles** : des références aux primitives, chacune avec son usage écrit.
- **Consommateurs** : les classes de texte, les styles d’écran et les composants. Ils lisent seulement les rôles.
- **Adaptation mobile** : définie à côté des tokens, sans seuil recopié dans les écrans.

Exemple correct quand un assemblage ne peut pas recevoir de classe :

```css
.page-heading {
  font-family: var(--font-sans);
  font-size: var(--type-title-size);
  line-height: var(--type-title-leading);
  font-weight: var(--type-title-weight);
  letter-spacing: var(--type-title-tracking);
}
```

Refuser dans les consommateurs : les tailles, graisses, interlignes ou approches écrites en chiffres, les familles en dur, les styles en ligne équivalents (par exemple dans React) et les utilitaires arbitraires qui contournent les rôles. L’héritage CSS reste permis.

## Validation avant adoption

- Vérifier le rendu avec la vraie police du projet.
- Vérifier les retours à la ligne des titres et des libellés longs.
- Vérifier sur ordinateur et sur téléphone, en clair et en sombre.
- Vérifier le zoom, les préférences de taille du lecteur et la saisie tactile.
- Vérifier le contraste avec les tokens de couleur du projet.
- Vérifier qu’un export se régénère quand une primitive change, et qu’il ne contient aucune variable non définie.

Ce document est un **instantané réutilisable** de la version 1.1. Une évolution part de la source de tokens, puis régénère les livrables. Chaque projet adopte une version de façon explicite et garde ses propres polices et couleurs.

## Changements depuis la version 1.0

- **Texte courant** : l’interligne passe de 22 px à un rapport de 1,75 (26,25 px à 15 px).
- **Chiffres tabulaires** : `hero` et `figure` les appliquent eux-mêmes. Les commentaires de la 1.0 le promettaient, mais les classes ne le faisaient pas.
- **`.type-field`** : reçoit aussi `font-optical-sizing`, comme les autres classes.
- **Nettoyage** : retrait des références à un autre projet (nom de projet, séances, sport, calendrier, contrôles « épinglés »). Tous les commentaires sont en français.
- **Primitives inutilisées retirées** : `11 px`, `30 px` et l’interligne `40 px`.
- **Tailwind** : retrait des surcharges `--leading-*` et `--tracking-*`. Elles redonnaient les valeurs par défaut de Tailwind et servaient seulement des composants d’un projet précis.
- **Nom du fichier** : `typographie.css` au lieu de `typography-equilibre.css`.

## Pistes pour une version 1.2

Ces pistes changent le rendu. Elles ne sont pas appliquées.

- **Arrondir `micro` à 11 px.** 11,52 px vient d’une référence externe. Un nombre rond est plus simple à retenir et l’écart ne se voit presque pas.
- **Distinguer `text-lg` et `text-xl` dans Tailwind.** Les deux pointent vers `section` : une marche de l’échelle disparaît.
- **Équilibrer les titres sur plusieurs lignes** avec `text-wrap: balance` sur `hero`, `title` et `section`. Les lignes gardent alors une longueur proche.
- **Remplacer le seuil `40rem` par une requête de conteneur** (`@container`). Le titre s’adapterait à la largeur du panneau, et non à celle de l’écran.

## CSS complet prêt à enregistrer

```css
/*
 * Typographie, version 1.1, choisie par Antoine le 5 novembre 2026.
 *
 * Aucune dépendance, aucun import de police, aucune couleur, aucun reset global.
 * Importer ce fichier une fois, puis utiliser .type-title, .type-heading, .type-body, etc.
 * Chaque rôle couple taille, graisse, interligne et approche : ne pas les recomposer.
 * Famille : garder celle du projet en surchargeant --font-sans et --font-mono après cet import.
 * Les rem suivent le réglage du lecteur : ne pas fixer la racine en pixels.
 * Le seuil mobile vit ici : une variable CSS ne fonctionne pas dans une condition @media.
 * Les valeurs brutes vivent seulement dans les primitives ; les consommateurs lisent les rôles.
 * Un titre par écran ; micro et tag servent seulement aux métadonnées et aux mots courts.
 * Chiffres : .type-numeric ; code : .type-code ; emphase : .type-emphasis ; champs : .type-field.
 * Les variables natives de Tailwind 4 lisent les mêmes rôles ; les classes .type-* marchent sans framework.
 * Même échelle en clair et en sombre.
 */

/* ---------- Primitives : les seules valeurs brutes ---------- */
:root {
  /* Familles : la police système d'abord (tailles optiques sur Apple), puis Inter. */
  --primitive-family-system:
    -apple-system, BlinkMacSystemFont, system-ui, "Inter", "Segoe UI",
    sans-serif;
  --primitive-family-mono: "Roboto Mono", "SFMono-Regular", Consolas, monospace;

  /* Tailles en rem : toute l'échelle suit la taille de texte choisie par le lecteur. */
  --primitive-font-11-52: 0.72rem; /* plus petite métadonnée, jamais du texte courant */
  --primitive-font-12: 0.75rem;
  --primitive-font-13: 0.8125rem;
  --primitive-font-14: 0.875rem;
  --primitive-font-15: 0.9375rem;
  --primitive-font-16: 1rem;
  --primitive-font-17: 1.0625rem;
  --primitive-font-19: 1.1875rem;
  --primitive-font-24: 1.5rem;
  --primitive-font-26: 1.625rem; /* titre sur petit écran */
  --primitive-font-28: 1.75rem;
  --primitive-font-44: 2.75rem;

  /* Interlignes : serrés en rem pour l'interface, un rapport pour la lecture. */
  --primitive-leading-14: 0.875rem;
  --primitive-leading-16: 1rem;
  --primitive-leading-18: 1.125rem;
  --primitive-leading-20: 1.25rem;
  --primitive-leading-24: 1.5rem;
  --primitive-leading-28: 1.75rem;
  --primitive-leading-34: 2.125rem;
  --primitive-leading-46: 2.875rem;
  --primitive-leading-reading: 1.75; /* rapport : suit la taille du texte */

  /* Graisses : lecture, titres, chiffres et emphase. 300 sert seulement à Tailwind. */
  --primitive-weight-300: 300;
  --primitive-weight-400: 400;
  --primitive-weight-500: 500;
  --primitive-weight-600: 600;
  --primitive-weight-700: 700;

  /* Approche : négative quand le texte grandit, un peu positive sur le plus petit texte. */
  --primitive-tracking-tightest: -0.03em;
  --primitive-tracking-tighter: -0.02em;
  --primitive-tracking-tight: -0.01em;
  --primitive-tracking-normal: 0em;
  --primitive-tracking-wide: 0.01em;
  --primitive-tracking-wider: 0.05em;

  /* Chiffres de même largeur, pour les valeurs qui changent et les colonnes. */
  --primitive-numeric-tabular: tabular-nums;
  /* Laisse la police choisir sa taille optique quand elle en a. */
  --primitive-optical-auto: auto;
}

/* ---------- Rôles : un usage écrit pour chaque groupe de valeurs ---------- */
:root {
  /* Taille du texte des champs au toucher : 16 px évite le zoom d'iOS. */
  --touch-input-size: var(--primitive-font-16);
  /* Famille de l'interface. */
  --font-sans: var(--primitive-family-system);
  /* Famille du code et des valeurs à aligner chiffre par chiffre. */
  --font-mono: var(--primitive-family-mono);

  /* hero : le chiffre qui répond à l'écran ; un par écran, chiffres tabulaires. */
  --type-hero-size: var(--primitive-font-44);
  --type-hero-leading: var(--primitive-leading-46);
  --type-hero-weight: var(--primitive-weight-600);
  --type-hero-tracking: var(--primitive-tracking-tightest);
  /* title : titre de l'écran ; un par écran. */
  --type-title-size: var(--primitive-font-28);
  --type-title-leading: var(--primitive-leading-34);
  --type-title-weight: var(--primitive-weight-500);
  --type-title-tracking: var(--primitive-tracking-tighter);
  /* figure : chiffre d'une tuile ; chiffres tabulaires. */
  --type-figure-size: var(--primitive-font-24);
  --type-figure-leading: var(--primitive-leading-28);
  --type-figure-weight: var(--primitive-weight-600);
  --type-figure-tracking: var(--primitive-tracking-tighter);
  /* section : titre d'un groupe de cartes, d'une section ou d'un dialogue. */
  --type-section-size: var(--primitive-font-19);
  --type-section-leading: var(--primitive-leading-24);
  --type-section-weight: var(--primitive-weight-500);
  --type-section-tracking: var(--primitive-tracking-tight);
  /* subheading : un niveau à l'intérieur d'une section ; pas un nom de carte. */
  --type-subheading-size: var(--primitive-font-16);
  --type-subheading-leading: var(--primitive-leading-24);
  --type-subheading-weight: var(--primitive-weight-500);
  --type-subheading-tracking: var(--primitive-tracking-tight);
  /* heading : titre d'une carte ou d'un élément de liste. */
  --type-heading-size: var(--primitive-font-15);
  --type-heading-leading: var(--primitive-leading-20);
  --type-heading-weight: var(--primitive-weight-500);
  --type-heading-tracking: var(--primitive-tracking-normal);
  /* body : texte de lecture. */
  --type-body-size: var(--primitive-font-15);
  --type-body-leading: var(--primitive-leading-reading);
  --type-body-weight: var(--primitive-weight-400);
  --type-body-tracking: var(--primitive-tracking-normal);
  /* lede : courte introduction éditoriale ; pas un texte d'interface permanent. */
  --type-lede-size: var(--primitive-font-17);
  --type-lede-leading: var(--primitive-leading-28);
  --type-lede-weight: var(--primitive-weight-400);
  --type-lede-tracking: var(--primitive-tracking-tight);
  /* label : boutons, lignes, onglets et champs. */
  --type-label-size: var(--primitive-font-14);
  --type-label-leading: var(--primitive-leading-20);
  --type-label-weight: var(--primitive-weight-500);
  --type-label-tracking: var(--primitive-tracking-tight);
  /* small : détail sous un titre. */
  --type-small-size: var(--primitive-font-13);
  --type-small-leading: var(--primitive-leading-18);
  --type-small-weight: var(--primitive-weight-400);
  --type-small-tracking: var(--primitive-tracking-normal);
  /* caption : unité, date, axe, aide sous un champ. */
  --type-caption-size: var(--primitive-font-13);
  --type-caption-leading: var(--primitive-leading-18);
  --type-caption-weight: var(--primitive-weight-400);
  --type-caption-tracking: var(--primitive-tracking-wide);
  /* code : lecture du code. */
  --type-code-size: var(--primitive-font-13);
  --type-code-leading: var(--primitive-leading-20);
  --type-code-weight: var(--primitive-weight-400);
  --type-code-tracking: var(--primitive-tracking-normal);
  /* overline : petit surtitre au-dessus d'un titre, en casse de phrase. */
  --type-overline-size: var(--primitive-font-12);
  --type-overline-leading: var(--primitive-leading-18);
  --type-overline-weight: var(--primitive-weight-500);
  --type-overline-tracking: var(--primitive-tracking-wider);
  /* tag : une pastille courte ; jamais une phrase ni un champ. */
  --type-tag-size: var(--primitive-font-12);
  --type-tag-leading: var(--primitive-leading-16);
  --type-tag-weight: var(--primitive-weight-400);
  --type-tag-tracking: var(--primitive-tracking-normal);
  /* micro : valeur sur un graphique ou pastille compacte ; jamais une phrase. */
  --type-micro-size: var(--primitive-font-11-52);
  --type-micro-leading: var(--primitive-leading-14);
  --type-micro-weight: var(--primitive-weight-400);
  --type-micro-tracking: var(--primitive-tracking-wide);
  /* wordmark : le nom compact du projet ; jamais un titre de page. */
  --type-wordmark-size: var(--primitive-font-17);
  --type-wordmark-leading: var(--primitive-leading-20);
  --type-wordmark-weight: var(--primitive-weight-600);
  --type-wordmark-tracking: var(--primitive-tracking-tightest);

  /* Emphase dans le texte ; ne pas mettre tous les titres en gras. */
  --type-emphasis-weight: var(--primitive-weight-600);
  /* Chiffres tabulaires pour les colonnes et les valeurs qui changent. */
  --type-numeric-variant: var(--primitive-numeric-tabular);
  /* Taille optique choisie par la police. */
  --type-optical-sizing: var(--primitive-optical-auto);

  /* Graisses nommées, lues par Tailwind ci-dessous. */
  --weight-light: var(--primitive-weight-300);
  --weight-regular: var(--primitive-weight-400);
  --weight-medium: var(--primitive-weight-500);
  --weight-semibold: var(--primitive-weight-600);
  --weight-bold: var(--primitive-weight-700);
}

/* ---------- Tailwind 4 : variables natives reliées aux rôles, sans compilateur ---------- */
:root {
  --text-hero: var(--type-hero-size);
  --text-hero--line-height: var(--type-hero-leading);
  --text-hero--font-weight: var(--type-hero-weight);
  --text-hero--letter-spacing: var(--type-hero-tracking);
  --text-title: var(--type-title-size);
  --text-title--line-height: var(--type-title-leading);
  --text-title--font-weight: var(--type-title-weight);
  --text-title--letter-spacing: var(--type-title-tracking);
  --text-figure: var(--type-figure-size);
  --text-figure--line-height: var(--type-figure-leading);
  --text-figure--font-weight: var(--type-figure-weight);
  --text-figure--letter-spacing: var(--type-figure-tracking);
  --text-section: var(--type-section-size);
  --text-section--line-height: var(--type-section-leading);
  --text-section--font-weight: var(--type-section-weight);
  --text-section--letter-spacing: var(--type-section-tracking);
  --text-subheading: var(--type-subheading-size);
  --text-subheading--line-height: var(--type-subheading-leading);
  --text-subheading--font-weight: var(--type-subheading-weight);
  --text-subheading--letter-spacing: var(--type-subheading-tracking);
  --text-heading: var(--type-heading-size);
  --text-heading--line-height: var(--type-heading-leading);
  --text-heading--font-weight: var(--type-heading-weight);
  --text-heading--letter-spacing: var(--type-heading-tracking);
  --text-body: var(--type-body-size);
  --text-body--line-height: var(--type-body-leading);
  --text-body--font-weight: var(--type-body-weight);
  --text-body--letter-spacing: var(--type-body-tracking);
  --text-lede: var(--type-lede-size);
  --text-lede--line-height: var(--type-lede-leading);
  --text-lede--font-weight: var(--type-lede-weight);
  --text-lede--letter-spacing: var(--type-lede-tracking);
  --text-label: var(--type-label-size);
  --text-label--line-height: var(--type-label-leading);
  --text-label--font-weight: var(--type-label-weight);
  --text-label--letter-spacing: var(--type-label-tracking);
  --text-small: var(--type-small-size);
  --text-small--line-height: var(--type-small-leading);
  --text-small--font-weight: var(--type-small-weight);
  --text-small--letter-spacing: var(--type-small-tracking);
  --text-caption: var(--type-caption-size);
  --text-caption--line-height: var(--type-caption-leading);
  --text-caption--font-weight: var(--type-caption-weight);
  --text-caption--letter-spacing: var(--type-caption-tracking);
  --text-code: var(--type-code-size);
  --text-code--line-height: var(--type-code-leading);
  --text-code--font-weight: var(--type-code-weight);
  --text-code--letter-spacing: var(--type-code-tracking);
  --text-overline: var(--type-overline-size);
  --text-overline--line-height: var(--type-overline-leading);
  --text-overline--font-weight: var(--type-overline-weight);
  --text-overline--letter-spacing: var(--type-overline-tracking);
  --text-tag: var(--type-tag-size);
  --text-tag--line-height: var(--type-tag-leading);
  --text-tag--font-weight: var(--type-tag-weight);
  --text-tag--letter-spacing: var(--type-tag-tracking);
  --text-micro: var(--type-micro-size);
  --text-micro--line-height: var(--type-micro-leading);
  --text-micro--font-weight: var(--type-micro-weight);
  --text-micro--letter-spacing: var(--type-micro-tracking);
  --text-wordmark: var(--type-wordmark-size);
  --text-wordmark--line-height: var(--type-wordmark-leading);
  --text-wordmark--font-weight: var(--type-wordmark-weight);
  --text-wordmark--letter-spacing: var(--type-wordmark-tracking);

  /* Échelle par défaut de Tailwind, rabattue sur les rôles. */
  --text-xs: var(--type-caption-size);
  --text-xs--line-height: var(--type-caption-leading);
  --text-sm: var(--type-label-size);
  --text-sm--line-height: var(--type-label-leading);
  --text-base: var(--type-body-size);
  --text-base--line-height: var(--type-body-leading);
  --text-lg: var(--type-section-size);
  --text-lg--line-height: var(--type-section-leading);
  --text-xl: var(--type-section-size);
  --text-xl--line-height: var(--type-section-leading);
  --text-2xl: var(--type-figure-size);
  --text-2xl--line-height: var(--type-figure-leading);
  --text-3xl: var(--type-title-size);
  --text-3xl--line-height: var(--type-title-leading);

  /* Graisses de Tailwind, sans valeur indépendante. */
  --font-weight-light: var(--weight-light);
  --font-weight-normal: var(--weight-regular);
  --font-weight-medium: var(--weight-medium);
  --font-weight-semibold: var(--weight-semibold);
  --font-weight-bold: var(--weight-bold);
}

/* Titre sur écran étroit ; les champs gardent leur propre taille tactile. */
@media (max-width: 40rem) {
  :root {
    --type-title-size: var(--primitive-font-26);
    --type-title-leading: var(--primitive-leading-34);
  }
}

/* ---------- Consommateurs : une classe par rôle ---------- */
.type-hero {
  font-family: var(--font-sans);
  font-size: var(--type-hero-size);
  line-height: var(--type-hero-leading);
  font-weight: var(--type-hero-weight);
  letter-spacing: var(--type-hero-tracking);
  font-variant-numeric: var(--type-numeric-variant);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-title {
  font-family: var(--font-sans);
  font-size: var(--type-title-size);
  line-height: var(--type-title-leading);
  font-weight: var(--type-title-weight);
  letter-spacing: var(--type-title-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-figure {
  font-family: var(--font-sans);
  font-size: var(--type-figure-size);
  line-height: var(--type-figure-leading);
  font-weight: var(--type-figure-weight);
  letter-spacing: var(--type-figure-tracking);
  font-variant-numeric: var(--type-numeric-variant);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-section {
  font-family: var(--font-sans);
  font-size: var(--type-section-size);
  line-height: var(--type-section-leading);
  font-weight: var(--type-section-weight);
  letter-spacing: var(--type-section-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-subheading {
  font-family: var(--font-sans);
  font-size: var(--type-subheading-size);
  line-height: var(--type-subheading-leading);
  font-weight: var(--type-subheading-weight);
  letter-spacing: var(--type-subheading-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-heading {
  font-family: var(--font-sans);
  font-size: var(--type-heading-size);
  line-height: var(--type-heading-leading);
  font-weight: var(--type-heading-weight);
  letter-spacing: var(--type-heading-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-body {
  font-family: var(--font-sans);
  font-size: var(--type-body-size);
  line-height: var(--type-body-leading);
  font-weight: var(--type-body-weight);
  letter-spacing: var(--type-body-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-lede {
  font-family: var(--font-sans);
  font-size: var(--type-lede-size);
  line-height: var(--type-lede-leading);
  font-weight: var(--type-lede-weight);
  letter-spacing: var(--type-lede-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-label {
  font-family: var(--font-sans);
  font-size: var(--type-label-size);
  line-height: var(--type-label-leading);
  font-weight: var(--type-label-weight);
  letter-spacing: var(--type-label-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-small {
  font-family: var(--font-sans);
  font-size: var(--type-small-size);
  line-height: var(--type-small-leading);
  font-weight: var(--type-small-weight);
  letter-spacing: var(--type-small-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-caption {
  font-family: var(--font-sans);
  font-size: var(--type-caption-size);
  line-height: var(--type-caption-leading);
  font-weight: var(--type-caption-weight);
  letter-spacing: var(--type-caption-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-code {
  font-family: var(--font-mono);
  font-size: var(--type-code-size);
  line-height: var(--type-code-leading);
  font-weight: var(--type-code-weight);
  letter-spacing: var(--type-code-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-overline {
  font-family: var(--font-sans);
  font-size: var(--type-overline-size);
  line-height: var(--type-overline-leading);
  font-weight: var(--type-overline-weight);
  letter-spacing: var(--type-overline-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-tag {
  font-family: var(--font-sans);
  font-size: var(--type-tag-size);
  line-height: var(--type-tag-leading);
  font-weight: var(--type-tag-weight);
  letter-spacing: var(--type-tag-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-micro {
  font-family: var(--font-sans);
  font-size: var(--type-micro-size);
  line-height: var(--type-micro-leading);
  font-weight: var(--type-micro-weight);
  letter-spacing: var(--type-micro-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-wordmark {
  font-family: var(--font-sans);
  font-size: var(--type-wordmark-size);
  line-height: var(--type-wordmark-leading);
  font-weight: var(--type-wordmark-weight);
  letter-spacing: var(--type-wordmark-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-field {
  font-family: var(--font-sans);
  font-size: var(--type-label-size);
  line-height: var(--type-label-leading);
  font-weight: var(--type-label-weight);
  letter-spacing: var(--type-label-tracking);
  font-optical-sizing: var(--type-optical-sizing);
}

.type-numeric {
  font-variant-numeric: var(--type-numeric-variant);
}

.type-emphasis {
  font-weight: var(--type-emphasis-weight);
}

@media (pointer: coarse) {
  .type-field {
    font-size: var(--touch-input-size);
  }
}
```
