import pytest
from pathlib import Path
from models import MediaItem

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

def test_natural_sort_logic():
    from parsers.format_utils import natural_sort_key
    list_to_sort = ["Kapitel 1", "Kapitel 10", "Kapitel 2", "Kapitel 21", "Kapitel 3"]
    sorted_list = sorted(list_to_sort, key=natural_sort_key)
    assert sorted_list == ["Kapitel 1", "Kapitel 2", "Kapitel 3", "Kapitel 10", "Kapitel 21"]
