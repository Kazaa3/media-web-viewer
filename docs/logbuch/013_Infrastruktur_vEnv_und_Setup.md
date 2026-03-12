<!-- Category: Documentation -->
<!-- Title_DE: Infrastruktur, vEnv & Setup -->
<!-- Title_EN: Infrastructure, vEnv & Setup -->
<!-- Summary_DE: Das technische Fundament von "dict": Multi-vEnv Konzept, Python 3.14 Integration und automatisierte Umgebungs-Validierung. -->
<!-- Summary_EN: The technical foundation of "dict": Multi-vEnv concept, Python 3.14 integration and automated environment validation. -->
<!-- Status: ACTIVE -->

# Infrastruktur, vEnv & Setup

## Stabilität durch Isolation
Ein Projekt der Komplexität von **dict - Web Media Player & Library** benötigt ein unerschütterliches Fundament. Um Abhängigkeits-Konflikte zu vermeiden und maximale Portabilität zu garantieren, setzen wir auf ein striktes **Multi-vEnv Konzept**.

## Das Multi-vEnv Konzept
Anstatt einer einzigen riesigen Umgebung nutzt dict spezialisierte virtuelle Umgebungen (vEnvs):
- **`venv_core`:** Enthält nur die absolut notwendigen Runtime-Abhängigkeiten (Eel, Bottle, NiceGUI).
- **`venv_dev`:** Erweitert um Developer-Tools, Linter und Dokumentations-Generatoren.
- **`venv_testbed`:** Die Spielwiese für Integrationstests mit FFmpeg, VLC und speziellen Parsern.
- **`venv_selenium`:** Eine dedizierte Umgebung für Browser-Automatisierung und E2E-Tests.
- **`venv_build`:** Isoliert für den finalen Packaging-Prozess (PyInstaller, Debian Packages).

## Python 3.14: Die Zukunft im Blick
Dict wurde frühzeitig auf **Python 3.14** vorbereitet, um von den neuesten Performance-Verbesserungen und der verbesserten Parallelität (Subinterpreters) zu profitieren. Dies ist besonders kritisch für unsere **Parser-Pipeline**, die viele Dateien gleichzeitig analysieren muss.

## Automatisierte Validierung
Um Fehlkonfigurationen beim Setup zu vermeiden, verfügt dict über eine integrierte **Umgebungs-Prüfung**:
- **Dependency-Check:** Prüft beim Start, ob alle benötigten Pakete in der korrekten Version vorhanden sind.
- **System-Tools:** Verifiziert die Verfügbarkeit von FFmpeg, VLC und MKVToolNix auf dem Host-System.
- **Write-Permissions:** Stellt sicher, dass die App in ihre Cache- und Datenbank-Verzeichnisse schreiben kann.

## Installations-Skripte
Ein zentrales `setup.sh` (oder `setup.py`) automatisiert diesen Prozess: Es erkennt das Betriebssystem, installiert System-Abhängigkeiten und baut die vEnv-Struktur rekursiv auf.

*Durch diese saubere Trennung von Code und Umgebung ist dict nicht nur für Entwickler leicht zu handhaben, sondern auch extrem robust im täglichen Betrieb.*

<!-- lang-split -->

# Infrastructure, vEnv & Setup

## Stability through Isolation
A project of the complexity of **dict - Web Media Player & Library** needs an unwavering foundation. To avoid dependency conflicts and guarantee maximum portability, we rely on a strict **multi-vEnv concept**.

## The Multi-vEnv Concept
Instead of a single huge environment, dict uses specialized virtual environments (vEnvs):
- **`venv_core`:** Contains only the absolutely necessary runtime dependencies (Eel, Bottle, NiceGUI).
- **`venv_dev`:** Expanded with developer tools, linters and documentation generators.
- **`venv_testbed`:** The playground for integration tests with FFmpeg, VLC and special parsers.
- **`venv_selenium`:** A dedicated environment for browser automation and E2E tests.
- **`venv_build`:** Isolated for the final packaging process (PyInstaller, Debian packages).

## Python 3.14: Eye on the Future
Dict was prepared for **Python 3.14** at an early stage to benefit from the latest performance improvements and improved parallelism (subinterpreters). This is particularly critical for our **parser pipeline**, which has to analyze many files at the same time.

## Automated Validation
To avoid misconfigurations during setup, dict has an integrated **environment check**:
- **Dependency Check:** Checks when starting whether all required packages are present in the correct version.
- **System Tools:** Verifies the availability of FFmpeg, VLC and MKVToolNix on the host system.
- **Write Permissions:** Ensures that the app can write to its cache and database directories.

## Installation Scripts
A central `setup.sh` (or `setup.py`) automates this process: it detects the operating system, installs system dependencies and builds the vEnv structure recursively.

*Through this clean separation of code and environment, dict is not only easy to handle for developers, but also extremely robust in daily operation.*
