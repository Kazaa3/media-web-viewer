# Reference: Selenium / GUI Screenshots

Purpose: document where automated GUI tests (Selenium / Playwright) write screenshots, how to configure the path, and how to collect/clean them for CI or local debugging.

Default locations used in this repository (convention):

- `tests/gui/screenshots/` — recommended location for per-test artifacts (each test writes a subfolder or timestamped files).
- `screenshots/` — legacy project-wide screenshots folder (already excluded in `.gitignore`).
- `Screens/` — historical folder (excluded in `.gitignore`).

How to configure your test runner:

- Selenium tests: set the path in your test fixture or driver helper, e.g.:

```python
SCREENSHOT_DIR = Path("tests/gui/screenshots")
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
driver.save_screenshot(str(SCREENSHOT_DIR / "test_name.png"))
```

- Playwright: use `page.screenshot(path=...)` with the same directory above.

CI recommendations:

- Use `ENABLE_XVFB=1` for headless runs and collect `tests/gui/screenshots/` as an artifact on failure.
- Keep per-run subfolders (timestamp or CI_JOB_ID) to avoid collisions.

Housekeeping:

- `.gitignore` already contains `Screens/` and `screenshots/`. If you want `tests/gui/screenshots/` ignored as well, add that explicit entry to `.gitignore` (optional).
- To clear local screenshots quickly:

```bash
rm -rf tests/gui/screenshots/*
```

If you want, I can also add `tests/gui/screenshots/` to `.gitignore` now — tell me to proceed or provide a different path to ignore.
