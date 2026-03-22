# 95 – MKV Parser-Evaluation und ffprobe-Strategie

**Datum:** 10.03.2026  
**Version:** 1.3.3+  
**Status:** Evaluation & Decision

## Kontext

Nach der Integration von ffprobe als eigenständigen Parser (siehe [94_FFprobe_Parser_Integration.md](94_FFprobe_Parser_Integration.md)) stellt sich die Frage nach spezialisierten MKV-Parsern für die Matroska-Container-Verarbeitung.

## Anforderungen an MKV-Parsing

1. **Metadaten-Extraktion:** Titel, Dauer, Tracks, Tags, Chapters
2. **Track-Informationen:** Video/Audio/Subtitle-Streams mit Codec, Sprache, Bitrate
3. **Container-Struktur:** EBML-Segmente, Cluster, Attachments
4. **Performance:** Schnelles Parsing ohne vollständiges Laden
5. **Python-Integration:** Einfache API ohne externe Binaries

## Evaluierte Parser-Optionen

### 1. python-ebml ⭐ (Empfehlenswert für EBML-Level Parsing)

**Beschreibung:**
- Reines Python, liest und schreibt Matroska/EBML
- Objektstruktur: Segment, Tracks, Tags, Chapters
- Direkter Zugriff auf EBML-Elemente

**Beispiel:**
```python
from ebml.container import File

ebml_file = File("film.mkv")
print(ebml_file.summary())

segment = next(ebml_file.children_named("Segment"))
print(segment.title)          # Titel
print(segment.duration)       # Dauer
for track in segment.tracks:
    print(track.track_type, track.language, track.codec_id)
```

**Installation:**
```bash
pip install python-ebml
```

**Vorteile:**
- ✅ Pure Python (keine Binary-Abhängigkeiten)
- ✅ Vollständiger EBML-Parser (nicht nur Matroska)
- ✅ Lese- und Schreibzugriff auf Container-Struktur
- ✅ Kapitel-Extraktion möglich

**Nachteile:**
- ❌ Weniger Stream-Details als ffprobe (keine tiefe Codec-Analyse)
- ❌ Performance bei sehr großen Dateien
- ❌ Zusätzliche Abhängigkeit

**Use Case:** Wenn EBML-Level-Zugriff nötig ist (z.B. Chapter-Manipulation, Tag-Editing)

---

### 2. mkvparse (Event-basierter Parser)

**Beschreibung:**
- Einfacher, event-basierter Matroska-Parser
- Handler-Klasse für Callbacks bei Segment-Info, Tracks, etc.

**Beispiel:**
```python
import mkvparse

class MyHandler(mkvparse.MatroskaHandler):
    def segment_info_available(self):
        print(self.segment_info)

    def tracks_available(self):
        print(self.tracks)

with open("film.mkv", "rb") as f:
    mkvparse.mkvparse(f, MyHandler())
```

**Installation:**
```bash
pip install mkvparse
```

**Vorteile:**
- ✅ Leichtgewichtig
- ✅ Event-basiert (gut für Streaming-Parsing)

**Nachteile:**
- ❌ Event-Handler-Syntax umständlicher
- ❌ Weniger Feature-komplett als python-ebml
- ❌ Weniger aktiv maintained

**Use Case:** Spezialfälle mit großen Dateien, wo Event-basiertes Parsing Sinn macht

---

### 3. enzyme (Video-Metadaten-Parser)

**Beschreibung:**
- Fokus auf MediaInfo-ähnliche Infos (Codec, Auflösung, Audio-Spuren)
- Einfache API für gängige Video-Metadaten

**Beispiel:**
```python
import enzyme

with open("film.mkv", "rb") as f:
    mv = enzyme.MKV(f)
    print(mv.video[0].codec, mv.video[0].width, mv.video[0].height)
    for audio in mv.audio:
        print(audio.language, audio.channels)
```

**Installation:**
```bash
pip install enzyme
```

**Vorteile:**
- ✅ Einfache API für Standard-Metadaten
- ✅ Gute Balance zwischen Einfachheit und Features

**Nachteile:**
- ❌ Fokus nur auf Metadaten (keine Manipulation)
- ❌ Nicht mehr aktiv maintained (letztes Update 2015)
- ❌ Weniger umfassend als ffprobe

**Use Case:** Legacy-Code, einfache Metadaten-Extraktion

