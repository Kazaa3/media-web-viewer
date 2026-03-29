/**
 * Media Viewer Core Orchestrator
 * Central entry point for cross-module coordination and global event handling.
 */

// --- Global Application State ---
let activeAudioPipeline = document.getElementById('native-html5-audio-pipeline-element');
let currentLogbuchEntries = [];
let currentPlaylist = []; // Shared across Audio/Video modules
let currentVideoItem = null;
let currentVideoPath = null;
let vjsPlayer = null;

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
    if (tabId === 'playlist' && typeof renderPlaylist === 'function') {
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
window.addEventListener('DOMContentLoaded', () => {
    console.log("Core Orchestrator: System checks passing.");
    
    // Initialize Library & Inventory
    if (typeof loadLibrary === 'function') loadLibrary();
    if (typeof loadEditItems === 'function') loadEditItems();
});
