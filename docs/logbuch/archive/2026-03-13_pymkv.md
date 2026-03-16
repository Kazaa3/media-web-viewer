# Logbuch-Eintrag: pymkv Integration

**Datum:** 13. März 2026

## Integration von pymkv in Media Web Viewer

### Features & Status
- Die Python-Bibliothek pymkv wurde in das Backend integriert.
- Verfügbarkeit und Version von pymkv werden im Environment-Status angezeigt.
- Ermöglicht das direkte Arbeiten mit Matroska-Dateien (MKV) aus Python heraus.
- Keine Abhängigkeit von mkvinfo CLI: pymkv nutzt eigene Logik und ruft ggf. mkvmerge CLI für Operationen auf.

### Vorteile
- Python-native Manipulation und Analyse von MKV-Dateien.
- Automatische Diagnose, ob pymkv installiert und einsatzbereit ist.
- Erweiterbarkeit für weitere Matroska-Features (z.B. Merge, Edit, Extract).

### Technische Umsetzung
- main.py: `_get_runtime_tools_status()` prüft pymkv und zeigt Version an.
- GUI zeigt pymkv-Status im Bereich FFprobe/MKVinfo.

---
