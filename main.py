# Todo
## Funktionen
# File-Handling
# - Medien scannen (Ordner durchsuchen, Metadaten extrahieren)
# - Weitere Funktionen hinzufügen, z.B. zum Abspielen von Medien, Verwalten von Wiedergabelisten, etc.
##### GUI
# - Hauptfenster mit Navigation (Medienbibliothek, Wiedergabelisten, Einstellungen)
# - Medienbibliothek (Datei-Explorer, Drag & Drop)
##### Datenbank
# Wechsel zu:  pywebview oder Flask
# SQLite über sqlite3 oder SQLAlchemy
############ Datenmodel
# Datenstruktur für Medien
# class MediaItem(name, path, type, duration, tags, ...)


#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import os
from pathlib import Path
import subprocess
import re  # For MKV parsing


# Audio-Tag-Bibliothek
from mutagen.mp3 import MP3  # Für MP3-Dauer
from mutagen.flac import FLAC  # Für FLAC-Dauer
from mutagen.oggvorbis import OggVorbis  # Für OGG
from mutagen.mp4 import MP4  # Für ALAC/M4A
from mutagen.oggopus import OggOpus
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen.asf import ASF # Für WMA

from mutagen.id3 import ID3

#Video-Tag-Bibliothek
#mkvinfo

#M4B
from mutagen.mp4 import MP4

# weitere Container
# mp4, avi, mov, mkv, webm, flv, wmv, mpg, mpeg, m4v, 3gp, 3g2, ogv, ogg, mts, m2ts

#Dokumente
# pdf, doc, docx, txt, md, html, htm
# epub, mobi, azw, fb2

# sonstige
# zip, rar, 7z, tar, gz, bz2, xz
# exe, dmg, deb, rpm, apk
# iso, img, vhd, vmdk, vdi
# bat, sh, ps1, cmd
# py, js, html, css, php, java, c, cpp, h, hpp, cs, rb, go, rs, swift, kt,kts,kts


