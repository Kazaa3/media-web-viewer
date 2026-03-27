import logging
from .ffprobe_analyzer import ffprobe_analyze

# Specialized logger
log = logging.getLogger("mode_router")

def smart_route(file_path):
    """
    @brief The central decision engine for playback modes.
    @details Maps media analysis to one of the 5 primary streaming paths.
    @param file_path Path to the media file.
    @return String identifier of the chosen mode.
    """
    info = ffprobe_analyze(file_path)
    if "error" in info:
        log.warning(f"Routing fallback to direct_play due to analysis error: {info['error']}")
        return "direct_play"
    
    log.info(f"[Router] Analyzing {file_path}: Res={info['resolution']}, Codec={info['codec']}, ISO={info['is_iso']}")

    # Priority 1: Direct Play (0% CPU)
    # Native browser support: H.264/AAC in predictable containers
    # Note: We keep this strict for maximum reliability
    if info['codec'] == 'h264' and info['container'] in ['mp4', 'mov', 'm4a']:
        return 'direct_play'
    
    # Priority 2: VLC Bridge (Interactive Menus)
    # Essential for DVD/ISO with menus
    if info['is_iso'] or info['has_menus']:
        return 'vlc_bridge'
    
    # Priority 3: MSE fMP4 (0.5s Ultra-Fast)
    # Best for most SD/HD transcodes (MKV, AVI, etc.)
    # We use MSE for lower latency on non-4K content
    if info['resolution'] in ["SD", "720p", "1080p"] and not info['atmos']:
        return 'mse'
    
    # Priority 4: HLS fMP4 (Universal / High-End / 4K)
    # Best for 4K / Atmos / HDR to ensure buffer stability and multi-track handling
    return 'hls_fmp4'
