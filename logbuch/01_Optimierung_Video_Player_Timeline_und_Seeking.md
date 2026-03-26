# Logbuch: Optimierung Video Player Timeline und Seeking

## Ziel
Sicherstellung einer stabilen und reaktionsschnellen Timeline-Steuerung für alle Video-Player-Modi, insbesondere für transkodierte Streams und VLC-HLS-Einstufungen.

---

## Konzept
- Implementierung eines effizienten Event-Handlings für den Seek-Slider, um unnötige Backend-Restarts beim "Scrubbing" (Ziehen des Sliders) zu vermeiden.
- Trennung von UI-Feedback (Dragging) und tatsächlichem Seek-Commit (Release).

---

## Umsetzung
- **Event-Refactor**: `seekSlider` nutzt nun `input` für die Live-Anzeige der Zeit im UI und `change` für das tatsächliche Absenden des Seek-Befehls an den Player.
- **Backend-Schonung**: Durch den Wechsel auf `change` wird bei Streaming-Modis (VLC Embedded, FFmpeg Transcode) nur noch ein einziger Backend-Restart ausgelöst, statt hunderte während der Mausbewegung.
- **Transcode-Seeking**: Die Hot-Reload-Logik in `app.html` (Zusatz von `?ss=TIME`) wurde für native Streams und HLS verifiziert.

---

## Vorteile
- Massive Reduktion der Serverlast bei Nutzung der Timeline.
- Verhindert Port-Kollisionen und Subprozess-Staus durch zu viele gleichzeitige VLC/FFmpeg-Instanzen.
- Bessere User Experience durch flüssiges Zeit-Feedback während des Slidings.

---

## Status
- Erledigt / Implementiert

**Stand:** 26. March 2026

---

## Kontext & Verweise
- Scripts: `scripts/logbook_manager.py` (zur Erstellung genutzt)
- Code: `web/app.html` (Funktion `startEmbeddedVideo`, `seekVideo`)
