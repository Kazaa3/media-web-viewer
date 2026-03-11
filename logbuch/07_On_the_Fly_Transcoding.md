<!-- Category: Development -->
<!-- Title_DE: 06 On-the-Fly Transcoding: Grenzen überwinden -->
<!-- Title_EN: 06 On-the-Fly Transcoding: Overcoming Limits -->
<!-- Summary_DE: Web-Kompatibilität für jedes Format durch Echtzeit-Konvertierung mit FFmpeg. -->
<!-- Summary_EN: Web compatibility for any format through real-time conversion with FFmpeg. -->
<!-- Status: COMPLETED -->
<!-- Anchor: 07_On_the_Fly_Transcoding -->
<!-- Redundancy: Section covers real-time transcoding, FFmpeg, caching, latency. -->

# 06 On-the-Fly Transcoding: Grenzen überwinden

Trotz der Format-Vielfalt in Entry 04 blieb ein Problem: Browser sind wählerisch. Formate wie ALAC oder High-Res FLAC werden oft nicht nativ unterstützt.

### Die Lösung: Streamen statt Konvertieren
Anstatt den Nutzer zu zwingen, seine Sammlung manuell umzuwandeln, integriert die App **Echtzeit-Transcoding**:
- Das Backend erkennt inkompatible Codecs beim Start des Playbacks.
- Ein **FFmpeg-Prozess** wird gestartet, der die Datei in Echtzeit in einen kompatiblen Stream (z. B. FLAC oder OGG) umwandelt.
- Dieser Stream wird direkt an den Bottle-Server weitergereicht und im Browser abgespielt.

### Technische Finesse
- **Caching:** Einmal transkodierte Inhalte landen im `.cache`-Verzeichnis, um CPU-Zyklen bei wiederholtem Abspielen zu sparen.
- **Latenz:** Durch effizientes Piping startet die Musik fast ohne spürbare Verzögerung.

Damit löst der *Media Web Viewer* das "Format-Problem" endgültig und wird zum Allesfresser für Audioinhalte.

<!-- lang-split -->

# 06 On-the-Fly Transcoding: Overcoming Limits

Despite the format diversity documented in entry 04, one problem remained: browsers are picky. Formats like ALAC or high-res FLAC are often not natively supported.

### The Solution: Streaming instead of Converting
Instead of forcing the user to manually convert their collection, the app integrates **real-time transcoding**:
- The backend detects incompatible codecs when playback starts.
- An **FFmpeg process** is started, converting the file in real-time into a compatible stream (e.g., FLAC or OGG).
- This stream is passed directly to the Bottle server and played in the browser.

### Technical Finesse
- **Caching:** Once transcoded, content ends up in the `.cache` directory to save CPU cycles during repeated playback.
- **Latency:** Efficient piping allows the music to start with almost no noticeable delay.

With this, the *Media Web Viewer* finally solves the "format problem" and becomes a universal player for audio content.
