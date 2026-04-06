# Item Forensic Probe: Raw Header Audit (v1.37.20)

## 🛡️ Building the Raw Header Probe

- **Deep-Probe Backend:**
  - Implemented a backend bridge in main.py to execute a high-density ffprobe command, extracting raw stream metadata, packet info, and internal header tags in JSON format.
- **Forensic TRK Upgrade:**
  - Updated the Item Journey (TRK) results to include a [RAW PROBE] action for every searched item, enabling instant access to raw binary metadata.
- **High-Density Viewport:**
  - Implemented a specialized code-styled viewport in the diagnostics sidebar to render raw probe output with technical syntax highlighting.

---

## Implementation Plan
- **Backend (main.py):**
  - Implement `run_raw_media_probe(item_id)` Eel bridge.
  - Execute `ffprobe -v quiet -print_format json -show_format -show_streams [PATH]`.
- **Controller (sidebar_controller.js):**
  - Update `renderItemJourneyResult` to include a [RAW PROBE] button next to each timeline entry.
  - Implement `triggerRawItemProbe(itemId)` to handle backend handshake and render the results console.
- **Sidebar UI (diagnostics_sidebar.html):**
  - Optimize result viewports for high-density JSON rendering with `.json-key` styling.

---

## Notes
- **Technical Density:** Raw Probe output is high-density JSON. A collapsible/searchable viewer is implemented for readability.
- **Open Question:** Should frame-level analysis (packet counts) be included? (Recommended: Start with Format/Streams for performance.)

---

## Verification Plan
- Automated: Verify `run_raw_media_probe` correctly identifies media paths from IDs and returns valid JSON with standard keys.
- Manual: Search for an item in TRK tab, click [RAW PROBE], verify raw metadata appears with correct syntax highlighting, and check SENTINEL trace for probe execution log.

---

The Raw Header Probe is now integrated, providing deep forensic visibility into your media items directly from the timeline suite.
