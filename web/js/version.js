/**
 * version.js (v1.35.59)
 * Central version and performance monitoring.
 * Milestone: Precision Video Cinema (Native, HD-Pass, Legacy, ISO).
 */

window.MWV_VERSION = 'v1.35.59';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Cinema-Precision-Baseline';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
