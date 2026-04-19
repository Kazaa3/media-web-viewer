# Implementation Plan – Granular Footer Extension & Hybrid Registry (v1.41.158)

## Ziel
Die Flat-Flag-Architektur bleibt für alle primären Workstation-Toggles erhalten. Die neue `footer_settings`-Struktur ergänzt granular steuerbare Sub-Elemente im Footer. Das Backend-API und die UI-Logik werden hybridisiert, sodass beide Ebenen (flat & nested) unterstützt werden.

---

## 1. BACKEND REGISTRY (Python)
- **[MODIFY] config_master.py**
  - Restoration: Alle 7 Flat-Flags (`enable_...`) bleiben erhalten und sind korrekt kommentiert.
  - Extension: Neues verschachteltes Dictionary `footer_settings` mit:
    - `show_version_info`: Steuert die "v1.41.x"-Versionsanzeige.
    - `show_hydration_labels`: Steuert die "M/R/B"-Buttons im DB-Cluster.
    - `show_danger_zone`: Steuert den "RESET"-Button.
    - `show_sync_status`: Steuert den "● Synchronized"-Status-Text.

## 2. HYBRID BACKEND API (Python)
- **[MODIFY] main.py**
  - Update: `get_footer_registry` gibt ein gemergtes Dictionary aus Flat-Flags und `footer_settings` zurück.
  - Update: `set_footer_element_state` routet automatisch zum richtigen Pfad (flat oder nested) anhand des Key-Namens.

## 3. GRANULAR UI ORCHESTRATION (JS)
- **[MODIFY] ui_core.js**
  - Expansion: `syncUIWithConfig` erhält Logik, um die Sichtbarkeit granularer Elemente zu steuern:
    - Version Info (`#mwv-footer-version`)
    - Hydration Row (`#hud-hydr`)
    - Reset Button (`#footer-btn-reset`)
    - Sync Status Text (`#sync-status`)

---

## Verification Plan
- **Manual Verification:**
  - Primary Toggle Test: Die 6 Header-Icons funktionieren weiterhin über ihre Flat-Flags.
  - Granular Test: Über die Browser-Konsole `footer_settings.show_version_info` auf `false` setzen → Nur die Version verschwindet.

---

**Review erforderlich vor Umsetzung!**
