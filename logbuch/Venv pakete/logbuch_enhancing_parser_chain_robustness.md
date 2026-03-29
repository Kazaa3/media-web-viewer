# Logbuch: Enhancing Parser Chain Robustness

## Overview
This log documents the multi-phase enhancement of the media-web-viewer’s parser chain, focusing on resilience, technical metadata extraction, format expansion, playability logic, and project structure modernization. Each phase is tracked with proposed changes, affected components, and verification plans.

---

## Phase 1: Parser Chain Robustness
### Goals
- Isolate parser state to prevent corruption from crashes.
- Enhance exception handling (TimeoutExpired, ImportError, partial tag leaks).
- Improve error logging with contextual information.
- Add per-call timeout wrappers to prevent hangs.

### Key Changes
- **media_parser.py**: Pass copies/backups of `current_tags` to each parser; restore on failure. Add granular exception handling and contextual logging. Consider timeout decorators for parser calls.
- **Individual Parsers**: Ensure all treat input as read-only; all subprocess calls use timeouts.
- **Logging**: Include file, parser, and attempt info in error logs.

### Verification
- Simulate parser crashes and timeouts; verify state isolation and recovery.
- Check logs for detailed error context.

---

## Phase 2: Advanced Robustness Measures
### Goals
- Data sanitization (limit tag/chapter size, handle Unicode errors).
- Resource leak prevention (file handles, try...finally).
- Optional: Process/thread isolation for heavy parsers.

### Key Changes
- **media_parser.py**: Validate metadata size, use `errors='replace'` for decoding, enforce resource cleanup.
- **All Parsers**: Audit for file handle leaks and ensure robust error handling.

### Verification
- Test with oversized/corrupt files; verify no UI lag or memory issues.
- Check for file handle leaks and Unicode decode errors.

---

## Phase 3: ISO Metadata Expansion
### Goals
- Expand pycdlib extraction (PVD, dates, extensions, DVD/BD detection).
- Robust decoding for specialized pycdlib objects.

### Key Changes
- **pycdlib**: Extract more metadata fields, detect DVD/BD content, handle decoding errors.

### Verification
- Test with various ISO types; verify correct extraction and labeling.

---

## Phase 4: Exotic Formats & NTSC/PAL Handling
### Goals
- Extract deep technical video metadata (NTSC/PAL, scan type, chroma, color info).

### Key Changes
- **format_utils.py**: Add `format_scan_type`, `format_chroma`, `format_color_info`.
- **pymediainfo_parser.py**, **ffprobe_parser.py**: Extract and merge new technical fields.
- **media_parser.py**: Orchestrate reliable collection of new fields.

### Verification
- Automated tests for NTSC/PAL, HDR, interlaced/progressive detection.
- Corruption/timeout tests for parser resilience.

---

## Phase 5: Deep Exotic Formats & Settings Verification
### Goals
- Expand support for legacy/high-fidelity media (DSD, LaserDisc, HD DVD, CD Audio).
- Ensure parser settings (CLI flags) are respected.

### Key Changes
- **format_utils.py**: Add DSD extensions, update heuristics for legacy formats.
- **media_parser.py**: Update magic byte verification, detect HD DVD.
- **ffprobe_parser.py**, **ffmpeg_parser.py**: Ensure settings are passed and used.

### Verification
- Automated tests for HD DVD, DSD, settings effect, scan order extraction.

---

## Phase 6: Playability Logic & Game Categories
### Goals
- Distinguish between index-only software and playable media.

### Key Changes
- **format_utils.py**: Heuristics for PC/Digital games, `is_playable` helper.
- **models.py**: Add `is_playable` property to `MediaItem`.
- **UI**: Respect `is_playable` flag for play button visibility.

### Verification
- Automated tests for game/steam detection and playability filter.
- Manual UI verification.

---

## Phase 7: CD/DVD Standards (Rainbow & DVD Books)
### Goals
- Detect full spectrum of optical media standards (VCD, SVCD, CD-i, Photo CD, DVD-Audio, DVD-VR, etc.).

### Key Changes
- **format_utils.py**: Update detection for CD/DVD standards.
- **media_parser.py**: Scan for specialized directories in ISOs.

### Verification
- Automated tests for VCD/SVCD, DVD-Audio, Photo CD, CD-i detection.
- UI label verification.

---

## Phase 8: High-Resolution Audio Support
### Goals
- Detect and label high-res audio downloads (Qobuz, HDtracks, DSD).

### Key Changes
- **format_utils.py**: Update detection for high-res audio, DSD expansion.
- **is_playable**: Ensure all high-res variants are playable.

### Verification
- Automated and manual tests for high-res detection and UI highlighting.

---

## Phase 9: Advanced Transcoding & Multi-Engine Player
### Goals
- Matrix-based player architecture (FFmpeg, VLC, mkvmerge → Chrome, Embedded, VLC).

### Key Changes
- **app_bottle.py**, **main.py**: Add/expand streaming endpoints and player logic.
- **app.html**: Reorganize UI for engine/output pairs.

### Verification
- Automated tests for backend engines and audio routing.
- Manual tests for player switching and embedded feel.

---

## Phase 10: Parser Branch Separation
### Goals
- Separate audio-only and multimedia parsing logic.

### Key Changes
- **media_parser.py**: Define AUDIO_PARSER_IDS, MULTIMEDIA_PARSER_IDS, branch logic.
- **format_utils.py**: Consolidate category definitions.

### Verification
- Automated and manual tests for branch separation and logging.

---

## Phase 11: Directory Restructuring
### Goals
- Organize project files for maintainability and .gitignore effectiveness.

### Key Changes
- Create `src/core`, `src/parsers`, `infra`, `docs`, `scripts`, `data` directories.
- Update imports and path constants.
- Clean up .gitignore.

### Verification
- Automated and manual tests for import resolution, build scripts, and project cleanliness.

---

## Phase 12: Test Organization & Debug Artifacts
### Goals
- Group test scripts and centralize debug artifacts.

### Key Changes
- Organize `tests/` into subdirectories; add `tests/debug_artifacts/`.
- Update .gitignore for debug folder.

### Verification
- Automated and manual tests for test discovery and artifact redirection.

---

## Summary
All phases are tracked with explicit verification plans. Parser chain robustness, technical metadata extraction, format expansion, playability logic, and project structure have been systematically enhanced. Automated and manual tests confirm resilience, accuracy, and maintainability across the pipeline.
