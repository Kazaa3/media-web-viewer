A# SYSTEM_SYNTHESIS.md

## System Infrastructure Consolidation & Synthesis

This document provides a high-level overview of the consolidated system architecture and infrastructure management for the Media Web Viewer project.

### Configuration Management
- Branch-specific JSON configs (e.g., `config.main.json`, `config.develop.json`)
- Centralized in a dedicated config directory

### Environment Concept
- Multi-venv architecture: `.venv_core`, `.venv_dev`, `.venv_run`, etc.
- Requirements decoupled by purpose (see `requirements-run.txt`)

### Reporting & Benchmarks
- All test results and performance probes consolidated in `build/management_reports/`
- Automated reporting in CI and release pipelines

### Build Pipeline Strategy
- **Full Release (Tagged):** Complete build, test, and artifact generation for production
- **Main Push (CI-only):** Fast validation, no external artifact publishing
- See also: `90_Build_Pipeline_Strategy_FullRelease_vs_MainPush.md`

### Storage & Logging
- Standardized paths for database, logs, and temp artifacts
- All logs and temp files are excluded from version control

### Fragment Management
- Strict .gitignore gating: only source, docs, and whitelisted folders allowed
- All build/test fragments and legacy artifacts are auto-cleaned during build/clean

---

For further details, see the referenced documentation and scripts in the infra/ and scripts/ directories.
A# SYSTEM_SYNTHESIS.md

## System Infrastructure Consolidation & Synthesis

This document provides a high-level overview of the consolidated system architecture and infrastructure management for the Media Web Viewer project.

### Configuration Management
- Branch-specific JSON configs (e.g., `config.main.json`, `config.develop.json`)
- Centralized in a dedicated config directory

### Environment Concept
- Multi-venv architecture: `.venv_core`, `.venv_dev`, `.venv_run`, etc.
- Requirements decoupled by purpose (see `requirements-run.txt`)

### Reporting & Benchmarks
- All test results and performance probes consolidated in `build/management_reports/`
- Automated reporting in CI and release pipelines

### Build Pipeline Strategy
- **Full Release (Tagged):** Complete build, test, and artifact generation for production
- **Main Push (CI-only):** Fast validation, no external artifact publishing
- See also: `90_Build_Pipeline_Strategy_FullRelease_vs_MainPush.md`

### Storage & Logging
- Standardized paths for database, logs, and temp artifacts
- All logs and temp files are excluded from version control

### Fragment Management
- Strict .gitignore gating: only source, docs, and whitelisted folders allowed
- All build/test fragments and legacy artifacts are auto-cleaned during build/clean

---

For further details, see the referenced documentation and scripts in the infra/ and scripts/ directories.
