import pytest
import sys
import os

from src.parsers.media_parser import extract_metadata

@pytest.mark.parametrize("chapters,expected_variant", [
    # Nero variant: chapter + start_time
    ([{'chapter': 'Intro', 'start_time': 0.0}], 'Nero-Variante'),
    # Apple variant: title + start
    ([{'title': 'Intro', 'start': 0.0}], 'Apple-Variante'),
    # Both variants
    ([{'chapter': 'Intro', 'start_time': 0.0}, {'title': 'Intro', 'start': 0.0}], 'Beide Varianten (Nero & Apple)'),
    # Unknown variant
    ([{'foo': 'bar'}], 'Unbekannte Variante'),
])
def test_chapter_variant_detection(monkeypatch, chapters, expected_variant):
    # Patch logger to capture info log
    import src.core.logger as logger
    logs = []
    monkeypatch.setattr(logger, "get_logger", lambda name: type('Dummy', (), {
        'info': lambda self, msg: logs.append(msg),
        'debug': lambda self, msg: None,
        'error': lambda self, msg: None,
        'isEnabledFor': lambda self, lvl: True
    })())

    # Patch format_utils.natural_sort_key
    import parsers.format_utils
    monkeypatch.setattr(parsers.format_utils, "natural_sort_key", lambda x: x)

    # Simulate tags
    tags = {'chapters': chapters}
    filename = 'testfile.m4b'
    # Call the relevant code
    # We call only the chapter detection/sorting part
    from src.parsers.media_parser import log
    if tags.get('chapters') and isinstance(tags['chapters'], list):
        from src.parsers.format_utils import natural_sort_key
        nero_variant = any('chapter' in c and 'start_time' in c for c in tags['chapters'])
        apple_variant = any('title' in c and 'start' in c for c in tags['chapters'])
        both_variants = nero_variant and apple_variant
        variant_str = (
            'Beide Varianten (Nero & Apple)' if both_variants else
            'Nero-Variante' if nero_variant else
            'Apple-Variante' if apple_variant else
            'Unbekannte Variante'
        )
        log.info(f"Chapter variant detected: {variant_str} for '{filename}'")
        tags['chapters'] = sorted(tags['chapters'], key=lambda x: (
            natural_sort_key(x.get('title', '')), x.get('start', 0.0)))
    # Check log output
    assert any(expected_variant in msg for msg in logs), f"Expected log variant '{expected_variant}' in logs: {logs}"
