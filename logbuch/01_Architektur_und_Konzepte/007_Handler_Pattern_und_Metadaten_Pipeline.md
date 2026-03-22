<!-- Category: Documentation -->
<!-- Title_DE: Handler-Pattern & Metadaten-Pipeline -->
<!-- Title_EN: Handler Pattern & Metadata Pipeline -->
<!-- Summary_DE: Architektur des Kern-Parsers, Implementierung des Handler-Patterns und die Orchestrierung verschiedener Parser-Tools. -->
<!-- Summary_EN: Core parser architecture, Handler Pattern implementation, and orchestration of various parser tools. -->
<!-- Status: ACTIVE -->

# Handler-Pattern & Metadaten-Pipeline

## Die Architektur der Flexibilität
Eines der markantesten Merkmale von **dict** ist die Fähigkeit, unterschiedlichste Medienformate (Audio, Video, E-Books) einheitlich zu verarbeiten. Dies wird durch zwei Konzepte ermöglicht:

### 1. Das Handler-Pattern
Anstatt eines monolithischen Parsers nutzt dict eine Kette von spezialisierten Handlern. Jeder Handler (z. B. `AudioTagHandler`, `FFprobeHandler`) entscheidet selbstständig, ob er eine Datei verarbeiten kann.
- **Vorteil:** Neue Tools (wie `isoparser` für DVDs oder `tinytag` für Audio) können einfach als neue Glieder in die Kette eingefügt werden, ohne bestehenden Code zu gefährden.
- **Fail-Safe:** Wenn ein spezialisierter Parser (z. B. Mutagen) scheitert, übernimmt ein generischer Fallback-Handler (z. B. FFprobe), um zumindest Basisdaten wie die Dauer zu extrahieren.

### 2. Die Metadaten-Pipeline
Die Metadaten fließen durch verschiedene Stufen:
1.  **Detection:** Bestimmung des Dateityps (nicht nur nach Endung, sondern via Magic Bytes/FFprobe).
2.  **Extraction:** Paralleles Auslesen von Tags, Covern und technischen Streams.
3.  **Sanitization:** Bereinigung der Dictionary-Keys zu einem einheitlichen Schema für das UI.
4.  **Enrichment:** Ergänzung durch Scraper (Discogs, ISBN-APIs).

## Orchestrierung der Tools
Dict nutzt das Beste aus verschiedenen Welten:
- **Mutagen/TinyTag:** Für präzise Audio-Tags und Kapitellisten.
- **FFprobe:** Als universelles Schweizer Taschenmesser für Video-Container und technische Metadaten.
- **PyMediaInfo:** Für detaillierte Stream-Analysen (Bitrate, Codecs).

*Diese Architektur garantiert, dass dict auch bei exotischen Formaten stabil bleibt und immer ein Maximum an Informationen liefert.*

<!-- lang-split -->

# Handler Pattern & Metadata Pipeline

## The Architecture of Flexibility
One of the most distinctive features of **dict** is the ability to process a wide variety of media formats (audio, video, e-books) uniformly. This is made possible by two concepts:

### 1. The Handler Pattern
Instead of a monolithic parser, dict uses a chain of specialized handlers. Each handler (e.g., `AudioTagHandler`, `FFprobeHandler`) independently decides whether it can process a file.
- **Advantage:** New tools (such as `isoparser` for DVDs or `tinytag` for audio) can easily be inserted as new links in the chain without compromising existing code.
- **Fail-Safe:** If a specialized parser (e.g., Mutagen) fails, a generic fallback handler (e.g., FFprobe) takes over to extract at least basic data such as duration.

### 2. The Metadata Pipeline
The metadata flows through various stages:
1.  **Detection:** Determination of the file type (not just by extension, but via magic bytes/FFprobe).
2.  **Extraction:** Parallel reading of tags, covers, and technical streams.
3.  **Sanitization:** Cleaning of dictionary keys to a uniform schema for the UI.
4.  **Enrichment:** Addition by scrapers (Discogs, ISBN APIs).

## Orchestrating the Tools
Dict uses the best of different worlds:
- **Mutagen/TinyTag:** For precise audio tags and chapter lists.
- **FFprobe:** As a universal Swiss army knife for video containers and technical metadata.
- **PyMediaInfo:** For detailed stream analysis (bitrate, codecs).

*This architecture guarantees that dict remains stable even with exotic formats and always provides a maximum of information.*
