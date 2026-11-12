"""Vérifie les contrats du thème avec la bibliothèque standard de Python."""

from pathlib import Path
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
MARKER = "<!-- Généré par `python3 outils/palettes.py --markdown`. Ne pas modifier à la main. -->\n"


def css_rules(css):
    """Feuilles de règles : les blocs @media/@supports contiennent ces feuilles."""
    return re.findall(r"([^{}]+)\{([^{}]*)\}", css)


def check_source(text):
    css = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    errors = []
    declared = set(re.findall(r"(--tasogare-[\w-]+)\s*:", css))
    used = set(re.findall(r"var\(\s*(--tasogare-[\w-]+)\s*[,)]", css))
    errors.extend(f"Variable non déclarée : {name}" for name in sorted(used - declared))
    errors.extend(f"Variable inutilisée : {name}" for name in sorted(declared - used))
    if "!important" in css:
        errors.append(
            "Déclaration !important : les surcharges doivent rester possibles."
        )
    if re.search(r"@import|url\(\s*['\"]?(?:https?:)?//", css, re.I):
        errors.append("Ressource distante : le thème doit fonctionner hors ligne.")
    if "Couche 2 : rôles" not in text:
        return errors + ["Section des rôles absente."]
    roles = text.index("Couche 2 : rôles")
    consumers = re.sub(r"/\*.*?\*/", "", text[roles:], flags=re.S)
    if re.search(r"#[0-9a-f]{3,8}\b|\b(?:rgb|hsl|oklch)\(", consumers, re.I):
        errors.append("Couleur littérale hors des fondations.")
    for value in re.findall(r"(?<![\w-])(?:\d*\.)?\d+(?:px|rem|em|ms)\b", consumers):
        if value not in {"1rem", "1em", "0ms"}:
            errors.append(f"Mesure littérale hors des fondations : {value}")
    for selector, declarations in css_rules(css):
        properties = re.findall(r"(?:^|;)\s*([\w-]+)\s*:", declarations)
        repeated = sorted({name for name in properties if properties.count(name) > 1})
        errors.extend(
            f"Déclaration répétée ({selector.strip()}) : {name}" for name in repeated
        )
        if (
            re.search(
                r"\.metadata-(?:property(?:-key(?:-input)?|-value)?|input-longtext)(?:::[\w-]+)?\s*$",
                selector,
            )
            and ".metadata-container" not in selector
        ):
            errors.append(f"Métadonnées sans portée de note : {selector.strip()}")
    return errors


def main():
    errors = check_source((ROOT / "theme.css").read_text())
    result = subprocess.run(
        [sys.executable, "-I", str(ROOT / "outils/palettes.py")],
        capture_output=True,
        text=True,
    )
    if result.returncode:
        errors.append(result.stderr.strip() or result.stdout.strip())
    generated = subprocess.run(
        [sys.executable, "-I", str(ROOT / "outils/palettes.py"), "--markdown"],
        capture_output=True,
        text=True,
    )
    doc = (ROOT / "docs/couleur-obsidian.md").read_text()
    if MARKER not in doc or doc.split(MARKER, 1)[1].strip() != generated.stdout.strip():
        errors.append("Tableaux de couleur non synchronisés avec les données du thème.")
    version = json.loads((ROOT / "manifest.json").read_text())["version"]
    if not re.search(
        r"^## " + re.escape(version) + r"$", (ROOT / "CHANGELOG.md").read_text(), re.M
    ):
        errors.append("Version du manifeste absente du journal.")
    for error in errors:
        print("Défaut : " + error)
    print("Vérification : " + ("échec" if errors else "réussie"))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
