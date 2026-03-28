# Checklist: Bugfix & MPV Refinement (Phase 10)

## Status: Ongoing

---

### UI – Frontend
- [x] 19 JS-Syntaxfehler in app.html behoben (verschachtelte Quotes, fehlerhafte Strings)
- [x] Malformed SVG-Icon-IDs korrigiert (Spaces in hrefs entfernt)
- [x] Fehlende triggerBatchExtract JS-Funktion implementiert
- [x] window.onerror-Bridge für Echtzeit-Backend-Error-Reporting ergänzt

### MPV Bridge
- [x] web/js/mpv-player.js zu web/js/mpv_player.js umbenannt (Naming-Consistency)

### Verification Plan
- [x] Master Diagnostic Runner ausgeführt (python3 tests/run_all.py)
- [x] AdvancedPlayerSuite für open_mpv und mkv_batch_extract getestet (python3 tests/engines/suite_advanced_player.py)
- [x] Static GUI Integrity Suite (tests/engines/suite_ui_integrity.py) für JS-Syntax, SVG-IDs, Struktur-Balance ausgeführt
- [ ] 100% statischer Diagnostic-Pass (Frontend Integrity)

### Manual Verification
- [x] Startup Audit: Anwendung gestartet, keine Konsolenfehler
- [x] Toggle Verification: "Batch Extraktion"-Button löst Toast/Backend-Action aus
- [x] MPV Verification: "MPV Native"-Button startet WASM/Desktop MPV Player ohne JS-Fehler

---

*Diese Checkliste dokumentiert die finalen Bugfixes, Refactorings und Verifikationsschritte für Phase 10 der Diagnostic Infrastructure Modernization.*