class MediaItem:
    def __init__(self, name, path):
        self.name = name
        self.path = Path(path)
        self.type = self.path.suffix.lower()
        self.duration = self._get_duration()
        self.tags = self._get_tags()

    def _get_duration(self):
        """Extrahiert Dauer in Sekunden (mit mutagen)."""
        try:
            if self.type == '.mp3':
                audio = MP3(self.path)
                return int(audio.info.length)
            elif self.type == '.flac':
                audio = FLAC(self.path)
                return int(audio.info.length)
            elif self.type == '.ogg':
                audio = OggVorbis(self.path)
                return int(audio.info.length)
            elif self.type in {'.m4a', '.alac', '.m4b'}:
                audio = MP4(self.path)
                return int(audio.info.length)
            elif self.type == '.opus':
                audio = OggOpus(self.path)
                return int(audio.info.length) 
            elif self.type == '.wav':
                audio = WAVE(self.path)
                return int(audio.info.length)  
        except:
            pass
            
        # FFmpeg fallback if mutagen fails
        try:
            import subprocess, re
            cmd = ["ffmpeg", "-i", self.path.as_posix()]
            output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
            dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", output)
            if dur_match:
                hours = int(dur_match.group(1))
                minutes = int(dur_match.group(2))
                seconds = float(dur_match.group(3))
                return int(hours * 3600 + minutes * 60 + seconds)
        except:
            pass
            
        return 0

    def _get_tags(self):
        """Extrahiert umfassende Metadaten (Jahr, Genre, Album, Stream Info) (mutagen)."""
        tags = {
            'duration': '', 'bitrate': '', 'samplerate': '', 'bitdepth': '',
            'codec': '', 'size': '', 'tagtype': '', 'container': '',
            'has_art': 'No', 'title': '', 'artist': '', 'album': '',
            'date': '', 'genre': '', 'track': '', 'totaltracks': '',
            'disc': '', 'totaldiscs': ''
        }
        
        try:
            import os
            tags['size'] = f"{os.path.getsize(self.path) / (1024 * 1024):.2f} MB"
        except:
            pass
            
        # Try finding Artist / Title from the filename string as fallback
        if " - " in self.name:
            parts = self.name.split(" - ", 1)
            tags['artist'] = parts[0].strip()
            tags['title'] = parts[1].rsplit(".", 1)[0].strip() if "." in parts[1] else parts[1].strip()
        else:
            tags['title'] = self.name.rsplit(".", 1)[0] if "." in self.name else self.name
        
        def safe_get(audio_obj, key, default=''):
            val = audio_obj.get(key)
            if not val:
                return default
            if isinstance(val, list) and len(val) > 0:
                return str(val[0])
            return str(val)

        def format_samplerate(hz):
            try:
                hz = float(hz)
                khz = hz / 1000
                return f"{int(khz)} kHz" if khz.is_integer() else f"{khz:g} kHz"
            except:
                return ""

        try:
            # Info stream info fallback block 
            audio_for_info = None
            
            if self.type == '.flac':
                audio = FLAC(self.path)
                audio_for_info = audio
                tags['artist'] = safe_get(audio, 'ARTIST', default='Unbekannt')
                tags['title'] = safe_get(audio, 'TITLE', default=self.name)
                tags['year'] = safe_get(audio, 'DATE')
                tags['genre'] = safe_get(audio, 'GENRE')
                tags['track'] = safe_get(audio, 'TRACKNUMBER')
                tags['totaltracks'] = safe_get(audio, 'TRACKTOTAL') or safe_get(audio, 'TOTALTRACKS')
                tags['album'] = safe_get(audio, 'ALBUM')
                tags['albumartist'] = safe_get(audio, 'ALBUMARTIST')
                tags['disc'] = safe_get(audio, 'DISCNUMBER')
                tags['codec'] = 'FLAC'
                if hasattr(audio.info, 'bits_per_sample') and audio.info.bits_per_sample:
                    tags['bitdepth'] = f"{audio.info.bits_per_sample} Bit"
                
            elif self.type == '.mp3':
                audio = MP3(self.path)
                audio_for_info = audio
                art = audio.get('TPE1')
                tit = audio.get('TIT2')
                yr = audio.get('TDRC') or audio.get('TYER')
                gn = audio.get('TCON')
                tr = audio.get('TRCK')
                alb = audio.get('TALB')
                aart = audio.get('TPE2')
                dsc = audio.get('TPOS')
                
                tags['artist'] = str(art.text[0]) if art and hasattr(art, 'text') else (str(art[0]) if art else 'Unbekannt')
                tags['title'] = str(tit.text[0]) if tit and hasattr(tit, 'text') else (str(tit[0]) if tit else self.name)
                tags['year'] = str(yr.text[0]) if yr and hasattr(yr, 'text') else (str(yr) if yr else '')
                tags['genre'] = str(gn.text[0]) if gn and hasattr(gn, 'text') else (str(gn) if gn else '')
                tags['album'] = str(alb.text[0]) if alb and hasattr(alb, 'text') else (str(alb[0]) if alb else '')
                tags['albumartist'] = str(aart.text[0]) if aart and hasattr(aart, 'text') else (str(aart[0]) if aart else '')
                tags['disc'] = str(dsc.text[0]).split('/')[0] if dsc and hasattr(dsc, 'text') else (str(dsc) if dsc else '')
                
                tr_val = str(tr.text[0]) if tr and hasattr(tr, 'text') else (str(tr) if tr else '')
                if '/' in tr_val:
                    tags['track'] = tr_val.split('/')[0]
                    tags['totaltracks'] = tr_val.split('/')[1]
                else:
                    tags['track'] = tr_val
                    
                tags['codec'] = 'MP3'
                
            elif self.type in {'.m4a', '.alac', '.m4b'}:
                audio = MP4(self.path)
                audio_for_info = audio
                tags['artist'] = safe_get(audio, '\xa9ART', default='Unbekannt')
                tags['title'] = safe_get(audio, '\xa9nam', default=self.name)
                tags['year'] = safe_get(audio, '\xa9day')
                tags['genre'] = safe_get(audio, '\xa9gen')
                tags['album'] = safe_get(audio, '\xa9alb')
                tags['albumartist'] = safe_get(audio, 'aART')
                
                trkn = audio.get('trkn')
                if trkn and len(trkn) > 0 and isinstance(trkn[0], tuple):
                    if len(trkn[0]) > 0 and int(trkn[0][0]) > 0: tags['track'] = str(trkn[0][0])
                    if len(trkn[0]) > 1 and int(trkn[0][1]) > 0: tags['totaltracks'] = str(trkn[0][1])
                elif trkn and len(trkn) > 0:
                    tags['track'] = str(trkn[0])
                    
                disk = audio.get('disk')
                if disk and len(disk) > 0 and isinstance(disk[0], tuple):
                    if len(disk[0]) > 0 and int(disk[0][0]) > 0: tags['disc'] = str(disk[0][0])
                elif disk and len(disk) > 0:
                    tags['disc'] = str(disk[0])
                    
                tags['codec'] = getattr(audio.info, 'codec', self.type[1:].upper())
                    
            elif self.type in {'.ogg', '.opus', '.wav', '.aac', '.wma'}:
                if self.type == '.ogg': audio = OggVorbis(self.path)
                elif self.type == '.opus': audio = OggOpus(self.path)
                elif self.type == '.wav': audio = WAVE(self.path)
                elif self.type == '.aac': audio = AAC(self.path)
                elif self.type == '.wma': audio = ASF(self.path)
                
                audio_for_info = audio
                
                tags['artist'] = safe_get(audio, 'artist', default='Unbekannt')
                tags['title'] = safe_get(audio, 'title', default=self.name)
                tags['year'] = safe_get(audio, 'date') or safe_get(audio, 'year')
                tags['genre'] = safe_get(audio, 'genre')
                tags['album'] = safe_get(audio, 'album')
                tags['albumartist'] = safe_get(audio, 'albumartist')
                tags['track'] = safe_get(audio, 'tracknumber') or safe_get(audio, 'track')
                tags['disc'] = safe_get(audio, 'discnumber')
                tags['codec'] = self.type[1:].upper()
            
            # Retrieve common stream info elements
            if audio_for_info and hasattr(audio_for_info, 'info'):
                info = audio_for_info.info
                if hasattr(info, 'bitrate') and info.bitrate:
                    tags['bitrate'] = f"{int((info.bitrate + 500) // 1000)} kbps"
                if hasattr(info, 'sample_rate') and info.sample_rate:
                    tags['samplerate'] = format_samplerate(info.sample_rate)
                if hasattr(info, 'bits_per_sample') and info.bits_per_sample:
                    tags['bitdepth'] = f"{info.bits_per_sample} Bit"
                elif hasattr(info, 'bits_per_sample'):
                    if info.bits_per_sample > 0:
                        tags['bitdepth'] = f"{info.bits_per_sample} Bit"
                    else:
                        tags['bitdepth'] = ''
                else:
                    tags['bitdepth'] = ''
                    
                # Append exact FFmpeg stream format for uniformity across all formats if missing
                try:
                    import subprocess, re
                    cmd = ["ffmpeg", "-i", self.path.as_posix()]
                    output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
                    
                    # ==========================================
                    # CONTAINER-FORMAT AUSWERTUNG (FFmpeg)
                    # ==========================================
                    # FFmpeg gibt in der Line "Input #0" das exakte Demuxer-Format an.
                    # Viele Formate teilen sich historisch denselben Container-Standard:
                    # 
                    # 1. ISOBMFF (Apple QuickTime Derivate):
                    #    Formate wie .mp4, .m4a (Audio) und .m4b (Audiobooks) basieren alle 
                    #    auf dem "Base Media" Format (ISO/IEC 14496-12). FFmpeg fasst diese 
                    #    beim Einlesen generisch unter dem Begriff "mov,mp4,m4a,3gp,3g2,mj2" zusammen.
                    #    Wenn wir "MOV" auslesen, aber die Datei eigentlich ".m4b" heißt, 
                    #    korrigieren wir die Anzeige für den User exakt auf die Dateiendung (z.B. M4B).
                    #
                    # 2. Matroska / WebM:
                    #    Ein extrem flexibler Open-Source Container, der fast alle Streams schluckt.
                    #    FFmpeg meldet hier "matroska,webm". Wir bereinigen das visuell zu "MKV".
                    # ==========================================
                    input_match = re.search(r"Input #0,\s*([^,]+)", output)
                    if input_match:
                        raw_cont = input_match.group(1).upper().strip()
                        raw_ext = self.type[1:].upper()
                        
                        # Apple/ISOBMFF Container Bereinigung
                        if raw_cont == 'MOV' and raw_ext in ('MP4', 'M4A', 'M4B', 'M4V'):
                            tags['container'] = raw_ext
                        # Matroska Container Bereinigung
                        elif raw_cont == 'MATROSKA':
                            tags['container'] = 'MKV'
                        else:
                            tags['container'] = raw_cont
                            
                    stream_match = re.search(r"Stream #.*?: Audio:(.*)", output)
                    if stream_match:
                        audio_line = stream_match.group(1)
                        fmt_match = re.search(r"\b(s16|s16p|s24|s24p|s32|s32p|fltp|flt)\b", audio_line)
                        if fmt_match:
                            fmt = fmt_match.group(1)
                            # If mutagen found e.g. '16 Bit', append '(s16p)'
                            if tags['bitdepth']:
                                if '(' not in tags['bitdepth']:
                                    tags['bitdepth'] += f" ({fmt})"
                            else:
                                if fmt in ('s16', 's16p'): tags['bitdepth'] = f"16 Bit ({fmt})"
                                elif fmt in ('s24', 's24p'): tags['bitdepth'] = f"24 Bit ({fmt})" # Das liegt daran, dass Computer-Prozessoren (CPUs) nativ keine 24-Bit-Blöcke verarbeiten können (es gibt nur 8, 16, 32, 64 Bit Architektur). Wenn FFmpeg also ein hochauflösendes 24-Bit-Signal dekodiert, wird es für die interne Sound-Verarbeitung in der Regel mit Nullen aufgefüllt (Zero-Padding) und als flüssiger 32-Bit-Integer (s32p = signed 32-bit planar) an die Soundkarte weitergereicht
                                elif fmt in ('s32', 's32p'): tags['bitdepth'] = f"32 Bit ({fmt})"
                                elif fmt in ('fltp', 'flt'): tags['bitdepth'] = f"16 Bit ({fmt})"
                except Exception:
                    pass
                    
            # ==========================================
            # AUDIO-TAG AUSWERTUNG (Mutagen)
            # ==========================================
            # Je nach Dateityp verwendet die Mutagen-Bibliothek völlig unterschiedliche Parser.
            # Um dem Nutzer saubere, branchenübliche Tag-Typen anzuzeigen, schlüsseln wir diese auf:
            #
            # 1. ID3 (MP3):
            #    ID3-Tags haben historisch viele Iterationen (v1, v2.2, v2.3, v2.4). Da die Version hier
            #    elementar für die Kompatibilität von Car-Audios und Playern ist, lesen wir explizit
            #    den `tags.version` Tuple (z.B. (2,3,0)) aus und wandeln ihn formal in "ID3v2.3" um.
            # 
            # 2. ISOBMFF / Apple (MP4/M4A/M4B):
            #    Nutzt intern sogenannte "MP4 Atoms" (ilst). Ein versionierungsgeladenes Chaos 
            #    wie bei ID3 gibt es hier nicht. Wir benennen Mutagens rohes "MP4Tags" in das
            #    cleane "MP4" um.
            #
            # 3. Xiph (Ogg/FLAC):
            #    Nutzen den "Vorbis Comment" Standard (eine simple LISTE von Schlüssel=Wert paaren).
            #    Auch hier gibt es keine nennenswerte Unterversionierung. Um sie voneinander 
            #    zu trennen, benennen wir "OggVComment" und "FLACVComment" in menschliche Strings um.
            # ==========================================
            if audio_for_info and hasattr(audio_for_info, 'tags') and audio_for_info.tags is not None:
                tag_name = type(audio_for_info.tags).__name__
                if tag_name == 'ID3' and hasattr(audio_for_info.tags, 'version'):
                    # e.g., (2, 3, 0) -> ID3v2.3
                    tags['tagtype'] = f"ID3v{audio_for_info.tags.version[0]}.{audio_for_info.tags.version[1]}"
                elif tag_name == 'MP4Tags':
                    tags['tagtype'] = 'MP4Tags'
                elif tag_name == 'OggVComment':
                    tags['tagtype'] = 'Vorbis Comment (Ogg)'
                elif tag_name == 'VCFLACDict': # FLACVComment
                    tags['tagtype'] = 'Vorbis Comment (FLAC)'
                else:
                    tags['tagtype'] = tag_name
                
            # Detect Embedded Cover Art
            if self.type == '.mp3' and audio_for_info:
                tags['has_art'] = 'Yes' if any(k.startswith('APIC') for k in audio_for_info.keys()) else 'No'
            elif self.type == '.flac' and audio_for_info:
                tags['has_art'] = 'Yes' if len(audio_for_info.pictures) > 0 else 'No'
            elif self.type in {'.m4a', '.alac', '.m4b'} and audio_for_info:
                tags['has_art'] = 'Yes' if 'covr' in audio_for_info.keys() else 'No'
                    
        except Exception as e:
            # Für .aac oder Dateien ohne korrekte Tags fangen wir den Fehler ab
            pass
            
        # FFmpeg Fallback für fehlende Metadaten (speziell für untagged AAC Dateien)
        if not tags['samplerate'] or not tags['bitrate'] or tags['tagtype'] == 'None' or not tags['bitdepth']:
            try:
                import subprocess, re
                cmd = ["ffmpeg", "-i", self.path.as_posix()]
                output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
                
                # Container / Format aus Input Info lesen: Input #0, matroska,webm, from ...
                if not tags['container']:
                    # ==========================================
                    # FALLBACK CONTAINER-FORMAT AUSWERTUNG
                    # ==========================================
                    # Falls Mutagen komplett fehlgeschlagen ist (z.B. bei komplexen MKVs),
                    # extrahieren wir den Container nachträglich nochmal sauber analog zur Head-Logik.
                    # Dies verhindert fehlerhafte "Tag Format" Anzeigen, da ein Container (MKV) 
                    # kein Tag-Format (wie ID3) ist!
                    input_match = re.search(r"Input #0,\s*([^,]+)", output)
                    if input_match:
                        raw_cont = input_match.group(1).upper().strip()
                        raw_ext = self.type[1:].upper()
                        
                        if raw_cont == 'MOV' and raw_ext in ('MP4', 'M4A', 'M4B', 'M4V'):
                            tags['container'] = raw_ext
                        elif raw_cont == 'MATROSKA':
                            tags['container'] = 'MKV'
                        else:
                            tags['container'] = raw_cont
                
                # Suche Audio-Stream Zeile: Stream #0:0: Audio: aac (LC), 44100 Hz, stereo, fltp, 256 kb/s
                stream_match = re.search(r"Stream #.*?: Audio:(.*)", output)
                if stream_match:
                    audio_line = stream_match.group(1)
                    
                    if not tags['codec'] or tags['codec'] == self.type[1:].upper():
                        codec_match = re.search(r"^\s*([a-zA-Z0-9_]+)", audio_line)
                        if codec_match:
                            tags['codec'] = codec_match.group(1).upper()
                            
                    if not tags['samplerate']:
                        sr_match = re.search(r"(\d+)\s*Hz", audio_line) # Suche nach Sample Rate
                        if sr_match:
                            tags['samplerate'] = format_samplerate(sr_match.group(1))
                            
                    if not tags['bitdepth']:
                        fmt_match = re.search(r"\b(s16|s16p|s24|s24p|s32|s32p|fltp|flt)\b", audio_line)
                        if fmt_match:
                            fmt = fmt_match.group(1)
                            if fmt in ('s16', 's16p'): tags['bitdepth'] = f"16 Bit ({fmt})"
                            elif fmt in ('s24', 's24p'): tags['bitdepth'] = f"24 Bit ({fmt})"
                            elif fmt in ('s32', 's32p'): tags['bitdepth'] = f"32 Bit ({fmt})"
                            elif fmt in ('fltp', 'flt'): tags['bitdepth'] = f"16 Bit ({fmt})"
                        
                    if not tags['bitrate']:
                        br_match = re.search(r"(\d+)\s*kb/s", audio_line)
                        if br_match:
                            tags['bitrate'] = f"{br_match.group(1)} kbps"
                
            # Duration: ... bitrate: 256 kb/s
                bit_match = re.search(r"bitrate:\s*(\d+)\s*kb/s", output)
                if bit_match and not tags['bitrate']:
                    tags['bitrate'] = f"{bit_match.group(1)} kbps"
                    
                if not tags['codec']:
                    tags['codec'] = self.type[1:].upper()
            except Exception:
                pass
                
        # If bitdepth is not available, leave it empty so the UI hides it cleanly.
        return tags

    def to_dict(self):
        hours, remainder = divmod(self.duration, 3600)
        mins, secs = divmod(remainder, 60)
        
        if hours > 0:
            duration_str = f"{hours}:{mins:02d}:{secs:02d}"
        else:
            duration_str = f"{mins}:{secs:02d}"
            
        return {
            'name': self.name,
            'path': self.path.as_posix(),
            'duration': duration_str,
            'tags': self.tags,
            'type': self.type[1:]  # 'mp3'
        }


