# Implementation Plan – v1.41.103 Tiered SSOT

This plan implements a professional tiered versioning system centralized in config_master.py.

---

## User Review Required
**IMPORTANT**
- **Versioning Tiers:** I am splitting the versioning into three distinct tiers:
  - **APP_VERSION:** The global project version.
  - **BACKEND_VERSION:** Specifically for Python core/registry logic.
  - **FRONTEND_VERSION:** Specifically for the JS/UI framework.

---

## Proposed Changes

### Configuration Core (Registry)
- **[MODIFY] config_master.py**
  - **Central Registry:** Define the three constants at the top level.
    ```python
    APP_VERSION = "1.43.00-FINAL"  # Global
    BACKEND_VERSION = "1.43.00-BE"
    FRONTEND_VERSION = "1.43.00-FE"
    ```

### Main Engine (Eel Handshake)
- **[MODIFY] main.py**
  - **Multi-Version Export:** Expose a new eel function `get_version_info()` that returns a dictionary of all three versions.
  - **Legacy Support:** Keep `get_version()` returning the primary `APP_VERSION`.

### UI Synchronization
- **[MODIFY] version.js**
  - **Full Sync:** Update the synchronization logic to fetch the full version dictionary.
  - **Trace Logs:** Log all three versions to the console during browser boot for better forensics.

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Console Check:** Open the browser console and verify all three versions (APP, BE, FE) are logged.
- **Footer Check:** Verify the main footer displays the correct `APP_VERSION`.
- **Diagnostics:** Check the diagnostics sidebar to ensure it can display the BE/FE specific versions if needed.
