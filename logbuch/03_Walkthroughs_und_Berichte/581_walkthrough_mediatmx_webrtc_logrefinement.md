# Walkthrough: MediaMTX WebRTC & Log Refinement

## Datum
16. März 2026

---

## 🎬 Fortgeschrittene Wiedergabe

### MediaMTX Expansion
- **Protokolle:** Neben HLS wird nun auch WebRTC (WHEP) unterstützt, Latenzen <100ms.
- **Konfiguration:** Automatische Auswahl zwischen hls und webrtc im Selektor.

### "Öffnen mit" (Open With)
- Neuer Button im Video-Tab startet Medium explizit im gewählten Modus (z.B. cvlc solo, mkvmerge Pipe).
- Backend-API open_video übernimmt Routing für alle spezialisierten Modi.

### VLC Pipe Varianten
- Neben ffmpeg kann mkvmerge als Engine für Remux-Stream zu VLC genutzt werden.
- Modus cvlc solo startet VLC direkt ohne Pipe-Overhead.

---

## 🛠️ Debugging & Stabilität

### Log-Level Fixes
- **Visibility:** Bestätigungsmeldung beim Log-Level-Wechsel wird vor Umstellung geloggt, bleibt sichtbar.
- **Support:** Alle 5 Stufen (DEBUG, INFO, WARNING, ERROR, CRITICAL) synchronisiert.
- **Persistenz:** Log-Level-Änderungen werden in der Konfiguration gespeichert.

### i18n Expansion
- Alle neuen Modi und UI-Elemente sind in Deutsch und Englisch lokalisiert.

---

## ✅ Verifizierungsergebnisse
- **Log-Level:** Mit standalone-Skript verifiziert, alle Stufen schalten korrekt um.
- **MediaMTX WebRTC:** Frontend-Integration für webrtc Modus abgeschlossen.
- **Open With:** Getestet für alle Varianten (ffmpeg, mkvmerge, cvlc, mediamtx).
- **mkvmerge:** Erfolgreich als alternative Remux-Engine integriert.

---

## Open With Interface
Schematisch: Der neue 'Öffnen mit' Button neben dem Modus-Selektor

---

## Kommentar
Ctrl+Alt+M

---

*Siehe logbuch/2026-03-16_implementation_plan_playback_log.md für Details zum Implementation Plan.*
