# Implementation Plan – Global Config Control & Context Menu Fix (v1.41.147)

## Ziel
Verknüpfung der Haupt-UI-Features (Diagnostics HUD, Kontextmenü) mit der globalen Python-Konfiguration und finale Korrektur der Kontextmenü-Positionierung.

---

## 1. BACKEND CONFIGURATION (PYTHON)
- **[MODIFY] config_master.py**
  - Neue Flags:
    - `enable_context_menu`: Schaltet das Rechtsklick-Menü global ein/aus.
    - `enable_diagnostics_hud`: Schaltet das technische HUD im Header global ein/aus.

## 2. UI ORCHESTRATION (JS)
- **[MODIFY] ui_core.js**
  - Integration: Die `apply`-Funktion steuert Sichtbarkeit von `#header-technical-hud` und `#header-btn-diag-overlay` anhand der Backend-Flags.
- **[MODIFY] common_helpers.js**
  - Coordinate Hardening: Die Positionierung von `showContextMenu` wird mit Sanity-Check abgesichert (Fallback bei e.clientX=0 oder fehlend).
  - Config Enforcement: Das Menü wird komplett deaktiviert, wenn `enable_context_menu` in der globalen Config auf `false` steht.
  - Strict Mode: Das Kontextmenü erscheint nur bei gültigen Medienobjekten, nicht beim Rechtsklick auf den Hintergrund.

## 3. DOM CLARITY (HTML)
- **[MODIFY] app.html**
  - Default State: Das Technical HUD ist per Default `display: none`, wird nur durch die Orchestrierung sichtbar gemacht, wenn aktiviert.

---

## Verification Plan
- **Manual Verification:**
  - Python Config: Setze `enable_diagnostics_hud: False` in `config_master.py` und prüfe, ob das HUD nach Reload verschwindet.
  - Context Menu: Rechtsklick auf Medienobjekt → Menü erscheint am Cursor. Rechtsklick auf Hintergrund → kein Menü.

---

**Review erforderlich vor Umsetzung!**
