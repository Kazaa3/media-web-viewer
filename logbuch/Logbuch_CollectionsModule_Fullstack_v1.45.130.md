# Logbuch: Automated Folder & Collection Management (v1.45.130) – Full-Stack Implementation Plan

## Overview
This plan details the implementation of a full-stack collection management system for the Forensic Media Workstation. It introduces a global forensic toggle, backend-driven .nfo metadata extraction, and specialized frontend logic for grouping and categorizing media clusters.

---

## Key Features & Proposed Changes

### 1. Backend Configuration & Parsing
- **config_master.py:**
  - Add global flags to `GLOBAL_CONFIG`:
    - `enable_collection_management`: Master switch for folder grouping.
    - `enable_nfo_parsing`: Enable/disable XML parsing of .nfo files.
- **main.py:**
  - Update `_scan_media_execution` to:
    - Search for .nfo files within media directories.
    - Use `xml.etree.ElementTree` to extract `<title>`, `<year>`, `<genre>`, `<artist>`.
    - Detect "Various Artists" (VA, Varios, Various Artists) for compilation categorization.
    - Map genres `klassik`/`classical` to klassik, `soundtrack`/`ost` to soundtrack.
- **models.py:**
  - Expand `MASTER_CAT_MAP` to include:
    - album, compilation, podcast, single, series, documentation, soundtrack, klassik, nfo.

### 2. Frontend Collection Logic
- **collections.js:**
  - Folder parser for movie and album naming conventions.
  - `groupItemsByFolder(items)` to consolidate multi-part media into a single collection badge in the UI.
- **common_helpers.js:**
  - Add inline SVGs for new categories:
    - klassik (Violin/Cello), soundtrack (Reel+Note), podcast (Microphone), nfo (Info Doc), etc.
  - Update `getCategoryBadgeHtml` to render these icons based on new category mappings.

### 3. Application Integration
- **shell_master.html:**
  - Include `js/collections.js?v=1.45.130` in the header.

---

## Open Questions
- **NFO Hierarchy:** If a folder has multiple .nfo files, should one be prioritized (e.g., movie.nfo over folder.nfo)?
- **SVG Styles:** Should icons be monochromatic (forensic theme) or use color accents for different categories?

---

## Verification Plan

### Automated Tests
- Unit test: Parse sample .nfo XML to verify tag extraction.
- Regex test: Verify folder name parsing with years and dashes.

### Manual Verification
- Verify that the extended branch displays the nfo category in the sidebar.
- Verify that grouping a folder with CD1.mp3 and CD2.mp3 results in a single "Album" entry in the library grid.

---

**Awaiting user input on NFO file prioritization and SVG icon style before implementation.**
