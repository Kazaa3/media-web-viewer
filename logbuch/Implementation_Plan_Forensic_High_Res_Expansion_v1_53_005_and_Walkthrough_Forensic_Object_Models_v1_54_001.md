# Implementation Plan - Forensic High-Res Expansion (v1.53.005)

This plan finalizes the Phase 13 diagnostic suite by implementing specialized support for High-Res (DSD) and Multichannel (Mehrkanal) audio, resolves indentation mismatches in the dependency registry, and synchronizes bitrate quality logic with the user's standard.

---

## 1. Forensic High-Res Taxonomy
- **[MODIFY] `config_master.py`**
  - **Registry Restoration:** Fix indentation of `DEPENDENCY_REGISTRY` and ensure all self-healing flags (`auto_install_enabled`, `offline_mode_enforced`) are initialized at the top.
  - **DSD & Multichannel Registry:**
    - Add `DSD_EXTENSIONS = {".dsf", ".dff", ".sacd"}`.
    - Add `MULTICHANNEL_EXTENSIONS = {".ac3", ".dts", ".thd", ".eac3", ".dtshd"}`.
  - **Taxonomy Expansion:**
    - Add `dsd` (High-Res DSD) and `mehrkanal` (Multichannel) to `GLOBAL_MEDIA_TAXONOMY`.
  - Update version to v1.53.005.

---

## 2. UI Quality Refinement (Phase 13 Finalization)
- **[MODIFY] `app_core.js`**
  - **Bitrate Logic:** Update `getBitrateQualityClass` with the exact logic:
    - `>= 1000`: `quality-high`
    - `>= 320`: `quality-high`
    - `>= 192`: `quality-std`
    - default: `quality-low`
  - **Animation Trigger:** Ensure `triggerAuditPulse()` targets the correct `.sidebar` or `.sidebar-lane` element for consistent visual feedback.

---

## Verification Plan

### Automated Tests
- `python3 -m py_compile src/core/config_master.py`
- Verify that DSD files are correctly categorized in the library rescan.

### Manual Verification
- Confirm the "Audit Pulse" glow is visible on the sidebar during filter changes.
- Verify that bitrates `>= 1000 kbps` (FLAC/DSD) show as High Quality (Green).
- Confirm that the dependency registry is correctly initialized in the backend logs.

---

# Walkthrough - Forensic Object Models (v1.54.001)

This phase modernizes the workstation's media model by introducing "Grouped Objects" and resolving critical environment stability issues.

---

## 1. Workstation Startup Repair (v1.53 Rebuild)
- **Venv Reset:** Cleared the corrupted `.venv` and rebuilt it from scratch.
- **Bundle Restoration:** Installed the 35+ package "Ultimate Bundle" from `infra/requirements-full.txt`.
- **Integrity Audit:** Verified all 4 tiers (Core, Forensic, Media, Analytics) are operational via `startup_auditor.py`.

## 2. Forensic Object Architecture (v1.54)
- Introduced a new orchestration layer in `src/core/objects.py` for complex media entities:
  - **Film Objects:** Unified grouping for theatrical/extended versions and multi-country covers.
  - **Album Objects:** Specialized support for multiple releases (CD, Digital), CUE files, and EAC Logs.
  - **Sidecar Registry:** Automatic association of `.nfo`, `.cue`, and `.log` files to their parent objects.

## 3. Object Discovery Engine
- Implemented `src/core/object_discovery.py` to automate grouping:
  - **Heuristic Scanning:** Identifies related files in folders using nomenclature matching (e.g., Director's Cut, Extended Edition).
  - **Parent-Child Linking:** Uses the workstation's `parent_id` database architecture to link technical items to logical parent containers.

## 4. UI & API Integration
- Refined library access layers for high-density grouping:
  - **Unified Library View:** Child items (individual cut versions) are hidden from the main list in `api_library.py`, presenting only the unified "Object" to the user.
  - **Version Persistence:** Parent Objects track all child IDs and versions for forensic observability.

---

## Verification Results
- `startup_auditor.py`: AUDIT SUCCESS
- `db.py`: Verified `parent_id` and subtype persistence.
- `api_library.py`: Verified "Object Guard" filtering logic.
- **System Version:** v1.54.001 (Object-Centric)
