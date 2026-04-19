# Implementation Plan – v1.41.100 SUPER-STABLE

This plan restores the auto-re-execution mechanism by moving the environment guard to the absolute top of the file.

---

## User Review Required
**IMPORTANT**
- **Bootstrap Fix:** My previous edit placed the psutil import before the environment check. This caused a crash because your system Python doesn't have psutil. I am moving the check to the top so it can automatically switch to your project's .venv before trying to load psutil.

---

## Proposed Changes

### Startup Engine (Bootstrap Phase)
- **[MODIFY] main.py**
  - **High-Priority Guard:** Move the `ensure_stable_environment()` call and the "Flash Burn" port kill to the absolute top of the file execution path.
  - **Import Deferral:** Ensure no non-standard libraries (like psutil, eel, bottle) are imported before the environment has been verified and switched if necessary.

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Launch Test:** Run the app with the system Python (`/home/xc/.local/bin/python3.14`).
- **Auto-Switch:** Verify it detects the missing psutil, switches to the project's .venv, and starts successfully.
