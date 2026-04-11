# Implementation Plan — Extended Sync Diagnostics (v1.35.40)

## Ziel
Die Datenpipeline zwischen Backend (DB) und Frontend (UI) wird transparent gemacht. Ein "Data X-Ray"-Overlay zeigt jederzeit, wie viele Items tatsächlich in der Datenbank liegen, wie viele im Frontend gerendert werden und ob die Synchronisation funktioniert.

---

## Key Goals

- **Backend Row Counter:**
  - Im Python-Backend wird ein Log-Eintrag wie `[DB-SYNC] Found X rows in database` hinzugefügt, sobald die UI Daten anfordert. So sieht man sofort, ob die Datenbank gefüllt ist.

- **Diagnostic HUD (Heads-Up Display):**
  - Ein "Control Center" wird als Overlay (z.B. unten rechts) in die UI injiziert.
  - Zeigt:
    - **DB Count:** Anzahl der Items, die das Backend tatsächlich liefert.
    - **DOM Count:** Anzahl der Items, die im UI/DOM sichtbar sind.
    - **Sync Status:** Grün/Rot-Indikator, ob die UI "stale" oder "synchron" ist.

- **Stage 5: Live Integrity Audit:**
  - Ein neuer Test-Button erzwingt einen Handshake zwischen DB und UI und hebt fehlende "Real Files" hervor, die beim Hydratisieren übersprungen wurden.

- **Non-Destructive Hydration:**
  - Die Diagnostik fügt Test-Tracks zu den echten Items hinzu (append), statt sie zu überschreiben. So sieht man Testdaten und echte Daten gleichzeitig.

---

## Umsetzungsschritte

1. **Backend (Python):**
   - Logging im get_library-Endpunkt: `[DB-SYNC] Found X rows in database` bei jedem Aufruf.

2. **Frontend (JS):**
   - Neues Diagnostic HUD als Overlay-Element (z.B. `#diagnostic-hud`).
   - HUD zeigt DB-Count, DOM-Count, Sync-Status (grün/rot).
   - Live-Button für Integrity Audit (Stage 5).
   - Hydration-Logik so anpassen, dass Testdaten angehängt werden.

3. **Verifikation:**
   - Nach Boot: HUD zeigt konsistente Zahlen, Sync-Status ist grün.
   - Bei Fehlern: Sync-Status wird rot, DB- und DOM-Count stimmen nicht überein.
   - Stage 5: Audit hebt fehlende Real-Files hervor.

---

## Feedback
Soll dieses "Data X-Ray"-Overlay wie beschrieben umgesetzt werden? Rückmeldung erwünscht!

---

**ArtifactType:** implementation_plan
**RequestFeedback:** true
**Summary:** Erweiterte Diagnostik mit HUD und Backend-Logging für vollständige Pipeline-Transparenz.
