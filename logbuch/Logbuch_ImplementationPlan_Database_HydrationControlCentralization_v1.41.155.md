# Implementation Plan – Database & Hydration Control Centralization (v1.41.155)

## Ziel
Die Steuerung des gesamten technischen Footer-Clusters (DB-Status, Hydration-Buttons, Probe/Reset) wird in den Header zentralisiert. Ein neuer Amber-Button im Header toggelt die Sichtbarkeit aller zugehörigen Footer-Elemente.

---

## 1. BACKEND REGISTRY (Python)
- **[MODIFY] config_master.py**
  - Neuer Flag: `enable_footer_db_status: True` in `ui_settings` für globale Steuerung.

## 2. UI ORCHESTRATION (HTML/JS)
- **[MODIFY] app.html**
  - Footer Tagging: Weisen Sie dem Container auf Zeile 765 die ID `footer-db-status-cluster` zu.
  - Header Expansion: Fügen Sie `header-btn-db-status` (Server/DB-Icon) in die System-Cluster ein.
- **[MODIFY] ui_nav_helpers.js**
  - Toggle Helper: Neue globale Funktion `toggleFooterDBStatus()` zum Ein-/Ausblenden des Clusters.
- **[MODIFY] ui_core.js**
  - Config Sync: Das Flag `enable_footer_db_status` steuert die Sichtbarkeit des Header-Buttons.

## 3. VISIBILITY STYLES (CSS)
- **[MODIFY] main.css**
  - Interaktive States: Amber Hover-, Active- und Glow-Styles für den neuen DB-Button.

---

## Verification Plan
- **Manual Verification:**
  - Toggle Test: Amber-Server-Icon toggelt den gesamten DB/Hydration-Cluster im Footer sichtbar/unsichtbar.
  - Registry Test: Backend-Flag deaktivieren → Button verschwindet aus dem Header.

---

**Review erforderlich vor Umsetzung!**
