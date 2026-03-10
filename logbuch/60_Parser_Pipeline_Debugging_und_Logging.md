<!-- Category: debugging -->
<!-- Title_DE: Parser-Pipeline Debugging und Logging-Überarbeitung -->
<!-- Title_EN: Parser Pipeline Debugging and Logging Overhaul -->
<!-- Summary_DE: Überarbeitung der gesamten Parser-Pipeline mit Fokus auf Logging, Debugging und modularer Erweiterbarkeit. -->
<!-- Summary_EN: Complete overhaul of the parser pipeline with focus on logging, debugging, and modular extensibility. -->
<!-- Status: in-progress -->
<!-- Date: 2026-03-10 -->

# Parser-Pipeline Debugging und Logging-Überarbeitung

## Ziel
Die Parser-Pipeline soll vollständig modular, nachvollziehbar und robust werden. Jeder Parser-Schritt (ffprobe, python-ebml, mkvparse, enzyme, pycdlib, pymkv etc.) wird optional und mit Logging/Debugging-Hooks versehen.

## Umsetzung
- Integration aller relevanten Parser als optionale Pipeline-Schritte.
- Logging für jeden Schritt: Kontext, Input, Output, Fehler, Performance.
- Debug-Flags für gezielte Aktivierung einzelner Parser und Diagnosen.
- GUI-Konfiguration: Parser-Kette und Debug-Flags steuerbar.
- Fehlerbehandlung: Jeder Parser kann Fehler loggen und überspringen.

## Ergebnis (Stand: in-progress)
- python-ebml als optionaler MKV-Parser integriert.
- mkvparse, enzyme, pycdlib, ffprobe-python, pymkv installiert und bereit zur Integration.
- Logging und Debugging für alle Parser vorbereitet.
- GUI zeigt Parser-Kette und Debug-Flags an.

## Hinweise für Entwickler
- Neue Parser immer als optionale Schritte mit Logging integrieren.
- Debug-Ausgaben nur über das zentrale Logging-System.
- Tests für alle neuen Parser-Schritte im `tests/`-Ordner anlegen.
- Dokumentation im Logbuch fortlaufend ergänzen.

## Nächste Schritte
- Integration von mkvparse, enzyme, pycdlib, ffprobe-python, pymkv als Pipeline-Schritte.
- Erweiterung der Tests und GUI-Konfiguration.
- Abschluss der Logging/Debugging-Überarbeitung.

