# Video Health: Live Worker Audit Walkthrough (v1.37.25)

Successfully upgraded the VID (Video Health) diagnostics suite with a professional-grade process monitoring dashboard.

---

## Forensic Worker Features

### 1. Live Worker Matrix
- **Action:** Open the VID tab and click [AUDIT WORKERS].
- **The Dashboard:** Instantly identifies active background media processes.
- **Worker ID (PID):** The system process identifier.
- **Worker Name:** FFmpeg or MKVMerge instance.
- **Context Check:** Chromatic markers (Green/Yellow) indicate if the process was initiated by the current application environment.

### 2. Surgical Process Control
- **Action:** Use the [KILL] button on any individual worker.
- **Precision Management:** Allows for the tactical termination of specific stalled streams without needing to execute a global pipeline recovery or application reset.
- **Safety:** Requires manual confirmation to prevent accidental stream disruption.

### 3. SENTINEL Trace Integration
- **Total Observability:** Every audit execution and process termination is documented in the SENTINEL trace log.
- **Trace History:** Includes specific PIDs and status results (e.g., [SUCCESS] Surgical Kill complete for PID: 1245).

---

## Technical Implementation
- **Backend Bridges:** Implemented `get_active_video_workers()` and `terminate_video_worker()` in `main.py`.
- **System Logic:** Uses optimized ps commands to filter for application-specific workers.
- **Forensic Handshake:** Integrated `runVideoWorkerAudit()` and `surgicalTerminateWorker()` into `sidebar_controller.js`.

---

## Verification
- **Checked:** Real-time discovery of active FFmpeg workers? OK
- **Checked:** Surgical SIGTERM execution via PID? OK
- **Checked:** Workspace filtering (CWD check)? OK
- **Checked:** SENTINEL trace synchronization? OK

---

"Nur ergänzen und nichts entfernen" — Walkthrough complete. (Continue / "weiter")
