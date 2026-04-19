# Implementation Plan – Centralized Status/Audit Control & Registry Integration (v1.41.151)

## Ziel
Die "7-POINT DOM AUDIT"-Funktion wird von einem persistenten Popup zu einem zentral gesteuerten UI-Panel migriert, das per Button im Header togglbar ist und über das Backend (config_master.py) global aktiviert/deaktiviert werden kann.

---

## 1. BACKEND REGISTRY (Python)
- **[MODIFY] config_master.py**
  - Neuer Flag: `enable_dom_auditor: True` im `ui_settings`-Dictionary für globale Feature-Flag-Steuerung.

## 2. UI ORCHESTRATION (HTML/JS)
- **[MODIFY] app.html**
  - Header Button: Neuer `header-btn-auditor`-Button in der `.secondary-cluster` (rechts oben).
  - Icon: Shield/Target-SVG für den DOM Auditor.
  - Action: `onclick="toggleDomAuditor()"`.
- **[MODIFY] dom_auditor.html**
  - Default State: Root-Container erhält `display: none;`, damit das Panel nicht automatisch beim Boot erscheint.
- **[MODIFY] ui_nav_helpers.js**
  - Toggle Logic: Neue Funktion `toggleDomAuditor()`.
  - Auto-Scan: Öffnen des Panels triggert automatisch `runDomAudit()`.
- **[MODIFY] ui_core.js**
  - Config Sync: Der neue `enable_dom_auditor`-Flag steuert die Sichtbarkeit des Header-Buttons.

## 3. VISIBILITY STYLES (CSS)
- **[MODIFY] main.css**
  - Panel Standardization: Glassmorphismus-Styles für den Auditor zentralisieren, Z-Index für konsistente Überlagerung über alle Tabs.

---

## Verification Plan
- **Manual Verification:**
  - Toggle Test: Shield-Icon im Header toggelt das Panel sichtbar/unsichtbar.
  - Registry Test: `enable_dom_auditor` auf `False` → Button verschwindet aus der UI.
  - Audit Test: "RE-SCAN" im Panel funktioniert weiterhin wie erwartet.

---

**Review erforderlich vor Umsetzung!**