# Testdateien
MEDIA_DIR = "./media"  # Ordner, in dem deine Dateien liegen

import bottle
import mimetypes
import subprocess
import os
import uuid

@bottle.hook('before_request')
def log_request():
    with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
        f.write(f"REQ IN: {bottle.request.url}\n")

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    ext = filepath.lower()
    
    # Strip the disguise extension added by Javascript
    if filepath.endswith('.flac_transcoded'):
        filepath = filepath[:-16]
        ext = filepath.lower()

    with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
        f.write(f"ROUTE CALLED: filepath={filepath}, ext={ext}\n")
    
    if ext.endswith('.alac') or ext.endswith('.m4a') or ext.endswith('.m4b'):
        full_path = os.path.join(MEDIA_DIR, filepath)
        cache_dir = os.path.join(MEDIA_DIR, '.cache')
        os.makedirs(cache_dir, exist_ok=True)
        
        # Cachename replaces extension with .flac to avoid collisions
        cache_filename = filepath.replace('/', '_').rsplit('.', 1)[0] + '.flac'
        cache_path = os.path.join(cache_dir, cache_filename)
        tmp_path = cache_path + f'.{uuid.uuid4().hex[:6]}.tmp'
        
        # Check if we already transcoded this file
        if not os.path.exists(cache_path):
            with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
                f.write(f"TRANSCODING STARTED: full_path={full_path}\n")
            try:
                # Run ffmpeg to generate the FLAC file to a temporary path first
                subprocess.run(
                    ['ffmpeg', '-y', '-v', 'warning', '-i', full_path, '-vn', '-f', 'flac', tmp_path],
                    check=True, capture_output=True, text=True
                )
                # Atomic rename ensures other concurrent requests don't read a half-written file
                os.replace(tmp_path, cache_path)
                with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
                    f.write("TRANSCODING SUCCESS\n")
            except subprocess.CalledProcessError as e:
                with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
                    f.write(f"TRANSCODING FAILED: {e.stderr}\n")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                return bottle.HTTPError(500, "Transcoding Error")
                
        # Serve the cached FLAC file instead of the ALAC one
        return bottle.static_file(cache_filename, root=cache_dir, mimetype='audio/flac')

    if ext.endswith('.flac'):
        mime_type = 'audio/flac'
    
    if mime_type:
        return bottle.static_file(filepath, root=MEDIA_DIR, mimetype=mime_type)
    return bottle.static_file(filepath, root=MEDIA_DIR)

