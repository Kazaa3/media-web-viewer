<!-- Category: Übersicht -->

# Logbuch - Media Web Viewer Dokumentation

Strukturierte Dokumentation aller Entwicklungsschritte, Aufgaben und Implementierungen für die Media Web Viewer Anwendung.

---

## 📑 Inhaltsverzeichnis

### 🔍 Untersuchungen & Verifikationen
- **01_Media_Player_Investigation.md** - Untersuchung des Media Players und Kapitel-Funktionalität
- **04_Parser_Tab_Verification.md** - Parser-Tab Verifikation und Komponentenprüfung
- **05_Test_Tab_Verification.md** - Test-Tab Überprüfung und Testausführung
- **10_Inspect_Parser_Tab.md** - Detaillierte Inspektion des Parser-Tabs
- **17_UI_Test_Checklist.md** - UI Test Checkliste für GUI-Überprüfung
- **26_GUI_Verification_Checklist.md** - Umfassende GUI Verifizierungs-Checkliste

### 🧪 Tests & Test-Suiten
- **02_Dynamic_Test_Suite_Discovery.md** - Dynamische Erkennung von Test-Suiten
- **21_Dynamic_Test_Suite.md** - Test-Suite Implementierung
- **23_Implementation_Plan_Test_Tab.md** - Implementierungsplan für Test-Tab
- **24_Making_Test_Suites_Editable.md** - Bearbeitbare Test-Suiten
- **30_Task_Test_Tab.md** - Aufgaben für Test-Tab Verbesserungen

### 📊 Parser & Metadaten-Extraktion
- **07_Parser_Benchmarking.md** - Parser Performance Benchmarking
- **08_Chapter_Support.md** - Audiobook Chapter Support Implementierung
- **09_Chapter_Sorting.md** - Chapter Sorting und Media-Kategorisierung
- **12_Parser_Chain_Optimization.md** - Parser Chain Optimierung
- **13_Parser_Tab_Settings.md** - Parser Settings Tab Implementierung
- **14_Parser_Enhancements.md** - Parser Verbesserungen
- **19_Capture_Test.md** - Metadaten Capture Tests
- **20_Database_Duplicates.md** - Datenbank Duplikat-Handling
- **22_Extract_Metadata.md** - Metadaten Extraktions-Strategie
- **27_Natural_Sorting.md** - Natural Sorting für numerische Reihenfolge

### 🎨 UI & Funktionen
- **03_Chapter_Sorting_Walkthrough.md** - Chapter Sorting Walkthrough
- **11_Metadata_Editor.md** - Metadaten-Editor UI Integration
- **15_Rename_Media.md** - Medien Umbenennen & Löschen Funktionalität
- **16_Task_Debug_Flags_Sync.md** - Debug Flags Synchronisierung
- **25_Media_Categorization.md** - Media Datei-Kategorisierung
- **28_Premium_Sidebar_Info.md** - Sidebar Info Anzeige

### 📋 Planung & Überblick
- **06_Rework_Missing_Features.md** - Rework fehlender Funktionen
- **18_Todo_Features_Tasks.md** - TODO-Liste Features und Aufgaben
- **29_Task_Fix_Missing_Items.md** - Aufgabe: Fehlende GUI Elemente beheben
- **31_Feature_Liste.md** - Feature Liste und Status
- **32_Logbook_Index.md** - Logbook Index und Verweise
- **33_Unsort_Notes.md** - Unsortierte Notizen und Ideen
- **34_Walkthrough.md** - Allgemeiner Walkthrough

---

## 🎯 Kategorien

### Nach Komponente
- **Parser**: 07, 08, 09, 12, 13, 14, 19, 20, 22, 27
- **Tests**: 02, 21, 23, 24, 30
- **UI/Frontend**: 03, 11, 15, 16, 25, 28
- **Verifikation**: 01, 04, 05, 10, 17, 26

### Nach Status
- **Implementiert**: 02, 03, 11, 13, 14, 15, 16, 21, 24
- **In Planung**: 06, 18, 29, 31
- **Verifikation ausstehend**: 01, 04, 05, 10, 17, 26

---

## 📌 Schnellzugriff

