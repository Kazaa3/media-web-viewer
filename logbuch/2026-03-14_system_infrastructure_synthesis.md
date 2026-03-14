# System Infrastructure Consolidation & Synthesis – 2026-03-14

This plan addresses the fragmented infrastructure by creating centralized documentation, fixing environment setup inconsistencies, and cleaning up legacy artifacts.

---

## User Review Required
**IMPORTANT:**
This plan involves deleting redundant root-level scripts and consolidating configuration/storage paths. This will significantly "clean" the repository root.

---

## Proposed Changes

### Documentation (Synthesis)
- **[NEW] SYSTEM_SYNTHESIS.md**: High-level architecture, config management, venv concept, reporting, build pipeline, storage/logging.
- **[NEW] 90_Build_Pipeline_Strategy_FullRelease_vs_MainPush.md**: Formal build strategy doc.
- **[NEW] requirements-run.txt**: Dedicated requirements for developer execution.

### Environment Management (Fixes)
- **[MODIFY] setup_venvs.sh**: Dot-prefixed venvs, fixed requirements paths, .venv_run/legacy venv creation.
- **[MODIFY] .gitignore**: Clean up, catch all build/test fragments, exclude legacy scripts now in infra/scripts.

### Repository Cleanup (Deep)
- **[DELETE] Legacy Metadata Fragments**: Remove redundant root scripts, obsolete build artifacts, consolidate .spec files.

### System Integration & Reporting
- **[MODIFY] build_system.py**: Benchmark outputs to build/management_reports/, performance probes in main push, global monitor_utils, auto-clean fragments.

### Fragment & Debug Level-Up
- **[MODIFY] .gitignore**: Gated Purification (whitelist only source/docs), block *.log/png/txt except in whitelisted folders, add Selenium/E2E fragments.

### Packaging Purification
- **[DELETE] Redundant Spec Files**: Only keep central MediaWebViewer.spec.
- **[DELETE] Packaging Build Residue**: Remove infra/packaging/releases/ if needed, move staging templates.
- **[MODIFY] build_system.py**: Unified spec lookup, consistent VERSION_SYNC.json path.
- **[MODIFY] VERSION_SYNC.json**: Update internal paths for new structure.

### Venv Redirection & Stability (Fixes)
- **[MODIFY] main.py/env_handler.py**: Support .venv_* naming, fix venv detection, prevent re-exec if already in venv, update validation logic.

### Configuration Centralization
- **[MODIFY] format_utils.py/main.py**: Harmonize SCAN_MEDIA_DIR/BROWSER_DEFAULT_DIR with PARSER_CONFIG, add browse_default_dir, expose API to update.

### Repository History Purification (Squash)
- **[ACTION] Git History Rewrite**: git reset --soft origin/main, new v1.34 Consolidated Release commit.

### Central Configuration Overhaul
- **[MODIFY] format_utils.py**: Ensure all categories in PARSER_CONFIG.
- **[DELETE] config.json**: Move settings to parser_config.json, frontend fetch via get_environment_info().
- **[MODIFY] main.py**: Expose consolidated config, reliable SCAN_MEDIA_DIR init.

### debug_flags Consolidation
- **[MODIFY] format_utils.py/main.py**: Add full debug_flags dict to config, load/override logic.

### Release Branch Strategy & DB Policy
- **[ACTION] Branch Hierarchy Consolidation**: Merge release/v1.34-purified into meilenstein-1-mediaplayer.
- **[ACTION] Database Policy**: Purge old DBs, verify fresh schema on launch.

---

## Release Plan Update (2026-03-14)

Ich habe den Plan für den finalen Release von v1.34 angepasst:

- **Branch-Hierarchie:** Der gereinigte Stand (release/v1.34-purified) wird lokal in meilenstein-1-mediaplayer gemergt. Das ist die Vorstufe für den PR nach main. Meilenstein 2 bleibt wie gewünscht außen vor.
- **Datenbank (DB):** Für den Release-Commit ist eine "Surgical Purge" (Löschen der lokalen database.db) vorgesehen, damit der gereinigte Stand mit einem frischen Index startet. Bitte um Zustimmung.
- **Debug-Flags:** Die ~20 einzelnen Debug-Flags (scan, parser, ui, etc.) werden direkt in die parser_config.json überführt, um sie zentral steuerbar zu machen.

Bitte schau dir den implementation_plan.md an, Sektion "Release Branch Strategy & DB Policy". Sobald du grünes Licht gibst, setze ich das um.

_Comprehensive plan for v1.34 release: consolidate DEBUG_FLAGS into parser_config.json, merge purified prerelease into M1, and execute a clean DB purge. Includes branch strategy and final diagnostic flag homogenization._

---

## Verification Plan
- **Automated:** Run infra/build_system.py --pipeline, verify debug_flags propagation.
- **Manual:** App starts with empty library, debug flags controllable via parser_config.json.

---

Comment
Ctrl+Alt+M
