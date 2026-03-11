import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import set_current_playlist, get_current_playlist, move_item_to


def test_move_item_to_basic_reposition():
    set_current_playlist(['a', 'b', 'c', 'd'], start_index=1, replace=True)
    # move 'b' (index 1) to position 0
    res = move_item_to(1, 0)
    assert res['status'] == 'ok'
    cur = get_current_playlist()
    assert [it['name'] for it in cur['items']] == ['b', 'a', 'c', 'd']
    assert cur['index'] == 0  # was current (1) -> moved to 0


def test_move_item_to_shift_current_forward_and_back():
    # Move an item ahead of current index
    set_current_playlist(['a', 'b', 'c', 'd'], start_index=2, replace=True)  # current = 2 ('c')
    res = move_item_to(1, 3)  # move 'b' from 1 to 3
    assert res['status'] == 'ok'
    cur = get_current_playlist()
    assert [it['name'] for it in cur['items']] == ['a', 'c', 'd', 'b']
    # current 'c' was at 2 -> after move it should be at 1
    assert cur['index'] == 1

    # Move an item before current index
    set_current_playlist(['a', 'b', 'c', 'd'], start_index=0, replace=True)  # current = 'a'
    res2 = move_item_to(2, 0)  # move 'c' to front
    assert res2['status'] == 'ok'
    cur2 = get_current_playlist()
    assert [it['name'] for it in cur2['items']] == ['c', 'a', 'b', 'd']
    # current 'a' was index 0 -> should now be index 1
    assert cur2['index'] == 1
