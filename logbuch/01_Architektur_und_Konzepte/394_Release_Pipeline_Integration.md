# 55 — Release Pipeline Integration

**Date:** 2026-03-08  
**Version:** 1.3.2  
**Status:** ✅ Completed

## Goal

Integrate a reproducible release pipeline and document it in test and logbook context.

## Implemented

### 1) Startup robustness fix

- File: `env_handler.py`
- Fixed false-negative dependency detection for `gdk-pixbuf-query-loaders`:
  - accepts known Debian library paths outside `PATH`
  - corrected apt mapping from `libgdk-pixbuf2.0-0` to `libgdk-pixbuf-2.0-0`

### 2) Debian dependency alignment

- File: `packaging/DEBIAN/control`
- Updated `Depends`:
  - added `mediainfo` (CLI required by startup validation)
  - replaced `libgdk-pixbuf2.0-0` with `libgdk-pixbuf-2.0-0`

### 3) Build pipeline command

- File: `build_system.py`
- Added CLI options:
  - `--pipeline`
  - `--destructive` (with `--pipeline`)
- Added release pipeline flow:
  1. Environment check
  2. Version sync check (`tests/test_version_sync.py`)
  3. Debian build
  4. Reinstall validation (safe)
  5. Optional destructive reinstall validation

### 4) Pipeline test suite

- Test file added: `tests/test_pipeline.py`
- This logbook entry added: `logbuch/55_Release_Pipeline_Integration.md`

## Pipeline Guide

### Purpose

The pipeline verifies that:
- version references are synchronized,
- Debian package build works,
- reinstall workflow validation passes,
- optional destructive reinstall flow works when explicitly enabled.

### Usage

**Safe pipeline (default):**

```bash
python build_system.py --pipeline
```

Steps executed:
1. Environment check
2. `python tests/test_version_sync.py`
3. Debian build (`build_deb.sh`)
4. `python tests/test_reinstall_deb.py` (safe mode)

**Destructive pipeline:**

```bash
python build_system.py --pipeline --destructive
```

Additional step:
- `RUN_DESTRUCTIVE_TESTS=1 python tests/test_reinstall_deb.py`

### Notes

- Destructive mode performs purge/reinstall via `reinstall_deb.sh`.
- Use destructive mode only on systems where replacing the current installation is intended.
- The version source of truth is `VERSION`; synchronization targets are defined in `VERSION_SYNC.json`.

## Result

The project now has a dedicated, documented release pipeline entrypoint with automated validation tests.
