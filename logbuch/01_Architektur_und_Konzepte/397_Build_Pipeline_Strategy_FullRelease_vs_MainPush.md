# Build Pipeline Strategy: Full Release vs Main Push

## Overview

This document formalizes the build and deployment strategy for the Media Web Viewer project.

### Full Release (Tagged)
- Triggered by a version tag
- Runs full build, test, and artifact generation
- Publishes packages and management reports
- Ensures all version sync and metadata are up to date

### Main Push (CI-only)
- Triggered by push to main branch (no tag)
- Runs fast validation and test suite
- No external artifact publishing
- Used for rapid iteration and integration

### Key Differences
- Artifact publishing (Full Release only)
- Depth of validation and reporting
- Version/metadata synchronization

---

For implementation details, see `build_system.py` and CI workflow files in `.github/workflows/`.
