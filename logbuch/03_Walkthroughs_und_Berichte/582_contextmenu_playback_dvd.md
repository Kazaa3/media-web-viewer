# Logbuch: Context-Menü, Playback-Refinement & DVD Support

## Datum
16. März 2026

---

## Kontext-Menü (Rechtsklick)
- Modernes Glassmorphism-Menü für Videos in Bibliothek/Playlist.
- Direkter Zugriff auf alle Wiedergabe-Modi (Chrome, ffmpeg, mkvmerge, cvlc solo, MediaMTX).
- Backend-Kommunikation über robuste Slugs, Sprachkonflikte vermieden.
- Menü passt sich dynamisch an Bildschirmgrenzen an, global schließbar.

---

## UI-Polishing & Workflow
- Variable currentVideoItem wird global und konsistent für alle Playback-Funktionen genutzt.
- Fehler currentSong undefined und select nicht gefetched in triggerOpenWith behoben.
- Menü-Workflow im Walkthrough dokumentiert.

---

## Debugging JavaScript Errors
- currentSong durch currentVideoItem ersetzt.
- select-Referenz in triggerOpenWith gefixt.
- Player-Logik auditiert, globale Variable für Playback vereinheitlicht.

---

## Playback & DVD Support Integration
- Eel-Server nutzt dynamische Port-Allokation (find_free_port), daher keine Hardcoded-Ports.
- Port-Logging für Startup und automatisierte Tests ergänzt.
- Spezial-Handler für DVD/ISO und VLC-GUI-Fenster vorbereitet.

---

## Verification Plan
- Aktiven Port der Anwendung im Startup loggen.
- http://localhost:<port>/app.html aufrufen.
- Debug & DB Tab prüfen: Startup-Logs und Log-Updates alle 2 Sekunden.
- DVD/ISO-Playback separat testen (Muxing, VLC-GUI).

---

## Kommentar
Ctrl+Alt+M

---

*Siehe Walkthrough für Details zum neuen Menü-Workflow und Playback-Refinement.*
