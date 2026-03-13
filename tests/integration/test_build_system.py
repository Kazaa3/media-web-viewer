# =============================================================================
# Kategorie: Build System Test
# Eingabewerte: BuildSystem-Objekt, Version, Umgebung
# Ausgabewerte: Build-Status, Banner, Environment-Check
# Testdateien: test_build_system.py
# Kommentar: Testet die BuildSystem-Klasse und ihre Methoden.
# Startbefehl: pytest tests/test_build_system.py -v
# =============================================================================
"""
Build System Test Suite (DE/EN)
===============================

DE:
Testet die BuildSystem-Klasse, Versionserkennung, Banner-Ausgabe und Environment-Checks.

EN:
Tests the BuildSystem class, version detection, banner output, and environment checks.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import unittest
from infra.build_system import BuildSystem

class TestBuildSystem(unittest.TestCase):
    """
    DE:
    Testet die BuildSystem-Klasse und deren Methoden.

    EN:
    Tests the BuildSystem class and its methods.
    """
    def setUp(self):
        """
        DE:
        Initialisiert das BuildSystem-Objekt für jeden Test.

        EN:
        Initializes the BuildSystem object for each test.
        """
        self.bs = BuildSystem()

    def test_read_version(self):
        """
        DE:
        Testet das Auslesen der Version.

        EN:
        Tests reading the version.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Version kein String ist.
        """
        version = self.bs._read_version()
        self.assertIsInstance(version, str)

    def test_print_banner(self):
        """
        DE:
        Testet die Banner-Ausgabe.

        EN:
        Tests banner output.
        Returns:
            Keine.
        Raises:
            Keine.
        """
        self.bs._print_banner("Test Banner")

    def test_check_environment(self):
        """
        DE:
        Testet die Environment-Prüfung.

        EN:
        Tests environment check.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Ergebnis kein bool ist.
        """
        result = self.bs.check_environment()
        self.assertIsInstance(result, bool)

    def test_check_browser_available(self):
        """
        DE:
        Testet die Browser-Verfügbarkeitsprüfung.

        EN:
        Tests browser availability check.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Ergebnis kein bool ist.
        """
        result = self.bs._check_browser_available()
        self.assertIsInstance(result, bool)

if __name__ == '__main__':
    unittest.main()
