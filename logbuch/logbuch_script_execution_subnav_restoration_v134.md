# UI Master: Script Execution & Sub-Nav Restoration (v1.34)

## Problem
Sub-navigation tabs (e.g., 'Mediengalerie', 'Debug DB') were unresponsive due to browser security: scripts inside fragments loaded via innerHTML were not executed, breaking sub-tab logic.

## Solution Plan

### 1. Refactor Fragment Loader
- Updated fragment_loader.js:
  - After setting innerHTML, all <script> tags are found and re-injected as new script elements.
  - Script contents and attributes are copied, and scripts are appended to the document head or target container, ensuring execution.

### 2. Verify Sub-Nav Functionality
- Confirmed that switching functions in fragments are globally available:
  - Player: switchPlayerView('mediengalerie')
  - Options: switchOptionsView('general')
  - Diagnostics: switchDiagnosticsView('debug-db')

## Verification Plan

### Automated
- [ ] Script Extraction Test: Inject mock fragment with console.log script and verify execution.
- [ ] Category Audit: Confirm clicking 'Queue' or 'Mediengalerie' toggles visibility classes.

### Manual
- [ ] Navigation Audit: Manually click all 11 category sub-tabs to ensure 'black screen' states are resolved.
