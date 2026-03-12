# Media Web Viewer - Style Guide & Standards

This document establishes the technical standards and best practices for the Media Web Viewer project. Adherence to these rules is mandatory to ensure code consistency, prevent regressions, and maintain a high-quality test suite.

## 1. Python Syntax & Coding Standards

### Avoid Syntax Bloat & Regression
- **Parentheses Management**: Always verify that multi-line statements (especially `assert`, `subprocess.run`, and `re.search`) are properly closed.
  - *Bad*: `assert condition, (`
  - *Good*: `assert condition, (f"Error: {detail}")`
- **Linting**: Run `flake8` or a similar linter before committing to catch unclosed strings or parentheses.

### Assertions in Tests
- Use descriptive error messages in all `assert` statements.
- Group multiple related assertions into logical blocks with comments.

## 2. Test Classification & Reporting

Tests MUST be grouped according to their focus and complexity:

- `tests/tech/`: Technology-specific tests (FFmpeg, VLC, Mutagen, Scapy).
- `tests/basic/`: Core functionality, smoke tests, and fast validation.
- `tests/advanced/`: Integration, E2E, and performance scenarios.
- `tests/category/`: Organized by media type (Audio, Video, Playlist, UI).
- `tests/iso/`: Long-running tests for disk images (DVD/Blu-ray).

### Test Artifacts
- All logs, screenshots, and temporary fragments must be stored in `tests/artifacts/`.
- Never use hardcoded absolute paths to personal directories (e.g., `/home/username/`). Use `Path(__file__)` or established project constants.

## 3. Privacy & Copyright (Non-Public Assets)

### User Data & Environment
- **Anonymization**: Never hardcode personal linux usernames (`xc`), file paths, or IP addresses in tests.
- **Dynamic Probes**: Use environment variables or dynamic discovery for sensitive paths.

### Media Assets
- **Copyright**: Do not include copyrighted media (covers, albums, videos) in the repository.
- **Mocks**: Use binary-zeroed dummies or metadata-only mocks for testing.
- **Reference Images**: GUI comparison screenshots must be stored in `tests/reference_screenshots/` (local only, ignored by Git).

## 4. Repository Hygiene (.gitignore)

The following items MUST NOT be pushed to the public repository:
- `*.log`: Application and test logs.
- `*.json` (fragments): Temporary result files (e.g., `m4b_all_tools_results.json`).
- `database/`: Local SQLite databases.
- `media/.cache/`: Transcoder and thumbnail caches.
- `screenshots/` & `*.png`: UI capture fragments.

## 5. Web Frontend Standards

- **i18n**: All UI strings must be localized via `web/i18n.json`.
- **Kebab-Case**: Use kebab-case for HTML IDs (`my-button-id`).
- **Trace Logging**: Use `appendUiTrace()` for diagnostic feedback in the Debug tab.
