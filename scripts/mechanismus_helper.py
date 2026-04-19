#!/usr/bin/env python3
"""
mechanismus_helper.py - Automated Environment & Cache Management
Utility for clean updates, multi-venv management, and system maintenance.
Enhanced with Progress Indicators and Stall Watchdog.
"""

import os
import sys
import shutil
import subprocess
import argparse
import time
import threading
from pathlib import Path

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
PACKAGES_DIR = PROJECT_ROOT / "packages"

# Venv Mapping
VENV_MAP = {
    "core": {
        "path": PROJECT_ROOT / ".venv_run",
        "reqs": [PROJECT_ROOT / "infra" / "requirements-core.txt", PROJECT_ROOT / "infra" / "requirements-run.txt"],
        "link": PROJECT_ROOT / ".venv_core"
    },
    "dev": {
        "path": PROJECT_ROOT / ".venv_dev",
        "reqs": [PROJECT_ROOT / "infra" / "requirements-dev.txt"]
    },
    "test": {
        "path": PROJECT_ROOT / ".venv_test",
        "reqs": [PROJECT_ROOT / "infra" / "requirements-test.txt"]
    },
    "selenium": {
        "path": PROJECT_ROOT / ".venv_selenium",
        "reqs": [PROJECT_ROOT / "infra" / "requirements-selenium.txt"]
    },
    "build": {
        "path": PROJECT_ROOT / ".venv_build",
        "reqs": [PROJECT_ROOT / "infra" / "requirements-build.txt"]
    },
    "full": {
        "path": PROJECT_ROOT / ".venv",
        "reqs": [
            PROJECT_ROOT / "infra" / "requirements-core.txt",
            PROJECT_ROOT / "infra" / "requirements-run.txt",
            PROJECT_ROOT / "infra" / "requirements-dev.txt",
            PROJECT_ROOT / "infra" / "requirements-test.txt",
            PROJECT_ROOT / "infra" / "requirements-selenium.txt",
            PROJECT_ROOT / "infra" / "requirements-build.txt"
        ]
    }
}

