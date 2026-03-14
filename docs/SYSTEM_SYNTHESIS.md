# SYSTEM_SYNTHESIS.md

## System Infrastructure Consolidation & Synthesis (v1.34)

This document provides a high-level overview of the consolidated system architecture and infrastructure management for the Media Web Viewer project.

### 1. Configuration Management (Single Source of Truth)
- **Centralized Config**: All application settings are now consolidated in `parser_config.json`.
- **Media Categories**: Support for 10 distinct media categories (Audio, Video, Games, etc.) is deeply integrated.
- **Diagnostic Logging**: 20+ granular `debug_flags` are now managed directly via the central configuration.
- **Branch-Specific Profiles**: Reference configurations like `web/config.main.json` and `web/config.develop.json` serve as templates for different environments.

### 2. Environment Architecture (Multi-Venv Strategy)
- **Decoupled Environments**: The project uses specialized virtual environments to isolate core logic from development and testing tools:
  - `.venv_core`: Production/runtime dependencies.
  - `.venv_dev`: Development tools (formatting, documentation).
  - `.venv_run`: Lightweight execution environment for rapid testing.
- **Automated Setup**: Managed via `scripts/setup_venvs.sh` and `scripts/manage_venvs.py`.

### 3. Integrated Build & Packaging
- **Release Strategy**: 
  - **Prerelease**: `release/v1.34-purified` contains the squashed/purified source.
  - **Milestone 1**: `meilenstein-1-mediaplayer` is the staging branch for the v1.34 release.
  - **Main**: The `main` branch is protected and receives the final PR from M1.
- **Unified Packaging**: `infra/packaging/specs/MediaWebViewer.spec` provides a single point of truth for PyInstaller builds.
- **Version Synchronization**: Managed via `infra/VERSION_SYNC.json` across all source, packaging, and documentation files.

### 4. Quality Assurance & Reporting
- **Test Pipeline**: The `infra/build_system.py --pipeline` command executes 24 test gates, from unit tests to E2E Selenium flows.
- **Management Reporting**: All benchmark data, performance probes, and test results are consolidated in `build/management_reports/`.
- **Continuous Monitoring**: `scripts/monitor_utils.py` provides watchdog capabilities for long-running synchronization and scanning tasks.

### 5. Repository Purification (Git Purity)
- **Restrictive Gating**: The `.gitignore` uses a "Gated Purification" strategy (ignore-all by default) to ensure no binary residue or Selenium artifacts enter the version tree.
- **Root Discipline**: The repository root is kept clean; all infrastructure files are strictly organized in `infra/`, `scripts/`, or `docs/`.

---
*Last Updated: 2026-03-14 | Release v1.34*