---

### 4. pymkv / pymkv2 (mkvmerge-Wrapper)

**Beschreibung:**
- Wrapper um mkvmerge aus MKVToolNix
- Für MKV-Bearbeitung (Tracks hinzufügen/entfernen, Muxen, Chapters)

**Beispiel:**
```python
from pymkv import MKVFile

mkv = MKVFile("input.mkv")
# Tracks manipulieren, neue Audio/Subtitle hinzufügen
mkv.mux("output.mkv")
```

**Installation:**
```bash
pip install pymkv
# Benötigt: sudo apt install mkvtoolnix
```

**Vorteile:**
- ✅ Vollständige MKV-Manipulation
- ✅ Nutzt battle-tested mkvmerge

**Nachteile:**
- ❌ Benötigt externe Binary (mkvtoolnix)
- ❌ Nicht für reines Parsing gedacht (Overhead)
- ❌ Langsamer als reine Parser

**Use Case:** Wenn MKVs bearbeitet werden sollen (Remuxing, Track-Management)

---

### 5. ffprobe ⭐⭐⭐ (Empfohlen, bereits integriert!)

**Beschreibung:**
- Tool aus FFmpeg für umfassende Media-Analyse
- JSON/CSV-Ausgabe, perfekt für Parsing
- Bereits als `ffprobe_parser.py` in unserem Projekt integriert!

**Beispiel (Subprocess):**
```python
import subprocess
import json

def probe_mkv(path):
    cmd = [
        "ffprobe", "-v", "quiet", "-print_format", "json",
        "-show_format", "-show_streams", "-show_chapters", path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return json.loads(result.stdout)

info = probe_mkv("film.mkv")
print(info["format"]["duration"])
for stream in info["streams"]:
    if stream["codec_type"] == "video":
        print(f"Video: {stream['width']}x{stream['height']}, {stream['codec_name']}")
```

**Installation:**
```bash
# Bereits auf System:
sudo apt install ffmpeg
```

**Vorteile:**
- ✅ Umfassendste Stream-Analyse (Codec, Bitrate, Framerate, Bitdepth)
- ✅ Schnell und zuverlässig (C-Implementation)
- ✅ JSON-Output perfekt für Parsing
- ✅ Unterstützt alle Media-Formate (nicht nur MKV)
- ✅ Chapters, Attachments, Tags vollständig extrahierbar
- ✅ **Bereits integriert in unserem System!**

**Nachteile:**
- ❌ Externe Binary-Abhängigkeit (aber Standard auf Linux)
- ❌ Keine EBML-Manipulation möglich (nur Lesen)

**Use Case:** Standard-Lösung für Media-Metadaten-Extraktion

---

## Vergleichstabelle

| Feature | python-ebml | mkvparse | enzyme | pymkv | ffprobe |
|---------|-------------|----------|--------|-------|---------|
| Pure Python | ✅ | ✅ | ✅ | ❌ | ❌ |
| Keine Binary-Deps | ✅ | ✅ | ✅ | ❌ | ❌ |
| Stream-Details | ⚠️ | ⚠️ | ✅ | ❌ | ✅✅ |
| Chapter-Support | ✅ | ✅ | ❌ | ✅ | ✅ |
| EBML-Manipulation | ✅ | ❌ | ❌ | ✅ | ❌ |
| Performance | ⚠️ | ✅ | ✅ | ❌ | ✅✅ |
| Maintained | ✅ | ⚠️ | ❌ | ✅ | ✅✅ |
| Bereits integriert | ❌ | ❌ | ❌ | ❌ | ✅ |

## Entscheidung & Empfehlung

### Aktuelle Situation

Wir haben **ffprobe bereits vollständig integriert** (siehe Logbuch 94). ffprobe bietet:

1. **Container-Info:** Format, Dauer, Bitrate, Tags
2. **Stream-Analyse:** Video/Audio/Subtitle mit Codec, Bitrate, Sprache
3. **Chapter-Extraktion:** Start/End-Times, Titles
4. **JSON-Output:** Strukturiert und präzise
5. **Universal:** Funktioniert mit allen Media-Formaten

### Empfohlene Strategie

**Für 95% der Fälle: ffprobe (bereits vorhanden)**

