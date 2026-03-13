
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: GUI Testbed Value Audit
# Eingabewerte: testbed markdown files
# Ausgabewerte: Liste fehlender GUI-Testvariablen/Werte
# Testdateien: logbuch/*.md
# ERWEITERUNGEN (TODO): [ ] Automatische Korrektur fehlender Variablen/Werte
# KOMMENTAR: Prüft Style-Guide-konforme GUI-Testvariablen und Werte in Testbed-Markdown-Dateien
# VERWENDUNG: python tests/check_gui_testbed_values.py

"""
KATEGORIE:
----------
GUI Testbed Value Audit

ZWECK:
------
Prüft, ob Testbed-Markdown-Dateien die Style-Guide-konformen GUI-Testvariablen und Werte enthalten.

EINGABEWERTE:
-------------
- logbuch/*.md

AUSGABEWERTE:
-------------
- Liste der Dateien mit fehlenden GUI-Testvariablen/Werten

TESTDATEIEN:
------------
- logbuch/*.md

ERWEITERUNGEN (TODO):
---------------------
- [ ] Automatische Korrektur fehlender Variablen/Werte

VERWENDUNG:
-----------
    python tests/check_gui_testbed_values.py
"""

import os
import re

# List of relevant testbed markdown files (add full paths as needed)
testbed_files = [
    "logbuch/Testplan_PID_Tracking_Session_Abgleich.md",
    "logbuch/Environment_Split_venv_core_venv_testbed.md",
    # Add more as needed...
]

VARIABLE_PATTERN = re.compile(r"\b(var|variable|Wert|value|GUI|Testbed|testvariable|testwert)\b", re.IGNORECASE)


def check_variables(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            # Check for variable pattern and at least one value assignment
            has_var = bool(VARIABLE_PATTERN.search(content))
            has_assignment = bool(re.search(r"=|:|\d+|true|false", content, re.IGNORECASE))
            return has_var and has_assignment
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def main():
    missing = []
    for file in testbed_files:
        if not check_variables(file):
            missing.append(file)
    if missing:
        print("Testbed markdowns missing GUI test variables/values:")
        for file in missing:
            print(f" - {file}")
    else:
        print("All testbed markdowns contain required GUI test variables and values.")

if __name__ == "__main__":
    main()
