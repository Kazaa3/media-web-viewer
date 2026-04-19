# Implementation Plan – Footer Control Backend API (v1.41.156)

## Ziel
Ein dedizierter Backend-API-Abschnitt in main.py ermöglicht die programmatische Steuerung und Abfrage aller Elite-Footer-Diagnoseelemente. Damit kann der Backend-Code gezielt einzelne Footer-Komponenten ein-/ausblenden und den Zustand persistent verwalten.

---

## 1. BACKEND API (Python)
- **[MODIFY] main.py**
  - Neuer Abschnitt: "UI & Footer Orchestration API"
  - Implementierung:
    - `get_footer_registry()`: Gibt alle Footer-relevanten Flags aus `GLOBAL_CONFIG['ui_settings']` zurück.
    - `set_footer_element_state(element_id, is_active)`: Setzt gezielt den State eines Footer-Elements und persistiert die Änderung in config_master.py (über `set_ui_config_value`), inkl. Spezial-Logging für das Footer-System.

## 2. REGISTRY PERSISTENCE (Python)
- **[MODIFY] config_master.py**
  - Gruppiere alle neuen Footer-Flags logisch, damit sie von der neuen API einfach abgerufen werden können.

---

## Verification Plan
- **Automated Verification:**
  - Mit einem Scratch-Script werden die neuen Eel-Funktionen aufgerufen (Frontend-Mock), um zu prüfen, ob `GLOBAL_CONFIG` korrekt aktualisiert wird.
- **Manual Verification:**
  - Über die Browser-Konsole (via eel) wird `set_footer_element_state` aufgerufen, um zu prüfen, ob die UI-Elemente und Header-Toggle-Buttons korrekt ein-/ausgeblendet werden.

---

**Review erforderlich vor Umsetzung!**
