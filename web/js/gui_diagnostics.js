/**
 * MWV_Diagnostics: GUI Logging & Hub (v1.41)
 * Provides a real-time, forensic logging overlay.
 */
window.MWV_Diagnostics = (() => {
    let logOverlay = null;
    let isMonitoring = false;
    let pollInterval = null;

    function init() {
        createLogOverlay();
        console.info("[MWV-DIAG] Diagnostics Engine Ready.");
    }

    function createLogOverlay() {
        if (document.getElementById('mwv-log-overlay')) return;

        logOverlay = document.createElement('div');
        logOverlay.id = 'mwv-log-overlay';
        logOverlay.className = 'forensic-overlay';
        logOverlay.style.cssText = `
            position: fixed; top: 50px; right: 20px; bottom: 60px; width: 450px;
            background: rgba(5, 5, 8, 0.96); backdrop-filter: blur(25px);
            border: 1px solid var(--accent-color); border-radius: 12px;
            box-shadow: var(--shadow-medium); z-index: 10006;
            display: none; flex-direction: column; overflow: hidden;
            font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
            color: #eee;
        `;

        logOverlay.innerHTML = `
            <div class="overlay-header" style="padding: 12px 15px; background: rgba(0, 242, 255, 0.1); border-bottom: 1px solid rgba(0, 242, 255, 0.2); display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 11px; font-weight: 900; color: var(--accent-color);">SYSTEM TRACE LOGS</span>
                <button onclick="MWV_Diagnostics.toggle()" style="background: none; border: none; color: #fff; cursor: pointer; font-size: 16px;">&times;</button>
            </div>
            <div id="mwv-log-content" style="flex: 1; padding: 10px; overflow-y: auto; font-size: 10px; line-height: 1.4;">
                <div style="color: #666; font-style: italic;">Connecting to log buffer...</div>
            </div>
            <div class="overlay-footer" style="padding: 8px 15px; border-top: 1px solid #222; display: flex; gap: 10px;">
                <button class="hud-btn-tiny" onclick="MWV_Diagnostics.clear()">CLEAR</button>
                <div style="font-size: 9px; opacity: 0.5; flex: 1; text-align: right;">v1.41 Global-Sync</div>
            </div>
        `;

        document.body.appendChild(logOverlay);
    }

    async function pollLogs() {
        if (!isMonitoring) return;
        try {
            if (typeof eel !== 'undefined' && typeof eel.get_ui_logs === 'function') {
                const logs = await eel.get_ui_logs()();
                updateLogList(logs);
            }
        } catch (e) {
            console.warn("[MWV-DIAG] Log poll failed:", e);
        }
    }

    function updateLogList(logs) {
        const content = document.getElementById('mwv-log-content');
        if (!content) return;

        content.innerHTML = logs.map(log => {
            let color = "#eee";
            if (log.includes("[ERROR]")) color = "#ff453a";
            if (log.includes("[WARN]")) color = "#ffd60a";
            if (log.includes("[DEBUG]")) color = "#bf5af2";
            if (log.includes("[JS-NAV]")) color = "#64d2ff";

            return `<div style="color: ${color}; margin-bottom: 4px; border-bottom: 1px solid rgba(255,255,255,0.03); padding-bottom: 2px;">${formatLog(log)}</div>`;
        }).join('');
        
        // Auto-scroll to bottom
        content.scrollTop = content.scrollHeight;
    }

    function formatLog(raw) {
        // Strip timestamps if repetitive or format nicely
        return raw.replace(/</g, "&lt;").replace(/>/g, "&gt;");
    }

    function toggle() {
        if (!document.getElementById('mwv-log-overlay')) {
            console.warn("[MWV-DIAG] Log overlay missing during toggle. Re-creating...");
            createLogOverlay();
        }
        
        const overlay = document.getElementById('mwv-log-overlay');
        if (!overlay) return;

        isMonitoring = !isMonitoring;
        overlay.style.display = isMonitoring ? 'flex' : 'none';

        if (isMonitoring) {
            pollLogs();
            const pollMs = window.CONFIG?.technical_orchestrator?.intervals?.log_polling_ms || 1000;
            pollInterval = setInterval(pollLogs, pollMs);
        } else {
            clearInterval(pollInterval);
        }
    }

    function clear() {
        const content = document.getElementById('mwv-log-content');
        if (content) content.innerHTML = '';
        // Note: This only clears the UI view, not the backend buffer.
    }

    /**
     * [v1.41.122] Emergency Hydration Test
     * Forces hardcoded items into the queue and triggers a re-render.
     */
    function forceHydrationTest() {
        console.warn("[MWV-DIAG] Triggering Emergency Hydration Test (Centralized Mock Registry)...");
        
        // [v1.55.020] Fetch from Centralized Registry (v1.55.020 Transition)
        const eliteMockPack = window.CONFIG?.mock_collection || [];
        
        if (eliteMockPack.length === 0) {
            console.error("[MWV-DIAG] FAILED: No mock_collection found in window.CONFIG.");
            if (typeof showToast === 'function') showToast("ABORTED: Registry Empty", "error");
            return;
        }

        // 1. Force state into global registries
        window.allLibraryItems = [...eliteMockPack]; // Crucial for renderLibrary to work
        window.currentPlaylist = [...eliteMockPack];
        window.__mwv_last_db_count = eliteMockPack.length;

        // 2. Sync with UI Components
        if (typeof window.syncQueueWithLibrary === 'function') {
            console.log("[MWV-DIAG] Syncing Centralized Mock Pack with session...");
            window.currentPlaylist = [...eliteMockPack];
        }

        // 3. Force Global Re-Render
        if (typeof window.renderAudioQueue === 'function') window.renderAudioQueue();
        if (typeof window.renderLibrary === 'function') window.renderLibrary();

        // 4. Update HUD and Toast
        const countEls = document.querySelectorAll('.synced-count');
        countEls.forEach(el => el.innerText = `${eliteMockPack.length} Titel`);
        
        if (typeof switchMainCategory === 'function') switchMainCategory('media');

        if (typeof showToast === 'function') showToast("EMERGENCY HYDRATION ACTIVE", 3000);
    }

    function getState() {
        return {
            isMonitoring,
            overlayVisible: logOverlay && logOverlay.style.display !== 'none'
        };
    }

    return { init, toggle, clear, forceHydrationTest, getState };
})();

// Auto-inject appendUiTrace hook for real-time (called by backend)
// Created with MWV v1.46.017-MASTER
window.MWV_Diagnostics = MWV_Diagnostics;

document.addEventListener('DOMContentLoaded', () => {
    if (window.MWV_Diagnostics && typeof window.MWV_Diagnostics.init === 'function') {
        window.MWV_Diagnostics.init();
    }
});
