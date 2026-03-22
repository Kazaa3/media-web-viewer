# HLS → video.js: Nachteile & Fallstricke

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
