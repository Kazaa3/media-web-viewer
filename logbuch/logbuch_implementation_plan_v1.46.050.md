# Implementation Plan: Restoring Hydration Mode Parity (v1.46.050)

## Context
Aktuell bleibt die UI im "Mock-Stall"-Zustand, d.h. Mock-Items werden immer angezeigt, auch wenn "Real" oder "Both" gewählt ist. Ursache ist ein zu aggressives Fallback im Backend, das bei leeren Real-Sets Mock-Items zurückgibt.

---

## User Review Required

### Wichtige Hinweise
- Die Datenbank enthält derzeit 0 echte Medien. Entweder wurde kein Scan durchgeführt oder das Zielverzeichnis (`./media`) enthält keine passenden Dateien.
- Es wird ein klarer "No Media Detected"-State implementiert, um Verwirrung zu vermeiden.

---

## Proposed Changes

### [Backend] API Library & Hydration Bridge
#### [MODIFY] `api_library.py`
- Konsolidierung der Hydration-Filterlogik, um doppelte Durchläufe zu vermeiden.
- **Fallback-Härtung:**
    - Zeile 185: Wenn `h_mode == 'real'`, KEIN Rückfall auf Mock-Items mehr. Stattdessen leere Liste oder spezialisierter Fehlerstatus.
- `fs_audit` erweitern, um die Gesamtanzahl Real vs. Mock Items zu loggen (für UI-Statistiken).

### [Frontend] UI Feedback & Transparenz
#### [MODIFY] `common_helpers.js`
- `refreshForensicLeds` aktualisieren, um anzuzeigen, wenn ein Modus "leer" ist (z.B. 'R'-Button dimmen oder Warnsymbol, wenn REAL=0).
- Sicherstellen, dass `setHydrationMode` nach Backend-ACK ein vollständiges UI-Reload triggert.

#### [MODIFY] `bibliothek.js`
- "Filtered Black Hole"-State verbessern: Explizite Meldung anzeigen, wenn 0 Real-Items in der DB gefunden wurden, inkl. Scan-Hinweis.

---

## Verification Plan

### Automated Tests
- `python3 src/core/main.py` (manuelle Prüfung der Logs auf [HYDR-TRACE])
- Im Browser prüfen: Wechsel zu "Real"-Modus mit leerer DB → leere UI + Scan-Hinweis, keine Mock-Items.

### Manual Verification
- 'R' im Footer klicken → "No items found"-Meldung erscheint.
- 'B' oder 'M' klicken → Mock-Items erscheinen wie erwartet.
- (Optional) Echte .mp3 in ./media legen, SCAN ausführen, prüfen, dass sie im 'R'-Modus erscheinen.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
