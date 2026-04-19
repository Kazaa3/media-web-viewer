# Logbuch: Automated Folder & Collection Management (v1.45.130) – Implementation Plan

## Overview
This plan introduces a dedicated module (collections.js) for managing complex media folder structures, grouping related files, and parsing advanced metadata for forensic categorization. The goal is to provide robust, automated handling of collections (e.g., multi-ISO movies, multi-CD albums) and support new forensic categories with specialized metadata and icons.

---

## Key Features & Proposed Changes

### 1. New Collections Module
- **collections.js:**
  - `parseFolderName(folderName)`: Extracts title and year for films (Movie Name (Year)) and albums (Artist - Album Name (Year)).
  - `resolveCollectionMetadata(items)`: Scans for cover.jpg, folder.jpg, .nfo, and associates metadata.
  - `getCollectionCategory(item)`: Maps to new forensic categories (album, compilation, podcast, single, series, documentation, soundtrack, klassik).
  - Compilation logic: Detects VA, Varios, Various Artists as Artist.
  - Klassik logic: Maps genre klassik/classical to klassik category.
  - Soundtrack logic: Maps genre soundtrack/ost to soundtrack category.
  - `groupItemsByFolder(items)`: Groups files (ISOs, MKVs, CDs) sharing a parent directory into a logical collection.
  - ISOBootstrap: Special handling for .iso, .bin, .img clusters.

### 2. Integration with Library Rendering
- **bibliothek.js:**
  - Update `renderLibrary` to use `groupItemsByFolder` when in "Collection View" mode.
  - Update category filtering to support new forensic categories.
- **common_helpers.js:**
  - Update `getCategoryBadgeHtml` to support icons for new categories (klassik, podcast, etc.).

### 3. HTML Integration
- **shell_master.html:**
  - Add `<script src="js/collections.js?v=1.45.130"></script>` after item.js.

---

## Open Questions
- **Grouped vs. Flat View:** Should the library always group items by folder, or should there be a toggle for "Folder View" vs. "Flat View"?
- **NFO Parsing:** Should the backend (Python) parse .nfo XML and send metadata, or should the frontend parse it? (Recommended: Backend parsing for performance.)
- **Icon Mapping:** Do you have specific SVG icons for klassik, soundtrack, documentation, or should generic forensic symbols be used?

---

## Verification Plan

### Automated Tests
- Test `parseFolderName` with various naming conventions (e.g., Movie (2024), Album [2023], Single - 2022).
- Test `groupItemsByFolder` with simulated multi-ISO directories.

### Manual Verification
- Verify folders with cover.jpg display the cover in the library grid.
- Verify "Series" items display S1E1 badges correctly when grouped.
- Check that new categories (soundtrack, klassik, etc.) appear in the filter sidebar.

---

**Awaiting user input on grouping toggle, backend NFO parsing, and icon preferences before implementation.**
