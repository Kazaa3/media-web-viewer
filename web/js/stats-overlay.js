/**
 * @file stats-overlay.js
 * @brief Real-time performance monitoring for the Video Player.
 * @details Displays GPU usage, bitrate, FPS, and RTT via a glassmorphism overlay.
 * 
 * [AI-READINESS: High Level Context]
 * This module orchestrates real-time diagnostic overlays for video playback.
 * Main Entry: window.StatsOverlay.toggle()
 * Dependencies: Video.js, eel (Python Backend)
 * Complexity: Low (Pure DOM manipulation and interval polling)
 */

window.StatsOverlay = (function() {
    let overlay = null;
    let updateInterval = null;
    let isVisible = false;

    function init() {
        if (overlay) return;
        
        overlay = document.createElement('div');
        overlay.id = 'video-stats-overlay';
        overlay.style = `
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: #00f0ff;
            padding: 15px;
            border-radius: 12px;
            font-family: 'Inter', sans-serif;
            font-size: 12px;
            z-index: 10000;
            border: 1px solid rgba(0, 240, 255, 0.3);
            display: none;
            pointer-events: none;
            box-shadow: 0 4px 20px rgba(0,0,0,0.5);
            min-width: 200px;
        `;
        
        overlay.innerHTML = `
            <h4 style="margin: 0 0 10px 0; font-size: 14px; color: #fff; border-bottom: 1px solid #333; padding-bottom: 5px;">Stats for Nerds</h4>
            <div id="stats-content">
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span>Protocol:</span><span id="stat-protocol">-</span></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span>Resolution:</span><span id="stat-resolution">-</span></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span>Codec:</span><span id="stat-codec">-</span></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span>Bitrate:</span><span id="stat-bitrate">-</span></div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span>Frames:</span><span id="stat-fps">-</span> / <span id="stat-dropped">0</span> dropped</div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;"><span>GPU/HWA:</span><span id="stat-gpu">-</span></div>
                <div style="display:flex; justify-content:space-between;"><span>Buffer/RTT:</span><span id="stat-rtt">-</span></div>
            </div>
        `;
        
        const playerContainer = document.querySelector('.video-container') || document.body;
        playerContainer.appendChild(overlay);
    }

    function toggle() {
        isVisible = !isVisible;
        if (isVisible) {
            init();
            overlay.style.display = 'block';
            startUpdating();
        } else {
            if (overlay) overlay.style.display = 'none';
            stopUpdating();
        }
    }

    function startUpdating() {
        stopUpdating();
        updateInterval = setInterval(updateStats, 1000);
        updateStats();
    }

    function stopUpdating() {
        if (updateInterval) {
            clearInterval(updateInterval);
            updateInterval = null;
        }
    }

    async function updateStats() {
        if (!overlay && !document.getElementById('video-analyzer-panel')) return;
        
        let player = null;
        try {
            player = videojs('native-html5-video-resource-node');
        } catch(e) {}
        if (!player) return;

        // Frontend Stats
        const tech = player.tech({ IWillNotUseThisInPlugins: true });
        let dropped = 0;
        let fps = 0;
        let buffer = 0;
        
        if (tech && tech.el()) {
            const el = tech.el();
            if (el.getVideoPlaybackQuality) dropped = el.getVideoPlaybackQuality().droppedVideoFrames;
            
            // Calculate buffer
            if (el.buffered && el.buffered.length > 0) {
                buffer = (el.buffered.end(el.buffered.length - 1) - el.currentTime()).toFixed(1);
            }
        }

        // Update Overlay (if visible)
        if (isVisible && overlay) {
            document.getElementById('stat-protocol').innerText = window.currentPlaybackProtocol || 'Auto-Route';
            document.getElementById('stat-resolution').innerText = `${player.videoWidth()}x${player.videoHeight()}`;
            document.getElementById('stat-dropped').innerText = dropped;
        }

        // Update Integrated Analyzer (Cinema Engine Tab)
        const analyzer = document.getElementById('video-analyzer-panel');
        if (analyzer) {
            safeText('metric-buffer', buffer + 's');
            // Mocking FPS/Bitrate from player if not available from backend
            safeText('metric-fps', (window._vjs_fps || 24).toFixed(1));
        }
        
        // Backend Stats via Eel
        try {
            const stats = await eel.get_playback_stats()();
            if (stats) {
                if (isVisible && overlay) {
                    document.getElementById('stat-codec').innerText = stats.codec || '-';
                    document.getElementById('stat-bitrate').innerText = stats.bitrate || '-';
                    document.getElementById('stat-gpu').innerText = stats.gpu_info || 'Software';
                    document.getElementById('stat-rtt').innerText = `${stats.rtt_ms || '-'}ms`;
                }

                if (analyzer) {
                    safeText('metric-bitrate', stats.bitrate || '0');
                    if (stats.fps) safeText('metric-fps', stats.fps.toFixed(1));
                    safeText('metric-hw', stats.gpu_info ? 'ACTIVE' : 'OFF');
                }
            }
        } catch (e) {
            console.warn("[Stats] Backend heartbeat failed:", e);
        }
    }

    function safeText(id, text) {
        const el = document.getElementById(id);
        if (el) el.innerText = text;
    }

    return {
        toggle: toggle,
        init: init
    };
})();
