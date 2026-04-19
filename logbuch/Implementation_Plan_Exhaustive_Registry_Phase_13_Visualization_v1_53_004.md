# Implementation Plan - Exhaustive Registry & Phase 13 Visualization (v1.53.004)

This plan achieves 100% dependency parity with `infra/requirements-full.txt`, harmonizes cross-platform support for Win32 and Linux, and initiates Phase 13 with high-density diagnostic visualization.

---

## 1. Registry Harmonization (The Ultimate Stack)
- **[MODIFY] `config_master.py`**
  - **Exhaustive Group Expansion:**
    - **core:** Add `mutagen`, `pymediainfo`, `chardet`, `future`, `gevent`, `bottle`, `pycdlib`, `isoparser`, `scapy`, `eyed3`, `tinytag`, `music-tag`, `pymkv`, `pychromecast`, `zeroconf`, `pysubs2`, `pysrt`.
    - **forensic:** Add `webdriver-manager`, `xvfbwrapper`, `pytest-playwright`.
  - **System Requirements (Win32 & Linux):**
    - **linux:** `["python3-tk", "python3-dev", "ffmpeg", "libmediainfo0v5", "doxygen", "shared-mime-info", "libgdk-pixbuf2.0-0"]`
    - **win32:** `["ffmpeg.exe", "MediaInfo.dll", "vlc.exe"]`
  - Update version to v1.53.004.

---

## 2. Diagnostic Visualization (Phase 13)
- **[MODIFY] `shell_master.css`**
  - Implement `audit-pulse` animation for the sidebar.
  - Add utility classes for bitrate diagnostics (`.quality-high`, `.quality-std`, `.quality-low`).
- **[MODIFY] `app_core.js`**
  - Implement `formatBitrateLabel(bitrate)` with color-coding logic.
  - Trigger `audit-pulse` on the sidebar-lane when any Pentagon Filter mode is changed.

---

## Verification Plan

### Automated Tests
- `python3 -m py_compile src/core/config_master.py src/core/startup_auditor.py`
- Verify that the `DEPENDENCY_REGISTRY` contains all 35+ registered Python modules.

### Manual Verification
- Verify that the "Audit Pulse" glowing border triggers when toggling between ROUTE and OBJECTS.
- Verify that technical metadata for MKV files displays the correct color-coded bitrate marker (Green/Orange/Red).
- Confirm that Win32-specific system flags are correctly registered in the backend JSON data.

---

**Status:**
- Pending implementation and review.
- This plan ensures full dependency coverage, cross-platform readiness, and advanced diagnostic visualization.
