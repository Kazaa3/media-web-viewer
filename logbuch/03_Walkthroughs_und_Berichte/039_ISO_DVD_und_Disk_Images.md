<!-- Category: Documentation -->
<!-- Title_DE: ISO, DVD & Disk Images -->
<!-- Title_EN: ISO, DVD & Disk Images -->
<!-- Summary_DE: Unterstützung für physische Medienformate: ISO-Parsing, DVD-Ordner-Strukturen und Volume-ID Extraktion. -->
<!-- Summary_EN: Support for physical media formats: ISO parsing, DVD folder structures and volume ID extraction. -->
<!-- Status: ACTIVE -->

# ISO, DVD & Disk Images

## Die Brücke zur physischen Welt
In einer Welt voller digitaler Einzeldateien behält **dict - Web Media Player & Library** auch die Übersicht über ganze Disk-Images. Ob ISO-Dateien von DVDs oder klassische DVD-Ordnerstrukturen (`VIDEO_TS`) – dict behandelt sie als erstklassige Medienobjekte.

## Technische Umsetzung
Die Verarbeitung von Disk-Images erforderte spezialisierte Tools jenseits der Standard-Medienparser:

1.  **ISO-Parsing (`isoparser` & `pycdlib`):** Diese Bibliotheken ermöglichen es uns, in die ISO-Datei "hineinzuschauen", ohne sie mounten zu müssen. So extrahieren wir die **Volume-ID** (den Namen der Disk) als primären Titel.
2.  **DVD-Ordner-Erkennung:** Dict erkennt automatisch `VIDEO_TS` Ordner und fasst sie zu einem einzigen "DVD"-Item zusammen, anstatt hunderte kleine `.VOB` Dateien einzeln anzuzeigen.

## PAL/NTSC & Frame-Raten
Ein technischer Meilenstein war die Extraktion von Video-Standards aus Disk-Images:
- **Herausforderung:** ISO-Dateien liefern oft keine direkten Metadaten über das Videoformat.
- **Lösung:** Durch einen gezielten Scan der ersten Video-Streams via FFmpeg innerhalb des Images können wir den Standard (PAL vs. NTSC) und die exakte Frame-Rate bestimmen. Dies hilft bei der korrekten Einordnung von regionalen Medien (z.B. europäische DVDs).

## Metadaten-Fallback
Wenn eine ISO keine internen Metadaten liefert, nutzt dict den Dateinamen und die Volume-ID als Basis und ergänzt diese durch Scraper, die gezielt nach DVD-Veröffentlichungen suchen.

*Ob digitaler Download oder Image einer alten DVD-Sammlung – dict sorgt dafür, dass jedes Medium seinen Platz in der Bibliothek findet.*

<!-- lang-split -->

# ISO, DVD & Disk Images

## The Bridge to the Physical World
In a world full of individual digital files, **dict - Web Media Player & Library** also keeps track of entire disk images. Whether ISO files from DVDs or classic DVD folder structures (`VIDEO_TS`) – dict treats them as first-class media objects.

## Technical Implementation
The processing of disk images required specialized tools beyond standard media parsers:

1.  **ISO Parsing (`isoparser` & `pycdlib`):** These libraries allow us to "look inside" the ISO file without having to mount it. This is how we extract the **Volume ID** (the name of the disk) as the primary title.
2.  **DVD Folder Detection:** Dict automatically detects `VIDEO_TS` folders and combines them into single "DVD" items instead of displaying hundreds of small `.VOB` files individually.

## PAL/NTSC & Frame Rates
A technical milestone was the extraction of video standards from disk images:
- **Challenge:** ISO files often do not provide direct metadata about the video format.
- **Solution:** Through a targeted scan of the first video streams via FFmpeg within the image, we can determine the standard (PAL vs. NTSC) and the exact frame rate. This helps with the correct classification of regional media (e.g., European DVDs).

## Metadata Fallback
If an ISO does not provide internal metadata, dict uses the file name and Volume ID as a basis and supplements them with scrapers that specifically search for DVD releases.

*Whether it's a digital download or an image of an old DVD collection – dict ensures that every medium finds its place in the library.*
