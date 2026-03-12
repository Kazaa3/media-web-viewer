#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Application Launcher Test
# Eingabewerte: main.py
# Ausgabewerte: Application startup (subprocess)
# Testdateien: main.py
# Kommentar: Startet main.py als subprocess (einfacher App-Launcher für Test-Zwecke).
import sys
import subprocess

print("Starting app...")
p = subprocess.Popen([sys.executable, "src.core.main.py"])
p.wait()
