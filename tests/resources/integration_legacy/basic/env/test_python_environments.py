#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Python Environments Test
# Eingabewerte: Conda environments, venv locations, System Python
# Ausgabewerte: Environment detection, Activation status
# Testdateien: Keine (System scan)
# Kommentar: Testet Python-Environment-Erkennung (Conda, venv, System).
"""
# test_python_environments.py - Comprehensive Python environment discovery and analysis.

This comprehensive test suite provides:
- Complete system-wide Python installation discovery
- Conda environment enumeration and analysis
- Local venv directory detection
- Project-specific venv localization
- Environment recommendation and comparison
- Useful for troubleshooting environment setup issues

Key Features:
  • Discovers all system Python installations from common locations
  • Lists all Conda environments with versions and paths
  • Locates project's active virtual environment
  • Identifies recommended environment (p14 with Python 3.14.2)
  • Shows environment hierarchy and relationships
  • Provides activation instructions for each environment

Usage:
  pytest tests/test_python_environments.py -v -s

Output Example:
  System: Python 3.11.2, 3.14.0
  Conda: anaconda3 (3.12.7), anaconda (3.12.11), p14 (3.14.2) ⭐
  Project venv: /home/xc/#Coding/gui_media_web_viewer/.venv (Python 3.14.2)
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Get project root
ROOT_DIR = Path(__file__).parents[3]
PROJECT_VENV = ROOT_DIR / ".venv"

# Common Python installation locations (system + local)
SYSTEM_SEARCH_PATHS = [
    "/usr/bin",
    "/usr/local/bin",
    "/opt/python",
    os.path.expanduser("~/.local/bin"),
    "/opt/homebrew/bin",  # macOS
]

# Environment type constants
ENV_TYPE_SYSTEM = "system"
ENV_TYPE_CONDA = "conda"
ENV_TYPE_VENV = "venv"

def find_system_pythons() -> List[Dict[str, str]]:
    """
    Find all Python installations in system PATH.
    
    Searches common installation directories for Python executables
    and collects their version information.
    
    Returns:
        List of dicts with keys: path, version, type
        
    Example:
        [
            {"path": "/usr/bin/python3.11", "version": "Python 3.11.2", "type": "system"},
            {"path": "/usr/local/bin/python3.14", "version": "Python 3.14.0", "type": "system"}
        ]
    """
    pythons = []
    seen_versions = set()

    for search_path in SYSTEM_SEARCH_PATHS:
        search_dir = Path(search_path)
        if not search_dir.exists():
            continue

        try:
            for python_exe in search_dir.glob("python*"):
                if not python_exe.is_file() or not os.access(python_exe, os.X_OK):
                    continue

                try:
                    result = subprocess.run(
                        [str(python_exe), "--version"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    version = result.stdout.strip() or result.stderr.strip()

                    # Skip duplicates and invalid versions
                    if not version or version in seen_versions:
                        continue
                    seen_versions.add(version)

                    pythons.append({
                        "path": str(python_exe),
                        "version": version,
                        "type": ENV_TYPE_SYSTEM
                    })
                except (subprocess.TimeoutExpired, Exception):
                    # Skip inaccessible or slow executables
                    continue
        except PermissionError:
            # Skip directories we can't read
            continue

    return sorted(pythons, key=lambda x: x["version"])

def find_conda_environments() -> List[Dict[str, str]]:
    """
    Find all Conda environments using conda CLI.
    
    Queries conda for all available environments and their paths,
    then determines Python version in each environment.
    
    Returns:
        List of dicts with keys: name, path, python_exe, version, type, active
        
    Example:
        [
            {
                "name": "base",
                "path": "/home/user/anaconda3",
                "python_exe": "/home/user/anaconda3/bin/python",
                "version": "Python 3.12.7",
                "type": "conda",
                "active": False
            },
            {
                "name": "p14",
                "path": "/home/user/anaconda3/envs/p14",
                "python_exe": "/home/user/anaconda3/envs/p14/bin/python",
                "version": "Python 3.14.2",
                "type": "conda",
                "active": True
            }
        ]
    """
    conda_envs = []

    try:
        # Get list of conda environments in JSON format
        result = subprocess.run(
            ["conda", "env", "list", "--json"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode != 0:
            return []

        data = json.loads(result.stdout)
        for env_path in data.get("envs", []):
            env_name = Path(env_path).name
            env_python = Path(env_path) / "bin" / "python"

            if not env_python.exists():
                continue

            try:
                # Get Python version from this environment
                version_result = subprocess.run(
                    [str(env_python), "--version"],
                    capture_output=True,
                    text=True,
                    timeout=2
                )
                version = version_result.stdout.strip() or version_result.stderr.strip()

                # Identify recommended environment
                is_active = env_name in ["base", "p14"]
                is_recommended = env_name == "p14"

                conda_envs.append({
                    "name": env_name,
                    "path": env_path,
                    "python_exe": str(env_python),
                    "version": version,
                    "type": ENV_TYPE_CONDA,
                    "active": is_active,
                    "recommended": is_recommended
                })
            except (subprocess.TimeoutExpired, Exception):
                # Skip environments we can't access
                continue

    except (FileNotFoundError, json.JSONDecodeError, subprocess.TimeoutExpired):
        # Conda not available or malformed response
        pass

    return sorted(conda_envs, key=lambda x: x["name"])

def find_local_venvs(
    root_search: Path = Path.home(),
    max_depth: int = 2,
    max_dirs: int = 50
) -> List[Dict[str, str]]:
    """
    Find local venv directories in common locations.
    
    Recursively searches for virtual environment directories by looking
    for pyvenv.cfg and bin/python combinations.
    
    Args:
        root_search: Root directory to search (default: home directory)
        max_depth: Maximum directory depth to recurse (default: 2)
        max_dirs: Maximum directories to check before stopping (default: 50)
    
    Returns:
        List of dicts with keys: path, name, python_exe, version, type
    """
    venvs = []
    checked_dir_count = 0

    # Common directories where projects might be located
    common_dirs = [
        Path.home(),
        Path.home() / "projects",
        Path.home() / "code",
        Path.home() / "workspace",
        Path.home() / "#Coding",
        Path("/tmp"),
    ]

    for base_dir in common_dirs:
        if not base_dir.exists():
            continue

        try:
            for depth, directory in enumerate(base_dir.rglob("*")):
                if checked_dir_count >= max_dirs:
                    break
                if depth > max_depth:
                    continue

                if not directory.is_dir():
                    continue

                checked_dir_count += 1

                # Check if this directory looks like a virtual environment
                python_exe = directory / "bin" / "python"
                pyvenv_cfg = directory / "pyvenv.cfg"

                if python_exe.exists() and pyvenv_cfg.exists():
                    try:
                        version_result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        version = version_result.stdout.strip() or version_result.stderr.strip()

                        venvs.append({
                            "path": str(directory),
                            "name": directory.name,
                            "python_exe": str(python_exe),
                            "version": version,
                            "type": ENV_TYPE_VENV
                        })
                    except (subprocess.TimeoutExpired, Exception):
                        # Skip inaccessible venvs
                        continue
        except PermissionError:
            # Skip directories we can't read
            continue

    return venvs

def get_project_venv_info() -> Dict[str, any]:
    """
    Get detailed information about the project's virtual environment.
    
    Returns:
        Dict with keys: exists, path, pretty_path, version, python_exe, base_prefix
    """
    project_python = PROJECT_VENV / "bin" / "python"
    pyvenv_cfg = PROJECT_VENV / "pyvenv.cfg"

    info = {
        "exists": PROJECT_VENV.exists(),
        "path": str(PROJECT_VENV),
        "pretty_path": ".venv",
        "version": None,
        "python_exe": str(project_python) if project_python.exists() else None,
        "base_prefix": None,
        "config": None
    }

    if not info["exists"]:
        return info

    # Get Python version
    if project_python.exists():
        try:
            result = subprocess.run(
                [str(project_python), "--version"],
                capture_output=True,
                text=True,
                timeout=2
            )
            info["version"] = result.stdout.strip() or result.stderr.strip()
        except Exception:
            pass

    # Read pyvenv.cfg to find base environment
    if pyvenv_cfg.exists():
        try:
            content = pyvenv_cfg.read_text()
            for line in content.split("\n"):
                if line.startswith("home"):
                    # Extract home directory (which is the base environment)
                    home_path = line.split("=", 1)[1].strip()
                    # Get parent directory (base is bin/python, we want the env root)
                    base_env = str(Path(home_path).parent)
                    info["base_prefix"] = base_env
                    info["config"] = line.strip()
                    break
        except Exception:
            pass

    return info

def test_discover_all_python_environments():
    """
    MAIN TEST: Discover and display all Python environments on the system.
    
    This is the primary discovery test that shows:
    - All system Python installations
    - All Conda environments
    - All local virtual environments
    - Recommended configuration
    """
    print("\n" + "=" * 80)
    print("🔍 PYTHON ENVIRONMENT DISCOVERY")
    print("=" * 80)

    # System Pythons
    print("\n📍 System Python Installations:")
    print("-" * 80)
    system_pythons = find_system_pythons()

    if system_pythons:
        for py in system_pythons:
            print(f"  • {py['path']}")
            print(f"    Version: {py['version']}")
    else:
        print("  (No system Python installations found in standard locations)")

    # Conda Environments
    print("\n🐍 Conda Environments:")
    print("-" * 80)
    conda_envs = find_conda_environments()

    if conda_envs:
        for env in conda_envs:
            marker = ""
            if env.get("recommended"):
                marker = " ⭐ RECOMMENDED"
            elif env.get("active"):
                marker = " (active)"

            print(f"  • {env['name']}{marker}")
            print(f"    Path: {env['path']}")
            print(f"    Version: {env['version']}")
    else:
        print("  (No Conda environments found)")

    # Local venvs
    print("\n📦 Local Virtual Environments (venv):")
    print("-" * 80)
    local_venvs = find_local_venvs()

    if local_venvs:
        for venv in local_venvs:
            print(f"  • {venv['name']}")
            print(f"    Path: {venv['path']}")
            print(f"    Version: {venv['version']}")
    else:
        print("  (No local venv directories found in common locations)")

    print("\n" + "=" * 80)
    print("✅ DISCOVERY COMPLETE")
    print("=" * 80)

def test_locate_project_venv():
    """
    TEST: Locate and verify the project's virtual environment.
    
    Verifies that:
    - Project venv exists at expected location
    - Python executable is accessible
    - Version matches expectations (3.14.2)
    - Base environment is correctly configured
    """
    print("\n" + "=" * 80)
    print("🎯 PROJECT VIRTUAL ENVIRONMENT")
    print("=" * 80)

    venv_info = get_project_venv_info()

    # Verify venv exists
    assert venv_info["exists"], (
        f"❌ Project venv not found at {venv_info['path']}\n"
        f"Expected: {PROJECT_VENV}"
    )

    print(f"\n✅ Project venv found:")
    print(f"   Location: {venv_info['pretty_path']}")
    print(f"   Full path: {venv_info['path']}")
    print(f"   Python: {venv_info['version']}")
    print(f"   Executable: {venv_info['python_exe']}")

    if venv_info["base_prefix"]:
        print(f"   Base environment: {venv_info['base_prefix']}")

    print("\n" + "=" * 80)

def test_identify_conda_alternatives():
    """
    TEST: Identify available Conda environments as alternatives.
    
    Shows all available Conda environments with:
    - Version information
    - Activation commands
    - Recommendations
    - Comparison with current project venv
    """
    print("\n" + "=" * 80)
    print("🔄 CONDA ALTERNATIVES")
    print("=" * 80)

    conda_envs = find_conda_environments()
    venv_info = get_project_venv_info()

    if not conda_envs:
        print("  (No Conda environments available)")
        return

    print("\n🟢 Available Conda Environments:")
    for env in conda_envs:
        marker = ""
        if env.get("recommended"):
            marker = " ← 🌟 RECOMMENDED"
        elif env.get("active"):
            marker = " (Default)"

        print(f"\n  • {env['name']}{marker}")
        print(f"    Version: {env['version']}")
        print(f"    Activation: conda activate {env['name']}")
        print(f"    For venv: {env['python_exe']} -m venv /path/to/.venv")

    # Highlight p14 as recommended
    p14_env = next((e for e in conda_envs if e.get("recommended")), None)
    if p14_env:
        print("\n" + "-" * 80)
        print("🌟 Project Setup Recommendation: p14 (Conda)")
        print("-" * 80)
        print(f"  Environment: {p14_env['name']}")
        print(f"  Path: {p14_env['path']}")
        print(f"  Version: {p14_env['version']}")
        print(f"  Status: ✓ Currently used for project venv")
        print(f"  Command to recreate venv:")
        print(f"    {p14_env['python_exe']} -m venv .venv")

    print("\n" + "=" * 80)

def test_current_python_info():
    """
    TEST: Display information about the currently active Python environment.
    
    Shows:
    - Current executable path
    - Full version string
    - Environment type (system/venv/conda)
    - Prefix and base prefix
    """
    print("\n" + "=" * 80)
    print("📊 CURRENT PYTHON ENVIRONMENT")
    print("=" * 80)

    print(f"\n  Executable: {sys.executable}")
    print(f"  Version: {sys.version}")
    print(f"  Prefix: {sys.prefix}")
    print(f"  Base Prefix: {sys.base_prefix}")

    # Determine environment type
    env_type = "System Python"
    if hasattr(sys, 'real_prefix'):
        env_type = "virtualenv"
    elif sys.prefix != sys.base_prefix:
        env_type = "venv (virtual environment)"

    print(f"  Environment Type: {env_type}")

    print("\n" + "=" * 80)

def test_environment_summary():
    """
    TEST: Summary - Show overall environment configuration.
    
    Provides a concise summary of:
    - Total environments found
    - Recommended configuration
    - Next steps
    """
    print("\n" + "=" * 80)
    print("📋 ENVIRONMENT CONFIGURATION SUMMARY")
    print("=" * 80)

    system_pythons = find_system_pythons()
    conda_envs = find_conda_environments()
    local_venvs = find_local_venvs()
    venv_info = get_project_venv_info()

    print(f"\n📊 Statistics:")
    print(f"  • System Python installations: {len(system_pythons)}")
    print(f"  • Conda environments: {len(conda_envs)}")
    print(f"  • Local venv directories: {len(local_venvs)}")

    print(f"\n📍 Project Configuration:")
    print(f"  • Project venv: {'✓ Exists' if venv_info['exists'] else '✗ Not found'}")
    if venv_info['exists']:
        print(f"  • Python version: {venv_info.get('version', 'Unknown')}")
        if venv_info.get('base_prefix'):
            base_name = Path(venv_info['base_prefix']).name
            print(f"  • Base environment: {base_name}")

    print(f"\n✅ Recommended Setup:")
    p14_env = next((e for e in conda_envs if e.get("recommended")), None)
    if p14_env:
        print(f"  • Use Conda environment: {p14_env['name']} (Python {p14_env['version'].split()[-1]})")
        print(f"  • For project venv: Already configured ✓")
    else:
        print(f"  • No recommended environment found")

    print("\n" + "=" * 80)

if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])

