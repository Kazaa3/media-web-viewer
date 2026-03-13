#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Maintenance / Cleanup
# Eingabewerte: Project Root, .git, caches, build artifacts
# Ausgabewerte: Status-Logs, gelöschte Dateien/Ordner
# Testdateien: Keine (Utility-Skript)
# ERWEITERUNGEN (TODO): [ ] Integration in pre-commit hooks, [ ] Automatische Platzwarnung
# KOMMENTAR: Zentraler Garbage Collector für das Projekt (Python Caches, Git-Bloat, etc.)
# VERWENDUNG: python3 scripts/project_garbage_collector.py [--dry-run] [--git-gc]

"""
KATEGORIE: Maintenance / Cleanup
ZWECK: Zentraler Garbage Collector zur Bereinigung von Projekt-Caches, temporären Dateien und Git-Bloat.
EINGABEWERTE: Project Root Verzeichnis-Struktur
AUSGABEWERTE: Detailliertes Log der bereinigten Ressourcen
TESTDATEIEN: Keine
ERWEITERUNGEN (TODO): [ ] Integration in CI, [ ] Konfigurierbare Ausschlusslisten
KOMMENTAR: Schützt vor Repository-Aufblähung durch automatisches Entfernen von tmp_pack Dateien.
VERWENDUNG: python3 scripts/project_garbage_collector.py [--force] [--git-gc]
"""

import os
import shutil
import subprocess
import sys
import argparse
import time
import threading
from pathlib import Path

# --- Configuration ---
CACHE_PATTERNS = [
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".coverage",
    "htmlcov",
    ".tox",
    ".cache"
]

FILE_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.pyd",
    "*.swp",
    "*.bak",
    "*.tmp",
    ".DS_Store",
    "Thumbs.db"
]

PROJECT_DIRS = [
    "media/.cache",
    "data/logs",
    "logs"
]

class AliveIndicator:
    """Displays a simple spinner to show the process is still alive."""
    def __init__(self, message="Working"):
        self.message = message
        self.stop_event = threading.Event()
        self.thread = threading.Thread(target=self._spin)

    def _spin(self):
        chars = "|/-\\"
        i = 0
        while not self.stop_event.is_set():
            sys.stdout.write(f"\r[*] {self.message}... {chars[i % len(chars)]} ")
            sys.stdout.flush()
            time.sleep(0.1)
            i += 1

    def start(self):
        self.thread.start()

    def stop(self):
        self.stop_event.set()
        self.thread.join()
        sys.stdout.write("\r" + " " * (len(self.message) + 20) + "\r")
        sys.stdout.flush()

def get_git_status(root):
    """Get basic git status info (ahead/behind)."""
    try:
        # Check ahead/behind main
        res = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", "main...HEAD"],
            cwd=root, capture_output=True, text=True, check=False
        )
        if res.returncode == 0:
            ahead_behind = res.stdout.strip().split()
            if len(ahead_behind) == 2:
                return f"Main Context: {ahead_behind[1]} commits ahead, {ahead_behind[0]} behind"
    except Exception:
        pass
    return "Git Status: No main branch comparison available"

def clean_patterns(root, dry_run=True):
    """Clean directories matching CACHE_PATTERNS and files matching FILE_PATTERNS using os.walk."""
    deleted_count = 0
    freed_space = 0

    print(f"[*] Scanning for cache patterns in {root}...")
    
    # Define paths to skip
    skip_dirs = {".venv", ".venv_dev", ".git", "media", "node_modules", "dist", "build"}

    for root_dir, dirs, files in os.walk(root):
        # Skip restricted directories in-place to avoid descending into them
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        
        # 1. Check for directory-based cache patterns
        for d in list(dirs):
            if d in CACHE_PATTERNS:
                item_path = Path(root_dir) / d
                try:
                    size = sum(f.stat().st_size for f in item_path.rglob('*') if f.is_file())
                    print(f"  [DIR]  {'[DRY-RUN] ' if dry_run else ''}Removing {item_path} ({size / 1024:.1f} KB)")
                    if not dry_run:
                        shutil.rmtree(item_path)
                        dirs.remove(d) # Don't walk into deleted dir
                    deleted_count += 1
                    freed_space += size
                except Exception as e:
                    print(f"  [ERR]  Could not process directory {item_path}: {e}")

        # 2. Check for file-based patterns
        import fnmatch
        for pattern in FILE_PATTERNS:
            for f in fnmatch.filter(files, pattern):
                item_path = Path(root_dir) / f
                try:
                    size = item_path.stat().st_size
                    print(f"  [FILE] {'[DRY-RUN] ' if dry_run else ''}Removing {item_path} ({size / 1024:.1f} KB)")
                    if not dry_run:
                        item_path.unlink()
                    deleted_count += 1
                    freed_space += size
                except Exception as e:
                    print(f"  [ERR]  Could not delete file {item_path}: {e}")

    return deleted_count, freed_space

