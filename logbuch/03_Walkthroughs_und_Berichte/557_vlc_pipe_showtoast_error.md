# Logbuch: Fehleranalyse – showToast nicht definiert & VLC Pipe mit mkvmerge (2026-03-15)

**Datum:** 2026-03-15

## 1. Fehler: Uncaught Promise: ReferenceError: showToast is not defined
- Beim Auslösen des Fallbacks (z.B. im Hybrid-Modus) wird versucht, die Funktion `showToast` aufzurufen.
- Ist diese Funktion im aktuellen Scope nicht definiert, führt dies zu einem ungefangenen Promise-Fehler und verhindert die Anzeige der Benachrichtigung.
- **Empfehlung:**
  - Sicherstellen, dass `showToast` global oder im relevanten Scope verfügbar ist, bevor sie aufgerufen wird.
  - Alternativ: Vor dem Aufruf prüfen (`if (typeof showToast === 'function') ...`).
  - Fehler im Logbuch dokumentieren und im UI ggf. als Fallback-Alert anzeigen.

## 2. VLC Pipe mit mkvmerge/mkv startet nicht
- Beim Versuch, mkv-Dateien per mkvmerge über die VLC Pipe abzuspielen, schlägt der Start fehl.
- Ursache: mkvmerge ist für Live-Piping in VLC weniger robust als FFmpeg (insbesondere bei komplexen oder beschädigten Matroska-Containern).
- **Empfehlung:**
  - Für VLC Pipe ausschließlich FFmpeg als Streaming-Engine verwenden (wie bereits im aktuellen System umgesetzt).
  - mkvmerge nur für statische Remuxes oder Dateikonvertierungen nutzen, nicht für Live-Streaming.
  - Fehlerausgaben von mkvmerge/ffmpeg im Backend loggen und im UI anzeigen.

## Ergebnis
- Die Fehlerursachen sind identifiziert und dokumentiert.
- Die Architektur sollte auf FFmpeg für VLC Pipe setzen und showToast robust implementieren.

---

*Letzte Änderung: 2026-03-15*
