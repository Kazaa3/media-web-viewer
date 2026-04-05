# Implementation Plan — Format Expansion (v1.35.53)

## Overview
High-fidelity collection scan identified healthy samples for the final three formats: M4B (Audiobooks), AAC (Native Streams), and M4A. This plan expands the diagnostic suite to cover all major modern audio containers.

## 🛠️ Key Goals
- **Stage 10 Expansion (22 Titel total):**
  - Add 3 new items to the "Real Format Verify" stage, bringing the diagnostic baseline to 22 Titel.
- **New Real-File Targets:**
  - **M4A:** 02 We the People….m4a
  - **M4B (Audiobook):** Adrienne Herbert - Power Hour.m4b
  - **AAC:** Heinz Strunk - Fleisch ist mein Gemüse (Komplettes Hörbuch).aac
- **Metadata Proofing:**
  - Verify AudioPlayer displays correct titles and durations for M4B and AAC, even in diagnostic hydration.
- **Backend Integrity:**
  - Further stress-test unquote() path hardening for filenames with ellipsis (…) and parentheses.

## 📂 Files to Modify
- [MODIFY] `web/js/diagnostics/stages/stage_format_real.js`: Expand by +3 items.
- [MODIFY] `web/js/version.js`: Increment to v1.35.53.

## 🧪 Expected Outcome
- Queue grows to 22 Titel.
- Actual M4B audiobooks and AAC files are playable from the diagnostic suite.
- System is 100% library-ready for all major formats.

---

*This plan completes format coverage and ensures robust metadata and path handling for all supported audio types.*
