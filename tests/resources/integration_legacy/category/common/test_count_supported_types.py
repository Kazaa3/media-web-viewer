# Test: Anzahl unterstützter Datentypen

import pytest
from pathlib import Path
from src.core.main import process_any_file  # oder universal_processor
import json

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
def test_supported_types(fmt, path):
    file = Path(path)
    assert file.exists(), f"Testdatei für {fmt} fehlt: {path}"
    result = process_any_file(str(file))
    data = json.loads(result)
    assert 'format' in data or 'success' in data, f"Format {fmt} nicht erkannt: {result}"

def test_count_supported_types():
    supported = 0
    for fmt, path in TEST_FILES.items():
        file = Path(path)
        if file.exists():
            result = process_any_file(str(file))
            data = json.loads(result)
            if 'error' not in data:
                supported += 1
    print(f"Unterstützte Datentypen: {supported} von {len(TEST_FILES)}")
    assert supported >= 1, "Mindestens ein Datentyp muss unterstützt werden!"
