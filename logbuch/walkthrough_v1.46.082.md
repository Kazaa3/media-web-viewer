# Walkthrough: Global Process Forensics (v1.46.082)

## Date: 2026-04-19

---

## Key Accomplishments

### 1. Unified Forensic Probe (`get_system_forensics`)
- **Implementation:** Expanded the forensic engine in `main.py` to scan for a suite of critical media binaries.
- **Targets:** Now monitors FFmpeg, VLC, FFplay, FFprobe, MediaInfo, and Mkvmerge.
- **Resilience:** Uses a dual-stage scan: a recursive child-check (for processes triggered directly by Eel) and a global process fallback (for detached external windows like VLC).

### 2. Multi-LED Forensic HUD
- **Mechanism:** Updated `version.js` to pipe different forensic streams into the footer:
  - **FE LED:** Tracks the Browser Frontend PID and Engine Identity.
  - **BE LED:** Tracks the Backend PID and all Active Media Tools (with their respective PIDs).

### 3. Dynamic Tool Audit
- **Result:** The BE HUD tooltip now acts as a real-time monitor for background activity. If you start a transcode or launch a file in VLC, the PID will appear in the HUD automatically during the next synchronization pulse.

---

## Verification Summary

### Tool Sensitivity
- Confirmed that starting ffmpeg manually or via the UI triggers an "ACTIVE: FFMPEG" status in the HUD.
- Confirmed that VLC is detected even if launched as an independent system process.

### Versioning
- The system identity is now formally synchronized to v1.46.082-EVO-STABLE.

---

## TIP
**HOW TO AUDIT:** Restart the application, start a video transcode, and hover over the BE LED in the bottom-left cluster. You will see the active FFmpeg PID in real-time.
