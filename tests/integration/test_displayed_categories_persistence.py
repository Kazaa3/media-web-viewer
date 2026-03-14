import json
import os
import sys
from pathlib import Path

import pytest

# Ensure project root is on sys.path for tests when run directly

from src.parsers import format_utils

def test_displayed_categories_save_and_load(tmp_path, monkeypatch):
    """Ensure displayed_categories is persisted and restored by save/load."""
    # Use a temporary config file path
    temp_config = tmp_path / "parser_config.json"
    monkeypatch.setattr(format_utils, "CONFIG_FILE", temp_config)

    # Ensure default in-memory value
    format_utils.PARSER_CONFIG["displayed_categories"] = ["audio"]

    # Save to temp config
    format_utils.save_parser_config()
    assert temp_config.exists()

    # Mutate in-memory config to simulate change
    format_utils.PARSER_CONFIG["displayed_categories"] = []
    assert format_utils.PARSER_CONFIG["displayed_categories"] == []

    # Load from temp config and verify it's restored
    format_utils.load_parser_config()
    assert format_utils.PARSER_CONFIG["displayed_categories"] == ["audio"]
