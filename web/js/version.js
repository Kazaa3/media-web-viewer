/**
 * version.js (v1.35.63)
 * Central version and performance monitoring.
 * Milestone: Diagnostic Sync & Routing (29 Items).
 */

window.MWV_VERSION = 'v1.35.68';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Pro-Options-Active';

// Diagnostic mode is now controlled via Options panel
if (localStorage.getItem('mwv_diagnostic_mode') === null) {
    localStorage.setItem('mwv_diagnostic_mode', 'false');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
