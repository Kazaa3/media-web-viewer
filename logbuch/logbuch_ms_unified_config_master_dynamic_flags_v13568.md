# Logbuch Meilenstein: Unified Config Master & Dynamic Flags (v1.35.68)

## Ziel
Vollständige Zentralisierung aller Konfigurations- und Parser-Flags. Die Anwendung nutzt jetzt ein einheitliches Core-Registry-System, das Umgebungsvariablen für alle kritischen Modi und Pfade respektiert.

---

## Umsetzung & Details

### 1. Centralized Modes & Flags
- **Audio vs. Multimedia:** Gesteuert über active_branch (Env: MWV_BRANCH), UI bootet dynamisch im richtigen Modus
- **Parser Modes:** parser_mode (z.B. lightweight) global und env-aware (Env: MWV_PARSER_MODE)
- **SLOW_PARSERS:** Nach config_master.py verschoben, alle Parser-Module nutzen dieselbe Exclusion-Liste

### 2. Storage & Navigation
- **Storage Paths:** library_dir und db_filename zentralisiert, Umschalten der Datenquelle via MWV_LIB_DIR oder MWV_DB
- **Start Tab:** start_tab (Env: MWV_START_TAB) steuert initiale Ansicht in app_core.js (direkter Start in Library, Player oder Video möglich)

### 3. Code Cleanliness
- **format_utils.py:** Hardcodiertes PARSER_CONFIG entfernt, ersetzt durch Alias: PARSER_CONFIG = GLOBAL_CONFIG
- **app_core.js:** Boot-Logik prüft window.CONFIG für Start-Tab und Branch, keine Hardcodierung mehr

---

## Nutzung der neuen Flags

```bash
# Beispiel: Start im Multimedia-Mode auf dem Video-Tab mit Lightweight-Parsing
export MWV_BRANCH=multimedia
export MWV_START_TAB=video
export MWV_PARSER_MODE=lightweight
bash run.sh
```

---

## Ergebnis
Die Konfigurationsarchitektur ist jetzt vollständig modernisiert und bereit für dynamische Environment-Deployments.

---

**Meilenstein abgeschlossen: Unified Config Master & Dynamic Flags (v1.35.68)**
