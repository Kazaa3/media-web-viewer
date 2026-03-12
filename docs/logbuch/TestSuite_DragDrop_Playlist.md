# Test Suite: Drag & Drop Playlist Item

## Ziel
Eine vollständige Test-Suite für das Drag & Drop-Verhalten in der Playlist. Es soll möglich sein, ein Item mit der Maus zu greifen, gedrückt zu halten und an eine gewünschte Position zu verschieben. Das Verhalten soll robust und nach jedem Tab-Wechsel funktionieren.

## Testfälle
1. **Startup-Test:** Initialisiere die Playlist und prüfe, ob Drag & Drop sofort funktioniert.
2. **Item-Drag:** Greife ein Item, halte es gedrückt und verschiebe es an eine neue Position.
3. **Drop-Position:** Lasse das Item an der gewünschten Nummerierung los und prüfe, ob es dort einsortiert wird.
4. **Tab-Wechsel:** Wechsle mehrfach zwischen Tabs und prüfe, ob Drag & Drop weiterhin funktioniert.
5. **Reihenfolge-Check:** Nach jedem Drag & Drop muss die Reihenfolge korrekt sein.
6. **Edge Cases:** Drag & Drop am Anfang/Ende der Liste, mit leerer oder voller Playlist.

## Test-Workflow (Pseudo-Code)
```python
# ...existing code...
def test_drag_and_drop_playlist():
    # Startup
    open_playlist_tab()
    assert drag_and_drop_enabled()

    # Drag Item
    item = get_playlist_item(2)
    drag_item(item)
    drop_item_at_position(5)
    assert playlist_order_correct()

    # Tab-Wechsel
    for _ in range(3):
        switch_tab('Player')
        switch_tab('Playlist')
        assert drag_and_drop_enabled()

    # Edge Cases
    drag_item(get_playlist_item(0))
    drop_item_at_position(len(playlist)-1)
    assert playlist_order_correct()
```

## Status
- Test-Suite definiert
- Startup-Test für Parser/Playlist muss ergänzt werden
- Drag & Drop Verhalten wird nach jedem Tab-Wechsel geprüft

---
Letzte Aktualisierung: 11. März 2026
