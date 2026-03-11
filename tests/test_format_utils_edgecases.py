import os
import sys
from pathlib import Path

import pytest

sys.path.append(str(Path(__file__).resolve().parents[1]))

from parsers.format_utils import detect_file_format


def test_detect_with_none_path():
    assert detect_file_format(None) == 'UNKNOWN'


def test_detect_uppercase_extension(tmp_path):
    f = tmp_path / 'SONG.MP3'
    f.write_text('x')
    assert detect_file_format(f) == 'MP3'


def test_detect_no_extension(tmp_path):
    f = tmp_path / 'README'
    f.write_text('x')
    # No extension -> UNKNOWN or fallback
    assert detect_file_format(f) in ('UNKNOWN', 'README'.upper())


def test_detect_directory(tmp_path):
    d = tmp_path / 'folder'
    d.mkdir()
    assert detect_file_format(d) == 'DIRECTORY'


def test_detect_disk_image_with_tag(tmp_path):
    f = tmp_path / 'disk.iso'
    f.write_text('x')
    res = detect_file_format(f, tags={'pycdlib_volume_id': 'BLU123'})
    # Tag indicates blu -> Blu-ray (Abbild)
    assert 'Blu-ray' in res or 'Disk' in res
