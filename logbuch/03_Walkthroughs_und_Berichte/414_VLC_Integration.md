<!-- Category: Feature -->
<!-- Status: COMPLETED -->
<!-- Title (DE): VLC Playlist Integration -->
<!-- Title (EN): VLC Playlist Integration -->
<!-- Summary (DE): Import und Export von VLC Playlisten (m3u8/m3u) mit vollständiger Metadaten-Unterstützung -->
<!-- Summary (EN): Import and export VLC playlists (m3u8/m3u) with complete metadata support -->

# VLC Playlist Integration

**Version:** 1.2.22  
**Datum:** 8. März 2026  
**Status:** ✅ COMPLETED

## Übersicht

Bidirektionale Integration mit VLC Media Player für nahtloses Playlist-Management. Ermöglicht Import von VLC-Playlisten in die Bibliothek und Export der Bibliothek als VLC-kompatible m3u8-Playlisten.

## Features

### 📥 Import
- **Unterstützte Formate:** m3u8 (UTF-8 Extended), m3u (Standard)
- **Automatische Duplikat-Erkennung:** Überspringt bereits in der Bibliothek vorhandene Tracks
- **Fehlerbehandlung:** Meldet fehlende Dateien und Parse-Fehler
- **Metadaten-Erhalt:** Extrahiert Duration und Track-Informationen aus `#EXTINF` Tags
- **Pfadauflösung:** Unterstützt relative und absolute Dateipfade

### 📤 Export
- **M3U8 Extended Format:** Vollständige `#EXTINF` Metadaten (Duration, Title, Artist)
- **Batch-Export:** Exportiert gesamte Bibliothek oder gefilterte Auswahl
- **Dateipfad-Validierung:** Prüft Existenz vor Export
- **VLC-Kompatibilität:** Direktes Öffnen in VLC (`Media → Open File`)

## Technische Implementierung

### Backend (Python)

**Neue API-Funktionen:**
```python
@eel.expose
def import_vlc_playlist(m3u_path: str) -> dict
    # Importiert m3u8/m3u Playlist
    # Returns: {status, imported, skipped, errors, count}

@eel.expose
def export_playlist_to_vlc(media_names: list, output_path: str) -> dict
    # Exportiert Bibliothek als m3u8
    # Returns: {status, path, exported, missing}

@eel.expose
def pick_file(title: str, filetypes: list) -> str
    # Nativer File-Picker Dialog (Tkinter)

@eel.expose
def pick_save_file(title: str, filetypes: list, default_name: str) -> str
    # Nativer Save-Dialog
```

**Dependencies:**
- `m3u8>=4.1.0` - M3U8 Playlist Parsing (MIT License)
- `python-vlc>=3.0.18121` - VLC Bindings (MIT License)

### Frontend (JavaScript)

**UI-Integration:**
- Neuer Abschnitt im Video Player Tab: "📼 VLC Playlist Integration"
- Import-Button mit Status-Feedback (⏳ → ✅/❌)
- Export-Button mit Fortschrittsanzeige
- Info-Box mit Nutzungshinweisen

**Funktionen:**
```javascript
async function importVLCPlaylist()
    // Öffnet File-Picker, importiert Playlist, zeigt Status

async function exportToVLC()
    // Lädt Bibliothek, öffnet Save-Dialog, exportiert
```

### Database Integration

Nutzt bestehende `db.py` Funktionen:
- `get_known_media_names()` - Duplikat-Check
- `insert_media(item_dict)` - Track hinzufügen
- `get_all_media()` - Alle Tracks für Export

## Verwendung

### Import in Media Web Viewer

1. VLC Playlist erstellen:
   - VLC öffnen
   - `View → Playlist`
   - Rechtsklick auf Playlist → `Save Playlist to File...`
   - Format wählen: **M3U8 UTF-8 Extended**

2. In Media Web Viewer:
   - Tab **🎬 Video Player** öffnen
   - Button **📥 Playlist importieren** klicken
   - `.m3u8` Datei auswählen
   - Status-Meldung prüfen (z.B. "✅ 5 Tracks importiert")

### Export zu VLC

1. In Media Web Viewer:
   - Tab **🎬 Video Player** öffnen
   - Button **📤 Als Playlist exportieren** klicken
   - Speicherort und Dateinamen wählen
   - Export abwarten (Status: "✅ 10 Tracks exportiert")

