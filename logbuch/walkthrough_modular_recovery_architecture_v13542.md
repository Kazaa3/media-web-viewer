# Walkthrough — Modular Recovery Architecture (v1.35.42)

We have successfully overhauled the MWV Diagnostic Suite from a monolithic file into a scalable, modular "Recovery Engine." This architecture allows for independent testing of negative and positive scenarios while maintaining persistent GUI integrity monitoring.

## 🧱 New Architecture
The diagnostics are now split into specialized modules under `web/js/diagnostics/`:

| Module                | Role           | Description                                                      |
|-----------------------|---------------|------------------------------------------------------------------|
| recovery_manager.js   | The Brain     | Central orchestrator (Control File) that manages stage registration and hydration. |
| gui_integrity.js      | The Eyes      | Manages the Live Sync HUD, MutationWatch, and persistent Visibility Styles. |
| stage_negative.js     | Negative Test | Stages 1 & 2: Missing file simulations (404 verification).        |
| stage_positive.js     | Positive Test | Stages 3 & 4: Real asset verification (Playback & Metadata).      |

## 🚀 Key Improvements
1. **Independent Stage Control**  
   You can now toggle stages independently. To add a new testing level for the Bibliothek (Library), simply create `bibliothek_stage.js` and call `RecoveryManager.registerStage()`.

2. **Non-Destructive Hydration**  
   The Manager now merges diagnostic items with real items. If the background scan (AutoScanThread) populates the database while diagnostics are active, you will see both the test tracks and your real media files.

3. **Persistent Data HUD**  
   The MWV DATA-HUD is always visible in Diagnostic Mode, showing:
   - **BACKEND DB:** Actual row count from the database.
   - **FRONTEND ITEMS:** Total items currently in the JS library.
   - **SYSTEM STATUS:** Real-time sync health (e.g., "STABLE SYNC" or "DATA LEAK").

## 🧪 Verification Results
- **Manager Registry:** Logs confirm: `[MANAGER] Registered Stage: Negative Recovery (2 items)` and `Positive Playback (2 items)`.
- **Sync Handshake:** Logs confirm: `[DB-SYNC] get_library: Found 0 records (on fresh boot)` then triggering Handled Recovery.
- **GUI Integrity:** MutationObserver is active and MutationEvents are being logged for the `#player-main-viewport`.

> **TIP:**
> Use `Diagnostics.toggle()` or the header buttons to switch modes. The modular system is designed to be "plug-and-play" with no future edits required to the core `app_core.js` or `bibliothek.js`.

---

**v1.35.42 Modular Recovery Suite — Finalized & Verified.**
