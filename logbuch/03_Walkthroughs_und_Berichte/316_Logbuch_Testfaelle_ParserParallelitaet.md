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
