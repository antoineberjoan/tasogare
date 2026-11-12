"""Vérifie Tasogare dans un coffre isolé et compare ses interactions avec Minimal.

Prérequis : Obsidian ouvert avec CDP, interface anglaise, zéro plugin communautaire.
Les notes de test sont créées puis supprimées ; les autres fichiers Markdown restent identiques.
"""

from contextlib import contextmanager
from pathlib import Path
import argparse
import hashlib
import json
import shutil

from playwright.sync_api import sync_playwright

FOLDER = "Notes/Test Tasogare"
DATA = FOLDER + "/Données"
BASE = FOLDER + "/Comparaison.base"
NOTE = FOLDER + "/Propriétés.md"
BASE_TEXT = """filters:
  and:
    - file.inFolder("Notes/Test Tasogare/Données")
    - file.ext == "md"
properties:
  file.name:
    displayName: Fiche
  note.prix:
    displayName: Prix
  note.achete:
    displayName: Acheté
views:
  - type: table
    name: Tableau
    order: [file.name, prix, achete]
    sort:
      - property: file.name
        direction: ASC
  - type: cards
    name: Cartes
    order: [file.name, prix, achete]
  - type: table
    name: Filtrés
    order: [file.name, prix, achete]
    filters: note.achete == true
"""
FIELDS = {
    "type": "Source",
    "domaine": "Connaissance",
    "mots-clés": [
        "Obsidian",
        "Écriture",
        "Une valeur de liste particulièrement longue",
    ],
    "source": "https://obsidian.md/" + "connaissance-transverse-" * 8,
    "Critère de sélection particulièrement important": "Une description longue et éditable. "
    * 8,
    "vide": "",
    "achete": True,
    "prix": 39,
}
NOTE_TEXT = (
    "---\n"
    + "".join(f"{k}: {json.dumps(v, ensure_ascii=False)}\n" for k, v in FIELDS.items())
    + "---\n\n# Propriétés\n\n## Une idée lisible\n\nUn paragraphe de référence.\n\n### Un détail\n\nTexte et `code`.\n"
)


def hashes(vault):
    return {
        str(p.relative_to(vault)): hashlib.sha256(p.read_bytes()).hexdigest()
        for p in vault.rglob("*.md")
    }


class Obsidian:
    def __init__(self, page, vault, output):
        self.page = page
        self.vault = vault
        self.output = output

    def open(self, file, view=None):
        kind = "bases" if file.endswith(".base") else "markdown"
        state = (
            {"file": file, "viewName": view}
            if view
            else {"file": file, "mode": "preview"}
        )
        self.page.evaluate(
            "async arg => app.workspace.getMostRecentLeaf().setViewState(arg)",
            {"type": kind, "state": state},
        )
        if kind == "markdown":
            self.page.wait_for_selector(".mod-root .markdown-preview-view")

    def theme(self, name):
        self.page.evaluate(
            """async name => {
                app.customCss.setTheme(name);
                await app.customCss.loadTheme();
            }""",
            name,
        )

    def mode(self, name):
        self.page.evaluate(
            "m => {app.vault.setConfig('theme', m === 'dark' ? 'obsidian' : 'moonstone'); app.setTheme()}",
            name,
        )
        self.page.wait_for_function(
            "m => document.body.classList.contains('theme-' + m)", arg=name
        )

    def sides(self, left, right):
        sizes = self.page.evaluate(
            """s => {
            app.workspace.leftSplit[s[0] ? 'expand' : 'collapse']();
            app.workspace.rightSplit[s[1] ? 'expand' : 'collapse']();
            const l = app.workspace.getLayout();
            return {left: s[0] ? l.left.width : 0, right: s[1] ? l.right.width : 0};
        }""",
            [left, right],
        )
        self.page.wait_for_function(
            """s => {
            const l = document.querySelector('.mod-left-split').getBoundingClientRect();
            const r = document.querySelector('.mod-right-split').getBoundingClientRect();
            return Math.abs(l.width - s.left) < 1 && Math.abs(r.width - s.right) < 1;
        }""",
            arg=sizes,
        )

    def count(self, expected):
        self.page.wait_for_function(
            "n => [...document.querySelectorAll('.text-button-label')].some(e => e.getBoundingClientRect().width > 0 && e.textContent.trim() === n + ' result' + (n === 1 ? '' : 's'))",
            arg=expected,
        )

    def switch(self, before, after):
        self.page.locator(".mod-root").get_by_text(before, exact=True).click()
        self.page.get_by_text(after, exact=True).click()
        self.page.wait_for_function(
            "v => app.workspace.getMostRecentLeaf().getViewState().state.viewName === v",
            arg=after,
        )

    def rows(self):
        return self.page.locator(
            ".mod-root .bases-table-container:visible .bases-tr .internal-link"
        ).all_text_contents()

    def cache(self, file, key, value):
        self.page.wait_for_function(
            """arg => {
            const f = app.vault.getAbstractFileByPath(arg.file);
            return app.metadataCache.getFileCache(f)?.frontmatter?.[arg.key] === arg.value;
        }""",
            arg={"file": file, "key": key, "value": value},
        )

    def reset(self):
        self.page.evaluate(
            """async arg => {
            for (const [name, price, bought] of [['Alpha', 10, false], ['Bêta', 20, true], ['Gamma', 30, false]]) {
                const f = app.vault.getAbstractFileByPath(arg.data + '/' + name + '.md');
                const text = ['---', 'prix: ' + price, 'achete: ' + bought, '---', ''].join(String.fromCharCode(10));
                await app.vault.modify(f, text);
            }
            await app.vault.modify(app.vault.getAbstractFileByPath(arg.base), arg.baseText);
            await app.vault.modify(app.vault.getAbstractFileByPath(arg.note), arg.noteText);
        }""",
            {
                "data": DATA,
                "base": BASE,
                "note": NOTE,
                "baseText": BASE_TEXT,
                "noteText": NOTE_TEXT,
            },
        )
        self.cache(DATA + "/Alpha.md", "prix", 10)

    def screenshot(self, name):
        self.page.mouse.move(40, 750)
        self.page.screenshot(path=str(self.output / name))


