# Media Viewer v1.35.96 — Zero-Item Bug Resolution & SSOT Finalization

This plan resolves the persistent discrepancy between the backend database (541 items) and the GUI (0-9 items) by standardizing all path resolution and migrating remaining hardcoded parameters to the GLOBAL_CONFIG Single Source of Truth (SSOT).

## User Review Required

**IMPORTANT**

- **Database Path Standardization:** Enforce absolute path resolution for the database in both CLI and Eel environments. If items still don't show, a new "Diagnostic Audit" tab will be provided in the UI to display exactly which file the app is opening.

**TIP**

- **Category Sync:** Implement an automatic migration in the startup sequence to ensure all database categories are lowercase (e.g., 'Audio' → 'audio'), preventing filtering mismatches in `_apply_library_filters`.

## Proposed Changes

### [Component] Config Master (SSOT Extension)
- **[MODIFY] config_master.py**
    - Expand `storage_registry` with:
        - `log_dir`: `PROJECT_ROOT / "data" / "logbuch"`
        - `benchmark_path`: `PROJECT_ROOT / "data" / "benchmarks.json"`
        - `test_results_path`: `PROJECT_ROOT / "data" / "test_results.json"`
        - `mkv_cache_dir`: `PROJECT_ROOT / "cache" / "extracted"`
    - Expand `perf_settings` with `task_timeout: 900`.
    - Expand `test_settings` with `pytest_cmd: ["pytest", "-q"]`.

### [Component] Application Logic & Diagnostics
- **[MODIFY] main.py**
    - Refactor Hardcoded Paths: Replace all instances of `PROJECT_ROOT / "..."` for Logbuch, Benchmarks, and Tests with the new `GLOBAL_CONFIG` references.
    - Implement `get_deep_audit()`: A new Eel-exposed function returning:
        - Actual absolute `PROJECT_ROOT`.
        - Resolved `DB_PATH` and existence status.
        - Raw DB counts vs. Filtered GUI counts.
        - Category distribution in the active DB.
    - Fix `_apply_library_filters`: Ensure it consistently handles the 'Audio' vs 'audio' case sensitivity.
    - MKV Batch Extract: Use `GLOBAL_CONFIG["storage_registry"]["mkv_cache_dir"]`.

- **[MODIFY] db.py**
    - Wrap `get_db_stats` in a more robust error handler.
    - Ensure `DB_FILENAME` is always converted to an absolute path before connecting.

### [Component] Database Migration
- **[MODIFY] db.py**
    - Update `init_db()` migration to lowercase ALL existing categories in the media table to prevent filtering drops.

## Open Questions
- Should the logbuch remain in the root or move to the `data/` subfolder? (Plan currently moves it to `data/logbuch` for better portability).

## Verification Plan

### Automated Tests
- `python3 scripts/check_db_path.py`: A new scratch script to verify that the Eel process and CLI see the exact same absolute database path.

### Manual Verification
- Launch with `bash run.sh --debug`.
- Verify the status bar `[DB: X | GUI: X]` matches the actual database count.
- Check the new "Logbuch" and "Benchmarks" tabs to ensure they still load data from the new centralized paths.
