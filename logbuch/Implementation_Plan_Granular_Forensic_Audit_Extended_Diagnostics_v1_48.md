# Implementation Plan: Granular Forensic Audit & Extended Diagnostics (v1.48)

This plan restores and expands the workstation's diagnostic suite with a granular, phase-aware audit engine. The goal is to provide deep, stepwise visibility into the GUI lifecycle, enabling precise identification of failures during DIV hydration, DOM structure, or intermediate bridge states.

---

## 1. Problem Statement

- Previous audit logic was too coarse, only reporting up/down status.
- Loss of granular, internal diagnostic logic made crash recovery and root cause analysis difficult.
- Need for a high-density, phase-aware audit suite that can trace UI failures at every stage.

---

## 2. Proposed Changes

### Forensic Audit Expansion
- **[MODIFY] `api_audit.py`**
  - **run_granular_dom_audit()**: Verifies presence and state of core DOM nodes (`#navbar`, `#main-stage`, `#hud-controls`).
  - **trace_hydration_lifecycle()**: Multi-step audit tracing component state transitions from initialization to full rendering.
  - **extended_forensic_crash_audit()**: High-density diagnostic suite triggered during workstation failures, orchestrating all available technologies (PyAutoGUI, Selenium, Playwright).
  - **Internal Restoration**: Restore all previously removed local diagnostic logic as a baseline audit. The extended suite will be additive, not a replacement.

### Centralized Integration
- **[MODIFY] `main.py`**
  - Synchronize with the extended audit endpoints.
  - Ensure all intermediate stages (Zwischenstufen) are reported to the logs for stepwise recovery.

---

## 3. Verification Plan

### Automated "Crash Recovery" Simulation
- Trigger the Extended Audit.
- Verify the resulting report contains a step-by-step breakdown of DOM/DIV status.
- Confirm that "Black Hole" or "Empty State" conditions are explicitly detected in the logs.

### Manual Verification
- Review `logs/audit_reports/` for the new high-fidelity "Extended Audit" JSON layout.

---

## 4. Stabilizing Forensic Workstation Backend

- Unified Audit API: `api_audit.py` is the global hub for multi-tier diagnostics, synchronizing DOM auditing, logging extraction, and forensic screenshot capture.
- Modular Multi-Tier Support: PyAutoGUI, Playwright, and Selenium are all supported and decoupled from `main.py`.
- Dependency Shielding: Robust guards for bottle and eel ensure audits run even in minimal environments.
- AI-Anchored Registry: All audit settings are consolidated in `FORENSIC_AUDIT_REGISTRY` in `config_master.py`.

---

## 5. User Review Required

- Confirm that all legacy and new granular audit logic is preserved and extended, not replaced.
- Validate that intermediate diagnostic stages are visible in the logs and reports.

---

**Status:**
- Pending implementation and review.
- This plan ensures the workstation is equipped for high-frequency, granular forensic diagnostics and robust crash recovery.
