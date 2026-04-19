# Implementation Plan – v1.41.123 Sub-Nav Forensic Alignment

## Ziel
Die Sub-Navigation (Queue, Playlist, Lyrics) wird auf denselben forensischen Konfigurationsstandard wie Header und Sidebar gebracht. Die horizontale Ausrichtung und Breite sind nun zentral steuerbar.

---

## Phase 1: Configuration Layer
- **[MODIFY] config_master.py**
  - Geometry Injection: Ergänze `ui_settings` um:
    - `"sub_nav_offset_left": "auto"` (Standard: flex-start, alternativ px oder %)
    - `"sub_nav_width": "100%"`

## Phase 2: UI Orchestration
- **[MODIFY] ui_core.js**
  - Dynamic CSS Variables: Aktualisiere `updateGeometry()` (und `init`), sodass folgende Variablen gesetzt werden:
    - `--sub-nav-offset-left`
    - `--sub-nav-width`
  - Sync Logic: Stelle sicher, dass diese Werte beim Start aus dem Backend geladen werden.

## Phase 3: Styling
- **[MODIFY] shell_master.css**
  - Container alignment: Passe `#sub-nav-container` an:
    - `padding-left: var(--sub-nav-offset-left, 15px);`
    - `width: var(--sub-nav-width, 100%);`

---

## Open Questions
- Sollen die Buttons standardmäßig "centered" oder "forensic left" ausgerichtet sein? **Annahme:** Default ist konfigurierbar, volle Flexibilität.

---

## Verification Plan
- **Config Test:** Setze `sub_nav_offset_left` auf 20% → "Queue"-Button rückt deutlich nach rechts.
- **Toggle Test:** Alt+N → Ganze Leiste verschwindet, Layout kollabiert nach oben.
- **Geometry Test:** Setze `sub_nav_height` auf 50 → Leiste wächst, Inhalt verschiebt sich korrekt.

---

**Review erforderlich nach Umsetzung!**
