# Implementation Plan: Finalizing Phase 11 & 12 Restructuring

## Ziel
Abschluss der systematischen Umstrukturierung (Phasen 11 & 12) durch Konsolidierung der Verzeichnisstruktur und Fix des Entry Points auf src/core/main.py.

## Proposed Changes

### Directory Structure Refinement
- [MODIFY] Verschiebe Dateien von logbuch/ nach docs/logbuch/.
- [MODIFY] Verschiebe tools/ffprobe_wrapper.py nach src/parsers/ (oder src/core/).
- [MODIFY] Verschiebe ui/file_dialogs.py nach src/core/.
- [DELETE] Legacy main.py im Root (nach Verifikation).

### Core Logic: src/core/main.py
- [MODIFY] _ensure_project_venv_active zeigt auf .venv_core im Projekt-Root (zwei Ebenen über src/core/).
- [MODIFY] Alle absoluten Importe aus src.* konsistent.
- [MODIFY] Validierung der Pfad-Konstanten für web/ und data/.

## Verification Plan

### Automated Tests
- Führe non-GUI Tests mit pytest aus:
  ```bash
  pytest tests/ -m "not selenium"
  ```

### Manual Verification
- Starte die Anwendung vom neuen Entry Point:
  ```bash
  python3 src/core/main.py
  ```
- Prüfe DB-Verbindung und Verfügbarkeit der Web-Assets.

---

**Kommentar:**
- Logbuch wurde nach docs/logbuch/ verschoben (nach Refactoring).
- Ctrl+Alt+M für Logbuch-Update.


---

**Task: Finalizing Phase 11 & 12 Restructuring**
  Planning and Audit [id: 0]
  Review Phase 11 & 12 logbook entries [id: 1]
  Audit current project structure vs proposed structure [id: 2]
  Inspect src/core/main.py for path and import issues [id: 3]
  Execution: Completing the Restructuring [id: 4]
  Move remaining files to their target directories [id: 5]
  Update src/core/main.py to correctly handle the new structure [id: 6]
  Verify imports across the project [id: 7]
  Clean up redundant root-level files (e.g., old main.py) [id: 8]
  Verification [id: 9]
  Run non-GUI tests [id: 10]
  Verify app start (backend) [id: 11]
  Update logbook with success [id: 12]
