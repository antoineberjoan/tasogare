#!/usr/bin/env python3
"""Lit les palettes dans theme.css, vérifie leurs contrastes (WCAG 2.x) et génère leurs tableaux.

Usage :
    python3 outils/palettes.py              # vérifie ; code de sortie 1 au premier défaut
    python3 outils/palettes.py --markdown   # imprime les tableaux pour docs/couleur-obsidian.md

theme.css reste la seule source : ce script ne contient aucune couleur.
Il échoue, avec un message, si une palette de Style Settings n'a pas ses deux modes,
si une valeur n'est pas une couleur hexadécimale à 6 chiffres, si --accent-h/s/l ne
correspond pas à l'accent, ou si un contraste passe sous son seuil.
"""
import colorsys
import pathlib
import re
import sys

THEME = pathlib.Path(__file__).resolve().parent.parent / "theme.css"

# Un bloc de palette : .theme-light { … }, .theme-dark.tasogare-the { … }, etc.
# Un sélecteur précédé d'une virgule (le bloc des rôles) n'est pas une palette.
BLOC = re.compile(r"(?<!,\n)^\.theme-(light|dark)(?:\.tasogare-([a-z]+))?\s*\{(.*?)^\}", re.S | re.M)
VARIABLE = re.compile(r"--tasogare-([a-z0-9-]+):\s*([^;]+);")
# Les noms affichés viennent des options de Style Settings, dans le même fichier.
OPTION = re.compile(r"label: (.+)\n\s+value: tasogare-([a-z]+)")
MODES = {"light": "clair", "dark": "sombre"}

# (texte, fond, minimum, usage)
CONTROLES = [
    ("encre", "carte", 7, "texte courant"),
    ("encre", "cadre", 4.5, "texte sur le cadre"),
    ("encre-moyenne", "cadre", 4.5, "texte secondaire sur le cadre"),
    ("encre-moyenne", "carte", 4.5, "texte secondaire sur la carte"),
    ("encre-pale", "carte", 3, "texte discret (décor, jamais sur le cadre)"),
    ("accent", "carte", 4.5, "liens et titre"),
    ("accent-survol", "carte", 4.5, "lien survolé"),
    ("sur-action", "action", 4.5, "texte des boutons"),
    ("sur-action", "action-survol", 4.5, "bouton survolé"),
    ("coche-marque", "coche", 3, "marque de la coche"),
    ("coche", "carte", 3, "case cochée"),
]
SIGNAUX = ["rouge", "orange", "jaune", "vert", "cyan", "bleu", "violet", "rose"]
EMPLACEMENTS = [
    "cadre", "carte", "creux", "encre", "encre-moyenne", "encre-pale",
    "accent", "accent-survol", "action", "action-survol", "sur-action",
    "coche", "coche-marque", "surlignage", "selection", "recherche",
] + SIGNAUX


class Defaut(Exception):
    """Un défaut du thème : le message dit lequel."""


def lire_noms(texte):
    """Rend {palette: nom affiché}, dans l'ordre des options de Style Settings."""
    noms = {cle: nom.strip() for nom, cle in OPTION.findall(texte)}
    if "crepuscule" not in noms:
        raise Defaut("l'option Style Settings « tasogare-crepuscule » manque")
    return noms


def resoudre(valeur, emplacements, sources, profondeur=0):
    """Remplace chaque var(--tasogare-x) par la valeur de l'emplacement x, sinon de la couleur source x."""
    if profondeur > 10:
        raise Defaut(f"renvoi circulaire : {valeur}")

    def un(m):
        nom = m.group(1)
        if nom in emplacements:
            return resoudre(emplacements[nom], emplacements, sources, profondeur + 1)
        if nom in sources:
            return sources[nom]
        raise Defaut(f"variable inconnue : --tasogare-{nom}")

    return re.sub(r"var\(--tasogare-([a-z0-9-]+)\)", un, valeur.strip())


def lire_palettes(texte, noms):
    """Rend {(palette, mode): {emplacement: valeur résolue}}, chaque palette héritant de Crépuscule."""
    sources = dict(re.findall(r"--tasogare-([a-z0-9-]+):\s*(#[0-9a-fA-F]{6});", texte))
    brut = {}
    for mode, palette, corps in BLOC.findall(texte):
        brut.setdefault((palette or "crepuscule", mode), {}).update(VARIABLE.findall(corps))
    for palette in noms:
        for mode in MODES:
            if (palette, mode) not in brut:
                raise Defaut(f"la palette « {noms[palette]} » n'a pas de bloc pour le mode {MODES[mode]}")
    palettes = {}
    for (palette, mode), valeurs in brut.items():
        fusion = {**brut[("crepuscule", mode)], **valeurs}
        palettes[(palette, mode)] = {cle: resoudre(v, fusion, sources) for cle, v in fusion.items()}
    return palettes


def hexa(valeur, ou):
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", valeur):
        raise Defaut(f"{ou} : « {valeur} » n'est pas une couleur hexadécimale à 6 chiffres")
    return valeur.lower()


def luminance(h):
    def canal(v):
        return v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * canal(r) + 0.7152 * canal(g) + 0.0722 * canal(b)


def contraste(a, b):
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def teinte(h):
    """Rend (teinte en degrés, saturation %, luminosité %) arrondies, comme les écrit le thème."""
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    t, l, s = colorsys.rgb_to_hls(r, g, b)
    return round(t * 360), round(s * 100), round(l * 100)


def verifier(palettes, noms):
    echecs = 0
    for palette, nom in noms.items():
        for mode, libelle in MODES.items():
            c = palettes[(palette, mode)]
            ou = f"{nom} / {libelle}"
            print(f"== {ou}")
            for texte, fond, mini, usage in CONTROLES:
                r = contraste(hexa(c[texte], f"{ou}, {texte}"), hexa(c[fond], f"{ou}, {fond}"))
                ok = r >= mini
                echecs += not ok
                print(f"  {'OK ' if ok else 'NON'} {r:5.2f} (min {mini}) {usage}")
            faible = min((contraste(hexa(c[s], f"{ou}, {s}"), c["carte"]), s) for s in SIGNAUX)
            ok = faible[0] >= 3
            echecs += not ok
            print(f"  {'OK ' if ok else 'NON'} {faible[0]:5.2f} (min 3) signal le plus faible : {faible[1]}")
            attendu = teinte(hexa(c["accent"], f"{ou}, accent"))
            ecrit = tuple(int(c[f"accent-{x}"].rstrip("%")) for x in "hsl")
            ok = ecrit == attendu
            echecs += not ok
            print(f"  {'OK ' if ok else 'NON'} accent-h/s/l {ecrit} {'=' if ok else '≠'} {attendu}")
    print("Échecs :", echecs)
    return echecs


def markdown(palettes, noms):
    for palette, nom in noms.items():
        print(f"### {nom}\n")
        print("| Emplacement | Clair | Sombre |")
        print("| --- | --- | --- |")
        for e in EMPLACEMENTS:
            print(f"| `{e}` | `{palettes[(palette, 'light')][e]}` | `{palettes[(palette, 'dark')][e]}` |")
        print()


def main():
    texte = THEME.read_text(encoding="utf-8")
    try:
        noms = lire_noms(texte)
        palettes = lire_palettes(texte, noms)
        if "--markdown" in sys.argv:
            markdown(palettes, noms)
            return 0
        return 1 if verifier(palettes, noms) else 0
    except Defaut as d:
        print(f"Défaut : {d}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
