# Swiss HUD: Reactive Pulsar LEDs Plan (v1.37.16)

## 🛡️ Swiss HUD Pulsar Upgrade

- **Reactive Glow:**
  - Ambient "breathing" animations for FE, BE, and DB indicators, responsive to system activity.
- **Hover-Forensics:**
  - Real-time tooltips display the last 3 SENTINEL trace events for each module on hover.
- **Chromatic Transitions:**
  - Smooth, fluid color fades (Green ↔ Amber ↔ Red) for health state changes, replacing hard-toggle indicators.
- **Glassmorphic Polish:**
  - Footer receives refined gradients and high-density typography for a professional look.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.

---

## Proposed Changes
- main.css:
  - Implement `@keyframes pulsar-glow` for ambient LEDs.
  - Define glassmorphic styles for `.hud-led` and `.hud-pill` containers.
  - Add chromatic transition utilities for health states.
- diagnostics_helpers.js:
  - Update LED logic for transparency-controlled glows.
  - Implement Hover-Forensic bridge to feed tooltips from SENTINEL history.

---

## Open Questions
- Should the DB LED pulse faster during active SCAN or SYNC? (Recommend "Rapid Pulse" mode for background work.)
- Is the default 2s "Breathing" speed comfortable, or should it be faster for high-activity modules?

---

## Verification Plan
- Automated: Trigger health state changes and verify smooth color transitions; hover-tooltips show last 3 SENTINEL entries.
- Manual: Visual inspection of glow and responsiveness; ensure no overflow on small viewports.
