# Logbuch Meilenstein: Recovery – Sync-Chain Unification & Detailed Diagnostics (v1.35.68)

## Ziel
Behebung des „Black Hole“-Problems in der Audio-Queue durch Vereinheitlichung der Backend-Kategorielogik und Einführung eines Parser-Only-Modus. Verbesserung der Entwicklerdiagnose durch detaillierte Status-Popups.

## Maßnahmen & Änderungen

### Backend Core (src/core/main.py)
- **Unification:**
  - cat_map (CTA map) und displayed_categories in eine zentrale Helper-Funktion _apply_library_filters() ausgelagert.
- **Parser-Only Toggle:**
  - window.__mwv_parser_only_mode (Frontend) wird an das Backend übergeben.
  - Ist der Modus aktiv, liefert get_library die rohen DB-Items ohne Kategorie-Filterung.

### UI Bridge (web/js/diagnostics_helpers.js)
- **Detaillierte Benachrichtigungen:**
  - notifyDiagnosticChange zeigt jetzt sprechende Statusmeldungen:
    - DIAG → „Nuclear Recovery Mode (S1-S15 Stages)“
    - NATV → „Native HTML5 Engine (No Transcoding)“
    - HIDB → „Hide Real DB Items (Mock Flow Only)“
    - PARS → „Parser-Only Mode (Bypass Category Filters)“

### Audio Queue (web/js/audioplayer.js)
- **Queue Sync Audit:**
  - syncQueueWithLibrary-Filter ist jetzt toleranter.
  - Wenn Queue 0, aber Library > 0, wird ein detailliertes [FE-AUDIT-QUEUE] Log ausgegeben, warum Items fehlen.

### Footer UI (web/app.html)
- **Neuer Toggle:**
  - PARS (Parser) Button im Diagnostic-Cluster hinzugefügt.

## Verifikation
- **Automatisiert:**
  - [FE-AUDIT-QUEUE] Logs erscheinen in der Konsole.
  - updateSyncAnchor(541, 527) wird rot angezeigt, wenn die Queue leer bleibt.
- **Manuell:**
  - PARS-Toggle: ON → Items erscheinen in Library/Queue?
  - DIAG-Toggle: ON → Neue Popup-Meldung sichtbar?
  - Queue zeigt Items, wenn Library > 0?

## Ergebnis
- Die Sync-Chain ist vereinheitlicht, Black Holes in der Queue werden sofort sichtbar.
- Parser-Only-Modus ermöglicht gezielte Filterdiagnose.
- Status-Popups und Audit-Logs bieten maximale Transparenz für Entwickler und User.

---

**Meilenstein abgeschlossen: Recovery – Sync-Chain Unification & Detailed Diagnostics.**
