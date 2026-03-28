# Implementation Plan: Bugfix & MPV Refinement (Phase 10)

## Ziel
Behebung des gemeldeten JavaScript-Startup-Fehlers (fehlende Klammer/Zeichenkettenende), Implementierung der fehlenden Batch-Extraktionslogik und Refactoring der MPV-Komponenten für Namenskonsistenz.

---

## Proposed Changes

### [Component: UI – Frontend]
- **[MODIFY] app.html**
  - Zeilen 12732, 12737, 12741: Verschachtelte doppelte Anführungszeichen in showToast-Aufrufen durch einfache Anführungszeichen für den String und doppelte für SVG-Attribute ersetzen. Behebt "JS error on startup" und "missing )" durch fehlerhafte String-Literale.
  - Neue Funktion: Async function triggerBatchExtract() im passenden Script-Block ergänzen (UI-Button bei Zeile 8320). Ruft eel.mkv_batch_extract(currentVideoPath) auf.
  - Cleanup: SVG-Icon-Referenzen korrigieren (z.B. #icon-sparkles statt #icon - sparkles).
  - Refactor: <script src="js/mpv-player.js"> zu <script src="js/mpv_player.js"> ändern.

### [Component: Playback – MPV Bridge]
- **[MODIFY] mpv_player.js [RENAMED FROM mpv-player.js]**
  - web/js/mpv-player.js zu web/js/mpv_player.js umbenennen (Naming-Convention: Unterstriche).

---

## Verification Plan

### Automated Tests
- Master Diagnostic Runner ausführen, um Python/JS-Integrität zu prüfen:
  ```bash
  python3 tests/run_all.py
  ```
- AdvancedPlayerSuite gezielt für open_mpv und mkv_batch_extract testen:
  ```bash
  python3 -m unittest tests/engines/suite_advanced_player.py
  ```

### Manual Verification
- **Startup Audit:** Anwendung starten und prüfen, dass keine Konsolenfehler beim Initialisieren auftreten.
- **Toggle Verification:** "Batch Extraktion"-Button in der Subtitle Management UI klicken und prüfen, ob Toast/Backend-Action ausgelöst wird (Konsole/Logs).
- **MPV Verification:** "MPV Native"-Button klicken und prüfen, ob WASM/Desktop MPV Player ohne JS-Fehler startet.

---

*Dieser Plan stellt sicher, dass Phase 10 die letzten Bugs und Inkonsistenzen im MPV- und Batch-Extraktions-Workflow beseitigt.*
