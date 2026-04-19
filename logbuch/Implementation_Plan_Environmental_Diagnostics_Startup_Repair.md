# Implementation Plan: Environmental Diagnostics & Startup Repair

This plan expands the forensic inventory with Python environment diagnostics and resolves a critical ModuleNotFoundError during standalone launch.

---

## 1. Problem Statement

- **ModuleNotFoundError**: Standalone launch fails due to a redundant `import eel` in the core configuration module.
- **Limited Diagnostics**: The current environment inventory lacks Python environment details (venv, conda, etc.).

---

## 2. Proposed Changes

### Core Configuration
- **File:** `config_master.py`
- **Action:** Remove `import eel` to keep this module dependency-clean and compatible with lightweight path discovery.

### Diagnostic API
- **File:** `api_testing.py`
- **Action:** Expand `get_environment_inventory` to include a new `python_environment` section:
  - `executable`: `sys.executable`
  - `prefix`: `sys.prefix` (for venv detection)
  - `base_prefix`: `sys.base_prefix`
  - `is_venv`: `sys.prefix != sys.base_prefix`
  - `conda_prefix`: `os.environ.get('CONDA_PREFIX')` if present

---

## 3. Verification Plan

### Automated Tests
- Run `.venv/bin/python3 src/core/api_testing.py` to verify the local payload generation.
- Run `verify_v1_46.py` to ensure startup isolation remains intact.

### Manual Verification
- Execute `main.py` directly to confirm the `eel` import error is resolved.
- Check the BOOT/DIAGNOSTICS UI tab (once integrated) to see the new environment metadata.

---

## 4. User Review Required

- Confirm that removing the `eel` import from `config_master.py` does not impact any indirect dependencies.
- Validate that the new diagnostics payload meets requirements for venv/conda detection.

---

**Status:**
- Pending implementation and review.
- This plan ensures robust diagnostics and restores standalone compatibility.
