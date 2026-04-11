# Fixing Gevent Concurrency and Scan Errors

## Summary
Implemented gevent status checks and WebSocket stress testing. Encountered a `ConcurrentObjectUseError` and a new `AUDIO_EXTENSIONS` error during media scan. Currently investigating root causes to ensure stability and correct scan logic.

---

## Progress Updates

### 1. Investigating AUDIO_EXTENSIONS Error
- Searched for `AUDIO_EXTENSIONS` usage in `src/core/main.py`:
  - Import: Line 99
  - Comment: Line 1816
  - Usage: Lines 2786, 3021, 4349, 4393
- These lines are involved in file extension checks during media scan and format detection.

### 2. Gevent Concurrency Issue
- After adding gevent status checks and stress testing, the app failed with a `ConcurrentObjectUseError`.
- This error typically indicates unsafe concurrent access to an object (often due to missing or incorrect monkey patching, or thread/greenlet misuse).
- Next steps: Review all gevent usage, ensure correct patching order, and audit scan logic for concurrency hazards.

---

## Next Steps
- Deep-dive into scan logic and extension checks for possible race conditions or misuse.
- Validate gevent patching is applied before any imports that use threading or sockets.
- Add targeted tests for scan concurrency and extension handling.

---

*Logbuch-Eintrag erstellt: 20. März 2026*
