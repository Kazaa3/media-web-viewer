import eel
from src.core.ffprobe_analyzer import ffprobe_analyze # type: ignore
from src.core.logger import get_logger
log = get_logger("mode_router")

@eel.expose
def smart_route(file_path):
    """
    @brief The central decision engine for playback modes.
    @details Maps media analysis to one of the 8+ primary streaming paths.
    @param file_path Path to the media file.
    @return Dictionary with 'mode' and 'info'.
    """
    log.info(f"[PLAY-PULSE] smart_route analysis started for: {file_path}")
    info = ffprobe_analyze(file_path)
    if "error" in info:
        log.warning(f"[PLAY-PULSE] Routing fallback to direct_play due to analysis error: {info['error']}")
        return {"mode": "direct_play", "info": info}

    # 0. Load Configuration (v1.46.045 Integration)
    from src.core.config_master import GLOBAL_CONFIG
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {}).get("video", {})
    flags = reg.get("orchestration_flags", {})
    thresholds = reg.get("bitrate_thresholds", {})
    
    # Analysis
    codec = info.get('codec', 'unknown')
    container = info.get('container', 'unknown')
    resolution = info.get('resolution', 'SD')
    bitrate = info.get('bitrate_kbps', 0)
    
    # [v1.46.049] Granular Steering Matrix
    steering_c = flags.get("codec_steering", {})
    steering_r = flags.get("resolution_steering", {})
    
    # Defaults
    mode = 'hls_fmp4'
    reason = "Fallback (HLS/fMP4)"
    
    # [v1.46.048] Hardware & Complexity Matrix
    hw_info = GLOBAL_CONFIG.get("hardware_info", {})
    hevc_hw = hw_info.get("hevc_hw_decoding_available", False)
    # [v1.46.049/051] Master Steering Matrix
    steering_f = flags.get("frequency_steering", {})
    steering_c = flags.get("codec_steering", {})
    steering_r = flags.get("resolution_steering", {})
    
    # Defaults
    mode = 'hls_fmp4'
    reason = "Fallback (HLS/fMP4)"
    
    # [v1.46.048] Hardware & Complexity Matrix
    hw_info = GLOBAL_CONFIG.get("hardware_info", {})
    hevc_hw = hw_info.get("hevc_hw_decoding_available", False)
    subtype = info.get('media_subtype', 'FILE')
    
    is_easy_container = container in ['mp4', 'mkv', 'webm', 'mov', 'ts']
    is_complex_media = subtype.startswith(("DVD", "BD")) or info.get('is_3d')
    
    # 1. 4K HEVC Mandatory Hardware Check (Forensic Guard)
    if resolution == "4K" and info.get('is_hevc'):
        if not hevc_hw:
            log.warning(f"[PLAY-PULSE] 4K HEVC Detect: Hardware decoder missing! Forensic error triggered.")
            return {
                "mode": "error_hardware", 
                "message": "Transcoding of 4K HEVC requires hardware support (QSV/VAAPI/NVDEC).",
                "info": info
            }
        else:
            reason = "4K HEVC (Hardware Supported)"
            mode = 'direct_play' if bitrate < thresholds.get("direct_play_max_kbps", 20000) else 'mpv_native'
            return {"mode": mode, "info": info, "reason": reason}

    # 2. Priority: Physical Media & Specialized Steering (COMPLEX MASTERS)
    if is_complex_media:
        if subtype.startswith("DVD"):
            routing = flags.get("dvd_pal_routing" if info.get('is_pal') else "dvd_ntsc_routing", "menu")
            mode = 'vlc_bridge' if routing == "menu" else 'mse'
            reason = f"Complex Steering ({subtype} via {routing})"
        elif subtype.startswith("BD"):
            bd_mode_map = {"BD-4K": "bd_4k_routing", "BD-3D": "bd_3d_routing", "BD-STD": "bd_standard_routing"}
            routing = flags.get(bd_mode_map.get(subtype, "bd_standard_routing"), "menu")
            mode = 'vlc_bridge' if routing == "menu" else 'mse'
            reason = f"Complex Steering ({subtype} via {routing})"
        elif info.get('is_3d'):
            mode = 'vlc_bridge'
            reason = "3D Specialized Routing"
        return {"mode": mode, "info": info, "reason": reason}

    # 3. Priority: Frequency Master Overrides (v1.46.051 - 50Hz vs 60Hz)
    f_policy = "auto"
    if info.get('is_pal'): f_policy = steering_f.get("pal_50hz", "auto")
    elif info.get('is_ntsc'): f_policy = steering_f.get("ntsc_60hz", "auto")
    
    if f_policy != "auto":
        mode = 'direct_play' if f_policy == "direct" else 'mse' if f_policy == "mse" else 'mpv_native' if f_policy == "native" else 'hls_fmp4'
        reason = f"Frequency Master Override ({'PAL' if info.get('is_pal') else 'NTSC'} -> {f_policy})"
        return {"mode": mode, "info": info, "reason": reason}
    
    # 4. Priority: Manual Codec/Resolution Overrides (v1.46.049 Override Path)
    c_policy = steering_c.get(codec.replace("h265", "hevc"), "auto")
    r_key = resolution.lower() if resolution in ["720p", "1080p", "2160p"] else "pal" if info.get('is_pal') else "ntsc" if info.get('is_ntsc') else "auto"
    r_policy = steering_r.get(r_key, "auto")

    if c_policy != "auto":
        mode = 'direct_play' if c_policy == "direct" else 'mse' if c_policy == "mse" else 'hls_fmp4'
        reason = f"Manual Codec Steering ({codec} -> {c_policy})"
        return {"mode": mode, "info": info, "reason": reason}
    
    if r_policy != "auto":
        mode = 'direct_play' if r_policy == "direct" else 'mse' if r_policy == "mse" else 'mpv_native' if r_policy == "native" else 'hls_fmp4'
        reason = f"Manual Resolution Steering ({resolution} -> {r_policy})"
        return {"mode": mode, "info": info, "reason": reason}

    # 5. HEVC HD Steering Policy (Resolution-Aware Backup)
    if resolution in ["1080p", "720p"] and info.get('is_hevc'):
        if flags.get("hevc_force_transcode_on_hd", True):
            mode = 'mse' if bitrate < thresholds.get("mse_max_kbps", 15000) else 'hls_fmp4'
            reason = "HEVC HD Force-Transcode Policy"
        else:
            mode = 'direct_play'
            reason = "HEVC HD Native (Policy: Direct)"
        return {"mode": mode, "info": info, "reason": reason}

    # 6. Standard Digital Steering (EASY)
    direct_limit = thresholds.get("direct_play_max_kbps", 20000)
    if codec == 'h264' and is_easy_container:
        if resolution != "4K" and bitrate < direct_limit:
            mode = 'direct_play'
            reason = "Direct Play (Easy Container/Bitrate)"
            return {"mode": mode, "info": info, "reason": reason}
            
 
    # 7. MSE / HLS Fallback (Standard Heuristics)
    if bitrate < thresholds.get("mse_max_kbps", 15000) and codec in ['h264', 'vp9', 'av1']:
        mode = 'mse'
        reason = "MSE Standard Heuristic"
    else:
        mode = 'hls_fmp4'
        reason = "HLS/fMP4 Standard Heuristic (Fallback)"

    log.info(f"[PLAY-PULSE] Final Routing: {mode} | Reason: {reason} | Subtype: {subtype}")
    return {
        "mode": mode,
        "info": info,
        "reason": reason
    }

def get_mode_description(mode):
    """
    @brief Returns a human-readable description and tech-stack for the mode.
    """
    mapping = {
        'direct_play': "Direkte Dateiübertragung (Chrome Native)",
        'mse': "FFmpeg fMP4 zu MSE (Ultra-Low-Latency)",
        'hls_fmp4': "FFmpeg fMP4 zu HLS (Universal)",
        'vlc_bridge': "VLC HLS zu MSE (Interaktiv / Menüs)",
        'mpv_wasm': "libmpv zu Canvas (WASM / Interaktiv)",
        'mpv_native': "Externer MPV Player (Verlustfrei / 4K)",
        'vlc_native': "Externer VLC Player (Verlustfrei / ISO)",
        'dash': "Dynamic Adaptive Streaming over HTTP (High-End)",
        'webtorrent': "P2P WebTorrent Streaming (Dezentral)",
        'hls_native': "Natives HLS (Safari / Edge compatible)"
    }
    return mapping.get(mode, "Unbekannter Modus")
