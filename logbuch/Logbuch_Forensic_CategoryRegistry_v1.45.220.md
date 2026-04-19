# Forensic Note: Category Registry Architecture (v1.45.220)

## Context
This note clarifies the intended separation of concerns for the category/branch architecture in the media-web-viewer project.

## Key Point
- **"media" and "library"** should NOT be present in the branch architecture registry.
- The registry should only contain true content types, as defined in models.py:
  - audio
  - video
  - iso-image
  - dokumente
  - bilder
  - usw. (etc.)

## Current State
- Some legacy or transitional code may still reference generic categories like "media" or "library" in the registry.
- This is a known architectural debt and will be addressed in a future refactor.

## Action Required
- **Future Refactor:**
  - Remove all references to "media" and "library" from the branch/category registry.
  - Ensure only true content types (as defined in models.py) are present.
  - Audit all registry usages for compliance.

## Rationale
- This separation ensures that the registry accurately reflects the domain model and supports robust, branch-aware filtering and UI logic.

---

**Note:** This is a transitional state. Update the registry as soon as the forensic realignment is complete and the new category system is stable.
