/**
 * version.js (v1.35.63)
 * Central version and performance monitoring.
 * Milestone: Diagnostic Sync & Routing (29 Items).
 */

window.MWV_VERSION = 'v...';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Pro-Options-Active';

/**
 * syncVersion()
 * Authoritative sync from Python backend to UI.
 */
async function syncVersion() {
    if (typeof eel !== 'undefined' && typeof eel.get_version === 'function') {
        try {
            const v = await eel.get_version()();
            window.MWV_VERSION = 'v' + v;
            const el = document.getElementById('mwv-footer-version');
            if (el) el.innerText = window.MWV_VERSION;
            console.log(`>>> [SYSTEM] MWV Version Synchronized: ${window.MWV_VERSION}`);
        } catch (e) {
            console.warn('[Version] Sync failed:', e);
        }
    }
}

// Initial sync on script load
syncVersion();

// Diagnostic mode is now controlled via Options panel
if (localStorage.getItem('mwv_diagnostic_mode') === null) {
    localStorage.setItem('mwv_diagnostic_mode', 'false');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
