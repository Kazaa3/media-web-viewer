/**
 * version.js (v1.35.48)
 * Central version and performance monitoring.
 * Nuclear Diagnostic Override (Ensures tools are visible).
 */

window.MWV_VERSION = 'v1.35.48';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Hydration-Harden';

// Forced Diagnostic Enable (v1.35.48)
// Ensures the Red Header and Green HUD appear for the user.
if (localStorage.getItem('mwv_diagnostic_mode') !== 'true') {
    console.log(">>> [SYSTEM] Enabling Nuclear Diagnostic Mode (v1.35.48)");
    localStorage.setItem('mwv_diagnostic_mode', 'true');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
console.log(`>>> [SYSTEM] Boot-Timer started.`);
