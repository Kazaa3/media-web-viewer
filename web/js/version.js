/**
 * version.js (v1.35.56)
 * Central version and performance monitoring.
 * Milestone: Audio Transcoding Baseline (ALAC, WMA).
 */

window.MWV_VERSION = 'v1.35.56';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Audio-Transcoding-Baseline';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
