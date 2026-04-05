/**
 * version.js (v1.35.61)
 * Central version and performance monitoring.
 * Milestone: Diagnostic Baseline & Filtered Queue (29 Items).
 */

window.MWV_VERSION = 'v1.35.61';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Baseline-Hydrated-Filter-Active';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
