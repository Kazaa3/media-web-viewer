# 56 — Chrome App Mode & VLC Dependencies Fix

**Date:** 2026-03-08  
**Version:** 1.3.2  
**Status:** ✅ Completed

## Problem

1. **Browser Opening Issue**: Application opened as new tab in existing browser instead of standalone app window
2. **Missing VLC Dependencies**: VLC playlist support (m3u8 package) was not installed in venv

## Root Cause

### Browser Tab Issue
- Used `webbrowser.open(url)` which delegates to existing browser process
- Chrome/Chromium opens URL as new tab instead of standalone app
- No app-mode flags were passed to browser

### Missing m3u8 Package
- `m3u8>=4.1.0` listed in `requirements.txt` but not installed in `.venv`
- Environment validation detected missing package and blocked startup
- VLC playlist import/export functionality unavailable

## Solution

### 1) Chrome App Mode Implementation

File: `main.py` (lines ~1985-2015)

**Before:**
```python
browser = get_preferred_browser()
browser.open(session_url)
```

**After:**
```python
# Launch Chrome/Chromium in app mode (standalone window without browser UI)
browser_candidates = [
    'google-chrome-stable',
    'google-chrome',
    'chrome',
    'chromium-browser',
    'chromium',
]

for browser_cmd in browser_candidates:
    browser_path = shutil.which(browser_cmd)
    if browser_path:
        subprocess.Popen([
            browser_path,
            f'--app={session_url}',
            '--new-window',
            '--no-first-run',
            '--no-default-browser-check',
        ])
        break
```

**Chrome Flags:**
- `--app=URL`: App mode (no tabs, no address bar, standalone window)
- `--new-window`: Forces new window instead of reusing existing
- `--no-first-run`: Skips welcome screens
- `--no-default-browser-check`: Suppresses default browser prompts

### 2) VLC Dependencies Installation

```bash
pip install m3u8>=4.1.0
```

## Verification

### App Mode Test
```bash
python main.py
# → Opens in standalone Chrome window without browser UI
```

### VLC Support Test
```bash
python -c "import m3u8; print(m3u8.__version__)"
# → 6.0.0
```

### No-GUI Mode Test
```bash
python main.py --ng
# → Starts successfully without missing dependency errors
```

## Documentation Updates

- Updated `DOCUMENTATION.md`: Prerequisites section with m3u8 requirement
- Updated `README.md`: Core Stack section
- Created `tests/test_browser_launch.py`: Validates Chrome app mode launch logic

## Result

- Application now opens in standalone window (app mode)
- VLC playlist support fully functional
- Environment validation passes without errors
