import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(os.getcwd())

from src.parsers import media_parser

test_cases = [
    "The Matrix (1999) [4K] - br",
    "Inception (2010)",
    "Blade Runner 2049 [Director's Cut] - bd",
    "Star Wars - A New Hope (1977)"
]

for name in test_cases:
    print(f"\nParsing: {name}")
    # Simulate a path that doesn't exist (directory or missing)
    path = Path("/tmp/non_existent_media") / name
    tags, _ = media_parser.extract_metadata(path, name)
    print(f"  Title:  {tags.get('title')}")
    print(f"  Year:   {tags.get('year')}")
    print(f"  Artist: {tags.get('artist')}")
    print(f"  Season/Episode: {tags.get('season')}/{tags.get('episode')}")

