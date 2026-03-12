# Logbuch: Integrierter Web-Player mit Engine-Auswahl

## Zielsetzung
Ablösung externer Player-Fenster und Drag-and-Drop-Workarounds durch ein konsistentes, integriertes Erlebnis im "Video"-Tab der Anwendung.

## Funktionale Anforderungen
1. **Player-Auswahl (Selection)**
   - Benutzer kann im Video-Tab zwischen verschiedenen Wiedergabe-Engines wählen:
     - **Chromium Native:** Direkte Nutzung des Browser-eigenen HTML5-Players.
       - Vorteil: Minimale Latenz, keine CPU-Last durch Transcoding.
       - Einschränkung: Nur native Formate (MP4, WebM, OGG).
     - **VLC Integrated (Transcoded):** Nutzung von VLC/FFmpeg im Backend, um den Inhalt live in ein browser-kompatibles Format zu überführen.
       - Vorteil: Hohe Kompatibilität (spielt fast alles ab, inkl. ISO/DVD/MKV).
       - Nachteil: Höhere CPU-Last durch Echtzeit-Transkodierung.

2. **Wiedergabe-Qualität & Performance**
   - Stream soll "sauber" sein (keine Ruckler, korrekter Aspekt-Ratio).
   - Schnelle Startzeit (Buffer-Optimierung).
   - Unterstützung für ISO-Dateien direkt im Web-Player.

3. **UI/UX Anforderungen**
   - Wegfall von Drag-and-Drop Aufforderungen.
   - Auswahl erfolgt direkt über die Medienbibliothek (Sidebar).
   - Player-Zustand (Modus-Auswahl) wird persistent gespeichert.

## Technische Strategie
- **Backend:** Streaming-Endpoint (z.B. Bottle + FFmpeg), Live-Transcoding für "VLC Integrated".
- **Frontend:** Erweiterung des video-player Elements in `app.html` für adaptive Streams (HLS via hls.js) oder direkte MP4-Streams.
- **ISO-Handling:** Hauptfilm via VLC/FFmpeg extrahieren und an Web-Player streamen.

## Ausschlusskriterien
- Keine Nutzung von veralteten NPAPI/ActiveX VLC-Backend-Plugins.
- Keine externen VLC-Fenster mehr im Standard-Workflow.

---
