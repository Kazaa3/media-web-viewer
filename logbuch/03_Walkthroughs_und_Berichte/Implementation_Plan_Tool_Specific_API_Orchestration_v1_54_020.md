# Implementation Plan – Tool-Specific API Orchestration (v1.54.020)

## Objective
Expand `api_tools.py` to include specialized orchestration for external playback tools (FFplay) and remote casting (Chromecast).

---

## User Review Required

### IMPORTANT
- Chromecast support requires the `pychromecast` library. Implementation will include defensive checks; if missing, "Cast" functionality will be gracefully disabled in the technical HUD.

---

## Proposed Changes

### [Component] Tool API Expansion
- **api_tools.py**
  - [NEW] `launch_ffplay(file_path)`: Implement a safe process trigger using `subprocess.Popen` for rapid forensic-grade media preview outside the main browser.
  - [NEW] `discover_chromecast()`: Implement device discovery using `pychromecast` to scan the local network for casting targets.
  - [NEW] `cast_to_device(device_id, file_path)`: Implement media remote-play logic.
  - **Eel Exposure:** Decorate these functions with `@eel.expose` for access from navigation and tools dashboard.

### [Component] Workstation UI Integration
- **ui_nav_helpers.js**
  - Tool Triggers: Add baseline handlers for triggering these new tool pulses from the workstation's technical menus.

---

## Open Questions
- Should ffplay be launched with specific forensic flags (e.g., `-stats`, `-loop 0`, or `-autoexit`) by default?

---

## Verification Plan

### Automated Tests
- `python3 src/core/startup_auditor.py`: Verify new tool dependencies do not block the boot sequence.

### Manual Verification
- Open the "Tools" dashboard or a media context menu.
- Trigger "Preview (FFplay)" for an asset and confirm the external window opens.
- Trigger "Chromecast Scan" and verify available devices are listed in diagnostic logs.
