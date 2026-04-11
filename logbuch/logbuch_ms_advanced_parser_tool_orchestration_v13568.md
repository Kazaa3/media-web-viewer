# Logbuch Meilenstein: Advanced Parser & Tool Orchestration (v1.35.68)

## Ziel
Vollständige Zentralisierung und Modernisierung der Parser- und Tool-Konfiguration. Die Anwendung bietet jetzt eine einzige Quelle für das Verhalten und die Performance der gesamten Parsing-Engine.

---

## Umsetzung & Details

### 1. Advanced Parser Modes
- **Drei Performance-Stufen:**
  - `lightweight`: Schnelles Indexing, minimale Metadaten (nur Filename/Container)
  - `full`: Standard-Extraktion (Mutagen/Pymediainfo)
  - `ultimate`: Tiefenanalyse (FFmpeg/MKVMerge/ISO)
- Steuerung via MWV_PARSER_MODE (z.B. `export MWV_PARSER_MODE=ultimate`)

### 2. Fine-Grained Tool Parameters
- **parser_settings** Registry in config_master.py
- Zentrale Steuerung von Timeout & cli_flags für mkvmerge, ffprobe, ffmpeg, vlc, mkvinfo
- Backend/Frontend-Parität: Einstellungen werden an die UI synchronisiert, Diagnostik kann Tool-Performance in Echtzeit überwachen

### 3. Legacy Registry Cleanup
- **format_utils.py:** Letzte Hardcodings entfernt, nutzt nur noch GLOBAL_CONFIG
- **main.py:** Alle Eel-Endpoints für Config & Kategorien sind synchronisiert und operational

---

## Quick Start Beispiel
```bash
# Ultimate-Mode mit individuellem Tool-Timeout
export MWV_PARSER_MODE=ultimate
export MWV_DEBUG=1
bash run.sh
```

---

## Ergebnis
Die Media Viewer Architektur ist jetzt vollständig zentralisiert und bietet robuste Kontrolle über alle Aspekte der Medienaufnahme und -wiedergabe.

---

**Meilenstein abgeschlossen: Advanced Parser & Tool Orchestration (v1.35.68)**
