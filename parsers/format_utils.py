import re
import os
import json
from pathlib import Path

# Config File Path
CONFIG_FILE = Path.home() / '.config' / 'gui_media_web_viewer' / 'parser_config.json'

# Central Parser Configuration
# This avoids circular imports with main.py
PARSER_CONFIG = {
    "parser_chain": ["mutagen", "pymediainfo", "ffmpeg", "container", "filename"],
    "debug_scan": True,
    "debug_parser": True
}

def load_parser_config():
    """Loads parser configuration from disk."""
    global PARSER_CONFIG
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r') as f:
                loaded = json.load(f)
                PARSER_CONFIG.update(loaded)
        except Exception as e:
            print(f"Error loading config: {e}")
    else:
        # Ensure directory exists but wait to save until needed
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        save_parser_config()

def save_parser_config():
    """Saves parser configuration to disk."""
    try:
        os.makedirs(CONFIG_FILE.parent, exist_ok=True)
        with open(CONFIG_FILE, 'w') as f:
            json.dump(PARSER_CONFIG, f, indent=4)
    except Exception as e:
        print(f"Error saving config: {e}")

# Load immediately on import
load_parser_config()

def format_samplerate(hz):
    """Standardizes sample rate display (e.g., 44100 -> 44.1 kHz)."""
    try:
        hz = float(hz)
        khz = hz / 1000
        return f"{int(khz)} kHz" if khz.is_integer() else f"{khz:g} kHz"
    except (ValueError, TypeError):
        return ""

def format_codec(raw_codec, track_info=None):
    """
    Standardizes codec naming.
    Force lowercase for most, but uppercase PCM with details if track_info provided.
    """
    if not raw_codec:
        return ""
        
    codec = str(raw_codec).lower()
    
    # Generic mappings for common codecs to match user preference
    codec_map = {
        'mpeg audio': 'mp3',
        'vorbis': 'ogg',
        'opus': 'opus',
        'flac': 'flac',
        'alac': 'alac',
        'aac': 'aac',
        'm4a': 'aac'
    }
    
    # PCM specific handling
    if codec == 'pcm' and track_info:
        sign = 'S' if getattr(track_info, 'format_settings__sign', '') == 'Signed' else 'U'
        end = 'LE' if getattr(track_info, 'format_settings__endianness', '') == 'Little' else 'BE'
        bps = getattr(track_info, 'bit_depth', '')
        return f"PCM_{sign}{bps}{end}"
    
    # Special case for PCM if it already looks like PCM_S16LE
    if codec.startswith('pcm_'):
        return raw_codec.upper()
        
    return codec_map.get(codec, codec)

def format_container(raw_container, file_type=None):
    """Standardizes container naming."""
    container = str(raw_container).lower().strip() if raw_container else ""

    if not container and file_type:
        container = file_type[1:].lower()
    
    # Handle ambiguous FFmpeg container outputs
    if container == 'matroska,webm':
        if file_type == '.webm':
            return 'webm'
        return 'mkv'
    
    container_map = {
        'matroska': 'mkv',
        'mov,mp4,m4a,3gp,3g2,mj2': 'mp4',
        'mpeg-4': 'mp4',
        'quicktime': 'mp4',
        'asf': 'wma',
        'ogg': 'ogg',
        'flac': 'flac',
        'mp3': 'mp3'
    }
    
    # Fallback to file_type if we have a generic ID3/WAV container that isn't really a "container"
    if container in ('id3', 'wav') and file_type:
        return file_type[1:].lower()
        
    return container_map.get(container, container)

def format_tagtype(raw_tagtype):
    """Standardizes meta tag object types into human readable formats."""
    if not raw_tagtype:
        return ""
        
    tag = str(raw_tagtype).strip()
    
    # Already formatted versions (e.g. ID3v2.3)
    if tag.startswith("ID3v"):
        return tag
        
    tag_map = {
        'ID3': 'ID3',
        'MP4Tags': 'MP4Tags',
        'OggVComment': 'Vorbis Comment (Ogg)',
        'VCFLACDict': 'Vorbis Comment (FLAC)',
        'ASF': 'ASF',
        'APETag': 'APEv2'
    }
    
    return tag_map.get(tag, tag)

def format_bitdepth(bit_depth, codec=None, file_type=None, internal_fmt=None):
    """
    Standardizes bit depth display.
    Handles PCM mappings (e.g., 24-bit -> 24 Bit (s32)) and lossy fallbacks.
    """
    if not bit_depth:
        # Check for lossy extensions if bitdepth is missing
        lossy_extensions = {'.mp3', '.ogg', '.aac', '.m4a', '.m4b', '.wma', '.opus'}
        if file_type in lossy_extensions:
            return "16 Bit (lossy)"
        return "16 Bit" # Generic default
        
    try:
        bd_int = int(bit_depth)
        
        # Check if it is a PCM codec (either explicitly passed or detected in codec string)
        is_pcm = False
        if codec:
            c_upper = str(codec).upper()
            if 'PCM' in c_upper or c_upper == 'WAV':
                is_pcm = True
        
        if is_pcm:
            if bd_int == 24:
                return "24 Bit (s32)"
            elif bd_int == 16:
                return "16 Bit (s16)"
            elif bd_int == 32:
                # Could be float or int, usually s32 or flt
                suffix = f"({internal_fmt})" if internal_fmt else "(s32)"
                return f"32 Bit {suffix}"
                
        # FFmpeg internal format mapping (e.g. s16, s32, fltp)
        if internal_fmt:
            # Check for specific user requested mapping: 24 Bit (s32) if it came from PCM_S24LE
            if internal_fmt in ('s32', 's32p') and bd_int == 24:
                return "24 Bit (s32)"
                
            fmt_map = {
                'u8': '8 Bit (u8)', 'u8p': '8 Bit (u8p)',
                's16': '16 Bit (s16)', 's16p': '16 Bit (s16p)',
                's24': '24 Bit (s24)', 's24p': '24 Bit (s24p)',
                's32': '32 Bit (s32)', 's32p': '32 Bit (s32p)',
                's64': '64 Bit (s64)', 's64p': '64 Bit (s64p)',
                'flt': '32 Bit (flt)', 'fltp': '32 Bit (fltp)',
                'dbl': '64 Bit (dbl)', 'dblp': '64 Bit (dblp)',
            }
            if internal_fmt in fmt_map:
                label = fmt_map[internal_fmt]
                if internal_fmt in ('flt', 'fltp', 'dbl', 'dblp'):
                    return f"{label} Float ({internal_fmt})"
                return label

        return f"{bd_int} Bit"
    except (ValueError, TypeError):
        return str(bit_depth)
