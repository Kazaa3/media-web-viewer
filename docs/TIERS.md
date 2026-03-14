# Test Tiers & Classification

This document formalizes the testing strategy for the Media Web Viewer project. We use a **Tiered Testing Architecture** to balance execution speed, developer productivity, and release stability.

## 🚀 The Three Tiers

### Tier 1: Unit & Mock (Fast)
- **Goal**: Verify pure internal logic, data structures, and isolated function behavior.
- **Location**: `tests/unit/`
- **Rules**: 
  - **No** I/O (Filesystem, Network).
  - **No** external process calls (FFmpeg, MediaInfo).
  - Use `unittest.mock` to simulate dependencies.
- **Target Execution**: < 10 seconds.
- **CI Trigger**: Every commit/push.

### Tier 2: Technology & Integration (Medium)
- **Goal**: Verify interactions between the app and the Host OS environment.
- **Location**: `tests/integration/`
- **Scope**:
  - FFmpeg/MediaInfo extraction with real test assets.
  - SQLite database migrations and schema integrity.
  - Localization (i18n) key completeness.
  - Environment detection (venv/conda).
- **Target Execution**: 1 - 5 minutes.
- **CI Trigger**: Pushes to `develop`, PRs to `main`.

### Tier 3: E2E & Release Validation (Heavy)
- **Goal**: End-to-End verification of the user experience and installation health.
- **Location**: `tests/e2e/`
- **Scope**:
  - Selenium-based UI testing (Bottle + Browser interaction).
  - Debian package installation/reinstallation validation.
  - Upgrade path testing.
- **Target Execution**: 5 - 15 minutes.
- **CI Trigger**: PRs to `main`, Release Tags.

---

## 🛠️ Execution

Use the centralized build system to run specific tiers:

```bash
# Run Unit Tests
python infra/build_system.py --test unit -v

# Run Integration Tests with structured reporting
python infra/build_system.py --test integration --report

# Run All Tests
python infra/build_system.py --test all
```

## 📊 Reporting

When using the `--report` flag, structured JUnit XML reports are generated in:
`build/test-reports/report-<tier>.xml`

These reports are automatically picked up by the CI pipeline for visualization.

---

## 📝 Guidelines for New Tests

1. **Classify first**: Choose the lowest possible tier for your test. If it doesn't need FFmpeg, it's a Tier 1 test.
2. **Isolation**: Tier 1 and 2 tests should not leave side effects on the filesystem outside of `/tmp`.
3. **Re-use Assets**: Use files in `tests/assets/` instead of downloading media.
