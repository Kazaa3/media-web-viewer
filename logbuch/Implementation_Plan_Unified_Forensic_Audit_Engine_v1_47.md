# Implementation Plan: Unified Forensic Audit Engine (v1.47)

This plan restores and centralizes the full technical audit suite (PyAutoGUI, Selenium, Playwright) into a specialized Audit API, eliminating technical sprawl from `main.py` and providing a single source of truth for all audit capabilities.

---

## 1. Problem Statement

- Previous removal of Playwright/Selenium limited audit flexibility.
- Audit logic was fragmented across multiple files and scripts.
- `main.py` contained technical implementation details, reducing maintainability.

---

## 2. Proposed Changes

### Configuration SSOT
- **[MODIFY] `config_master.py`**
  - Introduce `FORENSIC_AUDIT_REGISTRY`:
    - `enabled_engines`: `["pyautogui", "selenium", "playwright"]`
    - `paths`: `{ "tests": "tests/", "reports": "logs/audit_reports/" }`
    - `capabilities`: `["dom", "logging", "connectivity"]`

### Standardized Audit API
- **[MODIFY] `api_diagnostics.py`**
  - Expand to a multi-tier Unified Audit Engine:
    - `capture_screenshot(engine="pyautogui")`: Standardized screenshot bridge.
    - `run_automated_audit(engine="playwright")`: Restores Playwright UI audit logic.
    - `run_session_test(engine="selenium")`: Restores Selenium session attachment.
    - `audit_workstation_health()`: Consolidates DOM, Logging, and Connectivity.
    - **AI Anchor Comments:** Add structural metadata for future logic processing.

### main.py Decoupling
- **[MODIFY] `main.py`**
  - Finalize the removal of technical implementation details.
  - `main.py` will only act as an Eel bridge to `api_diagnostics`.

---

## 3. Verification Plan

### Automated Multi-Tier Audit
- Run `generate_standardized_audit()` via the backend.
- Verify that PyAutoGUI snapshots are captured.
- Verify that Selenium/Playwright contexts are initialized (where environment allows).

### Manual Verification
- Check `logs/audit_reports/` for the synchronized multi-tier report.

---

## 4. User Review Required

- Confirm that all three engines (PyAutoGUI, Selenium, Playwright) are available and correctly registered.
- Validate that `main.py` is fully decoupled from technical details.

---

**Status:**
- Pending implementation and review.
- This plan ensures a unified, flexible, and future-proof forensic audit infrastructure.
