# Item Forensic Probe: Raw Header Audit — Task Summary (v1.37.20)

## 🛡️ Building the Raw Header Probe

- **Deep-Probe Backend:**
  - Implemented `run_raw_media_probe(item_id)` Eel bridge in main.py to extract raw ffprobe JSON metadata for any media item, ensuring full-stack data visibility.
- **Forensic TRK Upgrade:**
  - Added [RAW] probe button to each search result in the Item Timeline (TRK) tab, enabling instant access to raw stream headers.
- **High-Density Viewport:**
  - Implemented a technical JSON rendering engine in sidebar_controller.js to maintain the workstation aesthetic during deep-probes.

---

## Implementation Plan
- **Backend (main.py):**
  - Add `run_raw_media_probe(item_id)` Eel bridge.
  - Logic: Resolve ID to path → Execute ffprobe → Return raw JSON string.
- **Controller (sidebar_controller.js):**
  - Update `performItemJourneyAudit` results to include a [RAW] button.
  - Implement `triggerRawItemProbe(itemId)` for backend handshake.
  - Add a floating/inline "Raw Forensic Viewer" for syntax-highlighted JSON.
- **Sidebar UI (diagnostics_sidebar.html):**
  - Add a new result-pane or ensure existing viewports support large pre-formatted text.

---

## Notes
- **Technical Density:** Raw Probe output is high-density JSON. Viewer is code-styled for readability.
- **Open Question:** Should the Raw Probe also include Packet Analysis (-show_packets)? (Recommended: Add a "Deep Probe" toggle later.)

---

## Verification Plan
- Automated: Verify `run_raw_media_probe` handles invalid IDs gracefully and works for both Video and Audio containers.
- Manual: Search for an item in TRK tab, click [RAW], verify raw metadata appears with correct syntax highlighting, and inspect SENTINEL trace for [PROBE] audit logs.

---

The Raw Header Probe is now integrated, providing deep forensic visibility into your media items directly from the timeline suite.
