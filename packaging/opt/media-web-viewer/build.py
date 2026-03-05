import subprocess
import sys
import os

def build_app():
    print("Starte den Build-Prozess mit PyInstaller über Eel...")
    
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
