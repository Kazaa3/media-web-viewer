import sys
from pymediainfo import MediaInfo

def check_file(path):
    info = MediaInfo.parse(path)
    for t in info.tracks:
        if t.track_type == "Audio":
            print(f"{path}: BitDepth = {t.bit_depth}, Format = {t.format}")

check_file("media/01 - Einfach & Leicht.mp3")
check_file("media/02 We the People….flac")
check_file("media/02 We the People….m4a")  # ALAC
check_file("media/20-The Emerald Abyss.wav")
