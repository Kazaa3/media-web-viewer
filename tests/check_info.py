import glob
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

def dump_info(files, Type):
    for f in files:
        audio = Type(f)
        print(f"--- {f} ---")
        for k in dir(audio.info):
            if not k.startswith('_'):
                print(f"{k}: {getattr(audio.info, k)}")

dump_info(glob.glob('media/*.flac')[:1], FLAC)
dump_info(glob.glob('media/*.mp3')[:1], MP3)
dump_info(glob.glob('media/*.m4a')[:1], MP4)
