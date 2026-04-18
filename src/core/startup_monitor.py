#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
startup_monitor.py - Centralized Startup & Performance Profiling (v1.41.00)
Provides millisecond-accurate tracking of the Media Viewer bootstrap phases.
"""

import time
import os
import sys
import logging
from typing import List, Dict, Any, Optional

log = logging.getLogger("app.startup")

class StartupProfiler:
    """
    Singleton profiler for tracking bootstrap performance.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(StartupProfiler, cls).__new__(cls)
            # Use APP_START_TIME from main.py if available, otherwise now
            cls._instance.start_time = time.time()
            cls._instance.checkpoints = []
            cls._instance.phases = {}
            cls._instance.active_phase = None
        return cls._instance

    def set_base_time(self, base_time: float):
        """Overrides the initial start time from a very early boot stage."""
        self.start_time = base_time

    def log_checkpoint(self, msg: str, tag: str = "generic"):
        """Records a point-in-time event."""
        elapsed = time.time() - self.start_time
        self.checkpoints.append({
            "msg": msg,
            "elapsed": round(elapsed, 4),
            "tag": tag,
            "timestamp": time.time()
        })
        log.info(f"[Profiler] {elapsed:6.3f}s | {msg}")

    def start_phase(self, phase_name: str):
        """Starts timing a specific bootstrap phase."""
        if self.active_phase:
            self.end_phase(self.active_phase)
        
        self.active_phase = phase_name
        self.phases[phase_name] = {
            "start": time.time(),
            "end": None,
            "duration": None
        }
        log.info(f"[Profiler] >>> Starting Phase: {phase_name}")

    def end_phase(self, phase_name: str):
        """Ends timing a phase and calculates duration."""
        if phase_name in self.phases and self.phases[phase_name]["end"] is None:
            end_time = time.time()
            self.phases[phase_name]["end"] = end_time
            duration = end_time - self.phases[phase_name]["start"]
            self.phases[phase_name]["duration"] = round(duration, 4)
            log.info(f"[Profiler] <<< Finished Phase: {phase_name} (took {duration:.3f}s)")
            
            # Reset active phase if it matches
            if self.active_phase == phase_name:
                self.active_phase = None

    def get_report(self) -> Dict[str, Any]:
        """Generates a comprehensive JSON-ready report for the UI."""
        total_boot = time.time() - self.start_time
        
        # Hydration Metrics
        hydration_mode = "unknown"
        audit_stage = -1
        try:
            from src.core.config_master import GLOBAL_CONFIG
            hydr = GLOBAL_CONFIG.get("forensic_hydration_registry", {})
            hydration_mode = hydr.get("mode", "unknown")
            audit_stage = hydr.get("audit_stage", -1)
        except Exception:
            pass

        return {
            "total_boot_sec": round(total_boot, 3),
            "phases": self.phases,
            "checkpoints": self.checkpoints,
            "integrity_verified": hasattr(self, 'integrity_verified') and self.integrity_verified,
            "hydration": {
                "mode": hydration_mode,
                "audit_stage": audit_stage
            },
            "system_info": {
                "pid": os.getpid(),
                "python": sys.version.split()[0],
                "platform": sys.platform
            }
        }

    def mark_integrity_verified(self):
        """Signals that the pre-flight audit passed successfully."""
        self.integrity_verified = True
        self.log_checkpoint("System Integrity Verified", tag="integrity")

# Global singleton access
profiler = StartupProfiler()

def get_profiler():
    return profiler
