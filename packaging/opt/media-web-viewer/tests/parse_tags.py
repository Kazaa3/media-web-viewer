from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import glob

print("FLAC TAGS")
for f in glob.glob('media/*.flac'):
    try:
        audio = FLAC(f)
        print(f"--- {f} ---")
        for k, v in audio.items():
            print(f"{k}: {v}")
    except BaseException:
        pass

print("\nMP3 TAGS")
for f in glob.glob('media/*.mp3'):
    try:
        audio = MP3(f)
        print(f"--- {f} ---")
        for k, v in audio.items():
            if k == 'APIC:' or k.startswith('APIC'):
                continue  # skip huge binary art
            print(f"{k}: {v}")
    except BaseException:
        pass

print("\nM4A TAGS")
for f in glob.glob('media/*.m4a') + glob.glob('media/*.alac'):
    try:
        audio = MP4(f)
        print(f"--- {f} ---")
        for k, v in audio.items():
            if k == 'covr':
                continue  # skip art
            print(f"{k}: {v}")
    except BaseException:
        pass