@contextmanager
def fixture(app):
    page = app.page
    assert page.evaluate("() => app.vault.adapter.basePath") == str(app.vault)
    assert page.evaluate("() => Object.keys(app.plugins.plugins)") == []
    assert not page.evaluate("p => !!app.vault.getAbstractFileByPath(p)", FOLDER), (
        "Le dossier de test existe déjà."
    )
    layout = page.evaluate("() => app.workspace.getLayout()")
    theme = page.evaluate("() => app.vault.getConfig('cssTheme')")
    mode = page.evaluate(
        "() => document.body.classList.contains('theme-dark') ? 'dark' : 'light'"
    )
    before = hashes(app.vault)
    try:
        page.evaluate(
            """async arg => {
            await app.vault.createFolder(arg.folder);
            await app.vault.createFolder(arg.data);
            for (const name of ['Alpha', 'Bêta', 'Gamma']) await app.vault.create(arg.data + '/' + name + '.md', '');
            await app.vault.create(arg.base, arg.baseText);
            await app.vault.create(arg.note, arg.noteText);
            await app.vault.create(arg.wide, arg.wideText);
        }""",
            {
                "folder": FOLDER,
                "data": DATA,
                "base": BASE,
                "baseText": BASE_TEXT,
                "note": NOTE,
                "noteText": NOTE_TEXT,
                "wide": FOLDER + "/Large.md",
                "wideText": "---\ncssclasses: [wide]\n---\n\n![[Comparaison.base#Cartes]]\n",
            },
        )
        app.reset()
        yield
    finally:
        page.keyboard.press("Escape")
        page.evaluate("async l => app.workspace.changeLayout(l)", layout)
        page.evaluate("t => app.customCss.setTheme(t)", theme)
        app.mode(mode)
        page.evaluate(
            """async folder => {
            if (app.vault.getAbstractFileByPath(folder)) await app.vault.adapter.rmdir(folder, true);
            await app.workspace.saveLayout();
        }""",
            FOLDER,
        )
        assert hashes(app.vault) == before, (
            "Un fichier Markdown extérieur au test a changé."
        )


def metrics(page, reference=None):
    return page.evaluate(
        """css => {
            const style = app.customCss.styleEl;
            const previous = style.textContent;
            try {
                if (css !== null) style.textContent = css;
                const s = getComputedStyle(document.body);
                const fonts = ['p', 'h1', 'h2', 'h3', 'code'].map(q => {
                    const e = document.querySelector('.mod-root .markdown-rendered ' + q);
                    const c = getComputedStyle(e);
                    return Object.fromEntries(['fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing'].map(k => [k, c[k]]));
                });
                const colors = Object.fromEntries(['--background-primary', '--background-secondary', '--text-normal', '--text-muted', '--interactive-accent'].map(k => [k, s.getPropertyValue(k).trim()]));
                return {colors, fonts};
            } finally {
                if (css !== null) style.textContent = previous;
            }
        }""",
        reference,
    )


