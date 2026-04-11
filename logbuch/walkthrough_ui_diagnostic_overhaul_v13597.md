# Walkthrough — UI Diagnostic Overhaul (v1.35.97)

We have successfully reorganized the Media Viewer's diagnostic architecture to provide a clean, high-resolution audit of the data pipeline without cluttering the user interface.

## Key Accomplishments

### 1. Triple-Stage Footer Granularity
The footer status bar now identifies data drops at every layer, allowing us to pinpoint the "Black Hole" exactly:

- `[FS: 1.2MB | DB: 541 | GUI: 0]`
    - **FS (Filesystem):** The physical size of the SQLite file. If it shows `0B!`, the backend is opening an empty database.
    - **DB (Database):** The raw row count from the backend process.
    - **GUI (Interface):** The final count of items rendered after filtering.

### 2. Footer De-cluttering & Relocation
The main footer bar has been stripped of advanced developer toggles. The following controls have been moved to their logical home in the Diagnostics tab:

- **Relocated Toggles:** DIAG MODE, HIDE DB, RAW BYPASS, FORCE MOCK, FORCE NATIVE.
- **Relocated Audits:** DOM AUDIT, SELF TEST, DEEP PROBE.

### 3. Sidebar Diagnostics Integration
A new dedicated Diagnostics tab has been activated in the left sidebar.

- **Auto-Navigation:** When starting an audit stage (e.g., `auditSwitchStage(2)`), the UI now automatically switches to the Diagnostics view to display real-time trace logs and hardware metrics.
- **Footer Shortcut:** A new Pulse (Pulse Icon) button has been added to the right-hand toggle group in the footer, providing a one-click entry point to open the sidebar and switch to the Diagnostics tab instantly.
- **Decoupled Debug:** The top-level Debug & DB button now points to a clean, user-friendly Database Master overview.

## Verification Results

### Frontend Parity
- Verified that `loadLibrary` now correctly extracts `fsSize` from the backend handshake and updates the footer.
- Verified that `switchMainCategory('diagnostics')` loads the `fragments/diagnostics_suite.html` fragment.
- Verified that the System Toggles panel in the diagnostics suite provides visual feedback (Active/Inactive states) for all buttons.

### Manual Audit Steps
**TIP: Resolving the 0-Item Bug**

1. Open the console and run `auditSwitchStage(2)`.
2. The UI will jump to the Diagnostics sidebar.
3. Check the footer:
    - If FS shows your database size, pathing is correct.
    - If DB is 541 but GUI is 0, the problem is in Filtering.
4. Click RAW BYPASS in the Diagnostics panel. If items appear, adjust the Category filters in `main.py`.

**Status:** v1.35.97 UI Overhaul Complete. Diagnostic pipeline verified.
