<!-- Category: Library -->
<!-- Title_DE: Media Kategorisierung -->
<!-- Title_EN: Media Categorization -->
<!-- Summary_DE: Intelligente Erkennung von Hörbüchern (.m4b) und Integration in Datei-Browser. -->
<!-- Summary_EN: Intelligent detection of audiobooks (.m4b) and integration into file browser. -->
<!-- Status: COMPLETED -->

# Media Kategorisierung

## Konzept
Nicht alle Medien sind gleich. Musik benötigt Alben/Künstler, während Hörbücher oft in großen Einzeldateien (.m4b) mit Kapiteln vorliegen.

## Umsetzung
Wir haben eine Heuristik implementiert, die Dateien anhand ihrer Erweiterung und Metadaten kategorisiert.
- **Library**: Standard Musik-Ansicht.
- **Audiobooks**: Spezialisierte Ansicht für .m4b Dateien mit Fokus auf Kapitelmarken.

## Technischer Hintergrund
Der `MediaParser` erkennt den Dateityp und setzt das `category` Feld in der Datenbank. Das Frontend nutzt dieses Feld, um die passenden UI-Elemente (z.B. Kapitelauswahl) anzuzeigen.

<!-- lang-split -->

# Media Categorization

## Concept
Not all media are equal. Music needs albums/artists, while audiobooks are often large single files (.m4b) with chapters.

## Implementation
We implemented a heuristic that categorizes files based on their extension and metadata.
- **Library**: Standard music view.
- **Audiobooks**: Specialized view for .m4b files focusing on chapter marks.

## Technical Background
The `MediaParser` detects the file type and sets the `category` field in the database. The frontend uses this field to display appropriate UI elements (e.g., chapter selection).

3. **Database Flag**: A new `category` field exists in the `media` table.

## GUI Integration
- **Badges**: In the library list, items are marked with an "Audiobook" badge if applicable.
This system allows for a cleaner user experience when managing large libraries with mixed media types.
