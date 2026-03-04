
import sys
import os
from pathlib import Path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from parsers import filename_parser

def test_filename_parser_simple():
    name = "Artist - Title.mp3"
    path = Path("/path/to/" + name)
    tags = filename_parser.parse(path, name, {})
    assert tags['artist'] == "Artist"
    assert tags['title'] == "Title"

def test_filename_parser_complex():
    name = "01-Artist - Title (Remix).flac"
    path = Path("/path/to/" + name)
    tags = filename_parser.parse(path, name, {})
    # Depending on how the parser handles leading numbers and parentheticals
    assert "Artist" in tags['artist']
    assert "Title" in tags['title']
