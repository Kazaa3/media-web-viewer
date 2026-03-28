# Eel Exposed Function Audit

## Übersicht

Diese Reporting-Ansicht dokumentiert alle mit `@eel.expose` versehenen Funktionen in der Anwendung und gibt einen Überblick über die API-Struktur, Redundanzen und Optimierungsempfehlungen.

---

## Gesamtzahl der @eel.expose-Funktionen in src/core/main.py

**169**

---

## Functional Overview

Die Anwendung stellt eine umfangreiche API für Medienverwaltung, Wiedergabe und Systemdiagnostik bereit.

### Key Categories

- **Playback Control:**
  - play_media, open_video, vlc_seek, vlc_ts_mode, next_in_playlist, prev_in_playlist
- **Library Management:**
  - scan_media, get_library, add_file_to_library, delete_media, rename_media
- **Configuration:**
  - get_startup_config, update_startup_config, set_language, set_app_mode
- **Diagnostics:**
  - check_ui_integrity, run_tests, get_system_stats_static, rtt_ping
- **MKV/ISO Tools:**
  - mkv_batch_extract, remux_mkv_batch, extract_main_from_iso

---

## Detected Redundancies/Duplicates

| Function Name   | Location         | Issue                                      |
|----------------|------------------|--------------------------------------------|
| analyse_media  | main.py#4353     | Legacy synchronous analysis mode.          |
| analyze_media  | main.py#7739     | Modern asynchronous routing-focused analysis. |
| getTabButton   | app.html#2662 / #8611 | Duplicated JS definition. (To be removed). |

---

## Recommendation

- Konsolidiere `analyse_media` in den modernen Handler `analyze_media`.
- Entferne die doppelte Definition von `getTabButton` an Zeile 8611 in app.html.

---

*Diese Ansicht dient als Referenz für API- und Code-Audits sowie für die weitere Optimierung der Eel-Exposed-Funktionen.*

---

# UI Theme & AI Infrastructure Overview

---

# Toolchain & Advanced Playback Integration

---

# Implementation Plan – Final Stabilization & Advanced Playback

---

# Task: Finalizing Stabilization & Advanced Playback

**Status:** [/] (in Bearbeitung)

## 1. Diagnostic Infrastructure Enhancement [/]
- Test-Imports refaktorieren, um "Missing export"-Warnungen zu beheben
- MockEel so erweitern, dass decorator-basierte Exposure voll unterstützt wird
- Robusten Level 10 Integrity Check in suite_toolchain.py implementieren
- ISO-Kategorisierungslogik in format_utils.py fixen
- Fehlende/aliased Eel-Handler für Reporting/Logbuch wiederherstellen

## 2. Media Player Test Suite & Advanced Playback [/]
- suite_advanced_player.py für umfassende Player-Verifikation ausbauen
- swyh-rs-cli-Support und Verifikation ergänzen
- mpv- und vlc-Bridge-Stabilität prüfen
- Playback-Benchmarks an Reporting-UI anbinden

## 3. GUI Stabilization & JS Scrub [/]
- app.html auf JS-Syntaxfehler prüfen (verschachtelte Quotes, fehlende Handler)
- Item-Anzeige und Dictionary-Loading sicherstellen
- Tab-Navigation und Container-Nesting verifizieren

## 4. Final Verification & Walkthrough [ ]
- Alle Diagnostic Suites (Master Run) ausführen [/]
- >90% Erfolgsquote erreichen (bekannte fehlende System-Binaries ignorieren) [/]
- walkthrough.md mit Aufnahmen/Screenshots erstellen [/]

Dieser Plan fokussiert sich auf die Erweiterung der Diagnose-Infrastruktur und die robuste Integration sowie Verifikation der Advanced-Playback-Features.

## Proposed Changes

### Toolchain & Advanced Player Suites
- [MODIFY] suite_toolchain.py: Level 10 Integrity-Check um spezifische DB-Health-Checks (z.B. Connection, Schema-Version) erweitern
- [MODIFY] suite_advanced_player.py: Levels für swyh-rs-cli-Präsenz und Funktionsprüfung ausbauen; MPV-Bridge und alle 10+ Modi verifizieren

### Core Application Logic
- [MODIFY] main.py: toggle_swyh_rs-Logik mit subprocess implementieren (Prozessmanagement für swyh-rs-cli)
- Aliased Functions für Test-Alignment korrekt exposen
- update_metadata_entry und weitere fehlende Handler aus dem Alignment-Audit ergänzen

