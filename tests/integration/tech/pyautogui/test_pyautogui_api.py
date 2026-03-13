#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: PyAutoGUI API Test
# Eingabewerte: main.py, PyAutoGUI
# Ausgabewerte: API-Status, Screen- und Mausdaten
# Testdateien: Keine
# Kommentar: Testet PyAutoGUI-API und Datenrückgabe.
"""
PyAutoGUI API Test Suite (DE/EN)
================================

DE:
Testet die PyAutoGUI-API und prüft Rückgabe von Screen- und Mausdaten.

EN:
Tests the PyAutoGUI API and checks return of screen and mouse data.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import sys
# Ensure main.py and dependencies are importable

import unittest

class TestPyAutoGuiAPI(unittest.TestCase):
    """
    DE:
    Testet die PyAutoGUI-API und deren Rückgabewerte.

    EN:
    Tests PyAutoGUI API and its return values.
    """
    def test_pyautogui_api(self):
        """
        DE:
        Prüft, ob main.test_pyautogui() die erwarteten Daten liefert.

        EN:
        Verifies that main.test_pyautogui() returns expected data.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Daten fehlen oder falsch.
        """
        import src.core.main as main
        result = main.test_pyautogui()
        self.assertIn('status', result)
        self.assertEqual(result['status'], 'ok')
        self.assertIn('screen_size', result)
        self.assertIn('mouse_position', result)
        self.assertIsInstance(result['screen_size'], dict)
        self.assertIsInstance(result['mouse_position'], dict)
        self.assertIn('width', result['screen_size'])
        self.assertIn('height', result['screen_size'])
        self.assertIn('x', result['mouse_position'])
        self.assertIn('y', result['mouse_position'])

if __name__ == '__main__':
    unittest.main()
