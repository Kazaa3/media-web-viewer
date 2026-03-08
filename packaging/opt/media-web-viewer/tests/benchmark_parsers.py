# Kategorie: Performance Test
# Eingabewerte: Reale Medien im /media Ordner
# Ausgabewerte: Ausführungszeiten (STDOUT)
# Testdateien: /media/*
# Kommentar: Misst die Geschwindigkeit von pymediainfo, mutagen, ffmpeg etc.

from typing import Any
from parsers import filename_parser, mutagen_parser, pymediainfo_parser, ffmpeg_parser
import time
import glob
from pathlib import Path
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))
files = glob.glob(os.path.join(media_dir, '*.*'))

parser_times = {
    "filename": 0.0,
    "container": 0.0,
    "pymediainfo": 0.0,
    "ffmpeg": 0.0,
    "mutagen": 0.0
}

for f in files:
    name = os.path.basename(f)
    path_obj = Path(f)
    file_type = path_obj.suffix.lower()

    # filename parser
    t0 = time.time()
    tags_in: dict[str, Any] = {}
    tags_res = filename_parser.parse(path_obj, name, tags=tags_in)
    parser_times["filename"] += (time.time() - t0)

    # mutagen parser
    t0 = time.time()
    tags_res = mutagen_parser.parse(path_obj, file_type, {}, name)
    parser_times["mutagen"] += (time.time() - t0)

    # pymediainfo parser
    t0 = time.time()
    tags_res = pymediainfo_parser.parse(path_obj, file_type, {})
    parser_times["pymediainfo"] += (time.time() - t0)

    # ffmpeg parser
    t0 = time.time()
    tags_res = ffmpeg_parser.parse(path_obj, file_type, {})
    parser_times["ffmpeg"] += (time.time() - t0)

    # container parser
    t0 = time.time()
    tags_container: dict[str, Any] = {}
    if not tags_container.get('container'):
        tags_container['container'] = file_type[1:].lower()
        if not tags_container.get('codec'):
            tags_container['codec'] = file_type[1:].lower()
    parser_times["container"] += (time.time() - t0)

print(f"Total files: {len(files)}")
print("-" * 30)
for parser, t in parser_times.items():
    print(f"{parser:<15}: {t:.6f} seconds")
print("-" * 30)
