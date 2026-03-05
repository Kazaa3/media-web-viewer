<!-- Category: UI/UX -->

# Premium Sidebar Info

## Goal
Provide full technical transparency for every media file played.

## Displayed Data
- **Format**: Container type (m4b, mp3, mkv) and Tag versions (ID3v2.4, MP4Tags).
- **Audio properties**: 
    - Bitrate (kbps)
    - Sample Rate (kHz)
    - Bit Depth (16/24 bit)
    - Codec (aac, mp3, flac)
- **Parser Metrics**: Detailed timing of how long each parser (Mutagen, MediaInfo, FFmpeg) took to extract data.

## Implementation
We use a multi-parser chain. Each parser contributes specific fields, and the results are merged in `media_parser.py`.
The UI uses modern typography and subtle badges to make this technical data readable without being overwhelming.
