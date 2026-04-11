# Stall-Fix & Lifecycle Stabilization Plan (v1.35.68)

## Problem
The application is currently experiencing a "Stall" (Infinite Loop) during database initialization. This is caused by a recursive dependency between `init_db()` and `factory_reset()` when a connection error occurs, combined with hyper-aggressive logging that saturates the I/O.

### User Review Required
**WARNING**

The "stalling" you are seeing is likely a Recursion Loop in the database engine. If the database file is locked or inaccessible, the system tries to reset it, which triggers another initialization, which fails again, ad infinitum.

## Proposed Changes

### Backend Performance & Scanner (`src/core/main.py` & `src/core/db.py`)
- **db.py**
  - Muffle Insertion Logs: Change `[DB] [INSERT-SUCCESS]` from `log.info` to `log.debug` to prevent log-spam during mass indexing.
  - Connection Reuse: (Optional but recommended) Refactor `insert_media` to accept an optional `conn` to avoid open/close cycles in loops.
- **main.py**
  - Batch UI Updates: Update `_scan_media_execution` to only call `eel.append_debug_log` and `progress_update` every 5-10 items instead of every single file.
  - Throttled Scan Progress: Add a `time.time()` check in the scanning loops to ensure UI updates don't exceed 10 FPS.

### Logging & Diagnostics (`src/core/logger.py` & `web/js/trace_helpers.js`)
- **logger.py**
  - Echo Guard: Do not broadcast logs back to the UI if they originated from the UI (check for `[JS-NAV]` or `[UI-INPUT]` tags).
  - Strict Cooldown: Increase `UI_BROADCAST_COOLDOWN` if the loop persists.
- **trace_helpers.js**
  - Muffle `appendUiTrace`: Use a `DocumentFragment` or limit the number of visible log divs (e.g., max 100) to prevent DOM-freeze.
  - Throttled Tracing: Rate-limit `mwv_trace` so it doesn't fire for every single item during bulk renders.

### Startup Orchestration (`src/core/main.py`)
- **main.py**
  - Explicit Init Order: Ensure `init_db()` is called ONCE at startup by the main process, rather than being triggered by every sub-module import.

## Verification Plan

### Automated Tests
- Run the application with a read-only database file (`chmod 444 data/database.db`) and verify it logs a clean error instead of stalling.
- Run `scripts/check_backend_data.py` to verify DB sanity.

### Manual Verification
- Monitor the console for `[BD-AUDIT]` repetitions.
- Verify the UI (Player/Library) remains responsive even during large data transfers.
