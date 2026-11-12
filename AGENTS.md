# Revue des changements Tasogare

Minimal de Kepano est la référence de comportement Obsidian ; Tasogare conserve ses palettes, sa typographie et ses formes. Ne pas attribuer à Kepano une validation qu’il n’a pas donnée.

Pour chaque modification de présentation :

- lire les règles concernées et les variables natives avant de changer le CSS ;
- préférer les variables d’Obsidian, des sélecteurs peu spécifiques et des styles locaux ; éviter les doublons et les compensations liées à une largeur de sidebar ;
- comparer le comportement avec Minimal sur les mêmes fichiers et la même configuration, sans confondre différences de style et régressions fonctionnelles ;
- pour les Bases, vérifier vues tableau/cartes, tri, filtres, recherche, ouverture des fiches et édition native selon la portée de la modification ; les données ne doivent pas être dupliquées ni réécrites par le thème ;
- pour les onglets et panneaux, vérifier aussi le mode empilé, le repli et le redimensionnement ;
- vérifier le clavier, les contrôles masqués et les fenêtres étroites ;
- préserver les préférences de police et les palettes ; aucun plugin communautaire ne doit devenir obligatoire pour la présentation par défaut ;
- exécuter `python3 outils/verifier.py`, `git diff --check` et les contrôles natifs appropriés dans un coffre isolé ; annoncer la version d’Obsidian, de Minimal et les plateformes réellement testées ;
- une capture réussie, une émulation de plateforme ou des contrôles de variables ne constituent pas à eux seuls une validation de publication. Signaler les limites, notamment Mac et mobile réels.

Ne pas publier une release à la seule suite d’un aperçu visuel. Corriger les régressions confirmées et compléter les tests concernés avant publication. Les instructions explicites de l’utilisateur sur la publication restent prioritaires.
