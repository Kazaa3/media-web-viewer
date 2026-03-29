# Implementation Plan: Diagnostic Infrastructure Modernization (Phase 6)

## Goal
Further harden the diagnostic framework by adding specialized suites for configuration management, media routing logic, and helper script integrity. Introduce deployment-aware flags to distinguish between basic health checks and advanced architectural audits.

---

## Proposed Changes

### [NEW] suite_config.py
- **Level 1 (Basis):** JSON schema validation for config.json and parser_config.json.
- **Level 2 (Basis):** Enforcement of "Standard Audio View" preference.
- **Level 3 (Advanced):** Profile-specific key-value audits (e.g., dev vs prod ports).
- **Level 4 (Advanced):** Environment variable override precedence.
- **Level 5 (Advanced):** Dynamic config reload handshake.

### [NEW] suite_routing.py
- **Level 1 (Basis):** mode_router.smart_route dry-run for common containers.
- **Level 2 (Basis):** Fallback logic (Direct -> Transcode -> VLC).
- **Level 3 (Advanced):** HW-accelerated route prioritization.
- **Level 4 (Advanced):** RTT/Latency-aware routing simulations.
- **Level 5 (Advanced):** Multipath stream availability (MSE vs HLS).

### [NEW] suite_scripts.py
- **Level 1 (Basis):** Directory audit for /scripts or helper binaries.
- **Level 2 (Advanced):** Execution sanity for quick-edit scripts (rename, move, hash).

### [MODIFY] suite_env.py
- Expand Level 3 to include legacy build artifact checks (.deb size, .tgz integrity).

### [MODIFY] test_base.py
- Add supported flags to filter tests by BASIS or ADVANCED tags.

### [MODIFY] app.html
- **Phase 6: Optimization & AI-Readiness**
  - Migrate all Unicode icons to centralized SVG symbol library.
  - Inject data-i18n tags into ~686 remaining raw text nodes.
  - Add high-level [AI-READINESS] structural metadata to core JS modules.

---

## Verification Plan

### Automated Tests
- Run `python3 tests/run_all.py --basis` to verify baseline health.
- Target: 0 Unicode violations, 100% I18n coverage (L1/L2).
- Final Master Diagnostic: 230+ stages green.
