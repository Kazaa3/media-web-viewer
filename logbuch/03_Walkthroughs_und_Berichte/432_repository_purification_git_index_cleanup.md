# Repository Purification & Git Index Cleanup

**Date:** 14. März 2026

---

## Summary
Localized the cause of repository bloat to 565 unpushed commits on the local main branch, containing obsolete packing artifacts and large screenshots. These files, though deleted in the current state, remain in the unpushed history, causing excessive repository size.

---

## Planned Solution
- Perform a `git reset --soft origin/main` to squash all 565 local commits into a single clean commit.
- Ensure only the current, purified state (source, scripts, docs) is included in the new commit.
- This will restore a minimal, clean history, free from legacy artifacts.
- Note: Individual commit messages from the 565 commits will be lost and replaced by a summary message.

---

## Progress Updates
1. Listed all tracked files to identify unwanted artifacts.
2. Identified files tracked but should be ignored per .gitignore.
3. Checked git status and tracked files for version tree bloat.
4. Searched for large files and excessive file counts.
5. Confirmed tracked screenshots.
6. Listed all branches and references for other bloat sources.
7. Analyzed git index by file extension for overlooked artifacts.
8. Evaluated git object counts and unpushed changes.
9. Investigated long-running git rm and planned cleaner history.
10. Deep search for untracked artifacts with git ls-files -o.
11. Inspected docs/ and src/ for unexpected tracked files.
12. Visualized commit history, planned squash of 565 commits.
13. Searched git history for tracked .png files.
14. Investigated malformed filenames, prepared squash plan.
15. Identified large blobs in unpushed history.
16. Updated implementation plan with squash strategy.

---

## Root Cause
The local main branch is 565 commits ahead of origin/main, with old packing residues and screenshots (up to 7MB each) still present in the unpushed history.

---

## User Approval Request
Proceed with the squash/reset? (This will lose individual commit messages but result in a single, clean commit.)

---

## Configuration Note
Centralized configuration for scan and browse paths. Synchronized main.py globals with PARSER_CONFIG from format_utils.py. Refined default media directory resolution to point to project root. Added browse default path management.

---

## Central Configuration Refinement

The repository history squash for v1.34 is complete, resulting in a single clean commit. The following steps have been taken and planned for further configuration refinement:

### Progress Updates
1. Compared `parser_config.json` with `web/config.json` to identify consolidation opportunities.
2. Updated the implementation plan with a consolidated configuration strategy.
3. Refined the implementation plan for configuration consolidation and category expansion.

### Consolidation Plan
- **Zusammenführung (Consolidation):**
  - Move settings from `web/config.json` (e.g., feature flags, log level) directly into the main configuration `parser_config.json`.
  - This creates a single source of truth for all configuration.
- **Kategorien (Categories):**
  - Enable all categories (Video, Games/Spiel, Beigabe, E-Books, etc.) by default in `indexed_categories`.
- **API-Synchronisation:**
  - `main.py` will automatically provide these central settings to the web frontend.

**User Approval Request:**
Can I proceed with this consolidation?

---

Technical plan for consolidating unpushed history into a clean v1.34 release commit and identifying further configuration refinements has been documented above.

---

# System Infrastructure Consolidation & Synthesis

This plan addresses the fragmented infrastructure by creating centralized documentation, fixing environment setup inconsistencies, and cleaning up legacy artifacts.

**User Review Required**
**IMPORTANT**

This plan involves deleting redundant root-level scripts and consolidating configuration/storage paths. This will significantly "clean" the repository root.

---

## Proposed Changes

### Documentation (Synthesis)
- **[NEW] SYSTEM_SYNTHESIS.md**: Create a high-level architectural document that explains:
  - Configuration Management: Branch-specific JSON configs (config.main.json, config.develop.json).
  - Environment Concept: Multi-venv architecture (.venv_core, .venv_dev, etc.) and requirement decoupling.
  - Reporting & Benchmarks: Consolidation of test results and performance probes.
  - Build Pipeline Strategy: Explaining the difference between "Full Release" (Tagged) and "Main Push" (CI-only).
  - Storage & Logging: Standardized paths for database, logs, and temp artifacts.
- **[NEW] 90_Build_Pipeline_Strategy_FullRelease_vs_MainPush.md**: Formalize the build strategy documentation.
- **[NEW] requirements-run.txt**: Create dedicated requirement file for developer execution.

### Environment Management (Fixes)
- **[MODIFY] setup_venvs.sh**: Update venv names to use dot prefix. Fix requirements paths to ../infra/. Add .venv_run and legacy venv creation.
- **[MODIFY] .gitignore**: Consolidate and clean up redundant patterns. Ensure all build/test fragments (.pytest_cache, selenium_artifacts/, etc.) are caught. Explicitly exclude legacy root-level scripts that are now in infra/ or scripts/.

