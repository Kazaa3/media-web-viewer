#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Tag Type & Album Art Analysis
# Eingabewerte: media/*.flac, media/*.mp3, media/*.m4a
# Ausgabewerte: Tag-Type (ID3v2.3, Vorbis, MP4), Album-Art Status, Dateigröße
# Testdateien: media/*.flac, media/*.mp3, media/*.m4a
# Kommentar: Analysiert Tag-Types und Album-Art-Präsenz für FLAC/MP3/M4A (APIC, pictures, covr).
import os
import glob
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

def check(f, Type):
    try:
        audio = Type(f)
        size_mb = os.path.getsize(f) / (1024 * 1024)
        tag_type = type(audio.tags).__name__ if audio.tags else "None"

        has_art = False
        if isinstance(audio, MP3):
            has_art = any(k.startswith('APIC') for k in audio.keys())
        elif isinstance(audio, FLAC):
            has_art = len(audio.pictures) > 0
        elif isinstance(audio, MP4):
            has_art = 'covr' in audio.keys()

        print(f"{os.path.basename(f)} | Size: {size_mb:.2f} MB | Tags: {tag_type} | Art: {has_art}")
    except Exception as e:
        print(e)

for f in glob.glob('media/*.flac')[:1]:
    check(f, FLAC)
for f in glob.glob('media/*.mp3')[:1]:
    check(f, MP3)
for f in glob.glob('media/*.m4a')[:1]:
    check(f, MP4)
