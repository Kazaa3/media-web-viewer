<!-- Category: Tests -->
<!-- Title_DE: Dynamic Test Suite -->
<!-- Title_EN: Dynamic Test Suite -->
<!-- Summary_DE: Automatisches Finden und Ausführen von Test-Skripten im tests/ Ordner via GUI. -->
<!-- Summary_EN: Automatic discovery and execution of test scripts in the tests/ folder via GUI. -->
<!-- Status: COMPLETED -->

# Dynamic Test Suite

## Problem
Testing a complex media application requires many utility scripts to verify different parser results. Manually running these via CLI is tedious.

## Lösung
Wir haben eine dynamische Test-Suite implementiert, die:
1. Den `tests/` Ordner nach ausführbaren Python-Skripten scannt.
2. Diese in der UI auflistet.
3. Die Ausführung via Klick ermöglicht und den Output in Echtzeit in einer Konsole anzeigt.

## Integration
Die Suite nutzt `subprocess`, um die Tests isoliert auszuführen. Der Output wird captured und direkt an das Eel-Frontend gestreamt.

<!-- lang-split -->

# Dynamic Test Suite

## Problem
Testing a complex media application requires many utility scripts to verify different parser results. Manually running these via CLI is tedious.

## Solution
We implemented a dynamic test suite that:
1. Scans the `tests/` folder for executable Python scripts.
2. Lists these in the UI.
3. Enables execution via click and displays the output in real-time in a console.

## Integration
The suite uses `subprocess` to run tests in isolation. The output is captured and streamed directly to the Eel frontend.
ly in the GUI with color-coding (Green for pass, Red for fail).
- **Environment Isolation**: Tests run with the correct `PYTHONPATH` to ensure they can import project modules.

## How to use
Add any new `.py` file starting with `test_` to the `tests/` folder. It will immediately appear in the **Tests** tab of the application.
