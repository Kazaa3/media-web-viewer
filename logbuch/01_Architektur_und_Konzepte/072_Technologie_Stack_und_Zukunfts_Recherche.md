# 96 – Technologie-Stack und Zukunfts-Recherche

**Datum:** 10.03.2026  
**Version:** 1.3.3+  
**Status:** Dokumentation & Vorbereitung für zukünftige Meilensteine

## Zielsetzung

Dieser Eintrag dokumentiert den **aktuellen Technologie-Stack** und präsentiert **Recherche-Ergebnisse** für potenzielle zukünftige Features. Die Informationen dienen als Vorbereitung für kommende Meilensteine und als Entscheidungsgrundlage für technologische Erweiterungen.

**Wichtig:** Dies ist eine **Dokumentations- und Recherche-Phase**. Implementierung erfolgt in späteren Versionen (z.B. 1.4.0+).

---

## 📦 Aktueller Produktions-Stack (v1.3.3)

### Core Framework

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **Python** | 3.14.2 | PSF | Haupt-Programmiersprache | ✅ Produktiv |
| **Eel** | >=0.18.2 | MIT | Desktop GUI (Electron-like) | ✅ Produktiv |
| **Bottle** | >=0.13.0 | MIT | Web Framework & REST API | ✅ Produktiv |
| **SQLite** | 3.x | Public Domain | Datenbank für Medien-Library | ✅ Produktiv |

### Audio/Media Parsing

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **mutagen** | >=1.47.0 | GPL v2 | ID3/MP3/FLAC/M4A Tags (schnell) | ✅ Produktiv |
| **pymediainfo** | >=7.0.1 | MIT | MediaInfo-Wrapper (detailliert) | ✅ Produktiv |
| **ffprobe** | System | LGPL | JSON-basierte Medienanalyse | ✅ Produktiv |
| **ffmpeg** | System | LGPL | Transcoding & Fallback-Parser | ✅ Produktiv |

**Parser-Chain (seit Logbuch 94/95):**
```
filename → container → mutagen → pymediainfo → ffprobe → ffmpeg
```

### Async & Communication

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **gevent** | >=25.9.1 | MIT | Coroutine-basierte Async I/O | ✅ Produktiv |
| **gevent-websocket** | >=0.10.1 | MIT | WebSocket für Live-Updates | ✅ Produktiv |
| **bottle-websocket** | >=0.2.9 | MIT | WebSocket-Plugin für Bottle | ✅ Produktiv |

### Frontend

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **HTML5** | - | W3C | UI-Struktur | ✅ Produktiv |
| **CSS3** | - | W3C | Styling | ✅ Produktiv |
| **JavaScript** (Vanilla) | ES6+ | - | UI-Logik, DOM-Manipulation | ✅ Produktiv |
| **Google Chrome** | System | Proprietary | Browser-Backend für Eel | ✅ Produktiv |

### Testing & QA

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **pytest** | >=8.0.0 | MIT | Test-Framework | ✅ Produktiv |
| **pytest-cov** | >=4.1.0 | MIT | Code Coverage | ✅ Produktiv |
| **mypy** | >=1.9.0 | MIT | Static Type Checking | ✅ Produktiv |
| **flake8** | >=7.0.0 | MIT | Linting (PEP8) | ✅ Produktiv |

### Build & Packaging

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **PyInstaller** | latest | GPL v2+ | Standalone-Build (.exe/.deb) | ✅ Produktiv |
| **setuptools** | latest | MIT | Python-Packaging | ✅ Produktiv |
| **wheel** | latest | MIT | Binary Distribution | ✅ Produktiv |

### System Tools

| Technologie | Version | Lizenz | Zweck | Status |
|-------------|---------|--------|-------|--------|
| **ffmpeg** | System | LGPL | Audio/Video-Verarbeitung | ✅ Produktiv |
| **mediainfo** | System | BSD 2-Clause | CLI für pymediainfo | ✅ Produktiv |
| **VLC** | System (optional) | GPL v2+ | Externe Video-Wiedergabe | ✅ Produktiv |
| **Doxygen** | System | GPL v2 | Dokumentation | ✅ Produktiv |

---

## 🔬 Recherche-Ergebnisse für zukünftige Features

### 1. Video-Support (Milestone 1.4.0+)

