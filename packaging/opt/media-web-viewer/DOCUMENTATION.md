# Technical Documentation: Media Web Viewer (v1.2.22)

## 1. Technical Architecture & Data Flow
Media Web Viewer follows a decoupled architecture using Python for the heavy lifting and Vanilla JS for the presentation layer.

### Core Technologies
- **Backend (Python 3.11+)**: Handles file system access, metadata parsing, database operations, and media streaming.
- **Frontend (Vanilla JS/CSS/HTML)**: Implements a responsive, glassmorphism UI. No heavy frameworks are used.
- **EEL Bridge**: Facilitates bidirectional communication via WebSockets.
- **Bottle Server**: Provides internal API endpoints for media and cover art streaming.

### Data Flow Overview
`Media File` → `Parser Chain` → `Python dict` → `SQLite + JSON` → `Eel (WebSocket)` → `JS Frontend Object`

---

## 2. Metadata Extraction Pipeline
The application uses a sequential, additive parser chain to ensure maximum metadata accuracy with minimum overhead.

### The Parser Chain
| Order | Parser | Source | Library/Tool | Responsibility |
|:-----:|--------|--------|--------------|----------------|
| 1 | `filename` | Dateiname | Regex | Title, Artist, Year fallback. |
| 2 | `container` | Header | Python | Format identification (MKV, MP4, etc.). |
| 3 | `mutagen` | Tags | Mutagen | ID3, Vorbis, MP4 tags, Covers, Chapters. |
| 4 | `ffmpeg` | CLI | FFmpeg | Codec verification, Bit depth, Transcoding detection. |
| 5 | `pymediainfo`| MediaInfo | pymediainfo | Detailed technical data (v1.2.21+). |

### Granular Metadata Separation (v1.2.21)
Starting with v1.2.21, metadata is strictly separated into four fields for consistency:
- **Extension**: Physical file extension (`.mp3`, `.mkv`).
- **Container**: Media container detected (`mp4`, `flac`, `wav`).
- **Tag Type**: Format of internal tags (`ID3v2.3`, `m4tags`, `vorbis comment`).
- **Codec**: Encoding format (`aac`, `mp3`, `pcm_s16le`).

---

## 3. Database & Persistence Structure
The persistence layer uses SQLite with specialized JSON columns for technical flexibility.

### DB Schema Reference
```python
# table: media
# columns: id, name, path, type, duration, category, 
#          is_transcoded, transcoded_format, tags (JSON TEXT),
#          extension, container, tag_type, codec

def init_db():
    conn = sqlite3.connect(DB_FILENAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS media (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            path TEXT,
            type TEXT,
            duration TEXT,
            category TEXT,
            is_transcoded BOOLEAN,
            transcoded_format TEXT,
            tags TEXT,           -- JSON serialized dict
            extension TEXT,
            container TEXT,
            tag_type TEXT,
            codec TEXT
        )
    """)
    # ... migration logic for legacy databases ...
    conn.commit()
```

### JSON Serialization Strategy
To balance performance and flexibility, complex tags (chapters, parser timings, technical flags) are stored as serialized strings.
- **Storage**: `json.dumps(tags_dict)` → `SQLite TEXT`.
- **Retrieval**: `json.loads(row['tags'])` → `Python dict`.

---

## 4. Transcoding & Streaming Logic
Files not natively supported by browsers (ALAC/WMA) are transcoded on-the-fly.

### Workflow
1. **Detection**: `is_transcoded = True` if Codec = ALAC or WMA.
2. **Request**: Frontend requests `/media/<id>.flac_transcoded`.
3. **Execution**: `app_bottle.py` spawns `ffmpeg` process.
4. **Caching**: Results are cached in `media/.cache/` to speed up future access.

---

## 5. Development Standards & Testing

### Code Style (Standards)
- **Python**: PEP 8 compliant, formatted with **Black** (88 chars), verified with **Flake8**.
- **JavaScript**: Semicolons used, 2-space indentation.
- **Bilingual Support (i18n)**: All UI strings must use the `i18n.json` mapping.

### Integrated Test Suite
The app includes a GUI-integrated test runner based on `pytest`.
```python
def test_mp3_parsing():
    # Example logic used in tests/
    item = parse_file("test.mp3")
    assert item['extension'] == "mp3"
    assert item['tag_type'] == "ID3v2.3"
```

---

## 6. Logbook & Features System
The "Logbuch" tab uses Markdown files with specialized metadata headers.
```markdown
---
Title_DE: Metadaten-Trennung v1.2.21
Category: Parser
Status: COMPLETED
Summary_DE: Trennung von Extension, Container, Tag-Typ und Codec.
---
```
This metadata is parsed at runtime to populate the "Features & Updates" dashboard in the GUI.

---

## 7. Packaging & Environment
The project is optimized for Debian-based systems.

### .deb Creation
Run `bash build_deb.sh` to stage the application in `packaging/` and build a package using `dpkg-deb`.

### Development Environments
- **Conda/Mamba**: Use `environment.yml` for a reproducible cross-platform setup.
- **Python venv**: Use `requirements.txt` and ensure `ffmpeg` and `mediainfo` are in system PATH.

---

## 8. Project Structure / Struktur
Detailed overview of the project's file organization:

