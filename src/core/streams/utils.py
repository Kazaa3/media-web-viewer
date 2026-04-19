import subprocess
from pathlib import Path
from src.core import hardware_detector
from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG

# Specialized logger (v1.46.132 Modernized)
log = get_logger("streams_utils")

def get_best_ffmpeg_encoder():
    """
    @brief Returns the best available H.264 encoder for FFmpeg (HW or SW).
    @details Prefers NVENC > QSV > VAAPI > libx264.
    """
    try:
        gpu_info = hardware_detector.get_gpu_info()
        encoders = gpu_info.get("encoders", [])
        if "nvenc" in encoders: return "h264_nvenc"
        if "qsv" in encoders: return "h264_qsv"
        if "vaapi" in encoders: return "h264_vaapi"
    except Exception as e:
        log.warning(f"[HW-Detect] Failed, falling back to libx264: {e}", exc_info=True)
    return "libx264"

def get_base_ffmpeg_args(encoder):
    """
    @brief Returns base FFmpeg arguments for a given encoder. Includes device mapping.
    @details (v1.46.132) Pulse-aware VAAPI device configuration.
    """
    args = ["ffmpeg", "-hide_banner", "-loglevel", "error"]
    if encoder == "h264_vaapi":
        # Pull from config instead of hardcoding (Phase 9 Centralization)
        hw_cfg = GLOBAL_CONFIG.get("hardware_info", {})
        vaapi_dev = hw_cfg.get("vaapi_device", "/dev/dri/renderD128")
        args += ["-vaapi_device", vaapi_dev]
    return args

def get_video_filter(analysis, subs_idx=None, is_4k=False):
    """
    @brief Generates FFmpeg video filter chain based on analysis.
    """
    vf = []
    scan = analysis.get("scan_type", "progressive").lower()
    
    # Deinterlacing for PAL/SD or ISOs
    if (scan != "progressive" or analysis.get("is_iso")) and not is_4k:
        vf.append("yadif=0:-1:0")

    # Hardware acceleration specific filters
    return vf
