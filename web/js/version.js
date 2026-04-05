/**
 * version.js (v1.35.53)
 * Central version and performance monitoring.
 * Milestone: Format Expansion (M4B, AAC, M4A).
 */

window.MWV_VERSION = 'v1.35.53';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Format-Expansion';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
