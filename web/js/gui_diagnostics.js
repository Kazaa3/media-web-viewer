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
        console.warn("[MWV-DIAG] Triggering Emergency Hydration Test (Elite Mock Pack)...");
        
        const eliteMockPack = [
            { id: "mock_a1", name: "Cyberpunk_Nocturne.flac", path: "mock/a1.flac", category: "Audio", codec: "FLAC", bitrate: "1411kbps", samplerate: "44.1kHz", tags: { title: "Nocturne in Neon", artist: "Ghost City", album: "Electric Dreams", duration: 324 } },
            { id: "mock_a2", name: "Forensic_Vocal_Capture_04.wav", path: "mock/a2.wav", category: "Audio", codec: "PCM", bitrate: "2304kbps", samplerate: "48kHz", tags: { title: "Vocal Evidence #04", artist: "Field Recorder", album: "Forensic Samples", duration: 185 } },
            { id: "mock_v1", name: "Security_Cam_A4.mp4", path: "mock/v1.mp4", category: "Video", codec: "H.264", bitrate: "8Mbps", tags: { title: "Security Footage A4", artist: "CCTV-Node-09", duration: 1200 } },
            { id: "mock_a3", name: "Ambient_Rain_3D.mp3", path: "mock/a3.mp3", category: "Audio", codec: "MP3", bitrate: "320kbps", tags: { title: "City Rain (Binaural)", artist: "Atmos-X", album: "Soundscapes", duration: 600 } },
            { id: "mock_p1", name: "Tech_Weekly_Ep99.m4a", path: "mock/p1.m4a", category: "Podcast", codec: "AAC", bitrate: "128kbps", tags: { title: "AI Agency & The Future", artist: "Tech Weekly", album: "Podcast Archive", duration: 3600 } },
            { id: "mock_a4", name: "Deep_Blue_Sub_Bass.ogg", path: "mock/a4.ogg", category: "Audio", codec: "Vorbis", bitrate: "192kbps", tags: { title: "Deep Sea Frequency", artist: "Sub-Sonic", album: "Abyss", duration: 240 } },
            { id: "mock_v2", name: "Drone_Flyover_HD.mkv", path: "mock/v2.mkv", category: "Video", codec: "H.265", bitrate: "12Mbps", tags: { title: "City Flyover 4K", artist: "Drone-Unit-7", duration: 450 } },
            { id: "mock_a5", name: "Lost_Transmission.wav", path: "mock/a5.wav", category: "Audio", codec: "PCM", bitrate: "1536kbps", tags: { title: "Static Signal #01", artist: "EVP-Hunter", album: "Classified", duration: 45 } },
            { id: "mock_m1", name: "Metadata_Test_Extreme.flac", path: "mock/m1.flac", category: "Audio", codec: "FLAC", tags: { title: "Title with Special Char !@#$%", artist: "Extremely Long Artist Name That Should Be Truncated By The CSS System", album: "Standard Album", duration: 10 } },
            { id: "mock_a6", name: "Jazz_Midnight_Session.mp3", path: "mock/a6.mp3", category: "Audio", codec: "MP3", bitrate: "256kbps", tags: { title: "After Hours", artist: "The Blue Notes", album: "Jazz Room", duration: 520 } },
            { id: "mock_a7", name: "Classical_Requiem.opus", path: "mock/a7.opus", category: "Audio", codec: "Opus", bitrate: "96kbps", tags: { title: "Requiem in D Minor", artist: "Symphony Orchestra", album: "Masterpieces", duration: 900 } },
            { id: "mock_v3", name: "Thermal_Scan_A.mp4", path: "mock/v3.mp4", category: "Video", codec: "H.264", tags: { title: "Thermal Analysis A", artist: "Scan-Tech", duration: 300 } }
        ];

        // 1. Force state into global registries
        window.allLibraryItems = [...eliteMockPack]; // Crucial for renderLibrary to work
        window.currentPlaylist = [...eliteMockPack];
        window.__mwv_last_db_count = eliteMockPack.length;

        // 2. Sync with UI Components
        if (typeof window.syncQueueWithLibrary === 'function') {
            console.log("[MWV-DIAG] Syncing Elite Mock Pack with session...");
            // Manual population of currentPlaylist if syncQueueWithLibrary is too strict
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
