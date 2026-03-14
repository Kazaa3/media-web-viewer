
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Global Variables Preset Audit
# Eingabewerte: Preset-Dateien, Testdateien
# Ausgabewerte: Liste der globalen Variablen und deren Werte
# Testdateien: tests/global_variables_preset.py, preset/*.py
# ERWEITERUNGEN (TODO): [ ] Automatische Korrektur und Setzen von Preset-Werten
# KOMMENTAR: Prüft und listet globale Variablen aus Preset-Dateien für Testzwecke
# VERWENDUNG: python tests/global_variables_preset.py

"""
KATEGORIE:
----------
Global Variables Preset Audit

ZWECK:
------
Prüft und listet globale Variablen aus Preset-Dateien für Testzwecke.

EINGABEWERTE:
-------------
- preset/*.py
- tests/global_variables_preset.py

AUSGABEWERTE:
-------------
- Liste der globalen Variablen und deren Werte

TESTDATEIEN:
------------
- tests/global_variables_preset.py
- preset/*.py

ERWEITERUNGEN (TODO):
---------------------
- [ ] Automatische Korrektur und Setzen von Preset-Werten

VERWENDUNG:
-----------
    python tests/global_variables_preset.py
"""

# Central global variables for Media Web Viewer

APP_NAME = "Media Web Viewer"
DEVELOPER = "kazaa3"
LICENSE = "GPL-3.0"
VERSION = "1.34"  # Update as needed

# Short and long names for app
SHORT_NAME = "dict"
LONG_NAME = "Media Web Player & Library"

# Code name for app
CODE_NAME = "media web viewer"

# Alternative titles for app
ALTERNATIVE_TITLES = [
    "Web Vor Media",
    "Web-Vor-Media",
    "Player",
    "Web Player",
    "Web-Player",
    "Media Player",
    "Media-Player",
    "dict",
    "egasgat",
    "fverknüpft"
]

GLOBAL_VARIABLES = {
    "app_name": APP_NAME,
    "developer": DEVELOPER,
    "license": LICENSE,
    "version": VERSION,
    "short_name": SHORT_NAME,
    "long_name": LONG_NAME,
    "code_name": CODE_NAME,
    "alternative_titles": ALTERNATIVE_TITLES,
}