- **Anfangen**: README → Feature_Liste → Todo_Features_Tasks
- **Parser Setup**: Parser_Benchmarking → Parser_Chain → Parser_Tab
- **Tests Setup**: Dynamic_Test_Suite → Implementation_Plan → Test_Tab
- **UI/Verifikation**: GUI_Verification → UI_Test_Checklist

---

*Zuletzt aktualisiert: 4. März 2026*
│   ├── ffmpeg_parser.py
│   └── pymediainfo_parser.py
├── web/                  ← Frontend + Bottle-Webserver
│   ├── app.html          ← GUI (HTML/CSS/JS) mit Tabs (Library, Tests, Options)
│   ├── app_bottle.py     ← Bottle-Server mit Routen: /media/, /cover/
│   └── script.js         ← JavaScript für die GUI
├── tests/                ← Unit-Tests (Pytest) für DB, MediaItem und Parser
├── media/                ← Multimedia-Dateien (gitignored)
└── media_library.db      ← SQLite-DB (gitignored, wird automatisch erzeugt)
```

## Core Modules

### main.py

| Bereich | Beschreibung |
|---------|-------------|
| **API Exposure** | Exponiert Funktionen für das Frontend: `get_library`, `run_tests`, `get_debug_logs`, etc. |
| **Parser-Pipeline** | Koordiniert `filename → container → mutagen → pymediainfo → ffmpeg` |
| **scan_media()** | Eel-exposed: löscht DB, scannt alle Dateien neu, nutzt `MediaItem` |
| **run_tests()** | Führt ausgewählte Pytest-Suiten aus und gibt Ergebnisse an das GUI zurück. |
| **Startup** | `db.init_db()` → `eel.init()` → `eel.start()` |

### models.py

| Klasse | Beschreibung |
|--------|-------------|
| **MediaItem** | Repräsentiert ein Medium; extrahiert Dauer, Tags und Kapitel. |
| **to_dict()** | Formatiert Daten für das Frontend (inkl. Transkodierungs-Flags). |

### db.py

| Funktion | Beschreibung |
|----------|-------------|
| `init_db()` | Erstellt Tabellen `media`, `playlists`, `playlist_media` |
| `clear_media()` | Löscht alle Einträge aus `media` (für Refresh) |
| `insert_media()` | Fügt ein MediaItem-Dict ein (Tags als JSON-String) |
| `get_all_media()` | Gibt alle Medien als Liste von Dicts zurück |
| `get_known_media_names()` | Gibt Set aller bekannten Dateinamen zurück |

### Parser-Pipeline (`parsers/`)

| Reihenfolge | Parser | Quelle | Was er liefert |
|:-----------:|--------|--------|----------------|
| 1 | `filename_parser` | Dateiname | Basis-Tags: title, artist, Dateigröße |
| 2 | `mutagen_parser` | Mutagen-Lib | ID3/MP4/Vorbis-Tags, Cover-Erkennung, Bitrate, Samplerate |
| 3 | `ffmpeg_parser` | FFmpeg CLI | Container-Format, Codec, Bitdepth (Fallback) |
| 4 | `pymediainfo_parser` | pymediainfo | Ergänzende/fehlende Metadaten |

> Jeder Parser bekommt das bisherige `tags`-Dict und ergänzt fehlende Werte, ohne vorhandene zu überschreiben.

### Web-Frontend (`web/`)

| Datei | Beschreibung |
|-------|-------------|
| `app.html` | Komplette UI: Sidebar (Cover, Metadaten), Medienliste, Audio-Player, Tab-System (Library + Debug) |
| `app_bottle.py` | Bottle-Routen: `/media/<file>` (mit ALAC→FLAC Transkodierung + Caching), `/cover/<file>` (eingebettetes Cover-Art) |

## Transcoding

Dateien mit Apple Lossless (ALAC) Codec können nicht nativ im Browser abgespielt werden. Die App erkennt das und:

1. **`main.py`**: Setzt `is_transcoded = True` wenn Codec = ALAC
2. **`app.html`**: Hängt `.flac_transcoded` an die Media-URL an
3. **`app_bottle.py`**: Erkennt die Endung, transkodiert via `ffmpeg` nach FLAC, cached das Ergebnis in `media/.cache/`
4. **UI**: Zeigt `⚠️ Datei wird on-the-fly für den Webplayer transkodiert und als FLAC gestreamt.`
