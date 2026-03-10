import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../parsers')))
import pycdlib

def test_pycdlib_parser():
    test_iso = Path('../media/test.iso')
    tags = {}
    try:
        iso = pycdlib.PyCdlib()
        iso.open(str(test_iso))
        tags['pycdlib_volume_id'] = iso.get_volume_id()
        iso.close()
    except Exception as e:
        tags['pycdlib_error'] = str(e)
    print('pycdlib_parser test result:', tags)

if __name__ == '__main__':
    test_pycdlib_parser()
