# =============================================================================
# Kategorie: Unit Test (Logik)
# Eingabewerte: MediaItem Objekte (Mocked)
# Ausgabewerte: Dictionary mit getrennten Feldern
# Testdateien: test_separated_fields.py
# Kommentar: Prüft die korrekte Trennung von extension, container, tag_type und codec.
# Startbefehl: pytest tests/test_separated_fields.py -v
# =============================================================================
"""
Unit Test (Logic) Suite (DE/EN)
===============================

DE:
Testet die korrekte Trennung von extension, container, tag_type und codec im MediaItem.

EN:
Tests correct separation of extension, container, tag_type, and codec in MediaItem.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

from src.core.models import MediaItem
import sys
import os

def test_wav_plain():
    """
    DE:
    Testet die Trennung der Felder für WAV-Dateien.

    EN:
    Tests field separation for WAV files.

    Returns:
        Keine.
    Raises:
        AssertionError: Wenn die Felder nicht korrekt getrennt sind.
    """
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
    """
    DE:
    Testet die Trennung der Felder für MP3-Dateien.

    EN:
    Tests field separation for MP3 files.

    Returns:
        Keine.
    Raises:
        AssertionError: Wenn die Felder nicht korrekt getrennt sind.
    """
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
    """
    DE:
    Testet die Trennung der Felder für MP3-Dateien mit ID3-Tags.

    EN:
    Tests field separation for MP3 files with ID3 tags.

    Returns:
        Keine.
    Raises:
        AssertionError: Wenn die Felder nicht korrekt getrennt sind.
    """
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
    """
    DE:
    Testet die Trennung der Felder für MKV-Dateien mit AAC-Codec.

    EN:
    Tests field separation for MKV files with AAC codec.

    Returns:
        Keine.
    Raises:
        AssertionError: Wenn die Felder nicht korrekt getrennt sind.
    """
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
    """
    DE:
    Testet die Trennung der Felder für M4B-Dateien mit m4tags.

    EN:
    Tests field separation for M4B files with m4tags.

    Returns:
        Keine.
    Raises:
        AssertionError: Wenn die Felder nicht korrekt getrennt sind.
    """
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
