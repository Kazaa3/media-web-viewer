import subprocess
import re
from pathlib import Path
from typing import Any


def get_capabilities() -> dict[str, Any]:
    return {
        "name": "FFmpeg",
        "description": "Standard CLI-based media tool. Used as a robust fallback for container and stream identification when other parsers fail.",
        "supported_tags": ["container", "codec", "samplerate", "bitrate", "bitdepth", "chapters"],
        "supported_codecs": ["*"]
    }


def get_settings_schema() -> dict[str, Any]:
    return {
        "deep_analysis": {
            "type": "boolean",
            "default": False,
            "description": "Scan the entire file for more accurate stream details (slower)."
        },
        "timeout": {
            "type": "integer",
            "default": 30,
            "description": "Maximum execution time in seconds."
        }
    }


def parse(path, file_type, tags, filename=None, mode='lightweight', settings=None):
    """
    @brief Extracts metadata using FFmpeg CLI (last-resort fallback).
    @details Extrahiert Metadaten mittels FFmpeg CLI (letzte Instanz Fallback).
    @param path Absolute path / Absoluter Pfad.
    @param file_type Extension / Dateiendung.
    @param tags Existing tags dictionary / Vorhandene Tags.
    @param filename Current filename / Aktueller Dateiname.
    @param mode Extraction mode / Extraktionsmodus.
    @return Updated tags dictionary / Aktualisiertes Tag-Dictionary.
    """
    if filename is None:
        filename = Path(path).name

    if mode == 'full' and 'full_tags' not in tags:
        tags['full_tags'] = {}

    if settings is None:
        from .format_utils import PARSER_CONFIG
        settings = PARSER_CONFIG.get('parser_settings', {}).get('ffmpeg', {})

    try:
        cmd = ["ffmpeg"]
        # Add custom flags if any
        custom_flags = settings.get('cli_flags', '').split()
        if custom_flags:
            cmd.extend(custom_flags)
            
        if settings.get('deep_analysis'):
            cmd.extend(["-analyzeduration", "100M", "-probesize", "100M"])
        cmd.extend(["-i", str(path)])
        
        output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, timeout=settings.get('timeout', 30)).stderr

        if mode == 'full':
            tags['full_tags']['ffmpeg_raw'] = output

        # Container/Format fallback
        if not tags.get('container'):
            input_match = re.search(r"Input #0,\s*([^,]+)", output)
            if input_match:
                raw_cont = input_match.group(1).upper().strip()
                raw_ext = file_type[1:].upper()

                if raw_cont == 'MOV' and raw_ext in ('MP4', 'M4A', 'M4B', 'M4V', 'ALAC'):
                    tags['container'] = raw_ext.lower()
                else:
                    tags['container'] = raw_cont.lower()

        # Audio stream fallback
        stream_match = re.search(r"Stream #.*?: Audio:(.*)", output)
        if stream_match:
            audio_line = stream_match.group(1)
            from .format_utils import format_codec, format_bitdepth, format_samplerate

            # Codec
            if not tags.get('codec') or tags.get('codec') == file_type[1:].lower() or tags.get('container') == 'mkv':
                codec_match = re.search(r"^\s*([a-zA-Z0-9_\-]+)", audio_line)
                if codec_match:
                    tags['codec'] = format_codec(codec_match.group(1))

            # Sample rate
            if not tags.get('samplerate'):
                sr_match = re.search(r"(\d+)\s*Hz", audio_line)
                if sr_match:
                    tags['samplerate'] = format_samplerate(sr_match.group(1))

            # Bitdepth
            # First try to find explicit bit depth in parentheses (e.g., "s32 (24 bit)")
            explicit_bit_match = re.search(r"\((\d+)\s*bit\)", audio_line)
            if explicit_bit_match:
                bit_depth = explicit_bit_match.group(1)
                tags['bitdepth'] = f"{bit_depth} Bit"
            else:
                # Fall back to format string parsing
                fmt_match = re.search(r"\b(u8|u8p|s16|s16p|s24|s24p|s32|s32p|fltp|flt|dblp|dbl|s64|s64p)\b", audio_line)
                if fmt_match:
                    fmt = fmt_match.group(1)
                    tags['bitdepth'] = format_bitdepth(None, codec=tags.get('codec'), file_type=file_type, internal_fmt=fmt)

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
            tags['codec'] = file_type[1:].lower()

        # Chapter parsing
        if not tags.get('chapters'):
            ffmpeg_chapters: list[dict[str, Any]] = []
            lines = output.split('\n')
            current_chapter: Any = None
            for line in lines:
                chap_match = re.search(r"Chapter\s+#\d+:\d+:\s+start\s+([\d.]+),\s+end\s+([\d.]+)", line)
                if chap_match:
                    if current_chapter:
                        ffmpeg_chapters.append(current_chapter)
                    current_chapter = {
                        'start': float(chap_match.group(1)),
                        'end': float(chap_match.group(2)),
                        'title': f"Kapitel {len(ffmpeg_chapters) + 1}"
                    }
                    continue

                title_match = re.search(r"^\s+title\s+:\s+(.*)$", line)
                if title_match and current_chapter:
                    current_chapter['title'] = title_match.group(1).strip()

            if current_chapter:
                ffmpeg_chapters.append(current_chapter)

            if ffmpeg_chapters:
                from .format_utils import natural_sort_key
                tags['chapters'] = sorted(ffmpeg_chapters, key=lambda x: (
                    x.get('start', 0.0), natural_sort_key(x.get('title', ''))))

    except Exception:
        pass

    return tags