def palettes(app, reference):
    app.open(NOTE)
    app.page.wait_for_selector(".metadata-container")
    results = []
    try:
        for palette in [
            "graphite",
            "crepuscule",
            "gres",
            "the",
            "lac",
            "porte",
            "galet",
        ]:
            app.page.evaluate(
                "p => {for (const c of [...document.body.classList]) if (c.startsWith('tasogare-')) document.body.classList.remove(c); document.body.classList.add('tasogare-' + p)}",
                palette,
            )
            for mode in ["dark", "light"]:
                app.mode(mode)
                current = metrics(app.page)
                if reference:
                    previous = metrics(app.page, reference)
                    assert current == previous, {
                        "palette": palette,
                        "mode": mode,
                        "avant": previous,
                        "apres": current,
                    }
                results.append({"palette": palette, "mode": mode, "mesures": current})
    finally:
        app.page.evaluate(
            "() => {for (const c of [...document.body.classList]) if (c.startsWith('tasogare-')) document.body.classList.remove(c)}"
        )
    return results


def geometry(page):
    return page.evaluate("""() => {
        const r = e => e.getBoundingClientRect().toJSON();
        const visible = q => [...document.querySelectorAll(q)].find(e => e.getBoundingClientRect().width > 0);
        return {main: r(document.querySelector('.mod-root')), card: r(visible('.mod-root .workspace-leaf')),
            right: r(document.querySelector('.mod-right-split')), rightCard: visible('.mod-right-split .workspace-leaf') ? r(visible('.mod-right-split .workspace-leaf')) : null,
            header: r(document.querySelector('.mod-root .workspace-tab-header-container')),
            tab: r(document.querySelector('.mod-root .workspace-tab-header.is-active')),
            overflow: document.documentElement.scrollWidth > innerWidth};
    }""")


def layouts(app):
    results = []
    app.open(NOTE)
    for width in [1136, 900]:
        app.page.set_viewport_size({"width": width, "height": 812})
        for mode in ["dark", "light"]:
            app.mode(mode)
            for left, right in [
                (True, True),
                (True, False),
                (False, True),
                (False, False),
            ]:
                app.sides(left, right)
                g = geometry(app.page)
                assert not g["overflow"], g
                assert abs(g["main"]["right"] - g["card"]["right"] - 10) < 1, g
                assert abs(g["main"]["bottom"] - g["card"]["bottom"] - 10) < 1, g
                assert g["tab"]["top"] >= g["header"]["top"] + 9, g
                assert g["tab"]["bottom"] <= g["header"]["bottom"] - 9, g
                if left:
                    nav = app.page.locator(
                        ".mod-left-split .workspace-tab-header"
                    ).first.bounding_box()
                    assert nav["y"] >= 50, nav
                if right:
                    assert (
                        abs(g["right"]["right"] - g["rightCard"]["right"] - 10) < 1
                    ), g
                    assert abs(g["rightCard"]["top"] - g["card"]["top"]) < 1, g
                results.append(
                    {"largeur": width, "mode": mode, "gauche": left, "droite": right}
                )
    app.page.set_viewport_size({"width": 1136, "height": 812})
    app.sides(True, True)
    return results