**Ziel:** MP4/MKV/WebM-Wiedergabe im Browser

#### Option A: HTML5 Video (Empfohlen für Start)

**Technologie:** Natives `<video>`-Element

```html
<video controls>
  <source src="/media/film.mp4" type="video/mp4">
  <source src="/media/film.webm" type="video/webm">
</video>
```

**Vorteile:**
- ✅ Native Browser-Unterstützung (keine Dependencies)
- ✅ Hardware-Beschleunigung automatisch
- ✅ Touch/Mobile-freundlich
- ✅ Accessibility (Untertitel via `<track>`)

**Nachteile:**
- ❌ Format-Limitierungen (nur Browser-unterstützte Codecs)
- ❌ Keine erweiterte Kontrolle (Bitrate, Buffer-Strategie)

**Unterstützte Formate:**
- **MP4/H.264:** ✅ Alle Browser
- **WebM/VP8/VP9:** ✅ Chrome, Firefox
- **MKV:** ❌ Benötigt Transcoding zu MP4/WebM

**Implementation:**
```python
# Backend: Transcode zu browser-kompatiblen Formaten
def transcode_for_browser(mkv_path):
    output = "temp.mp4"
    subprocess.run([
        "ffmpeg", "-i", mkv_path,
        "-c:v", "libx264", "-c:a", "aac",
        "-movflags", "faststart",  # Web-optimiert
        output
    ])
    return output
```

---

#### Option B: Video.js (Feature-reich)

**Technologie:** JavaScript Video Player Library

**Installation:**
```html
<link href="//vjs.zencdn.net/8.0.4/video-js.css" rel="stylesheet">
<script src="//vjs.zencdn.net/8.0.4/video.js"></script>
```

**Features:**
- ✅ Einheitliches UI über alle Browser
- ✅ Plugin-System (HLS, DASH, Untertitel)
- ✅ Responsive & themeable
- ✅ Accessibility-Features

**Nachteile:**
- ❌ Externe JavaScript-Dependency (~50KB)
- ❌ Höherer Wartungsaufwand

**Use Case:** Wenn erweiterte Features nötig sind (z.B. adaptive Bitrate, Playlists)

---

#### Option C: VLC Web Plugin (Fortgeschritten)

**Technologie:** VLC als Embedded Player

**Vorteile:**
- ✅ Unterstützt **alle** Formate (MKV, AVI, etc.)
- ✅ Keine Transcoding-Notwendigkeit
- ✅ Bereits als Dependency vorhanden (python-vlc)

**Nachteile:**
- ❌ Browser-Plugin deprecated (moderne Browser blocken NPAPI)
- ❌ Nur über Electron/Eel möglich (nicht Web-Standard)

**Implementation (Eel):**
```python
import vlc

player = vlc.MediaPlayer("film.mkv")
player.play()

# In Eel: Embedded in Canvas/Frame
```

**Use Case:** Nur wenn native Formate absolut nötig sind (z.B. HDR, DTS-Audio)

---

### 2. Erweiterte MKV-Manipulation (Optional, 1.5.0+)

**Ziel:** Chapter-Editing, Track-Management, Tag-Editing

#### Option A: python-ebml (EBML-Level Zugriff)

**Technologie:** Pure Python EBML/Matroska Parser

**Installation:**
```bash
pip install python-ebml
```

**Features:**
```python
from ebml.container import File

# MKV öffnen und Titel ändern
ebml_file = File("film.mkv")
segment = next(ebml_file.children_named("Segment"))
segment.title = "Neuer Titel"
ebml_file.save()

# Chapters bearbeiten
for chapter in segment.chapters:
    chapter.title = f"Kapitel {chapter.chapter_number}"
```

**Vorteile:**
- ✅ Pure Python (keine Binary-Deps)
- ✅ Vollständiger EBML-Zugriff
- ✅ Lese- und Schreibzugriff

**Nachteile:**
- ❌ Langsamer als ffprobe für Metadaten
- ❌ Zusätzliche Dependency

**Use Case:** Wenn User MKVs direkt bearbeiten sollen (z.B. Chapter-Editor-Feature)

**Status:** 📦 Vorbereitet, noch nicht implementiert

---

#### Option B: pymkv (mkvmerge-Wrapper)

**Technologie:** Python-Wrapper für MKVToolNix

