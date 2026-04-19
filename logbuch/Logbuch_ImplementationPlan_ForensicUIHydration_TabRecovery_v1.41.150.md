# Implementation Plan – Forensic UI Hydration & Tab Recovery (v1.41.150)

## Ziel
Behebung des "Black Screen"-Problems durch vollständige Synchronisierung der WindowManager-Registrierungen mit den tatsächlichen DOM-IDs und Sicherstellung der Sichtbarkeit aller Content-Fragmente.

---

## 1. DOM SYNCHRONIZATION (HTML)
- **[MODIFY] app.html**
  - ID Standardization:
    - `coverflow-library-panel` → `library-panel-container`
    - `indexed-sqlite-media-repository-panel` → `inventory-panel-container`
    - `metadata-writer-crud-panel` → `edit-panel-container`
  - Domain Tagging: Füge jedem `.tab-content`-Div ein `data-tab-domain="..."` hinzu, um die Forensic-Fallback-Logik des WindowManagers zu unterstützen.

## 2. REGISTRY ALIGNMENT (JS)
- **[MODIFY] app_core.js**
  - WM Registry Rebuild: Alle `WM.register`-Aufrufe werden auf die neuen, standardisierten IDs in `app.html` angepasst.
  - Fragment Path Parity: Jeder registrierte Window-Eintrag erhält einen gültigen `fragmentPath` zur passenden .html-Fragmentdatei.

## 3. VISIBILITY ENFORCEMENT (CSS)
- **[MODIFY] main.css**
  - Active State Overrides: `.tab-content.active` erhält `display: flex !important;` und `background: var(--bg-primary);`, um "Black Hole"-Effekte durch fehlerhafte Vererbung zu verhindern.

---

## Verification Plan
- **Manual Verification:**
  - Tab Stress Test: Alle Header-Tabs (Player, Library, Database, Edit, Tools) nacheinander anklicken.
  - DOM Check: Beim Tab-Wechsel erhält der entsprechende `#*-panel-container` die Klasse `active` und den Style `display: flex`.
  - Hydration Audit: Im "7-POINT DOM AUDIT"-Overlay prüfen, ob alle Fragmente erfolgreich geladen werden.

---

**Review erforderlich vor Umsetzung!**
