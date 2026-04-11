# Kategorie: Logic / Sorting Test
# Eingabewerte: Listen von Strings ("1", "21", "2", "Kapitel 1")
# Ausgabewerte: Richtig sortierte Listen (1, 2, 21)
# Testdateien: Keine (Mocks)
# Kommentar: Verifiziert das Natural Sorting, um das Problem der 1, 21, 22, 2 Sortierung zu lösen.

from src.parsers.format_utils import natural_sort_key

def test_natural_sort_numeric_strings():
    # User case: "1, 21, 22, 2" -> should be 1, 2, 21, 22
    titles = ["1", "21", "22", "2"]
    res = sorted(titles, key=natural_sort_key)
    assert res == ["1", "2", "21", "22"]

def test_natural_sort_mixed_strings():
    titles = ["Kapitel 1", "Kapitel 22", "Kapitel 2", "Kapitel 10"]
    res = sorted(titles, key=natural_sort_key)
    assert res == ["Kapitel 1", "Kapitel 2", "Kapitel 10", "Kapitel 22"]

def test_chronological_plus_natural_sort():
    # Primary sort by time, secondary by name
    chapters = [
        {'start': 100.0, 'title': 'Kapitel 2'},
        {'start': 0.0, 'title': 'Kapitel 10'},
        {'start': 0.0, 'title': 'Kapitel 1'},
        {'start': 50.0, 'title': 'Kapitel 5'}
    ]
    # At 0.0, Kapitel 1 should come before Kapitel 10
    # Then 50.0 (Kapitel 5), then 100.0 (Kapitel 2)
    res = sorted(chapters, key=lambda x: (x.get('start', 0.0), natural_sort_key(x.get('title', ''))))
    assert res[0]['title'] == 'Kapitel 1'
    assert res[1]['title'] == 'Kapitel 10'
    assert res[2]['title'] == 'Kapitel 5'
    assert res[3]['title'] == 'Kapitel 2'

def test_complex_numbering():
    titles = ["Track 1.1", "Track 1.10", "Track 1.2"]
    res = sorted(titles, key=natural_sort_key)
    assert res == ["Track 1.1", "Track 1.2", "Track 1.10"]
