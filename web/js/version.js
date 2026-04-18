/**
 * version.js (v1.35.63)
 * Central version and performance monitoring.
 * Milestone: Diagnostic Sync & Routing (29 Items).
 */

window.MWV_VERSION = 'v1.46.00-STABLE';
window.MWV_BOOT_START = performance.now();
window.MWV_STABILITY = 'Pro-Options-Active';

/**
 * syncVersion()
 * Authoritative sync from Python backend to UI (v1.41.103 Tiered SSOT).
 */
async function syncVersion(retries = 5) {
    if (typeof eel !== 'undefined' && typeof eel.get_version_info === 'function') {
        try {
            const info = await eel.get_version_info()();
            
            // Smart Version Handling (Prevent double 'vv' prefix)
            const cleanVer = (v) => v.startsWith('v') ? v : 'v' + v;
            
            window.MWV_VERSION = cleanVer(info.app);
            window.MWV_BE_VERSION = cleanVer(info.backend);
            window.MWV_FE_VERSION = cleanVer(info.frontend);

            const el = document.getElementById('mwv-footer-version');
            if (el) {
                el.innerText = window.MWV_VERSION;
                el.style.opacity = "1";
                el.style.color = "var(--accent-color)";
            }

            console.log(`[SYSTEM] Tiered Version Sync Succeeded: ${window.MWV_VERSION}`);

            // [v1.46.081] FE Forensics (PID & Browser Identity)
            if (typeof eel.get_frontend_forensics === 'function') {
                try {
                    const feInfo = await eel.get_frontend_forensics()();
                    const hudFe = document.getElementById('hud-fe');
                    if (hudFe) {
                        const browserStr = feInfo.browser_type !== "Discovery..." ? feInfo.browser_type : "N/A";
                        hudFe.setAttribute('data-hud-metrics', `[FRONTEND FORENSICS] PID: ${feInfo.fe_pid} | Browser: ${browserStr}`);
                    }
                } catch (feErr) {
                    console.warn('[Forensics] FE Probe failed:', feErr);
                }
            }
        } catch (e) {
            console.warn(`[Version] Sync failed (Retries left: ${retries}):`, e);
            if (retries > 0) {
                setTimeout(() => syncVersion(retries - 1), 1000);
            }
        }
    } else {
        if (retries > 0) {
            setTimeout(() => syncVersion(retries - 1), 500);
        }
    }
}

// Created with MWV v1.46.00-MASTER

// Initial sync on script load
syncVersion();

// Diagnostic mode is now controlled via Options panel
if (localStorage.getItem('mwv_diagnostic_mode') === null) {
    localStorage.setItem('mwv_diagnostic_mode', 'false');
}

console.log(`>>> [SYSTEM] MWV Frontend version initialized: ${window.MWV_VERSION}`);
