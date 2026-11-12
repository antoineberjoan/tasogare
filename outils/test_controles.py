"""Régressions des contrôles : syntaxe CSS valide et refus des défauts interdits."""

import unittest

from palettes import Defaut, resoudre
from verifier import check_source

MARKER = "/* Couche 2 : rôles */\n"


class Controles(unittest.TestCase):
    def test_alias_multiligne(self):
        self.assertEqual(
            resoudre("var(\n --tasogare-encre \n)", {"encre": "#123456"}, {}), "#123456"
        )

    def test_alias_inconnu(self):
        with self.assertRaises(Defaut):
            resoudre("var(--tasogare-inconnue)", {}, {})

    def test_alias_circulaire(self):
        with self.assertRaises(Defaut):
            resoudre("var(--tasogare-encre)", {"encre": "var(--tasogare-encre)"}, {})

    def test_usage_multiligne(self):
        css = (
            "body {--tasogare-espace: 2px;}\n"
            + MARKER
            + ".note {padding: var(\n --tasogare-espace \n);}"
        )
        self.assertEqual(check_source(css), [])

    def test_source_interdite(self):
        css = (
            MARKER
            + ".note {color: #123456 !important; background: url(https://example.com/image.png); padding: 42px;}"
        )
        errors = check_source(css)
        for token in [
            "!important",
            "distante",
            "Couleur littérale",
            "Mesure littérale",
        ]:
            self.assertTrue(any(token in e for e in errors), errors)

    def test_declaration_repetee(self):
        errors = check_source(MARKER + ".note {padding: 0; padding: 0;}")
        self.assertTrue(any("répétée" in e for e in errors), errors)

    def test_proprietes_portees(self):
        self.assertTrue(check_source(MARKER + ".metadata-property {flex: none;}"))
        self.assertEqual(
            check_source(
                MARKER + ".metadata-container .metadata-property {flex: none;}"
            ),
            [],
        )


if __name__ == "__main__":
    unittest.main()
