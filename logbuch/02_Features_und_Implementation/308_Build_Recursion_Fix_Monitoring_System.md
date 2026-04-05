# Logbuch 54: Build Recursion Fix & Monitoring System (v1.34)

## Context
Version 1.34 focuses on build infrastructure stability. A persistent recursion issue in `build_deb.sh` caused build hangs and excessive disk usage.

## Build Recursion Fix
- Moved to **out-of-tree staging**: Source is copied to a temporary directory before packaging.
- Refined `rsync` exclusions: Explicitly excluded `media/`, `.venv*/`, and `infra/packaging/` to break recursion loops.
- Added size-guard: Aborts build if staging exceeds 1.5GB.

## Robust Monitoring (Watchdog)
- Implemented `monitor_utils.py`: A non-blocking process supervisor.
- Integrated into `BuildSystem` and `manage_venvs.py`.
- Features: Hang detection (no output timeout), "Still Alive" markers, and safe process tree termination.

## Environment Management
- Support for specific Python versions (e.g., Python 3.14 for `.venv_core`).
- Integrated version mismatch detection in `manage_venvs.py --status`.

## Results
Full automation of the DEB and EXE build process with safety valves and real-time feedback.