class ProgressBar:
    """Simple terminal progress bar."""
    def __init__(self, total, prefix='', suffix='', length=40, fill='█'):
        self.total = total
        self.prefix = prefix
        self.suffix = suffix
        self.length = length
        self.fill = fill
        self.iteration = 0

    def update(self, iteration, msg=''):
        self.iteration = iteration
        percent = ("{0:.1f}").format(100 * (self.iteration / float(self.total)))
        filled_length = int(self.length * self.iteration // self.total)
        bar = self.fill * filled_length + '-' * (self.length - filled_length)
        print(f'\r{self.prefix} |{bar}| {percent}% {self.suffix} {msg}', end='\r')
        if self.iteration == self.total:
            print()

def log(msg):
    print(f"\n[Mechanismus] {msg}")

def run_with_watchdog(cmd, timeout=300, msg="Processing"):
    """Runs a command with a heartbeat watchdog to detect stalling."""
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def monitor():
        start_time = time.time()
        while proc.poll() is None:
            elapsed = time.time() - start_time
            if elapsed > timeout:
                print(f"\n[WATCHDOG] CRITICAL: Process stalled (Timeout {timeout}s)! Terminating...")
                proc.terminate()
                break
            if int(elapsed) % 10 == 0 and int(elapsed) > 0:
                print(f"\r[HEARTBEAT] {msg} ({int(elapsed)}s elapsed)...", end='', flush=True)
            time.sleep(1)

    monitor_thread = threading.Thread(target=monitor)
    monitor_thread.start()
    
    stdout, stderr = proc.communicate()
    monitor_thread.join()
    
    if proc.returncode != 0:
        if proc.returncode == -15: # Terminated
            raise TimeoutError(f"Process timed out after {timeout}s")
        raise subprocess.CalledProcessError(proc.returncode, cmd, output=stdout, stderr=stderr)
    return stdout

def clean():
    """Deep cleans cache and temporary files."""
    log("Starting deep clean...")
    patterns = [
        "**/__pycache__",
        "**/.pytest_cache",
        "**/build",
        "**/dist",
        "**/*.pyc",
        "**/frontend_errors.log",
        "**/*.log"
    ]
    
    files_to_clean = []
    for pattern in patterns:
        files_to_clean.extend(list(PROJECT_ROOT.glob(pattern)))
    
    if not files_to_clean:
        log("Everything is already clean.")
        return

    pb = ProgressBar(len(files_to_clean), prefix='Cleaning:', length=50)
    for i, path in enumerate(files_to_clean):
        try:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.is_file():
                path.unlink()
            pb.update(i + 1, msg=f"Removed {path.name[:20]}")
        except Exception:
            pass
    log("Clean completed successfully.")

def update(target="core", offline=False):
    """Updates dependencies for a specific venv target."""
    if target == "all":
        targets = list(VENV_MAP.keys())
        for t in targets:
            update(target=t, offline=offline)
        return

    if target not in VENV_MAP:
        log(f"ERROR: Unknown target '{target}'")
        return

    entry = VENV_MAP[target]
    venv_path = entry["path"]
    req_files = entry["reqs"]

    if not venv_path.exists():
        log(f"ERROR: Venv '{target}' not found at {venv_path}. Use bootstrap first.")
        return

    venv_python = venv_path / "bin" / "python"
    log(f"Synchronizing '{target}' dependencies (Offline: {offline})...")

    # Base pip/setuptools update
    pip_base = [str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "setuptools", "wheel"]
    find_links = []
    if offline:
        for p in PACKAGES_DIR.rglob("pypi"):
            if p.is_dir():
                find_links.extend(["--find-links", str(p)])
        pip_base = [str(venv_python), "-m", "pip", "install", "--no-index"] + find_links + ["pip", "setuptools", "wheel"]

    try:
        run_with_watchdog(pip_base, msg="Updating pip core")
        
        pb = ProgressBar(len(req_files), prefix=f'Syncing {target}:', length=40)
        for i, req in enumerate(req_files):
            if not req.exists():
                pb.update(i + 1, msg=f"Skip missing {req.name}")
                continue
            
            install_cmd = [str(venv_python), "-m", "pip", "install", "-r", str(req)]
            if offline:
                install_cmd = [str(venv_python), "-m", "pip", "install", "--no-index"] + find_links + ["-r", str(req)]
            
            run_with_watchdog(install_cmd, msg=f"Installing {req.name}")
            pb.update(i + 1, msg=f"Finished {req.name}")
            
    except Exception as e:
        log(f"Update for '{target}' failed: {e}")

def bootstrap(target="core", python_bin="/usr/local/bin/python3.14", offline=False):
    """Recreates the virtual environment for a specific target."""
    if target == "all":
        for t in VENV_MAP.keys():
            bootstrap(target=t, python_bin=python_bin, offline=offline)
        return

    if target not in VENV_MAP:
        log(f"ERROR: Unknown target '{target}'")
        return

    entry = VENV_MAP[target]
    path = entry["path"]
    link = entry.get("link")

    log(f"Bootstrapping '{target}' environment (Offline: {offline})...")
    
    # Remove old venv/link
    for p in [path, link]:
        if p and os.path.lexists(str(p)):
            if p.is_symlink():
                p.unlink()
            elif p.is_dir():
                shutil.rmtree(p)

    try:
        # Create venv
        subprocess.run([python_bin, "-m", "venv", str(path)], check=True)
        log(f"Created virtual environment: {path.name}")
        
        # Create symlink if needed
        if link:
            os.symlink(path.name, link)
            log(f"Created symlink: {link.name} -> {path.name}")
        
        # Initial update
        update(target=target, offline=offline)
        log(f"Bootstrap for '{target}' completed successfully.")
    except Exception as e:
        log(f"Bootstrap for '{target}' failed: {e}")

def main():
    parser = argparse.ArgumentParser(description="Mechanismus System Helper")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Clean
    subparsers.add_parser("clean", help="Clean cache and temporary files")

    # Update
    update_parser = subparsers.add_parser("update", help="Update dependencies")
    update_parser.add_argument("--target", default="core", choices=list(VENV_MAP.keys()) + ["all"], help="Venv target")
    update_parser.add_argument("--offline", action="store_true", help="Use local packages directory")

    # Bootstrap
    bootstrap_parser = subparsers.add_parser("bootstrap", help="Recreate virtual environment")
    bootstrap_parser.add_argument("--target", default="core", choices=list(VENV_MAP.keys()) + ["all"], help="Venv target")
    bootstrap_parser.add_argument("--python", default="/usr/local/bin/python3.14", help="Path to Python binary")
    bootstrap_parser.add_argument("--offline", action="store_true", help="Use local packages directory")

    args = parser.parse_args()

    if args.command == "clean":
        clean()
    elif args.command == "update":
        update(target=args.target, offline=args.offline)
    elif args.command == "bootstrap":
        bootstrap(target=args.target, python_bin=args.python, offline=args.offline)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
