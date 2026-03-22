# Logbuch Eintrag 027: VLC HLS Streaming Upgrade (V1.34)

## Datum: 2026-03-18
## Status: COMPLETED / OPTIMIZED

### Zielstellung
Das bisherige HTTP-FLV Streaming für eingebettete DVDs wurde durch den moderneren HLS-Standard (HTTP Live Streaming) ersetzt. Ziel war eine stabilere Seek-Performance und bessere Browser-Native-Integration.

### Implementierte HLS-Architektur
1.  **HLS Segmenter**: VLC wird nun im Hintergrund mit der `livehttp` Access-Methode gestartet. Dies erzeugt rotierende `.ts`-Segmente und eine `.m3u8` Playlist im Verzeichnis `/tmp/vlc_hls/`.
2.  **HLS Live-Proxy**: Im Backend wurde eine neue Eel/Bottle-Route `/vlc-hls-live/` implementiert. Diese fungiert als High-Performance Proxy, der die Segmente mit den korrekten MIME-Types (`application/x-mpegURL` und `video/MP2T`) an den Browser liefert.
3.  **Video.js Integration**: Der Video-Player erkennt den HLS-Datenstrom automatisch und schaltet in den adaptiven Streaming-Modus.

### Vorteile gegenüber FLV
- **Puffer-Management**: HLS ist robuster gegenüber Netzwerk-Lags.
- **Seek-Support**: Durch die Segmentierung ist ein präziseres Springen im Zeitstrahl möglich (sofern die Segmente generiert sind).
- **Chrome Native Alignment**: HLS ist der bevorzugte Standard für moderne Web-Wiedergabe.

### UI Konfiguration
- **Player-Engine**: `VLC Player (DVD/ISO)`
- **Wiedergabe-Modus**: `VLC Embedded HLS (Popup-frei)`

Dies schließt die Integration von DVDs und ISOs als erstklassige Bürger im Web-Viewer ab.
