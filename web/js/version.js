/**
 * version.js (v1.35.60)
 * Central version and performance monitoring.
 * Milestone: Universal Interaction Polish (Menu Fixes & Routing).
 */

window.MWV_VERSION = 'v1.35.60';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Interaction-Complete-Baseline';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
