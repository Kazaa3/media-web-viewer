# Logbuch: Videoplayer – VLC Pipe, Embedded VLC & Hybrid Fallback (2026-03-15)

**Datum:** 2026-03-15

## Wichtige Änderungen

### 1. Neuer Modus: vlc pipe (Default)
- "Local VLC Pipe" wurde in **vlc pipe** umbenannt und ist jetzt die Standardauswahl.
- Streaming-Engine von mkvmerge auf **FFmpeg** umgestellt: bessere Kompatibilität, zuverlässigeres Echtzeit-Muxing für VLC.
- Neues Debug-Logging mit `[vlc pipe]`-Prefix. Fehler beim Piping (z.B. VLC kann Stream nicht öffnen) werden samt FFmpeg-Fehlertext im Backend geloggt und gemeldet.

### 2. Embedded VLC Option
- "VLC Engine → Browser" heißt jetzt **Embedded VLC**.
- Serverseitige VLC-Instanz transkodiert Medien in einen browserfreundlichen MP4-Stream.

### 3. Hybrid Fallback gehärtet
- "Chrome Native (Hybrid VLC Fallback)" erkennt jetzt exakt MEDIA_ERR_SRC_NOT_SUPPORTED.
- Bei Fallback erscheint ein Toast: "Browser unsupported - Falling back to VLC..." für sofortiges User-Feedback.

### 4. Backend-Robustheit & Lint-Fixes
- Pfad-Handling-Bugs in `src/core/main.py` behoben (Linting).
- `stream_to_vlc` unterstützt ISO-Dateien via dvd://-Protokoll.
- Alle Kommando-Argumente werden explizit als String gecastet (Type-Sicherheit).

### 5. Video-Mode-Reihenfolge (neu)
1. **vlc pipe (Default):** FFmpeg → VLC Pipe
2. **Embedded VLC:** VLC transkodiert für Browser
3. **Chrome Native (Hybrid VLC Fallback):** Erst Browser, dann VLC bei Bedarf
4. **FFmpeg Engine → Chrome:** FFmpeg-Transcoder für Browser

## Ergebnis
- VLC-"FEHLER OPENING"-Probleme gelöst (FFmpeg-Pipe ist robuster für Matroska/ISO).
- Playback-Architektur ist klarer, robuster und besser debugbar.
- UI und Backend spiegeln die neuen Modi und Fehlerbehandlungen wider.

---

*Letzte Änderung: 2026-03-15*
