import subprocess
import os
import time
import requests # type: ignore
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Global dict to track vlc processes
log = get_logger("streams_vlc_bridge")
VLC_PROCESSES = {}

def start_vlc_bridge(file_path, port=8080):
    """
    @brief Starts VLC with HTTP interface and HLS streaming for interactive playback.
    @details Essential for DVD/Blu-ray menus and advanced Atmos/Surround.
    @param file_path Source path (ISO or file).
    @param port HTTP control port.
    @return True if started.
    """
    if not os.path.exists(file_path):
        log.error(f"[VLC-Bridge] File not found: {file_path}")
        return False

    # Pull configuration (Phase 9 Centralization)
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {}).get("video", {})
    flags = reg.get("orchestration_flags", {}).get("vlc_bridge", {})
    
    password = flags.get("http_password", "admin")
    sout_template = flags.get("sout_template", "#transcode{vcodec=h264,vb=800,scale=auto,acodec=aac,ab=128,channels=2,samplerate=44100}:std{access=livehttp,mux=mpegts,dst=web/streams/vlc/vlc.m3u8}")

    log.info(f"[VLC-Bridge] Starting Bridge for {file_path} on port {port} (Trace: {password[:1]}***)")

    # VLC command for HTTP control + HLS streaming
    cmd = [
        "vlc",
        "-I", "http",
        "--http-port", str(port),
        "--http-password", password,
        str(file_path),
        "--sout", sout_template
    ]

    try:
        # Ensure output directory exists (Centralized Path)
        out_dir = Path("web/streams/vlc")
        out_dir.mkdir(parents=True, exist_ok=True)
        
        process = subprocess.Popen(cmd)
        VLC_PROCESSES[port] = process
        return True
    except Exception as e:
        log.error(f"[VLC] Failed to start bridge: {e}", exc_info=True)
        return False

def send_vlc_command(command, port=8080):
    """Sends a control command to the VLC HTTP interface."""
    reg = GLOBAL_CONFIG.get("media_pipeline_registry", {}).get("video", {})
    password = reg.get("orchestration_flags", {}).get("vlc_bridge", {}).get("http_password", "admin")
    
    url = f"http://127.0.0.1:{port}/requests/status.json?command={command}"
    try:
        response = requests.get(url, auth=("", password), timeout=2)
        return response.json()
    except Exception as e:
        log.error(f"[VLC-Bridge] Command {command} failed: {e}", exc_info=True)
        return {"error": str(e)}

def stop_vlc_bridge(port=8080):
    """Stops the VLC bridge."""
    process = VLC_PROCESSES.pop(port, None)
    if process:
        if hasattr(process, "terminate"):
            process.terminate()
            try:
                process.wait(timeout=3)
            except:
                process.kill()
        return True
    return False

