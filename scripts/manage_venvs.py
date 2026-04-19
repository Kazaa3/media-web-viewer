#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Centralized Virtual Environment Management
Handles discovery, creation, and synchronization of all project venvs.
"""

import os
import sys
import subprocess
import shutil
import time
from pathlib import Path
from typing import Dict, List, Optional

# Project Structure
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
INFRA = ROOT / "infra"
REQUIREMENTS_DIR = INFRA

# Venv Mapping: {venv_name: requirements_file}
VENVS = {
    ".venv_core": "requirements-core.txt",
    ".venv_build": "requirements-build.txt",
    ".venv_dev": "requirements-dev.txt",
    ".venv_testbed": "requirements-test.txt",
    ".venv_selenium": "requirements-selenium.txt",
    ".venv_run": "requirements-run.txt",
    "venv": "requirements.txt",
}

# Python version mapping: {venv_name: python_version}
# Note: uses system discovery (e.g., 'python3.14')
VENV_PYTHON_VERSIONS = {
    ".venv_core": "python3.14",
}


def print_status(message: str, category: str = "INFO"):
    """Print a formatted status message."""
    icons = {"INFO": "ℹ️", "SUCCESS": "✅", "WARNING": "⚠️", "ERROR": "❌", "PROCESS": "⚙️"}
    icon = icons.get(category, "•")
    print(f"{icon} {message}")

class VenvManager:
    def __init__(self):
        self.root = ROOT
        self.conda_active = "CONDA_PREFIX" in os.environ

    def get_venv_path(self, name: str) -> Path:
        """Return absolute path to a venv."""
        return self.root / name

    def check_venv(self, name: str) -> bool:
        """Check if a venv exists and has a python executable."""
        py_bin = self.get_venv_path(name) / "bin" / "python"
        return py_bin.exists()

    def sync_venv(self, name: str, force: bool = False):
        """Create or update a venv."""
        venv_path = self.get_venv_path(name)
        req_name = VENVS.get(name, "requirements.txt")
        req_file = REQUIREMENTS_DIR / req_name
        
        # Fallback to ROOT if not in INFRA
        if not req_file.exists():
             req_file = ROOT / req_name

        if not req_file.exists():
            print_status(f"Requirement file {req_file.name} missing for {name}", "ERROR")
            return False

        if force and venv_path.exists():
            print_status(f"Removing existing {name} (force=True)...", "PROCESS")
            shutil.rmtree(venv_path)

        if not venv_path.exists():
            print_status(f"Creating venv: {name}...", "PROCESS")
            python_exe = VENV_PYTHON_VERSIONS.get(name, sys.executable)
            print_status(f"Using base python: {python_exe}", "INFO")
            try:
                subprocess.run([python_exe, "-m", "venv", str(venv_path)], check=True)
            except subprocess.CalledProcessError as e:
                print_status(f"Failed to create venv with {python_exe}: {e}", "ERROR")
                # Fallback to sys.executable if it was a specific version request
                if python_exe != sys.executable:
                    print_status(f"Retrying with current interpreter: {sys.executable}", "WARNING")
                    subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
                else:
                    raise

        
        py_bin = venv_path / "bin" / "python"
        pip_bin = venv_path / "bin" / "pip"

        print_status(f"Syncing {name} dependencies with monitoring...", "PROCESS")
        
        # Use our new monitoring utility
        SCRIPTS_PATH = ROOT / "scripts"
        if str(SCRIPTS_PATH) not in sys.path:
            sys.path.append(str(SCRIPTS_PATH))
        import monitor_utils  # type: ignore
        from monitor_utils import run_monitored
        
        cmd = [str(pip_bin), "install", "-r", str(req_file), "--upgrade"]
        
        def on_pip_output(line):
            if "Requirement already satisfied" not in line:
                print(f"  [pip] {line}")

        success = run_monitored(
            cmd,
            hang_timeout=120,    # Pip can be slow but should output something
            alive_interval=20,
            on_output=on_pip_output
        )

        if success:
            print_status(f"Venv {name} is up to date.", "SUCCESS")
            return True
        else:
            print_status(f"Failed to sync {name}.", "ERROR")
            return False

    def get_installed_packages(self, name: str) -> List[str]:
        """Get list of installed packages in a venv."""
        if not self.check_venv(name):
            return []
        
        pip_bin = self.get_venv_path(name) / "bin" / "pip"
        try:
            result = subprocess.run(
                [str(pip_bin), "freeze"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.splitlines()
        except Exception:
            return []

    def clean_fragments(self):
        """Clean temporary build/test fragments if any exist."""
        fragments = [ROOT / "build" / "deb_staging", ROOT / "tests" / "__pycache__"]
        for frag in fragments:
            if frag.exists():
                print_status(f"Cleaning fragment: {frag}", "PROCESS")
                if frag.is_file():
                    frag.unlink()
                else:
                    shutil.rmtree(frag)

    def clean_venv(self, name: str):
        """Completely remove a venv directory."""
        venv_path = self.get_venv_path(name)
        if venv_path.exists():
            print_status(f"Removing venv: {name}...", "PROCESS")
            try:
                shutil.rmtree(venv_path)
                print_status(f"Venv {name} removed.", "SUCCESS")
                return True
            except Exception as e:
                print_status(f"Failed to remove {name}: {e}", "ERROR")
                return False
        else:
            print_status(f"Venv {name} does not exist.", "INFO")
            return True

    def show_status(self, detailed: bool = False):
        """Show status of all venvs."""
        print("\n" + "="*40)
        print("  Project Venv Status")
        print("="*40)
        
        if self.conda_active:
            conda_env = os.environ.get('CONDA_DEFAULT_ENV')
            conda_prefix = os.environ.get('CONDA_PREFIX')
            print_status(f"Conda active: {conda_env} ({conda_prefix})", "WARNING")

        for name in VENVS:
            exists = self.check_venv(name)
            status = "✅ Installed" if exists else "❌ Missing"
            
            py_ver = "unknown"
            ver_ok = True
            if exists:
                py_bin = self.get_venv_path(name) / "bin" / "python"
                try:
                    ver_res = subprocess.run([str(py_bin), "--version"], capture_output=True, text=True)
                    py_ver = ver_res.stdout.strip()
                    
                    target = VENV_PYTHON_VERSIONS.get(name)
                    if target and target not in py_ver.lower():
                        status = f"⚠️ Version Mismatch (Target: {target})"
                        ver_ok = False
                except Exception:
                    py_ver = "unknown"

            rec_tag = " ⭐ RECOMMENDED" if name == ".venv_core" else ""
            print(f"- {name:15} : {status} ({py_ver}){rec_tag}")
            
            if detailed and exists:
                packages = self.get_installed_packages(name)
                # Show top 5 packages as a summary using loop to avoid slice lints
                count = 0
                for pkg in packages:
                    if count >= 5: break
                    print(f"    • {pkg}")
                    count += 1
                if len(packages) > 5:
                    print(f"    ... and {len(packages)-5} more.")
        print("="*40 + "\n")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Media Web Viewer Venv Manager")
    parser.add_argument("--sync", choices=list(VENVS.keys()) + ["all"], help="Sync specified venv or all")
    parser.add_argument("--rebuild", choices=list(VENVS.keys()) + ["all"], help="Rebuild (force sync) specified venv or all")
    parser.add_argument("--clean-venv", choices=list(VENVS.keys()) + ["all"], help="Remove specified venv or all")
    parser.add_argument("--status", action="store_true", help="Show current venv status")
    parser.add_argument("--detailed", action="store_true", help="Show detailed status with packages")
    parser.add_argument("--clean-fragments", action="store_true", help="Clean test/log fragments")
    parser.add_argument("--force", action="store_true", help="Force recreation of venv (used with --sync)")

    args = parser.parse_args()
    manager = VenvManager()

    if args.status or args.detailed or not any(vars(args).values()):
        manager.show_status(detailed=args.detailed)

    if args.clean_fragments:
        manager.clean_fragments()

    if args.sync:
        if args.sync == "all":
            for name in VENVS:
                manager.sync_venv(name, force=args.force)
        else:
            manager.sync_venv(args.sync, force=args.force)

    if args.rebuild:
        if args.rebuild == "all":
            for name in VENVS:
                manager.sync_venv(name, force=True)
        else:
            manager.sync_venv(args.rebuild, force=True)

    if args.clean_venv:
        if args.clean_venv == "all":
            for name in VENVS:
                manager.clean_venv(name)
        else:
            manager.clean_venv(args.clean_venv)

if __name__ == "__main__":
    main()
