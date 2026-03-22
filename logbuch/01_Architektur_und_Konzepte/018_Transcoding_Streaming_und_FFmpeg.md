<!-- Category: Documentation -->
<!-- Title_DE: Transcoding, Streaming & FFmpeg -->
<!-- Title_EN: Transcoding, Streaming & FFmpeg -->
<!-- Summary_DE: Die technische Engine hinter dem Playback: FFmpeg-Optimierung, On-the-Fly Transcoding und Streaming-Strategien. -->
<!-- Summary_EN: The technical engine behind playback: FFmpeg optimization, on-the-fly transcoding and streaming strategies. -->
<!-- Status: ACTIVE -->

# Transcoding, Streaming & FFmpeg

## Die Herausforderung des Web-Playbacks
Moderne Browser sind wählerisch: Während sie MP3 und H.264 nativ abspielen, scheitern sie oft an High-Fidelity-Formaten wie **ALAC (Apple Lossless)**, **FLAC** oder spezialisierten Containern wie **WMA**. Für **dict - Web Media Player & Library** war die Lösung von Anfang an klar: **On-the-Fly Transcoding.**

## Die FFmpeg-Engine
FFmpeg bildet das Herzstück unseres Transcoders. Wir nutzen es nicht nur zur Analyse, sondern zur Echtzeit-Umwandlung von Audio-Streams.

### Optimierungen & Parameter
Um Latenzen beim Start eines Songs zu minimieren, wurden die FFmpeg-Parameter über mehrere Iterationen verfeinert:
- **`libmp3lame`:** Als universeller Ziel-Codec für Audio-Streaming.
- **Bitrate-Steuerung:** Dynamische Anpassung (Standard 192k oder 320k), um ein Gleichgewicht zwischen Qualität und Bandbreite zu finden.
- **Pipe-Streaming:** FFmpeg streamt die Daten direkt in den Bottle-Response-Body, was Speicherplatz spart und sofortiges Seek-Verhalten ermöglicht.

### Performance & Cache
Ein Meilenstein war die Einführung der **Transcoding-Optimierung**:
- **Caching:** Bereits transcodierte Fragmente werden in `media/.cache` zwischengespeichert, um wiederholte CPU-Last zu vermeiden.
- **Fragmentierung:** Unterstützung von fragmentiertem MP4 für stabileres Video-Streaming.

## Sonderfall: Hörbücher (M4B)
Hörbücher stellen besondere Anforderungen. Sie sind oft Stunden lang und besitzen Kapitel-Metadaten.
- **Kapitel-Splitting:** FFmpeg erlaubt uns, gezielt in Kapitel zu springen, ohne die gesamte 10-Stunden-Datei vorab zu laden.
- **Fehlerbehandlung:** Robuste Behandlung von 24-bit PCM und unüblichen Sample-Raten, die früher zu Abstürzen führten.

*Durch die kontinuierliche Verfeinerung der FFmpeg-Integration bietet dict heute ein nahtloses Playback-Erlebnis, unabhängig vom Quellformat.*

<!-- lang-split -->

# Transcoding, Streaming & FFmpeg

## The Challenge of Web Playback
Modern browsers are picky: while they play MP3 and H.264 natively, they often fail with high-fidelity formats like **ALAC (Apple Lossless)**, **FLAC**, or specialized containers like **WMA**. For **dict - Web Media Player & Library**, the solution was clear from the start: **on-the-fly transcoding.**

## The FFmpeg Engine
FFmpeg forms the heart of our transcoder. We use it not only for analysis, but for the real-time conversion of audio streams.

### Optimizations & Parameters
To minimize latency when starting a song, the FFmpeg parameters were refined over several iterations:
- **`libmp3lame`:** As a universal target codec for audio streaming.
- **Bitrate Control:** Dynamic adjustment (standard 192k or 320k) to find a balance between quality and bandwidth.
- **Pipe-Streaming:** FFmpeg streams the data directly into the Bottle response body, which saves storage space and enables immediate seek behavior.

### Performance & Cache
A milestone was the introduction of **transcoding optimization**:
- **Caching:** Already transcoded fragments are cached in `media/.cache` to avoid repeated CPU load.
- **Fragmentation:** Support for fragmented MP4 for more stable video streaming.

## Special Case: Audiobooks (M4B)
Audiobooks pose special requirements. They are often hours long and have chapter metadata.
- **Chapter Splitting:** FFmpeg allows us to specifically jump into chapters without preloading the entire 10-hour file.
- **Error Handling:** Robust handling of 24-bit PCM and unusual sample rates that previously caused crashes.

*Through the continuous refinement of the FFmpeg integration, dict today offers a seamless playback experience, regardless of the source format.*