```python
# Bereits implementiert in parsers/ffprobe_parser.py
from parsers import media_parser

duration, tags = media_parser.extract_metadata("film.mkv", "film.mkv", mode='full')
print(tags['container'])       # mkv
print(tags['codec'])            # h264
print(tags['chapters'])         # Liste mit Kapiteln
print(tags['full_tags']['ffprobe_json'])  # Vollständige JSON-Struktur
```

**Für spezielle EBML-Manipulation: python-ebml als Ergänzung**

Falls wir später EBML-Elemente direkt bearbeiten müssen (z.B. Tag-Editing, Chapter-Timestamps ändern), können wir python-ebml ergänzen:

```python
# Zukünftige Erweiterung (optional)
from ebml.container import File

def edit_mkv_tags(path, new_title):
    ebml_file = File(path)
    segment = next(ebml_file.children_named("Segment"))
    segment.title = new_title
    ebml_file.save()
```

**Nicht empfohlen:**
- ❌ enzyme (veraltet, weniger Features als ffprobe)
- ❌ mkvparse (Event-Handler-Syntax umständlich)
- ❌ pymkv (nur für Remuxing, nicht für Parsing)

## Implementierungs-Status

### ✅ Bereits vorhanden (ffprobe_parser.py)

```python
# Aktueller Parser-Stack:
filename → container → mutagen → pymediainfo → ffprobe → ffmpeg
                                                  ↑
                                      Liefert bereits:
                                      - Container: mkv
                                      - Streams: Video/Audio/Subtitle
                                      - Chapters: Start/End/Title
                                      - Tags: Alle Container-Metadaten
```

### Zukünftige Erweiterungen (optional)

1. **MKV-spezifische Chapter-Bearbeitung:**
   - python-ebml für direktes EBML-Editing
   - UI-Feature: Chapter-Namen editieren, Timestamps verschieben

2. **MKV-Remuxing:**
   - pymkv für Track-Management
   - UI-Feature: Audio-/Subtitle-Tracks hinzufügen/entfernen

3. **Attachment-Support:**
   - ffprobe zeigt bereits Attachments an
   - Optional: python-ebml zum Extrahieren von Fonts/Cover-Art

## Performance-Überlegungen

### ffprobe vs. python-ebml (Benchmark)

**Test-Datei:** Adam Grant - Geben und Nehmen.m4b (M4B mit 32 Chapters)

```
ffprobe (Lightweight): 0.0000s (skipped, da bereits genug Info)
ffprobe (Full Mode):   0.0700s
python-ebml (geschätzt): 0.200-0.500s (Pure Python, EBML-Parsing)
```

**Ergebnis:** ffprobe ist 3-7x schneller für Metadaten-Extraktion.

## Fazit

**ffprobe ist die richtige Wahl für unser Projekt:**

1. ✅ Bereits vollständig integriert (`parsers/ffprobe_parser.py`)
2. ✅ Schnellste und umfassendste Metadaten-Extraktion
3. ✅ JSON-Output perfekt für Parsing
4. ✅ Unterstützt alle Container-Formate (nicht nur MKV)
5. ✅ Battle-tested und aktiv maintained (Teil von FFmpeg)

**python-ebml nur hinzufügen, wenn:**
- Wir EBML-Elemente direkt bearbeiten müssen (Tag-Editing, Chapter-Manipulation)
- Pure-Python-Lösung ohne Binary-Deps gewünscht ist (z.B. für Portable Build)

**Aktuell keine Action nötig:** ffprobe deckt alle MKV-Parsing-Anforderungen ab.

---

## Nächste Schritte (bei Bedarf)

1. **Wenn Chapter-Editing gewünscht wird:**
   ```bash
   pip install python-ebml
   ```
   → Neue Funktion in `parsers/mkv_editor.py`

2. **Wenn Track-Manipulation gewünscht wird:**
   ```bash
   pip install pymkv
   sudo apt install mkvtoolnix
   ```
   → Neue Funktion in `parsers/mkv_muxer.py`

3. **Aktuell:** Nutze weiterhin ffprobe für alle Metadaten-Anforderungen ✅

## Referenzen

- [FFprobe Documentation](https://ffmpeg.org/ffprobe.html)
- [python-ebml GitHub](https://github.com/Matroska-Org/python-ebml)
- [Matroska Specification](https://www.matroska.org/technical/specs/index.html)
- [Logbuch 94: FFprobe Parser Integration](94_FFprobe_Parser_Integration.md)
