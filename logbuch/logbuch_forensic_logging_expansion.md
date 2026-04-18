# Logbuch: Forensic Logging Expansion (Ausbau)

## Ziel
Vollständige forensische Kontrolle durch "Full-Stack Trace"-Logging: Backend, Bridge und Renderer werden mit tiefen Audit-Logs ausgestattet, um stille Fehlerquellen auszuschließen und die Medienhydration lückenlos nachvollziehbar zu machen.

---

## Maßnahmen

### 1. Backend Forensic Audit (Python)
- [MODIFY] main.py
    - `get_library`: Category-Distribution-Audit vor Rückgabe einbauen.
    - Aktiven `active_branch` und `h_mode` (Hydration Mode) loggen.
    - `log.debug` für die exakten Item-IDs im "Emergency Recovery"-Modus.
    - `_apply_library_filters`: Logs für Branch-Filterung (z.B. "Branch 'audio' matched 497 items").

### 2. Bridge Handshake Visibility (JS)
- [MODIFY] bibliothek.js
    - `loadLibrary`: `console.warn` für das rohe JSON-Payload von Eel.
    - Kategorieverteilung loggen, wie sie im Frontend ankommt (vor lokaler Filterung).

### 3. Renderer Integrity Monitoring (JS)
- [MODIFY] audioplayer.js
    - "Type Mismatch"-Logs: Wenn ein Renderer ein Item überspringt, Audit-Trace mit Name und erkannter Kategorie loggen.
    - Zeitmessung für jeden Rendering-Pulse (`window.__mwv_last_render_ms`).

## Verifikation
- [Automatisiert] main.py: STDOUT-Logs auf [BD-AUDIT] prüfen.
- [Manuell] UI-Refresh durchführen, Browser-Konsole auf [FE-AUDIT] und [Sync-Pulse] prüfen.
- [Manuell] app.log auf Backend-Filterzusammenfassungen prüfen.

---

*Letztes Update: 18.04.2026*
