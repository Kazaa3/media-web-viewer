<!-- Category: Library -->
<!-- Summary: Intelligente Erkennung von Hörbüchern (.m4b) und Integration in Datei-Browser. -->
<!-- Status: COMPLETED -->

# Media Categorization

## Overview
To improve organization within the library, we added a categorization system that distinguishes between standard Music and Audiobooks.

## Logic
1. **File Extension**: Files ending in `.m4b` are automatically flagged as `Audiobook`.
2. **Path Heuristics**: Folders containing "Hörbuch" or "Audiobook" in their path are also considered.
3. **Database Flag**: A new `category` field exists in the `media` table.

## GUI Integration
- **Badges**: In the library list, items are marked with an "Audiobook" badge if applicable.
- **Filtering**: The database can now be queried specifically for one category (Music or Audiobook).

This system allows for a cleaner user experience when managing large libraries with mixed media types.
