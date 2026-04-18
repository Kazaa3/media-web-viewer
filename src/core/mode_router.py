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
    
    # Defaults
    mode = 'hls_fmp4'
    reason = "Fallback (HLS/fMP4)"
    
    # [v1.46.048] Hardware & Complexity Matrix
    hw_info = GLOBAL_CONFIG.get("hardware_info", {})
    hevc_hw = hw_info.get("hevc_hw_decoding_available", False)
    subtype = info.get('media_subtype', 'FILE')
    
    is_easy_container = container in ['mp4', 'mkv', 'webm', 'mov', 'ts']
    is_complex_media = subtype.startswith(("DVD", "BD")) or info.get('is_3d')
    
    # 1. 4K HEVC Mandatory Hardware Check (Forensic Policy)
    if resolution == "4K" and info.get('is_hevc'):
        if not hevc_hw:
            # 4K HEVC is too heavy for software transcode. Warn and steer to native if possible or error.
            log.warning(f"[PLAY-PULSE] 4K HEVC Detect: Hardware decoder missing! Forensic error triggered.")
            return {
                "mode": "error_hardware", 
                "message": "Transcoding of 4K HEVC requires hardware support (QSV/VAAPI/NVDEC).",
                "info": info
            }
        else:
            reason = "4K HEVC (Hardware Supported)"
            mode = 'direct_play' if bitrate < thresholds.get("direct_play_max_kbps", 20000) else 'mpv_native'

    # 2. Priority: Physical Media & Specialized Steering (COMPLEX)
    elif is_complex_media:
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

    # 3. HEVC HD Steering Policy (Resolution-Aware)
    elif resolution in ["1080p", "720p"] and info.get('is_hevc'):
        if flags.get("hevc_force_transcode_on_hd", True):
            mode = 'mse' if bitrate < thresholds.get("mse_max_kbps", 15000) else 'hls_fmp4'
            reason = "HEVC HD Force-Transcode Policy"
        else:
            mode = 'direct_play'
            reason = "HEVC HD Native (Policy: Direct)"

    # 4. Standard Digital Steering (EASY)
    else:
        # Native Direct Play (Chrome compatible)
        direct_limit = thresholds.get("direct_play_max_kbps", 20000)
        if codec == 'h264' and is_easy_container:
            if resolution != "4K" and bitrate < direct_limit:
                mode = 'direct_play'
                reason = "Direct Play (Easy Container/Bitrate)"
                
        # MSE / HLS Fallback
        elif bitrate < thresholds.get("mse_max_kbps", 15000) and codec in ['h264', 'vp9', 'av1']:
            mode = 'mse'
            reason = "MSE Transcode (Easy/Standard)"
            
        # MPV WASM (Interactive)
        if info.get('is_interactive') or (container == 'webm' and flags.get("prefer_mpv_wasm_for_webm", True)):
            mode = 'mpv_wasm'
            reason = "MPV WASM (Interactive/WebM)"

    log.info(f"[PLAY-PULSE] smart_route decision: {mode} | Subtype: {subtype} | HW-HEVC: {hevc_hw} | Reason: {reason} (v1.46.048)")
 
    return {
        "mode": mode,
        "info": info
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
