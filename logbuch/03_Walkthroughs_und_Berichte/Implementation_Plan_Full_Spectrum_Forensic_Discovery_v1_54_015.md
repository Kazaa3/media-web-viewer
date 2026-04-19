# Implementation Plan – Full-Spectrum Forensic Discovery (v1.54.015)

## Objective
Modernize the Video discovery experience and ensure all media formats are accurately represented with technical quality metrics.

---

## User Review Required

### IMPORTANT
- **Unified Pulse Alignment:** Integrate `renderVideoQueue()` into the global hydration cycle to ensure video items are tracked and rendered alongside audio and photos.

### TIP
- **Quality Badges:** Video items in the queue will now display their Resolution and Bitrate as part of the forensic summary.

---

## Proposed Changes

### [UI] ui_nav_helpers.js
- [MODIFY] Update `switchPlayerView` to include `renderVideoQueue()` in the "Aggressive Hydration" pulse.

### [UI] video.js
- [MODIFY] Enhance `renderVideoQueue()` to extract and display technical metadata:
  - `i.resolution` (Width x Height)
  - `i.bitrate`
  - `i.codec`
- [MODIFY] Add forensic provenance badges ([R]eal, [M]ock, [D]iag) to video items for nomenclature parity.

### [Core] app_core.js
- [MODIFY] Update `initForensicHeartbeat()` to pulse `renderVideoQueue()` during every evaluation cycle.

### [Core] audioplayer.js
- [MODIFY] Update `renderAudioQueue()` to ensure that if `activeQueueFilter` is 'all', the message "Mixed Forensic Stream" is displayed or specialized badges are applied.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/.local/bin/python3.14 src/core/startup_auditor.py` to verify system integrity.

### Manual Verification
- **Video Queue Sync:** Add a video to the queue and verify it appears in the Mediengalerie (if appropriate) or the Cinema tab with its resolution.
- **Sentiment Check:** Verify that "All Formats" in the discovery view shows a high-density list of mixed media.
