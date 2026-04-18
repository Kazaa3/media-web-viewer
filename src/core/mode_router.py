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

    # Analysis
    codec = info.get('codec', 'unknown')
    container = info.get('container', 'unknown')
    resolution = info.get('resolution', 'SD')
    bitrate = info.get('bitrate_kbps', 0)
    
    # Defaults
    mode = 'hls_fmp4'
    
    # 1. Native Direct Play (Chrome compatible)
    if codec == 'h264' and container in ['mp4', 'mov', 'm4a', 'quicktime']:
        if resolution != "4K" and bitrate < 20000:
            mode = 'direct_play'
            
    # 2. MSE (H.264 / VP9 / AV1 in various containers)
    elif resolution in ["SD", "720p", "1080p"] and bitrate < 15000:
        if codec in ['h264', 'vp9', 'av1']:
            mode = 'mse'
            
    # 3. VLC Bridge (ISO / Heavy Containers / Atmos)
    elif info.get('is_iso') or info.get('has_menus') or info.get('atmos') or container == 'ts':
        mode = 'vlc_bridge'
        
    # 4. DASH (Experimental high-bitrate)
    elif container == 'mpd' or (resolution == '4K' and bitrate > 30000):
        mode = 'dash'
        
    # 5. MPV WASM (Interactive / libmpv features)
    elif info.get('is_interactive') or container == 'webm':
        mode = 'mpv_wasm'

    # 6. Fallback to Native External (Ultra high-end)
    if resolution == '4K' and bitrate > 50000:
        mode = 'mpv_native'

    log.info(f"[PLAY-PULSE] smart_route decision: {mode} | Codec: {codec} | Res: {resolution}")
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
