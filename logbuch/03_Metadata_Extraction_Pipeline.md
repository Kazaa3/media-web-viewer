<!-- Category: Development -->
<!-- Title_DE: Metadaten-Extraktions-Pipeline -->
<!-- Title_EN: Metadata Extraction Pipeline -->
<!-- Summary_DE: Details zur robusten Extraktion von Medien-Metadaten. -->
<!-- Summary_EN: Details on robust media metadata extraction. -->
<!-- Status: COMPLETED -->

# Metadaten-Extraktions-Pipeline

Ein zentraler Aspekt des Viewers ist die akkurate Anzeige von Medieninformationen. Da die Qualität von Tags in Musikarchiven stark variiert, nutzt die Anwendung eine mehrstufige Strategie.

### Mehrstufige Extraktion
1. **Mutagen (Primär):** Wird für Standard-Tags (ID3, Vorbis, MP4) verwendet. Es ist schnell und deckt die meisten Anwendungsfälle ab.
2. **PyMediaInfo / MediaInfo (Sekundär):** Liefert detaillierte technische Informationen wie Bitrate, Sample-Rate und Codec-Details, die oft über reine Tags hinausgehen.
3. **FFmpeg Fallback:** Wenn herkömmliche Bibliotheken scheitern (z.B. bei beschädigten Headern), wird FFmpeg via Subprocess genutzt, um die Spurdauer und grundlegende Metadaten zu extrahieren.

### Filename-Parsing
Falls gar keine Metadaten vorhanden sind, greift ein intelligentes System zum Parsen des Dateinamens, um zumindest Titel und Künstler (z.B. aus `Interpret - Titel.mp3`) zu erraten.

### Cover-Art Handling
Die Pipeline sucht nach eingebetteten Covern in den Dateien. Werden diese nicht gefunden, wird im Verzeichnis nach Dateien wie `folder.jpg` oder `cover.png` gesucht, um eine ansprechende Visualisierung im Player zu gewährleisten.

Dank dieser Redundanz erreicht der *Media Web Viewer* eine hohe Zuverlässigkeit bei der Indizierung großer Bibliotheken.

<!-- lang-split -->

# Metadata Extraction Pipeline

A central aspect of the Viewer is the accurate display of media information. Since the quality of tags in music archives varies greatly, the application uses a multi-stage strategy.

### Multi-stage Extraction
1. **Mutagen (Primary):** Used for standard tags (ID3, Vorbis, MP4). It is fast and covers most use cases.
2. **PyMediaInfo / MediaInfo (Secondary):** Provides detailed technical information such as bitrate, sample rate, and codec details that often go beyond pure tags.
3. **FFmpeg Fallback:** If conventional libraries fail (e.g., with corrupted headers), FFmpeg is used via subprocess to extract track duration and basic metadata.

### Filename Parsing
If no metadata is present at all, an intelligent system for parsing the filename kicks in to at least guess the title and artist (e.g., from `Artist - Title.mp3`).

### Cover-Art Handling
The pipeline looks for embedded covers in the files. If these are not found, it searches the directory for files like `folder.jpg` or `cover.png` to ensure an attractive visualization in the player.

Thanks to this redundancy, the *Media Web Viewer* achieves high reliability when indexing large libraries.