**Installation:**
```bash
pip install pymkv
sudo apt install mkvtoolnix
```

**Features:**
```python
from pymkv import MKVFile

mkv = MKVFile("input.mkv")
mkv.add_track("new_audio.aac")  # Audio-Track hinzufügen
mkv.remove_track(2)  # Subtitle-Track entfernen
mkv.mux("output.mkv")
```

**Vorteile:**
- ✅ Battle-tested (nutzt mkvmerge)
- ✅ Alle MKV-Features (Muxing, Splitting, Chapters)

**Nachteile:**
- ❌ Benötigt mkvtoolnix-Binary
- ❌ Nicht für reines Parsing gedacht

**Use Case:** Wenn Remuxing/Track-Management gewünscht ist

**Status:** 📦 Vorbereitet, noch nicht implementiert

---

### 3. Frontend-Frameworks (Modernisierung, 2.0.0+)

**Aktuell:** Vanilla JavaScript (ES6+)

**Überlegungen für Zukunft:**

#### Option A: Vue.js (Leichtgewichtig)

**Installation:**
```html
<script src="https://cdn.jsdelivr.net/npm/vue@3/dist/vue.global.js"></script>
```

**Vorteile:**
- ✅ Reaktive UI-Updates (kein manuelles DOM-Management)
- ✅ Component-basiert
- ✅ Kleinere Bundle-Size als React

**Beispiel:**
```javascript
const { createApp } = Vue;

createApp({
  data() {
    return { media: [] };
  },
  methods: {
    async loadMedia() {
      this.media = await eel.get_media()();
    }
  }
}).mount('#app');
```

**Use Case:** Wenn UI komplexer wird (z.B. Drag & Drop, Live-Filtering)

---

#### Option B: Alpine.js (Minimal)

**Installation:**
```html
<script src="//unpkg.com/alpinejs" defer></script>
```

**Vorteile:**
- ✅ Minimal (<15KB)
- ✅ Keine Build-Step nötig
- ✅ Ähnlich wie Vanilla JS, aber reaktiver

**Beispiel:**
```html
<div x-data="{ open: false }">
  <button @click="open = !open">Toggle</button>
  <div x-show="open">Inhalt</div>
</div>
```

**Use Case:** Wenn leichte Interaktivität ohne Framework gewünscht ist

---

#### Option C: Bleibe bei Vanilla JS (Aktuell)

**Begründung:**
- ✅ Keine External Dependencies
- ✅ Maximale Kontrolle
- ✅ Kleinere Codebase

**Use Case:** Solange UI nicht zu komplex wird

**Status:** ✅ Aktueller Ansatz bleibt

---

### 4. Playlist-Formate (1.4.0)

**Ziel:** Import/Export von M3U/PLS/XSPF Playlists

#### Option A: m3u8 (Bereits vorhanden!)

**Status:** ✅ Bereits als Dependency vorhanden

**Features:**
```python
import m3u8

# M3U8-Playlist laden
playlist = m3u8.load("playlist.m3u8")
for item in playlist.segments:
    print(item.uri)

# Playlist erstellen
new_playlist = m3u8.M3U8()
new_playlist.add_segment(m3u8.Segment(uri="song1.mp3"))
new_playlist.dump("output.m3u8")
```

**Use Case:** HLS-Streaming, Audio-Playlists

**Status:** 📦 Dependency vorhanden, Feature-Implementation pending

---

#### Option B: python-pls

**Technologie:** PLS-Parser für Winamp/VLC-Playlists

```bash
pip install plsparser
```

**Use Case:** Legacy-Playlist-Support

---

### 5. Audio-Visualisierung (1.5.0+)

**Ziel:** Waveform, Spektrogram, Album Art Animation

#### Option A: Wavesurfer.js (Web-basiert)

**Technologie:** JavaScript Audio Visualization Library

**Installation:**
```html
<script src="https://unpkg.com/wavesurfer.js"></script>
```

**Features:**
```javascript
const wavesurfer = WaveSurfer.create({
  container: '#waveform',
  waveColor: 'violet',
  progressColor: 'purple'
});

wavesurfer.load('audio.mp3');
```

**Vorteile:**
- ✅ Schöne Waveform-Darstellung
- ✅ Interaktiv (Click to seek)
- ✅ Plugin-System (Spectogram, Minimap)

