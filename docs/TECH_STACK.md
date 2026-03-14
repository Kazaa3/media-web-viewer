# Tech Stack Quick Reference (dict)

**Version:** 1.34  
**Letzte Aktualisierung:** 13. März 2026


## Produktiv-Stack

### Core
- **Python** 3.14.2 (venv)
- **Eel** 0.18.2 (Desktop GUI)
- **Bottle** 0.13.0 (Web Framework)
- **SQLite** 3.x (Database)

### Media Parsing
- **mutagen** 1.47.0 (Fast Tags)
- **pymediainfo** 7.0.1 (Detailed Info)
- **ffprobe** (JSON Parser)
- **ffmpeg** (Transcoding)

### Monitoring & Infrastructure
- **monitor_utils.py** (Watchdog System)
- **psutil** (Process Management)


### Frontend
- **Vanilla JavaScript** (ES6+)
- **HTML5** + **CSS3**
- **Chrome** (Eel Backend)

### Testing
- **pytest** 8.0.0
- **pytest-cov** 4.1.0
- **mypy** 1.9.0

## Multi-Venv Strategie

Das Projekt nutzt spezialisierte virtuelle Umgebungen zur Trennung von Verantwortlichkeiten:

| Venv | Rolle | Zweck |
|------|-------|-------|
| `.venv_core` | **CORE** | Zentrale Laufzeit für die App-Logik. |
| `.venv_build` | **BUILD** | Packaging, Deployment und PyInstaller. |
| `.venv_dev` | **DEV** | Entwicklungstools (Linter, Formatierer). |
| `.venv_testbed` | **TEST** | Integrations- und Performance-Tests. |
| `.venv_selenium` | **E2E** | Automatisierte Browser-Tests. |

Management via: `scripts/manage_venvs.py --status`

## Geplante Features

| Feature | Version | Technologie | Status |
|---------|---------|-------------|--------|
| Video-Support | ${NEXT_VERSION} | HTML5 `<video>` | 🔮 Geplant |
| MKV-Transcoding | ${NEXT_VERSION} | ffmpeg | 🔮 Geplant |
| Playlist-Import | ${NEXT_VERSION} | m3u8 (✅ vorhanden) | 🔮 Geplant |
| GUI-Modernisierung | ${FUTURE_VERSION} | Vue.js / Tailwind | 🔍 Recherche |
| Chapter-Editing | ${FUTURE_VERSION} | python-ebml | 🔮 Recherchiert |
| Waveform-Viz | ${FUTURE_VERSION} | Wavesurfer.js | 🔮 Recherchiert |
| Lyrics-Lookup | ${FUTURE_VERSION} | lyricsgenius | 🔮 Recherchiert |

Vollständige Dokumentation: [logbuch/96_Technologie_Stack_und_Zukunfts_Recherche.md](logbuch/96_Technologie_Stack_und_Zukunfts_Recherche.md)
