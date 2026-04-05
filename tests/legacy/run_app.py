###############################################################################
# Kategorie: Application Launcher Test
# Eingabewerte: main.py
# Ausgabewerte: Application startup (subprocess)
# Testdateien: main.py
# Kommentar: Startet main.py als subprocess (einfacher App-Launcher für Test-Zwecke).
###############################################################################
"""
Application Launcher Test (DE/EN)
===============================

DE:
Startet main.py als Subprozess für Testzwecke.

EN:
Launches main.py as a subprocess for testing purposes.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import sys
import subprocess

print("Starting app...")
p = subprocess.Popen([sys.executable, "src/core/main.py"])
p.wait()
