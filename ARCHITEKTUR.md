# Architekturüberblick – Media Web Viewer

**Datum:** 13.03.2026
**Autor:** Copilot

## Systemübersicht
Der Media Web Viewer ist eine modulare Desktop-Anwendung zur Medienverwaltung und -wiedergabe. Die Architektur ist auf Erweiterbarkeit, Performance und Plattformunabhängigkeit ausgelegt.

## Komponenten

### Backend
- **Sprache:** Python 3.11+
- **Frameworks:** Bottle (API), Eel (UI-Bridge)
- **Kernmodule:**
  - `main.py`: Orchestrator, API-Entry
  - `db.py`: SQLite-Datenbankzugriff
  - `env_handler.py`: Umgebungsvalidierung
  - `logger.py`: Logging, UI-Logbuffer
  - `media_format.py`: Format- und Kategorielogik
  - `parsers/`: Modulare Metadatenextraktion (Mutagen, FFmpeg, MediaInfo, etc.)
- **Build/CI:** Integrierter Build-Watchdog, automatisierte Tests, Versionierung

### Frontend
- **Technologien:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **UI-Architektur:** Tab-basiert, Event-Loop, i18n-Integration
- **Features:**
  - Responsive Design
  - Dynamische Tab-Verwaltung
  - Status- und Fehleranzeigen
  - Visualisierung von Medienstatistiken

### Datenbank
- **Typ:** SQLite
- **Modell:** Entity-Attribute-Value (EAV) für flexible Metadaten
- **Persistenz:** Medien, Playlists, User-Settings

### Media Tooling
- **Formate:** Audio, Video, Bild, Container (u.a. ALAC, FLAC, MP4, MKV, ISO)
- **Tools:** Mutagen, pymediainfo, FFmpeg, python-vlc, m3u8
- **Transcoding:** Echtzeit-Konvertierung für Browser-Kompatibilität

### Virtual Environment Management
- **Venv/Conda:** Zentrale Steuerung, 5-Venv-Konzept (core, dev, build, selenium, testbed)
- **Dependency-Checks:** Automatisiert via `env_handler.py`

### Build Monitoring & CI/CD
- **Build-Watchdog:** Überwacht und stabilisiert DEB/EXE-Builds
- **CI/CD:** GitHub Actions, automatisierte Tests, Release-Pipeline

## Erweiterbarkeit & Zukunft
- **Parser-Architektur:** Neue Formate/Tools als Plug-in
- **Frontend:** Geplant: React/Vue UI, erweiterte Statistik- und Streaming-Tabs
- **Netzwerk:** SMB/NFS-Streaming, Low-Bandwidth/Heavy-Mode

---

**Fazit:**
Die Architektur des Media Web Viewer vereint modulare Python-Backends, ein modernes Web-Frontend und robuste Build-/Testprozesse zu einer zukunftssicheren Medienplattform.
