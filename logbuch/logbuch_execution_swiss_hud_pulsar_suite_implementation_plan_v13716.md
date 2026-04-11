# Swiss HUD: Reactive Pulsar LEDs Implementation Plan (v1.37.16)

## 🛡️ Building Reactive Pulsar LEDs

- **Ambient Pulse Styling:**
  - Implement high-performance @keyframes and glassmorphic styling for the .hud-led elements in main.css.
- **Hover-Forensics Bridge:**
  - Modify the sentinelPulse engine to maintain module-specific mini-buffers (FE, BE, DB) so footer tooltips display the last 3 forensic events in real-time.
- **Chromatic Transitions:**
  - Implement smooth CSS transitions for health states (Green ↔ Amber ↔ Red) to ensure a premium technical aesthetic.
- **Active Sync Pulse:**
  - Verify where background tasks like library scans trigger a specialized "Scanning" pulse state for the indicators.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.

---

## Approval
Do you approve this Swiss HUD Pulsar upgrade? (Continue / "weiter")
