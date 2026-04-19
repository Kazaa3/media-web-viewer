# Implementation Plan: Restoring Real Media Hydration & Repairing Mock Metadata

## Context
Der Nutzer sieht nur 12 "Untitled" Mock-Items, echte Medien fehlen. Die Datenbank ist leer (DB: 0), wodurch ein Stage-1-"Emergency Hydration"-Fallback im Frontend ausgelöst wird. Ziel: Mock-Metadaten verbessern und den Nutzer gezielt zum Scan führen.

---

## User Review Required

### Wichtige Maßnahmen
- Ein neues "Scanner Dashboard" Overlay erscheint, wenn die Library leer ist. Die 12 "Untitled" Mocks werden durch eine professionelle Diagnose-Oberfläche ersetzt, die explizit zum Scan auffordert.

---

## Proposed Changes

### Forensic Hydration Bridge (Frontend)
#### [MODIFY] `forensic_hydration_bridge.js`
- `forceEmergencyHydration` nutzt jetzt standardisierte MediaItem-Keys (name, tags, etc.), um "Untitled"-Fallbacks zu verhindern.
- Mock-Items erhalten randomisierte, professionelle Forensik-Titel (z.B. "EXHIBIT-001_SIG_DATA.mp3").

### Library UI (Frontend)
#### [MODIFY] `bibliothek.js`
- Neue Funktion `renderEmptyLibraryDashboard()` implementieren.
- Wenn `window.__mwv_last_db_count === 0`, statt leerer Slots/Mocks ein hochwertiges "Scanner Infrastructure"-Interface anzeigen.
- Großer, glassmorpher "INDEX MEDIA DIRECTORY"-Button, der `eel.scan_media()` triggert.

### Backend Scanner (Core)
#### [MODIFY] `main.py`
- `_scan_media_execution`-Pfad-Resolution prüfen.
- Nach Scan-Abschluss ein `js_hydration_pulse` an das Frontend senden, um automatisches UI-Refresh auszulösen.

### HUD & Diagnostics
#### [MODIFY] `shell_master.html`
- Forensic HUD so anpassen, dass DB: 0 Status rot hervorgehoben wird, wenn ein Scan empfohlen ist.

---

## Verification Plan

### Automated Tests
- `sqlite3 data/database.db "SELECT count(*) FROM media WHERE is_mock = 0;"` nach Scan ausführen, um Ingestion zu prüfen.

### Manual Verification
- Sicherstellen, dass Stage 1 keine "Untitled"-Items mehr zeigt.
- "INDEX MEDIA"-Button klicken und prüfen, dass echte Dateien aus dem media/-Ordner in der Gallery erscheinen.
- Forensic HUD prüfen: DB: count aktualisiert sich auf reale Zahl (z.B. 541).

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