def metadata(app):
    app.open(NOTE)
    results = []
    for width in [1136, 900, 760]:
        app.page.set_viewport_size({"width": width, "height": 900})
        for right in [True, False]:
            app.sides(True, right)
            rows = app.page.evaluate("""() => [...document.querySelectorAll('.metadata-container .metadata-property')].map(e => {
                const k = e.querySelector('.metadata-property-key'), v = e.querySelector('.metadata-property-value');
                return {key: e.dataset.propertyKey, row: e.getBoundingClientRect().toJSON(), keyWidth: k.getBoundingClientRect().width, value: v.getBoundingClientRect().toJSON()};
            })""")
            assert rows
            assert all(
                r["keyWidth"] <= r["row"]["width"] / 2 + 1
                and r["value"]["right"] <= r["row"]["right"] + 1
                for r in rows
            ), rows
            assert all(
                b["row"]["top"] >= a["row"]["bottom"] - 1
                for a, b in zip(rows, rows[1:])
            ), rows
            short = [
                r
                for r in rows
                if r["key"] in ["type", "domaine", "mots-clés", "source"]
            ]
            if rows[0]["row"]["width"] > 350:
                assert len({round(r["value"]["x"]) for r in short}) >= 3
            results.append({"largeur": width, "droite": right})
    app.page.set_viewport_size({"width": 1136, "height": 812})
    value = app.page.locator('[data-property-key="type"] .metadata-input-longtext')
    value.fill("Article")
    value.press("Tab")
    app.cache(NOTE, "type", "Article")
    key = app.page.locator('[data-property-key="domaine"] .metadata-property-key-input')
    key.fill("champ temporaire")
    key.press("Enter")
    app.cache(NOTE, "champ temporaire", "Connaissance")
    add = app.page.locator(".metadata-add-button")
    add.focus()
    assert add.evaluate("e => getComputedStyle(e).opacity") == "1"
    for flag, selector in [
        ("tasogare-barre-etat", ".status-bar"),
        (
            "tasogare-actions-fichiers",
            '.workspace-leaf-content[data-type="file-explorer"] .nav-header',
        ),
        ("tasogare-icones-proprietes", ".metadata-property-icon"),
    ]:
        element = app.page.locator(selector).first
        assert element.evaluate("e => getComputedStyle(e).display") == "none"
        app.page.evaluate("c => document.body.classList.add(c)", flag)
        assert element.evaluate("e => getComputedStyle(e).display") != "none"
        app.page.evaluate("c => document.body.classList.remove(c)", flag)
    return {
        "dispositions": results,
        "edition": True,
        "renommage": True,
        "ajout_au_clavier": True,
    }


def interactions(app):
    app.reset()
    app.open(BASE, "Tableau")
    app.sides(True, False)
    app.count(3)
    result = {"initial": app.rows()}
    assert result["initial"] == ["Alpha", "Bêta", "Gamma"]
    app.page.locator(".mod-root").get_by_text("Sort", exact=True).click()
    app.page.locator(".bases-sort-direction").click()
    app.page.get_by_text("Z → A", exact=True).click()
    app.page.keyboard.press("Escape")
    app.page.wait_for_function(
        "() => document.querySelector('.bases-tr .internal-link')?.textContent === 'Gamma'"
    )
    result["tri"] = app.rows()
    app.page.locator(".mod-root").get_by_text("Search", exact=True).click()
    search = app.page.get_by_placeholder("Find...", exact=True)
    search.fill("Alpha")
    app.page.wait_for_function(
        "() => document.querySelectorAll('.bases-tr .internal-link').length === 1"
    )
    result["recherche"] = app.rows()
    search.fill("")
    app.page.keyboard.press("Escape")
    app.switch("Tableau", "Cartes")
    app.count(3)
    result["cartes"] = 3
    app.switch("Cartes", "Filtrés")
    app.count(1)
    result["filtre"] = app.rows()
    app.page.locator(".mod-root").get_by_text("Filter", exact=True).click()
    result["editeur_filtre"] = app.page.locator(".bases-toolbar-menu").inner_text()
    app.page.keyboard.press("Escape")
    app.switch("Filtrés", "Tableau")
    app.count(3)
    row = app.page.locator(".bases-tr").filter(
        has=app.page.locator('.internal-link[data-href="' + DATA + '/Alpha.md"]')
    )
    number = row.locator("input[type=number]")
    number.fill("42")
    number.press("Tab")
    row.locator("input[type=checkbox]").check()
    app.cache(DATA + "/Alpha.md", "prix", 42)
    app.cache(DATA + "/Alpha.md", "achete", True)
    result["edition"] = {"prix": 42, "achete": True}
    app.switch("Tableau", "Cartes")
    app.count(3)
    app.screenshot(
        "bases-" + app.page.evaluate("() => app.vault.getConfig('cssTheme')") + ".png"
    )
    app.page.locator(".bases-cards-item").filter(has_text="Alpha").first.click()
    app.page.wait_for_function(
        "f => app.workspace.getMostRecentLeaf().getViewState().state.file === f",
        arg=DATA + "/Alpha.md",
    )
    result["ouverture"] = True
    return result


