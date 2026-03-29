
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Logbuch Header Audit
# Eingabewerte: logbuch markdown files
# Ausgabewerte: Liste fehlender Header/Docstrings
# Testdateien: logbuch/*.md
# ERWEITERUNGEN (TODO): [ ] Automatische Korrektur fehlender Header
# KOMMENTAR: Prüft Style-Guide-konforme Header und Docstrings in Logbuch-Dateien
# VERWENDUNG: python tests/check_logbuch_headers.py

"""
KATEGORIE:
----------
Logbuch Header Audit

ZWECK:
------
Prüft, ob Logbuch-Markdown-Dateien den Style-Guide-konformen Header und bilingualen Docstring enthalten.

EINGABEWERTE:
-------------
- logbuch/*.md

AUSGABEWERTE:
-------------
- Liste der Dateien mit fehlendem Header/Docstring

TESTDATEIEN:
------------
- logbuch/*.md

ERWEITERUNGEN (TODO):
---------------------
- [ ] Automatische Korrektur fehlender Header

VERWENDUNG:
-----------
    python tests/check_logbuch_headers.py
"""

import os
import re

# List of logbuch files (add full paths as needed)
logbuch_files = [
    "logbuch/4_Venv_Konzept_Planung_Umsetzung_Validierung.md",
    "logbuch/52_FFmpeg_Transcoding_Fix_and_Optimization.md",
    "logbuch/54_Build_Recursion_Fix_Monitoring_System.md",
    "logbuch/55_CI_CD_Integration_and_Build_Watchdog.md",
    "logbuch/56_Milestone_2_Modernisierung_Automatisierung.md",
    "logbuch/Digitale_HiFi_Formate_Qobuz_Tidal.md",
    "logbuch/Environment_Split_venv_core_venv_testbed.md",
    "logbuch/Exotic_Formats_NTSC_PAL_Phase4.md",
    "logbuch/Fix_Unicode_Icon_GUI.md",
    "logbuch/Freier_Tab_Fuer_Weiteres.md",
    "logbuch/Hörbuch_GUI_Fix.md",
    "logbuch/ItemType_Category_Map.md",
    "logbuch/Logbuch_CLI_vEnv_Parser_Pipeline.md",
    "logbuch/Logbuch_KI_Log_AI_Anchor.md",
    "logbuch/Logbuch_Kontextfenster_Nutzung.md",
    "logbuch/Logbuch_MKVToolNix.md",
    "logbuch/Logbuch_Session_Management_Automatisierung.md",
    "logbuch/Logbuch_Streaming_Chrome.md",
    "logbuch/Logbuch_Testfaelle_ParserParallelitaet.md",
    "logbuch/Logbuch_UI_Tab_Switch_Keepalive.md",
    "logbuch/ParserPipeline_Haerten.md",
    "logbuch/ParserPipeline_Performance_Visualisierung.md",
    "logbuch/ParserPipeline_Performance.md",
    "logbuch/Player_GUI_Anforderungen.md",
    "logbuch/Plotly_js.md",
    "logbuch/Seaborn_GUI_Integration.md",
    "logbuch/Testplan_PID_Tracking_Session_Abgleich.md",
    # Add more as needed...
]

HEADER_PATTERN = re.compile(r"^#+.*Kategorie.*", re.MULTILINE)
DOCSTRING_PATTERN = re.compile(r'(?i)DE:.*EN:')


def check_header(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read(2048)  # Only read the first 2KB
            return bool(HEADER_PATTERN.search(content)) and bool(DOCSTRING_PATTERN.search(content))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False


def main():
    missing = []
    for file in logbuch_files:
        if not check_header(file):
            missing.append(file)
    if missing:
        print("Logbuch files missing standardized header/docstring:")
        for file in missing:
            print(f" - {file}")
    else:
        print("All listed logbuch files have standardized headers.")

if __name__ == "__main__":
    main()
