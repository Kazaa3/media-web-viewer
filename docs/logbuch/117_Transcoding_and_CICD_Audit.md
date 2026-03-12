# Logbuch 117 – Transcoding & CI/CD Audit

## Status Quo: Transcoding Tests
The audit revealed two primary transcoding tests:
1. **`test_transcoding_fixed.py`**: Validates the logic in `app_bottle.py` and `models.py`.
2. **`test_transcoding_performance_debug.py`**: Benchmarks transcoding performance and checks debug logging.

These tests are functional but are not systematically integrated into the CI/CD pipelines.

## Status Quo: CI/CD Pipelines
Current pipelines are localized to specific tasks but lack a comprehensive testing gate:
- **Backend Integration**: Limited to a parser smoke test in Docker.
- **CI Artifacts**: Builds binaries without prior testing.
- **Release**: Generates releases on tags but does not enforce a test passing requirement.

## Environment-Integration
The project defines five virtual environments (`venv_core`, `venv_dev`, `venv_testbed`, `venv_selenium`, `venv_build`).
- These are currently used for local development but are not mirrored in the GitHub Actions workflows.
- Requirements are correctly split into separate files.

## Proposed Strategy
1. **Unified Test Workflow**: Create a workflow that executes tech/basic tests in `venv_testbed`.
2. **UI Test Workflow**: Create a dedicated workflow for Selenium tests in `venv_selenium`.
3. **Release Protection**: Update `release.yml` to require successful completion of both test workflows before proceeding with the build and release steps.
