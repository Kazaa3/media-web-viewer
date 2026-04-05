/**
 * version.js (v1.35.55)
 * Central version and performance monitoring.
 * Milestone: Nuclear Restart & Script Overhaul.
 */

window.MWV_VERSION = 'v1.35.55';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Nuclear-Reboot-Ready';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
