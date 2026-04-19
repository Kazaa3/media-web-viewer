# Workstation Infrastructure & API Decoupling Walkthrough

The Forensic Media Workstation backend has been modernized to professional industry standards. We successfully decoupled the monolithic core, centralized tool discovery, and established a modular API architecture.

---

## Key Accomplishments

### 1. Centralized Forensic Tooling SSOT
- **Refactored discover_binary:** Now platform-aware (Linux/Windows) and prioritizes discovery in `tools/linux/bin` and `tools/windows/bin` over system paths.
- **PROGRAM_REGISTRY:** A single source of truth in `config_master.py` for all 23+ forensic binaries (FFmpeg, VLC, MKVToolNix, Docker, etc.).
- **BROWSER_REGISTRY:** Organized discovery for Chrome (Stable/Dev/Beta), Chromium, and Firefox engines.
- **MEDIA_RESOURCE_REGISTRY:** Structured access to reference media, mock files, and test ISOs for automated forensics audits.

### 2. API Modularization
We eliminated the monolithic complexity of `main.py` by delegating logic to four specialized API services:
- `api_tools.py`: Centralized health diagnostics and stalled process cleanup.
- `api_transcoding.py`: Encapsulated the complex FFmpeg/MKVMerge "Pipe-Kit" streaming and remuxing logic.
- `api_core_app.py`: Managed application lifecycle and environment (VENV) stabilization.
- `api_parsing.py`: Orchestrated high-fidelity metadata extraction chains.

### 3. Infrastructure Evolution
- Established `tools/linux/bin` and `tools/windows/bin` directories for portable binary distribution.
- Stabilized cyclic imports in the logging system by adding robust fallback guards in `logger.py`.

---

## Validation Results
We verified the refactor using a dedicated verification script within the workstation's virtual environment:

```bash
SUCCESS: All API modules and registries loaded.
FFmpeg Path: /usr/bin/ffmpeg
VLC Path: /usr/bin/vlc
Project Root: /home/xc/#Coding/gui_media_web_viewer
Tool Health Check: 23 tools registered.
```

---

## Impact on Maintenance
The entry point `main.py` has been reduced in complexity, serving now primarily as a routing layer. Developers can now modify transcoding logic or tool discovery rules in dedicated, localized files without risk of breaking the main application loop.

> **TIP:**
> All new forensic tools should now be registered in `PROGRAM_REGISTRY` in `config_master.py` to be automatically detected across the entire workstation.
