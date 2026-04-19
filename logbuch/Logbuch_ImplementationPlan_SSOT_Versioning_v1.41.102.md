# Implementation Plan – v1.41.102 SSOT Versioning

This plan centralizes the application versioning in the config_master.py to provide a Single Source of Truth for the entire system.

---

## User Review Required
**IMPORTANT**
- **SSOT Strategy:** From now on, the application version will be defined exclusively in `src/core/config_master.py`. I am removing calculations or hardcoded strings from `main.py` and other modules.

---

## Proposed Changes

### Configuration Core (SSOT)
- **[MODIFY] config_master.py**
  - **Central Version:** Define `VERSION = "1.41.102-SSOT"` at the top level of the configuration module.

### Main Engine (Backend)
- **[MODIFY] main.py**
  - **Import Version:** Remove the hardcoded `VERSION` constant and instead import it from `core.config_master`.
  - **Eel Handshake:** Ensure the `get_version()` function returns the imported value.

### Logic Alignment
- **[MODIFY] ui_nav_helpers.js**
  - **Version Awareness:** Ensure any logic relying on version-based feature flags uses the centralized value received from the backend at boot.

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Startup Check:** Verify the terminal displays the new `1.41.102-SSOT` string during bootstrap.
- **UI Footer Check:** Verify the footer displays the correct version.
- **Consistency Check:** Search the entire project for any remaining `1.41.101` or `1.41.00` strings and eliminate them.
