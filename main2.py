import eel
import os
import json
from pathlib import Path
import subprocess
import re
import bottle
import mimetypes
import uuid

# Audio-Tags
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp4 import MP4
from mutagen.oggopus import OggOpus
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen.asf import ASF

MEDIA_DIR = "./media"

class MediaItem:
    def __init__(self, name, path):
        self.name = name
        self.path = Path(path)
        self.duration = self._get_duration()
        self.type = self.path.suffix.lower()
        self.tags = self._get_tags()

    def _get_duration(self):
        try:
            if self.type == '.mp3': audio = MP3(self.path); return int(audio.info.length)
            elif self.type == '.flac': audio = FLAC(self.path); return int(audio.info.length)
            elif self.type == '.ogg': audio = OggVorbis(self.path); return int(audio.info.length)
            elif self.type in {'.m4a', '.alac', '.m4b'}: audio = MP4(self.path); return int(audio.info.length)
            elif self.type == '.opus': audio = OggOpus(self.path); return int(audio.info.length)
            elif self.type == '.wav': audio = WAVE(self.path); return int(audio.info.length)
            elif self.type == '.aac': audio = AAC(self.path); return int(audio.info.length)
            elif self.type == '.wma': audio = ASF(self.path); return int(audio.info.length)
        except: pass
        
        # FFmpeg Fallback
        try:
            cmd = ["ffmpeg", "-i", self.path.as_posix()]
            output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
            dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", output)
            if dur_match:
                h, m, s = map(float, dur_match.groups())
                return int(h * 3600 + m * 60 + s)
        except: pass
        return 0

    def _get_tags(self):
        tags = {'artist': 'Unbekannt', 'title': self.name, 'year': '', 'genre': '', 'track': '', 
                'totaltracks': '', 'album': '', 'albumartist': '', 'disc': '', 'bitrate': '', 
                'samplerate': '', 'bitdepth': '', 'codec': '', 'filesize': '', 'tagtype': 'None', 'has_art': 'No'}
        
        tags['filesize'] = f"{self.path.stat().st_size / (1024*1024):.2f} MB"
        
        # Filename fallback
        if " - " in self.name:
            parts = self.name.split(" - ", 1)
            tags['artist'] = parts[0].strip()
            tags['title'] = parts[1].rsplit(".", 1)[0].strip()
        
        def safe_get(audio_obj, key, default=''):
            val = audio_obj.get(key)
            if not val: return default
            if isinstance(val, list) and len(val): return str(val[0])
            return str(val)
        
        audio_for_info = None
        try:
            if self.type == '.flac':
                audio = FLAC(self.path); audio_for_info = audio
                tags.update({k: safe_get(audio, k.upper()) for k in ['artist','title','year','genre','track','totaltracks','album','albumartist','disc']})
                tags['codec'] = 'FLAC'
                if hasattr(audio.info, 'bits_per_sample') and audio.info.bits_per_sample:
                    tags['bitdepth'] = f"{audio.info.bits_per_sample} Bit"
                    
            elif self.type == '.mp3':
                audio = MP3(self.path); audio_for_info = audio
                tags.update({
                    'artist': safe_get(audio, 'TPE1'),
                    'title': safe_get(audio, 'TIT2'),
                    'year': safe_get(audio, ['TDRC','TYER']),
                    'genre': safe_get(audio, 'TCON'),
                    'album': safe_get(audio, 'TALB'),
                    'albumartist': safe_get(audio, 'TPE2'),
                    'track': safe_get(audio, 'TRCK'),
                    'codec': 'MP3'
                })
                
            elif self.type in {'.m4a', '.alac', '.m4b'}:
                audio = MP4(self.path); audio_for_info = audio
                tags.update({
                    'artist': safe_get(audio, '\xa9ART'),
                    'title': safe_get(audio, '\xa9nam'),
                    'year': safe_get(audio, '\xa9day'),
                    'genre': safe_get(audio, '\xa9gen'),
                    'album': safe_get(audio, '\xa9alb'),
                    'albumartist': safe_get(audio, 'aART'),
                    'codec': 'M4B' if self.type == '.m4b' else getattr(audio.info, 'codec', self.type[1:].upper())
                })
                trkn = audio.get('trkn', [])
                if trkn and isinstance(trkn[0], (list, tuple)) and len(trkn[0]) > 0:
                    tags['track'], tags['totaltracks'] = str(trkn[0][0]), str(trkn[0][1]) if len(trkn[0]) > 1 else ''
            
            elif self.type in {'.ogg', '.opus', '.wav', '.aac', '.wma'}:
                constructors = {'.ogg': OggVorbis, '.opus': OggOpus, '.wav': WAVE, '.aac': AAC, '.wma': ASF}
                audio = constructors[self.type](self.path); audio_for_info = audio
                tags.update({k: safe_get(audio, k.lower()) for k in ['artist','title','year','genre','album','albumartist','track','disc']})
                tags['codec'] = self.type[1:].upper()
            
            # Stream info
            if audio_for_info and hasattr(audio_for_info, 'info'):
                info = audio_for_info.info
                if hasattr(info, 'bitrate') and info.bitrate: tags['bitrate'] = f"{int(info.bitrate/1000)} kbps"
                if hasattr(info, 'sample_rate') and info.sample_rate: tags['samplerate'] = f"{round(info.sample_rate/1000,1)} kHz"
                if hasattr(info, 'bits_per_sample') and info.bits_per_sample > 0: tags['bitdepth'] = f"{info.bits_per_sample} Bit"
            
            tags['tagtype'] = type(audio_for_info.tags).__name__ if audio_for_info and audio_for_info.tags else 'None'
            tags['has_art'] = 'Yes' if (
                (self.type == '.mp3' and any(k.startswith('APIC') for k in audio_for_info.keys())) or
                (self.type == '.flac' and len(audio_for_info.pictures)) or
                (self.type in {'.m4a','.alac','.m4b'} and 'covr' in audio_for_info)
            ) else 'No'
            
        except: pass
        
        # FFmpeg Fallback (dein Code hier - verkürzt)
        if not tags['samplerate'] or not tags['bitrate']:
            try:
                cmd = ["ffmpeg", "-i", self.path.as_posix()]
                output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
                stream_match = re.search(r"Stream #.*?: Audio:\s*([^,]+),\s*(\d+)\s*Hz", output)
                if stream_match:
                    tags['codec'] = stream_match.group(1).split()[0].upper()
                    tags['samplerate'] = f"{int(stream_match.group(2))/1000:.1f} kHz"
                bit_match = re.search(r"bitrate:\s*(\d+)\s*kb/s", output)
                if bit_match: tags['bitrate'] = f"{bit_match.group(1)} kbps"
            except: pass
        
        if not tags['bitdepth'] and tags['codec'] in ['MP3','AAC']: tags['bitdepth'] = '-- Bit'
        return tags

    def to_dict(self):
        h, rem = divmod(self.duration, 3600); m, s = divmod(rem, 60)
        dur_str = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
        return {'name': self.name, 'path': self.path.as_posix(), 'duration': dur_str, 
                'tags': self.tags, 'type': self.type[1:]}

