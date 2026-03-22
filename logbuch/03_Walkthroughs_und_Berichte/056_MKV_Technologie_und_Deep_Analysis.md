<!-- Category: Documentation -->
<!-- Title_DE: MKV-Technologie & Deep Analysis -->
<!-- Title_EN: MKV Technology & Deep Analysis -->
<!-- Summary_DE: Tiefenanalyse von Matroska-Containern: MKVToolNix-Integration, Stream-Mapping und Kapitel-Extraktion. -->
<!-- Summary_EN: Deep analysis of Matroska containers: MKVToolNix integration, stream mapping and chapter extraction. -->
<!-- Status: ACTIVE -->

# MKV-Technologie & Deep Analysis

## Die "Matroska"-Herausforderung
MKV (Matroska) ist kein einfacher Codec, sondern ein extrem flexibler Container, der beliebig viele Audio-, Video- und Untertitel-Streams enthalten kann. Für **dict - Web Media Player & Library** war es wichtig, nicht nur die Hülle zu erkennen, sondern den Inhalt präzise zu analysieren.

## MKVToolNix Integration
Ein Meilenstein in der Entwicklung war die Integration von **MKVToolNix** (insbesondere `mkvmerge` und `mkvinfo`) als Ergänzung zu FFmpeg:
- **Stream-Identifikation:** MKVToolNix liefert oft detailliertere Informationen über Sprach-Tags und Standard-Streams als FFmprobe.
- **Deep Scans:** Ermöglicht das Auslesen von Anhängen (z.B. Cover-Bilder oder Fonts), die tief im Matroska-Container eingebettet sind.

## Kapitel & Navigation
MKV-Dateien (besonders bei Filmen und Konzert-Aufnahmen) sind oft in Kapitel unterteilt.
- **Kapitel-Extraktion:** Dict nutzt spezialisierte Parser, um die Kapitel-Namen und Zeitstempel direkt aus dem Container auszulesen.
- **UI-Integration:** Diese Kapitel werden im Player angezeigt, was ein gezieltes Springen innerhalb großer Videodateien erlaubt.

## Optimiertes Stream-Mapping
Bei Dateien mit mehreren Tonspuren (z.B. Deutsch/Englisch/Kommentar) ist das korrekte Mapping entscheidend.
- **Standard-Spuren:** Dict erkennt das `default`-Flag im MKV-Header und priorisiert diese Spur beim Transcoding.
- **Sprach-Präferenz:** Durch die Analyse der Sprach-Tags (z.B. `ger`, `eng`) kann das System automatisch die bevorzugte Sprache des Nutzers wählen.

*MKV ist für dict mehr als nur eine Datei – es ist ein Container voller Informationen, die wir bis ins letzte Detail auswerten.*

<!-- lang-split -->

# MKV Technology & Deep Analysis

## The "Matroska" Challenge
MKV (Matroska) is not just a simple codec, but an extremely flexible container that can contain any number of audio, video and subtitle streams. For **dict - Web Media Player & Library**, it was important not only to recognize the envelope, but to analyze the content precisely.

## MKVToolNix Integration
A milestone in development was the integration of **MKVToolNix** (specifically `mkvmerge` and `mkvinfo`) as a supplement to FFmpeg:
- **Stream Identification:** MKVToolNix often provides more detailed information about language tags and default streams than FFprobe.
- **Deep Scans:** Allows for the reading of attachments (e.g., cover images or fonts) that are embedded deep within the Matroska container.

## Chapters & Navigation
MKV files (especially for movies and concert recordings) are often divided into chapters.
- **Chapter Extraction:** Dict uses specialized parsers to read chapter names and timestamps directly from the container.
- **UI Integration:** These chapters are displayed in the player, allowing for targeted jumping within large video files.

## Optimized Stream Mapping
For files with multiple audio tracks (e.g., German/English/Commentary), correct mapping is crucial.
- **Default Tracks:** Dict recognizes the `default` flag in the MKV header and prioritizes this track during transcoding.
- **Language Preference:** By analyzing the language tags (e.g., `ger`, `eng`), the system can automatically select the user's preferred language.

*For dict, MKV is more than just a file – it's a container full of information that we evaluate down to the smallest detail.*
