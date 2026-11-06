#!/usr/bin/env python3
"""Vérifie le dépôt Tasogare : ce qu'une machine peut contrôler ne repose pas sur une relecture.

Usage : python3 outils/verifier.py   (code de sortie 1 au moindre défaut)

Contrôles :
1. chaque var(--tasogare-x) est déclaré, et chaque --tasogare-x déclaré sert ;
2. aucun !important dans le thème ni dans les snippets ;
3. aucune couleur hexadécimale hors de la couche 1 (primitives) ;
4. les contrastes des palettes passent (outils/palettes.py) ;
5. les tableaux de docs/couleur-obsidian.md sont ceux que génère outils/palettes.py ;
6. CHANGELOG.md a une section pour la version de manifest.json.
"""
import json
import pathlib
import re
import subprocess
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
THEME = RACINE / "theme.css"
MARQUE_TABLEAUX = "<!-- Généré par `python3 outils/palettes.py --markdown`. Ne pas modifier à la main. -->\n"


def sans_commentaires(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def controles():
    defauts = []
    texte = THEME.read_text(encoding="utf-8")
    css = sans_commentaires(texte)

    # 1. Variables du thème déclarées et utilisées
    declarees = set(re.findall(r"(--tasogare-[a-z0-9-]+)\s*:", css))
    lues = set(re.findall(r"var\((--tasogare-[a-z0-9-]+)[,)]", css))
    defauts += [f"variable lue mais jamais déclarée : {v}" for v in sorted(lues - declarees)]
    defauts += [f"variable déclarée mais jamais lue : {v}" for v in sorted(declarees - lues)]

    # 2. Aucun !important
    for fichier in [THEME, *sorted((RACINE / "snippets").glob("*.css"))]:
        if "!important" in sans_commentaires(fichier.read_text(encoding="utf-8")):
            defauts.append(f"!important dans {fichier.relative_to(RACINE)}")

    # 3. Couleurs en dur seulement dans la couche 1
    couche2 = texte.find("Couche 2 : rôles")
    if couche2 < 0:
        defauts.append("repère « Couche 2 : rôles » introuvable dans theme.css")
    else:
        for ligne, contenu in enumerate(sans_commentaires(texte[couche2:]).splitlines()):
            if re.search(r"#[0-9a-fA-F]{3,8}\b", contenu):
                defauts.append(f"couleur en dur hors de la couche 1 : {contenu.strip()}")

    # 4. Contrastes
    palettes = RACINE / "outils" / "palettes.py"
    r = subprocess.run([sys.executable, "-I", str(palettes)], capture_output=True, text=True)
    if r.returncode != 0:
        defauts.append("outils/palettes.py échoue : " + (r.stderr.strip() or r.stdout.strip().splitlines()[-1]))

    # 5. Tableaux de la doc à jour
    doc = (RACINE / "docs" / "couleur-obsidian.md").read_text(encoding="utf-8")
    if MARQUE_TABLEAUX not in doc:
        defauts.append("docs/couleur-obsidian.md : repère des tableaux générés introuvable")
    else:
        genere = subprocess.run([sys.executable, "-I", str(palettes), "--markdown"], capture_output=True, text=True).stdout
        if doc.split(MARQUE_TABLEAUX, 1)[1].strip() != genere.strip():
            defauts.append("docs/couleur-obsidian.md : tableaux périmés, relancer outils/palettes.py --markdown")

    # 6. Journal de la version
    version = json.loads((RACINE / "manifest.json").read_text(encoding="utf-8"))["version"]
    journal = (RACINE / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(rf"^## {re.escape(version)}$", journal, flags=re.M):
        defauts.append(f"CHANGELOG.md : pas de section « ## {version} »")

    return defauts


if __name__ == "__main__":
    trouves = controles()
    for d in trouves:
        print(f"Défaut : {d}")
    print("Vérification :", "réussie" if not trouves else f"{len(trouves)} défaut(s)")
    sys.exit(1 if trouves else 0)
