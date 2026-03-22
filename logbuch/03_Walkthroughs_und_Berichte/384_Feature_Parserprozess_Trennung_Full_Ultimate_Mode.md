# Logbuch-Eintrag: Parserprozess-Trennung, Full/Ultimate-Mode und Tag-Optionen

**Datum:** 13.03.2026  
**Autor:** Copilot

## Kontext
Im Zuge der Weiterentwicklung der Parser-Architektur im Media Web Viewer wurde das Ziel formuliert, die einzelnen Parserprozesse klar zu trennen, flexible Tag-Optionen zu ermöglichen und die Modi "full" und "ultimate" für maximale Metadatentiefe zu unterstützen. Zusätzlich soll die Persistenz aller relevanten Parser- und Tag-Informationen in der Datenbank sichergestellt werden.

## Motivation
- Bessere Nachvollziehbarkeit und Debuggability durch getrennte Parserprozesse
- Flexible Steuerung, welche Tags und Parser in welchem Modus (Standard, Full, Ultimate) ausgeführt werden
- Optimale Nutzung der Parserkette für verschiedene Anwendungsfälle (z.B. schnelle Analyse vs. vollständige Extraktion)
- Vollständige und konsistente Speicherung aller Metadaten in der Datenbank

## Feature-Beschreibung
- **Parserprozess-Trennung:**
  - Jeder Parser kann einzeln oder in beliebiger Kette ausgeführt werden (z.B. für Tests, Debugging, Parallelisierung).
  - Die Ausführungskette (parser_chain) ist konfigurierbar und kann dynamisch angepasst werden.
- **Full/Ultimate-Mode:**
  - Im "full"-Modus werden zusätzliche, tiefergehende Tags extrahiert (z.B. technical, hidden, vendor-spezifisch).
  - Im "ultimate"-Modus werden alle verfügbaren Parser und Tag-Extraktionen aktiviert.
- **Tag-Optionen:**
  - Nutzer/Entwickler können gezielt steuern, welche Tag-Sets (basic, extended, full_tags) extrahiert und gespeichert werden.
  - Die Tag-Auswahl wird im Prozess und in der Datenbank dokumentiert.
- **Datenbankintegration:**
  - Alle relevanten Parser-Resultate und Tag-Sets werden strukturiert in der Datenbank persistiert.
  - Historisierung und Nachvollziehbarkeit der Parserläufe (inkl. Modus, Chain, Zeitstempel, Fehler, Dauer).

## Technische Überlegungen
- Refactoring der `media_parser.py` zur klaren Trennung von Parserprozess, Tag-Handling und Modus-Logik
- Erweiterung der Datenbankmodelle für flexible Tag- und Parser-Resultat-Speicherung
- Optionale Parallelisierung der Parserprozesse (Vorbereitung für Python 3.14+)
- CLI- und API-Optionen für gezielte Einzelparser- oder Full-Chain-Läufe

## Nächste Schritte
- Implementierung der Prozess- und Modus-Logik im Parser-Framework
- Anpassung der Datenbankmodelle und Migrationsskripte
- Erweiterung der CLI/API für flexible Steuerung
- Test- und Debugging-Tools für Einzelparserläufe
- Dokumentation und Beispiel-Workflows

---

**Fazit:**
Die Trennung der Parserprozesse, flexible Tag-Optionen und die Unterstützung von Full/Ultimate-Modi schaffen die Grundlage für eine zukunftssichere, modulare und maximal auswertbare Medienanalyse im Media Web Viewer.
