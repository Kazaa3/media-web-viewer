# Logbuch Eintrag 026: VLC Embedded Integration (Popup-frei)

## Datum: 2026-03-18
## Status: IMPLEMENTED / VERIFIED

### Zielstellung
Eliminierung des externen VLC-Popup-Fensters bei der Wiedergabe von DVDs und ISOs. Die Kompatibilität von VLC soll erhalten bleiben, aber das Video soll direkt im Browser-Tab des Video-Players erscheinen.

### Die Lösung: VLC als Background-Streamer
Anstatt VLC als Desktop-Applikation zu starten, wird er nun als "Headless Stream Engine" genutzt:
1.  **Headless Mode**: VLC startet im Hintergrund (`-I dummy`) ohne eigenes Fenster.
2.  **Real-time Transcoding**: Mittels `--sout` wird der DVD/ISO-Datenstrom live in einen Browser-kompatiblen HTTP-FLV-Stream umgewandelt (`h264/mp3`).
3.  **Browser-Ingress**: Der integrierte Video.js Player empfängt diesen Stream über `http://localhost:8099/vlc.flv`.

### Vorteile
- **Seamless UI**: Kein Wechsel zwischen App-Fenstern mehr nötig.
- **Volle Kompatibilität**: Alle Formate (ISO, BIN, VIDEO_TS), die VLC lesen kann, sind nun "embedded" verfügbar.
- **Singleton Guard**: Die bestehende `pkill` Logik stellt sicher, dass auch der Hintergrund-Streamer immer nur in einer Instanz läuft.

### Bedienung
- **Auto-Modus**: DVDs werden nun standardmäßig im eingebetteten Player (via VLC-Stream) gestartet.
- **Manueller Wechsel**: Über das Dropdown `VLC (Desktop/Embedded)` → `Embedded VLC Stream` kann dieser Modus erzwungen werden.
- **Fallback**: Der klassische Desktop-VLC bleibt als Option (`Desktop VLC (Extern)`) für Power-User erhalten.

Status: **SUCCESSFULLY DEPLOYED**
