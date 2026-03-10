import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../parsers')))
import isoparser_parser

def test_isoparser_parser():
    test_iso = Path('../media/test.iso')
    tags = {}
    result = isoparser_parser.parse(test_iso, '.iso', tags)
    assert 'iso_volume_label' in result or 'iso_error' in result
    print('isoparser_parser test result:', result)

if __name__ == '__main__':
    test_isoparser_parser()
