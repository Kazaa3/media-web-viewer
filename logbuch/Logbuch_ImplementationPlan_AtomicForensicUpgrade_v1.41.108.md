# Implementation Plan – v1.41.108 Atomic Forensic Upgrade

## Ziel
Upgrade der Atomic Shell zur „Forensic Workstation v2“ durch Integration hochdichter Monitoring-Tools und DOM-basierter State-Observability.

---

## Phase 1: High-Density Footer & Sidebar
- **[MODIFY] shell_master.html**
  - Footer Integration: Semantic <footer> mit den Swiss Army Clustern:
    - **FE Cluster:** Sync/Refresh-Tools
    - **BE Cluster:** Process/Eel-Tools
    - **DB Cluster:** Reconnect/Reset-Tools
    - **HYDR Cluster:** Mock/Real/Both-Toggles
    - **RX Cluster:** RAW/BYPS-Diagnose-Toggles
  - Sidebar Support: Struktur für das modulare Sidebar-System ergänzen

## Phase 2: DOM State Machine
- **[MODIFY] ui_nav_helpers.js**
  - Attribute Handshake: Navigationsfunktionen aktualisieren, sodass der State in den DOM gespiegelt wird:
    - `document.body.setAttribute('data-mwv-category', cat);`
    - `document.body.setAttribute('data-mwv-tab', tabId);`

## Phase 3: Design & Styling (Design System)
- **[MODIFY] shell_master.css**
  - Footer Design: High-Density-Glassmorphism-Styling für die dynamischen Cluster
  - State-Based Selectors: CSS-Regeln, die auf data-mwv-* Attribute reagieren (z.B. Hervorhebung aktiver Bereiche)

---

## Verification Plan
- **State Reflection:** Tabs wechseln und im Browser-Inspector prüfen, ob <body data-mwv-tab="..."> korrekt aktualisiert wird.
- **Tool Handshake:** Klick auf „SYNC“ oder „RECON“ im neuen Footer löst die zugehörigen JS-Funktionen aus.
- **Layout Stability:** Footer überlappt nicht mit dem Haupt-Viewport.

---

**Review erforderlich nach Umsetzung!**
