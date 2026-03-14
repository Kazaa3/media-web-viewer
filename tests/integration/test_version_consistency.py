# =============================================================================
# Kategorie: Versioning / Release Consistency Test
# Eingabewerte: VERSION, main.py, packaging/DEBIAN/control, DOCUMENTATION.md
# Ausgabewerte: Konsistenz-Checks für Versionsnummern
# Testdateien: test_version_consistency.py
# Kommentar: Testet zentrale Ableitung und Konsistenz der Projektversion.
# =============================================================================
"""
Versioning / Release Consistency Test Suite (DE/EN)
===================================================

DE:
Testet die zentrale Ableitung und Konsistenz der Projektversion über alle relevanten Dateien.

EN:
Tests central derivation and consistency of project version across all relevant files.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import re
from pathlib import Path

def _root_dir() -> Path:
    """
    DE:
    Gibt das Projekt-Root-Verzeichnis zurück.
    EN:
    Returns the project root directory.
    """
    return Path(__file__).parents[3].parent

def _read_current_version() -> str:
    """
    DE:
    Liest die aktuelle Version aus der VERSION-Datei.
    EN:
    Reads the current version from the VERSION file.
    """
    version_file = _root_dir() / "VERSION"
    version = version_file.read_text(encoding="utf-8").strip()
    assert re.fullmatch(r"\d+\.\d+\.\d+", version), (
        f"Ungültiges VERSION-Format in {version_file}: {version!r}"
    )
    return version

def test_version_file_is_valid_semver():
    """
    DE:
    Testet, ob die VERSION-Datei ein gültiges Semver-Format hat.
    EN:
    Tests if the VERSION file has valid semver format.
    """
    current = _read_current_version()
    print(f"✅ VERSION: {current}")

def test_canonical_locations_match_version_file():
    """
    DE:
    Testet, ob alle kanonischen Orte die Version aus der VERSION-Datei übernehmen.
    EN:
    Tests if all canonical locations adopt the version from the VERSION file.
    """
    current = _read_current_version()
    root = _root_dir()

    main_py = (root / "src/core/main.py").read_text(encoding="utf-8")
    control = (root / "packaging/DEBIAN/control").read_text(encoding="utf-8")
    docs = (root / "DOCUMENTATION.md").read_text(encoding="utf-8")

    fallback_match = re.search(r'VERSION\s*=\s*"(\d+\.\d+\.\d+)"\s*#\s*Fallback', main_py)
    assert fallback_match, "Fallback-Version in main.py nicht gefunden"
    assert fallback_match.group(1) == current, (
        f"src/core/main.py Fallback-Version ist {fallback_match.group(1)}, erwartet {current}"
    )

    control_match = re.search(r"^Version:\s*(\d+\.\d+\.\d+)\s*$", control, flags=re.MULTILINE)
    assert control_match, "Version in packaging/DEBIAN/control nicht gefunden"
    assert control_match.group(1) == current, (
        f"control-Version ist {control_match.group(1)}, erwartet {current}"
    )

    docs_version_match = re.search(r"\*\*Version:\*\*\s*(\d+\.\d+\.\d+)", docs)
    assert docs_version_match, "**Version:** in DOCUMENTATION.md nicht gefunden"
    assert docs_version_match.group(1) == current, (
        f"Doku-Version ist {docs_version_match.group(1)}, erwartet {current}"
    )

    docs_current_match = re.search(r"\*\*Current Version:\*\*\s*(\d+\.\d+\.\d+)", docs)
    assert docs_current_match, "**Current Version:** in DOCUMENTATION.md nicht gefunden"
    assert docs_current_match.group(1) == current, (
        f"Doku Current Version ist {docs_current_match.group(1)}, erwartet {current}"
    )

def test_no_old_deb_version_examples_in_documentation():
    """
    DE:
    Testet, dass keine alten .deb Versionsbeispiele in der Dokumentation stehen.
    EN:
    Tests that no old .deb version examples are present in the documentation.
    """
    current = _read_current_version()
    docs = (_root_dir() / "DOCUMENTATION.md").read_text(encoding="utf-8")

    deb_versions = re.findall(r"media-web-viewer_(\d+\.\d+\.\d+)_amd64\.deb", docs)
    assert deb_versions, "Keine .deb Versionsbeispiele in DOCUMENTATION.md gefunden"

    stale = sorted({version for version in deb_versions if version != current})
    assert not stale, (
        "Veraltete .deb Versionsbeispiele in Doku gefunden: "
        f"{', '.join(stale)} (erwartet überall {current})"
    )
