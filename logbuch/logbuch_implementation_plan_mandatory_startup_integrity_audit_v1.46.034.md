# Implementation Plan: Mandatory Startup Integrity Audit (v1.46.034)

## Purpose
Implement a mandatory "Pre-Flight" integrity check during application bootstrap. This audit will proactively catch regressions (e.g., missing config keys, logic errors) before UI initialization, preventing silent startup failures and enforcing system health.

## Key Features
- **Circuit Breaker Pattern:** On critical failure (e.g., missing VLC port, invalid Library API), log a CRITICAL error and exit immediately.
- **Golden Schema Validation:** Ensure all required config keys (vlc_port, forensic_hydration_registry, port, etc.) are present.
- **Logic Symbolic Check:** Verify existence and accessibility of essential functions (e.g., api_library.get_library).
- **Integrity Reporting:** Generate a clear success/fail summary with actionable fix suggestions.

## Proposed Changes

### [Backend] [NEW] startup_auditor.py
- `ConfigAuditor`: Validates `GLOBAL_CONFIG` against the golden schema.
- `LogicAuditor`: Checks for presence of critical functions and modules.
- `IntegrityReport`: Summarizes results and suggests fixes.

### [Backend] startup_monitor.py
- Integrate `StartupAuditor.run_all()` into a new verification phase.
- Update profiler to report integrity status.

### [Backend] main.py
- Hook audit into `start_app()`:
  ```python
  from src.core.startup_auditor import run_preflight_audit
  if not run_preflight_audit():
      log.critical("[Bootstrap] INTEGRITY AUDIT FAILED. Terminating for safety.")
      sys.exit(1)
  ```

## Verification Plan
- **Automated Tests:**
  - Negative: Remove a key from `config_master.py` and verify auditor blocks startup.
  - Positive: Normal startup logs `[Audit] SUCCESS: System Integrity Verified`.
- **Manual Verification:**
  - Confirm "Audit Phase" appears in diagnostics log at startup.

## Status
- User review required before implementation.
- Ensures robust, auditable, and fail-safe startup.
