import subprocess
import json
from typing import Any


def parse(path, file_type, tags, mode='lightweight'):
    """
    @brief Extracts metadata using ffprobe CLI with JSON output.
    @details Extrahiert Metadaten mittels ffprobe CLI mit JSON-Ausgabe.
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if mode == 'full' and 'full_tags' not in tags:
        tags['full_tags'] = {}

    try:
        cmd = [
            "ffprobe",
            "-v", "quiet",
            "-print_format", "json",
            "-show_format",
            "-show_streams",
            "-show_chapters",
            str(path)
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode != 0:
            return tags
            
        data = json.loads(result.stdout)
        
        if mode == 'full':
            tags['full_tags']['ffprobe_json'] = data

        # Extract format information
        fmt = data.get('format', {})
        
        # Duration
        if not tags.get('duration') and 'duration' in fmt:
            try:
                tags['duration'] = int(float(fmt['duration']))
            except (ValueError, TypeError):
                pass
        
        # Container
        if not tags.get('container') and 'format_name' in fmt:
            format_name = fmt['format_name'].split(',')[0].upper()
            raw_ext = file_type[1:].upper()
            
            # Handle MOV/MP4 container variants
            if format_name == 'MOV' and raw_ext in ('MP4', 'M4A', 'M4B', 'M4V', 'ALAC'):
                tags['container'] = raw_ext.lower()
            else:
                tags['container'] = format_name.lower()
        
        # Overall bitrate
        if not tags.get('bitrate') and 'bit_rate' in fmt:
            try:
                bitrate_kbps = int(int(fmt['bit_rate']) / 1000)
                tags['bitrate'] = f"{bitrate_kbps} kbps"
            except (ValueError, TypeError):
                pass
        
        # Extract format tags (metadata)
        fmt_tags = fmt.get('tags', {})
        tag_mapping = {
            'title': ['title', 'TITLE'],
            'artist': ['artist', 'ARTIST'],
            'album': ['album', 'ALBUM'],
            'date': ['date', 'DATE', 'year', 'YEAR'],
            'genre': ['genre', 'GENRE'],
            'track': ['track', 'TRACK'],
            'disc': ['disc', 'DISC']
        }
        
        for tag_key, possible_keys in tag_mapping.items():
            if not tags.get(tag_key):
                for pk in possible_keys:
                    if pk in fmt_tags:
                        tags[tag_key] = str(fmt_tags[pk])
                        break
        
        # Extract stream information (audio)
        streams = data.get('streams', [])
        audio_stream = None
        
        for stream in streams:
            if stream.get('codec_type') == 'audio':
                audio_stream = stream
                break
        
        if audio_stream:
            from .format_utils import format_codec, format_bitdepth, format_samplerate
            
            # Codec
            if not tags.get('codec') or tags.get('codec') == file_type[1:].lower():
                codec_name = audio_stream.get('codec_name', '')
                if codec_name:
                    tags['codec'] = format_codec(codec_name)
            
            # Sample rate
            if not tags.get('samplerate') and 'sample_rate' in audio_stream:
                tags['samplerate'] = format_samplerate(audio_stream['sample_rate'])
            
            # Bitdepth
            if not tags.get('bitdepth'):
                bits_per_sample = audio_stream.get('bits_per_sample')
                bits_per_raw_sample = audio_stream.get('bits_per_raw_sample')
                sample_fmt = audio_stream.get('sample_fmt', '')
                
                if bits_per_sample and bits_per_sample > 0:
                    tags['bitdepth'] = f"{bits_per_sample} Bit"
                elif bits_per_raw_sample and bits_per_raw_sample > 0:
                    tags['bitdepth'] = f"{bits_per_raw_sample} Bit"
                elif sample_fmt:
                    tags['bitdepth'] = format_bitdepth(
                        None, 
                        codec=tags.get('codec'), 
                        file_type=file_type, 
                        internal_fmt=sample_fmt
                    )
            
            # Stream-specific bitrate
            if not tags.get('bitrate') and 'bit_rate' in audio_stream:
                try:
                    bitrate_kbps = int(int(audio_stream['bit_rate']) / 1000)
                    tags['bitrate'] = f"{bitrate_kbps} kbps"
                except (ValueError, TypeError):
                    pass
        
        # Extract chapters
        if not tags.get('chapters'):
            chapters_data = data.get('chapters', [])
            if chapters_data:
                ffprobe_chapters: list[dict[str, Any]] = []
                
                for idx, chap in enumerate(chapters_data):
                    chapter_dict: dict[str, Any] = {}
                    
                    # Start and end times
                    if 'start_time' in chap:
                        try:
                            chapter_dict['start'] = float(chap['start_time'])
                        except (ValueError, TypeError):
                            chapter_dict['start'] = 0.0
                    else:
                        chapter_dict['start'] = 0.0
                    
                    if 'end_time' in chap:
                        try:
                            chapter_dict['end'] = float(chap['end_time'])
                        except (ValueError, TypeError):
                            chapter_dict['end'] = 0.0
                    else:
                        chapter_dict['end'] = 0.0
                    
                    # Chapter title
                    chap_tags = chap.get('tags', {})
                    title = chap_tags.get('title') or chap_tags.get('TITLE') or f"Kapitel {idx + 1}"
                    chapter_dict['title'] = title
                    
                    ffprobe_chapters.append(chapter_dict)
                
                if ffprobe_chapters:
                    from .format_utils import natural_sort_key
                    tags['chapters'] = sorted(ffprobe_chapters, key=lambda x: (
                        x.get('start', 0.0), natural_sort_key(x.get('title', ''))))

    except subprocess.TimeoutExpired:
        pass
    except json.JSONDecodeError:
        pass
    except Exception:
        pass

    return tags
