import os
import sys
from unittest.mock import patch
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import set_current_playlist, get_current_playlist, next_in_playlist, prev_in_playlist, jump_to_index
from parsers.format_utils import PARSER_CONFIG


def test_playlist_set_and_get():
    # Set a simple playlist of names
    res = set_current_playlist(["song1.mp3", "song2.mp3"], start_index=0, replace=True)
    assert res["status"] == "ok"
    current = get_current_playlist()
    assert current["index"] == 0
    assert len(current["items"]) == 2


@patch('db.get_all_media')
def test_next_prev_play_calls(mock_get_all):
    # Mock DB so name resolution works
    mock_get_all.return_value = [
        {"name": "song1.mp3", "path": "/tmp/song1.mp3"},
        {"name": "song2.mp3", "path": "/tmp/song2.mp3"},
    ]

    # Initialize playlist
    set_current_playlist([{"name": "song1.mp3"}, {"name": "song2.mp3"}], start_index=0, replace=True)

    # next should play song2
    res_next = next_in_playlist()
    assert res_next["status"] == "play"
    assert res_next["path"].endswith("song2.mp3")

    # prev should go back to song1
    res_prev = prev_in_playlist()
    assert res_prev["status"] == "play"
    assert res_prev["path"].endswith("song1.mp3")


def test_jump_to_index_out_of_range():
    set_current_playlist(["a", "b", "c"], start_index=0, replace=True)
    res = jump_to_index(10)
    assert res["status"] == "error"
