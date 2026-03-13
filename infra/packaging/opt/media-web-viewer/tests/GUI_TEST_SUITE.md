# Industry Standard GUI Test Suite

Diese Test-Suite ist darauf ausgelegt, die Benutzeroberfläche von `dict` (Media Web Viewer) automatisiert und robust zu testen.

## Architektur: Page Object Model (POM)

Wir verwenden das Page Object Model, um die Testlogik von den UI-Details zu trennen.
- **tests/pages/**: Enthält Klassen, die einzelne Seiten oder Komponenten repräsentieren.
- **tests/test_*.py**: Enthält die eigentlichen Test-Szenarien.

## Sicherheit & Datenschutz (Industrie-Standard)

1. **Screenshot-Isolierung**: Alle während der Tests erzeugten Bilder werden im Verzeichnis `tests/selenium_artifacts/` gespeichert. Dieses Verzeichnis wird niemals in Git eingecheckt (siehe `.gitignore`), um Urheberrechte an Medien-Inhalten zu schützen.
2. **Umgebungs-Validierung**: Die Tests prüfen vor dem Start, ob die richtige `venv` aktiv ist und ob die Ports (Standard: 8003) frei sind.
3. **Session-Management**: Jeder Testlauf erzwingt eine neue Sitzung (`MWV_FORCE_NEW_SESSION=1`), um Seiteneffekte zu vermeiden.

## Aktueller Fokus: Playlist Steuerung

Die Playlist-Tests prüfen die Integrität der Sortierung (Up/Down) und das Entfernen von Elementen. 
- **Up/Down Bugfix**: Wir überwachen die DOM-Verschiebungen und die Persistenz im Backend.

## Ausführung

```bash
# Einzelner Test
python3 tests/test_playlist_ui.py

# Gesamte GUI Suite
python3 tests/run_gui_tests.py
```
