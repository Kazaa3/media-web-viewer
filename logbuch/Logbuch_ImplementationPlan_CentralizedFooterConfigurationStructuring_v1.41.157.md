# Implementation Plan – Centralized Footer Configuration Structuring (v1.41.157)

## Ziel
Die technischen Footer-Flags werden in config_master.py in ein zentrales, verschachteltes Dictionary `footer_settings` überführt. Die gesamte Sichtbarkeits- und Steuerungslogik wird auf diese neue Struktur umgestellt, um Wartbarkeit und Übersicht zu maximieren.

---

## 1. BACKEND REGISTRY (Python)
- **[MODIFY] config_master.py**
  - Refactor: Entferne alle flachen `enable_...`-Footer-Flags.
  - New Structure: Füge ein verschachteltes `footer_settings`-Dictionary zu `ui_settings` hinzu:
    ```python
    "footer_settings": {
        "sync_anchor": True,      # Anchor Icon
        "hud_cluster": True,      # Grid Icon
        "db_status": True,        # Server Icon
        "zen_mode": True,         # Moon Icon
        "diagnostics": True,      # Pulse Icon
        "auditor": True           # Shield Icon
    }
    ```

## 2. BACKEND API (Python)
- **[MODIFY] main.py**
  - Update: Passe `get_footer_registry` an, sodass das neue verschachtelte Objekt zurückgegeben wird.
  - Update: Passe `set_footer_element_state` an, sodass Dot-Notation (z.B. `footer_settings.sync_anchor`) unterstützt wird.

## 3. UI ORCHESTRATION (JS)
- **[MODIFY] ui_core.js**
  - Engine Update: Die Sichtbarkeits-/Hydrationslogik liest jetzt aus dem neuen verschachtelten `footer_settings`-Pfad.

---

## Verification Plan
- **Manual Verification:**
  - Toggle Test: Alle 6 Header-Buttons zeigen/verstecken die Footer-Komponenten gemäß der neuen Konfiguration.
  - Persistence Test: Änderung eines States in der UI wird korrekt im verschachtelten `footer_settings`-Objekt in config_master.py gespeichert.

---

**Review erforderlich vor Umsetzung!**
