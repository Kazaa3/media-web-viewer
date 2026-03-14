# System Infrastructure Consolidation & Synthesis

**Date:** 14. März 2026  
**Author:** [Your Name/Team]  
**Status:** User Review Required

---

## Overview

This initiative addresses repository fragmentation by centralizing documentation, standardizing environment setup, and purging legacy artifacts. The plan will significantly clean the repository root and harmonize configuration, build, and environment management.

---

## Key Actions

### Documentation (Synthesis)
- **[NEW] SYSTEM_SYNTHESIS.md:**  
  High-level architecture, config management, multi-venv concept, reporting, build pipeline, storage/logging.
- **[NEW] 90_Build_Pipeline_Strategy_FullRelease_vs_MainPush.md:**  
  Formal build strategy documentation.
- **[NEW] requirements-run.txt:**  
  Dedicated requirements for developer execution.

### Environment Management (Fixes)
- **[MODIFY] setup_venvs.sh:**  
  - Use dot-prefixed venv names  
  - Fix requirements paths  
  - Add `.venv_run` and legacy `venv` creation
- **[MODIFY] .gitignore:**  
  - Clean redundant patterns  
  - Exclude legacy scripts now in infra/scripts

### Repository Cleanup (Deep)
- **[DELETE] Legacy Metadata:**  
  - Remove redundant root-level logger.py, models.py  
  - Remove obsolete build artifacts  
  - Consolidate PyInstaller specs

### System Integration & Reporting
- **[MODIFY] build_system.py:**  
  - Direct benchmarks to build/management_reports  
  - Ensure probes active in main push  
  - Integrate monitor_utils.py  
  - Auto-clean legacy fragments during build/clean

### Fragment & Debug Level-Up
- **[MODIFY] .gitignore:**  
  - Gated Purification: allow only source/docs, block logs/png/txt except whitelisted  
  - Add Selenium/E2E fragments

### Packaging Purification
- **[DELETE] Redundant Spec Files:**  
  - Keep only central MediaWebViewer.spec  
- **[DELETE] Packaging Build Residue:**  
  - Remove infra/packaging/releases if artifacts present  
  - Move staging templates to isolated structure
- **[MODIFY] build_system.py:**  
  - Update spec lookup to unified spec  
  - Ensure VERSION_SYNC.json path is infra/
- **[MODIFY] VERSION_SYNC.json:**  
  - Update internal paths

### Venv Redirection & Stability (Fixes)
- **[MODIFY] main.py:**  
  - Remove .resolve() from venv paths  
  - Allow any .venv_* naming  
  - Prevent re-exec if already in valid venv
- **[MODIFY] env_handler.py:**  
  - Support new venv naming  
  - Validate .venv_run correctly

### Configuration Centralization
- Harmonize SCAN_MEDIA_DIR and BROWSER_DEFAULT_DIR with PARSER_CONFIG.
- **[MODIFY] format_utils.py:**  
  - Update scan dir logic  
  - Add browse_default_dir to config  
  - Add save_browse_default_dir helper
- **[MODIFY] main.py:**  
  - Sync global dirs with config  
  - Expose API to update browse dir

### UI Reordering & Venv Promotion
- **[MODIFY] app.html:**  
  - Move "Local Virtual Environments" above "requirements.txt Status"  
  - Add info about setup_venvs.sh
- **[MODIFY] i18n.json:**  
  - Update keys for environment setup and section titles

---

## 5. Configuration Centralization & UI Refinement

- **Centralized Paths:** Synchronized `SCAN_MEDIA_DIR` and `BROWSER_DEFAULT_DIR` with `PARSER_CONFIG`, ensuring consistent media discovery across the backend.
- **Dynamic UI Pathing:** Implemented dynamic path injection in `app.html` to display the actual `default_scan_dir` instead of hardcoded strings.
- **UI Architecture Prioritization:**
  - Reordered the "Options" tab to place "Local Virtual Environments" at the top (Priority 1).
  - Added a prominent project guidance section for the `scripts/setup_venvs.sh` script.
  - Demoted the environment-specific "Requirements Status" below the global project infrastructure overview to reduce confusion.

---

## Verification Plan

- Run `infra/build_system.py --pipeline` (automated)
- Run `bash scripts/setup_venvs.sh` and verify venvs
- Check docs/SYSTEM_SYNTHESIS.md for completeness
- Ensure root folder is clean (`git status`)
- Verify UI changes in environment tab

---

## Verification Results

- **Configuration Sync:** Verified that `main.py` correctly pulls paths from `PARSER_CONFIG`.
- **UI Layout:** Confirmed that the "Local Virtual Environments" section is now prominently displayed.
- **i18n:** Verified that both German and English translations for the new sections are correctly implemented.

---

**Comment:**  
This plan will streamline development, reduce confusion, and improve maintainability. User review and feedback are required before proceeding with deletions and major restructuring.

## Release-Status v1.34 (14.03.2026)

- Archivierung v1.33: Der bisherige Stand von main (386418d) ist nun sicher unter dem Tag v1.33 archiviert.
- Tagging v1.34: Der aktuelle, gereinigte Stand auf meilenstein-1-mediaplayer wurde als v1.34 getaggt und gepusht.
- M1 Synchronisation: Ergänzungen in docs/SYSTEM_SYNTHESIS.md committed und auf den Remote-Branch meilenstein-1-mediaplayer gepusht.
- Push nach main: GitHub-Schutz blockiert Force-Push, aber meilenstein-1-mediaplayer ist bereit für den PR und Merge auf GitHub.
- Kontext: Weiterarbeit erfolgt auf meilenstein-1-mediaplayer.
- Repo-Purity und Dokumentation sind vollständig, v1.34 Release ist abgeschlossen und bereit für den Merge.

## Finalisierung: M1-Merge und Release-Check (v1.34)

- Die Repo-Purity ist hergestellt, die Dokumentation ist aktuell und der v1.34 Release-Stammbaum ist sauber dokumentiert.
- Der finale Merge von meilenstein-1-mediaplayer (M1) nach main erfolgt per Pull Request auf GitHub.
- Die lokale main wurde bereits auf den v1.34 purified state gebracht.
- Alle requirements sind in infra/ korrekt gelistet.
- setup_venvs.sh und die venv-Struktur wurden final geprüft.
- Das Repository ist 100% frei von visuellen Altlasten (Screenshots, Artefakte) und bereit für den Release.
- Nächster Schritt: PR auf GitHub abschließen und v1.34 als neuen Main-Branch etablieren.