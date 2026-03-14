<!-- Category: Documentation -->
<!-- Title_DE: Format-Diversität: Audio & Video -->
<!-- Title_EN: Format Diversity: Audio & Video -->
<!-- Summary_DE: Unterstützung für verschiedenste Medienformate, Implementierung des Diversity-Tests und präzise Kategorisierung. -->
<!-- Summary_EN: Support for various media formats, implementation of the diversity test and precise categorization. -->
<!-- Status: ACTIVE -->

# Format-Diversität: Audio & Video

## Das Ziel: "Play Anything"
Eine der größten Stärken von **dict - Web Media Player & Library** ist seine Robustheit gegenüber einer Vielzahl von Medienformaten. Anstatt sich auf MP3 und MP4 zu beschränken, unterstützt dict das gesamte Spektrum moderner und historischer Codecs.

## Kategorisierung & Logik
Dict erkennt automatisch, um welchen Typ von Medium es sich handelt. Dies geschieht durch eine Kombination aus:
1.  **Container-Analyse:** Erkennung von MKV, OGG, FLAC, M4A, etc.
2.  **Stream-Inspektion:** Unterscheidung zwischen reinen Audiostreams und Videostreams via FFmpeg/PyMediaInfo.
3.  **Heuristiken:** Logik zur Identifizierung von:
    - **Musik:** Kurze Tracks in Musik-Formaten.
    - **Hörbücher:** Lange Dateiblöcke (oft M4B) mit Kapitel-Marken.
    - **Filme:** Videodateien mit hoher Bitrate und Auflösung.
    - **Serien:** Dateien mit Staffel- und Episoden-Mustern im Dateinamen.

## Die "Diversity Test" Suite
Um die Stabilität dauerhaft zu garantieren, wurde ein spezieller Benchmark-Test implementiert:
- **Test-Samples:** Eine Sammlung von Dateien mit unterschiedlichsten Eigenschaften (VBR vs. CBR, verschiedene Sample-Raten, Multi-Channel Audio).
- **XZ-Diversity:** Tests mit komprimierten Test-Paketen, um eine breite Palette an Randfällen abzudecken, ohne das Repository-Volumen unnötig aufzublähen.
- **Validierung:** Der Test stellt sicher, dass alle Metadaten korrekt extrahiert werden und das Playback initialisiert werden kann.

## Unterstützte Formate (Auszug)
- **Lossless Audio:** FLAC, ALAC (via Transcoding), WAV.
- **Lossy Audio:** MP3, Opus, Vorbis, AAC.
- **Video:** H.264, H.265 (HEVC), VP9 in MKV/MP4 Containern.
- **Spezialformate:** Opus in OGG, M4B mit Kapiteln.

*Durch diese enorme Diversität ist dict das ultimative Werkzeug für Nutzer mit umfangreichen und historisch gewachsenen Mediensammlungen.*

<!-- lang-split -->

# Format Diversity: Audio & Video

## The Goal: "Play Anything"
One of the greatest strengths of **dict - Web Media Player & Library** is its robustness against a wide variety of media formats. Instead of limiting itself to MP3 and MP4, dict supports the entire spectrum of modern and historical codecs.

## Categorization & Logic
Dict automatically recognizes the type of medium. This is done through a combination of:
1.  **Container Analysis:** Detection of MKV, OGG, FLAC, M4A, etc.
2.  **Stream Inspection:** Distinguishing between pure audio streams and video streams via FFmpeg/PyMediaInfo.
3.  **Heuristics:** Logic to identify:
    - **Music:** Short tracks in music formats.
    - **Audiobooks:** Long files (often M4B) with chapter markers.
    - **Movies:** Video files with high bitrate and resolution.
    - **Series:** Files with season and episode patterns in the file name.

## The "Diversity Test" Suite
To guarantee stability in the long term, a special benchmark test was implemented:
- **Test Samples:** A collection of files with a wide variety of properties (VBR vs. CBR, various sample rates, multi-channel audio).
- **XZ Diversity:** Tests with compressed test packages to cover a wide range of edge cases without unnecessarily inflating the repository size.
- **Validation:** The test ensures that all metadata is correctly extracted and playback can be initialized.

## Supported Formats (Excerpt)
- **Lossless Audio:** FLAC, ALAC (via transcoding), WAV.
- **Lossy Audio:** MP3, Opus, Vorbis, AAC.
- **Video:** H.264, H.265 (HEVC), VP9 in MKV/MP4 containers.
- **Special Formats:** Opus in OGG, M4B with chapters.

*Through this enormous diversity, dict is the ultimate tool for users with extensive and historically grown media collections.*
