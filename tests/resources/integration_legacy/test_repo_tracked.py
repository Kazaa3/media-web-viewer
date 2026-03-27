# =============================================================================
# Kategorie: Repository Tracking Test
# Eingabewerte: Dateipfade, Git-Status
# Ausgabewerte: Existenz- und Git-Tracking-Status
# Testdateien: test_repo_tracked.py
# Kommentar: Prüft, ob wichtige Dateien im Workspace existieren und von Git getrackt werden.
# Startbefehl: pytest tests/test_repo_tracked.py -v
# =============================================================================
"""
Repository Tracking Test Suite (DE/EN)
======================================

DE:
Testet, ob relevante Dateien im Workspace existieren und von Git getrackt werden.

EN:
Tests whether relevant files in the workspace exist and are tracked by Git.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import subprocess
from pathlib import Path
import pytest

FILES_TO_CHECK = [
    "logbuch/324_SMB_and_Docker_Headless_CLI.md",
    "logbuch/325_mwv-cli.md",
    "tests/test_cli_parse.py",
    "tests/test_subprocess_wrapper.py",
    "tests/test_docker_headless_integration.py",
    "cli.py",
    "tools/ffprobe_wrapper.py",
    "Dockerfile.headless",
    "docker-compose.ci.yml",
    ".github/workflows/backend-integration.yml",
]

def test_files_exist():
    """
    DE:
    Testet, ob alle angegebenen Dateien im Workspace existieren.

    EN:
    Tests if all specified files exist in the workspace.

    Returns:
        Keine.
    Raises:
        AssertionError: Wenn Dateien fehlen.
    """
    missing = [p for p in FILES_TO_CHECK if not Path(p).exists()]
    assert not missing, f"Missing files in workspace: {missing}"

def test_files_tracked_by_git():
    """
    DE:
    Testet, ob alle angegebenen Dateien von Git getrackt werden.

    EN:
    Tests if all specified files are tracked by Git.

    Returns:
        Keine.
    Raises:
        pytest.skip: Wenn kein Git-Repository vorhanden ist.
        pytest.fail: Wenn Dateien nicht getrackt werden.
    """
    # Skip if not a git repo
    if not Path('.git').exists():
        pytest.skip('Not a git repository; skipping git-tracking checks')

    not_tracked = []
    for p in FILES_TO_CHECK:
        try:
            subprocess.run(["git", "ls-files", "--error-unmatch", p], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except subprocess.CalledProcessError:
            not_tracked.append(p)

    if not_tracked:
        hint_lines = [f"git add {p}" for p in not_tracked]
        hint = '\n'.join(hint_lines)
        pytest.fail(f"These files are not tracked by git:\n{not_tracked}\n\nSuggested fix:\n{hint}")
