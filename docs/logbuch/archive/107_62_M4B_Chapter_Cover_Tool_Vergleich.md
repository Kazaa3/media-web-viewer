<!-- Category: parser-comparison -->
<!-- Title_DE: M4B-Chapter- und Cover-Support: Tool-Vergleich -->
<!-- Title_EN: M4B Chapter and Cover Support: Tool Comparison -->
<!-- Summary_DE: Vergleich der Parser-Tools bzgl. M4B-Kapitel und Cover-Art-Unterstützung. -->
<!-- Summary_EN: Comparison of parser tools regarding M4B chapter and cover art support. -->
<!-- Status: in-progress -->
<!-- Date: 2026-03-10 -->

# M4B-Chapter- und Cover-Support: Tool-Vergleich

## Mutagen
- **Kapitel:** Vollständige Unterstützung (Nero/QuickTime-Chapters via moov.udta.chpl), Lesen und Schreiben, Startzeit und Titel, API: `MP4Chapters`.
- **Cover-Art:** Vollständige Unterstützung (JPEG/PNG via covr-Tag, API: `MP4Cover`).
- **Praxis:** Kapitel und Cover können direkt ausgelesen und hinzugefügt werden.

## ffprobe/ffmpeg
- **Kapitel:** Kann Kapitel auslesen, aber keine native API zum Hinzufügen. Kapitel werden als Streams/Metadata erkannt.
- **Cover-Art:** Cover wird als Metadata/Stream erkannt, aber keine native API zum Hinzufügen.
- **Praxis:** Für reine Analyse geeignet, nicht für Editing.

## pymediainfo
- **Kapitel:** Erkennt Kapitel als "Menu"-Tracks, Startzeit/Titel werden extrahiert.
- **Cover-Art:** Cover wird als "Cover"-Tag erkannt.
- **Praxis:** Nur Lesend, keine Schreibfunktion.

## mkvparse, python-ebml, pymkv, enzyme
- **Kapitel:** Nicht für MP4/M4B, nur für MKV/Matroska relevant.
- **Cover-Art:** Nicht für MP4/M4B, nur für MKV/Matroska relevant.

## tinytag, mutagen (allgemein), eyed3, music-tag
- **Kapitel:** Keine Unterstützung für M4B-Kapitel.
- **Cover-Art:** Cover wird für MP3/M4A erkannt, aber keine spezifische M4B-Unterstützung.

## Zusammenfassung
- **Mutagen** ist das einzige Tool mit vollständiger M4B-Kapitel- und Cover-Unterstützung (Lesen/Schreiben).
- **ffprobe/ffmpeg/pymediainfo** können Kapitel/Cover auslesen, aber nicht schreiben.
- **tinytag, eyed3, music-tag** erkennen Cover, aber keine Kapitel.
- **Matroska-Tools** sind für M4B nicht relevant.

## Praxis-Empfehlung
- Für M4B-Editing: Mutagen verwenden.
- Für reine Analyse: ffprobe, pymediainfo, Mutagen.
- Für MP3/M4A: eyed3, music-tag, tinytag für Cover.

