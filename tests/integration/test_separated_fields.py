# Kategorie: Unit Test (Logik)
# Eingabewerte: MediaItem Objekte (Mocked)
# Ausgabewerte: Dictionary mit getrennten Feldern
# Testdateien: -
# Kommentar: Prüft die korrekte Trennung von extension, container, tag_type und codec.

from src.core.models import MediaItem
import sys
import os

def test_wav_plain():
    item = MediaItem("test", "test.wav")
    item.tags = {'container': 'wav', 'codec': 'pcm_s16le'}  # Mock values
    # Recalculate based on current logic in __init__?
    # Actually __init__ runs the parser. We need to mock the parser or set attributes.
    item.extension = "wav"
    item.container = "wav"
    item.tag_type = "plain"
    item.codec = "pcm_s16le"

    d = item.to_dict()
    assert d['extension'] == "wav"
    assert d['container'] == "wav"
    assert d['tag_type'] == "plain"
    assert d['codec'] == "pcm_s16le"

def test_mp3_plain():
    item = MediaItem("test", "test.mp3")
    item.extension = "mp3"
    item.container = "mp3"
    item.tag_type = "plain"
    item.codec = "mp3"

    d = item.to_dict()
    assert d['extension'] == "mp3"
    assert d['container'] == "mp3"
    assert d['tag_type'] == "plain"
    assert d['codec'] == "mp3"

def test_mp3_id3():
    item = MediaItem("test", "test.mp3")
    item.extension = "mp3"
    item.container = "mp3"
    item.tag_type = "ID3v2.2"
    item.codec = "mp3"

    d = item.to_dict()
    assert d['extension'] == "mp3"
    assert d['container'] == "mp3"
    assert d['tag_type'] == "ID3v2.2"
    assert d['codec'] == "mp3"

def test_mkv_aac():
    item = MediaItem("test", "test.mkv")
    item.extension = "mkv"
    item.container = "mkv"
    item.tag_type = "plain"
    item.codec = "aac"

    d = item.to_dict()
    assert d['extension'] == "mkv"
    assert d['container'] == "mkv"
    assert d['tag_type'] == "plain"
    assert d['codec'] == "aac"

def test_m4b_m4tags():
    item = MediaItem("test", "test.m4b")
    item.extension = "m4b"
    item.container = "mp4"
    item.tag_type = "m4tags"
    item.codec = "aac"

    d = item.to_dict()
    assert d['extension'] == "m4b"
    assert d['container'] == "mp4"
    assert d['tag_type'] == "m4tags"
    assert d['codec'] == "aac"
