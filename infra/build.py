import subprocess
import sys
import os


BUILD_TEST_GATE = [
    "tests/test_performance_probes.py",
    "tests/test_bottle_health_latency.py",
    "tests/test_installed_packages_ui.py",
    "tests/test_environment_packages_fallback.py",
    "tests/test_ui_session_stability.py",
]

GUI_TEST_GATE = [
    "tests/test_mouse_interaction.py",
    "tests/test_scenario_hammerhart.py",
    "tests/test_ui_integrity.py",
]


def run_build_test_gate() -> None:
    print("Führe Build-Test-Gate aus...")
    cmd = [sys.executable, "-m", "pytest", "-q", *BUILD_TEST_GATE]
    subprocess.run(cmd, check=True)
    print("✅ Build-Test-Gate bestanden")


def build_app():
    print("Starte den Build-Prozess mit PyInstaller über Eel...")

    skip_gate = str(os.environ.get("SKIP_BUILD_TESTS", "0")).strip() == "1"
    run_gui = str(os.environ.get("RUN_GUI_TESTS", "0")).strip() == "1"

    if skip_gate:
        print("⚠️ Build-Test-Gate übersprungen (SKIP_BUILD_TESTS=1)")
    else:
        run_build_test_gate()

    if run_gui:
        print("🧪 Führe GUI-Test-Gate aus...")
        try:
            cmd = [sys.executable, "-m", "pytest", "-q", *GUI_TEST_GATE]
            subprocess.run(cmd, check=True)
            print("✅ GUI-Test-Gate bestanden")
        except subprocess.CalledProcessError:
            print("❌ GUI-Tests fehlgeschlagen. Build abgebrochen.")
            sys.exit(1)

    # Der Befehl, um Eel mit Pyinstaller zusammenzufassen
    # --onefile: Alles in eine einzige ausführbare Datei packen
    # --noconsole: Blendet das Terminal-Fenster aus (nur wichtig für Windows)
    # web/: Der Ordner, den Eel miteinbinden muss
    command = [
        sys.executable, "-m", "eel", "main.py", "web",
        "--onefile", "--noconsole", "--clean",
        "--name", "MediaWebViewer"
    ]

    try:
        subprocess.run(command, check=True)
        print("\n✅ Build erfolgreich!")
        print("Die ausführbare Datei befindet sich nun im 'dist/'-Ordner.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Fehler beim Build: {e}")


if __name__ == "__main__":
    build_app()
