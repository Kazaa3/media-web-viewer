# [PLAN] Video Health: Live Worker Audit (v1.37.25)

## Objective
Implement a professional-grade process monitoring dashboard for the Video Health (VID) tab to provide observability into active transcoding workers.

---

## User Review Required
**NOTE:**
- **Process Observability:** This upgrade provides an instant technical overview of any background FFmpeg or MKVMerge processes currently active on your system that are being managed by the Media Viewer.

---

## Proposed Changes

### Backend (`main.py`)
- **[MODIFY]** Implement `get_active_video_workers()` Eel bridge.
- **Logic:** Scan for processes matching patterns (ffmpeg, mkvmerge) specifically initiated by the application's working directory.

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Ensure the VID (Video Health) tab header includes an [AUDIT WORKERS] trigger.
- Add a high-density viewport for the Active Worker Matrix.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement `runVideoWorkerAudit()`: handles the process-discovery handshake.
- Render the process list with PIDs, CPU/Memory (if available), and forensic status markers.
- Integrate with SENTINEL for persistent lifecycle logging.

---

## Open Questions
- Should the audit include a "Surgical Terminate" button per worker? (Recommendation: Add this for precise pipeline control, complementing the existing global "RECOVER PIPELINE" kill-switch).

---

## Verification Plan

### Automated Tests
- Verify `get_active_video_workers` accurately detects a dummy ffmpeg process started for testing.
- Confirm total PIDs listed match the system `ps aux` output for the relevant patterns.

### Manual Verification
- Navigate to VID tab → Click AUDIT WORKERS.
- Verify the Active Worker Matrix appears correctly with technical workstation styling.
- Start a video stream → Verify the new worker PID is instantly reflected in the audit matrix.
- Inspect the SENTINEL trace for the results.

---

## Implementation Checklist
- [ ] Implement get_active_video_workers() Eel bridge in main.py
- [ ] Add [AUDIT WORKERS] trigger and Active Worker Matrix viewport to diagnostics_sidebar.html
- [ ] Implement runVideoWorkerAudit() in sidebar_controller.js
- [ ] Render process list with PIDs, CPU/Memory, and status markers
- [ ] Integrate SENTINEL trace logging for all process audits

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
