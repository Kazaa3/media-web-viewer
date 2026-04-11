import pytest
from src.core import db

def test_db_stats_loading():
    stats = db.get_stats()
    assert isinstance(stats, dict)
    assert 'total_items' in stats
    assert stats['total_items'] >= 0
    assert 'types' in stats
    assert isinstance(stats['types'], dict)
    # Performance: Simulate large DB
    # (Optional: Add more checks for integrity)

# Add more tests for GUI integration if needed
