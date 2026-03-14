# Logbuch: Testfälle für Parser-Parallelität (Python 3.14)

## Ziel
Testfälle und Benchmarks zur Messung des Performance-Gewinns durch echte Parallelität (Multi-Core, keine GIL-Beschränkung) in der Parser-Pipeline.

---

## Offene Punkte
- Parallelität ist in den Benchmarks und Tests vorbereitet, aber noch nicht vollständig umgesetzt (ThreadPool/ProcessPool, Multi-Core).
- Bisher werden Parser meist sequenziell getestet.
- Testfälle für parallele Ausführung und Vergleich mit sequenzieller Ausführung fehlen noch.

---

## Testfälle für Parallelität
1. **Sequenzieller Benchmark:**
   - Alle Parser laufen nacheinander auf allen Dateien
   - Zeitmessung pro Datei und Parser
2. **Paralleler Benchmark (ThreadPool/ProcessPool):**
   - Parser laufen parallel auf mehreren Dateien
   - Zeitmessung pro Datei und Parser
   - Vergleich: Gesamtzeit vs. sequenziell
3. **Skalierungstest:**
   - Anzahl der parallelen Prozesse/Kerne variieren (1, 2, 4, 8, ...)
   - Performance-Gewinn und Fehlerhäufigkeit messen
4. **Fehlerhandling im Parallelbetrieb:**
   - Fehler, Timeouts, Ressourcenkonflikte erfassen und loggen
5. **Visualisierung:**
   - Ergebnisse als Tabelle und Diagramm (Pandas, Matplotlib, Seaborn)

---

## Anforderungsmanagement für Parser-Parallelität

### Pflichtanforderungen
- Echte Parallelität (Multi-Core, keine GIL-Beschränkung, Python 3.14)
- Performance-Gewinn messbar und dokumentiert
- Fehlerhandling und Isolation im Parallelbetrieb
- Skalierbarkeit: mehrere Parser-Prozesse gleichzeitig
- Visualisierung der Ergebnisse

### Minimalanforderungen
- Sequenzieller und paralleler Benchmark
- Zeitmessung und Fehlerprotokoll
- Vergleich: Gesamtzeit sequenziell vs. parallel

### Maximalanforderungen
- Dynamische Anpassung der Prozessanzahl (Auto-Scaling)
- Integration mit CI/CD und Docker
- Multi-User- und Batch-Betrieb
- Erweiterbare Visualisierung (Heatmap, Boxplot, Violinplot)
- Automatisierte Regressionstests für Performance

### Optionale Anforderungen
- Ressourcenmanagement (CPU, RAM, IO)
- Priorisierung und Scheduling von Parser-Jobs
- Live-Monitoring und Alerting

---

## Requirements Engineering & Anforderungsmanagement (allgemein)

### Ziel
- Systematische Erfassung, Dokumentation und Pflege aller Anforderungen (funktional, nicht-funktional, technischer Kontext)
- Nachvollziehbarkeit und Priorisierung für Entwicklung, Test und Betrieb

### Vorgehen
1. **Anforderungsquellen:**
   - Stakeholder, Nutzer, Entwickler, Betrieb, Gesetzgebung
2. **Kategorisierung:**
   - Funktionale Anforderungen (Features, Use Cases)
   - Nicht-funktionale Anforderungen (Performance, Sicherheit, Skalierbarkeit, Usability)
   - Technische Anforderungen (Plattform, Schnittstellen, Tools)
3. **Dokumentation:**
   - Logbuch-Einträge, Tickets, User Stories, Spezifikationen
   - Versionierung und Änderungsmanagement
4. **Priorisierung:**
   - Muss-, Soll-, Kann-Anforderungen
   - Business Value, Risiko, Aufwand
5. **Validierung & Verifikation:**
   - Tests, Reviews, Abnahme
   - Traceability (Anforderung → Testfall → Implementierung)
6. **Pflege & Monitoring:**
   - Regelmäßige Überprüfung, Anpassung, Status-Tracking

### Best Practices
- Anforderungen klar, messbar und testbar formulieren
- Änderungen transparent und nachvollziehbar dokumentieren
- Stakeholder regelmäßig einbinden
- Automatisierte Tools für Traceability und Status-Tracking nutzen

---

## Beispielcode für parallele Ausführung
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

## Status
- Parallelität muss noch vollständig implementiert und getestet werden
- Testfälle und Visualisierung sind vorbereitet
- Performance-Gewinn wird nach Umsetzung dokumentiert

**Stand:** 12. März 2026
