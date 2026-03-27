import subprocess
import os
import threading
import logging
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

from src.core.logger import get_logger
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

            logger.info(f"Starting transcode: {' '.join(cmd)}")
            task.process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True
            )

            if task.process.stdout:
                for line in task.process.stdout:
                    line = line.strip()
                    if not line: continue
                    
                    # Store in log buffer
                    task.log_buffer.append(line)
                    if len(task.log_buffer) > 1000: task.log_buffer.pop(0)
                    
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
        # Basic HandBrakeCLI command
        cmd = ["HandBrakeCLI", "-i", task.input_path, "-o", task.output_path]
        
        encoder = task.options.get("encoder", "auto")
        if encoder == "auto":
            encoder = self._auto_select_encoder()
            
        if encoder == "nvenc": cmd += ["-e", "nvenc_h264"]
        elif encoder == "qsv": cmd += ["-e", "qsv_h264"]
        elif encoder == "vaapi": cmd += ["-e", "vaapi_h264"]
        else: cmd += ["-e", "x264"]

        preset = task.options.get("preset", "fast")
        cmd += ["--preset", preset]
        
        return cmd

    def _build_webm_cmd(self, task: TranscodeTask) -> List[str]:
        # FFmpeg VP9/WebM command
        # Auto-detect encoder for webm too if needed
        from src.core import hardware_detector
        gpu_info = hardware_detector.get_gpu_info()
        encoders = gpu_info.get("encoders", [])
        
        cmd = ["ffmpeg", "-i", task.input_path]
        
        # Check for HW acceleration for VP9 if available
        # (Standard webm uses VP9)
        cmd += ["-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0"]
        cmd += ["-c:a", "libopus", "-b:a", "128k"]
        cmd += ["-deadline", "realtime", "-y", task.output_path]
        return cmd

    def _get_duration(self, task: TranscodeTask):
        """Usee ffprobe to get duration in seconds."""
        try:
            cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", task.input_path]
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
