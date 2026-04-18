# Logbuch: Implementation Plan – Centralized Hydration Orchestration (v1.46.032)

## Ziel
Zentralisierung der Hydration-Steuerung (Mock, Real, Both, DB) in einem Single Source of Truth (SSOT) forensic_hydration_registry in config_master.py. Dadurch wird konsistentes Verhalten zwischen Library-API und Orchestrator sichergestellt.

---

## Maßnahmen
### 1. Backend: config_master.py
- forensic_hydration_registry in GLOBAL_CONFIG definiert:
  ```python
  "forensic_hydration_registry": {
      "mode": "both",                 # "real", "mock", "both"
      "db_active": True,              # Master DB switch
      "mock_limit": 516,              # Zielanzahl für Mock-Assets
      "auto_repair_enabled": True,    # Self-Healing-Flag
      "audit_stage": 0                # Forensik-Stufe (0=Raw, 1=Mock-Only, 2=Sync)
  }
  ```
- Fallback: HYDRATION_MODE = "both" für Legacy-Komponenten.

### 2. Backend: api_library.py
- Alle internen Calls von _apply_library_filters auf apply_library_filters umgestellt.
- get_library und apply_library_filters lesen Status aus GLOBAL_CONFIG["forensic_hydration_registry"].

### 3. Backend: main.py
- set_hydration_mode aktualisiert jetzt GLOBAL_CONFIG["forensic_hydration_registry"]["mode"].
- Lokale HYDRATION_MODE-Initialisierung entfernt.

---

## Verifikation
- [Automatisiert] Syntax-Check main.py, api_library.py, config_master.py (z.B. python3 -m py_compile).
- [Manuell] M/R/B-Toggle im UI: Logs zeigen, dass forensic_hydration_registry aktualisiert wird und die Bibliothek korrekt hydriert.
- [Manuell] DB-LED im Footer spiegelt db_active-Flag wider.

---

*Letztes Update: 18.04.2026*
