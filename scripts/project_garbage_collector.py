#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Maintenance / Cleanup
# Eingabewerte: Project Root, .git, caches, build artifacts
# Ausgabewerte: Status-Logs, gelöschte Dateien/Ordner
# Testdateien: Keine (Utility-Skript)
# ERWEITERUNGEN (TODO): [ ] Integration in pre-commit hooks, [ ] Automatische Platzwarnung
# KOMMENTAR: Zentraler Garbage Collector für das Projekt (Python Caches, Git-Bloat, etc.)
# VERWENDUNG: python3 scripts/project_garbage_collector.py [--force] [--git-gc]

"""
KATEGORIE: Maintenance / Cleanup
ZWECK: Zentraler Garbage Collector zur Bereinigung von Projekt-Caches, temporären Dateien und Git-Bloat.
EINGABEWERTE: Project Root Verzeichnis-Struktur
AUSGABEWERTE: Detailliertes Log der bereinigten Ressourcen
KOMMENTAR: Schützt vor Repository-Aufblähung durch automatisches Entfernen von tmp_pack Dateien.
VERWENDUNG: python3 scripts/project_garbage_collector.py [--force] [--git-gc]
"""

import os
import shutil
import subprocess
import sys
import argparse
import time
from pathlib import Path
from status_bar_utils import StatusBar

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

def get_git_status(root):
    """Get basic git status info (ahead/behind)."""
    try:
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
    """Clean directories matching CACHE_PATTERNS and files matching FILE_PATTERNS."""
    deleted_count = 0
    freed_space = 0
    skip_dirs = {".venv", ".venv_dev", ".git", "media", "node_modules", "dist", "build"}

    for root_dir, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for d in list(dirs):
            if d in CACHE_PATTERNS:
                item_path = Path(root_dir) / d
                try:
                    size = sum(f.stat().st_size for f in item_path.rglob('*') if f.is_file())
                    if not dry_run:
                        shutil.rmtree(item_path)
                    deleted_count += 1
                    freed_space += size
                except Exception:
                    pass
        import fnmatch
        for pattern in FILE_PATTERNS:
            for f in fnmatch.filter(files, pattern):
                item_path = Path(root_dir) / f
                try:
                    size = item_path.stat().st_size
                    if not dry_run:
                        item_path.unlink()
                    deleted_count += 1
                    freed_space += size
                except Exception:
                    pass
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
                if not dry_run:
                    for item in target.iterdir():
                        if item.is_dir(): shutil.rmtree(item)
                        else: item.unlink()
                deleted_count += 1
                freed_space += size
            except Exception:
                pass
    return deleted_count, freed_space

def clean_git_bloat(root, dry_run=True, run_gc=False):
    """Remove temporary git packs and optionally run garbage collection."""
    git_dir = Path(root) / ".git"
    deleted_count = 0
    freed_space = 0
    if not git_dir.exists(): return 0, 0

    pack_dir = git_dir / "objects" / "pack"
    if pack_dir.exists():
        for tmp_pack in pack_dir.glob("tmp_pack_*"):
            try:
                size = tmp_pack.stat().st_size
                if not dry_run: tmp_pack.unlink()
                deleted_count += 1
                freed_space += size
            except Exception:
                pass

    if run_gc and not dry_run:
        with StatusBar("Running git gc", total=100) as sb:
            sb.update(50, "(Processing...)")
            subprocess.run(["git", "gc", "--prune=now"], cwd=root, capture_output=True)
            sb.update(100, "(Done)")
    return deleted_count, freed_space

def main():
    parser = argparse.ArgumentParser(description="Media Web Viewer Project Garbage Collector")
    parser.add_argument("--force", action="store_true", help="Execute deletion")
    parser.add_argument("--git-gc", action="store_true", help="Run git garbage collection")
    args = parser.parse_args()

    root_dir = Path(__file__).parents[1]
    dry_run = not args.force

    print("=" * 60)
    print(f"🧹 Project Garbage Collector - Mode: {'EXECUTE' if not dry_run else 'DRY-RUN'}")
    print(f"[*] {get_git_status(root_dir)}")
    print("=" * 60)

    steps = [("Patterns", clean_patterns), ("Project Dirs", clean_project_dirs), ("Git Bloat", clean_git_bloat)]
    total_deleted, total_space = 0, 0
    
    with StatusBar("Progress", total=len(steps)) as sb:
        for i, (name, func) in enumerate(steps):
            sb.update(i, f"({name})")
            if name == "Git Bloat":
                c, s = func(root_dir, dry_run, args.git_gc)
            else:
                c, s = func(root_dir, dry_run)
            total_deleted += c
            total_space += s
        sb.update(len(steps), "(Cleanup Finished)")

    print("=" * 60)
    print(f"📊 Summary: {total_deleted} items identified/removed")
    print(f"💾 Total space {'reclaimed' if not dry_run else 'identified'}: {total_space / (1024*1024):.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    main()