@bottle.route('/cover/<filepath:path>')
def serve_cover(filepath):
    # Determine the absolute filepath
    full_path = os.path.join(MEDIA_DIR, filepath)
    if not os.path.exists(full_path):
        return bottle.HTTPError(404, "File not found")
        
    path_obj = Path(full_path)
    file_type = path_obj.suffix.lower()
    
    img_data = None
    mime_type = "image/jpeg"
    
    try:
        if file_type == '.mp3':
            audio = MP3(full_path)
            # APIC contains the picture in ID3v2
            for tag in audio.tags.values():
                if tag.FrameID == 'APIC':
                    img_data = tag.data
                    mime_type = tag.mime
                    break
        elif file_type == '.flac':
            audio = FLAC(full_path)
            if audio.pictures:
                img_data = audio.pictures[0].data
                mime_type = audio.pictures[0].mime
        elif file_type in {'.m4a', '.alac', '.m4b'}:
            audio = MP4(full_path)
            if 'covr' in audio.tags and audio.tags['covr']:
                # MP4 covers are usually arrays of binary data
                img_data = bytes(audio.tags['covr'][0])
                # M4A covr images are typically JPEG or PNG. Check magic bytes
                if img_data.startswith(b'\x89PNG\r\n\x1a\n'):
                    mime_type = 'image/png'
                else:
                    mime_type = 'image/jpeg'
    except Exception as e:
        pass
        
    if img_data:
        bottle.response.content_type = mime_type
        return img_data
    
    return bottle.HTTPError(404, "No cover found")


# Funktion, um Medien zu scannen und an die GUI zu senden
@eel.expose("scan_media")
def scan_media():
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
        return {"error": "Ordner erstellt – füge Dateien hinzu"}
    media = []
    for f in Path(MEDIA_DIR).iterdir():
        if f.is_file() and f.suffix.lower() in {'.mp3', '.flac', '.ogg', '.wav', '.m4a', '.alac', '.opus', '.aac', '.wma', '.m4b'}:
            item = MediaItem(f.name, f)
            media.append(item.to_dict()) # Datenmodel
    return {"media": media}  # Reich an GUI mit Tags + Dauer

@eel.expose("play_media")
def play_media(path):
    """GUI ruft das an – aber HTML5 Audio handhabt Abspielen client-seitig."""
    return {"status": "play", "path": path}  # Bestätigung

# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    eel.init("web")            # Ordner mit HTML/CSS/JS
    eel.start("app.html", size=(1000, 600))    # Starte Seite
