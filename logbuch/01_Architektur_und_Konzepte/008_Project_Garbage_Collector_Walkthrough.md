#dict - Desktop Media Player and Library Manager v1.34

## Project Garbage Collector - Walkthrough & Features

Dieses Dokument beschreibt das Skript `scripts/project_garbage_collector.py` zur automatisierten Wartung und Bloat-Prävention im Media Web Viewer Workspace.

---

### Features

**1. Unified Cleanup**
- Python Caches: `__pycache__`, `.pyc`, etc.
- Tool Artifacts: `.pytest_cache`, `.mypy_cache`, `.ruff_cache`, `.coverage`.
- Project Bloat: `media/.cache`, `logs/`.
- Git Maintenance: Entfernt `tmp_pack`-Dateien und optional `git gc`.

**2. Enhanced Feedback**
- Progress Bar: Zeigt den aktuellen Cleanup-Status.
- Git Context: Zeigt, wie viele Commits der aktuelle Branch vor `main` liegt.
- Heartbeat Indicator: Spinner für langlaufende `git gc`-Operationen.
- Dry-Run Mode: Standardmäßig sicher, echte Löschung nur mit `--force`.

---

### Demonstration

**Status Check:**
```bash
python3 scripts/project_garbage_collector.py --status
```

**Full Cleanup:**
```bash
python3 scripts/project_garbage_collector.py --force --git-gc
```

---

### Accomplishments
- Standardisierte Dual-Header-Struktur.
- Optimierte Scan-Logik mit `os.walk`.
- Reduzierung der `.git`-Verzeichnisgröße.
- Robuste Interrupt-Handling (`KeyboardInterrupt`).

---

**Kommentar:**
Das Skript ist effizient, sicher und ideal für die kontinuierliche Pflege des Entwicklungs-Workspaces.

*Letzte Aktualisierung: 13. März 2026*
