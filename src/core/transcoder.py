import subprocess
import os
import threading
import logging
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

from src.core.logger import get_logger
from src.core.config_master import GLOBAL_CONFIG
log = get_logger("transcoder")

class TranscodeTask:
    def __init__(self, input_path: str, output_path: str, task_type: str, options: Dict[str, Any]):
        self.input_path = input_path
        self.output_path = output_path
        self.task_type = task_type  # 'handbrake' or 'webm'
        self.options = options
        self.progress = 0.0
        self.status = "queued"  # queued, processing, completed, error
        self.error_message = ""
        self.process: Optional[subprocess.Popen] = None
        self.log_buffer: List[str] = []
        self.duration: float = 0.0

class TranscoderManager:
    def __init__(self):
        self.tasks: Dict[str, TranscodeTask] = {}
        self.active_task_id: Optional[str] = None
        self._lock = threading.Lock()

    def add_task(self, input_path: str, output_path: str, task_type: str, options: Dict[str, Any]) -> str:
        task_id = str(hash(input_path + output_path + str(os.times())))
        task = TranscodeTask(input_path, output_path, task_type, options)
        with self._lock:
            self.tasks[task_id] = task
        return task_id

    def start_task(self, task_id: str, callback: Optional[Callable[[str, float], None]] = None):
        with self._lock:
            task = self.tasks.get(task_id)
        if not task: return

        thread = threading.Thread(target=self._run_task, args=(task_id, task, callback))
        thread.start()

    def _run_task(self, task_id: str, task: TranscodeTask, callback: Optional[Callable[[str, float], None]]):
        try:
            # Get duration for progress tracking
            self._get_duration(task)
            
            if task.task_type == "handbrake":
                cmd = self._build_handbrake_cmd(task)
            elif task.task_type == "webm":
                cmd = self._build_webm_cmd(task)
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")

            log.info(f"Starting transcode: {' '.join(cmd)}")
            task.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True
            )

            if task.process.stdout:
                for line in task.process.stdout:
                    line = line.strip()
                    if not line: continue
                    
                    # Store in log buffer
                    task.log_buffer.append(line)
                    max_size = GLOBAL_CONFIG.get("perf_settings", {}).get("transcoder_log_size", 1000)
                    if len(task.log_buffer) > max_size: task.log_buffer.pop(0)
                    
                    # Log to system logger for UI visibility
                    if task.task_type == "handbrake":
                        log.info(f"🚀 [HandBrake] {line}")
                    elif task.task_type == "webm":
                        log.info(f"🌐 [WebM] {line}")

                    progress = self._parse_progress(line, task)
                    if progress is not None:
                        task.progress = progress
                        if callback: callback(task_id, progress)

            task.process.wait()
            if task.process.returncode == 0:
                task.status = "completed"
                task.progress = 100.0
            else:
                task.status = "error"
                task.error_message = f"Process returned {task.process.returncode}"

        except Exception as e:
            task.status = "error"
            task.error_message = str(e)
            log.error(f"Transcode error: {e}")
        finally:
            if callback: callback(task_id, task.progress)

    def _auto_select_encoder(self) -> str:
        """Autodetect best hardware encoder using the hardware_detector."""
        from src.core import hardware_detector
        gpu_info = hardware_detector.get_gpu_info()
        encoders = gpu_info.get("encoders", [])
        
        if "nvenc" in encoders: return "nvenc"
        if "qsv" in encoders: return "qsv"
        if "vaapi" in encoders: return "vaapi"
        return "x264" # Default software fallback

    def _build_handbrake_cmd(self, task: TranscodeTask) -> List[str]:
        # HandBrakeCLI with GPU support and optimized parameters
        from src.core.config_master import GLOBAL_CONFIG
        hb_bin = GLOBAL_CONFIG["program_paths"].get("handbrake", "HandBrakeCLI")
        settings = GLOBAL_CONFIG.get("transcoding_settings", {}).get("handbrake_settings", {})
        
        cmd = [hb_bin, "-i", task.input_path, "-o", task.output_path]
        
        encoder = task.options.get("encoder", "auto")
        if encoder == "auto":
            encoder = self._auto_select_encoder()
            
        # GPU Encoders (v1.41.00 Centralized)
        encoder_map = settings.get("encoder_map", {})
        cmd += ["-e", encoder_map.get(encoder, encoder_map.get("fallback", "x264"))]

        # Additional optimizations for batch encoding
        preset = task.options.get("preset", settings.get("preset", "fast"))
        cmd += ["--preset", preset]
        
        # Audio Passthrough
        cmd += ["--aencoder", settings.get("a_encoder", "copy")]
        
        # Subtitle Passthrough
        if settings.get("subtitle_scan"):
            cmd += ["--subtitle", "scan", "--native-language", settings.get("native_lang", "ger")]
            if settings.get("native_dub"):
                cmd += ["--native-dub"]
        
        # Performance flags
        if settings.get("markers"):
            cmd += ["--markers"]
        
        return cmd

    def add_batch_tasks(self, file_pairs: List[Dict[str, str]], options: Dict[str, Any]) -> List[str]:
        """Adds a list of transcoding tasks as a batch."""
        task_ids = []
        for pair in file_pairs:
            input_p = pair.get("input")
            output_p = pair.get("output")
            if input_p and output_p:
                task_ids.append(self.add_task(input_p, output_p, "handbrake", options))
        return task_ids

    def _build_webm_cmd(self, task: TranscodeTask) -> List[str]:
        # FFmpeg VP9/WebM command with HW acceleration if available (v1.41.00)
        from src.core.config_master import GLOBAL_CONFIG
        ffmpeg_bin = GLOBAL_CONFIG["program_paths"].get("ffmpeg", "ffmpeg")
        settings = GLOBAL_CONFIG.get("transcoding_settings", {}).get("webm_settings", {})
        
        cmd = [ffmpeg_bin, "-hide_banner", "-loglevel", "error", "-i", task.input_path]
        
        from src.core import hardware_detector
        gpu_info = hardware_detector.get_gpu_info()
        encoders = gpu_info.get("encoders", [])
        
        # VP9 HW Encoders (if available via ffmpeg)
        v_codec = settings.get("v_codec", "libvpx-vp9")
        v_codec_hw = settings.get("v_codec_hw", "vp9_nvenc")
        
        if "nvenc" in encoders:
            # Note: nvenc supports hevc/h264, vp9 support depends on hardware
            # Use subprocess to check runtime availability of the hw encoder
            try:
                check_cmd = [ffmpeg_bin, "-encoders"]
                encoder_list = str(subprocess.run(check_cmd, capture_output=True, text=True).stdout)
                if v_codec_hw in encoder_list:
                    v_codec = v_codec_hw
            except Exception:
                pass
        
        cmd += ["-c:v", v_codec]
        cmd += ["-crf", settings.get("crf", "30"), "-b:v", settings.get("bitrate_v", "0")]
        cmd += ["-c:a", settings.get("a_codec", "libopus"), "-b:a", settings.get("bitrate_a", "128k")]
        cmd += ["-deadline", settings.get("deadline", "realtime"), "-row-mt", settings.get("row_mt", "1")]
        cmd += ["-y", task.output_path]
        return cmd

    def _get_duration(self, task: TranscodeTask):
        """Use ffprobe to get duration in seconds (v1.41.00)."""
        try:
            from src.core.config_master import GLOBAL_CONFIG
            ffprobe_bin = GLOBAL_CONFIG["program_paths"].get("ffprobe", "ffprobe")
            cmd = [ffprobe_bin, "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", task.input_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                task.duration = float(result.stdout.strip())
        except Exception as e:
            log.warning(f"Could not get duration for {task.input_path}: {e}")

    def _parse_progress(self, line: str, task: TranscodeTask) -> Optional[float]:
        if task.task_type == "handbrake":
            # Example: [20:05:10] reader: done. 10.50 %
            match = re.search(r"(\d+\.\d+)\s*%", line)
            if match: return float(match.group(1))
        elif task.task_type == "webm" and task.duration > 0:
            # FFmpeg example: time=00:00:15.50
            match = re.search(r"time=(\d+):(\d+):(\d+\.\d+)", line)
            if match:
                hours, minutes, seconds = map(float, match.groups())
                current_time = hours * 3600 + minutes * 60 + seconds
                progress = (current_time / task.duration) * 100
                return min(100.0, progress)
        return None

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        with self._lock:
            task = self.tasks.get(task_id)
        if not task: return {"status": "not_found"}
        return {
            "status": task.status,
            "progress": task.progress,
            "error": task.error_message,
            "type": task.task_type,
            "logs": task.log_buffer[-50:]  # Return last 50 lines of logs
        }
