# Logbuch: CLI-vEnv-Umgebung & Parser-Pipeline

## Ziel
Dokumentation und Testplan für die CLI-Umgebung (cli.py, run.sh, build_deb.sh) und die Parser-Pipeline (ffprobe, mutagen, mediainfo) im Media Web Viewer.

---

## CLI-vEnv-Umgebung
- Health-Check und Performance-Messung für CLI-Tools
- PID-Erfassung und Logging für CLI-Prozesse
- Fehlerhandling bei CLI-Absturz, Exit-Code, Ressourcenproblemen
- End-to-End-Test: CLI-Start → Health-Check → Performance-Messung → Logsystem/GUI
- Synchronisation und Status-Update zwischen CLI, Backend und Frontend
- Multi-User- und Parallelbetrieb
- Audit-Trail und Nachvollziehbarkeit

**Erfolgskriterien:**
- CLI-Tools laufen stabil und performant
- Health-, Performance- und PID-Daten werden korrekt erfasst und angezeigt
- Fehler und Engpässe werden sauber behandelt und geloggt
- Synchronisation und Nachvollziehbarkeit sind gewährleistet

---

## Parser-Pipeline
- PID-Erfassung und Anzeige für Parser-Prozesse
- Übergabe der PID von Parser-Prozessen an die GUI
- Synchronisation und Logging der Parser-PIDs im globalen Logsystem
- Fehlerhandling bei Parser-Absturz oder Timeout
- End-to-End-Test: Datei einlesen → Parser starten → PID erfassen → Ergebnis und PID in der GUI anzeigen
- Multi-Parser-Integration
- Mit Python 3.14 ist echte Parallelität für Parser-Prozesse endlich möglich (keine GIL-Beschränkung mehr, volle Nutzung    von Multi-Core für Medienanalyse).
**Erfolgskriterien:**

**Erfolgskriterien:**
- Parser-PIDs werden korrekt erfasst, geloggt und in der GUI angezeigt
- Fehler und Timeouts werden sauber im UI und Logsystem behandelt
- Synchronisation und Isolation bleiben auch bei parallelen Parser-Prozessen erhalten

---

## Erfolgskriterien für Parser-vEnv-Trennung
- Parser-vEnv hat eine eigene requirements.txt, nur mit den für Medienanalyse benötigten Tools und Libraries
- Keine Fremd- oder Entwicklungsabhängigkeiten in .venv_parser
- Core-Umgebung übernimmt ausschließlich Logging, Server und API-Handling – keine Parser-Logik
- Parser-Prozesse laufen unabhängig und performant, können parallel gestartet werden
- Ergebnisse und PIDs werden sauber an Core/GUI übergeben und geloggt
- Keine Konflikte oder Performance-Einbrüche durch vermischte Abhängigkeiten
- Architektur ist klar dokumentiert und nachvollziehbar

**Stand:** 12. März 2026

---

## Architektur: Trennung CLI-vEnv und Parser-vEnv
- Die CLI-Umgebung (cli.py, run.sh, build_deb.sh) und die Parser-Pipeline sollten strikt getrennt sein.
- Empfehlung: Eigene venv für Parser-Prozesse (z.B. .venv_parser), um maximale Performance und Isolation zu gewährleisten.
- Die CLI-vEnv läuft idealerweise als eigenständige Umgebung, erreichbar von außen (z.B. via Docker), ohne andere Prozesse zu beeinflussen.
- Parser-vEnv kann für intensive Medienanalyse optimiert werden (eigene requirements, keine Fremdabhängigkeiten).
- Beide Umgebungen laufen unabhängig und können parallel betrieben werden.

**Vorteile:**
- Maximale Isolation und Performance
- Keine Konflikte zwischen CLI- und Parser-Abhängigkeiten
- Flexible Erweiterung und Skalierung (z.B. mehrere Parser-Instanzen)
- Saubere Architektur für Docker- und CI/CD-Integration

---

## Logbuch-Eintrag: Parser-vEnv Requirements
- Eigene requirements.txt für .venv_parser
- Nur benötigte Parser-Tools und Libraries (ffprobe, mutagen, mediainfo, etc.)
- Keine Fremd- oder Entwicklungsabhängigkeiten
- Optimiert für Performance und parallele Verarbeitung
- Dokumentation und Pflege der Parser-Requirements als separater Logbuch-Eintrag

**Stand:** 12. März 2026
