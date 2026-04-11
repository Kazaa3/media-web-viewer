# Logbuch Meilenstein: Finalized Centralized Config & Flag Control (v1.35.68)

## Ziel
Vollständige Vereinheitlichung aller Backend- und Frontend-Settings in ein zentrales, full-stack Registry-System.

---

## Umsetzung & Details

### 1. Single Source of Truth
- Alle Flags & Settings (Raw Mode, Diagnostic, Parser Config, ...) werden zentral in **config_master.py** verwaltet

### 2. Environment Variable Support
- Jedes Setting kann per System-Umgebungsvariable vor dem Start überschrieben werden (z.B. export MWV_PORT=9000)

### 3. Real-Time Full-Stack Sync
- **Backend:** get_global_config und set_global_config via Eel-API verfügbar
- **Frontend:** Hydriert window.CONFIG beim Start automatisch, UI und Server sind immer synchron

### 4. Diagnostic Uniformity
- UI-Toggles persistieren Änderungen direkt ins Backend (keine Sync-Drift mehr, "0-Items"-Bugs ausgeschlossen)

---

## Verifikation
- Environment-Variablen (MWV_DEBUG=1, MWV_PORT=9000) überschreiben Defaults korrekt
- Frontend lädt und nutzt diese Overrides beim Initialisieren

---

**Meilenstein abgeschlossen: Finalized Centralized Config & Flag Control (v1.35.68)**
