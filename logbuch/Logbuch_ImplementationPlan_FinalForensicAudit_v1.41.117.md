# Implementation Plan – v1.41.117 Final Forensic Audit

## Ziel
Abschluss der Rekonstruktion des Media Viewers durch Synchronisierung der CSS-Geometrie, Korrektur von Positionsüberlappungen und Härtung der UI-State-Persistenz.

---

## Phase 1: CSS Geometry Synchronization
- **[MODIFY] web/css/main.css**
  - Variable Sync: Setze `--active-header-height` auf 48px.
  - Sub-Nav Variable: Definiere `--active-sub-nav-height` als 35px für aktive Zustände.

## Phase 2: Structural Positioning Refinement
- **[MODIFY] app.html**
  - Relative Layout: Passe das `top`-Property von `#sub-nav-container` an, sodass es eine Variable oder Berechnung nutzt (statt hartkodiert 40px).

## Phase 3: Navigation State Hardening
- **[MODIFY] web/js/ui_nav_helpers.js**
  - Storage Update: Aktualisiere `switchPlayerView()`, sodass der aktive SubTab in `localStorage` gespeichert wird.
  - Logic Sync: Sorge dafür, dass `updateGlobalSubNav()` den zuletzt gespeicherten State korrekt liest.

---

## Verification Plan
- **Geometry Check:** Sub-Nav-Pills sind klar unter dem Haupt-Header sichtbar, ohne Überlappung.
- **Persistence Check:** Nach Wechsel zu "Lyrics", dann "Library", dann zurück zu "Media" bleibt "Lyrics" aktiv und sichtbar.
- **Responsive Check:** Layout passt sich korrekt an, wenn Sidebars umgeschaltet werden.

---

**Review erforderlich nach Umsetzung!**
