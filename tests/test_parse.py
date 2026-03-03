import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import MediaItem
from pathlib import Path
import glob
import os

media_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))
for f in glob.glob(os.path.join(media_dir, '*.*')):
    name = os.path.basename(f)
    m = MediaItem(name, Path(f))
    print(name, " | SRT: ", m.tags.get('samplerate', 'MISSING'), " | BRT: ", m.tags.get('bitrate', 'MISSING'), " | SIZ: ", m.tags.get('filesize', 'MISSING'))
