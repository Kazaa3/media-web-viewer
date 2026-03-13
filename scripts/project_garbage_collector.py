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
                size = sum(f.stat().st_size for f in item_path.rglob('*') if f.is_file())
                print(f"  [DIR]  {'[DRY-RUN] ' if dry_run else ''}Removing {item_path} ({size / 1024:.1f} KB)")
                if not dry_run:
                    shutil.rmtree(item_path)
                    dirs.remove(d) # Don't walk into deleted dir
                deleted_count += 1
                freed_space += size

        # 2. Check for file-based patterns
        import fnmatch
        for pattern in FILE_PATTERNS:
            for f in fnmatch.filter(files, pattern):
                item_path = Path(root_dir) / f
                size = item_path.stat().st_size
                print(f"  [FILE] {'[DRY-RUN] ' if dry_run else ''}Removing {item_path} ({size / 1024:.1f} KB)")
                if not dry_run:
                    item_path.unlink()
                deleted_count += 1
                freed_space += size

    return deleted_count, freed_space

def clean_project_dirs(root, dry_run=True):
    """Clean specific project directories."""
    root_path = Path(root)
    deleted_count = 0
    freed_space = 0

    for rel_path in PROJECT_DIRS:
        target = root_path / rel_path
        if target.exists() and target.is_dir():
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
            size = tmp_pack.stat().st_size
            print(f"  [GIT]  {'[DRY-RUN] ' if dry_run else ''}Removing {tmp_pack.name} ({size / (1024*1024):.1f} MB)")
            if not dry_run:
                tmp_pack.unlink()
            deleted_count += 1
            freed_space += size

    if run_gc and not dry_run:
        print("[*] Running git gc --prune=now (this may take a while)...")
        subprocess.run(["git", "gc", "--prune=now"], cwd=root)

    return deleted_count, freed_space

def main():
    parser = argparse.ArgumentParser(description="Media Web Viewer Project Garbage Collector")
    parser.add_argument("--force", action="store_true", help="Execute deletion (otherwise dry-run)")
    parser.add_argument("--git-gc", action="store_true", help="Run git garbage collection")
    args = parser.parse_args()

    root_dir = Path(__file__).parents[1]
    dry_run = not args.force

    print("=" * 60)
    print(f"🧹 Project Garbage Collector - Mode: {'EXECUTE' if not dry_run else 'DRY-RUN'}")
    print("=" * 60)

    total_deleted = 0
    total_space = 0

    # 1. Patterns
    c, s = clean_patterns(root_dir, dry_run)
    total_deleted += c
    total_space += s

    # 2. Project Dirs
    c, s = clean_project_dirs(root_dir, dry_run)
    total_deleted += c
    total_space += s

    # 3. Git Bloat
    c, s = clean_git_bloat(root_dir, dry_run, args.git_gc)
    total_deleted += c
    total_space += s

    print("=" * 60)
    print(f"📊 Summary: {total_deleted} items identified/removed")
    print(f"💾 Estimated space: {total_space / (1024*1024):.2f} MB")
    if dry_run:
        print("\n[!] This was a dry-run. Use --force to actually delete files.")
    print("=" * 60)

if __name__ == "__main__":
    main()
