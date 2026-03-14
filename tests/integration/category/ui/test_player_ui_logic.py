#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Player UI Logic
# Eingabewerte: web/app.html (Static Content)
# Ausgabewerte: Element-Existenz (bool), Function-Existenz (bool)
# Testdateien: web/app.html
# ERWEITERUNGEN (TODO): [ ] Playlist-Backend Integration testen, [ ] Audio-Event Handler Validierung
# KOMMENTAR: Verifiziert die Existenz und Verknüpfung von Player-Steuerungselementen.
# VERWENDUNG: python3 tests/integration/category/ui/test_player_ui_logic.py

"""
KATEGORIE:
----------
Player UI Logic

ZWECK:
------
Verifiziert die Existenz und korrekte Verknüpfung von Player-Steuerungselementen in der UI.
Prüft auf Shuffle, Repeat, Navigation und Playlist-Tab Komponenten.

EINGABEWERTE:
-------------
- web/app.html (Statischer Inhalt)

AUSGABEWERTE:
-------------
- Element-Existenz (bool)
- Function-Existenz (bool)

TESTDATEIEN:
------------
- web/app.html

ERWEITERUNGEN (TODO):
---------------------
- [ ] Playlist-Backend Integration testen
- [ ] Audio-Event Handler Validierung

VERWENDUNG:
-----------
    python3 tests/integration/category/ui/test_player_ui_logic.py
"""

class TestPlayerUILogic(unittest.TestCase):
    def setUp(self):
        self.app_html_path = Path(__file__).parents[4] / "web" / "app.html"
        with open(self.app_html_path, "r", encoding="utf-8") as f:
            self.content = f.read()

    def test_shuffle_button_exists(self):
        self.assertIn('id="btn-shuffle"', self.content)
        self.assertIn('onclick="toggleShuffle()"', self.content)

    def test_repeat_button_exists(self):
        self.assertIn('id="btn-repeat"', self.content)
        self.assertIn('onclick="toggleRepeat()"', self.content)

    def test_navigation_buttons_exist(self):
        self.assertIn('onclick="playPrev()"', self.content)
        self.assertIn('onclick="playNext()"', self.content)

    def test_playlist_tab_exists(self):
        self.assertIn('onclick="switchTab(\'playlist\'', self.content)
        self.assertIn('id="playlist-tab"', self.content)
        self.assertIn('id="playlist-list"', self.content)

    def test_js_functions_implemented(self):
        self.assertIn('function toggleShuffle()', self.content)
        self.assertIn('function toggleRepeat()', self.content)
        self.assertIn('function playNext()', self.content)
        self.assertIn('function playPrev()', self.content)
        self.assertIn('function renderPlaylist()', self.content)

    def test_autoplay_listener_exists(self):
        self.assertIn('currentPlayer.onended', self.content)

if __name__ == "__main__":
    unittest.main()
