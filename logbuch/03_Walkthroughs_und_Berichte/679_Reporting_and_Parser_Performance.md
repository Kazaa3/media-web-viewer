# Logbucheintrag 020: Reporting-System & Parser Performance

**Datum:** 18. März 2026
**Fokus:** Transparenz und Benchmarking

## Übersicht
Das Reporting-System wurde grundlegend erweitert, um detaillierte Einblicke in die Performance des Video-Streamings, Audio-Streamings und der Metadaten-Extraktion zu geben. 

## Implementierte Features

### 1. Untermenüs im Reporting-Tab
Der Reporting-Tab verfügt nun über ein Dropdown-Menü mit folgenden spezialisierten Ansichten:
- **Dashboard**: Übersicht der Testläufe und Trends.
- **Datenbank (SQL)**: Direktzugriff auf Analyse-Queries.
- **Video Streaming**: Benchmarks für ffplay, VLC und MediaMTX (Latenz, Status).
- **Audio Streaming**: Benchmarks für Audio-Codecs und Transport-Latenzen.
- **Parser Reporting**: Statistische Auswertung aller Metadaten-Parser.

### 2. Parser Performance Übersicht
Sowohl im Reporting-Tab als auch direkt im **Parser-Tab** wurde eine Performance-Übersicht integriert. Diese zeigt:
- Die durchschnittliche Extraktionszeit für jeden Parser (Filename, Mutagen, FFmpeg, MKV-Remuxer etc.).
- Die Gesamtzahl der gescannten Medien für eine valide statistische Basis.
- Farblich kodierte Latenzwerte (Grün: <0.1s, Gelb: <0.5s, Orange: >0.5s).

### 3. Backend API Erweiterung
- `get_benchmark_results()`: Liefert die Historie aus `benchmarks.json`.
- `get_parser_stats()`: Berechnet aggregierte Statistiken aus dem `parser_times` Feld der SQLite-Datenbank.
- `get_test_results()`: Exponiert die Ergebnisse der Regression-Suite.

## Technische Details & Fixes
- **JS State Management**: `switchTab` und `switchReportingView` wurden synchronisiert, um Daten nur bei Bedarf zu laden (Lazy Loading).
- **UI Design**: Integration in den left-column des Parser-Layouts für direkten Feedback-Loop bei Konfigurationsänderungen.
- **i18n**: Volle Mehrsprachigkeit (DE/EN) für alle neuen Metriken.

## Fazit
Mit diesen Erweiterungen ist der Media Web Viewer bereit für großflächige Bibliotheksscans ("Ultimate Mode"), da Flaschenhälse in der Parsing-Pipeline nun sofort identifiziert werden können.
