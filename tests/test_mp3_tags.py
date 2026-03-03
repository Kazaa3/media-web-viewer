from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

try:
    audio = MP3('media/sample.mp3')
    print("MP3 Artist:", audio.get('TPE1'))
    print("MP3 Year:", type(audio.get('TDRC')))
    
    # Check what kind of object they are
    art = audio.get('TPE1')
    if art:
        print("TPE1 [0]:", art[0])
except Exception as e:
    print(e)
