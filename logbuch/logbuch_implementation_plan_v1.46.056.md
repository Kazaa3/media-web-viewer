# Plan: Forensic Library Stabilization & Non-Destructive Ingestion

## Ziel
Das "Verschwinden echter Items" wird behoben, indem der automatische Boot-Scan nicht-destruktiv wird und das Frontend echte Datenbankinhalte immer gegenüber Notfall-Mocks priorisiert.

---

## User Review Required

### Wichtige Maßnahmen
- Der automatische Start-Scan wird auf Additiv-Modus (clear_db=False) umgestellt. Echte Items bleiben über Neustarts erhalten, neue werden ergänzt/aktualisiert.
- Sichtbarkeits-Flag im Frontend verhindert "Mock Item Flash", wenn die DB bereits echte Items enthält.

---

## Proposed Changes

### Backend: Non-Destructive Boot Ingestion
#### [MODIFY] `main.py`
- `boot_scan_trigger` ruft jetzt `scan_media(clear_db=False)` auf.
- Die 599 Items aus der letzten Session werden beim Neustart NICHT gelöscht.

### Frontend: Hydration Guard & Refresh Logic
#### [MODIFY] `forensic_hydration_bridge.js`
- Stage-1-Check erweitert: Prüft, ob Backend gerade einen Boot-Scan durchführt.
- Verhindert Mock-Injektion, wenn `realDbCount == 0` aber ein Scan läuft (optional: "Scanning..."-Status anzeigen).

#### [MODIFY] `bibliothek.js`
- `refreshLibrary` sorgt dafür, dass Mock-Items entfernt werden, sobald echte Items eintreffen (kein "Mixed Library"-State).

---

## Verification Plan

### Automated Tests
- Keine.

### Manual Verification
- App neustarten, prüfen, dass "Items: 599" sofort im Footer sichtbar ist (DB wurde nicht gelöscht).
- Scanner Dashboard erscheint nur, wenn die DB wirklich leer ist (z.B. beim ersten Start).

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
