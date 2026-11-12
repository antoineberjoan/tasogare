# Mouvement dans Obsidian

Tasogare reprend la [fondation Mouvement 1.1](mouvement.md) : les gestes fréquents restent immédiats.

Le thème ne crée aucune animation de position. Il fournit deux rôles aux animations natives :

| Variable native        | Valeur                                        |
| ---------------------- | --------------------------------------------- |
| `--anim-duration-fast` | 150 ms                                        |
| `--anim-motion-swing`  | Décélération `cubic-bezier(0.23, 1, 0.32, 1)` |

Le moteur d’Obsidian gère les menus et le repli des panneaux. Aucun survol artificiel n’est superposé aux boutons. Avec la préférence système de réduction des animations, le rôle de durée rapide vaut zéro ; les autres comportements restent gérés par Obsidian.
