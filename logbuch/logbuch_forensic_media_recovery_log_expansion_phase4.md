# Logbuch: Forensic Media Recovery & Log Expansion (Phase 4)

## Problemstellung
- Echte Mediendateien fehlen weiterhin in der UI.
- Analyse: Viele Dateien liegen in Ordnern wie 'Beigabe' (Audio) oder 'Supplements' (Video/ISO). Die bisherige Logik mappt 'Beigabe' fälschlich zu Video, wodurch Audio-Dateien "geghostet" werden.

## Maßnahmen
### 1. Extension-First Category Mapping (Python)
- [MODIFY] main.py
    - Die Kategorie wird jetzt primär anhand der Dateiendung (z.B. .mp3, .m4a) bestimmt, bevor auf die Legacy-DB-Kategorie zurückgegriffen wird.
    - [FORENSIC-PATH]-Logs in log_dropped_reasons: Exakte Dateipfade der gefilterten Items werden geloggt.

### 2. High-Density Filtration Auditing (Python)
- [MODIFY] config_master.py
    - log_dropped_reasons akzeptiert jetzt eine Liste von "Sample Dropped Paths" für forensisches Feedback im app.log.

### 3. Frontend Forensic Parity (JS)
- [MODIFY] common_helpers.js
    - isAudioItem und isVideoItem prüfen jetzt zuerst die Dateiendung, bevor sie auf die Kategorie-Strings zurückgreifen. So werden z.B. MP3s in 'Beigabe' korrekt als Audio erkannt.

## Verifikation
- [Automatisiert] UI-Refresh und STDOUT auf [FORENSIC-PATH]-Logs prüfen.
- [Automatisiert] app.log auf neue "Dropped Paths"-Zusammenfassungen prüfen.
- [Manuell] MP3s im 'Beigabe'-Ordner erscheinen jetzt im Audio-Player.
- [Manuell] MKVs im 'Supplements'-Ordner erscheinen jetzt im Video-Orchestrator.

---

*Letztes Update: 18.04.2026*
