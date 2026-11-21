# Interface romā

Cette extension de bureau est fournie dans le coffre romā. Pour l’installer dans un autre coffre, copie `manifest.json`, `main.js` et `styles.css` dans le dossier `plugins/roma-interface` de la configuration du coffre, puis active **Interface romā** dans Obsidian.

Dans une Base, un clic ordinaire sur un lien vers une fiche Markdown ouvre un tiroir dans le bord droit du volet qui contient la Base. Le tiroir reprend l’espacement et la bordure du thème. Le clic modifié, le menu contextuel et les contrôles de la Base gardent leurs gestes natifs. Dans les cartes et le Kanban, la première propriété visible est le titre. Utilise `link(file.path, file.name)` comme formule de titre pour rendre toute la carte cliquable. Les dispositions de romā utilisent cette formule pour les tâches, le Portfolio et la galerie Design.

Le graphe local et ses onglets restent accessibles dans le panneau droit d’Obsidian, même quand le tiroir est ouvert. **Échap** ferme le tiroir lorsqu’il a le focus. **Ouvrir dans l’éditeur** ouvre la fiche dans le volet d’origine. Le menu contextuel des notes contient aussi **Aperçu à droite**.

Dans **Réglages → Interface romā → Éléments visibles**, coche les éléments de Tasogare à afficher. Les choix s’appliquent dès le premier changement. **Revenir aux réglages du thème** rend la main à Style Settings.

Le tiroir se monte dans le conteneur natif du volet et utilise `MarkdownRenderer`. La détection du clic est limitée aux liens de fichiers rendus dans les Bases du panneau principal. Si Obsidian change leur balisage, le clic natif et la commande **Aperçu à droite** restent disponibles.
