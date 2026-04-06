# 🛡️ Expanded Mission Recovery & SSOT Finalization (v1.35.96)

## Refined SSOT Expansion

- **HLS/FFmpeg Protocol:**
    - Moved `-hls_time 4` and `-hls_list_size 3` into `GLOBAL_CONFIG["transcoding_profiles"]["hls_fmp4"]`.
- **Cache Management:**
    - Standardized `MEDIA_CACHE` and `mkv_cache_dir` into the `storage_registry`.
- **Library Anchoring:**
    - Updated the `lib_dir` fallback and `resolve_media_path` to use the centralized `media_dir` from the SSOT.

## The "0 Item" Smoking Gun

- The Eel sub-process may be inheriting a different `PROJECT_ROOT` during re-execution, causing it to initialize a fresh, empty database.
- Implementing Absolute Path Hardening for `DB_FILENAME` and `PROJECT_ROOT` to ensure both CLI and GUI are locked to the same SQLite instance.

## Low-Level Category Normalization

- Added a startup routine to lowercase all categories in the database. This fixes the issue where `Audio` items are indexed but filtered out by a case-sensitive `audio` lookup.

## Next Steps

- Please review the revised `implementation_plan.md`.
- Once approved, the "once and for all" stabilization will begin.
