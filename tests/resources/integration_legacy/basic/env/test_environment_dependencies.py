# Kategorie: System / Environment
# Eingabewerte: Python-Umgebung, installierte Packages, System-Tools
# Ausgabewerte: Test-Ergebnisse (Pass/Fail/Skip), Environment-Report
# Testdateien: requirements.txt, .venv/, main.py
# Kommentar: Comprehensive test suite für Python venv, Dependencies und System-Tools Validierung

"""
Test Suite für Python-Umgebung und Dependencies

Diese Test-Suite überprüft die vollständige Python-Umgebung und alle Dependencies:

Kategorien:
- TestPythonEnvironment: Python-Version, venv-Aktivierung, Projekt-Struktur
- TestCriticalDependencies: Pflicht-Packages (eel, bottle, mutagen, pymediainfo, gevent, pytest)
- TestOptionalDependencies: Optional-Packages (python-vlc, m3u8, psutil)
- TestSystemDependencies: System-Tools (ffmpeg, mediainfo, python3-tk)
- TestRequirementsTxt: requirements.txt Konsistenz-Check
- TestBackendIntegration: main.py Import und get_environment_info() Test

Verwendung:
    pytest tests/test_environment_dependencies.py -v
    # oder direkt:
    python tests/test_environment_dependencies.py
"""

import importlib
from unittest.mock import patch
import pytest
import sys
import os
import subprocess
from pathlib import Path
import importlib.util

class TestPythonEnvironment:
    """Tests für Python-Umgebung und Version"""
    
    def test_python_version_minimum(self):
        """
        @test Prüft ob Python >= 3.11 verwendet wird
        @details Mindestversion für Media Web Viewer ist Python 3.11
        """
        version = sys.version_info
        assert version.major == 3, f"Python 3.x erforderlich, gefunden: {version.major}"
        assert version.minor >= 11, f"Python 3.11+ erforderlich, gefunden: 3.{version.minor}"
        print(f"✅ Python-Version: {version.major}.{version.minor}.{version.micro}")
    
    def test_virtual_environment_active(self):
        """
        @test Prüft ob eine virtuelle Umgebung (venv oder conda) aktiv ist
        @details Empfohlen für isolierte Dependencies
        """
        # Check for venv
        in_venv = sys.prefix != sys.base_prefix
        venv_env = os.environ.get('VIRTUAL_ENV', None)
        
        # Check for conda
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', None)
        conda_prefix = os.environ.get('CONDA_PREFIX', None)
        
        in_any_env = in_venv or venv_env or conda_env or conda_prefix
        
        # Warnung wenn keine Umgebung, aber kein Hard Fail
        if not in_any_env:
            pytest.skip("⚠️ Keine virtuelle Umgebung aktiv - Bitte venv oder conda aktivieren")
        
        # Display environment info
        if conda_env:
            print(f"✅ Conda Environment aktiv: {conda_env}")
            if conda_prefix:
                print(f"   Conda-Pfad: {conda_prefix}")
        elif in_venv:
            print(f"✅ Venv aktiv")
            print(f"   venv-Pfad: {sys.prefix}")
        elif venv_env:
            print(f"✅ Venv aktiv (via VIRTUAL_ENV)")
            print(f"   VIRTUAL_ENV: {venv_env}")
    
    def test_project_root_accessible(self):
        """
        @test Prüft ob Projekt-Root-Verzeichnis erreichbar ist
        @details Benötigt für relative Imports
        """
        project_root = Path(__file__).parents[3]
        assert project_root.exists(), "Projekt-Root nicht gefunden"
        assert (project_root / "src/core/main.py").exists(), "src/core/main.py nicht gefunden"
        print(f"✅ Projekt-Root: {project_root}")

class TestCriticalDependencies:
    """Tests für kritische Python-Dependencies"""
    
    def test_eel_installed(self):
        """@test Eel (Python-JS Bridge) muss installiert sein"""
        try:
            import eel
            print(f"✅ eel installiert: {eel.__version__ if hasattr(eel, '__version__') else 'version unknown'}")
        except ImportError as e:
            pytest.fail(f"❌ eel nicht installiert: {e}\n   Fix: pip install eel")
    
    def test_bottle_installed(self):
        """@test Bottle (Web Framework) muss installiert sein"""
        try:
            import bottle
            print(f"✅ bottle installiert: {bottle.__version__}")
        except ImportError as e:
            pytest.fail(f"❌ bottle nicht installiert: {e}\n   Fix: pip install bottle")
    
    def test_mutagen_installed(self):
        """@test Mutagen (Metadaten-Parser) muss installiert sein"""
        try:
            import mutagen
            print(f"✅ mutagen installiert: {mutagen.version_string}")
        except ImportError as e:
            pytest.fail(f"❌ mutagen nicht installiert: {e}\n   Fix: pip install mutagen")
    
    def test_pymediainfo_installed(self):
        """@test pymediainfo (Media-Info-Parser) muss installiert sein"""
        try:
            import pymediainfo
            print(f"✅ pymediainfo installiert: {pymediainfo.__version__ if hasattr(pymediainfo, '__version__') else 'ok'}")
        except ImportError as e:
            pytest.fail(f"❌ pymediainfo nicht installiert: {e}\n   Fix: pip install pymediainfo")
    
    def test_gevent_installed(self):
        """@test gevent (Async Networking) muss installiert sein"""
        try:
            import gevent
            print(f"✅ gevent installiert: {gevent.__version__}")
        except ImportError as e:
            pytest.fail(f"❌ gevent nicht installiert: {e}\n   Fix: pip install gevent")
    
    def test_pytest_installed(self):
        """@test pytest (Testing Framework) muss installiert sein"""
        try:
            import pytest as pt
            print(f"✅ pytest installiert: {pt.__version__}")
        except ImportError as e:
            pytest.fail(f"❌ pytest nicht installiert: {e}\n   Fix: pip install pytest")

