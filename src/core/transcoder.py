import subprocess
import os
import threading
import logging
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable

logger = logging.getLogger("transcoder")

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
        task.status = "processing"
        
        try:
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
                    progress = self._parse_progress(line, task.task_type)
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
            logger.error(f"Transcode error: {e}")
        finally:
            if callback: callback(task_id, task.progress)

    def _build_handbrake_cmd(self, task: TranscodeTask) -> List[str]:
        # Basic HandBrakeCLI command
        cmd = ["HandBrakeCLI", "-i", task.input_path, "-o", task.output_path]
        
        encoder = task.options.get("encoder", "x264")
        if encoder == "nvenc": cmd += ["-e", "nvenc_h264"]
        elif encoder == "qsv": cmd += ["-e", "qsv_h264"]
        elif encoder == "vaapi": cmd += ["-e", "vaapi_h264"]
        else: cmd += ["-e", "x264"]

        preset = task.options.get("preset", "fast")
        cmd += ["--preset", preset]
        
        return cmd

    def _build_webm_cmd(self, task: TranscodeTask) -> List[str]:
        # FFmpeg VP9/WebM command
        cmd = [
            "ffmpeg", "-i", task.input_path,
            "-c:v", "libvpx-vp9", "-crf", "30", "-b:v", "0",
            "-c:a", "libopus", "-b:a", "128k",
            "-deadline", "realtime",
            "-y", task.output_path
        ]
        return cmd

    def _parse_progress(self, line: str, task_type: str) -> Optional[float]:
        if task_type == "handbrake":
            # Example: [20:05:10] reader: done. 10.50 %
            match = re.search(r"(\d+\.\d+)\s*%", line)
            if match: return float(match.group(1))
        elif task_type == "webm":
            # FFmpeg doesn't give easy % without duration context, but we can estimated
            # This is a simplified placeholder
            pass
        return None

    def get_task_status(self, task_id: str) -> Dict[str, Any]:
        with self._lock:
            task = self.tasks.get(task_id)
        if not task: return {"status": "not_found"}
        return {
            "status": task.status,
            "progress": task.progress,
            "error": task.error_message,
            "type": task.task_type
        }
