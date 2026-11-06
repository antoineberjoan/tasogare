# Mouvement

Version : **1.1**. Décision : **5 novembre 2026**.

Cette spécification définit quand animer, avec quelles durées, quelles courbes et dans quel ordre. Ses règles et ses valeurs viennent des skills d'Emil Kowalski : `animate`, `emil-design-eng`, `choreograph` et `mobile-native` (licence MIT, © 2026 Emil Kowalski, <https://github.com/emilkowalski/skill>). Les règles sont traduites et adaptées ; les courbes et les durées sont reprises telles quelles. Les règles du mouvement composé et des sorties s'inspirent aussi d'Interface Craft (Josh Puckett), reformulées. La section sur les gestes s'appuie sur l'article « Using Gestures in Motion » de Jakub Krehel (<https://jakub.kr/work/motion-gestures>), reformulé.

## Principes

1. **Animer selon la fréquence.** Plus une action revient souvent, moins elle s'anime.
2. **Une fonction nommée par animation.** Sans fonction nommée, pas d'animation (voir la liste plus bas).
3. **Court en interface.** Une animation d'interface reste sous 300 ms.
4. **Jamais `ease-in` sur l'interface.** Elle démarre lentement, au moment précis où l'on regarde.
5. **`transform` et `opacity` d'abord.** Ce sont les deux propriétés que le navigateur anime sans recalculer la page.
6. **Une seule chose mène.** Dans un groupe qui bouge, un élément porte le sens ; les autres le suivent, plus discrets, ou ne bougent pas.
7. **Moins de mouvement ne veut pas dire zéro.** Avec la préférence « réduire les animations », on garde les fondus et les couleurs, on retire les déplacements.

## Faut-il animer ?

| Fréquence de l'action | Décision |
| --- | --- |
| Des centaines de fois par jour, ou au clavier | Pas d'animation |
| Des dizaines de fois par jour (survol, navigation dans une liste) | Retirer, ou réduire à un changement de couleur court |
| Occasionnelle (menu, fenêtre, notification) | Animation standard |
| Rare ou vue une fois (accueil, explication) | Plus de latitude |

## Pourquoi animer ?

Une animation remplit **une** de ces fonctions. Si sa seule raison est « ça fait bien » et qu'on la voit souvent, on ne l'anime pas.

| Fonction | Exemple |
| --- | --- |
| Guider | Une notification sort par où elle est entrée : on comprend où la balayer |
| Signaler un état | Un bouton se transforme pour montrer que l'action a réussi |
| Expliquer | Une animation montre comment marche une fonction |
| Répondre | Un bouton s'enfonce légèrement à l'appui : l'interface a entendu |
| Adoucir | Un élément qui apparaît ou disparaît sans transition semble cassé |

## Durées

