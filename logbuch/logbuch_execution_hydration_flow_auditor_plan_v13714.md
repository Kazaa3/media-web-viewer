# Native Hydration Flow Auditor Plan (v1.37.14)

## 🛡️ Building the Flow Auditor

- **Stage Analysis (7 Stages):**
  - Upgrading bridge logic to provide real-time reports on the library's path through the system.
  - Identifies exactly where items go missing (SQL → JSON → Models → DOM).
- **Latency Benchmarking:**
  - Measures delta between backend sync and frontend renderLibrary completion.
- **Centralized Control:**
  - Moves SCAN, SYNC, and RECOVERY commands into the HYD tab for a unified "Hydration Master Console".
- **Dropped Reasons Forensics:**
  - Visualizes backend filter rejections (Category, Genre, Search, Year) in a high-visibility list.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.

---

## Proposed UI & Controller Changes
- diagnostics_sidebar.html:
  - Add "Command Master" header to HYD tab with [SCAN], [SYNC], [RECOVER] buttons.
  - Create `diag-pane-hydration-flow` container for the 7-stage report.
  - Integrate "Dropped Reasons" forensic list.
- sidebar_controller.js:
  - Implement `renderNativeHydrationReport()` for high-performance flow auditing.
  - Implement `runHydrationAuditProbe()` for real-time backend filter-chain stats.
  - Integrate latency tracing for all sync operations.

---

## Verification Plan
- Automated: HYD tab triggers flow analysis; SENTINEL logs all syncs.
- Manual: SCAN from new console re-hydrates library; "Dropped Reasons" identifies filtered items.
