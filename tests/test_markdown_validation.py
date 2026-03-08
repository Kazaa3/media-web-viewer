# Kategorie: Markdown Validation
# Eingabewerte: README.md, DOCUMENTATION.md, etc.
# Ausgabewerte: Validierungs-Status
# Testdateien: *.md
# Kommentar: Prüft ob alle Markdown-Dateien im Projekt valide sind.

import os
import pytest


def test_markdown_validity() -> None:
    """Prüft die Validität der Markdown-Dateien."""
    try:
        import markdown  # type: ignore
    except ImportError:
        pytest.skip("markdown library not installed")

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    md_files = []
    for root, _, files in os.walk(root_dir):
        if "venv" in root or "node_modules" in root or "packaging" in root:
            continue
        for filename in files:
            if filename.endswith('.md'):
                md_files.append(os.path.join(root, filename))

    for md_file in md_files:
        with open(md_file, 'r', encoding='utf-8') as f_obj:
            content = f_obj.read()
            # Simple check if markdown can parse it without error
            try:
                markdown.markdown(content)
            except Exception as e:
                pytest.fail(f"Markdown validation failed for {md_file}: {e}")
