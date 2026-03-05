# Kategorie: UI / Types Test
# Eingabewerte: Pfade, Dateinamen, unsortierte Listen
# Ausgabewerte: Kategorien (Hörbuch, Film, etc.), Natural Sorting
# Testdateien: Keine (Mocks)
# Kommentar: Prüft die automatische Typ-Erkennung und Natural Sorting Logik.

import pytest
from pathlib import Path
from models import MediaItem
from parsers.format_utils import natural_sort_key

def test_category_audio():
    # Mocking components usually handled in extract_metadata
    item = MediaItem("song.mp3", "/media/music/song.mp3")
    assert item.category == "Audio"

def test_category_audiobook():
    # Folder naming convention
    item = MediaItem("chapter1.mp3", "/media/Hörbücher/HP1/chapter1.mp3")
    assert item.category == "Hörbuch"
    
    # Extension convention
    item = MediaItem("book.m4b", "/media/downloads/book.m4b")
    assert item.category == "Hörbuch"

def test_category_video():
    item = MediaItem("movie.mkv", "/media/movies/movie.mkv")
    assert item.category == "Film"

def test_category_series():
    item = MediaItem("ep01.mp4", "/media/series/BreakingBad/S01/ep01.mp4")
    assert item.category == "Serie"

def test_category_ebook():
    item = MediaItem("manual.epub", "/media/books/manual.epub")
    assert item.category == "E-Book"

def test_category_document():
    item = MediaItem("notes.txt", "/media/docs/notes.txt")
    assert item.category == "Dokument"

def test_natural_sort():
    titles = ["Kapitel 1", "Kapitel 21", "Kapitel 22", "Kapitel 2", "Kapitel 10"]
    sorted_titles = sorted(titles, key=natural_sort_key)
    # Expected: 1, 2, 10, 21, 22
    expected = ["Kapitel 1", "Kapitel 2", "Kapitel 10", "Kapitel 21", "Kapitel 22"]
    assert sorted_titles == expected

def test_chapter_sort_logic():
    chaps = [
        {'start': 0.0, 'title': 'Kapitel 10'},
        {'start': 0.0, 'title': 'Kapitel 2'},
        {'start': 10.0, 'title': 'Kapitel 21'},
        {'start': 5.0, 'title': 'Kapitel 1'}
    ]
    # Primary sort by start time, secondary by natural title
    # For start 0.0: Kapitel 2, then Kapitel 10
    # Then start 5.0: Kapitel 1
    # Then start 10.0: Kapitel 21
    res = sorted(chaps, key=lambda x: (x['start'], natural_sort_key(x['title'])))
    assert res[0]['title'] == 'Kapitel 2'
    assert res[1]['title'] == 'Kapitel 10'
    assert res[2]['title'] == 'Kapitel 1'
    assert res[3]['title'] == 'Kapitel 21'

def test_natural_sort_logic():
    list_to_sort = ["Kapitel 1", "Kapitel 10", "Kapitel 2", "Kapitel 21", "Kapitel 3"]
    sorted_list = sorted(list_to_sort, key=natural_sort_key)
    assert sorted_list == ["Kapitel 1", "Kapitel 2", "Kapitel 3", "Kapitel 10", "Kapitel 21"]
