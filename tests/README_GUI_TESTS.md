# GUI Test Suite Documentation

## Overview

This test suite provides industrial-standard end-to-end (E2E) testing for the `dict` (Media Web Viewer) application using Selenium WebDriver. It focuses on UI stability, event handling, and complex interactions like playlist reordering.

## Technical Setup

### 1. Virtual Environment (.venv_selenium)

To keep test dependencies isolated from the main application, a separate virtual environment is used.

```bash
# Create the environment
python3 -m venv .venv_selenium

# Install dependencies
.venv_selenium/bin/pip install selenium webdriver-manager
```

### 2. Wrapper Script: `run_gui_tests.py`

The script `tests/run_gui_tests.py` is the primary entry point for running the GUI test suite. It automatically:
- Detects the `.venv_selenium` environment.
- Re-executes itself using the correct Python interpreter if needed.
- Sets the `PYTHONPATH` to include the project root (enabling imports like `pages.*`).
- Runs a curated set of critical GUI tests.

**Usage:**
```bash
python3 tests/run_gui_tests.py
```

## Test Architecture

### Page Object Model (POM)
We use the POM pattern to separate element selectors and UI interactions from the test logic.
- **`tests/pages/`**: Contains page classes (e.g., `PlaylistPage`) with reusable methods.
- **`tests/test_*.py`**: Contains the actual test scenarios and assertions.

### Screenshot & Artifact Management
- **Directory**: `tests/selenium_artifacts/`
- All failed tests automatically save screenshots and DOM dumps here.
- This directory is excluded from Git via `.gitignore` to protect privacy and copyright of media content used during testing.

## Key Test Scenarios

### 1. Playlist Reordering (Hammerhart Scenario)
- **File**: `tests/test_scenario_hammerhart.py`
- **Logic**: Moves a specific song ("Hammerhart") to various positions (2nd, 5th, etc.) and verifies the order persistence.
- **Verification**: Checks both the DOM order and the backend state.

### 2. UI Integrity & Tabs
- **File**: `tests/test_ui_integrity.py`
- **Logic**: Verifies that all main tabs load correctly and critical elements (Player, Library, Options) are present.

### 3. Mouse Interaction & Picking
- **File**: `tests/test_mouse_interaction.py`
- **Logic**: Tests the "Long-Press" (Picking) functionality and ensures it's resistant to minor jitters.

## Debugging & Telemetry

The tests leverage the application's internal telemetry logs:
- **`[Startup-Trace]`**: Verifies the app starts within acceptable time limits.
- **`[Scan-Trace]`**: Monitors media database synchronization.
- **`[Parser-Trace]`**: Identifies slow parsers during GUI tests.
- **`UI Traces`**: The `appendUiTrace` function in `app.html` provides a real-time log of UI events that Selenium can capture from the console or the Debug-Tab.

## Manual Execution (Single Tests)

You can run individual tests as modules to ensure correct path resolution:
```bash
# Example: Run only the hammerhart scenario
export PYTHONPATH=$PYTHONPATH:.
.venv_selenium/bin/python3 tests/test_scenario_hammerhart.py
```
