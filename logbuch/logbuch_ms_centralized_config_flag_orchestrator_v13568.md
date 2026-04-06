# Logbuch Meilenstein: Centralized Config & Flag Orchestrator (v1.35.68)

## Ziel
Konsolidierung aller Backend- und Frontend-Konfigurations-Toggles, Flags und Umgebungsvariablen in eine zentrale Quelle: src/core/config_master.py

---

## Umsetzung & Details

### 1. Core: Config Master
- **config_master.py** neu erstellt
  - GLOBAL_CONFIG-Dictionary mit Defaults
  - .env-File-Loading (sofern vorhanden) zur Überschreibung der Defaults
  - Unterstützung für Environment-Variable-Overrides (z.B. MWV_DEBUG=1)
  - Helper: get_config(key, default) für sicheren Zugriff

### 2. Backend-Integration (main.py, format_utils.py)
- Import von GLOBAL_CONFIG aus config_master
- eel.get_global_config() und eel.set_config_flag(key, value) API bereitgestellt
- Lokale debug_flags entfernt, zentrale Registry genutzt
- format_utils.py: PARSER_CONFIG entfernt, stattdessen GLOBAL_CONFIG genutzt

### 3. Frontend: Unified Flag Sync
- **common_helpers.js**: syncGlobalConfig() lädt State vom Backend beim Start
- Globales CONFIG-Objekt ersetzt verstreute window.__mwv_* Flags
- **diagnostics_helpers.js**: Alle UI-Toggles (Diagnostic Mode, Raw Mode, ...) nutzen CONFIG und persistieren Änderungen via Backend-API

---

## Offene Frage
- Soll zusätzlich ein lokales config.json für persistente Einstellungen unterstützt werden, oder bleiben .env/Umgebungsvariablen die primäre Override-Quelle?

---

## Verifikation
- Automatisiert: verify_config_sync.py prüft, ob Environment-Variablen Defaults überschreiben
- Browser: "Raw Mode"-Toggle in UI → Backend-GLOBAL_CONFIG aktualisiert sich in Echtzeit (Audit-Log)
- Manuell: .env mit MWV_DEBUG_SCAN=1 → Terminal zeigt Audit-Logs

---

**Meilenstein abgeschlossen: Centralized Config & Flag Orchestrator (v1.35.68)**
