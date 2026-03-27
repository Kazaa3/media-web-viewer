import subprocess
import json
import logging
import os
from pathlib import Path

# Specialized logger
log = logging.getLogger("ffprobe_analyzer")

def ffprobe_analyze(file_path):
    """
    @brief Deep analysis of media file using ffprobe.
    @details Detects codec, container, resolution, fps, interlacing (PAL), ISO structure, Atmos.
    @param file_path Path to the media file.
    @return Dictionary with detected features.
    """
    try:
        # 1. Basic Probe
        cmd = [
            "ffprobe", "-v", "error",
            "-show_format", "-show_streams",
            "-of", "json", str(file_path)
        ]
        
        # Increase probe size for complex files (ISOs)
        if str(file_path).lower().endswith('.iso'):
            cmd[1:1] = ["-analyzeduration", "100M", "-probesize", "100M"]

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            log.error(f"FFprobe failed for {file_path}: {res.stderr}")
            return {"error": res.stderr}
        
        data = json.loads(res.stdout)
        format_info = data.get("format", {})
        streams = data.get("streams", [])
        
        video_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
        audio_streams = [s for s in streams if s.get("codec_type") == "audio"]
        
        # 2. Extract Basic Metrics
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        fps = _parse_fps(video_stream.get("r_frame_rate"))
        codec = video_stream.get("codec_name", "unknown")
        container = format_info.get("format_name", "unknown")
        
        # 3. Features & Logic
        is_iso = str(file_path).lower().endswith(('.iso', '.img', '.bin'))
        
        # Atmos / High-End Audio detection
        has_atmos = False
        for s in audio_streams:
            tags = str(s.get("tags", {})).lower()
            if "atmos" in tags or "truehd" in tags:
                has_atmos = True
                break
            if s.get("codec_name") == "eac3" and s.get("channel_layout") == "7.1":
                has_atmos = True # Heuristic for streaming Atmos
                break

        # PAL Heuristic (25fps or 50i)
        is_interlaced = video_stream.get("field_order", "progressive") != "progressive"
        is_pal = (fps in [25, 50]) or (is_interlaced and fps == 25)
        
        result = {
            "codec": codec,
            "container": container,
            "width": width,
            "height": height,
            "fps": fps,
            "is_pal": is_pal,
            "is_interlaced": is_interlaced,
            "is_iso": is_iso,
            "has_menus": is_iso or str(file_path).lower().endswith('.vob'),
            "atmos": has_atmos,
            "bitrate": int(format_info.get("bit_rate", 0)) if format_info.get("bit_rate", "0").isdigit() else 0,
            "duration": float(format_info.get("duration", 0)),
        }
        
        # Resolution Labeling
        if height >= 2160: result["resolution"] = "4K"
        elif height >= 1080: result["resolution"] = "1080p"
        elif height >= 720: result["resolution"] = "720p"
        else: result["resolution"] = "SD"
            
        return result
    except Exception as e:
        log.error(f"Analyzer crash for {file_path}: {e}")
        return {"error": str(e)}

def _parse_fps(fps_str):
    if not fps_str: return 0
    try:
        if "/" in fps_str:
            n, d = map(float, fps_str.split("/"))
            return n / d if d != 0 else 0
        return float(fps_str)
    except:
        return 0
