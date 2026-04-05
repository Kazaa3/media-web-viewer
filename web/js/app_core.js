console.log(">>> [JS-LOAD] app_core.js initialized.");
if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', 'JS-LOAD', { file: 'app_core.js', ts: Date.now() });
// --- Boot Watchdog & Progress Audit (v1.35) ---
let __mwv_boot_watchdog_timer = null;
let __mwv_boot_watchdog_ticks = 0;
let __mwv_boot_watchdog_status = 'INIT';
function startBootWatchdog() {
    if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', 'START', { ts: Date.now() });
    __mwv_boot_watchdog_status = 'STARTED';
    __mwv_boot_watchdog_ticks = 0;
    __mwv_boot_watchdog_timer = setInterval(() => {
        try {
            __mwv_boot_watchdog_ticks++;
            let phase = 'WAIT';
            if (document.readyState === 'complete') phase = 'DOM-READY';
            if (window.__mwv_ui_nav_loaded) phase = 'INIT-START';
            
            // Safe access using typeof (v1.35.1 Hardened)
            const hasLib = (typeof allLibraryItems !== 'undefined');
            const libCount = hasLib ? allLibraryItems.length : 0;
            if (hasLib && libCount > 0) phase = 'DATA-READY';
            
            if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', phase, { tick: __mwv_boot_watchdog_ticks, items: libCount });
            
            if (phase === 'DATA-READY' || __mwv_boot_watchdog_ticks > 12) { // Allow more time for slow handshakes
                if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', 'SUCCESS', { ticks: __mwv_boot_watchdog_ticks });
                clearInterval(__mwv_boot_watchdog_timer);
                __mwv_boot_watchdog_status = 'DONE';
            }
        } catch (e) {
            console.error("[Watchdog] Diagnostic Crash:", e);
        }
    }, 500);
}

window.addEventListener('DOMContentLoaded', () => {
    try {
        startBootWatchdog();
    } catch (e) {
        if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', 'FAIL', { error: e.message });
        console.error('BOOT-WATCHDOG error:', e);
    }
});

window.addEventListener('error', function (e) {
    if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', 'EXCEPTION', { message: e.message, stack: e.error && e.error.stack });
});
/**
 * Media Viewer Core Orchestrator
 * Central entry point for cross-module coordination and global event handling.
 */

// --- Global Application State ---
let activeAudioPipeline = document.getElementById('native-html5-audio-pipeline-element');
// let currentLogbuchEntries = [];
let currentPlaylist = []; // Shared across Audio/Video modules
let currentVideoItem = null;
let currentVideoPath = null;
let vjsPlayer = null; // Defined as a shared global in Orchestrator

/**
 * Unified Media Playback Router
 * Decides whether to engage the video player or the audio player.
 */
function play(item, path, startTime = 0) {
    if (!item) return;
    console.info(">>> [Orchestrator] Routing playback for:", item.name);
    
    currentVideoItem = item;
    
    // Decipher if it's a video file
    if (isVideoItem(item)) {
        if (typeof playVideo === 'function') {
            playVideo(item, path, startTime);
        } else {
            console.error("[Orchestrator] video.js not loaded or playVideo unavailable.");
        }
        return;
    }

    // Otherwise route to Audio Player
    if (typeof stopVideo === 'function') stopVideo();
    if (typeof playAudio === 'function') {
        playAudio(item, startTime);
    } else {
        console.error("[Orchestrator] audioplayer.js not loaded or playAudio unavailable.");
    }
}

/**
 * Global Routing for media items by object (often from Grid or Coverflow).
 */
function playMediaObject(item) {
    if (!item) return;
    if (isVideoItem(item)) {
        console.info("[Play-Routing] Video detected, switching to Video Player tab:", item.path);
        if (typeof switchTab === 'function') {
            switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
        }
        setTimeout(() => {
            if (typeof playVideo === 'function') playVideo(item, item.path);
        }, 100);
    } else {
        addToQueue(item);
        if (typeof switchTab === 'function') {
            switchTab('player', document.getElementById('active-queue-tab-trigger'));
        }
    }
}

/**
 * Adds an item to the global currentPlaylist.
 */
