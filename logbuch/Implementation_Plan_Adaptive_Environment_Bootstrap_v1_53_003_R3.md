# Implementation Plan - Adaptive Environment Bootstrap (v1.53.003-R3)

This plan resolves the 'Wrong Venv' and 'Missing Modules' issues by implementing a two-stage environment lock: automatic venv switching and comprehensive multi-tier dependency restoration.

---

## 1. Venv-Aware Entry Point
- **[MODIFY] `main.py`**
  - Insert a "Venv Switcher" guard at the very top (Line 16).
  - If `.venv/bin/python3` exists and does not match `sys.executable`, re-execute the current process with the venv python.
  - Ensures the app always runs in the correct forensic environment.

---

## 2. Multi-Tier Dependency Audit
- **[MODIFY] `startup_auditor.py`**
  - Refactor `ensure_critical_packages` to iterate through all tiers defined in the registry.
  - Improve the restoration loop to be more resilient and vocal about failures.

---

## 3. Registry Completion (v1.53.003-R3)
- **[MODIFY] `config_master.py`**
  - Ensure the `DEPENDENCY_REGISTRY` contains all packages the user is reporting missing (including playwright, selenium, etc.).
  - Update version to v1.53.003-R3.

---

## Verification Plan

### Automated Tests
- Run `python3 src/core/main.py` from the base environment and verify it restarts itself in `.venv`.
- `python3 -m py_compile src/core/main.py src/core/startup_auditor.py`

### Manual Verification
- Observe the terminal output for the `[Bootstrap] Wrong Venv detected` message.
- Confirm that the "System Status" or logs show the correct Python path after boot.

---

**Status:**
- Pending implementation and review.
- This plan ensures robust, environment-locked bootstrapping and complete dependency restoration for all functional groups.
