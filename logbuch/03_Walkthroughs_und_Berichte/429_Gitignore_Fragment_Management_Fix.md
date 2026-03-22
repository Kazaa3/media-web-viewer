# Gitignore & Fragment Management Fix

**Datum:** 13.03.2026
**Autor:** Copilot

## Problemstellung
Nach dem Build-Prozess werden Artefakte und temporäre Dateien nicht immer korrekt durch `.gitignore` ausgeschlossen. Auch das Management von Test- und Build-Fragmente ist noch nicht konsistent.

## Analyse
- Mehrfache, teils redundante Einträge für Artefakte, Screenshots, Logs und temporäre Dateien
- Teilweise doppelte oder widersprüchliche Patterns (z.B. mehrfach `__pycache__/`, `*.log`, `*.tmp`)
- Build- und Test-Fragmente werden nicht immer zentral verwaltet oder ausgeschlossen
- Alte Root-Level-Dateien werden nicht immer zuverlässig entfernt

## Lösungsvorschlag
- `.gitignore` aufräumen: doppelte und widersprüchliche Patterns entfernen, zentrale Regeln für Build-, Test- und Debug-Artefakte
- Sicherstellen, dass nach Build/Test keine temporären Dateien im Root oder in nicht vorgesehenen Ordnern verbleiben
- Fragment-Management: Alle temporären und Debug-Fragmente in zentralen, git-ignorierten Ordnern sammeln (z.B. `build/`, `tests/debug_artifacts/`)
- Root-Level nur essentielle Dateien und Ordner zulassen

## ToDos
- `.gitignore` konsolidieren und vereinfachen
- Build- und Testskripte prüfen, ob sie Artefakte korrekt ablegen
- Nach Build/Test: Root und relevante Ordner auf "sauberen" Zustand prüfen
- Dokumentation und Walkthrough ergänzen

## Status
- Analyse und Lösungsansatz dokumentiert
- Nächster Schritt: `.gitignore`- und Skriptanpassungen umsetzen