def stacked(app):
    layout = app.page.evaluate("() => app.workspace.getLayout()")
    try:
        app.open(NOTE)
        app.page.evaluate(
            """async file => {
            const leaf = app.workspace.getLeaf('tab');
            await leaf.setViewState({type: 'markdown', state: {file, mode: 'preview'}});
            app.workspace.setActiveLeaf(leaf);
            app.commands.executeCommandById('workspace:toggle-stacked-tabs');
        }""",
            DATA + "/Alpha.md",
        )
        app.page.wait_for_function(
            "() => document.querySelector('.mod-root .workspace-tabs').classList.contains('mod-stacked')"
        )
        app.page.wait_for_function(
            "() => [...document.querySelectorAll('.mod-root .workspace-tab-header')].every(e => e.getBoundingClientRect().height > 500)"
        )
        app.screenshot(
            "onglets-empiles-"
            + app.page.evaluate("() => app.vault.getConfig('cssTheme')")
            + ".png"
        )
        return True
    finally:
        app.page.evaluate("async l => app.workspace.changeLayout(l)", layout)


def wide(app):
    app.open(FOLDER + "/Large.md")
    app.sides(False, False)
    app.page.wait_for_selector(".bases-embed.is-loaded:visible")
    result = app.page.evaluate("""() => {
        const content = document.querySelector('.mod-root .markdown-preview-view');
        const sizer = content.querySelector('.markdown-preview-sizer');
        const base = [...content.querySelectorAll('.bases-embed.is-loaded')].find(e => e.getBoundingClientRect().width > 0);
        return {view: content.getBoundingClientRect().width, note: sizer.getBoundingClientRect().width,
                base: base.getBoundingClientRect().width, transform: getComputedStyle(base).transform};
    }""")
    assert result["note"] > 640 and result["base"] > 640, result
    assert result["transform"] == "none", result
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cdp", required=True)
    parser.add_argument("--coffre", required=True, type=Path)
    parser.add_argument("--minimal", required=True, type=Path)
    parser.add_argument("--sortie", required=True, type=Path)
    parser.add_argument(
        "--reference",
        type=Path,
        help="CSS de référence pour comparer les couleurs et la typographie.",
    )
    args = parser.parse_args()
    vault = args.coffre.resolve()
    args.sortie.mkdir(parents=True, exist_ok=True)
    if not (vault / ".obsidian").is_dir():
        parser.error("Le coffre isolé doit contenir .obsidian.")
    manifest = json.loads((args.minimal / "manifest.json").read_text())
    if manifest.get("name") != "Minimal" or not (args.minimal / "theme.css").is_file():
        parser.error("Le chemin de référence doit contenir le thème Minimal.")
    candidate = Path(__file__).resolve().parent.parent / "theme.css"
    if (
        vault / ".obsidian/themes/Tasogare/theme.css"
    ).read_bytes() != candidate.read_bytes():
        parser.error(
            "Installer le CSS de cette révision dans le coffre de test avant de lancer la vérification."
        )
    report = {"minimal": manifest["version"], "interactions": {}}
    with sync_playwright() as playwright:
        browser = playwright.chromium.connect_over_cdp(args.cdp)
        page = next(
            p for c in browser.contexts for p in c.pages if "obsidian.md" in p.url
        )
        page.set_default_timeout(8000)
        page.set_viewport_size({"width": 1136, "height": 812})
        page.reload()
        page.wait_for_function("() => window.app?.workspace?.layoutReady")
        assert page.evaluate("() => app.vault.adapter.basePath") == str(vault)
        assert page.evaluate("() => Object.keys(app.plugins.plugins)") == []
        target = vault / ".obsidian/themes/Minimal"
        installed = target.exists()
        try:
            if not installed:
                shutil.copytree(args.minimal, target)
            page.evaluate("async () => app.customCss.readThemes()")
            app = Obsidian(page, vault, args.sortie)
            report["user_agent"] = page.evaluate("() => navigator.userAgent")
            with fixture(app):
                app.theme("Tasogare")
                report["palettes"] = palettes(
                    app, args.reference.read_text() if args.reference else None
                )
                report["dispositions"] = layouts(app)
                report["proprietes"] = metadata(app)
                report["largeur"] = wide(app)
                for theme in ["Minimal", "Tasogare"]:
                    app.theme(theme)
                    app.mode("dark")
                    page.set_viewport_size({"width": 1136, "height": 812})
                    report["interactions"][theme] = interactions(app)
                    report["interactions"][theme]["empiles"] = stacked(app)
                assert (
                    report["interactions"]["Minimal"]
                    == report["interactions"]["Tasogare"]
                ), report["interactions"]
        finally:
            if not installed:
                shutil.rmtree(target)
    (args.sortie / "verification.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    )
    print(
        json.dumps(
            {
                "palettes": len(report["palettes"]),
                "dispositions": len(report["dispositions"]),
                "proprietes": report["proprietes"],
                "parite_minimal": True,
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