def clean_project_dirs(root, dry_run=True):
    """Clean specific project directories."""
    root_path = Path(root)
    deleted_count = 0
    freed_space = 0

    for rel_path in PROJECT_DIRS:
        target = root_path / rel_path
        if target.exists() and target.is_dir():
            try:
                size = sum(f.stat().st_size for f in target.rglob('*') if f.is_file())
                print(f"  [PROJ] {'[DRY-RUN] ' if dry_run else ''}Cleaning {target} ({size / 1024:.1f} KB)")
                if not dry_run:
                    # We often want to keep the directory but empty it
                    for item in target.iterdir():
                        if item.is_dir():
                            shutil.rmtree(item)
                        else:
                            item.unlink()
                deleted_count += 1
                freed_space += size
            except Exception as e:
                print(f"  [ERR]  Error cleaning project dir {target}: {e}")
            
    return deleted_count, freed_space

def clean_git_bloat(root, dry_run=True, run_gc=False):
    """Remove temporary git packs and optionally run garbage collection."""
    git_dir = Path(root) / ".git"
    if not git_dir.exists():
        return 0, 0

    deleted_count = 0
    freed_space = 0
    
    # Remove tmp_pack files
    pack_dir = git_dir / "objects" / "pack"
    if pack_dir.exists():
        for tmp_pack in pack_dir.glob("tmp_pack_*"):
            try:
                size = tmp_pack.stat().st_size
                print(f"  [GIT]  {'[DRY-RUN] ' if dry_run else ''}Removing {tmp_pack.name} ({size / (1024*1024):.1f} MB)")
                if not dry_run:
                    tmp_pack.unlink()
                deleted_count += 1
                freed_space += size
            except Exception as e:
                print(f"  [ERR]  Error removing git tmp pack {tmp_pack.name}: {e}")

    if run_gc and not dry_run:
        indicator = AliveIndicator("Running git gc --prune=now")
        indicator.start()
        try:
            subprocess.run(["git", "gc", "--prune=now"], cwd=root, capture_output=True)
            print("\n  [GIT]  Garbage collection completed successfully.")
        except Exception as e:
            print(f"\n  [ERR]  Git GC failed: {e}")
        finally:
            indicator.stop()

    return deleted_count, freed_space

def print_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=40, fill='█', print_end="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        print_end   - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total: 
        print()

def main():
    parser = argparse.ArgumentParser(description="Media Web Viewer Project Garbage Collector")
    parser.add_argument("--force", action="store_true", help="Execute deletion (otherwise dry-run)")
    parser.add_argument("--git-gc", action="store_true", help="Run git garbage collection")
    parser.add_argument("--status", action="store_true", help="Just show git status and space estimation")
    args = parser.parse_args()

    root_dir = Path(__file__).parents[1]
    dry_run = not args.force

    print("=" * 60)
    print(f"🧹 Project Garbage Collector - Mode: {'EXECUTE' if not dry_run else 'DRY-RUN'}")
    print(f"[*] {get_git_status(root_dir)}")
    print("=" * 60)

    if args.status:
        # Shallow check for status mode
        print("[!] Status mode: Estimating bloat (dry-run patterns)...")
        dry_run = True

    try:
        total_deleted = 0
        total_space = 0
        
        steps = [
            ("Patterns", clean_patterns),
            ("Project Dirs", clean_project_dirs),
            ("Git Bloat", clean_git_bloat)
        ]
        
        num_steps = len(steps)
        for i, (name, func) in enumerate(steps):
            print_progress_bar(i, num_steps, prefix='Progress:', suffix=f'Complete ({name})', length=40)
            if name == "Git Bloat":
                c, s = func(root_dir, dry_run, args.git_gc)
            else:
                c, s = func(root_dir, dry_run)
            total_deleted += c
            total_space += s
            
        print_progress_bar(num_steps, num_steps, prefix='Progress:', suffix='Cleanup Finished', length=40)

        print("=" * 60)
        print(f"📊 Summary: {total_deleted} items identified/removed")
        print(f"💾 Total space {'reclaimed' if not dry_run else 'identfied'}: {total_space / (1024*1024):.2f} MB")
        if dry_run and not args.status:
            print("\n[!] This was a dry-run. Use --force to actually delete files.")
        print("=" * 60)

    except KeyboardInterrupt:
        print("\n\n[!] ABORTED: Keyboard interruption detected. Stopping safely...")
        sys.exit(1)

if __name__ == "__main__":
    main()
