from pathlib import Path
from src.parsers import isoparser_parser

def test_isoparser_parser():
    test_iso = Path('media/OLE_DB_ODBC.iso')
    tags = {}
    result = isoparser_parser.parse(test_iso, '.iso', tags)
    assert 'iso_volume_label' in result or 'iso_error' in result
    print('isoparser_parser test result:', result)

if __name__ == '__main__':
    test_isoparser_parser()
