# Implementation Plan - Audio Release Architecture & UI Taxonomy (v1.54.005)

This plan refines the media workstation's organizational model by accurately classifying 'Audio Releases' and providing high-density UI categorization for professional media forensics.

---

## 1. Model Alignment & Structural Renaming
- **[MODIFY] `objects.py`**
  - Rename `AudioObject` ➔ `AudioRelease`.
  - Update the subtype to `AUDIO_RELEASE_OBJECT`.
  - Update the `create_forensic_object` factory to recognize the new name.

---

## 2. Forensic Taxonomy & UI Mapping
- **[MODIFY] `config_master.py`**
  - **Taxonomy Peer Promotion:**
    - Move `sampler`, `ost`, `soundtrack`, `klassik`, `audiobook`, `single`, `maxi` back to parent: `audio` (peers of `album`).
  - **Virtual Category Registration:**
    - Add `all_audio_releases` to `GLOBAL_MEDIA_TAXONOMY` (label: "Alle Audio Releases / All Objects").
  - **Branch Architecture Integration:**
    - Update `branch_architecture_registry` for `audio` and `multimedia` to include all specialized subtypes and the virtual 'All Releases' filter.

---

## 3. Filtering Engine Expansion
- **[MODIFY] `api_library.py`**
  - Update `apply_library_filters` to handle the `all_audio_releases` genre/category filter.
  - Logic: If `genre == 'all_audio_releases'`, return all items where `type == 'object'` and `category == 'audio'`.

---

## 4. UI Synchronization
- **[MODIFY] `app_core.js`**
  - Update `hydrateCategoryDropdown` to ensure labels are correctly resolved from the configuration and that the 'All Releases' filter is correctly injected.

---

## Open Questions
- **Ordering:** Should 'All Audio Releases' appear at the top or bottom of the audio-specific sections in the dropdown? (**Recommended:** Top, after the general 'Audio' filter).

---

**Status:**
- Pending implementation and review.
- This plan ensures accurate audio release modeling and professional, high-density UI taxonomy for forensic workflows.
