# Implementation Plan – Zen Mode Restoration & Orchestration (v1.41.154)

## Ziel
Die Zen-Mode-Funktion wird repariert, erweitert und vollständig in die zentrale MWV_UI-Orchestrierung und das Backend-Config-System integriert. Zen Mode blendet Header, Sub-Navigation und Footer aus, um maximale Medienfokussierung zu ermöglichen.

---

## 1. BACKEND REGISTRY (Python)
- **[MODIFY] config_master.py**
  - Neuer Flag: `enable_zen_mode: True` in `ui_settings` für globale Steuerung.

## 2. UI ORCHESTRATION (HTML/JS)
- **[MODIFY] ui_core.js**
  - Engine Update: Neue Methode `toggleZen()` im MWV_UI-Engine, die intern `toggleHeader()` und `toggleFooter()` triggert.
  - Config Sync: Das Flag `enable_zen_mode` steuert die Sichtbarkeit des Zen-Buttons im Header.
- **[MODIFY] ui_nav_helpers.js**
  - Logic Fix: Ersetze das alte `toggleZenMode()` durch eine Bridge zu `MWV_UI.toggleZen()`.
  - Targeting: Nutze das korrekte ID-Target `master-persistent-header` statt des alten `master-header`.
- **[MODIFY] app.html**
  - Button Mapping: Der Zen-Button im Header wird korrekt an die neue Logik gebunden und erhält das passende System-Cluster-Styling.

## 3. VISIBILITY STYLES (CSS)
- **[MODIFY] main.css**
  - States: `.active`-Styling für den Zen-Button (Moon-Icon).
  - Expansion: Das Haupt-Viewport expandiert auf 100% Höhe, wenn Zen Mode aktiv ist.

---

## Verification Plan
- **Manual Verification:**
  - Toggle Test: Moon/Expand-Icon blendet Header und Footer aus.
  - Escape Test: Zweiter Klick blendet UI wieder ein.
  - Registry Test: `enable_zen_mode` auf `False` → Button verschwindet.

---

**Review erforderlich vor Umsetzung!**
