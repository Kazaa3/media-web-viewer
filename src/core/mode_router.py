import eel
import os
from src.core.ffprobe_analyzer import ffprobe_analyze # type: ignore
from src.core.logger import get_logger
log = get_logger("mode_router")

@eel.expose
def smart_route(file_path):
    """
    @brief The central decision engine for playback modes.
    @details Maps media analysis to one of the 8+ primary streaming paths.
    @param file_path Path to the media file.
    @return Dictionary with 'mode' and 'info' and 'reason'.
    """
    log.info(f"[PLAY-PULSE] smart_route analysis started for: {file_path}")
    info = ffprobe_analyze(file_path)
    if "error" in info:
        log.warning(f"[PLAY-PULSE] Routing fallback to direct_play due to analysis error: {info['error']}")
        return {"mode": "direct_play", "info": info, "reason": "Analysis Error Fallback"}

    # --- [v1.46.052] EMERGENCY AUDIO REPAIR ---
    # Fix for: "repariere. alles sodass mp3s abgespielt werden"
    if info.get('has_audio') and not info.get('has_video'):
        reason = "Audio Direct Play (Bypass)"
        log.info(f"[PLAY-PULSE] Routing Audio: {os.path.basename(file_path)} -> direct_play")
        return {"mode": "direct_play", "info": info, "reason": reason}

    # 0. Load Configuration (v1.46.052 Ultimate Matrix)
    from src.core.config_master import GLOBAL_CONFIG
    item_name = os.path.basename(file_path)
    
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {}).get("video", {})
    flags = reg.get("orchestration_flags", {})
    thresholds = reg.get("bitrate_thresholds", {})
    
    # Extract Matrix Tiers
    steering_s = flags.get("special_format_steering", {})
    steering_f = flags.get("frequency_steering", {})
    steering_c = flags.get("codec_steering", {})
    steering_r = flags.get("resolution_steering", {})
    
    # Analysis
    codec = info.get('codec', 'unknown')
    container = info.get('container', 'unknown')
    resolution = info.get('resolution', 'SD')
    bitrate = info.get('bitrate_kbps', 0)
    subtype = info.get('media_subtype', 'FILE')
    
    # Hardware Awareness
    hw_info = GLOBAL_CONFIG.get("hardware_info", {})
    hevc_hw = hw_info.get("hevc_hw_decoding_available", False)
    is_easy_container = container in ['mp4', 'mkv', 'webm', 'mov', 'ts']
    
    # 1. Mandatory Hardware Safety Guard (4K HEVC)
    if resolution == "4K" and info.get('is_hevc'):
        if not hevc_hw:
            log.warning(f"[PLAY-PULSE] 4K HEVC Detect: Hardware decoder missing! Forensic error triggered.")
            return {
                "mode": "error_hardware", 
                "message": "Transcoding of 4K HEVC requires hardware support (QSV/VAAPI/NVDEC).",
                "info": info
            }
        else:
            reason = "4K HEVC Mandatory Hardware Path"
            mode = 'direct_play' if bitrate < thresholds.get("direct_play_max_kbps", 20000) else 'mpv_native'
            return {"mode": mode, "info": info, "reason": reason}

    # 2. Priority: Special Format Steering (3D Sonderfall)
    if info.get('is_3d'):
        s_policy = steering_s.get("3d", "auto")
        if s_policy != "auto":
            mode = 'vlc_bridge' if s_policy == "menu" else 'mse' if s_policy == "mse" else 'mpv_native' if s_policy == "native" else 'hls_fmp4'
            reason = f"Special Format Steering (3D -> {s_policy})"
            return {"mode": mode, "info": info, "reason": reason}
        else:
            # Default 3D behavior (often requires special depth handling)
            return {"mode": "vlc_bridge", "info": info, "reason": "3D Standard Routing"}

    # 3. Priority: Frequency Master Overrides (PAL-50Hz vs NTSC-60Hz)
    f_policy = "auto"
    if info.get('is_pal'): f_policy = steering_f.get("pal_50hz", "auto")
    elif info.get('is_ntsc'): f_policy = steering_f.get("ntsc_60hz", "auto")
    
    if f_policy != "auto":
        mode = 'direct_play' if f_policy == "direct" else 'mse' if f_policy == "mse" else 'mpv_native' if f_policy == "native" else 'hls_fmp4'
        reason = f"Frequency Master Override ({'PAL' if info.get('is_pal') else 'NTSC'} -> {f_policy})"
        return {"mode": mode, "info": info, "reason": reason}
    
    # 4. Priority: Granular Manual Overrides (Resolution & Codec Matrix)
    c_policy = steering_c.get(codec.replace("h265", "hevc"), "auto")
    
    # Dynamic Resolution Key Generation (High-Fidelity)
    suffix = 'i' if info.get('is_interlaced') else 'p'
    r_key = "auto"
    if resolution == "SD":
        r_key = "sd_pal" if info.get('is_pal') else "sd_ntsc" if info.get('is_ntsc') else "sd_p"
    elif resolution == "4K":
        r_key = "2160p"
    else:
        # Generate keys like "720p", "1080i"
        base_res = str(resolution).lower().replace("p", "").replace("i", "")
        if base_res in ["720", "1080"]:
            r_key = f"{base_res}{suffix}"
    
    r_policy = steering_r.get(r_key, "auto")

    if c_policy != "auto":
        mode = 'direct_play' if c_policy == "direct" else 'mse' if c_policy == "mse" else 'hls_fmp4'
        reason = f"Manual Codec Steering ({codec} -> {c_policy})"
        return {"mode": mode, "info": info, "reason": reason}
    
    if r_policy != "auto":
        mode = 'direct_play' if r_policy == "direct" else 'mse' if r_policy == "mse" else 'mpv_native' if r_policy == "native" else 'hls_fmp4'
        reason = f"Manual Resolution Steering ({r_key} -> {r_policy})"
        return {"mode": mode, "info": info, "reason": reason}

    # 5. Fallback Heuristics (Standard Digital)
    direct_limit = thresholds.get("direct_play_max_kbps", 20000)
    if codec == 'h264' and is_easy_container:
        if resolution != "4K" and bitrate < direct_limit:
            mode = 'direct_play'
            reason = "Direct Play (Easy Container/Bitrate)"
            return {"mode": mode, "info": info, "reason": reason}
            
    if bitrate < thresholds.get("mse_max_kbps", 15000) and codec in ['h264', 'vp9', 'av1']:
        mode = 'mse'
        reason = "MSE Standard Heuristic"
    else:
        mode = 'hls_fmp4'
        reason = "HLS/fMP4 Standard Heuristic (Fallback)"

    log.info(f"[PLAY-PULSE] Final Routing ({item_name}): {mode} | Reason: {reason} | Subtype: {subtype}")
    return {"mode": mode, "info": info, "reason": reason}

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
