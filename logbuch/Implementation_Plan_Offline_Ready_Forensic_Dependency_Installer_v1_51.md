# Implementation Plan: Offline-Ready Forensic Dependency Installer (v1.51)

This plan upgrades the workstation's dependency management to support air-gapped and restricted environments. It introduces a local package cache fallback and a global configuration toggle for all automated installation activity.

---

## 1. Problem Statement

- Workstation must operate in environments with no or restricted internet access.
- Need for a robust, auditable fallback to local package caches.
- Centralized governance of all automated dependency installation.

---

## 2. Proposed Changes

### Global Dependency Governance
- **[MODIFY] `config_master.py`**
  - Introduce `DEPENDENCY_REGISTRY`:
    - `auto_install_enabled`: Boolean flag (global switch for all automated installs).
    - `offline_mode_enforced`: Boolean flag (skip all internet checks, force offline mode).
    - `local_cache_path`: `PROJECT_ROOT / "packages" / "packages" / "linux"`

### High-Fidelity Offline Installer
- **[MODIFY] `startup_auditor.py`**
  - Enhance `ensure_critical_packages()`:
    - **Step 0:** Check `auto_install_enabled`. If `False`, abort startup with a "Manual Action Required" notice.
    - **Step 1:** Attempt online `pip install` (unless `offline_mode_enforced` is `True`).
    - **Step 2 (Fallback):** If online fails or offline mode is enforced, trigger `pip install --no-index --find-links=local_cache_path`.
    - **Audit Trace:** Log the source of each package installation (Repository vs. Local Cache) for forensic audit readiness.

---

## 3. Verification Plan

### Automated Offline Test
- Mock a network failure (e.g., invalid pip index) and verify fallback to the local `packages/` directory.
- Toggle the global `auto_install_enabled` flag and verify the workstation respects the restriction.

### Manual Verification
- Review bootstrap logs for `[Audit-Deps] RESTORED FROM LOCAL CACHE` markers.
- Confirm no external network calls are made when `offline_mode_enforced` is active.

---

## 4. User Review Required

- Confirm that the offline fallback logic is robust and auditable.
- Validate that the global flags in `DEPENDENCY_REGISTRY` are respected by all startup and install routines.

---

**Status:**
- Pending implementation and review.
- This plan ensures the workstation is fully operational and auditable in offline and restricted environments.
