# Implementation Plan – Phase 9: Advanced Playback & Toolchain Integration

## Ziel
Erweiterung der Media Toolchain um SWYH-RS, MKVcleaver-Style-Batching und signifikante Erweiterung der Video-Player-Modi (inkl. MPV).

---

## Proposed Changes

### [Backend] Media Toolchain & Bridges
- **[MODIFY] main.py**
  - **SWYH-RS Bridge:** Implementiere `toggle_swyh_rs`, um den swyh-rs-cli-Prozess zu starten (sofern verfügbar). State-Tracker verhindert Mehrfachinstanzen.
  - **Batch Extraction (MKVcleaver-Style):**
    - Implementiere `mkv_batch_extract(files, tracks)` mit mkvextract.
    - Unterstütze Extraktion aller Untertitel oder spezifischer Streams aus einer Liste von MKV-Dateien.
  - **MPV Native Support:** Implementiere `open_mpv(filepath)` als Pendant zu `open_vlc`.

### [MODIFY] mode_router.py
- **Expanded Modes:**
  - Füge dash, webtorrent, hls_native, native_chrome, mpv_native, vlc_native zur Mapping-Tabelle hinzu.
- **Smart Routing Logic:**
  - Aktualisiere `smart_route`, um mpv_native oder vlc_native für Ultra-High-Bitrate/4K-MKVs zu bevorzugen.
  - Standardmäßig mpv_wasm für experimentelle Container, falls in config aktiviert.

### [Frontend] UI & Playback Logic
- **[MODIFY] app.html**
  - **Player Orchestrator:**
    - Aktualisiere handleContextMenuAction für neue native Modi.
    - Implementiere Frontend-Bridge für mpv_wasm (Platzhalter verfeinern).
  - **Control Center Updates:**
    - Füge "Batch Extract"-Button zur Subtitle Management UI hinzu.
    - Verknüpfe toggle-swyh-rs Checkbox mit Backend.
  - **i18n:**
    - Ergänze Keys für neue Modi und Tools.

### [Testing] Diagnostic Engines
- **[NEW] suite_advanced_player.py**
  - Neue Diagnostic Engine zur Verifikation des Routings der 10+ Modi.

---

## Verification Plan

### Automated Tests
- **Routing Audit:** `python3 tests/run_all.py` ausführen und I18n-L02 (Parität) sowie die neue AdvancedPlayerSuite prüfen.
- **CLI Detection:** Sicherstellen, dass die Diagnostic Suite swyh-rs-cli korrekt erkennt (oder als fehlend meldet), ohne abzustürzen.

### Manual Verification
- **Casting Tab:** "SWYH-RS Enabled" toggeln und prüfen, ob das Backend den Subprozess korrekt loggt.
- **Subtitle Editor:** Mehrere MKV-Dateien auswählen, "Batch Extract Subtitles" auslösen und prüfen, ob Dateien im Cache erscheinen.
- **Playback:** Rechtsklick auf 4K MKV -> "Play with MPV (Native)" und prüfen, ob mpv auf dem Host startet.

---

*Bitte reviewe diesen Plan (implementation_plan.md) und gib Feedback, bevor die Umsetzung startet.*
