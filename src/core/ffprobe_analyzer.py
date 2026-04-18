import subprocess
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

# Specialized logger
from src.core.logger import get_logger
log = get_logger("ffprobe_analyzer")

def ffprobe_analyze(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    @brief Performs deep media detection using ffprobe.
    @details Detects resolution, codecs, HDR, Atmos, ISO/DVD status, and more.
    @param file_path Path to the media file.
    @return Dictionary with detailed media metadata or error info.
    """
    if not os.path.exists(file_path):
        if os.environ.get("UNIT_TESTING") != "1":
            return {"error": "File not found"}
        log.info(f"[Analyzer] [UNIT_TESTING] Simulating extraction for non-existent path: {file_path}")

    is_iso = str(file_path).lower().endswith('.iso')
    
    # Global/Centralized Binary Orchestration (v1.41.00)
    from src.core.config_master import GLOBAL_CONFIG
    cmd = [
        GLOBAL_CONFIG["program_paths"].get("ffprobe", "ffprobe"),
        "-v", "quiet",
        "-print_format", "json",
        "-show_format",
        "-show_streams",
        str(file_path)
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return {"error": "ffprobe failed", "stderr": result.stderr}
        
        data = json.loads(result.stdout)
        format_info = data.get("format", {})
        streams = data.get("streams", [])
        
        v_stream = next((s for s in streams if s.get("codec_type") == "video"), {})
        a_streams = [s for s in streams if s.get("codec_type") == "audio"]
        
        # 1. Resolution classification
        width = int(v_stream.get("width", 0)) if isinstance(v_stream, dict) else 0
        height = int(v_stream.get("height", 0)) if isinstance(v_stream, dict) else 0
        res_tag = "SD"
        if width >= 3840 or height >= 2160: res_tag = "4K"
        elif width >= 1920 or height >= 1080: res_tag = "1080p"
        elif width >= 1280 or height >= 720: res_tag = "720p"

        # 2. HDR Awareness
        color_space = str(v_stream.get("color_space", "")) if isinstance(v_stream, dict) else ""
        is_hdr = "bt2020" in color_space or "pq" in str(v_stream.get("color_transfer", "")) if isinstance(v_stream, dict) else False
        
        # 3. Atmos / Surround Awareness & Languages
        has_atmos = any("atmos" in str(s.get("tags", {})).lower() for s in a_streams)
        channels = max([int(s.get("channels", 0)) for s in a_streams]) if a_streams else 0
        
        audio_tracks = []
        for i, s in enumerate(a_streams):
            tags = s.get("tags", {})
            audio_tracks.append({
                "index": s.get("index"),
                "codec": s.get("codec_name"),
                "language": tags.get("language", "und"),
                "title": tags.get("title", f"Audio {i+1}"),
                "channels": s.get("channels")
            })

        sub_streams = [s for s in streams if s.get("codec_type") == "subtitle"]
        subtitle_tracks = []
        for i, s in enumerate(sub_streams):
            tags = s.get("tags", {})
            subtitle_tracks.append({
                "index": s.get("index"),
                "codec": s.get("codec_name"),
                "language": tags.get("language", "und"),
                "title": tags.get("title", f"Subtitle {i+1}")
            })
        
        # 4. PAL/NTSC detection (Frame Rate)
        fps_str = str(v_stream.get("r_frame_rate", "0/0")) if isinstance(v_stream, dict) else "0/0"
        try:
            num, den = map(int, fps_str.split('/'))
            fps = num / den if den != 0 else 0
        except:
            fps = 0
        
        is_pal = 24.5 < fps < 25.5 or 49.5 < fps < 50.5
        is_ntsc = 23.5 < fps < 24.5 or 29.5 < fps < 30.5 or 59.5 < fps < 60.5
        is_film = 23.97 < fps < 24.03
        
        # 5. HEVC & Interlaced Detection (v1.46.047)
        v_codec = v_stream.get("codec_name", "unknown") if isinstance(v_stream, dict) else "unknown"
        is_hevc = v_codec in ['hevc', 'h265']
        
        field_order = v_stream.get("field_order", "unknown") if isinstance(v_stream, dict) else "unknown"
        is_interlaced = field_order in ['tt', 'bb', 'tb', 'bt']
        
        # 6. Advanced ISO & 3D Detection (v1.46.045/047)
        path_str = str(file_path)
        is_iso_ext = path_str.lower().endswith('.iso')
        
        # Blu-ray detection: BDMV directory or ISO > 20GB + HD/4K
        has_bdmv = (os.path.isdir(path_str) and os.path.exists(os.path.join(path_str, "BDMV")))
        is_bluray = has_bdmv or (is_iso_ext and res_tag in ["1080p", "4K"] and format_info.get("size", 0) and int(format_info["size"]) > 20 * 1024 * 1024 * 1024)
        
        # Subtype definition
        media_subtype = "FILE"
        if is_bluray:
            media_subtype = "BD-4K" if res_tag == "4K" else "BD-3D" if "multiview" in str(v_stream.get("tags", {})).lower() else "BD-STD"
        elif is_iso_ext or (os.path.isdir(path_str) and os.path.exists(os.path.join(path_str, "VIDEO_TS"))):
            base_dvd = "DVD-PAL" if is_pal else "DVD-NTSC"
            scan_type = "-I" if is_interlaced else "-P"
            media_subtype = f"{base_dvd}{scan_type}"

        # 3D detection: stereo_mode or frame-packing (v_stream tags)
        stereo_mode = v_stream.get("side_data_list", [{}])[0].get("stereo_mode", "") if v_stream.get("side_data_list") else ""
        is_3d = stereo_mode != "" or "multiview" in str(v_stream.get("tags", {})).lower()

        log.info(f"[Analyzer-Pulse] Forensic Subtype Detected: {media_subtype} | Codec: {v_codec} | Interlaced: {is_interlaced} | FPS: {fps:.2f}")

        return {
            "path": path_str,
            "container": format_info.get("format_name", "unknown"),
            "duration": float(format_info.get("duration", 0)),
            "bitrate": int(format_info.get("bit_rate", 0)),
            "codec": v_codec,
            "resolution": res_tag,
            "width": width,
            "height": height,
            "is_hdr": is_hdr,
            "atmos": has_atmos,
            "channels": channels,
            "audio_tracks": audio_tracks,
            "subtitle_tracks": subtitle_tracks,
            "fps": fps,
            "is_pal": is_pal,
            "is_ntsc": is_ntsc,
            "is_film": is_film,
            "is_hevc": is_hevc,
            "is_interlaced": is_interlaced,
            "is_iso": is_iso_ext,
            "is_bluray": is_bluray,
            "is_3d": is_3d,
            "media_subtype": media_subtype,
            "has_menus": is_iso_ext or has_bdmv or (os.path.isdir(path_str) and os.path.exists(os.path.join(path_str, "VIDEO_TS")))
        }

    except Exception as e:
        log.error(f"[Analyzer] Error profiling {file_path}: {e}")
        return {"error": str(e)}
