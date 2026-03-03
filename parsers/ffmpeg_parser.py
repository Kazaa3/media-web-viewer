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
        cmd = ["ffmpeg", "-i", str(path)]
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
            fmt_match = re.search(r"\b(u8|u8p|s16|s16p|s24|s24p|s32|s32p|fltp|flt|dblp|dbl|s64|s64p)\b", audio_line)
            if fmt_match:
                fmt = fmt_match.group(1)
                fmt_map = {
                    'u8': '8 Bit', 'u8p': '8 Bit',
                    's16': '16 Bit', 's16p': '16 Bit',
                    's24': '24 Bit', 's24p': '24 Bit',
                    's32': '32 Bit', 's32p': '32 Bit',
                    's64': '64 Bit', 's64p': '64 Bit',
                    'flt': '32 Bit (Float)', 'fltp': '32 Bit (Float)',
                    'dbl': '64 Bit (Float)', 'dblp': '64 Bit (Float)',
                }
                bit_label = fmt_map.get(fmt, fmt)
                if tags.get('bitdepth'):
                    if '(' not in tags['bitdepth']:
                        tags['bitdepth'] += f" ({fmt})"
                else:
                    tags['bitdepth'] = f"{bit_label} ({fmt})"
                
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
