# [PLAN] Environment Forensic Audit: System Health (v1.37.29)

## Objective
Implement a professional-grade Environment (ENV) tab to provide real-time observability into backend resource usage, platform metadata, and network integrity.

---

## User Review Required
**IMPORTANT:**
- **Environmental Awareness:** This upgrade adds the "Infrastructure" layer to your forensic suite. You will have instant access to real-time resource telemetry (CPU/RAM Usage) and environmental metadata (Python/OS versions), ensuring your workstation's technical stability.

---

## Proposed Changes

### Backend (`main.py`)
- **[MODIFY]** Implement `get_system_environment()` Eel bridge.
- **Logic:**
  - Process-level Resource Usage (RAM/CPU).
  - Backend Uptime (since boot).
  - Network Status: Port 8345 Health.
  - Platforms: Python, Eel, and OS identification.

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Add ENV to the tab-switching navigation.
- Add the high-density [ENVIRONMENT FORENSICS] viewport.
- Render chromatic resource indicators (Load Meters).

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement `runEnvironmentAudit()` technical aggregator.
- Update the tab mapping to include the new domain.

---

## Open Questions
- Should we include Thread Count auditing? (Recommendation: Add it to monitor for potential resource leaks during high-velocity video transcoding).
- Should we include a "Restart Backend" trigger in the ENV tab? (Recommendation: Add as a nuclear option for full environmental restoration).

---

## Verification Plan

### Automated Tests
- Verify that `get_system_environment` correctly retrieves non-zero CPU and Memory values from the host system.
- Confirm that the UI handles "Permission Denied" errors when reading system-level metrics gracefully.

### Manual Verification
- Navigate to the ENV tab → Verify that the resource meters (CPU/RAM) are updating correctly.
- Inspect the SENTINEL trace for the environmental audit pulses.
- Compare reported CPU/RAM with system tools (top/htop) for accuracy.

---

## Implementation Checklist
- [ ] Implement get_system_environment() Eel bridge in main.py
- [ ] Add ENV tab and viewport to diagnostics_sidebar.html
- [ ] Render chromatic resource meters and metadata
- [ ] Implement runEnvironmentAudit() in sidebar_controller.js
- [ ] Integrate SENTINEL trace logging for all environment audits

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
