# Item Forensic Probe: Raw Header Audit — Backend Integration (v1.37.20)

## 🛡️ Building the Raw Header Probe

- **Backend Deep-Probe Hook:**
  - Implemented `run_raw_media_probe(item_id)` Eel bridge in src/core/main.py to extract complete ffprobe JSON metadata for any media item, enabling deep forensic audits.
  - Verified the bridge is correctly integrated and extracts full-stack stream metadata and format details.
- **Forensic TRK Upgrade:**
  - Next: Update the Item Journey (TRK) suite in sidebar_controller.js to include the interactive [RAW] probe button for every searched item.
- **Technical Viewport Rendering:**
  - Next: Ensure all raw metadata is rendered with workstation-grade syntax highlighting in the diagnostics overlay.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.

---

The backend deep-probe hook is now implemented and verified. Proceeding to the TRK upgrade and technical viewport rendering.
