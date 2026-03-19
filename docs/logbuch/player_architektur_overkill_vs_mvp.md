---

## MPEG-DASH: Überblick, Stärken & Schwächen

**Was ist DASH?**
- Steht für „Dynamic Adaptive Streaming over HTTP“
- Server encodiert Video in mehrere Bitraten/Resos, schneidet in Segmente, beschreibt alles in einer MPD-Manifestdatei (XML)
- Player lädt das MPD, holt je nach Bandbreite das passende Segment (ABR)

**Stärken:**
- Codec-agnostisch: H.264, HEVC, VP9, AV1 usw. ohne Protokolländerung
- Gute Low-Latency-Optionen: kurze Segmente, Chunked Transfer, CMAF → geringere Latenz als klassisches HLS, sehr gut für Live/Interaktiv
- Standardisiert (ISO/MPEG), viel genutzt bei großen Plattformen und DRM-Inhalten

**Schwächen (für Browser-Apps):**
- Schlechtere Apple-Kompatibilität: iOS/tvOS/macOS haben HLS nativ, DASH nur via JS-Player (dash.js, video.js-Plugin)
- Komplexeres Setup: MPD, Adaptation Sets, mehr Optionen → mehr Implementierungs- und Testaufwand als HLS

**Praxis für deine App:**
- DASH ist spannend als Zusatz-Modus (z.B. für AV1, Low-Latency, Overkill-Player)
- HLS bleibt der pragmatische Default für Browser-Playback
---

## MediaMTX als Streaming-Router: Kurzüberblick

MediaMTX (früher rtsp-simple-server) ist der zentrale „Streaming-Router“ zwischen FFmpeg/VLC/Kameras und Browser/Player:

- **Eingänge:** RTSP, RTMP, SRT, WebRTC, HLS, MPEG-TS/RTP
- **Ausgänge:** RTSP, RTMP, SRT, HLS, WebRTC (z.B. für VLC, ffplay, Browser, OBS)
- **Features:**
  - Automatisches Protokoll-Umschalten (z.B. RTSP rein, HLS/WebRTC raus)
  - Mehrere Pfade/Streams parallel
  - Aufnahme (fMP4/TS)
  - HTTP-API für Überwachung und Konfiguration

**Praxis für deine App:**
- Per ffmpeg eine Datei/Kamera als RTSP zu MediaMTX schicken
- Den Stream dann wahlweise konsumieren:
  - Im Browser als HLS/WebRTC
  - In VLC/mpv/ffplay als RTSP/SRT/RTMP
- Kein eigener komplexer Streaming-Server nötig – MediaMTX übernimmt das Routing und Protokollhandling.
# Overkill-Player vs. MVP-Player (MVP-Pattern)

**Ziel:**
Eine Architektur, die sowohl einen maximal flexiblen Orchestrator-Player als auch ein schlankes, testbares MVP-Modul ermöglicht – beide auf derselben Backend-Logik (Model–View–Presenter).

---

## 1. Gemeinsame Architektur (MVP-Pattern)
- **Model:**
  - `play_plan` (mode, url, meta), Status (playing, paused, error), Client-Fähigkeiten (HLS, DASH, MP4)
- **View:**
  - Video-Element/video.js, UI-Buttons, Modus/Qualität, Fehleranzeigen
- **Presenter:**
  - Ruft `get_play_plan()` im Backend, entscheidet Source/Library, reagiert auf User- und Player-Events

---

## 2. Overkill-Player (Maximalausbau)
- **Backend:**
  - `get_play_plan(item, clientCaps)` → { mode, protocol, url, extras }
  - Unterstützt: http-mp4, hls-ts, hls-fmp4, dash-fmp4, vlc-file, vlc-dvd, vlc-rtsp, pyvlc
  - Spezialfälle: PAL-DVD ISO/MKV → je nach Policy HLS oder VLC
- **JS (z.B. player_full.js):**
  - Presenter erkennt alle Protokolle, Client-Fähigkeiten, Modus-Umschalter, anpassbare Controls
  - View: video.js + hls.js + dash.js, Status-Banner, Codec/Reso-Info

---

## 3. MVP-Player (später mvp.js)
- **Ziel:** klein, stabil, testbar; nutzt dasselbe Backend, aber nur 1–2 Modi
- **Unterstützt:**
  - Pflicht: http-mp4
  - Optional: hls-ts oder hls-fmp4
  - Kein DASH, kein RTSP, kein VLC, keine PAL-DVD-Sonderfälle
