import subprocess
import os
import time
import requests # type: ignore
from src.core.logger import get_logger
log = get_logger("streams.vlc_bridge")

# Global dict to track vlc processes
VLC_PROCESSES = {}

def start_vlc_bridge(file_path, port=8080, password="admin"):
    """
    @brief Starts VLC with HTTP interface and HLS streaming for interactive playback.
    @details Essential for DVD/Blu-ray menus and advanced Atmos/Surround.
    @param file_path Source path (ISO or file).
    @param port HTTP control port.
    @return True if started.
    """
    if not os.path.exists(file_path):
        log.error(f"[VLC] File not found: {file_path}")
        return False

    log.info(f"[VLC] Starting Bridge for {file_path} on port {port}")

    # VLC command for HTTP control + HLS streaming
    # We use -I http for the web interface and --sout for the stream
    cmd = [
        "vlc",
        "-I", "http",
        "--http-port", str(port),
        "--http-password", password,
        str(file_path),
        "--sout", f"#transcode{{vcodec=h264,vb=800,scale=auto,acodec=aac,ab=128,channels=2,samplerate=44100}}:std{{access=livehttp,mux=mpegts,dst=web/streams/vlc/vlc.m3u8}}"
    ]

    try:
        # Ensure output directory exists
        os.makedirs("web/streams/vlc", exist_ok=True)
        
        process = subprocess.Popen(cmd)
        VLC_PROCESSES[port] = process
        return True
    except Exception as e:
        log.error(f"[VLC] Failed to start bridge: {e}")
        return False

def send_vlc_command(command, port=8080, password="admin"):
    """Sends a control command to the VLC HTTP interface."""
    url = f"http://127.0.0.1:{port}/requests/status.json?command={command}"
    try:
        response = requests.get(url, auth=("", password), timeout=2)
        return response.json()
    except Exception as e:
        log.error(f"[VLC] Command {command} failed: {e}")
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
