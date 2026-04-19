# Forensic Note: SUB_NAV_ALIASES Mapping (v1.45.220)

## Context
This file documents the current state and known issues with the `SUB_NAV_ALIASES` mapping in the codebase. The mapping is used to translate various navigation keys and legacy panel names to their canonical internal categories for the media-web-viewer project.

## Current State
- The mapping includes both UI navigation elements (e.g., "player", "bibliothek", "explorer") and content/media types (e.g., "audio", "album", "hörbuch").
- As of v1.45.220, all audio-related formats ("audio", "audio_native", "audio_transcode", "album", "single", "hörbuch", "sampler", "soundtrack") are aliased to "media".
- This is a temporary solution: ideally, these should be mapped to a dedicated audio category (e.g., "audio") for more precise filtering and UI logic.
- The same applies to other content types (e.g., "video_iso", "bilder", "epub"), which are currently aliased to "media".

## Known Issue
- **Incorrect Aliasing:** Audio formats and other content types are currently mapped to "media" instead of their correct, more granular categories (e.g., "audio").
- **Reason:** This is a transitional state to maintain compatibility and avoid breaking the current navigation and filtering logic during the forensic realignment phase.

## Temporary Justification
- This approach ensures that all content types remain accessible and visible in the UI while the backend and frontend category systems are being realigned.
- Once the category realignment is complete, these aliases should be updated to reflect their true content type (e.g., map all audio formats to "audio").

## Action Required
- **Future Refactor:** Update the `SUB_NAV_ALIASES` mapping to assign audio formats and other content types to their correct categories after the forensic realignment is finished.
- **Audit:** Review all usages of `SUB_NAV_ALIASES` to ensure that UI and backend filtering logic are updated accordingly.

## Example (Current Mapping)
```js
const SUB_NAV_ALIASES = {
    "player": "media",
    "bibliothek": "library",
    "database": "database",
    "explorer": "library",
    "tools": "tools",
    "debug": "debug",
    "diagnostics": "status",
    "optionen": "system",
    "report": "reporting",
    "reporting_dashboard": "reporting",
    "file": "file",
    "edit": "edit",
    "parser": "parser",
    "logbuch": "logbuch",
    "video": "video",
    "tests": "tests",
    "status": "status",
    // [v1.45.220] Forensic Content Aliases -> Media Controller
    "audio": "media",
    "audio_native": "media",
    "audio_transcode": "media",
    "album": "media",
    "single": "media",
    "hörbuch": "media",
    "sampler": "media",
    "soundtrack": "media",
    "video_iso": "media",
    "bilder": "media",
    "epub": "media"
};
```

---

**Note:** This mapping is intentionally imprecise for the duration of the forensic realignment. Update as soon as the new category system is stable.