function addToQueue(item) {
    if (!currentPlaylist) currentPlaylist = [];
    
    // Avoid duplicates in the active queue if desired
    if (!currentPlaylist.find(i => i.path === item.path)) {
        currentPlaylist.push(item);
        if (typeof renderPlaylist === 'function') renderPlaylist();
        if (typeof showToast === 'function') showToast(t('pl_added_to_queue') || "Added to queue");
    } else {
        if (typeof showToast === 'function') showToast(t('pl_already_in_queue') || "Already in queue", "info");
    }
}

/**
 * Global Tab Switching Override (Optional Bridge)
 * Ensures that specific domain logic (like playlist rendering) occurs during transitions.
 */
const originalSwitchTab = window.switchTab;
window.switchTab = function (tabId, btn) {
    if (typeof originalSwitchTab === 'function') {
        originalSwitchTab(tabId, btn);
    } else {
        // Fallback layout switcher if ui_nav_helpers.js is missing
        const contents = document.querySelectorAll('.tab-content');
        contents.forEach(c => c.classList.remove('active'));
        const target = document.getElementById(tabId + '-tab') || document.getElementById(tabId);
        if (target) target.classList.add('active');

        const btns = document.querySelectorAll('.tab-btn');
        btns.forEach(b => b.classList.remove('active'));
        if (btn) btn.classList.add('active');
    }

    // Cross-tab logic requirements
    if ((tabId === 'playlist' || tabId === 'player') && typeof renderPlaylist === 'function') {
        renderPlaylist();
    }
    if (tabId === 'library' && typeof renderLibrary === 'function') {
        renderLibrary();
    }
}

/**
 * VLC Interactive Remote Bridge
 * Captures navigation keys and routes them to the VLC backend when the video tab is active.
 */
document.addEventListener('keydown', async (e) => {
    if (!window._vlc_control_port) return;

    const activeTab = localStorage.getItem('mwv_active_tab');
    if (activeTab !== 'video') return;

    let vlcKey = null;
    switch (e.key) {
        case 'ArrowUp': vlcKey = 'key-up'; break;
        case 'ArrowDown': vlcKey = 'key-down'; break;
        case 'ArrowLeft': vlcKey = 'key-left'; break;
        case 'ArrowRight': vlcKey = 'key-right'; break;
        case 'Enter': vlcKey = 'key-enter'; break;
        case 'Escape': vlcKey = 'key-nav-activate'; break; 
        case 'm': case 'M': vlcKey = 'key-disc-menu'; break;
    }

    if (vlcKey) {
        e.preventDefault();
        console.info("[VLC-Remote] Sending key:", vlcKey);
        try {
            if (typeof eel !== 'undefined' && typeof eel.send_vlc_command === 'function') {
                await eel.send_vlc_command(window._vlc_control_port, 'key', vlcKey)();
            }
        } catch (err) {
            console.error("VLC Remote Error:", err);
        }
    }
});

/**
 * Application Boot Notification
 */
