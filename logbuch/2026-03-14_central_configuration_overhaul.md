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
