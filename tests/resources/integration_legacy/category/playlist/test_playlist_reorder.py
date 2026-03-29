import os
import sys
from pathlib import Path

from src.core.main import (
    set_current_playlist,
    get_current_playlist,
    move_item_up,
    move_item_down,
    move_current_up,
    move_current_down,
)

def test_move_item_up_down_by_index():
    set_current_playlist(['a', 'b', 'c', 'd'], start_index=1, replace=True)
    # move index 1 ('b') up to index 0
    res = move_item_up(1)
    assert res['status'] == 'ok'
    current = get_current_playlist()
    assert current['items'][0]['name'] == 'b' or current['items'][0]['name'] == 'b'
    # now move index 2 ('c') down to index 3
    res2 = move_item_down(2)
    assert res2['status'] == 'ok'
    current2 = get_current_playlist()
    assert current2['items'][3]['name'] == 'c'

def test_move_current_up_down():
    set_current_playlist(['one', 'two', 'three'], start_index=2, replace=True)
    # current index is 2 (three)
    res = move_current_up()
    assert res['status'] == 'ok'
    cur = get_current_playlist()
    # 'three' should now be at index 1
    assert cur['index'] == 1

    res2 = move_current_down()
    assert res2['status'] == 'ok'
    cur2 = get_current_playlist()
    assert cur2['index'] == 2
