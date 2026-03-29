# Walkthrough: Advanced Playback, MediaMTX Integration & UI Debugging

## Datum
16. März 2026

---

## Feature Overview
- **MediaMTX Integration:** Neue Option im Video-Modus, HLS/WebRTC Streaming via Docker Compose.
- **Playback Modes:** Alle Modi transparent benannt (z.B. "ffmpeg mit cvlc", "MediaMTX (HLS)", "Chrome Native").
- **Hardware Detection:** Desktop-Mode erkennt HDD/SSD/PCIe/Netzwerk.
- **Analyse/Write Modes:** Analyse prüft nur, Write bearbeitet Tags.
- **Drag & Drop Playlist:** Implementiert, unterstützt externes Öffnen.
- **Log Level:** CRITICAL, ERROR, WARNING, INFO, DEBUG – Backend/Frontend synchronisiert.
- **UI/UX:** Dropdown, Kontextmenü, global cats-Definition, showToast-Handler, deduplizierte i18n.json.

---

## Debugging & Fixes
- **cats:** Globale Definition in app.html, Fehler behoben.
- **showToast:** Implementiert, Fehler behoben.
- **Log Level:** Backend/Frontend synchronisiert, CRITICAL hinzugefügt.
- **Playback Mode Labels:** Hybrid-Modi umbenannt, konsistent.
- **i18n.json:** Dedupliziert, Syntaxfehler behoben, Keys standardisiert.

---

## Verification Results
- **Playback Modes:** Alle Modi funktionieren, MediaMTX-Streams laufen, Chrome Native unterstützt Seeking.
- **Hardware Detection:** Alle Typen korrekt erkannt.
- **Analyse/Write:** Funktioniert wie spezifiziert.
- **UI:** Dropdown, Kontextmenü, Toasts, Player-Switch – alles verifiziert.
- **i18n.json:** Keine doppelten Keys, Syntax OK.

---

## Proof of Work
- Siehe logbuch/2026-03-16_mediamtx_openwith_integration.md für MediaMTX.
- Siehe logbuch/2026-03-16_analyse_write_mode.md für Analyse/Write.
- Siehe logbuch/2026-03-16_advanced_playback_modes_hardware_detection.md für Taskplan.

---

## Abschluss
Alle Features und Fixes sind implementiert und verifiziert. Der Code ist bereit für Review und Release.

---

*Für Details siehe die jeweiligen logbuch-Einträge und walkthrough.md.*