# Bottle Routes
@bottle.hook('before_request')
def log_request():
    with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
        f.write(f"REQ: {bottle.request.url}\n")

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    if filepath.endswith('.flac_transcoded'): filepath = filepath[:-16]
    full_path = os.path.join(MEDIA_DIR, filepath)
    if not os.path.exists(full_path): return bottle.HTTPError(404)
    
    mime_type, _ = mimetypes.guess_type(filepath)
    if filepath.endswith(('.alac', '.m4a', '.m4b')):
        cache_dir = os.path.join(MEDIA_DIR, '.cache')
        os.makedirs(cache_dir, exist_ok=True)
        cache_filename = Path(filepath).stem.replace('/', '_') + '.flac'
        cache_path = os.path.join(cache_dir, cache_filename)
        if not os.path.exists(cache_path):
            tmp_path = cache_path + f'.{uuid.uuid4().hex[:6]}.tmp'
            subprocess.run(['ffmpeg', '-y', '-i', full_path, '-vn', '-f', 'flac', tmp_path], 
                          check=True, capture_output=True)
            os.replace(tmp_path, cache_path)
        return bottle.static_file(cache_filename, root=cache_dir, mimetype='audio/flac')
    return bottle.static_file(filepath, root=MEDIA_DIR, mimetype=mime_type or 'application/octet-stream')

@bottle.route('/cover/<filepath:path>')
def serve_cover(filepath):
    full_path = os.path.join(MEDIA_DIR, filepath)
    if not os.path.exists(full_path): return bottle.HTTPError(404, "No cover")
    try:
        p = Path(full_path)
        if p.suffix == '.mp3':
            audio = MP3(full_path)
            for tag in audio.tags.values():
                if tag.FrameID == 'APIC': return tag.data
        elif p.suffix == '.flac':
            audio = FLAC(full_path)
            if audio.pictures: return audio.pictures[0].data
        elif p.suffix in {'.m4a', '.alac', '.m4b'}:
            audio = MP4(full_path)
            if 'covr' in audio and audio['covr']: return bytes(audio['covr'][0])
    except: pass
    return bottle.HTTPError(404, "No cover")

@eel.expose
def scan_media():
    if not os.path.exists(MEDIA_DIR): os.makedirs(MEDIA_DIR); return {"error": "Ordner erstellt"}
    media = []
    suffixes = {'.mp3', '.flac', '.ogg', '.wav', '.m4a', '.alac', '.m4b', '.opus', '.aac', '.wma'}
    for f in Path(MEDIA_DIR).iterdir():
        if f.is_file() and f.suffix.lower() in suffixes:
            item = MediaItem(f.name, f)
            media.append(item.to_dict())
    return {"media": media}

@eel.expose
def play_media(path): return {"status": "play", "path": path}

if __name__ == "__main__":
    eel.init("web")
    eel.start('app.html', size=(1200, 800), port=8000, app=bottle.default_app())
