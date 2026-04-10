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
 * Authoritative sync from Python backend to UI (v1.41.103 Tiered SSOT).
 */
async function syncVersion() {
    if (typeof eel !== 'undefined' && typeof eel.get_version_info === 'function') {
        try {
            const info = await eel.get_version_info()();
            
            // Smart Version Handling (Prevent double 'vv' prefix)
            const cleanVer = (v) => v.startsWith('v') ? v : 'v' + v;
            
            window.MWV_VERSION = cleanVer(info.app);
            window.MWV_BE_VERSION = cleanVer(info.backend);
            window.MWV_FE_VERSION = cleanVer(info.frontend);

            const el = document.getElementById('mwv-footer-version');
            if (el) el.innerText = window.MWV_VERSION;

            console.group('>>> [SYSTEM] MWV Tiered Version Sync');
            console.log(`Global App:  ${window.MWV_VERSION}`);
            console.log(`Backend Core: ${window.MWV_BE_VERSION}`);
            console.log(`Frontend UI:  ${window.MWV_FE_VERSION}`);
            console.groupEnd();
        } catch (e) {
            console.warn('[Version] Tiered Sync failed:', e);
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
