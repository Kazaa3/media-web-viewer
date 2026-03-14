# Coverage-Test für Formate und Typen

import pytest
from pathlib import Path
from src.core.main import process_any_file  # oder universal_processor

# Liste aller Testdateien für Formate (Dummy-Files im testdata/)
TEST_FILES = {
    'epub': 'testdata/test.epub',
    'pdf': 'testdata/test.pdf',
    'docx': 'testdata/test.docx',
    'odt': 'testdata/test.odt',
    'rtf': 'testdata/test.rtf',
    'xlsx': 'testdata/test.xlsx',
    'pptx': 'testdata/test.pptx',
    'cbz': 'testdata/test.cbz',
    'cbr': 'testdata/test.cbr',
    'html': 'testdata/test.html',
    'mobi': 'testdata/test.mobi',
    'fb2': 'testdata/test.fb2',
    'djvu': 'testdata/test.djvu',
    'chm': 'testdata/test.chm',
    # ...weitere Formate nach Bedarf
}

@pytest.mark.parametrize("fmt, path", TEST_FILES.items())
def test_format_coverage(fmt, path):
    file = Path(path)
    assert file.exists(), f"Testdatei für {fmt} fehlt: {path}"
    result = process_any_file(str(file))
    assert 'error' not in result.lower(), f"Fehler beim Verarbeiten von {fmt}: {result}"
    assert fmt.upper() in result.upper(), f"Format {fmt} nicht korrekt erkannt: {result}"

# Typen-Test: Prüfe, ob Rückgabe ein dict/json ist
@pytest.mark.parametrize("fmt, path", TEST_FILES.items())
def test_format_type(fmt, path):
    file = Path(path)
    result = process_any_file(str(file))
    assert isinstance(result, str), "Rückgabe muss JSON-String sein"
    # Optional: parse JSON und Typ prüfen
    import json
    data = json.loads(result)
    assert isinstance(data, dict), "Rückgabe muss dict sein"

# Coverage-Report: pytest --cov=main --cov-report=term-missing