```text
media-web-viewer/
├── VERSION               ← Central version number (1.2.22)
├── Doxyfile              ← Doxygen configuration
├── environment.yml       ← Conda/Mamba environment setup
├── main.py               ← App entry point & Backend API
├── models.py             ← MediaItem data model (parsing, transcoding logic)
├── db.py                 ← SQLite database logic (init, insert, query, clear)
├── requirements.txt      ← Python package dependencies
├── DOCUMENTATION.md      ← This comprehensive technical manual
├── README.md             ← Concise project overview
├── DEPENDENCIES.md       ← Complete dependency list with licenses
├── build_deb.sh          ← Script to build a .deb package
├── parsers/              ← Metadata extraction pipeline
│   ├── media_parser.py   ← Parser orchestrator
│   ├── filename_parser.py
│   ├── container_parser.py
│   ├── mutagen_parser.py
│   ├── ffmpeg_parser.py
│   ├── pymediainfo_parser.py
│   └── format_utils.py   ← Codec formatting, parser configuration
├── web/                  ← Frontend + Bottle web server
│   ├── app.html          ← Full UI (tabs: Player, Browser, Edit, Tests, Logbook, …)
│   ├── app_bottle.py     ← Routes for media and cover art serving
│   ├── script.js         ← Frontend JavaScript logic
│   └── i18n.json         ← Localization strings (DE/EN)
├── tests/                ← pytest unit tests
├── logbuch/              ← Development logbook (Markdown entries)
├── packaging/            ← .deb packaging files (DEBIAN/, usr/)
└── media/                ← Your media files go here (gitignored)
```

---

## 9. Technology Tree / Technik-Baum
Hierarchical overview of the system layers and dependencies:

```text
Media Web Viewer (v1.2.22)
├── Frontend Layer
│   ├── HTML5/CSS3 (Responsive Design, Glassmorphism)
│   ├── Vanilla JavaScript (EEL Integration, Event Handling)
│   └── i18n System (German/English, JSON-based localization)
├── EEL Bridge
│   ├── WebSocket Communication (@eel.expose decorators)
│   ├── JSON Serialization (Python dict ↔ JS object)
│   └── Callback Handling (Async/await patterns)
├── Backend (Python 3.11+)
│   ├── Eel Framework (Desktop GUI bridge)
│   ├── Bottle Web Server (API routes, media streaming)
│   ├── Threading Support (Background tasks, indexing)
│   └── Exception Handling (Graceful error propagation)
├── Data Processing
│   ├── Parser Pipeline (Filename → Container → Mutagen → FFmpeg → pymediainfo)
│   ├── Transcoding Engine (ALAC/WMA → FLAC/OGG conversion)
│   ├── Category Detection (Smart media classification)
│   └── Cover Art Extraction (Embedded images from containers)
├── Data Persistence
│   ├── SQLite Database (media_library.db with JSON columns)
│   ├── JSON Config Files (settings.json, cache files)
│   └── Debug Flags (Per-module configuration)
├── System Integration
│   ├── .deb Packaging (Debian/Ubuntu distribution)
│   ├── FFmpeg Integration (Media transcoding, fallback parsing)
│   ├── Tkinter Dialogs (File browser, system integration)
│   └── File System Access (Media directory scanning)
└── Development & Testing
    ├── pytest Framework (Unit tests, fixtures)
    ├── Coverage Tools (Code coverage reports)
    ├── Black Formatter (PEP 8 code style)
    ├── Flake8 Linter (Code quality checks)
    └── Git Version Control (Change tracking)
```

---

## 10. Logging & Debugging System (v1.2.22+)
The application uses a centralized, multi-target logging system designed for both developers and end-users.

### Log Targets
- **Console**: Standard output for CLI debugging.
- **File**: Persisted to `~/.media-web-viewer/app.log` (Rotating, 5MB max, 3 backups).
- **UI Buffer**: A circular buffer (1000 lines) accessible via the "Debug Logs" tab in the GUI.

### Functional Debugging (DEBUG_FLAGS)
Debugging is granular. Instead of a single toggle, the system uses `DEBUG_FLAGS` to enable logs for specific components:

| Flag | Component | Responsibility |
|------|-----------|----------------|
| `system` | Core | Overrides all other flags (Force all logs). |
| `start` | Startup | Initialization and boot sequence. |
| `scan` | Parser | Detailed file indexing and matching info. |
| `db` | Database | SQL queries and record insertion details. |
| `api` | API/Eel | Function calls between JS and Python. |
| `web` | Server | Bottle internal routes and static serving. |
| `i18n` | Locale | Localization and translation lookups. |
| `websocket` | Eel/WS | WebSocket connection and protocol logs. |
| `performance`| Timing | Execution times and efficiency metrics. |
| `metadata` | Tags | Detailed extraction results for media tags. |
| `transcode` | FFmpeg | Server-side transcoding/caching details. |
| `file_ops` | FS | File renames, deletions and mutations. |
| `network` | HTTP | Inbound request logging (Method, URL). |
| `ui` | Frontend | UI-specific logic bridged from JS. |
| `player` | Audio | Playback state and control events. |
| `lib` | Library | High-level library management logic. |
| `tests` | Tests | Internal test suite execution logs. |

### Usage in Code
```python
import logger
# Basic logging
logger.get_logger("component").info("Standard message")
# Flag-controlled debugging
logger.debug("scan", "Attempting to parse complex filename...")
```

---
*Technical Manual v1.2.22. Developed by kazaa3.*