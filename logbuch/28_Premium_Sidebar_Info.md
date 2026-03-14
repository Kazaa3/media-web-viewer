<!-- Category: UI -->
<!-- Title_DE: Premium Sidebar Info -->
<!-- Title_EN: Premium Sidebar Info -->
<!-- Summary_DE: Detaillierte Anzeige von Bitrate, Codec, Container und Tag-Formaten. -->
<!-- Summary_EN: Detailed display of bitrate, codec, container, and tag formats. -->
<!-- Status: COMPLETED -->

# Premium Sidebar Info

## Konzept
Ein moderner Media Player sollte dem Nutzer tiefe Einblicke in seine Dateien geben. Statt nur "Audio" anzuzeigen, wollen wir technische Details präsentieren.

## Implementierung
Die Sidebar wurde erweitert, um folgende Metadaten aus dem `MediaParser` anzuzeigen:
- **Bitrate & Sample Rate**: Qualität auf einen Blick.
- **Codec & Container**: Technische Details (z.B. AAC in MP4).
- **Tag Format**: Welcher Standard wird genutzt (ID3v2, Vorbis, etc.).

## UI Design
Die Informationen werden dezent im unteren Bereich der Sidebar in einem "Glassmorphism" Look angezeigt, um den Fokus nicht vom Player abzulenken.

<!-- lang-split -->

# Premium Sidebar Info

## Concept
A modern media player should give the user deep insights into their files. Instead of just displaying "Audio", we want to present technical details.

## Implementation
The sidebar has been expanded to display the following metadata from the `MediaParser`:
- **Bitrate & Sample Rate**: Quality at a glance.
- **Codec & Container**: Technical details (e.g., AAC in MP4).
- **Tag Format**: Which standard is used (ID3v2, Vorbis, etc.).

## UI Design
The information is displayed subtly in the lower part of the sidebar in a "glassmorphism" look, so as not to distract from the player.
t, etc.).

## Implementation
We use the `PyMediaInfo` and `ffmpeg` parsers to extract this technical data. The UI then renders these as compact badges or sidebar meta entries.

This makes the Media Player feel like a professional tool rather than just a simple player.
