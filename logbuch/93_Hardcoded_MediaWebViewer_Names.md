# Hardcoded "MediaWebViewer" Names – Übersicht & ToDo

**Datum:** 14.03.2026
**Autor:** Copilot

## Problem
Der Projektname "MediaWebViewer" ist an vielen Stellen im Code und in der Build-Infrastruktur hartcodiert. Das erschwert spätere Umbenennungen oder eine flexible Parametrisierung.

## Fundstellen (Beispiele)
- build.py, build_system.py (Build-Logik)
- web/app_bottle.py (UI/App-Name)
- .gitignore, MediaWebViewer.spec (Artefakt-/Build-Namen)
- CI/CD-Workflows: .github/workflows/ci-main.yml, ci-artifacts.yml, release.yml (Artefakt- und Release-Namen)
- infra/packaging/specs/MediaWebViewer-*.spec (PyInstaller)

## Risiken
- Umbenennung oder Rebranding ist aufwendig
- Inkonsistente Artefakt-Namen bei zukünftigen Anpassungen
- Keine zentrale Steuerung des Projekt-/Produktnamens

## Empfehlung
- Einführung einer zentralen Variable (z.B. PROJECT_NAME) in Build-Skripten und Workflows
- Parametrisierung von Artefakt- und UI-Namen
- Dokumentation der Fundstellen und Anpassungsschritte

## ToDo
- [ ] Zentrale Variable für Projektname definieren (z.B. in build_system.py, pyproject.toml, .env)
- [ ] Alle Fundstellen auf Variable umstellen
- [ ] Workflows und Spezifikationen anpassen
- [ ] UI/App-Name dynamisch setzen
- [ ] Dokumentation aktualisieren

---

**Hinweis:**
Diese Übersicht dient als Grundlage für eine spätere, konsistente Umstellung auf einen variablen Projektnamen.
