#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_python_environments.py - Discovers and lists all Python environments on the system.

This test:
- Finds all system-wide Python installations
- Lists all Conda environments
- Locates local venv directories
- Identifies the project's active venv
- Shows p14 as Conda alternative environment
"""

import sys
import os
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Tuple


# Get project root
ROOT_DIR = Path(__file__).parent.parent
PROJECT_VENV = ROOT_DIR / ".venv"


def find_system_pythons() -> List[Dict[str, str]]:
    """Find all Python installations in system PATH."""
    pythons = []
    seen_versions = set()

    # Common locations to search
    search_paths = [
        "/usr/bin",
        "/usr/local/bin",
        "/opt/python",
        os.path.expanduser("~/.local/bin"),
    ]

    for search_path in search_paths:
        search_dir = Path(search_path)
        if not search_dir.exists():
            continue

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

                # Skip duplicates
                if version in seen_versions:
                    continue
                seen_versions.add(version)

                pythons.append({
                    "path": str(python_exe),
                    "version": version,
                    "type": "system"
                })
            except Exception:
                continue

    return pythons


def find_conda_environments() -> List[Dict[str, str]]:
    """Find all Conda environments using conda env list."""
    conda_envs = []

    try:
        result = subprocess.run(
            ["conda", "env", "list", "--json"],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            data = json.loads(result.stdout)
            for env_path in data.get("envs", []):
                env_name = Path(env_path).name
                env_python = Path(env_path) / "bin" / "python"

                if env_python.exists():
                    try:
                        version_result = subprocess.run(
                            [str(env_python), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=2
                        )
                        version = version_result.stdout.strip() or version_result.stderr.strip()

                        is_active = "base" in env_name or "p14" in env_name
                        conda_envs.append({
                            "name": env_name,
                            "path": env_path,
                            "python_exe": str(env_python),
                            "version": version,
                            "type": "conda",
                            "active": is_active
                        })
                    except Exception:
                        pass
    except Exception:
        pass

    return conda_envs


def find_local_venvs(root_search: Path = Path.home(), max_depth: int = 2) -> List[Dict[str, str]]:
    """Find local venv directories in common locations."""
    venvs = []
    checked_dir_count = 0
    max_dirs = 50  # Limit search to avoid long runtime

    # Common directories to check
    common_dirs = [
        Path.home(),
        Path.home() / "projects",
        Path.home() / "code",
        Path.home() / "workspace",
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

                # Check if this looks like a venv
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
                            "type": "venv"
                        })
                    except Exception:
                        pass
        except Exception:
            continue

    return venvs


def test_discover_all_python_environments():
    """Test: Discover and display all Python environments on the system."""
    print("\n" + "=" * 80)
    print("🔍 PYTHON ENVIRONMENT DISCOVERY")
    print("=" * 80)

    # Find system pythons
    print("\n📍 System Python Installations:")
    print("-" * 80)
    system_pythons = find_system_pythons()

    if system_pythons:
        for py in system_pythons:
            print(f"  • {py['path']}")
            print(f"    Version: {py['version']}")
    else:
        print("  (No additional system Python installations found)")

    # Find Conda environments
    print("\n🐍 Conda Environments:")
    print("-" * 80)
    conda_envs = find_conda_environments()

    if conda_envs:
        for env in conda_envs:
            marker = "✓ ACTIVE" if env.get("active") else ""
            print(f"  • {env['name']} {marker}")
            print(f"    Path: {env['path']}")
            print(f"    Version: {env['version']}")
            print(f"    Executable: {env['python_exe']}")
    else:
        print("  (No Conda environments found)")

    # Find local venvs
    print("\n📦 Local Virtual Environments (venv):")
    print("-" * 80)
    local_venvs = find_local_venvs()

    if local_venvs:
        for venv in local_venvs:
            print(f"  • {venv['name']}")
            print(f"    Path: {venv['path']}")
            print(f"    Version: {venv['version']}")
    else:
        print("  (No local venv directories found)")

    print("\n" + "=" * 80)
    print("✅ ENVIRONMENT DISCOVERY COMPLETE")
    print("=" * 80)


def test_locate_project_venv():
    """Test: Locate and verify the project's virtual environment."""
    print("\n" + "=" * 80)
    print("🎯 PROJECT VIRTUAL ENVIRONMENT")
    print("=" * 80)

    project_python = PROJECT_VENV / "bin" / "python"

    # Verify venv exists
    assert PROJECT_VENV.exists(), (
        f"❌ Project venv not found at {PROJECT_VENV}\n"
        f"Expected: {PROJECT_VENV}"
    )

    print(f"\n✅ Project venv found:")
    print(f"   Location: {PROJECT_VENV}")

    # Get version
    try:
        result = subprocess.run(
            [str(project_python), "--version"],
            capture_output=True,
            text=True,
            timeout=2
        )
        version = result.stdout.strip() or result.stderr.strip()
        print(f"   Python: {version}")
    except Exception as e:
        print(f"   Python: (could not determine - {e})")

    # Get executable
    print(f"   Executable: {project_python}")

    # Check pyvenv.cfg
    pyvenv_cfg = PROJECT_VENV / "pyvenv.cfg"
    if pyvenv_cfg.exists():
        content = pyvenv_cfg.read_text()
        print(f"   Config:")
        for line in content.split("\n"):
            if "home" in line.lower() or "version" in line.lower():
                print(f"     • {line}")

    print("\n" + "=" * 80)


def test_identify_conda_alternatives():
    """Test: Identify available Conda environments as alternatives."""
    print("\n" + "=" * 80)
    print("🔄 CONDA ALTERNATIVES")
    print("=" * 80)

    conda_envs = find_conda_environments()

    if not conda_envs:
        print("  (No Conda environments available)")
        return

    print("\n🟢 Available Conda Environments:")
    for env in conda_envs:
        marker = ""
        if env["name"] == "p14":
            marker = " ← 🌟 RECOMMENDED (Python 3.14.2)"
        elif env["name"] == "base":
            marker = " (Default)"

        print(f"\n  • {env['name']}{marker}")
        print(f"    Version: {env['version']}")
        print(f"    To activate: conda activate {env['name']}")

    # Show p14 specifically
    p14_env = next((e for e in conda_envs if e["name"] == "p14"), None)
    if p14_env:
        print("\n" + "-" * 80)
        print("🌟 Recommended: p14 (Conda)")
        print("-" * 80)
        print(f"  Path: {p14_env['path']}")
        print(f"  Version: {p14_env['version']}")
        print(f"  Why: Latest stable Python 3.14.2 release")
        print(f"  Usage for project venv creation:")
        print(f"    {p14_env['path']}/bin/python -m venv /path/to/project/.venv")

    print("\n" + "=" * 80)


def test_current_python_info():
    """Test: Display information about current Python environment."""
    print("\n" + "=" * 80)
    print("📊 CURRENT PYTHON ENVIRONMENT")
    print("=" * 80)

    print(f"\n  Executable: {sys.executable}")
    print(f"  Version: {sys.version}")
    print(f"  Prefix: {sys.prefix}")
    print(f"  Base Prefix: {sys.base_prefix}")

    if hasattr(sys, 'real_prefix'):
        print(f"  In virtualenv: Yes (virtualenv)")
    elif sys.prefix != sys.base_prefix:
        print(f"  In virtualenv: Yes (venv)")
    else:
        print(f"  In virtualenv: No (system Python)")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v", "-s"])
