# Implementation Plan: Comprehensive Multi-Tier Dependency Registry (v1.52)

This plan expands the workstation's `DEPENDENCY_REGISTRY` into a comprehensive Single Source of Truth (SSOT), categorizing all mandatory and optional packages and establishing a registry for environment-specific metadata.

---

## 1. Problem Statement

- The current dependency registry is too limited for full-stack verification and self-healing.
- Need for logical grouping of all packages and explicit environment metadata for robust audits.

---

## 2. Proposed Changes

### Global Registry Expansion
- **[MODIFY] `config_master.py`**
  - Expand `DEPENDENCY_REGISTRY`:
    - `package_groups`:
      - `core`: `["eel", "gevent", "bottle", "psutil", "requests"]`
      - `forensic`: `["pyautogui", "pillow", "playwright", "selenium"]`
      - `media`: `["vlc", "pyvidplayer2", "m3u8"]`
      - `analytics`: `["pytest", "psutil"]`
    - `environments`:
      - `core`: `.venv`
      - `testbed`: `.venv_testbed`
      - `research`: `.venv_dev`
    - `system_requirements`:
      - `linux`: `["python3-tk", "python3-dev"]` (Informational for the auditor)

### High-Fidelity Multi-Tier Auditor
- **[MODIFY] `startup_auditor.py`**
  - Refactor `ensure_critical_packages()`:
    - Iterate through all categorized `package_groups`.
    - Implement tiered logging: `[Audit-Deps] [CORE] OK`, `[Audit-Deps] [MEDIA] MISSING`, etc.
    - Provide specific "Self-Healing" instructions or actions based on the package group.

---

## 3. Verification Plan

### Automated Registry Test
- Trigger a standalone audit and verify the new grouped logging output.
- Mock a missing "Media" package and verify the auditor correctly identifies the group failure.

### Manual Verification
- Review `config_master.py` for professional organization and SSOT integrity.
- Verify that help messages correctly mention the required Linux system packages (`tkinter/dev`).

---

## 4. User Review Required

- Confirm that all package groups and environments are correctly defined and auditable.
- Validate that the auditor provides actionable, group-specific feedback.

---

**Status:**
- Pending implementation and review.
- This plan ensures the workstation is fully auditable, self-healing, and professionally organized for all environments.
