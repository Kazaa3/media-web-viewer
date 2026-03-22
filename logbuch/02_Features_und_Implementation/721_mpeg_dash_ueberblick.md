# MPEG-DASH: Überblick, Stärken & Schwächen

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