**Use Case:** Premium-UI für Audio-Player

---

#### Option B: librosa (Python Audio Analysis)

**Technologie:** Audio-Feature-Extraktion

```bash
pip install librosa
```

**Features:**
```python
import librosa
import numpy as np

# Waveform extrahieren
y, sr = librosa.load("audio.mp3")

# Spektrogramm generieren
S = librosa.feature.melspectrogram(y=y, sr=sr)

# Als Bild speichern
import matplotlib.pyplot as plt
plt.figure(figsize=(10, 4))
librosa.display.specshow(librosa.power_to_db(S), y_axis='mel', x_axis='time')
plt.savefig("spectrogram.png")
```

**Use Case:** Wenn Audio-Analyse serverseitig nötig ist

---

### 6. Erweiterte Metadaten (1.4.0)

**Ziel:** Lyrics, Cover Art, MusicBrainz-Integration

#### Option A: LyricWiki/Genius API

**Technologie:** Lyrics-Scraping

```bash
pip install lyricsgenius
```

**Features:**
```python
import lyricsgenius

genius = lyricsgenius.Genius("API_TOKEN")
song = genius.search_song("Bohemian Rhapsody", "Queen")
print(song.lyrics)
```

**Use Case:** Automatische Lyrics-Suche für Player

**Status:** 🔮 Recherche, nicht implementiert

---

#### Option B: MusicBrainz API

**Technologie:** Musik-Metadaten-Datenbank

```bash
pip install musicbrainzngs
```

**Features:**
```python
import musicbrainzngs

musicbrainzngs.set_useragent("MyApp", "1.0")
result = musicbrainzngs.search_recordings(artist="Queen", recording="Bohemian Rhapsody")

for recording in result['recording-list']:
    print(recording['title'], recording['id'])
```

**Use Case:** Metadaten-Enrichment (Genre, Release-Date, etc.)

**Status:** 🔮 Recherche, nicht implementiert

---

### 7. Performance-Optimierung (1.4.0)

#### Option A: Caching mit Redis

**Technologie:** In-Memory Cache für Metadaten

```bash
pip install redis
sudo apt install redis-server
```

**Features:**
```python
import redis
import json

r = redis.Redis(host='localhost', port=6379)

# Metadaten cachen
def get_metadata_cached(file_path):
    cached = r.get(file_path)
    if cached:
        return json.loads(cached)
    
    # Parse und cache
    metadata = parse_metadata(file_path)
    r.set(file_path, json.dumps(metadata), ex=3600)  # 1h TTL
    return metadata
```

**Vorteile:**
- ✅ Drastisch schnellerer Library-Scan
- ✅ Shared Cache über Prozesse

**Nachteile:**
- ❌ Zusätzlicher Service (redis-server)
- ❌ Memory-Overhead

**Use Case:** Bei sehr großen Libraries (>10k Dateien)

**Status:** 🔮 Recherche, erst bei Performance-Bottleneck

---

#### Option B: SQLite FTS5 (Full-Text Search)

**Technologie:** SQLite Virtual Table für Volltextsuche

**Features:**
```sql
CREATE VIRTUAL TABLE media_fts USING fts5(title, artist, album);

-- Schnelle Suche
SELECT * FROM media_fts WHERE media_fts MATCH 'queen bohemian';
```

**Vorteile:**
- ✅ Keine zusätzliche Dependency (SQLite built-in)
- ✅ Schnelle Suche in Metadaten

**Use Case:** Wenn Suche langsam wird

**Status:** 🔮 Vorbereitet, SQLite bereits vorhanden

---

## 🗂️ Abhängigkeitsmatrix für zukünftige Features

