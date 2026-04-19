# Implementation Plan - Object/Release Hierarchy & Multilateral Grouping (v1.54.006)

This plan refines the forensic workstation's architecture by distinguishing between the logical "Total Object" and its specific "Release" variants, supporting multilateral grouping and expanded metadata.

---

## 1. Structural Model Expansion
- **[MODIFY] `objects.py`**
  - **Rename:** `AudioRelease` ➔ `AudioObject` (subtype: `AUDIO_OBJECT`).
  - **Expand `ObjectRelease`:**
    - Add `source: str` (e.g., "Audible", "CD", "Vinyl").
    - Add `language: str` (e.g., "DE", "EN").
  - **Update Base:** Ensure `MediaObject` correctly serializes the expanded `ObjectRelease` data.
  - **Factory Update:** Update `create_forensic_object` to recognize the new hierarchy.

---

## 2. Grouping Intelligence (Archeology)
- **[MODIFY] `object_discovery.py`**
  - **Implement Multi-Release Detection:**
    - Update `ObjectDiscoveryEngine` to detect editions/versions within a single folder.
    - **Films:** Group `Theatrical.mkv` and `DirectorsCut.mkv` into one `FilmObject` with two releases.
    - **Audiobooks:** Group `[DE]` and `[EN]` versions into one `AudiobookObject`.
    - **Audio:** Group "Bonus Tracks" from different editions into the primary `AudioObject`.

---

## 3. UI Forensic Taxonomy Synchronization
- **[MODIFY] `config_master.py`**
  - Maintain peer categorization for subtypes in the UI.
  - Update `library_category_map` labels to reflect the "Total Object" nature.

---

## Open Questions
- **Member Inheritance:** If an item belongs to multiple releases (e.g., tracks common to both Standard and Deluxe), should it be listed twice or shared? (**Recommended:** Share the ID, but mark release membership in the items list).

---

**Status:**
- Pending implementation and review.
- This plan ensures robust object/release hierarchy, multilateral grouping, and synchronized forensic taxonomy.
