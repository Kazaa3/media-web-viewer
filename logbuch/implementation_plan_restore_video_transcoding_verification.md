# Implementation Plan: Restoring Video Transcoding & Verification

## Problem
Die Funktion `stream_video_fragmented` in src/core/main.py wurde versehentlich beschädigt/teilweise gelöscht. Das hat das Echtzeit-Video-Transcoding (MSE/FragMP4) gebrochen.

---

## Proposed Changes

### Core Backend

**[MODIFY] main.py**
- **stream_video_fragmented:**
  - Generator-Logik für FFmpeg-Output → Bottle-Response wiederherstellen (basierend auf src/core/streams/mse_stream.py).
- **video_remux_stream:**
  - Generator so anpassen, dass Prozess-Cleanup im finally-Block garantiert ist (wurde zuletzt abgeschnitten).
- **Consolidate Imports:**
  - Redundante Imports in Funktionsscope verschieben oder global bereitstellen.

---

### Diagnostics & Verification

**[NEW] verify_video_transcode.py**
- Standalone-Skript zur Überprüfung der Streaming-Endpunkte.
- **Workflow:**
  - Findet eine gültige Videodatei in media/.
  - Startet HTTP-GET auf /video-remux-stream/.
  - Prüft Content-Type und ersten Byte-Stream (ftyp MP4 Header).
  - Verifiziert, dass FFmpeg-Prozess korrekt startet und Daten streamt.

---

## Open Questions
- Hardware-Acceleration erzwingen (h264_vaapi/nvenc) oder Auto-Detection? **Empfehlung:** Auto-Detection, um Produktionsumgebung zu spiegeln.

---

## Verification Plan

### Automated Tests
- `python3 tests/diagnostics/verify_video_transcode.py` ausführen
- `python3 src/core/main.py --test-stream` (falls implementiert)

### Manual Verification
- UI öffnen, Video abspielen, das Transcoding benötigt (z.B. ISO/MKV)
- app.log auf [MSE] und [Remux] Trace-Einträge prüfen

---

**Status:**
- Geplante Wiederherstellung stellt Video-Transcoding und Streaming-Integrität sicher.
- Test- und Diagnose-Tools werden bereitgestellt.