### GUI & JS Integrity
- [MODIFY] app.html: JS-Syntaxfehler (verschachtelte Quotes, Brackets) bereinigen
- Sicherstellen, dass log_js_error korrekt aufgerufen und im Backend empfangen wird
- Fehler beheben, die "items displayed" oder "dict loading" verhindern (z.B. Race-Conditions beim Init)

## Verification Plan

### Automated Tests
- Master Diagnostic Suite: python3 tests/run_all.py
- suite_toolchain.py: Level 10 PASS
- suite_advanced_player.py: Level 2 (SWYH) und Level 6 (Binaries) PASS (oder WARN, falls System fehlt)
- suite_gui_integrity.py: 100% Pass auf Structural/Token Audits

### Manual Verification
- Reporting-Tab in der GUI öffnen und prüfen, ob der neue Media Player Testbereich sichtbar ist
- Logbuch-Tab prüfen: Einträge korrekt angezeigt (dict loading)
- SWYH-RS-Bridge im UI toggeln und Prozessmanagement im Hintergrund verifizieren

Die UI-Integrität und die Datenbank-Komponenten wurden stabilisiert (100% Brace-Balance in app.html, alle Diagnostic-Levels bestanden). Ein umfassender Function-Audit (169 Eel-Items) und Theme-Review wurden durchgeführt, "AI-READINESS"-Anker identifiziert und doppelte JS-Definitionen entfernt.

**Aktuelle Arbeiten und Fortschritte:**
- HandBrake-Integration und Advanced Playback Verification gestartet
- Hardware Detection und Transcoding-Infrastruktur geprüft
- HandBrakeCLI und mkvextract vorhanden, mpv und swyh-rs nachinstalliert
- Python-Abhängigkeiten (enzyme, pymkv, ffmpeg-python) installiert
- task.md mit Phase 8 und 9 aktualisiert
- transcoder.py für Batch-Processing und GPU-Beschleunigung erweitert
- Media Routing Test-Level zu suite_reporting.py hinzugefügt
- MPV- und SWYH-RS-Bridge in main.py identifiziert und zu Eel exposed
- Media Routing Debug-Endpoint zu main.py hinzugefügt
- suite_advanced_player.py erweitert
- Duplicate Exposure Errors und fehlende Imports in mode_router.py erkannt und in Bearbeitung
- Logging-Anforderungen global umgesetzt
- Fehlende Reporting-Handler für Benchmarks und DVD-Reports in main.py ergänzt
- Restoration von mode_router.py in Arbeit

**Background Steps:**
  python3 tests/engines/suite_advanced_player.py && python3 tests/engines/suite_reporting.py

Die Anwendung nutzt ein Premium-Theme im "Carbon/Glass"-Stil mit fortgeschrittenen strukturellen Ankerpunkten für KI-Orchestrierung.

**1. Wording & Style [Theme]**
- Glassmorphism und Glassmorphic Panels als zentrales Designprinzip
- Primärfarben: Cyan (#00f2fe), Dunkelgrau (#151515)
- Visuelle Effekte:
  - backdrop-filter: blur(14px) für Panel-Transparenz
  - -webkit-box-reflect für 3D-Coverflow-Effekte
  - Lineare Farbverläufe mit #00f2fe und #4facfe
- Wording: Premium-Terminologie wie "Sequential Buffer" (Playlist), "Telemetry Inspector" (Debug), "Chain Config" (Parser)

**2. KI-Anker [AI Readiness]**
- Explizite strukturelle Marker für KI-basierte Analyse und Orchestrierung
- Meta-Tag: <meta name="ai-readiness" content="verified" data-ai-id="root-manifest">
- Data-Attribute: Jedes Tab-Panel und zentrale UI-Element ist mit data-ai-id oder beschreibenden IDs versehen (z.B. für automatisiertes Testing und Discovery)
- Strukturelle Metadaten: Kommentare mit [AI-READINESS] geben Hinweise auf Komponenten-Hierarchien

**3. Structural Anchors**
- Kritische IDs in app.html:
  - main-sidebar: Root-Navigationsanker
  - main-content-area: Haupt-Rendering-Ziel
  - multiplexed-media-player-orchestrator-panel: Zentrale Player-Instanz
  - coverflow-library-panel: Primäre Medien-Discovery-Ansicht
