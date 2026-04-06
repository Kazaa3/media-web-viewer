# Forensic Expansion Plan: Video Health (VID) & Database Resilience (DBI) (v1.37.13)

## 🛡️ Building Forensic Station

- **Deep FFmpeg Probes:**
  - Modularized video-pipeline tracing to report on stream stability and remuxing latency.
  - Enables real-time detection of FFmpeg pipeline issues.

- **SQLite Resilience:**
  - Integrated `check_ui_integrity` audit into a dedicated DBI suite.
  - Identifies "0-item" anomalies and database inconsistencies.

- **Ghost Buster Forensic:**
  - File-System Parity Scan detects and reports any media entries in the database that are missing from disk.
  - Provides safe reporting and future pruning options for dead entries.

---

**Principle:** "Nur ergänzen und nichts entfernen" — All expansions are additive and modular.

---

The Diagnostics Overlay is being rebuilt as a professional forensic interface for deep-tracing FFmpeg pipelines and SQLite integrity.
