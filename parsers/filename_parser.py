import os

def parse(path, filename):
    tags = {
        'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
        'codec': '', 'size': '', 'tagtype': '', 'container': '',
        'has_art': 'No', 'title': '', 'artist': '', 'album': '',
        'date': '', 'genre': '', 'track': '', 'totaltracks': '',
        'disc': '', 'totaldiscs': ''
    }
    
    try:
        tags['size'] = f"{os.path.getsize(path) / (1024 * 1024):.2f} MB"
    except Exception:
        pass
        
    if " - " in filename:
        parts = filename.split(" - ", 1)
        tags['artist'] = parts[0].strip()
        tags['title'] = parts[1].rsplit(".", 1)[0].strip() if "." in parts[1] else parts[1].strip()
    else:
        tags['title'] = filename.rsplit(".", 1)[0] if "." in filename else filename
        
    return tags
