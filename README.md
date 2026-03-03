# GUI Media Web Viewer

Ein benutzerdefinierter Media Player mit eingebetteter Web-GUI. Das Projekt basiert auf Python, [Eel](https://github.com/python-eel/Eel) für das Desktop-Fenster und dem [Bottle](https://bottlepy.org/) Web-Framework für das Streaming. Es unterstützt eine Vielzahl von Audioformaten wie MP3, M4A, M4B, ALAC, FLAC, OGG und WAV.

## Features & Highlights

- **Web-basierte GUI:** Nutzt HTML/JS/CSS für ein modernes Interface, gerendert in einem Chromium-basierten Desktopfenster.
- **Zwei-Spalten-Metadateneditor:** Ein integrierter "Edit"-Tab mit Split-Pane-Layout. Rechts werden dynamisch bearbeitbare Textfelder für alle erkannten Metadaten generiert, links bleibt die durchsuchbare Bibliothek sichtbar.
- **Datei-Browser & Bibliothek-Trennung:** Importiere einzelne Dateien oder durchsuche beliebige Ordner (startend in `/home/xc`) ohne direkten Voll-Scan. Der automatische Start-Scan indexiert nur explizit den Projekt-`media/`-Ordner.
- **Persistente Debugging-Konsole:** Im "Debug DB"-Tab kann neben der rohen JSON-Ausgabe der Datenbank auch die Live-Python-Konsole verfolgt werden. Alle Start-Logs und Scans werden gepuffert und dem Frontend beim Start zur Verfügung gestellt.
- **On-the-Fly Transcoding:** Formate, die vom Browser nicht nativ unterstützt werden (z. B. Apple Lossless `ALAC`), werden im Hintergrund via `ffmpeg` gecached und als `FLAC` gestreamt.
- **Intelligente Metadaten-Extraktion:** Nutzt eine vierstufige Pipeline (`filename`, `mutagen`, `ffmpeg`, `pymediainfo`), um Dauer, Cover-Bilder, Bitraten und Tags zuverlässig auszuwerten.
- **Eingebettete Cover-Art:** Holt Albumcover direkt aus den ID3/MP4/FLAC-Headern und serviert sie nativ über eine eigene Bottle-Route im Player und der Sidebar.
- **SQLite-Datenbank:** Permanente Speicherung aller Metadaten zur schnellen Suche und Anzeige.

## Systemvoraussetzungen

- Python 3.11+
- Ein installiertes und im System-PATH verfügbares `ffmpeg`.
- Benötigte Python-Pakete (`eel`, `bottle`, `mutagen`, `pymediainfo`).

## Installation & Start

```bash
# Empfohlen: Virtuelles Environment nutzen
# python -m venv .venv
# source .venv/bin/activate

# Abhängigkeiten installieren
pip install eel bottle mutagen pymediainfo

# Programm starten
python main.py
```

## Projektstruktur

```
gui_media_web_viewer/
├── main.py               ← Haupteinstiegspunkt, Eel-Bootstrapping, Startup-Logik, MediaItem
├── db.py                 ← SQLite-Operationen (init, insert, clear, update_tags)
├── parsers/              ← Extraktions-Pipeline
│   ├── filename_parser.py
│   ├── mutagen_parser.py
│   ├── ffmpeg_parser.py
│   └── pymediainfo_parser.py
├── web/                  ← Frontend GUI (wird von Eel geladen)
│   ├── app.html          ← Das komplette UI mit Tabs (Player, Browser, Edit, Debug)
│   ├── app_bottle.py     ← Paralleler Bottle-Server für Audio-Streaming und Cover
│   └── script.js         ← Init-Logik und Dateibrowser-Anbindung
├── tests/                ← isolierte Entwickler-Skripte
├── media/                ← Standard-Indexierungsordner (SCAN_MEDIA_DIR)
└── media_library.db      ← SQLite DB (wird lokal angelegt)
```

## Kernmodule im Detail

### 1. `main.py` (App-Controller & Backend)

Das Herzstück der Anwendung, welches Eel initiiert und die Brücke zwischen UI und Python schlägt.
- **Konstanten-Trennung:** `SCAN_MEDIA_DIR` bestimmt den Ordner für den automatischen Bibliotheksaufbau (Projekt-Ornder `media/`). `BROWSER_DEFAULT_DIR` steuert nur die Startansicht im manuellen Browser-Tab.
- **`scan_media()`**: Wird nun exklusiv vom Startup-Prozess (oder manuell aus der GUI mit klaren Pfaden) gesteuert, um doppelte / unbeabsichtigte `/home`-Scans zu verhindern.
- **Log-Puffer:** Eine globale `LOG_BUFFER` Liste fängt alle `debug_log()` Aufrufe (und den Python-Startbefehl) auf. Die GUI kann diese via `@eel.expose("get_debug_logs")` asynchron laden.

### 2. `web/app.html` & `script.js` (Frontend)

Das Frontend ist in ein Tab-System unterteilt:
- **Player/Library:** Zeigt die indexierten Listen, ein dauerhaftes Footer-Audio-Element und eine Sidebar mit Metadaten.
- **Browser:** Lässt das lokale Dateisystem erkunden. Klickt man auf "➕", wird die Datei der Bibliothek hinzugefügt, ohne alles neuzuladen.
- **Edit:** Verwendet einen nativen HTML-Spalten-Teiler (`splitter-v`). Klickt man links auf ein Lied, parst JS alle DB-Felder und baut dynamisch die Eingabefelder für den Editor auf. Änderungen gehen an `db.py`.
- **Optionen/Debug:** Hier lassen sich Konsolen-Outputs betrachten, Feature-Flags schalten und die Datenbank komplett zurücksetzen.

### 3. `parsers/` (Metadaten-Pipeline)

Jede Audio-Datei wandert beim Scan durch vier Parser in dieser Reihenfolge:
1. **`filename_parser`**: Versucht Titel und Artist aus dem Dateinamen zu erraten.
2. **`mutagen_parser`**: Hauptparser für ID3/MP4/Vorbis-Tags, Sampling-Raten und Cover-Verfügbarkeit. (Schnell & Nativ).
3. **`pymediainfo_parser`**: Springt ein, wenn wichtige Infos wie Dauer oder tiefe Container-Infos fehlen.
4. **`ffmpeg_parser`**: (Optionaler Fallback) via FFmpeg CLI für absolute Härtefälle.

Jeder Parser erhält das Dictionary des vorherigen Parsers und überschreibt nur leere Werte (non-destructive).

### 4. `app_bottle.py` (Streaming & Covers)

Eel ist primär für Websockets (UI-Logik) zuständig. Für große Media-Dateien oder Suchvorgänge parallel im Netzwerk braucht es dediziertes HTTP.
- **Laden von Covern (`/cover/<file>`)**: Liest ID3/MP4-Metadaten on-the-fly im Speicher aus und serviert das Binärbild als `image/jpeg` oder `png`.
- **Media-Streaming (`/media/<file>`)**: Erkennt Dateiendungen. Unterstützt Datei-Serving anhand des absoluten Pfades aus der Datenbank statt fester Ordnerbindungen.
- **Transcoding**: Wenn eine `.flac_transcoded` Endung angefragt wird, spawnt ein FFmpeg-Subprozess, wandelt die Datei temporär in `.cache` um und streamed das verdauliche FLAC an den Browser.
