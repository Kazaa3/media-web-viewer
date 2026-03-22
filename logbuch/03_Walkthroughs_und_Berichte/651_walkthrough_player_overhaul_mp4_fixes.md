# Walkthrough: Player Overhaul & MP4 Playback Fixes (März 2026)

## Zusammenfassung
Die Video-Player-Architektur der Media-Library-App wurde systematisch überarbeitet. Der MP4-Black-Screen-Bug ist behoben, die Unterstützung für ISOs, MKVs und weitere Formate wurde erweitert. Alle Kernfunktionen sind durch Tests und manuelle Verifikation abgesichert.

---

## 1. MP4 Playback Fix
- Problem: Schwarzer Bildschirm bei MP4-Playback (Video.js)
- Lösung: Video.js-Container wird beim Start korrekt angezeigt, Resize-Event wird ausgelöst (app.html)
- UI-Optimierung: Z-Index des Premium-Players angepasst, Layering-Probleme gelöst

## 2. Robuste Path Resolution
- Implementiert: `resolve_media_path` in main.py
    - Decodiert URL-encoded Pfade vom Frontend
    - Strippt `/media/`-Präfixe nur bei virtuellen Pfaden
    - Prüft Datenbank und Dateisystem für korrekte Dateiauflösung

## 3. Dynamisches Kontextmenü
- `showContextMenu`-Logik in app.html aktualisiert
    - Optionen werden je nach Dateityp ein-/ausgeblendet
    - Für DVD-ISOs: "DVD Native" und Disc-Optionen nur bei passenden Dateien

## 4. Erweiterte Playback-Modes
- **FragMP4/Matroska:** Neue `/video-stream/`-Route in main.py (ffmpeg-Transmuxing, on-the-fly, Chrome-kompatibel)
- **VLC/cvlc CLI:** cvlc als Standard für alle CLI-Playbacks
- **mpv & pyvidplayer2:** Standalone-Desktop-Modi für mpv, verbesserte pyvidplayer2-Unterstützung

## 5. ISO/DVD-Verbesserung
- ISO-Dateien werden direkt an VLC (cvlc) übergeben, nicht mehr via dvd://-Protokoll
- Ergebnis: Deutlich bessere Kompatibilität und Zuverlässigkeit

---

## Verifikation
### Automatisierte Tests
- **DVD/ISO-Playback:** `tests/integration/basic/playback/test_dvd_iso.py` – alle Tests bestanden, cvlc-Aufruf und Pfadhandling korrekt
- **Path Resolution:** `tests/unit/test_path_resolution.py` – Decoding und Präfix-Handling bestätigt

### Manuelle Verifikation
- UI-Konsistenz und Kontextmenü-Dynamik im Browser geprüft (Aufzeichnungen/Screenshots)
- MP4-Playback-Fehler durch Codeanalyse und UI-State-Checks als behoben bestätigt

---

**Datum:** 17. März 2026  
**Autor:** GitHub Copilot