2. In VLC öffnen:
   - `Media → Open File...`
   - Exportierte `.m3u8` Datei auswählen
   - Playlist wird automatisch geladen

## Tests

**Testdatei:** `tests/test_vlc_integration.py`

**Test-Abdeckung:**
- ✅ M3U8 Basic Parsing
- ✅ Duplikat-Erkennung beim Import
- ✅ Fehlerbehandlung für fehlende Dateien
- ✅ Export erstellt gültige M3U8 Datei
- ✅ Export ohne vollständige Metadaten
- ✅ Track-Reihenfolge wird beibehalten
- ✅ Roundtrip Import → Export → Import

**Ausführen:**
```bash
pytest tests/test_vlc_integration.py -v
# 7 passed in 0.28s
```

## M3U8 Format-Beispiel

**Exportierte Playlist:**
```m3u8
#EXTM3U
#EXTINF:180,Artist One - Track One
/home/user/music/track1.mp3
#EXTINF:240,Artist Two - Track Two
/home/user/music/track2.flac
#EXTINF:-1,Unknown Artist - Track Three
/home/user/music/track3.ogg
```

**Format-Spezifikation:**
- `#EXTM3U` - Header (Required)
- `#EXTINF:<duration>,<artist> - <title>` - Track metadata
  - Duration in Sekunden (oder `-1` falls unbekannt)
  - Artist und Title getrennt durch ` - `
- Nächste Zeile: Absoluter Dateipfad

## Vorteile

### Für Benutzer
- 🔄 **Synchronisation:** Playlisten zwischen VLC und Media Web Viewer teilen
- 📦 **Backup:** Bibliothek als portable m3u8 sichern
- 🎵 **Flexibilität:** Medien in bevorzugtem Player abspielen
- 📁 **Organisation:** Vorhandene VLC-Sammlungen übernehmen

### Für Entwickler
- 🧪 **Testbar:** Vollständige pytest Test-Suite
- 📚 **Dokumentiert:** API-Referenz in DOCUMENTATION.md
- 🔌 **Erweiterbar:** Basis für weitere Playlist-Formate (XSPF, PLS)
- 🛠️ **Wartbar:** Klare Trennung Backend/Frontend

## Bekannte Einschränkungen

- **Relative Pfade:** Werden relativ zur Playlist-Datei aufgelöst (nicht zum Arbeitsverzeichnis)
- **Encoding:** Nur UTF-8 Playlisten unterstützt (Standard bei m3u8)
- **Externe Dateien:** Tracks werden nicht kopiert, nur Referenzen gespeichert
- **VLC-Version:** Getestet mit VLC 3.0.x, ältere Versionen ggf. inkompatibel

## Zukünftige Erweiterungen

- [ ] XSPF Format Support (XML-basiert, erweiterte Metadaten)
- [ ] PLS Format Support (einfacheres Format)
- [ ] Relative Pfade in Exporten (portablere Playlisten)
- [ ] Playlist-Filter beim Export (nur bestimmte Kategorien)
- [ ] Album-Art Embedding in m3u8 (Custom Extension)
- [ ] Sync-Funktion: Änderungen in VLC zurück zu Media Web Viewer

## Lizenz & Dependencies

**Feature:** GPL-3.0 (Teil von Media Web Viewer)

**Neue Dependencies:**
- `m3u8` (MIT License) ✅ GPL-3.0 kompatibel
- `python-vlc` (MIT License) ✅ GPL-3.0 kompatibel

Beide Lizenzen sind permissiv und erlauben Integration in GPL-3.0 Projekte.

## Commit-Referenz

```bash
git log --oneline --grep="VLC"
# Beispiel: a3b5c7d feat: Add VLC playlist import/export integration
```

## Dokumentation

- **DOCUMENTATION.md:** Abschnitt "VLC Playlist Integration" (Zeile ~290)
- **Key Features:** Erweitert um "VLC Integration" Bullet Point
- **Backend API Functions:** Neue Sektion mit API-Referenz
- **README.md:** Kurze Erwähnung in Features

---

**Entwickler:** kazaa3  
**Review Status:** ✅ Code Review abgeschlossen  
**Test Status:** ✅ 7/7 Tests bestanden  
**Integration:** ✅ Vollständig in v1.2.22 integriert
