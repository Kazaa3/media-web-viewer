import subprocess
import re

def format_samplerate(hz):
    try:
        hz = float(hz)
        khz = hz / 1000
        return f"{int(khz)} kHz" if khz.is_integer() else f"{khz:g} kHz"
    except:
        return ""

def parse(path, file_type, tags):
    try:
        cmd = ["ffmpeg", "-i", path.as_posix()]
        output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
        
        # Container/Format fallback
        if not tags.get('container'):
            input_match = re.search(r"Input #0,\s*([^,]+)", output)
            if input_match:
                raw_cont = input_match.group(1).upper().strip()
                raw_ext = file_type[1:].upper()
                
                if raw_cont == 'MOV' and raw_ext in ('MP4', 'M4A', 'M4B', 'M4V'):
                    tags['container'] = raw_ext
                elif raw_cont == 'MATROSKA':
                    tags['container'] = 'MKV'
                else:
                    tags['container'] = raw_cont
                    
        # Audio stream fallback
        stream_match = re.search(r"Stream #.*?: Audio:(.*)", output)
        if stream_match:
            audio_line = stream_match.group(1)
            
            # Codec
            if not tags.get('codec') or tags.get('codec') == file_type[1:].upper():
                codec_match = re.search(r"^\s*([a-zA-Z0-9_]+)", audio_line)
                if codec_match:
                    tags['codec'] = codec_match.group(1).upper()
                    
            # Sample rate
            if not tags.get('samplerate'):
                sr_match = re.search(r"(\d+)\s*Hz", audio_line)
                if sr_match:
                    tags['samplerate'] = format_samplerate(sr_match.group(1))
                    
            # Bitdepth
            fmt_match = re.search(r"\b(s16|s16p|s24|s24p|s32|s32p|fltp|flt)\b", audio_line)
            if fmt_match:
                fmt = fmt_match.group(1)
                if tags.get('bitdepth'):
                    if '(' not in tags['bitdepth']:
                        tags['bitdepth'] += f" ({fmt})"
                else:
                    if fmt in ('s16', 's16p'): tags['bitdepth'] = f"16 Bit ({fmt})"
                    elif fmt in ('s24', 's24p'): tags['bitdepth'] = f"24 Bit ({fmt})"
                    elif fmt in ('s32', 's32p'): tags['bitdepth'] = f"32 Bit ({fmt})"
                    elif fmt in ('fltp', 'flt'): tags['bitdepth'] = f"16 Bit ({fmt})"
                
            # Bitrate
            if not tags.get('bitrate'):
                br_match = re.search(r"(\d+)\s*kb/s", audio_line)
                if br_match:
                    tags['bitrate'] = f"{br_match.group(1)} kbps"
        
        # General Bitrate fallback
        bit_match = re.search(r"bitrate:\s*(\d+)\s*kb/s", output)
        if bit_match and not tags.get('bitrate'):
            tags['bitrate'] = f"{bit_match.group(1)} kbps"
            
        if not tags.get('codec'):
            tags['codec'] = file_type[1:].upper()

    except Exception:
        pass

    return tags
