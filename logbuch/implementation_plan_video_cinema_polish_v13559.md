# Implementation Plan — Video Cinema Polish (v1.35.59)

## Objective
Finalize the Precision Video Pipeline with a refined diagnostic sequence and high-speed HD Pass-through (Remuxing) for HD MKVs, ensuring instant browser playback and robust ISO transcoding.

---

## Key Goals
- **HD Pass-through (Remuxing) [BACKEND]:**
  - Add `.mp4_pass` suffix to the transcoding engine in `app_bottle.py`.
  - Use `ffmpeg -c:v copy` for zero-loss, high-speed remuxing (container change only, ~1% CPU).
- **Refined Stage 12–15 Sequence:**
  - Direct Player (Native): `30. Pleisweiler Gespräch... (720p).mp4` (No transcode)
  - HD Pass-through (Remux): `Stargate...PAL.mkv.mp4_pass`
  - Legacy PAL/NTSC: `Set It Off...PAL.mkv.mp4_transcoded` (Full conversion)
  - ISO DVD: `4_KOENIGE.iso.mp4_transcoded`
  - ISO Blu-ray: `RUSHHOUR3_D2.ISO.mp4_transcoded`
- **Baseline Expansion:**
  - Diagnostic baseline expands to 30 items, following the exact requested sequence.
- **Performance Pulse:**
  - DATA-HUD will indicate if a track is "Transcoding" (CPU heavy) or "Remuxing" (I/O fast).

---

## Components to Modify
- `web/app_bottle.py`: Add `.mp4_pass` for remuxing logic.
- `web/js/diagnostics/stages/stage_video_universal.js`: Update sequence and add HD Pass-through item.
- `web/js/version.js`: Increment to v1.35.59.

---

## Expected Outcome
- Queue reaches 30 items, with the new HD Pass item playing almost instantly (remuxed, not transcoded).
- ISO items still trigger full transcoding for compatibility.
- DATA-HUD accurately reflects current operation (Transcoding vs. Remuxing).

---

## Verification
1. Click play on the HD Pass item: playback should start instantly.
2. Click play on an ISO item: observe full transcoding and normal buffer.
3. Confirm DATA-HUD status updates correctly for each operation.

---

*Ready to proceed with the High-Speed HD Video expansion as described above.*
