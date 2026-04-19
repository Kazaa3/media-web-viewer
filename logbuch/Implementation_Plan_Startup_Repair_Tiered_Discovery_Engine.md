# Implementation Plan: Startup Repair & Tiered Discovery Engine

The workstation currently fails to start due to a singleton lock collision during module import. Additionally, key settings are not centralized, and binary discovery lacks container/local prioritization.

---

## User Review Required
**IMPORTANT**
- **Startup Isolation:** Top-level initialization logic in `main.py` will be moved into a protected `bootstrap` function to prevent errors when importing the module for testing or verification.
- **Tiered Discovery:** Forensic tools will now follow a strict priority: Container Standard (`/usr/bin`) → Project Local (`tools/bin`) → System Registry (`PATH`).

---

## Proposed Changes

### 1. Stabilization & Globalization
**[MODIFY]**
- `config_master.py`
  - Define `EEL_SETTINGS` with port, host, size, and default mode.
  - Implement `is_in_container()` to detect Docker environments.
  - Implement `get_binary_version(path)` to extract version strings for diagnostics.
- `main.py`
  - Move top-level assignments of port and `eel_kwargs` into a `def bootstrap_initial_state()` function.
  - Update `start_app()` to use `EEL_SETTINGS` from the centralized config.
  - Fix the logic that triggers the gevent lock error during import.
- `api_frontend.py`
  - Update `get_frontend_settings` to consume the new `EEL_SETTINGS` registry.

### 2. Tiered Binary Discovery
**[MODIFY]**
- `config_master.py`
  - Refactor `discover_binary()` to return a metadata object (path, type).
  - Tiers:
    - **Container:** `/usr/bin/{name}`
    - **Local:** `{PROJECT_ROOT}/tools/bin/{name}`
    - **System:** `shutil.which(name)`
  - Update `PROGRAM_REGISTRY` to store these metadata objects.

### 3. Forensic Inventory Expansion
**[MODIFY]**
- `api_testing.py`
  - Update `get_environment_inventory()` to return two lists:
    - `python_packages`: (Versioned pip list).
    - `forensic_binaries`: (Versioned tool list with discovery source).

---

## Verification Plan

### Automated Tests
- Run `verify_v1_46.py`: It should now succeed without a lock collision.
- Run `check_api.py`: Verify that the new `forensic_binaries` list is populated with correct paths and versions.

### Manual Verification
- Start the app normally to confirm Eel launches with the correct window size and port.
