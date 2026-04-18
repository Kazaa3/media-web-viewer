# Logbuch: DB Health Monitoring & Forensic Expansion

## Problemstellung
- Die DB-Anzeige (LED) bleibt dauerhaft gelb, es fehlt eine forensisch belastbare Überwachung des Datenbankzustands.
- Ziel: Umstellung von einer statischen Status-LED auf ein dynamisches Health-Beacon, das durch Echtzeit-Backend-Diagnostik gesteuert wird.

## Maßnahmen
### 1. Backend: Echtzeit-Integritätsprüfung (Python)
- [MODIFY] main.py
    - In `get_library` wird während des Filesystem-Audits ein `PRAGMA integrity_check` ausgeführt.
    - Das Ergebnis wird als `db_health` (z.B. "ok", "error", "corrupt") im Audit-Objekt zurückgegeben.
    - Der Health-Status wird im zentralen [BD-AUDIT]-Backend-Pulse geloggt.

### 2. Bridge: Health Handshake (JS)
- [MODIFY] bibliothek.js
    - `loadLibrary` extrahiert `db_health` und `size` aus dem Audit-Objekt.
    - Status wird in `window.__mwv_last_db_health` gespeichert und steht dem UI zur Verfügung.

### 3. UI: Dynamische Forensik-LED (JS)
- [MODIFY] common_helpers.js
    - `setHydrationMode` passt die DB-LED-Farbe an:
        - Grün (#2ecc71): Health ist "ok".
        - Rot (#e74c3c): Health ist "error" oder "corrupt".
        - Gelb (#f1c40f): Initialzustand oder "checking" (wenn Daten fehlen).

## Verifikation
- [Automatisiert] app.log auf [BD-AUDIT] Database Integrity: ok prüfen.
- [Manuell] Nach einem REFRESH sollte die DB-LED im HUD/Footer grün werden, wenn die DB gesund ist.
- [Manuell] Tooltip/Log der DB-Anzeige zeigt den technischen Health-Status an.

---

*Letztes Update: 18.04.2026*
