# Dynamic Test Suite

## Overview
To improve development speed and reliability, we implemented a dynamic test suite in the GUI.

## Features
- **Auto-Discovery**: The system scans the `tests/` directory for any `test_*.py` files.
- **Granular Control**: Selection of individual test suites via checkboxes.
- **Real-time Feedback**: Pytest output is captured and displayed directly in the GUI with color-coding (Green for pass, Red for fail).
- **Environment Isolation**: Tests run with the correct `PYTHONPATH` to ensure they can import project modules.

## How to use
Add any new `.py` file starting with `test_` to the `tests/` folder. It will immediately appear in the **Tests** tab of the application.