### Repository Cleanup (Deep)
- **[DELETE] Legacy Metadata Fragments**: Remove redundant root copies of logger.py, models.py (backups moved to /tmp). Remove obsolete build artifacts (media-web-viewer_1.3.3_amd64.deb). Consolidate PyInstaller .spec files into infra/packaging/specs/.

### System Integration & Reporting
- **[MODIFY] build_system.py**: Ensure all benchmark outputs are directed to build/management_reports/. Verify performance probes are active in the main push pipeline. Advanced Monitoring: Integrate monitor_utils.py globally for all high-risk commands. Fragment Management: Auto-clean legacy .png, .log, .txt fragments during any build or clean action.

### Fragment & Debug Level-Up
- **[MODIFY] .gitignore**: Implement "Gated Purification": Explicitly allow only source/docs, block all *.log, *.png, *.txt unless in specific whitelisted folders. Add Selenium/E2E specific fragments (geckodriver.log, chromedriver.log).

### Packaging Purification
- **[DELETE] Redundant Spec Files**: Remove infra/packaging/specs/MediaWebViewer-1.3.2.spec and MediaWebViewer-1.3.3.spec. Keep only the central MediaWebViewer.spec (with dynamic versioning).
- **[DELETE] Packaging Build Residue**: Remove infra/packaging/releases/ if it contains built artifacts. Move staging templates to a more isolated structure if necessary (avoiding root-relative ambiguity).
- **[MODIFY] build_system.py**: Update spec file lookup to target the unified MediaWebViewer.spec. Ensure VERSION_SYNC.json path is consistent (moved to infra/).
- **[MODIFY] VERSION_SYNC.json**: Update internal paths to reflect the purified repository structure (centralized specs).

### Venv Redirection & Stability (Fixes)
- **[MODIFY] main.py**: Remove .resolve() from venv python paths in _ensure_project_venv_active to preserve venv context during re-exec. Update venv detection to allow any .venv_* naming (not just .venv_core). Add logic to prevent re-exec if current environment is already a valid project venv.
- **[MODIFY] env_handler.py**: Update venv_path discovery to support the new .venv_* naming convention. Ensure validation logic doesn't trigger false positives when using .venv_run.

### Configuration Centralization
- Harmonize SCAN_MEDIA_DIR and BROWSER_DEFAULT_DIR with PARSER_CONFIG.
- **[MODIFY] format_utils.py**: Update get_default_scan_dir() to point to PROJECT_ROOT/media (3 parents up). Add browse_default_dir to PARSER_CONFIG with Path.home() as default. Add save_browse_default_dir(path: str) helper.
- **[MODIFY] main.py**: Synchronize global SCAN_MEDIA_DIR with PARSER_CONFIG["scan_dirs"][0]. Synchronize global BROWSER_DEFAULT_DIR with PARSER_CONFIG["browse_default_dir"]. Expose API to update browse default directory.

### Repository History Purification (Squash)
- **[ACTION] Git History Rewrite**: Perform git reset --soft origin/main to collapse all unpushed local history (565 commits). Verify that the resulting staging area contains only the "purified" source state. Create a new, clean "v1.34 Consolidated Release" commit. This permanently removes historical "packing" artifacts and screenshots from the unpushed branch.

### Central Configuration Overhaul: Finalization & Migration Logic

The repository squash is complete and v1.34 is now consolidated in a single commit.

#### Configuration Overhaul Plan (Completed)
- **Zusammenführung (Consolidation):**
  - Moved settings from `web/config.json` (feature flags, log level) into `parser_config.json`.
  - There is now a single source of truth for configuration.
- **Kategorien (Categories):**
  - All categories (Video, Spiele/Spiel, Beigabe, E-Books, etc.) are now enabled by default in `indexed_categories`.
- **API-Synchronisation:**
  - `main.py` exposes the consolidated configuration to the frontend via the `get_environment_info` API.

#### Migration Logic Refinement
- Identified that existing configuration files on disk could override new defaults, preventing category expansion.
- Improved migration logic in `format_utils.py` to ensure all intended categories are included, even if a previous config exists.
- Deleted obsolete `web/config.json` and finalized the configuration overhaul.

#### Verification & Walkthrough Update
- Verified that all media categories are correctly activated in the system.
- Confirmed that frontend settings are now consolidated into the backend's `PARSER_CONFIG`.
- Updated the walkthrough and finalized the consolidated v1.34 release documentation.

---

**Comment**
Error while editing
