# 54 — Documentation Completion v1.3.2

**Date:** 2026-03-08  
**Version:** 1.3.2  
**Status:** ✅ Completed

## Summary

This entry documents the final documentation completion for release **v1.3.2**.
The recent packaging and verification changes are now fully reflected in both the long and compact project documentation.

## Implemented

### 1) Linux Start Menu Version String

- Updated desktop entry:
  - `packaging/usr/share/applications/media-web-viewer.desktop`
- Application name now includes release version:
  - `Name=Media Web Viewer (v1.3.2)`

### 2) Version Sync Coverage Extended

- Updated `VERSION_SYNC.json` to include the Linux desktop entry check.
- Synchronization scope increased to **11 tracked locations**.
- Validation command:

```bash
python tests/test_version_sync.py
```

### 3) Reinstall Verification Test Coverage

- Existing reinstall suite was extended with:
  - strict installed-version check against `VERSION`
  - optional destructive end-to-end reinstall test
- Test file:
  - `tests/test_reinstall_deb.py`

#### Destructive test toggle

```bash
RUN_DESTRUCTIVE_TESTS=1 python tests/test_reinstall_deb.py
```

> Default behavior remains safe/non-destructive unless the environment variable is set.

### 4) Documentation Updated

#### `DOCUMENTATION.md`

Added/updated:
- Global versioning section now includes start menu version sync context
- explicit `VERSION_SYNC.json` workflow mention
- package structure clarification for `.desktop` version naming
- packaging/reinstall verification command block

#### `README.md`

Added:
- `Release Verification` section with commands for:
  - version sync checks
  - safe reinstall checks
  - optional destructive reinstall check

## Validation Results

### Version synchronization

```text
python tests/test_version_sync.py
→ PASSED (11/11 locations)
```

### Reinstall checks

```text
python tests/test_reinstall_deb.py
→ PASSED (safe mode)

RUN_DESTRUCTIVE_TESTS=1 python tests/test_reinstall_deb.py
→ PASSED (purge + reinstall verified)
```

## Outcome

Release **v1.3.2** is now documented consistently across:
- package metadata
- README
- full technical documentation
- Linux start menu entry
- automated validation and reinstall test workflows
