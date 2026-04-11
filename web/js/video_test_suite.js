/**
 * @file video_test_suite.js
 * @brief Automated JS-based validation for the Video Player.
 * @details Programmatically interacts with the video player to verify routing, stream health and Video.js stability.
 */

window.VideoTestSuite = (function() {
    const results = [];
    
    async function runAllTests() {
        console.info("<svg width='12' height='12'><use href='#icon-test'></use></svg> [VideoTestSuite] Starting Automated JS Batch...");
        results.length = 0; // Clear
        
        // 1. Check Video.js Presence
        const vjsCheck = typeof videojs !== 'undefined';
        logResult("Video.js Loaded", vjsCheck);
        
        // 2. Fetch Media Sample from Backend
        const media = await eel.get_all_media()();
        const videoFiles = media.filter(m => m.category === 'Film' || ['mp4', 'mkv', 'webm'].includes(m.name.toLowerCase().split('.').pop()));
        
        if (videoFiles.length === 0) {
            logResult("Media Discovery", false, "No video files found for testing.");
            displayResults();
            return;
        }
        logResult("Media Discovery", true, `Found ${videoFiles.length} candidate(s).`);

        // 3. Test first candidate in Direct Mode
        const sample = videoFiles[0];
        try {
            await testPlayback(sample, 'direct_play');
        } catch (e) {
            logResult("Playback: Direct Play", false, e.message);
        }

        // 4. Test first candidate in MSE Mode (if not 4K)
        try {
            await testPlayback(sample, 'mse');
        } catch (e) {
            logResult("Playback: MSE Remux", false, e.message);
        }

        console.info("<svg width='12' height='12'><use href='#icon-test'></use></svg> [VideoTestSuite] Finalizing results...");
        displayResults();
    }

    async function testPlayback(item, mode) {
        console.log(`[VideoTestSuite] Testing ${item.name} via ${mode}...`);
        
        // Use smart_route bypass logic for test forcing
        const url = await eel.get_universal_stream_url(item.path, mode)();
        if (!url || url === "") throw new Error("Backend failed to return stream URL.");
        
        const player = videojs('native-html5-video-resource-node');
        if (!player) throw new Error("Video.js player instance 'native-html5-video-resource-node' not found.");

        return new Promise((resolve, reject) => {
            const timeout = setTimeout(() => {
                player.off('error');
                player.off('playing');
                reject(new Error("Playback timeout (10s)"));
            }, 10000);

            player.one('error', () => {
                clearTimeout(timeout);
                reject(new Error(`Player Error: ${player.error().message}`));
            });

            player.one('playing', () => {
                clearTimeout(timeout);
                logResult(`Playback: ${mode}`, true, `Streaming ${item.name} successfully.`);
                player.pause();
                resolve();
            });

            player.src({ src: url, type: mode === 'mse' ? 'video/mp4' : 'video/mp4' }); // Simplified type for test
            player.play().catch(e => reject(new Error(`Play() failed: ${e.message}`)));
        });
    }

    function logResult(testName, success, message = "") {
        const icon = success ? "<svg width='12' height='12'><use href='#icon-save'></use></svg>" : "<svg width='12' height='12'><use href='#icon-delete'></use></svg>";
        console.log(`${icon} [VideoTestSuite] ${testName}: ${message}`);
        results.push({ name: testName, success, message, icon, time: new Date().toLocaleTimeString() });
    }

    function displayResults() {
        const container = document.getElementById('debug-logbuch-list') || document.body;
        const div = document.createElement('div');
        div.className = 'test-suite-summary-overlay';
        div.style = "position:fixed; bottom: 20px; right: 20px; background: rgba(0,0,0,0.9); color: white; padding: 20px; border-radius: 12px; z-index: 9999; border: 1px solid #00f0ff; max-width: 400px; font-family: 'Inter', sans-serif; box-shadow: 0 0 20px rgba(0,240,255,0.3);";
        
        let html = `<h2 style="margin-top:0; color:#00f0ff; display:flex; justify-content:space-between;"><svg width='20' height='20'><use href='#icon-test'></use></svg> Test Suite <span>${results.filter(r => r.success).length}/${results.length}</span></h2><hr style="border:0; border-top:1px solid #333;">`;
        results.forEach(r => {
            html += `<div style="margin: 8px 0; display:flex; justify-content:space-between;">
                        <span style="${r.success ? 'color:#00ff88' : 'color:#ff4444'}">${r.icon} ${r.name}</span>
                        <small style="opacity:0.6;">${r.time}</small>
                     </div>`;
            if (r.message && !r.success) {
                html += `<div style="font-size:11px; opacity:0.8; margin-left:22px; margin-bottom:10px; color:#ffcc00">${r.message}</div>`;
            }
        });
        html += `<button onclick="this.parentElement.remove()" style="width:100%; border:0; background:#333; color:white; padding:8px; border-radius:4px; cursor:pointer; margin-top:10px;">Schließen</button>`;
        
        div.innerHTML = html;
        document.body.appendChild(div);
    }

    return {
        run: runAllTests
    };
})();

// Created with MWV v1.46.00-MASTER
