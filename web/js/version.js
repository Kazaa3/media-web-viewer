/**
 * version.js (v1.35.51)
 * Central version and performance monitoring.
 * Hotfix: Relocated Diagnostic Bar to Bottom-Right.
 */

window.MWV_VERSION = 'v1.35.51';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'UI-Relocate-Hotfix';

// Forced Diagnostic Enable
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
