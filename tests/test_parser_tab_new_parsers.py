import pytest
from parsers import media_parser

@pytest.mark.parametrize("parser_name", [
    "ffprobe_parser",
    "mutagen_parser",
    "mediainfo_parser",
    "m3u8_parser",
    "iso_parser"
])
def test_parser_tab_lists_new_parsers(parser_name):
    available = media_parser.get_available_parsers()
    assert parser_name in available, f"Parser {parser_name} fehlt im Parser-Tab!"

@pytest.mark.parametrize("parser_name, sample_file", [
    ("ffprobe_parser", "tests/samples/sample.mp4"),
    ("mutagen_parser", "tests/samples/sample.mp3"),
    ("mediainfo_parser", "tests/samples/sample.mkv"),
    ("m3u8_parser", "tests/samples/sample.m3u8"),
    ("iso_parser", "tests/samples/sample.iso")
])
def test_parser_extracts_metadata(parser_name, sample_file):
    parser = media_parser.get_parser(parser_name)
    metadata = parser.parse(sample_file, None, {}, sample_file, "default")
    assert metadata, f"Parser {parser_name} liefert keine Metadaten für {sample_file}!"
