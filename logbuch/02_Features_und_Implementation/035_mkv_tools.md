# Logbuch-Eintrag: mkv_tools Integration

**Datum:** 13. März 2026

## mkv_tools Integration in Media Web Viewer

### Features & Status
- Die Runtime-Statusanzeige im Backend (main.py) wurde erweitert:
  - mkvinfo (CLI): Verfügbarkeit und Version werden automatisch erkannt und im GUI-Status angezeigt.
  - python-mkv (pymkv): Verfügbarkeit und Version werden ebenfalls im GUI-Status angezeigt.
- Die GUI zeigt unter FFprobe jetzt auch mkvinfo und python-mkv mit Versionsinformationen an.
- Die Integration ermöglicht eine schnelle Diagnose, ob mkv-basierte Features (z.B. Matroska-Parsing) nutzbar sind.

### Technische Umsetzung
- main.py: Funktion `_get_runtime_tools_status()` prüft mkvinfo (CLI) und pymkv (Python-Bibliothek).
- Versionserkennung erfolgt über `mkvinfo --version` und `pymkv.__version__`.
- Status wird im Environment-Info-API für die GUI bereitgestellt.

### Vorteile
- Nutzer sehen sofort, ob mkv-Tools installiert und einsatzbereit sind.
- Fehlerquellen bei Matroska-Dateien werden schneller erkannt.
- Erweiterbarkeit für weitere mkv-Tools (z.B. mkvmerge) vorbereitet.

---
