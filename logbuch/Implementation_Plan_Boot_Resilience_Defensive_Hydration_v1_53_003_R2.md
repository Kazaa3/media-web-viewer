# Implementation Plan - Boot Resilience & Defensive Hydration (v1.53.003-R2)

This plan addresses the persistent `ModuleNotFoundError` for pyautogui by implementing a defensive "Mock Fallback" strategy, ensuring that a missing dependency in a non-critical module does not block the entire application boot sequence.

---

## 1. Defensive Module Loading
- **[MODIFY] `api_diagnostics.py`**
  - Wrap `import pyautogui` in a `try/except ImportError` block.
  - Use `MagicMock` as a fallback to prevent secondary `NameError` failures in exposed functions.
  - Log a high-visibility warning if the fallback is active, indicating pyautogui-based forensic features are disabled until resolved.

---

## 2. Auditor Verbosity
- **[MODIFY] `startup_auditor.py`**
  - Update `_restore_packages` to log the actual exception if `pip install` fails.
  - Provide transparency on why the auto-install is failing (e.g., Network, Permissions, or PEP 668 nuances).
  - On Linux, if pyautogui install fails, log a warning recommending installation of system dependencies (e.g., `python3-tk`).

---

## 3. Versioning
- Standardize all components to v1.53.003-R2.

---

## Verification Plan

### Automated Tests
- `python3 src/core/main.py` (Verify the app starts even if pyautogui is uninstalled)
- `python3 -m py_compile src/core/api_diagnostics.py`

### Manual Verification
- Manually uninstall pyautogui (`pip uninstall pyautogui`).
- Run the app.
- Verify the "Live Logs" or "Diagnostics" tab shows a "Mock / Disabled" status for pyautogui instead of crashing the process.

---

**Status:**
- Pending implementation and review.
- This plan ensures robust bootstrapping and graceful degradation of non-critical forensic features.
