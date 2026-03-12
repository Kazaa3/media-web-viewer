# Logbuch: Paralleler Benchmark für Parser-Pipeline (Python 3.14)

## Ziel
Dokumentation und Testplan für parallele Benchmarks der Parser-Pipeline mit Python 3.14 (ThreadPool/ProcessPool, Multi-Core, keine GIL-Beschränkung).

---

## Testdesign
- Parser laufen parallel auf mehreren Dateien
- Zeitmessung pro Datei und Parser
- Vergleich: Gesamtzeit vs. sequenziell
- Skalierungstest: Anzahl der parallelen Prozesse/Kerne variieren (1, 2, 4, 8, ...)
- Fehlerhandling: Timeouts, Ressourcenkonflikte, Logging
- Visualisierung: Ergebnisse als Tabelle und Diagramm (Pandas, Matplotlib, Seaborn)

---

## Beispielcode
```python
import concurrent.futures
import time

def run_parser(parser_func, path, file_type, settings):
    t0 = time.time()
    try:
        result = parser_func(path, file_type, settings)
        duration = time.time() - t0
        return {"result": result, "duration": duration}
    except Exception as e:
        return {"error": str(e), "duration": time.time() - t0}

with concurrent.futures.ProcessPoolExecutor() as executor:
    futures = [executor.submit(run_parser, parser_func, path, file_type, settings)
               for parser_func, path, file_type, settings in jobs]
    results = [f.result() for f in futures]
```

---

## Schnittstellen in der Architektur

### Übersicht
- Die Architektur des Media Web Viewer ist modular aufgebaut und nutzt klar definierte Schnittstellen zwischen den Komponenten.

### Hauptschnittstellen
1. **Frontend ↔ Backend (Eel-Bridge):**
   - WebSocket-Kommunikation
   - @eel.expose API-Funktionen (z.B. Medienanalyse, Logging, Status)
   - JSON-Serialisierung
2. **Backend ↔ Parser-Pipeline:**
   - Python-Funktionsaufrufe (import, parse, orchestrate)
     - `import`: Lädt Parser-Module (z.B. mutagen_parser, ffprobe_parser)
     - `parse`: Führt die eigentliche Metadaten-Extraktion aus (parse(path, file_type, tags, filename, mode))
     - `orchestrate`: Steuert die Parser-Kette (extract_metadata() in media_parser.py), entscheidet Reihenfolge und Aggregation der Ergebnisse
     - Fehlerhandling und Logging sind integriert
     - Rückgabe: Metadaten, Performance-Daten, Fehler
   - Übergabe von Dateipfaden, Dateitypen, Settings
   - Rückgabe von Metadaten, Fehlern, Performance-Daten
3. **Backend ↔ Datenbank:**
   - SQLite-API (CRUD-Operationen)
   - Speicherung und Abfrage von Medien, Metadaten, Logs
4. **Backend ↔ Systemintegration:**
   - Subprozess-Aufrufe (ffmpeg, mediainfo)
   - Systemdialogs, Dateizugriff, OS-Integration
5. **Backend ↔ Web-GUI (Bottle-API):**
   - HTTP-Routen (z.B. /media/<file>, /cover/<file>)
   - JSON- und Datei-Response
6. **Testumgebung ↔ Komponenten:**
   - pytest, unittest, Mock-Objekte
   - Test-Schnittstellen für Health, Performance, Fehlerhandling

### Dokumentation
- Schnittstellen sind in der Architektur und im Code dokumentiert (main.py, parsers/, db.py, web/, tests/)
- API-Design und Datenformate sind in DOCUMENTATION.md und API.md beschrieben
- Schnittstellen können erweitert und getestet werden (z.B. neue API-Endpunkte, Parser-Plugins)

---

## Saubere Datenbank-Trennung der Umgebungen

### Ziel
- Jede Umgebung (Core, Parser, Testbed, UI, Build) nutzt eine eigene, klar getrennte Datenbank.
- Keine Vermischung von Daten, Logs oder Metadaten zwischen den Umgebungen.

### Umsetzung
- Separate SQLite-Datenbanken pro venv (z.B. media_library_core.db, media_library_parser.db, media_library_testbed.db)
- Eigene Konfigurationsdateien und Pfade für jede Umgebung
- Automatisierte Bereinigung und Migration (cleanup_legacy_databases())
- Zugriff nur über die jeweilige Umgebung (db.py, API)
- Testumgebungen nutzen Mock- oder Testdatenbanken

### Vorteile
- Maximale Isolation und Nachvollziehbarkeit
- Keine Konflikte oder Datenverluste durch parallele Nutzung
- Flexible Erweiterung und Skalierung (z.B. Multi-Standort, Docker)
- Einfache Backup- und Restore-Strategien

### Status
- Datenbank-Trennung ist geplant und teilweise umgesetzt
- Weitere Automatisierung und Validierung erforderlich

---

## Status
- Paralleler Benchmark ist vorbereitet, aber noch nicht vollständig umgesetzt
- Performance-Gewinn und Fehlerhäufigkeit werden nach Umsetzung dokumentiert

**Stand:** 12. März 2026