window.addEventListener('DOMContentLoaded', async () => {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('BOOT-WATCHDOG', 'DOM-READY');
    console.log("Core Orchestrator: System checks passing. Initializing UI fragments...");
    
    try {
        if (typeof mwv_trace_render === 'function') mwv_trace_render('BOOT-WATCHDOG', 'INIT-START');
        // 0. Load Modals Fragment
        if (typeof FragmentLoader?.load === 'function') {
            FragmentLoader.load('modals-placeholder', 'fragments/modals_container.html', () => {
                console.log("DOM: Modals fragment initialized.");
                if (typeof initTranslations === 'function') initTranslations();
            });
        } else {
            console.warn("DOM: FragmentLoader not found, modals might not load.");
        }

        // 1. Default Start Screen
        console.log("UI: Setting default category and tab...");
        if (typeof switchMainCategory === 'function') switchMainCategory('media');
        
        // Apply persisted sidebar state
        if (typeof applySidebarState === 'function') applySidebarState();
        
        // Start stats polling for integrated analyzer
        if (window.StatsOverlay && typeof window.StatsOverlay.init === 'function') {
            setInterval(() => {
                if (typeof window.StatsOverlay.updateStats === 'function') {
                    // Only poll if tab is active or overlay is visible
                    const activeTab = localStorage.getItem('mwv_active_tab');
                    if (activeTab === 'video' || window.StatsOverlay.isVisible) {
                        window.StatsOverlay.updateStats();
                    }
                }
            }, 2000);
        }
        
        // Ensure switchTab is called after a tiny delay to allow other modules to settle
        setTimeout(() => {
            if (typeof switchTab === 'function') {
                console.log("UI: Switching to 'player' tab.");
                switchTab('player');
            } else {
                console.error("UI: switchTab function missing during boot!");
            }
        }, 100);
        
        // 2. Initialize Library & Inventory (Prioritized for Video/Audio Sync)
        document.addEventListener('mwv_library_ready', () => {
            console.log("Data: Library ready, syncing specialized components...");
            if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
        });

        setTimeout(async () => {
            console.log("Data: Triggering library and edit-item loads...");
            if (typeof loadLibrary === 'function') await loadLibrary();
            if (typeof loadEditItems === 'function') await loadEditItems();
        }, 150);

        // 3. Fetch and Display Startup Time
        setTimeout(async () => {
            if (typeof eel !== 'undefined' && typeof eel.get_startup_info === 'function') {
                try {
                    const info = await eel.get_startup_info()();
                    const statusSpan = document.getElementById('sync-status');
                    if (statusSpan && info) {
                         const timeSpan = document.createElement('span');
                         timeSpan.style.color = 'var(--text-secondary)';
                         timeSpan.style.marginLeft = '5px';
                         timeSpan.innerText = `(Boot: ${info.boot_duration_sec}s | PID: ${info.pid})`;
                         statusSpan.parentNode.insertBefore(timeSpan, statusSpan);
                    }
                } catch(e) { console.warn("Failed to get startup info:", e); }
            }
        }, 300);

    } catch (e) {
        console.error("CRITICAL: Application boot sequence failed:", e);
    }
});

/**
 * [TEST-SUITE] [DOM-PROBE]
 * Backend-triggered diagnostic that checks UI state and reports via Eel.
 */
/**
 * Sets the Global DB Scanning status and updates UI.
 */
function set_db_status(isActive) {
    console.log(`[DB] Scan status change: ${isActive}`);
    const scanBtn = document.getElementById('footer-scan-btn');
    if (scanBtn) {
        if (isActive) {
            scanBtn.classList.add('loading');
            scanBtn.innerHTML = `<svg class="spin" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> SCANNING...`;
            if (typeof showToast === 'function') showToast("Bibliotheks-Scan gestartet...", "info");
        } else {
            scanBtn.classList.remove('loading');
            scanBtn.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg> SCAN`;
            if (typeof showToast === 'function') showToast("Scan abgeschlossen!", "success");
            // Refresh counts
            if (typeof loadEditItems === 'function') loadEditItems();
        }
    }
}

if (typeof eel !== 'undefined') {
    eel.expose(set_db_status);
    eel.expose(run_frontend_probe);
}

function run_frontend_probe() {
    console.log("[DOM-PROBE] Starting automated UI check...");
    
    // 1. Check for rendered media
    const playlistItems = document.querySelectorAll('.implementation-encapsulated-state-buffer-node');
    const queueItems = document.querySelectorAll('#player-queue-pane .implementation-encapsulated-state-buffer-node');
    const mediaCount = Math.max(playlistItems.length, queueItems.length);
    
    if (typeof eel !== 'undefined' && typeof eel.report_items_spawned === 'function') {
        eel.report_items_spawned(mediaCount, "probe")();
    }

    // 2. Playback Check (If media exists)
    if (mediaCount > 0) {
        const firstItemNode = playlistItems[0] || queueItems[0];
        console.log("[DOM-PROBE] Attempting to trigger playback on first item...");
        if (firstItemNode) firstItemNode.click();
        
        // Wait a bit for playback to start, then report state
        setTimeout(() => {
            const pipeline = document.getElementById('native-html5-audio-pipeline-element');
            if (pipeline && typeof eel !== 'undefined' && typeof eel.report_playback_state === 'function') {
                const isPlaying = !pipeline.paused && pipeline.currentTime > 0;
                const itemName = pipeline.src.split('/').pop() || "unknown";
                eel.report_playback_state(isPlaying, itemName, pipeline.currentTime)();
            }
        }, 2000);
    }
}
