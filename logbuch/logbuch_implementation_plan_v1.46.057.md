# Implementation Plan: Forensic Library Hydration Restoration (v1.46.057)

## Kontext
Die "Circular Failure"-Ursache für leere Bibliotheken (oder nur Mocks) wurde gefunden: In `api_library.py` wurde bei Hydration Stage 1 immer ein DB-Count von 0 zurückgegeben. Dadurch blieb das System in einer Mock-Loop, obwohl echte Items existierten.

---

## User Review Required

### Wichtige Maßnahmen
- **Backend Traps:** Entfernen der Codezeilen in `api_library.py`, die echte DB-Counts verstecken.
- **Logging Alignment:** Logging wird vereinheitlicht, damit alle Library-Handshakes und Drops/Inclusions nachvollziehbar im Log erscheinen.

---

## Proposed Changes

### Backend Core
#### [MODIFY] `api_library.py`
- **Standardize Logging:**
    - `logging.getLogger` durch `src.core.logger.get_logger` ersetzen, damit alle Library-Events im Log erscheinen.
- **Eliminate Stage-1 Trap:**
    - Zeilen entfernen, die bei `audit_stage == 1` immer `db_count: 0` zurückgeben.
    - Backend gibt immer die echte Größe der Medientabelle zurück.
- **Handshake Hardening:**
    - `db_count` an das Frontend ist immer die rohe Länge der Medientabelle, keine Filter.

### Frontend Orchestration
#### [MODIFY] `forensic_hydration_bridge.js`
- **Pulse Synergy:**
    - Bridge triggert sofort `loadLibrary()`, sobald ein echter DB-Count erkannt wird – auch wenn aktuell noch Mocks angezeigt werden.

#### [MODIFY] `bibliothek.js`
- **HUD Parity:**
    - `totalDbCount` bevorzugt strikt den vom Backend gelieferten `db_count` gegenüber dem gefilterten `incomingCount`.

---

## Verification Plan

### Automated/Manual Tests
- **Database Pulse:** Prüfen, dass `sqlite3 data/database.db "SELECT count(*) FROM media;"` mit dem HUD-Label übereinstimmt.
- **Log Audit:** Logs nach `[api_library] [BD-AUDIT]` durchsuchen, um erfolgreiche Handshakes zu bestätigen.
- **Visual Check:** Im Browser/Screenshot prüfen, dass echte Medien die blauen [M] EX-PULSE-Mocks ersetzen.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
