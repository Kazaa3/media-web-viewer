# Kategorie: Integration Test
# Eingabewerte: Echte Mediendateien aus ./media
# Ausgabewerte: Metadaten-Dicts (Lightweight vs. Full)
# Testdateien: /media/*
# Kommentar: Vergleicht die Performance und Informationstiefe zwischen "Lightweight" und "Full" Parser-Modi.

from src.parsers import media_parser
import sys
import os

def test_full_mode():
    media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..', 'media'))
    # Try testing on a known file, just list directory to find one
    files = os.listdir(media_dir)
    audio_files = [f for f in files if f.endswith(('.mp3', '.flac', '.m4b', '.mkv', '.m4a'))]
    if not audio_files:
        print("No audio files found in media dir to test.")
        return

    test_file = os.path.join(media_dir, audio_files[0])

    print(f"Testing on {test_file}")

    print("\n--- Testing Lightweight Mode ---")
    duration, tags_lw = media_parser.extract_metadata(test_file, audio_files[0], mode='lightweight')
    print(f"Tags extracted: {len(tags_lw.keys())}")
    print(f"Has full_tags: {'full_tags' in tags_lw}")

    print("\n--- Testing Full Mode ---")
    duration, tags_full = media_parser.extract_metadata(test_file, audio_files[0], mode='full')
    print(f"Tags extracted: {len(tags_full.keys())}")
    print(f"Has full_tags: {'full_tags' in tags_full}")
    if 'full_tags' in tags_full:
        print(f"Number of extended meta items in full_tags: {len(tags_full['full_tags'].keys())}")

    if 'chapters' in tags_full:
        print(f"Found {len(tags_full['chapters'])} chapters.")

test_full_mode()
