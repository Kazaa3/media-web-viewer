# 41 – VLC und MKVToolNix Echtzeit-Streaming

**Datum:** 12.03.2026  
**Version:** 1.3.4  
**Status:** Implementierung Direct Play & Batch-Remux

## Zielsetzung

Implementierung von "Direct Play" (Echtzeit-Streaming via VLC und MKVToolNix) und eines "Fast Batch-Remux" Dienstprogramms zur Verbesserung der Medienwiedergabe und -verwaltung.

## Technische Strategie

### 1. Direct Play (MKVmerge Piping)

Herkömmliches Streaming erfordert oft eine vollständige Transkodierung (CPU-intensiv) oder native Browser-Unterstützung (Format-limitiert). Direct Play nutzt `mkvmerge`, um Dateien in Echtzeit zu remuxen und direkt an VLC zu pipen:

```bash
mkvmerge <input> -o - | vlc -
```

**Vorteile:**
- Keine temporären Dateien auf der Festplatte.
- Sofortiger Start ohne Transkodierungspause.
- Unterstützung für alle MKV-Features (Kapitel, mehrere Tonspuren).

### 2. Fast Batch-Remux

Um die Library konsistent zu halten, wird ein Batch-Dienst implementiert, der alle Video-Container (MP4, AVI, MOV) verlustfrei in MKV umwandelt (Remuxing, nicht Re-Encoding).

## Implementierungsschritte

1.  **Backend (`main.py`):**
    - Prüfung auf `mkvmerge` Binary.
    - `stream_to_vlc`: Startet Popen-Pipeline für Echtzeit-Streaming.
    - `remux_mkv_batch`: Iteriert über Verzeichnis und führt `mkvmerge` aus.
2.  **Frontend (`app.html` / `app.js`):**
    - Neuer Toggle "Direct Play" im Video-Tab.
    - Integration in den VLC-Ribbon.
3.  **Lokalisierung (`i18n.json`):**
    - Ergänzung der neuen Modi und Statusmeldungen.

## Fazit

Diese Erweiterung macht den Video-Player-Tab zum leistungsstarken Werkzeug für High-End-Medienwiedergabe ohne die Einschränkungen von Browser-Codecs.

---

**Status:** 🚀 Implementierung gestartet.
