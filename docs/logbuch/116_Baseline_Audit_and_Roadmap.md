# 116 – Baseline-Audit und Benchmarking-Roadmap

**Datum:** 12.03.2026  
**Version:** 1.3.4+  
**Status:** Audit & Implementation

## Kontext

Nach der Stabilisierung des Testsystems (siehe [114_Test_Stabilisierung](114_14_Test_Stabilisierung_und_Infrastruktur.md)) liegt der Fokus nun auf der Messbarkeit von Performance-Regressionen und dem Ausbau der Testabdeckung über alle Medienformate hinweg. Dieses Logbuch dokumentiert den Audit der bestehenden Pipelines und die Einführung eines neuen Benchmarking-Systems.

## Baseline-Archivierung

Um zukünftige Optimierungen (oder Regressionen) objektiv bewerten zu können, wurden historische Testergebnisse zentralisiert:

- **Ort:** `tests/artifacts/baseline/`
- **Inhalt:** 
  - `parser_benchmark_results.json`: Extraktionszeiten für alle Medien im `/media` Ordner.
  - `m4b_all_tools_results.json`: Vergleichswerte spezialisierter M4B-Parser.
  - `dependency_probe_report.json`: Status der Systemabhängigkeiten (FFmpeg, VLC, etc.).

Diese Dateien dienen als "Ground Truth" für Version 1.3.4.

## Pipeline-Audit Ergebnisse

Ein umfassender Audit der Testordner ergab folgende Situation:

### 1. Tech-Pipelines (`tests/tech/`)
- ✅ **FFmpeg/VLC**: Gute Coverage für Basisfunktionen und Streaming.
- ⚠️ **Mutagen**: Fokus stark auf M4B begrenzt; andere Audioformate (FLAC, Ogg) unterrepräsentiert.
- ⚠️ **Scapy**: Nur Basistests; Netzwerk-Stress-Szenarien fehlen.

### 2. Category-Pipelines (`tests/category/`)
- ✅ **Common**: Sehr starke Coverage für i18n und allgemeine Parser-Logik.
- ❌ **Video/Audio**: Starke Fixierung auf MKV und MP3/M4B. Ein systematischer Test der Format-Diversität fehlte bisher.
- ✅ **Playlist**: UI-Interaktionen sind gut abgedeckt.

### 3. Advanced-Pipelines (`tests/advanced/`)
- ✅ **Integration**: Umfassende Tests für Browser-Präferenzen und Launcher.
- ⚠️ **Stress**: Belastungstests vorhanden (`hammerhart`), aber ohne systematisches Ressourcen-Monitoring.

## Implementierte Erweiterungen

### 📊 Vergleichs-Engine: `compare_benchmarks.py`
Ein neues Tool in `tests/advanced/performance/` erlaubt den Vergleich aktueller Extraktionszeiten mit der Baseline.
- **Feature**: Prozentuale Delta-Berechnung pro Datei.
- **Feature**: Automatisierte Warnung bei Regressionen > 10%.

### 🎬 Media Diversity Tests
Neue Testsuiten zur Erweiterung der Format-Abdeckung:
- `test_video_format_diversity.py`: Validiert MP4, AVI, MOV, WMV, FLV, WebM.
- `test_audio_codec_diversity.py`: Validiert FLAC, OGG, Opus, WAV, M4A.

### 🔨 Enhanced Stress-Testing
Update von `test_scenario_hammerhart.py`:
- Integration von `psutil` zur Überwachung von Memory-RSS und File-Handles während der E2E-Tests.
- Erlaubt das frühzeitige Erkennen von Memory Leaks bei komplexen UI-Interaktionen.

## Roadmap & Nächste Schritte

1. **Coverage Target**: Erreichung der >80% Gesamtabdeckung durch gezielte Mock-Tests für fehlende Codecs.
2. **Binary Cleanup**: Automatisierte Bereinigung von Transcoder-Cache-Fragmenten nach Testläufen.
3. **CI-Integration**: Einbindung der `compare_benchmarks.py` in den wöchentlichen Quality-Report.

---
*Audit durchgeführt von Antigravity (AI Coding Assistant)*