| Jeton | Valeur | Usage |
| --- | ---: | --- |
| `--duration-instant` | 0 ms | Action fréquente ou au clavier |
| `--duration-press` | 120 ms | Retour de pression d'un bouton (100–160 ms) |
| `--duration-fast` | 150 ms | Survol, changement de couleur, infobulle (125–200 ms) |
| `--duration-standard` | 200 ms | Menu, liste déroulante (150–250 ms) |
| `--duration-wide` | 300 ms | Fenêtre, tiroir, panneau (jusqu'à 500 ms pour une grande surface) |
| `--duration-explain` | 550 ms | Explication, accueil, page vue une fois (entrées de 0,5 à 0,6 s) |

Une durée peut suivre la distance : un petit déplacement va plus vite qu'un grand. Borner le calcul, par exemple entre 150 et 270 ms.

Une sortie dure environ 60 % de son entrée. Dans une explication ou une vidéo, un mouvement dure de 0,4 à 0,9 s selon la taille de l'objet, et son trajet suit la distance à parcourir.

## Courbes

| Jeton | Valeur | Usage |
| --- | --- | --- |
| `--ease-out` | `cubic-bezier(0.23, 1, 0.32, 1)` | Entrée et sortie ; le choix par défaut |
| `--ease-in-out` | `cubic-bezier(0.77, 0, 0.175, 1)` | Déplacement ou transformation à l'écran |
| `--ease-drawer` | `cubic-bezier(0.32, 0.72, 0, 1)` | Tiroir, à la façon d'iOS |
| `--ease-hover` | `ease` | Changement de couleur au survol |
| `--ease-linear` | `linear` | Mouvement continu (progression, défilement) |

Les courbes intégrées du navigateur (`ease-out` seul) sont trop faibles pour une entrée réfléchie : prendre `--ease-out`. Un ressort convient à un geste qu'on peut interrompre ; son rebond reste entre 0,1 et 0,3, et seulement après un geste qui donne de l'élan.

## Forme d'une entrée

- **Échelle de départ** : 0,95 à 0,97, avec un fondu. Jamais 0.
- **Origine** : l'élément naît de ce qui l'ouvre (un bouton, un mot), pas de son centre. Une fenêtre modale fait exception.
- **Retour de pression** : `scale(0.97)` sur `:active`, en 100 à 160 ms, avec `--ease-out`.
- **Flou** : léger (moins de 20 px) et rare, seulement pour relier les deux états d'un fondu. Jamais sur un texte à lire.
- **Chiffres** : une valeur ne dépasse jamais sa cible. Un ressort qui dépasse affiche un chiffre faux.

## Mouvement composé

Quand un même objet anime plusieurs propriétés :

- **Une propriété principale porte le sens** (par exemple le déplacement). Les autres l'accompagnent.
- **Trois propriétés au plus.** Au-delà, l'œil ne suit plus.
- **Les propriétés secondaires sont plus faibles et finissent avant la principale.** Un fondu se termine avant la fin du déplacement.
- **Transformer plutôt que remplacer.** Quand un objet change d'état, il se transforme (il grandit, il change de forme) au lieu de disparaître pour laisser place à un autre.

## Chorégraphie

Quand plusieurs éléments bougent ensemble :

1. **Donner un rôle à chacun.** Le **meneur** est la chose à remarquer : il bouge en premier et le plus loin. Le **soutien** suit, avec un mouvement plus court. Le **décor** (pastilles, filets) apparaît en fondu, sans déplacement. Le reste ne bouge pas.
2. **Une seule entrée par conteneur.** Si le panneau glisse, son contenu est déjà là. On n'anime pas le parent puis chaque enfant.
3. **Ensemble par défaut.** Deux éléments du même objet ou du même instant partent ensemble. On décale seulement quand l'ordre a un sens.
4. **Décalage court et irrégulier.** De 30 à 80 ms entre deux éléments, pour un total sous 300 ms environ. Des écarts tous égaux paraissent mécaniques : le meneur bouge le plus, le décor le moins.
5. **Jamais de décalage sur une interface fréquente** : menus, palette de commandes, lignes de liste.
6. **Une même famille de temps.** Les animations internes d'un composant partagent sa durée et sa famille de courbe.
7. **Les sorties sont simultanées, plus courtes et plus simples.** Tout part en même temps, par le chemin d'entrée.
8. **Rien ne bloque l'interaction.** Un élément visible est cliquable tout de suite.

## Gestes

Un geste est une action de la main sur l'interface. L'interface lui répond, comme un objet réel répond à la main.

| Geste | Ce qu'il déclenche | Réponse conseillée |
| --- | --- | --- |
| Survol | Le pointeur entre ou sort de l'élément | Un changement de couleur court ; un mouvement seulement avec une souris (voir « Sur téléphone ») |
| Appui | Le pointeur ou la touche Entrée presse puis relâche l'élément | `scale(0.97)` pendant l'appui ; l'appui s'annule si le pointeur s'éloigne trop |
| Glisser | L'élément suit le pointeur | Rester dans son conteneur ; un léger agrandissement pendant le geste |
| Déplacer | Le pointeur bouge de plus de 3 px en restant pressé (curseur, zone qui défile) | Un ressort plutôt qu'une courbe : le mouvement paraît plus naturel |
| Focus | L'élément reçoit le focus au clavier (`:focus-visible`) | Une réponse discrète ; un mouvement ample désoriente au clavier |
| Apparition | L'élément entre dans la zone visible en défilant | Une seule fois, quand la moitié de l'élément est visible ; jamais de flou sur un texte à lire |

- **Un ressort sans rebond par défaut** pour répondre à un geste. Un ressort se recible si le geste change en route ; une courbe repart de zéro.
- **Le clavier compte comme la main** : un appui à la touche Entrée donne la même réponse qu'un clic.
- **`transform`, `clip-path` et `filter`** s'animent sans recalculer la page, en CSS comme en JavaScript.

## Interruption

- Une animation déclenchée souvent est une **transition**, pas des images clés : une transition repart de la valeur en cours si on l'interrompt.
- Relancer une séquence en plein milieu arrête d'abord celle qui joue. Les animations ne s'empilent pas.
- Une infobulle attend un peu avant la première apparition ; les suivantes, dans la même barre, s'ouvrent sans délai.

## Sur téléphone

- Tout survol animé vit sous `@media (hover: hover) and (pointer: fine)`. Sinon, l'effet reste collé après un toucher.
- Le retour de pression part à l'appui (`pointer-down`), pas au relâchement. Ajouter `touch-action: manipulation` aux contrôles.
- Tester selon la capacité (`hover`, `pointer`), jamais selon l'appareil.

## À ne pas faire

| À ne pas faire | À faire |
| --- | --- |
| `transition: all` | Nommer chaque propriété animée |
| Apparaître depuis `scale(0)` | Partir de `scale(0.95)` à `0.97`, avec un fondu |
| `ease-in` sur un élément d'interface | `--ease-out` |
| Animer une action au clavier ou très fréquente | Aucune animation |
| Durée d'interface au-delà de 300 ms sans raison | 150 à 250 ms |
| Popover qui grandit depuis son centre | Origine sur l'élément qui l'ouvre |
| Images clés sur un élément déclenché souvent | Une transition |
| Animer `width`, `height`, `margin`, `top`, `left` | `transform` et `opacity` |
| Survol animé sans condition | `@media (hover: hover) and (pointer: fine)` |
| Oublier « réduire les animations » | Une variante plus douce, pas zéro |
| Tout faire entrer d'un coup | Un décalage de 30 à 80 ms, irrégulier |
| Animer un parent puis chacun de ses enfants | Une seule entrée par conteneur |
| Rebond sur une grande surface | Pas de rebond, sauf après un geste qui donne de l'élan |

## Validation avant adoption

- Chaque animation a une fonction nommée et passe le tableau de fréquence.
- Aucune durée ni courbe écrite à la main hors des jetons.
- Le mouvement est regardé au ralenti, puis image par image.
- On le revoit le lendemain, à froid : les défauts se voient mieux.
- La préférence « réduire les animations » est testée.
- Le survol est vérifié avec une souris, puis au toucher, sur un vrai téléphone.

## Changements depuis la version 1.0

- **Sources** : ajout des skills `choreograph` et `mobile-native` d'Emil Kowalski.
- **Ajouts** : les fonctions d'une animation, la forme d'une entrée (origine, pression, flou, chiffres), le mouvement composé, la durée des sorties et des explications, les gestes, la chorégraphie, l'interruption, le téléphone.
- **Nouveau jeton** : `--duration-explain` (550 ms) et `--motion-press-scale` (0,97).

## CSS complet prêt à enregistrer

```css
/*
 * Mouvement, version 1.1, choisie par Antoine le 5 novembre 2026.
 * D'après Emil Kowalski, skills animate, emil-design-eng, choreograph et mobile-native,
 * licence MIT, © 2026 Emil Kowalski, https://github.com/emilkowalski/skill.
 */
:root {
  --duration-instant: 0ms;
  --duration-press: 120ms;
  --duration-fast: 150ms;
  --duration-standard: 200ms;
  --duration-wide: 300ms;
  --duration-explain: 550ms;

  --ease-out: cubic-bezier(0.23, 1, 0.32, 1);
  --ease-in-out: cubic-bezier(0.77, 0, 0.175, 1);
  --ease-drawer: cubic-bezier(0.32, 0.72, 0, 1);
  --ease-hover: ease;
  --ease-linear: linear;

  /* Amplitude : un léger agrandissement, un petit déplacement, un décalage court. */
  --motion-scale-from: 0.96;
  --motion-press-scale: 0.97;
  --motion-shift: 4px;
  --motion-stagger: 50ms;
}

/* Moins de mouvement : on garde les fondus et les couleurs, on retire les déplacements. */
@media (prefers-reduced-motion: reduce) {
  :root {
    --motion-scale-from: 1;
    --motion-press-scale: 1;
    --motion-shift: 0px;
    --motion-stagger: 0ms;
  }
}

/* Exemple : un bouton qui répond à l'appui. */
.press {
  touch-action: manipulation;
  transition: transform var(--duration-press) var(--ease-out);
}
.press:active {
  transform: scale(var(--motion-press-scale));
}

/* Exemple : un menu qui entre depuis son bouton. */
.menu-enter {
  transform-origin: var(--transform-origin, top left);
  transition:
    opacity var(--duration-standard) var(--ease-out),
    transform var(--duration-standard) var(--ease-out);
}
.menu-enter[data-state="closed"] {
  opacity: 0;
  transform: translateY(calc(var(--motion-shift) * -1)) scale(var(--motion-scale-from));
}

/* Exemple : un survol, seulement avec une souris. */
@media (hover: hover) and (pointer: fine) {
  .row:hover {
    background-color: var(--color-hover);
    transition: background-color var(--duration-fast) var(--ease-hover);
  }
}
```
