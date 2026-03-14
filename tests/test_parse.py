# Kategorie: Parser Benchmark
# Eingabewerte: Verzeichnis /media
# Ausgabewerte: Zeitmessung pro Parser (filename, mutagen, pymediainfo, ffmpeg)
# Testdateien: Alle Dateien in /media
# Kommentar: Misst und vergleicht die Ausführungszeit der verschiedenen Metadaten-Parser.

from parsers import filename_parser, mutagen_parser, pymediainfo_parser, ffmpeg_parser
import time
from typing import Any
import glob
from pathlib import Path
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))


def benchmark_parsers():
    files = glob.glob(os.path.join(media_dir, '*.*'))

    total_times = {
        "filename": 0.0,
        "mutagen": 0.0,
        "pymediainfo": 0.0,
        "ffmpeg": 0.0,
        "container": 0.0
    }
    file_count = 0

    for f in files:
        name = os.path.basename(f)
        path_obj = Path(f)
        file_type = path_obj.suffix.lower()
        file_count += 1

        print(f"File: {name}")

        # filename parser
        t0 = time.time()
        filename_parser.parse(path_obj, name, tags={})
        t_filename = time.time() - t0
        total_times["filename"] += t_filename
        print(f"  filename    : {t_filename:.4f} sec")

        # mutagen parser
        t0 = time.time()
        mutagen_parser.parse(path_obj, file_type, {}, name)
        t_mutagen = time.time() - t0
        total_times["mutagen"] += t_mutagen
        print(f"  mutagen     : {t_mutagen:.4f} sec")

        # pymediainfo parser
        t0 = time.time()
        pymediainfo_parser.parse(path_obj, file_type, {})
        t_pymediainfo = time.time() - t0
        total_times["pymediainfo"] += t_pymediainfo
        print(f"  pymediainfo : {t_pymediainfo:.4f} sec")

        # ffmpeg parser
        t0 = time.time()
        ffmpeg_parser.parse(path_obj, file_type, {})
        t_ffmpeg = time.time() - t0
        total_times["ffmpeg"] += t_ffmpeg
        print(f"  ffmpeg      : {t_ffmpeg:.4f} sec")

        # container parser
        t0 = time.time()
        tags_container: dict[str, Any] = {}
        if not tags_container.get('container'):
            tags_container['container'] = file_type[1:].lower()
            if not tags_container.get('codec'):
                tags_container['codec'] = file_type[1:].lower()
        t_container = time.time() - t0
        total_times["container"] += t_container
        print(f"  container   : {t_container:.4f} sec")

        print("-" * 40)

    print("\n" + "=" * 40)
    print(f"TOTAL TIMES ({file_count} files):")
    for parser, t in total_times.items():
        print(f"  {parser:<15}: {t:.4f} sec")
    print("=" * 40)


if __name__ == "__main__":
    benchmark_parsers()
