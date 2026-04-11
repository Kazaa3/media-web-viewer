# SENTINEL Forensic Suite Walkthrough (v1.37.12)

## Overview
The SENTINEL Forensic Suite now provides persistent, exportable, and high-performance diagnostic trace management for the Media Viewer.

## Key Features
- **Persistent History**: Traces are buffered in localStorage and survive reloads/restarts.
- **Forensic Export**: [EXPORT] button downloads a .txt log of all system events.
- **Auto-Rehydration**: History is instantly restored when the sidebar opens.
- **Log Management**: [CLEAR] command resets the buffer for new sessions.

## Usage
1. Open the Diagnostics Overlay and navigate to the SENTINEL tab.
2. Observe live and historical traces.
3. Use [EXPORT] to download logs for analysis.
4. Use [CLEAR] to reset the trace buffer.

## Next Investigation
- Modularize Video Health (VID) tab for FFmpeg pipeline tracing?
- Focus on Database Index Resilience?
