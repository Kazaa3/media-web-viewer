import subprocess
import json
import logging
import os
from pathlib import Path
from typing import Dict, List, Any

# Specialized logger
log = logging.getLogger("ffprobe_analyzer")

def ffprobe_analyze(file_path: str | Path) -> Dict[str, Any]:
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
            cmd.insert(1, "-analyzeduration")
            cmd.insert(2, "100M")
            cmd.insert(3, "-probesize")
            cmd.insert(4, "100M")

        res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
        if res.returncode != 0:
            log.error(f"FFprobe failed for {file_path}: {res.stderr}")
            return {"error": res.stderr}
        
        data: Dict[str, Any] = json.loads(res.stdout)
        format_info: Dict[str, Any] = data.get("format", {})
        streams: List[Dict[str, Any]] = data.get("streams", [])
        
        # Explicitly find first video/audio streams
        video_stream: Dict[str, Any] = {}
        audio_streams: List[Dict[str, Any]] = []
        
        for s in streams:
            if s.get("codec_type") == "video" and not video_stream:
                video_stream = s
            elif s.get("codec_type") == "audio":
                audio_streams.append(s)

        # 2. Extract Basic Metrics
        width = int(video_stream.get("width", 0))
        height = int(video_stream.get("height", 0))
        fps = _parse_fps(str(video_stream.get("r_frame_rate", "0")))
        codec = str(video_stream.get("codec_name", "unknown"))
        container = str(format_info.get("format_name", "unknown"))
        
        # 3. Features & Logic
        is_iso = str(file_path).lower().endswith(('.iso', '.img', '.bin'))
        
        # Atmos / High-End Audio detection
        has_atmos = False
        for s in audio_streams:
            tags = str(s.get("tags", {})).lower()
            codec_name = str(s.get("codec_name", ""))
            layout = str(s.get("channel_layout", ""))
            
            if "atmos" in tags or "truehd" in codec_name:
                has_atmos = True
                break
            if codec_name == "eac3" and "7.1" in layout:
                has_atmos = True
                break

        # PAL Heuristic (25fps or 50i)
        is_interlaced = str(video_stream.get("field_order", "progressive")) != "progressive"
        is_pal = (fps in [25.0, 50.0]) or (is_interlaced and fps == 25.0)
        
        result: Dict[str, Any] = {
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
            "bitrate": int(format_info.get("bit_rate", 0)) if str(format_info.get("bit_rate", "0")).isdigit() else 0,
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

def _parse_fps(fps_str: str) -> float:
    if not fps_str: return 0.0
    try:
        if "/" in fps_str:
            n_v, d_v = map(float, fps_str.split("/"))
            return n_v / d_v if d_v != 0 else 0.0
        return float(fps_str)
    except:
        return 0.0
