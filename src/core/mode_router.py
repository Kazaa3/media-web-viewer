import logging
from src.core.ffprobe_analyzer import ffprobe_analyze # type: ignore

# Specialized logger
log = logging.getLogger("mode_router")

def smart_route(file_path):
    """
    @brief The central decision engine for playback modes.
    @details Maps media analysis to one of the 8+ primary streaming paths.
    @param file_path Path to the media file.
    @return String identifier of the chosen mode.
    """
    info = ffprobe_analyze(file_path)
    if "error" in info:
        log.warning(f"Routing fallback to direct_play due to analysis error: {info['error']}")
        return "direct_play"
    
    log.info(f"[Router] Analyzing {file_path}: Res={info['resolution']}, Codec={info['codec']}, Atmos={info['atmos']}, ISO={info['is_iso']}")

    # Priority 1: Direct Play (0.1s Latenz, 0% CPU)
    # Native support in Chrome/Video.js: H.264/AAC in predictable containers
    if info['codec'] == 'h264' and info['container'] in ['mp4', 'mov', 'm4a', 'quicktime']:
        if info['resolution'] != "4K": # 1080p and below
            return 'direct_play'
    
    # Priority 2: VLC Bridge (3s Latenz, 15% CPU)
    # Essential for DVD/ISO with menus or Atmos through bridge
    if info['is_iso'] or info['has_menus'] or info['atmos']:
        return 'vlc_bridge'
    
    # Priority 3: MPV.js WASM (2s Latenz, Browser-side)
    # Interactive menu support inside the browser (Fallback if VLC bridge is not preferred)
    # We might use this for smaller ISOs or specific user requests.
    
    # Priority 4: MSE fMP4 (0.5s Latenz, 20% CPU)
    # Low-latency fragmented remuxing for MKV, AVI, etc. (SD/HD)
    if info['resolution'] in ["SD", "720p", "1080p"]:
        return 'mse'
    
    # Priority 5: HLS fMP4 (2s Latenz, 25% CPU)
    # Universal fallback for 4K / HDR / High-End content or Multi-Client support
    mode = 'hls_fmp4'
    
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
        'mpv_wasm': "libmpv zu Canvas (WASM / Interaktiv)"
    }
    return mapping.get(mode, "Unbekannter Modus")
