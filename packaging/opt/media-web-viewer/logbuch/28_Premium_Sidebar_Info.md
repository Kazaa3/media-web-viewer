<!-- Category: UI -->
<!-- Summary: Detaillierte Anzeige von Bitrate, Codec, Container und Tag-Formaten in der Sidebar. -->
<!-- Status: COMPLETED -->

# Premium Sidebar Info

## Goal
The goal of this feature was to provide technical depth to the media player's interface, catering to power users who want to know the "Digital Identity" of their files.

## Metadata Points
When a song is selected, the sidebar now displays:
- **Codec/Container**: e.g., "flac / flac" or "mp3 / id3v2.4"
- **Technical Specs**: Sample rate, Bitrate, Channels.
- **Tag Format**: Specifically which tag system is being used (ID3v1, ID3v2.3, VorbisComment, etc.).

## Implementation
We use the `PyMediaInfo` and `ffmpeg` parsers to extract this technical data. The UI then renders these as compact badges or sidebar meta entries.

This makes the Media Player feel like a professional tool rather than just a simple player.
