# Logbuch: Bugfixes, Feature-Integration & Reporting

**Datum:** 16. März 2026

## Aufgaben & Fortschritt

- **Bugfixes:**
  - ISO Path Encoding Bug im Backend behoben (korrekte URL-Decodierung für .iso-Dateien).
  - Video.js pause() API Bug im Frontend behoben (korrekter Aufruf auf vjsPlayer-Instanz).

- **UI-Verbesserungen:**
  - Erweiterte Player-Controls: Stop, Shuffle, Repeat, Seek, Speed, EQ (Unicode-Symbole) integriert.

- **Casting-Integration:**
  - Chromecast & DLNA Casting implementiert (pychromecast, dlnap).
  - UI für Gerätesuche und Auswahl hinzugefügt.

- **Audio & Batch-Remux:**
  - swyh-rs Audio-Bridge integriert (Start/Stop via UI).
  - Batch-Remux zu MKV mit mkvmerge implementiert (Ordner-Remux per Button).

- **Reporting & Benchmarking:**
  - Reporting-Dashboard und grafische Ergebnisdarstellung hinzugefügt.
  - Neues Benchmarking-Skript für Start-Latenz und Performance.

- **Tests & Verifikation:**
  - DVD ISO Integrationstest: `tests/integration/basic/playback/test_dvd_iso.py` erstellt.
  - ffprobe Pre-Check für smarte Moduswahl integriert.
  - Gesamte Implementierung verifiziert und Benchmarks durchgeführt.

---

Weitere Details siehe vorherige Logbuch-Einträge und implementation_plan.md.
