# Implementation Plan – v1.41.111 Stability Restoration

## Ziel
Behebung einer kritischen zyklischen Importkette, die den Bootvorgang der Anwendung blockiert. Die Abhängigkeitskette entsteht durch: config_master → hardware_detector → logger → config_master (GLOBAL_CONFIG).

---

## Phase 1: Logic Decoupling
- **[MODIFY] config_master.py**
  - Top-Level Cleanup: Entferne `from core import hardware_detector` aus dem Modul-Header.
  - Lazy Injection: Importiere `from core import hardware_detector` lokal innerhalb der Logik, wo `get_hardware_info()` benötigt wird (vermutlich um Zeile 200).

## Phase 2: Registry Hardening
- **[MODIFY] logger.py**
  - Safe Imports: Schütze den Import `from src.core.config_master import GLOBAL_CONFIG` mit try/except oder implementiere Lazy-Loading, sodass der Logger auch initialisiert werden kann, wenn config_master noch nicht vollständig geladen ist.

---

## Verification Plan
- **Boot Test:** Starte `python3 src/core/main.py` und prüfe, ob "Eel loaded successfully" erscheint und das Browserfenster öffnet.
- **Telemetry Validation:** Verifiziere, dass der HUD (PID, BOOT) im Header der legacy app.html befüllt wird – dies bestätigt die Synchronisation von config_master und logger.

---

**Review erforderlich nach Umsetzung!**
