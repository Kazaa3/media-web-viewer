import subprocess
import logging
import bottle
import time
from .utils import get_best_ffmpeg_encoder, get_base_ffmpeg_args, get_video_filter
from src.core.ffprobe_analyzer import ffprobe_analyze

# Specialized logger
log = logging.getLogger("streams.mse")

def stream_mse(file_path, audio_idx=0, subs_idx=None, start_time=0):
    """
    @brief Fragmented MP4 stream for MediaSource Extensions (Video.js).
    @details Provides ultra-low latency (0.5s) by avoiding HLS segmentation.
    @param file_path Path to the media file.
    @param audio_idx Index of the audio track to include.
    @param subs_idx Optional index of subtitle track to burn.
    @param start_time Seek position in seconds.
    @return Generator for streaming binary data.
    """
    analysis = ffprobe_analyze(file_path)
    if "error" in analysis:
        log.error(f"[MSE-Stream] Analysis failed: {analysis['error']}")
        return bottle.HTTPError(404, f"Analysis failed: {analysis['error']}")

    is_4k = analysis.get("resolution") == "4K"
    is_hd = analysis.get("resolution") == "1080p" or analysis.get("resolution") == "720p"
    
    encoder = get_best_ffmpeg_encoder()
    cmd = get_base_ffmpeg_args(encoder)
    
    if float(start_time or 0) > 0:
        cmd += ["-ss", str(start_time), "-output_ts_offset", str(start_time)]
        
    # Input handling (bluray support if ISO)
    input_src = str(file_path)
    if str(file_path).lower().endswith('.iso') and analysis.get('bitrate', 0) > 20000000:
        input_src = f"bluray:{file_path}"

    cmd += ["-i", input_src]
    
    # Stream Mapping
    cmd += ["-map", "0:v:0", "-map", f"0:a:{audio_idx}"]
    
    # Filters
    vf = get_video_filter(analysis, subs_idx, is_4k)
    
    # Subtitle Burning Heuristic
    if subs_idx is not None:
        try:
            # Handle subtitle burn
            esc_path = str(file_path).replace("\\", "/").replace(":", "\\:")
            vf.append(f"subtitles='{esc_path}':si={subs_idx}")
        except: pass

    # Bitrate selection
    if is_4k: max_rate, buf_size = "15M", "30M"
    elif is_hd: max_rate, buf_size = "8M", "16M"
    else: max_rate, buf_size = "4M", "8M"

    # Encoder specific tuning
    if encoder == "h264_vaapi":
        vf.insert(0, "format=nv12,hwupload")
        cmd += ["-vf", ",".join(vf)]
        v_rate = "12M" if is_4k else "6M"
        cmd += ["-c:v", "h264_vaapi", "-b:v", v_rate, "-maxrate", v_rate, "-hwaccel_output_format", "vaapi"]
        if is_4k: cmd += ["-level", "5.1"]
    elif encoder == "h264_nvenc":
        if vf: cmd += ["-vf", ",".join(vf)]
        cmd += ["-c:v", "h264_nvenc", "-preset", "p1", "-tune", "hq", "-rc", "vbr", "-cq", "24", 
                "-maxrate", max_rate, "-bufsize", buf_size, "-profile:v", "high"]
    else:
        if vf: cmd += ["-vf", ",".join(vf)]
        cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-preset", "ultrafast", "-tune", "zerolatency", 
                "-crf", "25", "-maxrate", max_rate, "-bufsize", buf_size, "-profile:v", "high"]

    # Output Format: Fragmented MP4 for MSE
    cmd += [
        "-c:a", "aac", "-b:a", "128k", "-ac", "2",
        "-f", "mp4", "-movflags", "frag_keyframe+empty_moov+default_base_moof",
        "pipe:1"
    ]
    
    log.info(f"[MSE-Stream] Launching: {' '.join(cmd)}")
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    bottle.response.content_type = 'video/mp4'
    def stream():
        try:
            while True:
                data = process.stdout.read(1024 * 64)
                if not data:
                    if process.poll() is not None: break
                    continue
                yield data
        except Exception as e:
            log.error(f"[MSE-Stream] Runtime error: {e}")
        finally:
            if process.poll() is None:
                process.terminate()
                try: process.wait(timeout=1)
                except: process.kill()
            
    return stream()
