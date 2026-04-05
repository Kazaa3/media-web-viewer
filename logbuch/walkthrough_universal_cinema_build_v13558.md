# Walkthrough: Universal Cinema Build (v1.35.58)

## Overview
This walkthrough documents the successful deployment and verification of the Universal Video Cinema suite in the Media Web Viewer (v1.35.58). The system now supports high-fidelity video playback, on-the-fly transcoding, and direct ISO streaming, all visible and testable via the diagnostic baseline and Recovery HUD.

---

## 1. Backend: Universal Video Transcoding
- **Expanded app_bottle.py**: Now detects `.mp4_transcoded` suffix and triggers FFmpeg to convert MKV/ISO to browser-compatible MP4 (H.264/AAC).
- **Timeout & Hygiene**: Each video transcode is protected by a 120s timeout. Zombie processes are cleaned up by `reboot_mwv.sh`.
- **Logging**: Terminal logs show `TRANSCODING STARTED` and `TRANSCODING SUCCESS` with file size and latency for each operation.

---

## 2. Diagnostic Baseline: Video Stages
- **Stage 12 (Native)**: `clip.mp4` (Direct browser playback)
- **Stage 13 (MKV Transcode)**: `abc.mkv.mp4_transcoded` (FFmpeg conversion)
- **Stage 14 (Regional)**: `Stargate Continuum (2008) - PAL.mkv` (Native PAL/NTSC test)
- **Stage 15 (ISO Verifier)**: `4_KOENIGE.iso.mp4_transcoded`, `RUSHHOUR3_D2.ISO.mp4_transcoded` (DVD/Blu-ray ISO streaming)
- **Queue**: 29 items, 9 stages hydrated, all visible in the Recovery HUD.

---

## 3. Frontend: Live Recovery HUD
- **Version**: MWV Frontend v1.35.58
- **Status**: `CINEMA STATUS: ISO-TRANSCODE-ACTIVE`, `SYSTEM STATUS: BASELINE-FORMAT-COMPLETE`
- **Verification**: Logs confirm 29-item baseline after reboot. Recovery HUD displays all video stages and assets.

---

## 4. Verification Steps
1. **Reboot** the backend using `reboot_mwv.sh` to ensure a clean state.
2. **Open** the Recovery HUD. Confirm 29 items and 9 stages are hydrated.
3. **Click play** on `4 Könige (ISO)` or any ISO/Blu-ray item.
4. **Observe** the terminal: `TRANSCODING STARTED` appears, followed by `TRANSCODING SUCCESS`.
5. **Playback**: The Video Player streams the movie directly from the ISO image after a short buffer.

---

## 5. Troubleshooting
- If playback stalls, check for `TRANSCODING FAILED` in logs and ensure FFmpeg is installed.
- Use `reboot_mwv.sh` to clear any zombie processes and reset the backend.
- Confirm all assets are present in the media directory and paths are correct in the diagnostic stage file.

---

## 6. Conclusion
The Universal Cinema Build (v1.35.58) delivers robust, browser-compatible video playback for native, MKV, and ISO sources, with full diagnostic visibility and process hygiene. The system is now baseline-complete for universal video media.

---

*For further details, see the implementation plan and code in the repository.*
