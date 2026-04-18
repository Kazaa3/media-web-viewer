# Logbuch: Forensic Parity & Legacy Category Alignment

## Problemstellung
- Paritätsdefizit: 583 Dateien im Filesystem, aber nur 541 Items in der Datenbank.
- Viele DB-Items nutzen Legacy-Kategorien (album, series, beigabe, supplements), die von den aktuellen Branch-Governance-Filtern ignoriert werden.
- 42 Dateien fehlen komplett in der Datenbank ("Ghosting").

## Maßnahmen
### 1. Backend Category Normalization (Python)
- [MODIFY] main.py
    - Mapping in `get_library` erweitert:
        - album, podcast → audio
        - series, serie, beigabe, supplements, spiel → video
        - docs, nfo → document
    - `_apply_library_filters` akzeptiert jetzt auch diese Legacy-Typen.

### 2. Database Parity Recovery (Python)
- [MODIFY] db.py
    - `force_re_scan`-Trigger implementiert, um die 42 fehlenden Dateien zu erfassen.
    - Logging ergänzt, um zu erkennen, welche Dateien beim nächsten Scan nicht eingefügt werden können.

### 3. Frontend Category Support (JS)
- [MODIFY] common_helpers.js
    - `isAudioItem` und `isVideoItem` erkennen jetzt auch album, podcast, series, beigabe usw. als gültige Kategorien.

## Verifikation
- [Automatisiert] Mit sqlite3 prüfen, ob die Anzahl der Items in der Medientabelle Richtung 583 steigt.
- [Automatisiert] app.log auf [SCAN-RECOVERY]-Meldungen prüfen.
- [Manuell] "Alle Medien" zeigt jetzt auch vormals fehlende Items (z.B. mit Label 'Album' oder 'Beigabe').
- [Manuell] HUD-Item-Count entspricht dem Filesystem-Count (~583).

---

*Letztes Update: 18.04.2026*
