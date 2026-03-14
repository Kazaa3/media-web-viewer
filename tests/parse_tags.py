#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Mutagen Tag Dump Test
# Eingabewerte: media/*.flac, media/*.mp3, media/*.m4a
# Ausgabewerte: Alle Mutagen-Tags für FLAC, MP3, M4A (key: value pairs)
# Testdateien: media/*.flac, media/*.mp3, media/*.m4a
# Kommentar: Dumpt alle Mutagen-Tags für FLAC, MP3 und M4A Dateien (diagnostischer Tag-Dump).
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
import glob

print("FLAC TAGS")
for f in glob.glob('media/*.flac'):
    try:
        audio_flac = FLAC(f)
        print(f"--- {f} ---")
        for k, v in audio_flac.items():
            print(f"{k}: {v}")
    except BaseException:
        pass

print("\nMP3 TAGS")
for f in glob.glob('media/*.mp3'):
    try:
        audio_mp3 = MP3(f)
        print(f"--- {f} ---")
        for k_m3, v_m3 in audio_mp3.items():
            if k_m3 == 'APIC:' or k_m3.startswith('APIC'):
                continue  # skip huge binary art
            print(f"{k_m3}: {v_m3}")
    except BaseException:
        pass

print("\nM4A TAGS")
for f in glob.glob('media/*.m4a') + glob.glob('media/*.alac'):
    try:
        audio_mp4 = MP4(f)
        print(f"--- {f} ---")
        for k_m4, v_m4 in audio_mp4.items():
            if k_m4 == 'covr':
                continue  # skip art
            print(f"{k_m4}: {v_m4}")
    except BaseException:
        pass
