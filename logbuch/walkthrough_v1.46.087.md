# Walkthrough: Playback Handshake Restoration (v1.46.087)

## Date: 2026-04-19

---

## Changes Made

### 1. Handshake De-bottlenecking (`app_core.js`)
- **Direct Play Override:** Refactored `playMediaObject` and `addToQueue` to ensure clicking an item always triggers playback, even if already in the queue.
- **Silent Injection:** Introduced a "silent" mode for queue additions during playback triggers to eliminate redundant "Already in queue" toasts.

### 2. Forensic Audio Guard (`common_helpers.js`)
- **Strict Verification:** Hardened `isVideoItem` with an "Audio Guard". Files matching known audio extensions (e.g., .mp3, .wav) are now strictly prevented from being misrouted to the video player, even if categorized as "multimedia".

### 3. Backend Pulse Tracing (`main.py`)
- **Request Receipt Logging:** Added immediate `log.info` to the `/stream/via/direct/` route. The backend now confirms when a request arrives from the browser and logs the final resolved filesystem path.

### 4. Browser-Side Diagnostics (`audioplayer.js`)
- **Pipeline Tracking:** Updated `playAudio` to log the `proxyUrl` and the internal `readyState` of the HTML5 audio element.

---

## Verification Results

### Manual Verification
- **Double-Click Verification:** Verified that clicking a song twice restarts playback without blockage.
- **Routing Verification:** Confirmed that .mp3 files now correctly stay in the Audio Player context and no longer force-switch to the Video module.
- **Log Verification:** Confirmed `[PLAY-PULSE]` entries appear in the session log upon every click.
