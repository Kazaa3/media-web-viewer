# Kategorie: Unit Test
# Eingabewerte: Pfad zur FLAC / MP3
# Ausgabewerte: Pymediainfo Ausgaben
# Testdateien: Keine (Mock / Dummy)
# Kommentar: Prüft BitDepth extraction.

from pymediainfo import MediaInfo
import os


def check_file(path):
    if not os.path.exists(path):
        print(f"File not found, skipping bits test: {path}")
        return
    info = MediaInfo.parse(path)
    for track in info.tracks:
        if track.track_type == 'Audio':
            bit_depth = getattr(track, 'bit_depth', None)     # 16, 24
            format_name = getattr(track, 'format', None)      # FLAC
            print(f"{path}: BitDepth = {bit_depth}, Format = {format_name}")


# check_file("media/01 - Einfach & Leicht.mp3")
# check_file("media/02 We the People….flac")
# check_file("media/2007 - M.A.S.K/03. The Secret.m4a")
# ALAC
check_file("media/20-The Emerald Abyss.wav")
