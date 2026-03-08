#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Environment Check Script

Schnelle Überprüfung der Python-Umgebung und Dependencies
ohne pytest zu benötigen.

Usage:
    python check_environment.py
    # oder
    ./check_environment.py
"""

import sys
import os
import subprocess
from pathlib import Path


def print_header(text):
    """Formatierte Header-Ausgabe"""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")


def check_python_version():
    """Prüft Python-Version"""
    print("\n🐍 Python Version Check:")
    version = sys.version_info
    print(f"   Version: {version.major}.{version.minor}.{version.micro}")
    print(f"   Executable: {sys.executable}")
    
    if version.major != 3 or version.minor < 11:
        print(f"   ❌ FEHLER: Python 3.11+ erforderlich!")
        return False
    else:
        print(f"   ✅ OK")
        return True


def check_venv():
    """Prüft Virtual Environment (venv oder conda)"""
    print("\n📦 Virtual Environment Check:")
    
    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    # Check for conda
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    
    in_any_env = in_venv or venv_env or conda_env or conda_prefix
    
    if in_any_env:
        if conda_env:
            print(f"   Status: ✅ Aktiv (Conda)")
            print(f"   Conda Environment: {conda_env}")
            if conda_prefix:
                print(f"   Pfad: {conda_prefix}")
        elif in_venv:
            print(f"   Status: ✅ Aktiv (Venv)")
            print(f"   Pfad: {sys.prefix}")
        elif venv_env:
            print(f"   Status: ✅ Aktiv (Venv via VIRTUAL_ENV)")
            print(f"   Pfad: {venv_env}")
        return True
    else:
        print(f"   Status: ❌ NICHT AKTIV")
        print(f"   ⚠️  WARNUNG: Du solltest venv oder conda aktivieren:")
        print(f"      cd {Path(__file__).parent}")
        print(f"      source .venv/bin/activate  # für venv")
        print(f"      conda activate <env-name>  # für conda")
        return False


def check_package(package_name, import_name=None):
    """Prüft ob ein Package installiert ist"""
    if import_name is None:
        import_name = package_name
    
    try:
        import importlib
        module = importlib.import_module(import_name)
        version = getattr(module, '__version__', None) or \
                 getattr(module, 'version_string', None) or \
                 getattr(module, 'VERSION', 'unknown')
        return True, str(version)
    except ImportError:
        return False, None


def check_dependencies():
    """Prüft alle wichtigen Dependencies"""
    print("\n📚 Python Dependencies Check:")
    
    critical_packages = [
        ('eel', 'eel'),
        ('bottle', 'bottle'),
        ('mutagen', 'mutagen'),
        ('pymediainfo', 'pymediainfo'),
        ('gevent', 'gevent'),
    ]
    
    optional_packages = [
        ('python-vlc', 'vlc'),
        ('m3u8', 'm3u8'),
        ('pytest', 'pytest'),
    ]
    
    all_ok = True
    
    print("\n   Kritische Packages:")
    for package, import_name in critical_packages:
        installed, version = check_package(package, import_name)
        if installed:
            print(f"   ✅ {package:20s} {version}")
        else:
            print(f"   ❌ {package:20s} FEHLT")
            all_ok = False
    
    print("\n   Optionale Packages:")
    for package, import_name in optional_packages:
        installed, version = check_package(package, import_name)
        if installed:
            print(f"   ✅ {package:20s} {version}")
        else:
            print(f"   ⚠️  {package:20s} nicht installiert")
    
    if not all_ok:
        print(f"\n   ❌ FEHLER: Kritische Packages fehlen!")
        print(f"      Fix: pip install -r requirements.txt")
    
    return all_ok


def check_system_tools():
    """Prüft System-Tools"""
    print("\n🔧 System Tools Check:")
    
    tools = [
        ('ffmpeg', ['ffmpeg', '-version']),
        ('mediainfo', ['mediainfo', '--version']),
        ('chrome/browser', None),
    ]
    
    for tool_name, command in tools:
        try:
            if command is None:
                raise FileNotFoundError
            result = subprocess.run(command, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=3)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0][:60]
                print(f"   ✅ {tool_name:15s} {version_line}")
            else:
                print(f"   ❌ {tool_name:15s} nicht funktionsfähig")
        except FileNotFoundError:
            if tool_name == 'chrome/browser':
                # Special check for browsers
                import shutil
                browsers = ["google-chrome-stable", "google-chrome", "chrome", "chromium-browser", "chromium", "firefox"]
                found = False
                for b in browsers:
                    path = shutil.which(b)
                    if path:
                        print(f"   ✅ {'browser':15s} gefunden: {b}")
                        found = True
                        break
                if not found:
                    print(f"   ❌ {'browser':15s} NICHT GEFUNDEN")
                    print(f"      Fix: sudo apt install google-chrome-stable")
            else:
                print(f"   ❌ {tool_name:15s} NICHT GEFUNDEN")
                if tool_name == 'ffmpeg':
                    print(f"      Fix: sudo apt install ffmpeg")
        except subprocess.TimeoutExpired:
            print(f"   ❌ {tool_name:15s} timeout")
    
    # Check tkinter (GUI)
    try:
        import tkinter
        print(f"   ✅ {'tkinter':15s} (für GUI-Dialoge)")
    except ImportError:
        print(f"   ⚠️  {'tkinter':15s} nicht installiert (optional)")
        print(f"      Info: CLI-Picker als Fallback verfügbar")


def check_main_py():
    """Prüft ob main.py importierbar ist"""
    print("\n🎯 Backend Import Check:")
    
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root))
    
    try:
        import main
        print(f"   ✅ main.py erfolgreich importiert")
        
        # Check specific function
        if hasattr(main, 'get_environment_info'):
            info = main.get_environment_info()
            print(f"   ✅ get_environment_info() verfügbar")
            print(f"      Python: {info['python_version']}")
            print(f"      venv: {'✅ Ja' if info['in_venv'] else '❌ Nein'}")
        
        return True
    except Exception as e:
        print(f"   ❌ FEHLER beim Import: {e}")
        return False


def print_summary(checks_passed):
    """Ausgabe der Zusammenfassung"""
    print_header("ZUSAMMENFASSUNG")
    
    if all(checks_passed.values()):
        print("\n✅ Alle Checks bestanden!")
        print("   Du kannst die App starten mit:")
        print("   $ python main.py")
    else:
        print("\n❌ Einige Checks fehlgeschlagen:")
        for check, passed in checks_passed.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check}")
        
        print("\n📋 Empfohlene Schritte:")
        if not checks_passed['venv']:
            print("   1. Aktiviere das venv:")
            print("      $ source .venv/bin/activate")
        if not checks_passed['dependencies']:
            print("   2. Installiere Dependencies:")
            print("      $ pip install -r requirements.txt")
        if not checks_passed['python_version']:
            print("   3. Upgrade Python auf 3.11+")


def main():
    """Hauptfunktion"""
    print_header("Media Web Viewer - Environment Check")
    
    checks_passed = {
        'python_version': check_python_version(),
        'venv': check_venv(),
        'dependencies': check_dependencies(),
    }
    
    check_system_tools()
    
    checks_passed['main_py'] = check_main_py()
    
    print_summary(checks_passed)
    
    # Exit code
    exit_code = 0 if all(checks_passed.values()) else 1
    print(f"\n{'='*60}\n")
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
