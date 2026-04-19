# Walkthrough: Technical Orchestration Centralization (v1.46.017+)

## Datum
12. April 2026

## Zusammenfassung
Die technische Steuerung der Forensic Workstation ist jetzt vollständig konfigurationsgetrieben. Alle Intervalle, Polling-Frequenzen und Hydrations-Counts sind im technical_orchestrator-Registry von config_master.py zentralisiert. Änderungen sind projektweit ohne JS-Anpassungen möglich.

## Key Accomplishments

### 1. Centralized "Technical Orchestrator" Registry
- **config_master.py:**
    - Neues Registry für alle technischen Timing- und Performance-Parameter.
    - Beispiel-Parameter:
        - log_polling_ms: 1000ms (Log-Update-Frequenz)
        - hydration_audit_ms: 2000ms (DOM-Hydration-Check)
        - sentinel_audit_ms: 1000ms (Watchdog)
        - heartbeat_pulse_ms: 5000ms (Backend-Health)
        - mock_count: 12 (Notfall-Mocks)

### 2. Refactored Diagnostic Logic
- **gui_diagnostics.js:**
    - Polling-Geschwindigkeit ist jetzt dynamisch (log_polling_ms).
- **src/core/logger.py:**
    - MAX_BUFFER_SIZE und UI_BROADCAST_COOLDOWN werden aus dem globalen Config gelesen.
    - @contextlib.contextmanager wiederhergestellt.

### 3. Hardened Service Orchestration
- **app_core.js:**
    - Boot Watchdog und Heartbeat nutzen jetzt die zentralen Settings.
- **forensic_hydration_bridge.js:**
    - Audit-Loops und mockCount sind konfigurierbar.
- **nuclear_recovery_pulse.js:**
    - Sichtbarkeits-Pulse sind zentral steuerbar.

## Usage Guide: Hyper-Fast Logging
- log_polling_ms in config_master.py auf 200 setzen für "Hyper-Fast"-Log-Updates.
- ui_broadcast_cooldown_ms auf 10 für maximale Backend-zu-Frontend-Lograte.

## Verification
- window.CONFIG enthält das neue technical_orchestrator-Registry.
- Alle 8 Ziel-JS-Dateien wurden refaktoriert, Hardcodings entfernt.
- logger.py nutzt jetzt config-gesteuerte Schwellenwerte und ist wieder contextmanager-sicher.

---

**Nächste Schritte:**
- Bei Bedarf weitere technische Parameter zentralisieren.
- Performance und Diagnostik-Intervalle nach Bedarf anpassen.
