# Eigener Item-Type / Category-Mapping für Medien

## Ziel
Ein flexibles Mapping von Item-Typen und Kategorien ermöglicht die gezielte Zuordnung und Filterung von Medien (z.B. Hörbuch, Musik, Podcast, Video).

## Umsetzung
- Im Backend wird eine Mapping-Tabelle gepflegt, die Dateitypen, Tags und Metadaten auf Item-Typen und Kategorien abbildet.
- Die GUI kann diese Typen und Kategorien für Filter, Sortierung und Anzeige nutzen.
- Erweiterbar für neue Typen (z.B. Hörspiel, Dokumentation, Film).

## Beispiel: Category-Mapping (Python)
```python
CATEGORY_MAP = {
    'audiobook': ['Hörbuch', 'audiobook', 'spoken word'],
    'music': ['Musik', 'album', 'track'],
    'podcast': ['Podcast', 'episode'],
    'video': ['Video', 'movie', 'clip'],
    # Erweiterbar...
}

def map_item_type(tags):
    for item_type, keywords in CATEGORY_MAP.items():
        if any(tag in keywords for tag in tags):
            return item_type
    return 'unknown'
```

## Beispiel: displayed_cats und cat_map für GUI-Filter

```python
if displayed_cats is None:
    displayed_cats = ["audio", "video", "images", "documents", "ebooks", "abbild"]

# Mapping von internen Kategorien zu GUI-Keys
cat_map = {
    "audio": ["Audio", "Album", "Hörbuch", "Klassik", "Compilation", "Single"],
    "video": ["Video", "Film", "Serie"],
    "images": ["Bilder"],
    "documents": ["Dokument"],
    "ebooks": ["E-Book"],
    "abbild": ["Abbild", "ISO/Image", "Disk Image", "PAL DVD", "NTSC DVD", "Blu-ray", 
               "PAL DVD (Abbild)", "NTSC DVD (Abbild)", "DVD (Abbild)", "Blu-ray (Abbild)", 
               "Audio-CD (Abbild)", "CD-ROM (Abbild)", "Disk-Abbild", "Film",
               "Spiel", "Beigabe", "Software"]
}
```

- displayed_cats definiert die sichtbaren Hauptkategorien in der GUI.
- cat_map ordnet interne Kategorien den GUI-Filter-Keys zu.
- Erweiterbar für neue Typen und Spezialfälle.

## Hinweis: Category-Mapping existiert bereits

- Die Logik zur Zuordnung von Item-Typen und Kategorien ist im Projekt vorhanden:
    - In models.py: bestimmt get_category() die Kategorie anhand Dateiendung, Pfad und Metadaten.
    - Ein Mapping von Kategorien auf Medientypen ist ebenfalls in models.py (mapping = {...}).
    - Das flexible CATEGORY_MAP (siehe oben) kann erweitert werden.
    - Die GUI nutzt item.category für Anzeige und Filterung.
- Bestehende Logik kann weiterverwendet und angepasst werden.

## "Hörbuch" ist im Mapping enthalten

- Die Kategorie "Hörbuch" ist bereits Teil der audio-Kategorie im cat_map.
- Filter und Anzeige für Hörbücher funktionieren mit der bestehenden Mapping-Logik.
- Keine zusätzliche Anpassung für Hörbücher notwendig.

## Mapping-Ziel: cat_map wird auf GUI-Filter und Backend-Typen gemappt

- cat_map ordnet interne Kategorien den sichtbaren Filter-Keys der GUI zu (z.B. "audio", "video", "images").
- Im Backend werden die Kategorien für API-Ausgaben, Filter und Typzuordnung genutzt.
- Die GUI verwendet die gemappten Keys für Filter, Sortierung und Anzeige.
- Erweiterbar für neue Typen und Spezialfälle.

## Herkunft der Keys: VIDEO_EXTENSIONS, AUDIO_EXTENSIONS, DOCUMENT_EXTENSIONS

- Die Zuordnung der Kategorien basiert auf Extension-Listen im Backend:
    - VIDEO_EXTENSIONS: typische Video-Dateiendungen (z.B. .mp4, .mkv, .avi)
    - AUDIO_EXTENSIONS: typische Audio-Dateiendungen (z.B. .mp3, .flac, .m4b)
    - DOCUMENT_EXTENSIONS: typische Dokument-Dateiendungen (z.B. .pdf, .doc, .txt)
- Diese Listen werden in models.py und media_format.py gepflegt und für die Typbestimmung genutzt.
- Die Keys für cat_map und Filter stammen aus diesen Extension-Listen und der get_category()-Logik.

## Hinweise
- Das Mapping kann zentral gepflegt und erweitert werden.
- GUI und Backend nutzen die Typen für Filter, Anzeige und Spezialfunktionen.
- Für neue Medienarten einfach neue Kategorien und Keywords ergänzen.



---
Letzte Aktualisierung: 11. März 2026
