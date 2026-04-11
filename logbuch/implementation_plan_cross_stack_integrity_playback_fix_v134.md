# Implementation Plan – Cross-Stack Integrity & Playback Fix (v1.34)

## Problem Statement
Media-Playback und Rendering sind im neuen Duo-View-Layout "broken". Ursache ist ein Fehler in der Pfadauflösung beim Proxy-Serving und fehlende End-to-End-Tests.

---

## Proposed Changes

### [Backend] Media Pipeline Correction

**[MODIFY] main.py**
- **Fix serve_media (L:3814):**
  - Ersetze `os.path.abspath(decoded_path)` durch `resolve_media_path(decoded_path)`.
  - Relative Bibliothekspfade werden so korrekt gegen das Media-Root aufgelöst.
- **Enhanced Test Reporting:**
  - `report_items_spawned` und `report_playback_state` loggen detaillierten Kontext ins Terminal.

---

### [Frontend] Automated Integrity Suite

**[NEW] ui_integrity_verify.js**
- Implementiere eine Self-Diagnostic-Routine, die aus der UI getriggert werden kann:
  - **DOM Audit:** Scannt nach `#player-view-legacy` und `.legacy-track-item`.
  - **Playback Probe:** Klickt programmatisch den ersten Track und überwacht die Pipeline.
  - **Trace Integration:** Jeder Testschritt wird via `mwv_trace('DOM-TEST', ...)` ans Backend gemeldet.

**[MODIFY] audioplayer.js**
- `renderPlaylist` synchronisiert zuverlässig zwischen `currentPlaylist` und den Duo-View-Containern.

---

### [Verification] Automated Playwright Suite

**[MODIFY] playback_verify.py**
- **Selector Update:** `.implementation-encapsulated-state-buffer-node` → `.legacy-track-item`
- **ID Update:** `#big-player-title` → `#big-player-title-legacy`
- **Wait Logic:** Timeouts für Glassmorphism-Transitions verlängern.

---

## Verification Plan

### Automated Tests
- **Playwright:** `python3 tests/ui/playback_verify.py` – Tracks müssen gefunden und Playback bestätigt werden.
- **Integrity Suite:** `runIntegrityCheck()` im Browser-Console ausführen.

### Manual Verification
- Audio Player Tab öffnen.
- Prüfen, ob Items als weiße Karten erscheinen.
- Track anklicken und prüfen, ob Audio startet (Visualizer animiert).
- Backend-Terminal auf `[GUI-TRACE]` und `[DOM-TEST]` Logs kontrollieren.

---

**User Review Required:**
- Die Änderungen in main.py sind kritisch für die Behebung des Playback-Problems.
- Bitte Review und Freigabe vor Umsetzung!
