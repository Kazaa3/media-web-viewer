# Logbuch: Videoplayer – Finalisierte Orchestrierung & Hybrid-Logik (2026-03-15)

**Datum:** 2026-03-15

## 1. Videoauswahl-UI aktualisiert
- Dropdown-Menü ist jetzt wie folgt sortiert und beschriftet:
  1. **vlc pipe (Default / Internal: vlc_pipe):** Hybrid-Modus, versucht Chrome Native, fällt bei Bedarf auf VLC zurück
  2. **FFmpeg (Internal: integrated):** Serverseitiger FFmpeg-Engine streamt fragmented MP4 zu Chrome
  3. **Direct Play (Internal: directplay):** Startet direkt den FFmpeg→VLC-Pipe, ohne Browser-Versuch
  4. **Embedded VLC (Internal: vlc_browser):** VLC transkodiert und streamt ins Browserfenster
  5. **Chrome Native:** Reines Browser-Playback
  6. **VLC (Extern):** Öffnet Datei in externer VLC-Instanz

## 2. "vlc pipe" Hybrid-Logik gefixt
- Logik-Mismatch zwischen `vlc_pipe` und `hybrid` behoben
- Matrix-Fallback korrekt implementiert:
  - Versucht Chrome Native
  - Bei MEDIA_ERR_SRC_NOT_SUPPORTED (Code 4): Toast "Browser unsupported - Falling back to VLC..." und Start des VLC-Pipes
- Logging nutzt konsistent das `[vlc pipe]`-Prefix (Frontend & Backend)

## 3. Lokalisierung konsistent
- `i18n.json` (de/en) aktualisiert: Alle Namen und Benachrichtigungen sind präzise und konsistent
- Fehlende Keys für Fallback-Toast und Pipe-Fehler ergänzt

## 4. Backend-Robustheit
- `stream_to_vlc` ist gegen Pfadprobleme gehärtet und nutzt überall die bevorzugte Bezeichnung `vlc pipe`
- "FEHLER OPENING" und fehlende Optionen sind gelöst
- Player startet standardmäßig im robusten `vlc pipe`-Modus und bietet für alle Formate zuverlässige Wiedergabe

---

*Letzte Änderung: 2026-03-15*
