# Logbuch-Eintrag: Build Recursion Fix & Monitoring Integration

**Datum:** 13. März 2026

**Debian Build Recursion Resolved:**
- Rsync recursion eliminated by strict out-of-tree staging (using /tmp/tmp.XXXXXX).
- Exclusion of media/ prevents package bloat.
- Staging area size check: aborts if >1.5GB.

**Robust Monitoring Pipeline:**
- Added monitor_utils.py for non-blocking process health tracking.
- Hang detection: kills process tree if no output for 5-10 min.
- "Still Alive" markers for user feedback.
- Integrated in build_system.py (--monitor flag) and manage_venvs.py (pip install).

**Verification Results:**
- Staging size reduced from 9GB+ to 177MB.
- Build steps (rsync, dpkg-deb) now fast and stable.
- Monitoring utility correctly reports process status.

**Screenshots & Recordings:**
- Visual confirmation of successful monitored DEB build.

**Tipp:**
- Für überwachte Produktion: `./.venv_build/bin/python infra/build_system.py --build deb --monitor`

---