class TestOptionalDependencies:
    """Tests für optionale Dependencies (Features können fehlen)"""
    
    def test_vlc_available(self):
        """@test python-vlc für VLC-Integration (optional)"""
        try:
            import vlc
            print(f"✅ python-vlc installiert")
        except ImportError:
            pytest.skip("⚠️ python-vlc nicht installiert - VLC-Features deaktiviert\n   Fix: pip install python-vlc")
    
    def test_m3u8_available(self):
        """@test m3u8 für Playlist-Import (optional)"""
        try:
            import m3u8
            print(f"✅ m3u8 installiert")
        except ImportError:
            pytest.skip("⚠️ m3u8 nicht installiert - Playlist-Import deaktiviert\n   Fix: pip install m3u8")
    
    def test_psutil_available(self):
        """@test psutil für System-Monitoring (optional)"""
        try:
            import psutil
            print(f"✅ psutil installiert: {psutil.__version__}")
        except ImportError:
            pytest.skip("⚠️ psutil nicht installiert (optional)")

class TestSystemDependencies:
    """Tests für System-Level Dependencies"""
    
    def test_ffmpeg_available(self):
        """@test FFmpeg für Audio-Transcoding"""
        try:
            result = subprocess.run(['ffmpeg', '-version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=3)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ ffmpeg installiert: {version_line}")
            else:
                pytest.fail("❌ ffmpeg nicht funktionsfähig")
        except FileNotFoundError:
            pytest.fail("❌ ffmpeg nicht gefunden\n   Fix: sudo apt install ffmpeg")
        except subprocess.TimeoutExpired:
            pytest.fail("❌ ffmpeg timeout")
    
    def test_mediainfo_available(self):
        """@test mediainfo für erweiterte Metadaten"""
        try:
            result = subprocess.run(['mediainfo', '--version'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=3)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                print(f"✅ mediainfo installiert: {version_line}")
            else:
                pytest.skip("⚠️ mediainfo nicht funktionsfähig")
        except FileNotFoundError:
            pytest.skip("⚠️ mediainfo nicht gefunden (optional)\n   Fix: sudo apt install mediainfo")
        except subprocess.TimeoutExpired:
            pytest.skip("⚠️ mediainfo timeout")
    
    def test_browser_available(self):
        """@test Webbrowser für Eel UI (Chrome/Chromium empfohlen)"""
        import shutil
        browsers = ["google-chrome-stable", "google-chrome", "chrome", "chromium-browser", "chromium", "firefox"]
        found = any(shutil.which(b) for b in browsers)
        if found:
            # Try to find which one
            for b in browsers:
                path = shutil.which(b)
                if path:
                    print(f"✅ Browser gefunden: {b} ({path})")
                    break
        else:
            pytest.fail("❌ Kein unterstützter Browser gefunden (Chrome/Chromium/Firefox erforderlich)")
    
    def test_mime_database_available(self):
        """@test shared-mime-info muss installiert sein"""
        import shutil
        if not shutil.which("update-mime-database"):
            pytest.fail("❌ update-mime-database nicht gefunden (shared-mime-info fehlt)\n   Fix: sudo apt install shared-mime-info")
        print("✅ shared-mime-info gefunden")

    def test_pixbuf_loaders_available(self):
        """@test libgdk-pixbuf2.0-0 muss installiert sein"""
        import shutil
        loader_tool = shutil.which("gdk-pixbuf-query-loaders")
        
        # Fallback for common Linux paths if not in PATH
        if not loader_tool:
            common_paths = [
                "/usr/lib/x86_64-linux-gnu/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders",
                "/usr/lib/i386-linux-gnu/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders",
                "/usr/lib/gdk-pixbuf-2.0/gdk-pixbuf-query-loaders"
            ]
            for p in common_paths:
                if os.path.exists(p):
                    loader_tool = p
                    break
                    
        if not loader_tool:
            pytest.fail("❌ gdk-pixbuf-query-loaders nicht gefunden (libgdk-pixbuf2.0-0 fehlt)\n   Fix: sudo apt install libgdk-pixbuf2.0-0")
        print(f"✅ gdk-pixbuf-query-loaders gefunden: {loader_tool}")
    
    def test_python3_tk_available(self):
        """@test python3-tk für native Datei-Dialoge"""
        try:
            import tkinter
            # Try to create a root window (will fail on headless)
            root = tkinter.Tk()
            root.withdraw()
            root.destroy()
            print(f"✅ tkinter installiert und funktionsfähig")
        except ImportError:
            pytest.skip("⚠️ tkinter nicht installiert - CLI-Picker als Fallback\n   Fix: sudo apt install python3-tk")
        except Exception as e:
            # Headless system or display issue
            pytest.skip(f"⚠️ tkinter installiert, aber nicht nutzbar (Headless?): {e}")

class TestRequirementsTxt:
    """Tests für requirements.txt Konsistenz"""
    
    def test_requirements_file_exists(self):
        """@test requirements.txt muss existieren"""
        project_root = Path(__file__).parents[3]
        requirements_file = project_root / "requirements.txt"
        assert requirements_file.exists(), "requirements.txt nicht gefunden"
        print(f"✅ requirements.txt gefunden")
    
    def test_all_requirements_installed(self):
        """@test Alle Packages aus requirements.txt müssen installiert sein"""
        project_root = Path(__file__).parents[3]
        requirements_file = project_root / "requirements.txt"
        
        if not requirements_file.exists():
            pytest.skip("requirements.txt nicht gefunden")
        
        with open(requirements_file, 'r') as f:
            lines = f.readlines()
        
        missing = []
        installed = []
        
        for line in lines:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue
            
            # Extract package name (before ==, >=, etc.)
            package_name = line.split('==')[0].split('>=')[0].split('<')[0].strip()
            
            # Special handling for some packages
            import_name = package_name
            if package_name == 'python-vlc':
                import_name = 'vlc'
            elif package_name == 'bottle-websocket':
                import_name = 'bottle_websocket'
            elif package_name == 'gevent-websocket':
                import_name = 'geventwebsocket'
            elif package_name == 'pytest-cov':
                import_name = 'pytest_cov'
            elif package_name == 'pyinstaller':
                import_name = 'PyInstaller'
            
            # Try to import
            try:
                if importlib.util.find_spec(import_name) is not None:
                    installed.append(package_name)
                else:
                    missing.append(package_name)
            except (ImportError, ModuleNotFoundError):
                missing.append(package_name)
        
        print(f"✅ Installiert: {len(installed)} Packages")
        for pkg in installed:
            print(f"   - {pkg}")
        
        if missing:
            pytest.fail(f"❌ Fehlende Packages ({len(missing)}): {', '.join(missing)}\n   Fix: pip install -r requirements.txt")

class TestBackendIntegration:
    """Tests für die Integration der Backend-Module"""

    def test_main_py_importable(self):
        """@test main.py muss importierbar sein"""
        
        with patch('src.core.env_handler.validate_safe_startup'), patch('eel.expose', side_effect=lambda x: x):
            try:
                import src.core.main as main
                importlib.reload(main) # Ensure fresh import
                print(f"✅ main.py erfolgreich importiert")
            except Exception as e:
                pytest.fail(f"❌ main.py konnte nicht importiert werden: {e}")

    def test_get_environment_info_available(self):
        """@test get_environment_info() Funktion muss existieren"""
        
        with patch('src.core.env_handler.validate_safe_startup'), patch('eel.expose', side_effect=lambda x: x):
            try:
                import src.core.main as main
                assert hasattr(main, 'get_environment_info'), "get_environment_info() nicht gefunden"
    
                # Call it and check return type
                info = main.get_environment_info()
                assert isinstance(info, dict), f"get_environment_info() muss dict zurückgeben, bekam {type(info)}"
                assert 'python_version' in info, "python_version fehlt in Rückgabe"
                assert 'in_venv' in info, "in_venv fehlt in Rückgabe"
    
                print(f"✅ get_environment_info() funktioniert")
                print(f"   Python: {info['python_version']}")
                print(f"   venv: {info['in_venv']}")
            except Exception as e:
                pytest.fail(f"❌ get_environment_info() Test fehlgeschlagen: {e}")

# Summary-Funktion für manuellen Run
def print_environment_summary():
    """Gibt eine Zusammenfassung der Umgebung aus (nicht als Test)"""
    print("\n" + "="*60)
    print("ENVIRONMENT SUMMARY")
    print("="*60)
    
    print(f"\n🐍 Python:")
    print(f"   Version: {sys.version}")
    print(f"   Executable: {sys.executable}")
    print(f"   Prefix: {sys.prefix}")
    
    venv_active = sys.prefix != sys.base_prefix
    print(f"\n📦 Virtual Environment:")
    print(f"   Aktiv: {'✅ Ja' if venv_active else '❌ Nein'}")
    if venv_active or os.environ.get('VIRTUAL_ENV'):
        print(f"   Pfad: {sys.prefix if venv_active else os.environ.get('VIRTUAL_ENV')}")
    
    print(f"\n💻 System:")
    import platform
    print(f"   Platform: {platform.platform()}")
    print(f"   System: {platform.system()} {platform.release()}")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    print_environment_summary()
    print("▶️  Starte Environment-Tests...\n")
    pytest.main([__file__, '-v', '--tb=short'])
