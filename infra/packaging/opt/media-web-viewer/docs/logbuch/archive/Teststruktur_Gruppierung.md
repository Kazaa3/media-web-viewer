## Anforderungen: GUI- und Testbilder

Alle Bilder, die für GUI-Tests oder als Cover-Art/Testdaten verwendet werden, dürfen nicht ins Git-Repository gepusht werden.

- Testbilder, Cover-Art, UI-Screenshots und Medien-Dummies gehören in einen eigenen Ordner (z.B. tests/assets/ oder tests/data/).
- Der Ordner muss in .gitignore eingetragen werden.
- Nur Metadaten, Pfade oder Mock-Referenzen werden versioniert.
- CI/CD kann die Testdaten bei Bedarf dynamisch bereitstellen (z.B. Download aus Artefakt-Storage).

**Empfohlene .gitignore-Regel:**
```
tests/assets/
tests/data/
```

---
# Teststruktur & Gruppierung

## Ziel
Tests werden nach Technologie, Schwierigkeitsgrad und Kategorie gruppiert, um Übersicht, Wartbarkeit und gezielte Ausführung zu verbessern.

## Struktur

- `tests/tech/` – Technologie-spezifische Tests (z.B. FFmpeg, VLC, Mutagen)
- `tests/basic/` – Basistests (Schnelltests, Smoke-Tests, Kernfunktionalität)
- `tests/advanced/` – Advanced-Tests (Komplexe Szenarien, Integration, Performance)
- `tests/category/` – Tests nach Kategorie (z.B. Audio, Video, Playlist, UI)
- `tests/iso/` – Langlaufende/ISO-Tests (z.B. Medien-ISO, DVD, Blu-ray)

## Vorteile
- Schnellere Testauswahl und gezielte Ausführung
- Trennung von schnellen und langlaufenden Tests
- Bessere Wartbarkeit und Erweiterbarkeit
- Ermöglicht parallele und selektive Testausführung (z.B. nur basic oder nur tech)

## Beispiel
```bash
pytest tests/basic/
pytest tests/tech/
pytest tests/iso/ --maxfail=1
```


## Fachliche Details: Testgliederung

### Testbed

Das Testbed sollte modular aufgebaut sein und folgende Bereiche abdecken:

- Python-Umgebung (venv, venv_core, conda)
- Eel (Backend-Frontend-Kommunikation)
- Bottle (API, Routing)
- WebSocket (Echtzeit-Kommunikation)
- Session (Benutzer- und UI-Sessions)
- UI (Frontend-Tests, Rendering, Interaktion)
- Parser (Medienparser, Format-Erkennung)
- DB (Datenbank, SQLite)
- Logging (Logik, Fehlerbehandlung)

Jeder Bereich kann eigene Setup/Teardown-Logik und Fixtures haben.

### Selenium

Selenium-Tests sollten separat gehalten werden und folgende Aspekte abdecken:

- UI-Interaktion (Klicks, Eingaben, Navigation)
- End-to-End-Tests (gesamter Workflow)
- Modale Dialoge, Popups
- Session-Handling im Browser
- Medien-Playback und Fehlerfälle

Selenium-Tests können nach UI-Komponenten, Seiten und Szenarien gegliedert werden.

---

**Letzte Änderung:** 12. März 2026

- Advanced- und ISO-Tests laufen nur bei Nightly-Builds oder expliziten Triggern.
- UI/Selenium-Tests werden separat getriggert (z.B. nach UI-Änderungen).
- Testauswahl kann über Tags, Marker oder Ordnerstruktur erfolgen:
	- pytest -m "basic or tech"
	- pytest tests/advanced/ --nightly
	- pytest tests/iso/ --longrun
- CI/CD-Workflow (z.B. GitHub Actions, GitLab CI) steuert die Testmatrix.
- Ergebnisse werden nach Testgruppe aggregiert und reportet.

---

**Letzte Änderung:** 12. März 2026