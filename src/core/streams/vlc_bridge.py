import subprocess
import logging
import time
import os
import bottle
import shutil
from pathlib import Path

# Specialized logger
log = logging.getLogger("streams.vlc")

def start_vlc_hls_bridge(file_path):
    """
    @brief Starts a VLC instance that transcodes ISO/DVD to HLS for the browser.
    @details Enables interactive menus by bridging VLC's engine to an HLS stream.
    @param file_path Path to the ISO/DVD file.
    @return URL to the HLS playlist or None if failed.
    """
    output_dir = Path("/tmp/mwv_vlc_hls")
    if output_dir.exists():
        try: shutil.rmtree(output_dir)
        except: pass
    output_dir.mkdir(parents=True, exist_ok=True)
    
    playlist_name = "playlist.m3u8"
    playlist_path = output_dir / playlist_name
    
    # VLC command to stream HLS via sout
    # We use a standard H.264/AAC transcode compatible with Video.js
    vlc_bin = shutil.which("cvlc") or shutil.which("vlc") or "vlc"
    
    # sout-chain for livehttp (HLS)
    sout = (
        f"#transcode{{vcodec=h264,vb=4000,acodec=mp4a,ab=128,channels=2,samplerate=44100}}:"
        f"std{{access=livehttp{{seglen=4,deldone=true,num_segs=10,"
        f"index={playlist_path},index-url=segment-####.ts}},"
        f"mux=ts,dst={output_dir}/segment-####.ts}}"
    )
    
    cmd = [
        vlc_bin, "-I", "dummy", 
        "--no-osd", "--no-stats", "--no-video-title-show",
        str(file_path),
        "--sout", sout,
        "vlc://quit"
    ]
    
    log.info(f"[VLC-Bridge] Launching VLC HLS: {' '.join(cmd)}")
    # We use Popen so it runs in background
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Polling for playlist availability
    max_retries = 15
    for i in range(max_retries):
        if playlist_path.exists():
            log.info(f"[VLC-Bridge] HLS Playlist ready after {i}s")
            return f"/vlc_tmp/{playlist_name}"
        time.sleep(1)
        
    log.error("[VLC-Bridge] Failed to generate HLS playlist within timeout.")
    return None

def serve_vlc_hls(path):
    """
    @brief Bottle route handler for VLC HLS segments and playlists.
    """
    return bottle.static_file(path, root="/tmp/mwv_vlc_hls")
