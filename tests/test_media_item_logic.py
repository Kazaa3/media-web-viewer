# Kategorie: Unit Test (Logik)
# Eingabewerte: MediaItem Objekte
# Ausgabewerte: Dictionary / JSON Kompatibel
# Testdateien: test.mp3, test.alac, test.wma (Mocks)
# Kommentar: Prüft ob die Datenstrukturen und Transcoding-Parameter sauber abgebildet werden.

from models import MediaItem
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_media_item_to_dict():
    # Mocking a path that might not exist but the class should handle it
    # We use a real file if possible, but for unit test we can mock tags
    item = MediaItem("test", "test.mp3")

    # Manually set attributes to avoid triggerring full parser during unit test if possible
    # or just test the to_dict logic with what it currently has
    item.duration = 3661  # 1h 1m 1s
    item.tags = {
        'title': 'Test Title',
        'artist': 'Test Artist',
        'codec': 'MP3'
    }
    item.type = '.mp3'

    d = item.to_dict()
    assert d['name'] == "test"
    assert d['duration'] == "1:01:01"
    assert d['tags']['title'] == "Test Title"
    assert d['type'] == "audio"
    assert not d['is_transcoded']


def test_media_item_transcoding_logic():
    item = MediaItem("test", "test.alac")
    item.duration = 60
    item.tags = {'codec': 'ALAC'}
    item.type = '.alac'

    d = item.to_dict()
    assert d['is_transcoded']
    assert d['transcoded_format'] == 'FLAC'

    item_wma = MediaItem("test", "test.wma")
    item_wma.duration = 60
    item_wma.tags = {'codec': 'WMA'}
    item_wma.type = '.wma'

    d_wma = item_wma.to_dict()
    assert d_wma['is_transcoded']
    assert d_wma['transcoded_format'] == 'OGG'
