<!-- Category: Development -->
<!-- Title_DE: 05 Die Metadaten-Quest: Jenseits von Dateinamen -->
<!-- Title_EN: 05 The Metadata Quest: Beyond Filenames -->
<!-- Summary_DE: Evolution der Metadaten-Extraktion – von Mutagen bis zum FFmpeg-Fallback. -->
<!-- Summary_EN: Evolution of metadata extraction – from Mutagen to FFmpeg fallback. -->
<!-- Status: COMPLETED -->

<!-- ANKER: Die Metadaten-Quest -->
# 05 Die Metadaten-Quest: Jenseits von Dateinamen

Ein Medienplayer ohne Titel, Album und Künstler ist nur eine Liste von Dateien. Die "Quest" nach akkuraten Informationen führte zu einer immer komplexeren Pipeline.

### Die Strategie der Redundanz
Da Tags oft fehlerhaft oder unvollständig sind, nutzt der *Media Web Viewer* eine mehrstufige Eskalationsstrategie:
1. **Mutagen:** Der schnelle Standard für ID3-Tags, Vorbis-Kommentare und MP4-Tags.
2. **PyMediaInfo:** Für technische Details (Bitrate, Sample-Rate), die in Standard-Tags oft fehlen.
3. **FFmpeg Fallback:** Die "letzte Instanz". Wenn alles andere scheitert, extrahiert FFmpeg die Spurdauer und grundlegende Metadaten direkt aus dem Bitstream.

### Filename Parsing & Covers
Wenn gar keine Tags vorhanden sind, versucht die App, Informationen aus der Verzeichnisstruktur zu erraten. Parallel dazu sucht die Pipeline nach eingebetteten Covern oder Dateien wie `folder.jpg`, um die App visuell zum Leben zu erwecken.

### Erkenntnis
Metadaten-Extraktion ist keine exakte Wissenschaft, sondern ein Prozess der Annäherung. Diese Pipeline stellt sicher, dass der Nutzer in fast jedem Fall eine ansprechende Anzeige erhält.

<!-- ANKER: Strategie der Redundanz -->
### Die Strategie der Redundanz
Da Tags oft fehlerhaft oder unvollständig sind, nutzt der *Media Web Viewer* eine mehrstufige Eskalationsstrategie:
1. **Mutagen:** Der schnelle Standard für ID3-Tags, Vorbis-Kommentare und MP4-Tags.
2. **PyMediaInfo:** Für technische Details (Bitrate, Sample-Rate), die in Standard-Tags oft fehlen.
3. **FFmpeg Fallback:** Die "letzte Instanz". Wenn alles andere scheitert, extrahiert FFmpeg die Spurdauer und grundlegende Metadaten direkt aus dem Bitstream.

<!-- ANKER: Filename Parsing & Covers -->
### Filename Parsing & Covers
Wenn gar keine Tags vorhanden sind, versucht die App, Informationen aus der Verzeichnisstruktur zu erraten. Parallel dazu sucht die Pipeline nach eingebetteten Covern oder Dateien wie `folder.jpg`, um die App visuell zum Leben zu erwecken.

<!-- ANKER: Erkenntnis -->
### Erkenntnis
Metadaten-Extraktion ist keine exakte Wissenschaft, sondern ein Prozess der Annäherung. Diese Pipeline stellt sicher, dass der Nutzer in fast jedem Fall eine ansprechende Anzeige erhält.

<!-- lang-split -->

<!-- ANKER: The Metadata Quest EN -->
# 05 The Metadata Quest: Beyond Filenames

A media player without title, album, and artist is just a list of files. The "quest" for accurate information led to an increasingly complex pipeline.

### The Strategy of Redundancy
Since tags are often incorrect or incomplete, the *Media Web Viewer* uses a multi-stage escalation strategy:
1. **Mutagen:** The fast standard for ID3 tags, Vorbis comments, and MP4 tags.
2. **PyMediaInfo:** For technical details (bitrate, sample rate) that are often missing in standard tags.
3. **FFmpeg Fallback:** The "last resort." If everything else fails, FFmpeg extracts track duration and basic metadata directly from the bitstream.

### Filename Parsing & Covers
If no tags are present at all, the app tries to guess information from the directory structure. In parallel, the pipeline searches for embedded covers or files like `folder.jpg` to bring the app to life visually.

### Insight
Metadata extraction is not an exact science but a process of approximation. This pipeline ensures that the user receives an attractive display in almost every case.