- **Presenter:**
  - Holt `plan = get_play_plan(..., client="browser-mvp")`
  - Nur MP4/HLS werden akzeptiert, Rest → Fehler
- **Beispiel-JS:**

```js
class MvpPlayerPresenter {
  constructor(view) { this.view = view; }
  async play(item) {
    const plan = await eel.get_play_plan(item.relpath, 'browser-mvp')();
    if (plan.mode === 'http-mp4') {
      this.view.setSource(plan.url, 'video/mp4');
    } else if (plan.mode.startsWith('hls')) {
      this.view.setSource(plan.url, 'application/x-mpegURL');
    } else {
      this.view.showError('Dieser Titel ist im MVP-Player nicht abspielbar.');
    }
  }
}
class MvpPlayerView {
  constructor(videoElementOrVideoJs) { this.player = videoElementOrVideoJs; }
  setSource(url, mime) {
    this.player.src({ src: url, type: mime });
    this.player.play();
  }
  showError(msg) { alert(msg); }
}
```

- Im UI: Tab „Standard-Player (MVP)“ → mvp.js, Tab „Advanced-Player (Overkill)“ → player_full.js

---

## 4. Vorbereitung für spätere Trennung
- Striktes MVP-Pattern: keine Logik im DOM, alles im Presenter
- Backend liefert immer einen play_plan
- Trenne:
  - player_core.js → gemeinsame Hilfen
  - player_mvp.js → reduziert, nur MP4/HLS
  - player_full.js → lädt Dash, RTSP, VLC-Integration usw.

---

## 5. PAL-DVD-Speziallogik
- Overkill:
  - Presenter zeigt bei PAL-DVD (ISO/MKV) alle Modi: DVD in VLC, HLS-Stream, ggf. Direkt in VLC
- MVP:
  - Sieht nur das Ergebnis nach Konvertierung (H.264-MP4/HLS), keine Menüs, keine ISO-Buttons

---


**Fazit:**
- Overkill-Player: maximal flexibel, alle Pfade, alle Features
- MVP-Player: klein, stabil, testbar, gleiche Architektur, nur MP4/HLS
- Spätere Erweiterung/Reduktion jederzeit möglich durch klare Trennung von Model, View, Presenter

---

## HLS → video.js: Nachteile & Fallstricke

**Technische Nachteile von HLS:**
- **Höhere Latenz:** Klassisches HLS (6s-Segmente, 3er-Puffer) führt zu 15–30 s Delay – für Live/Interaktiv suboptimal.
- **Segment-Overhead & CPU/IO-Last:** Viele kleine Segmente → mehr HTTP-Requests, Cache-Last, ggf. höhere CPU-Last (mehr Keyframes).
- **Codec-/Format-Einschränkungen:** HLS ist primär für H.264/AAC optimiert; HEVC/AV1/VP9 sind mit HLS weniger verbreitet als mit DASH.

**Spezifische Punkte mit video.js:**
- **MSE-Abhängigkeit:** video.js nutzt für HLS MSE; alte Browser ohne MSE (z.B. IE11) können kein HLS.
- **Setup-/Größen-Overhead:** HLS braucht http-streaming im Bundle, was JS-Bundle und Konfiguration vergrößert.
- **ABR-Heuristiken:** Die Auto-Qualitätswahl ist konservativ, nimmt oft niedrigere Qualitäten, um Buffering zu vermeiden.
- **Browser-Eigenheiten/Bugs:** Es gibt immer wieder Issues mit bestimmten Chrome-Versionen, Source-Reihenfolgen oder Initialisierung.

**Wann HLS mit video.js trotzdem Sinn ergibt:**
- VOD + Adaptive Bitrate, viele Clients, auch Apple-Geräte → HLS ist der pragmatische Standard.
- Deine App kann mit etwas mehr Komplexität leben (Transcoding, Segmentierung), dafür bekommst du stabile Streams, adaptive Qualität und breite Kompatibilität.

**Kurz:** Für deine Architektur ist „HLS → video.js“ absolut legitim; du musst nur Latenz, Bundle-Größe und ABR/Edge-Cases im Hinterkopf behalten.
