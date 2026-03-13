#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: i18n Regression Test / Sync Status
# Eingabewerte: web/i18n.json, web/app.html
# Ausgabewerte: Validierung der Sync-Status i18n Keys und UI-Verwendung
# Testdateien: web/i18n.json, web/app.html
# Kommentar: Verhindert Regressionen beim String sync_offline_no_backend im Sync-Status.

import json
import unittest
from pathlib import Path

class TestSyncI18n(unittest.TestCase):
    """Regression tests for sync status translations and usage."""

    def setUp(self):
        self.root = Path(__file__).parents[3]
        self.i18n_path = self.root / "web" / "i18n.json"
        self.app_html_path = self.root / "web" / "app.html"

        self.i18n = json.loads(self.i18n_path.read_text(encoding="utf-8"))
        self.app_html = self.app_html_path.read_text(encoding="utf-8")

    def test_sync_keys_exist_in_de_and_en(self):
        required_keys = [
            "sync_synchronized",
            "sync_offline_no_backend",
            "sync_connection_lost",
        ]

        for lang in ("de", "en"):
            self.assertIn(lang, self.i18n, f"Missing language block: {lang}")
            for key in required_keys:
                self.assertIn(key, self.i18n[lang], f"Missing i18n key '{key}' in language '{lang}'")
                self.assertTrue(str(self.i18n[lang][key]).strip(), f"Empty value for '{key}' in '{lang}'")

    def test_sync_offline_key_is_used_in_connection_check(self):
        self.assertIn("text.innerText = t('sync_offline_no_backend');", self.app_html)

    def test_translation_function_has_de_fallback(self):
        self.assertIn("if (translations.de && translations.de[key])", self.app_html)

if __name__ == "__main__":
    unittest.main()