| Feature | Benötigte Technologie | Priorität | Earliest Version |
|---------|----------------------|-----------|------------------|
| Video-Playback (MP4/WebM) | HTML5 `<video>` | 🔥 Hoch | 1.4.0 |
| MKV-Playback | ffmpeg Transcoding | 🔥 Hoch | 1.4.0 |
| M3U8-Playlist-Support | m3u8 (✅ vorhanden) | 🟡 Mittel | 1.4.0 |
| Chapter-Editing (MKV) | python-ebml | 🟢 Niedrig | 1.5.0 |
| Track-Management (MKV) | pymkv | 🟢 Niedrig | 1.5.0 |
| Waveform-Visualisierung | Wavesurfer.js | 🟡 Mittel | 1.5.0 |
| Lyrics-Integration | lyricsgenius | 🟢 Niedrig | 1.6.0 |
| MusicBrainz-Enrichment | musicbrainzngs | 🟢 Niedrig | 1.6.0 |
| Redis-Caching | redis-py + redis-server | 🟢 Niedrig | 2.0.0 |
| SQLite FTS5-Search | SQLite (✅ vorhanden) | 🟡 Mittel | 1.4.0 |
| Vue.js-Frontend | Vue 3 | 🟢 Niedrig | 2.0.0 |
| Alpine.js-Frontend | Alpine.js | 🟢 Niedrig | 2.0.0 |

---

## 📊 Lizenz-Kompatibilität

Alle recherchierten Technologien sind **GPL-3.0-kompatibel**:

| Lizenz | Beispiele | GPL-3.0 Kompatibel? |
|--------|-----------|---------------------|
| MIT | Video.js, Vue.js, Alpine.js, redis-py | ✅ Ja |
| GPL v2 | pymkv (mkvmerge) | ✅ Ja (kann unter GPL-3.0 verwendet werden) |
| BSD | python-ebml, librosa | ✅ Ja (permissive) |
| LGPL | ffmpeg | ✅ Ja |
| Public Domain | SQLite | ✅ Ja |

---

## 🎯 Empfohlene Roadmap

### Version 1.4.0 (Video-Update)
- ✅ HTML5 Video-Support (MP4/WebM)
- ✅ ffmpeg Transcoding für MKV → MP4
- ✅ M3U8-Playlist-Import/Export
- ✅ SQLite FTS5 für schnellere Suche

**Dependencies:** Keine neuen (ffmpeg + m3u8 bereits vorhanden)

---

### Version 1.5.0 (Erweiterte Features)
- ✅ Waveform-Visualisierung (Wavesurfer.js)
- ✅ python-ebml für Chapter-Editing
- ✅ Cover Art Extraktion/Anzeige

**Neue Dependencies:** `python-ebml`, `wavesurfer.js` (CDN)

---

### Version 1.6.0 (Metadaten-Enrichment)
- ✅ Lyrics-Integration (lyricsgenius)
- ✅ MusicBrainz-Lookup
- ✅ Automatische Genre-Klassifikation

**Neue Dependencies:** `lyricsgenius`, `musicbrainzngs`

---

### Version 2.0.0 (Modernisierung)
- ✅ Vue.js-Frontend (optional)
- ✅ Redis-Caching für große Libraries
- ✅ API-Versionierung (REST API v2)

**Neue Dependencies:** `vue@3`, `redis-py`

---

## 🔧 Installation-Scripts für Zukunfts-Dependencies

### Video-Support (1.4.0)
```bash
# Keine neuen Dependencies - ffmpeg bereits vorhanden
# Optional: Video.js via CDN
```

### MKV-Editing (1.5.0)
```bash
pip install python-ebml pymkv
sudo apt install mkvtoolnix  # Für pymkv
```

### Metadaten-Enrichment (1.6.0)
```bash
pip install lyricsgenius musicbrainzngs librosa
```

### Performance-Upgrade (2.0.0)
```bash
pip install redis
sudo apt install redis-server
sudo systemctl enable redis-server
```

---

## 📝 Fazit

Dieser Logbuch-Eintrag dient als **Technologie-Kompass** für zukünftige Entwicklungen. Alle recherchierten Optionen sind:

1. ✅ GPL-3.0-kompatibel
2. ✅ Python/Web-Stack-konform
3. ✅ Performance-bewusst
4. ✅ Wartbar und gut dokumentiert

**Für Version 1.3.34:** Keine neuen Dependencies nötig - aktueller Stack ist robust.

**Für Version 1.4.0+:** Video-Support ist prioritär, mit minimalem Dependency-Overhead (nur HTML5).

**Nächste Schritte:**
1. Logbuch 97: Detailliertes Design für Video-Support (1.4.0 Vorbereitung)
2. Prototyp: HTML5 Video-Player Integration
3. Backend: ffmpeg-Transcoding-Pipeline für MKV

---

**Status:** 📚 Dokumentiert, bereit für Implementation ab 1.4.0
