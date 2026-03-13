# Logbuch-Idee: Parser-Trennung & Einzelaufrufbarkeit (Python 3.14 Parallelität)

## Idee
Die einzelnen Parser (z.B. mutagen, pymediainfo, ffprobe, pycdlib, isoparser) sollten als klar getrennte, einzeln aufrufbare Module/Services vorliegen. Ziel ist eine bessere Parallelisierbarkeit und Performance, insbesondere im Hinblick auf die neuen Parallel- und Nebenläufigkeitsfeatures von Python 3.14.

## Konzept
- **Parser-Trennung:**
  - Jeder Parser als eigenständige Python-Funktion oder sogar Subprozess/Service.
  - Klare API für Einzelaufruf (z.B. `parse_with_mutagen(path)`, `parse_with_ffprobe(path)`, ...).
- **Parallelität:**
  - Nutzung von `concurrent.futures`, `asyncio` oder neuen Python 3.14-Features (z.B. Task Groups, Subinterpreters) für echte Parallelverarbeitung.
  - Ermöglicht parallele Metadatenextraktion für große Batches oder komplexe Medien.
- **Vorteile:**
  - Bessere Ressourcenausnutzung (CPU, RAM), weniger Bottlenecks.
  - Einzelparser können gezielt getestet, optimiert und ggf. unabhängig deployed werden.
  - Fehler/Timeouts in einem Parser blockieren nicht den gesamten Pipeline-Run.

## Umsetzungsideen
- Refactoring der `media_parser.py`-Logik in modulare Einzelparser.
- CLI/Script-Interface für gezielten Einzelparser-Run (z.B. `python parse_with_ffprobe.py <file>`).
- Optionale Subprozess-Isolation für speicherintensive Parser.
- Integration in Build- und Audit-Tools für parallele Ausführung.

## Status
Idee eingetragen – Bewertung, Design und Prototyping offen.

## Stand
13. März 2026
