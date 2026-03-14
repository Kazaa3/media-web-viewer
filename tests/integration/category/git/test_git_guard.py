#dict - Desktop Media Player and Library Manager v1.34
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Integration Test / Git
# Eingabewerte: Scripts Path, Temp Directory
# Ausgabewerte: Test Results (Success/Failure)
# Testdateien: Generiert temporäre Dateien unterschiedlicher Größe
# KOMMENTAR: Validiert die Funktionalität von git_guard.py.

"""
KATEGORIE: Integration Test / Git
ZWECK: Testet, ob git_guard.py Dateien korrekt nach Größe filtert und warnt/stoppt.
VORAUSSETZUNGEN: scripts/git_guard.py muss existieren.
"""

import unittest
import subprocess
import os
import shutil
import tempfile
from pathlib import Path

class TestGitGuard(unittest.TestCase):
    def setUp(self):
        """Erstellt eine temporäre Testumgebung."""
        self.test_dir = tempfile.mkdtemp()
        self.script_path = os.path.abspath("scripts/git_guard.py")
        
    def tearDown(self):
        """Bereinigt die Testumgebung."""
        shutil.rmtree(self.test_dir)

    def create_file(self, name, size_mb):
        """Erstellt eine Datei mit der angegebenen Größe in MB."""
        path = os.path.join(self.test_dir, name)
        with open(path, "wb") as f:
            f.write(os.urandom(int(size_mb * 1024 * 1024)))
        return path

    def run_guard(self, target_dir):
        """Führt git_guard.py gegen ein Verzeichnis aus."""
        cmd = ["python3", self.script_path, "--dir", target_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result

    def test_small_files_pass(self):
        """Testet, ob kleine Dateien (<50MB) akzeptiert werden."""
        self.create_file("small.txt", 10)
        result = self.run_guard(self.test_dir)
        self.assertEqual(result.returncode, 0)
        self.assertIn("Alle 1 Dateien sind innerhalb der Limits", result.stdout)

    def test_medium_file_warns(self):
        """Testet, ob mittlere Dateien (50-100MB) eine Warnung auslösen, aber den Code 0 liefern."""
        self.create_file("medium.bin", 60)
        result = self.run_guard(self.test_dir)
        self.assertEqual(result.returncode, 0)
        self.assertIn("WARNHINWEIS (Große Dateien)", result.stdout)

    def test_large_file_blocks(self):
        """Testet, ob große Dateien (>100MB) den Commit blockieren (Exit Code 1)."""
        self.create_file("huge.iso", 105)
        result = self.run_guard(self.test_dir)
        self.assertEqual(result.returncode, 1)
        self.assertIn("FEHLER: Dateien überschreiten das GitHub-Limit (100MB)", result.stdout)
        self.assertIn("Commit wird blockiert", result.stdout)

if __name__ == "__main__":
    unittest.main()
