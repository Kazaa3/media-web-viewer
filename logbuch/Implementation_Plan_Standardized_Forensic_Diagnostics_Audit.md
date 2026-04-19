# Implementation Plan: Standardized Forensic Diagnostics & Audit

This plan centralizes all verification and audit logic into a professional diagnostics API, eliminates Playwright/Selenium, and standardizes forensic screenshot capture using pyautogui.

---

## 1. Problem Statement

- Verification logic is fragmented and relies on scratch scripts.
- Playwright/Selenium are present in documentation and placeholders but are strictly forbidden for this workstation.
- Forensic screenshot capture is not standardized.

---

## 2. Proposed Changes

### Diagnostic Infrastructure
- **[NEW] `api_diagnostics.py`**
  - `verify_frontend_liveness()`: Checks if port 8345 is responsive.
  - `capture_workstation_screenshot()`: Uses pyautogui to capture a forensic UI snapshot.
  - `audit_dom_state()`: Eel-exposed bridge to check for critical DOM nodes (Hydration Audit).
  - `standardized_audit_log()`: Centralized logging for environmental and structural diagnostics.

### Core Cleanup
- **[MODIFY] `main.py`**
  - Remove all references to Playwright/Selenium in comments and dummy functions.
  - Integrate `api_diagnostics` into the specialized API registry.

### Verification Logic
- **[DELETE] `verify_frontend_liveness.py`**
  - Migrate all logic into the standardized `api_diagnostics.py` module.

---

## 3. Verification Plan

### Automated Audit
- Launch the app via `.venv/bin/python3 src/core/main.py`.
- Execute a diagnostic command to trigger pyautogui screenshot capture.
- Verify the generated audit report in `logs/audit_reports/`.

### Manual Verification
- Confirm the BOOT/DIAGNOSTICS tab reconciles the new audit metadata.

---

## 4. User Review Required

- Confirm that all Playwright/Selenium references are removed.
- Validate that the new diagnostics API meets requirements for liveness, screenshot, and DOM audit.

---

**Status:**
- Pending implementation and review.
- This plan ensures a professional, standardized, and Playwright/Selenium-free diagnostics infrastructure.
