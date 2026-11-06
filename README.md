# Tasogare

黄昏, tasogare : le crépuscule, en japonais. Un thème Obsidian calme : une carte de note arrondie dans un cadre nu, sans séparateurs, avec un inset unique de 10 px, en clair comme en sombre.

![Tasogare : les six palettes, en clair et en sombre](images/palettes.png)

## Installer

1. Dans Obsidian, ouvre Réglages → Apparence → Thèmes → Gérer.
2. Cherche **Tasogare**, puis choisis Installer et utiliser.
3. Facultatif : installe le plugin communautaire **Style Settings** pour choisir la palette.
4. Règle Apparence → Taille de police sur 15 pour l'échelle typographique exacte.

## Palettes

Six palettes, chacune en clair et en sombre. Elles font le tour du cercle des couleurs : une palette par famille, pour qu'aucune ne double une autre.

- **Crépuscule alpin** (par défaut, violet et rouge) : Cabine rouge `#9E2B25`, Ciel lavande `#6E6BA8`, Alpenglow `#E8A3B4`, Neige d'ombre `#B9B3D6`, Lueur `#F4C66A`, Câble acier `#4A4E5C`, Sapin nuit `#1F2A3A`.
- **Grès rosé** (terre) : Grès rosé `#B98A72`, Chaux `#E6E2DA`, Travertin `#D3C7B2`, Olivier sec `#8C7E5E`, Ombre douce `#B4AEA2`, Argile cuite `#7A5443`, Encre taupe `#3F3832`.
- **Thé vert** (vert) : Matcha vif `#8DB33A`, Noyer usé `#5B3A24`, Céramique noire `#2A2622`, Mousse `#6E7A2C`, Jour pâle `#E9E6DC`, Laiton `#C2A25A`, Lin ardoise `#4A4F55`.
- **Lac profond** (bleu-vert) : Bouée rouge `#D2452B`, Lac profond `#1F5A5C`, Turquoise lac `#3E8A86`, Brume montagne `#7E9590`, Chanvre `#C8AE7E`, Écume `#EEEAE2`, Ponton gris `#6F685E`.
- **Porte bleue** (bleu) : Bleu cobalt `#2347A8`, Mur safran `#E6BE3A`, Bougainvillier `#C2287A`, Terracotta `#C0663E`, Cactus `#5E8B4A`, Zellige `#F0E3BE`, Nuit bleue `#13213F`.
- **Galet noir** (neutre) : Galet noir `#2B2A27`, Plâtre `#C9C4BA`, Lin avoine `#B3A68F`, Porcelaine `#EEEBE5`, Pierre grise `#8E8A80`, Fumée `#5F5B53`, Mousse sèche `#7D7A5E`.

Chaque palette garde un fond neutre ; sa couleur forte va à l'accent, aux boutons et aux signaux. Le titre et les liens portent la couleur de la famille ; quand elle est trop claire ou trop sombre pour du texte, elle est assombrie ou éclaircie à cet emplacement, sans changer de teinte.

Le choix se fait dans Réglages → Style Settings → Tasogare → Palette. Sans le plugin, le thème reste complet, avec Crépuscule alpin.

Chaque palette passe les seuils de contraste WCAG AA (4,5:1 pour les liens et le texte secondaire), et son texte courant atteint au moins 7:1.

## Typographie

Le thème suit la spécification [Typographie 1.1](docs/typographie.md) : titre 28 / 500, h2 19 / 500, texte 15 px avec un interligne de 1,75. La police est Inter, embarquée par Obsidian : rien à installer. Le détail de la correspondance avec les variables d'Obsidian est dans [docs/typographie-obsidian.md](docs/typographie-obsidian.md).

À une taille de police de 15, chaque rôle tombe sur la valeur exacte de la spécification ; une autre valeur agrandit ou réduit toute l'échelle, sans changer ses proportions.

## Design system

Le thème repose sur quatre fondations : couleur, typographie, espace et forme, mouvement. Chacune a une spécification réutilisable et un document qui la relie aux variables d'Obsidian. Le sommaire est dans [docs/README.md](docs/README.md).

Pour vérifier le thème après un changement (variables, couleurs, contrastes, docs) :

```bash
python3 outils/verifier.py
```

## Adapter

- **Couleurs et mesures** : elles vivent dans la couche 1 de `theme.css` (`--tasogare-*`). Une palette remplit les mêmes emplacements (`--tasogare-cadre`, `--tasogare-encre`, `--tasogare-accent`…) ; les règles ne lisent que des rôles.
- **Icônes des propriétés (facultatif)** : le snippet `snippets/tasogare-icones-proprietes.css` donne une icône à une clé de propriété précise (`statut`, `source`…). Copie-le dans le dossier `.obsidian/snippets/` de ton coffre, puis active-le dans Réglages → Apparence → Snippets CSS. Une clé absente garde l'icône de son type.

## Crédits

Le défilement révélé au survol et les filets des fenêtres s'inspirent du thème Border (Akifyss/obsidian-border). La structure des palettes en emplacements s'inspire du thème Minimal (kepano/obsidian-minimal, licence MIT). Les règles de mouvement viennent des skills d'Emil Kowalski (emilkowalski/skill, licence MIT) et de l'article « Using Gestures in Motion » de Jakub Krehel. Certaines règles de hiérarchie, d'alignement et de mouvement composé s'inspirent d'Interface Craft (Josh Puckett), reformulées.

## Licence

MIT, voir `LICENSE`.
