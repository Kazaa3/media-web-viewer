# Test Classification & Project Management

## Test Classes
- **TestInstalledToolsVersion**: Validates installation and version detection for essential CLI tools and video engines.

## Test Types
- **Environment/Dependency Validation**: Ensures all required tools are present and functional.
- **Media Engine Support**: Confirms browser/video engine candidates are available for playback.

## Project Management Notes
- Keep tool lists up-to-date with new media engines and browsers.
- Document all test candidates and their CLI invocation method.
- Use parameterized tests for extensibility and maintainability.
- Integrate results into milestone documentation and environment validation reports.
- Review and refactor test classes as new requirements emerge.

## Test Reporting

Test results should be collected and summarized for each milestone. Use the following guidelines:

- Run all environment and media engine tests with `pytest tests/test_installed_tools_version.py`.
- Record which tools and engines are installed and their detected versions.
- Note any missing or failed candidates and document reasons (e.g., not installed, unsupported, version mismatch).
- Summarize results in milestone documentation and logbuch entries.
- Attach pytest output or summary tables for traceability.

Example summary table:

| Tool/Engine              | Installed | Version Detected | Notes           |
|-------------------------|-----------|------------------|-----------------|
| chromium-browser        | Yes       | 123.0.4567.89    |                 |
| chrome                  | No        |                  | Not installed   |
| google-chrome           | Yes       | 123.0.4567.89    |                 |
| firefox                 | Yes       | 98.0.2           |                 |
| firefox-developer-edition | No      |                  | Not installed   |
| vlc                     | Yes       | 3.0.16           |                 |

Update this section after each test run and milestone.

## References
- See also: docs/TEST_SUITE_SUMMARY.md
- See also: docs/Project_Markdown_File_List.md

---

This logbuch entry documents the classification and management of environment validation and media engine support tests for the Media Web Viewer project. Update this file as new tools or requirements are added.
