# Logbuch-Idee: Interaktive Konsole & Venv-Auswahl

## Idee
Eine interaktive Konsolenfunktion, die es ermöglicht, direkt im Terminal zwischen verschiedenen Python-venvs zu wechseln und projektbezogene Kommandos auszuführen.

## Konzept
- **Interaktive Konsole:**
  - Startet im Projektverzeichnis und bietet eine Eingabeaufforderung für projektbezogene Kommandos (z.B. build, test, lint, run, audit).
  - Zeigt Statusinformationen zu aktiver venv, Python-Version, installierten Paketen und Umgebungsvariablen.
- **Venv-Auswahl:**
  - Listet alle im Projekt gefundenen venvs (z.B. .venv_dev, .venv_build, .venv_core).
  - Ermöglicht das Umschalten der aktiven venv per Auswahlmenü oder Befehl.
  - Optional: Automatische Aktivierung der empfohlenen venv für bestimmte Tasks (z.B. build vs. dev).

## Umsetzungsideen
- Python-Skript mit Prompt-Toolkit oder cmd2 für komfortable CLI.
- Integration in bestehende Management-Skripte (z.B. build_system.py, logbook_manager.py).
- Erweiterbar um weitere Umgebungsfeatures (z.B. Anzeige von Pip/Conda-Umgebungen, direkte Paketinstallation).

## Status
Idee eingetragen – Bewertung und Design offen.

## Stand
13. März 2026
