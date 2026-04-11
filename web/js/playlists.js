/**
 * playlists.js - Unified Media Queue & Playlist Management (v1.45.120)
 * Decoupled from app_core.js and audioplayer.js for modular forensic work.
 */

// --- Global Queue State (Single Source of Truth) ---
window.currentPlaylist = [];
window.playlistIndex = -1;

/**
 * syncQueueWithLibrary (v1.45.120 Centralized)
 * Hydrates the global currentPlaylist from the localized library cache.
 * Branch-aware filtering is primarily handled by the backend, this stage
 * performs final capability mapping and UI notification.
 */
function syncQueueWithLibrary() {
    if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
        console.warn("[Sync] Library empty. Skipping queue hydration.");
        return;
    }

    const hmode = window.__mwv_hydration_mode || 'both';
    console.warn(`[Sync] Hydrating Global Queue... Mode: ${hmode}, Items: ${allLibraryItems.length}`);

    // Stage 1: Local Filter Pulse (Mock/Real/Both)
    // Branch-level filtering happened in the backend library fetch.
    let filtered = allLibraryItems.filter(item => {
        const nameMock = item.name && item.name.startsWith('[MOCK]');
        const mockFlag = (item.is_mock === true || item.is_mock === 1 || nameMock);
        
        if (hmode === 'mock') return mockFlag || !!item.stage;
        if (hmode === 'real') return !mockFlag && !item.stage;
        return true; // 'both'
    });

    // Stage 2: Shared State Injection
    window.currentPlaylist = filtered;
    
    console.info(`[Sync] Global Queue ready: ${window.currentPlaylist.length} items.`);

    // Stage 3: Multi-Module UI Refresh Pulse
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
    if (typeof renderVideoQueue === 'function') renderVideoQueue();
    
    // Stage 4: Centralized Technical Anchors
    if (typeof updateSyncAnchor === 'function') {
        const dbCount = (window.__mwv_all_library_items && window.__mwv_all_library_items.length > 0) 
                        ? window.__mwv_all_library_items.length 
                        : (window.__mwv_last_db_count || 0);
        const guiCount = filtered.length;
        updateSyncAnchor(dbCount, guiCount);
    }
}

/**
 * Manipulation Functions (Moved from audioplayer.js)
 */

function clearQueue() {
    console.warn(">>> [Queue] Clearing all items.");
    window.currentPlaylist = [];
    window.playlistIndex = -1;
    
    // Stop playback if something is playing
    const pipeline = document.getElementById('native-html5-audio-pipeline-element');
    if (pipeline) {
        pipeline.pause();
        pipeline.src = "";
    }
    
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
    if (typeof showToast === 'function') showToast("Queue geleert", 1500);
}

function addToQueue(idx) {
    if (typeof allLibraryItems !== 'undefined' && allLibraryItems[idx]) {
        window.currentPlaylist.push(allLibraryItems[idx]);
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof renderVideoQueue === 'function') renderVideoQueue();
        if (typeof showToast === 'function') showToast("Zur Warteschlange hinzugefügt", "success");
    }
}

function removeItem(index) {
    window.currentPlaylist.splice(index, 1);
    if (window.playlistIndex === index) window.playlistIndex = -1;
    else if (window.playlistIndex > index) window.playlistIndex--;
    
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
    if (typeof renderVideoQueue === 'function') renderVideoQueue();
}

function moveItemUp(index) {
    if (index <= 0) return;
    const playlist = window.currentPlaylist;
    [playlist[index], playlist[index - 1]] = [playlist[index - 1], playlist[index]];
    if (window.playlistIndex === index) window.playlistIndex--;
    else if (window.playlistIndex === index - 1) window.playlistIndex++;
    
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
}

function moveItemDown(index) {
    const playlist = window.currentPlaylist;
    if (index >= playlist.length - 1) return;
    [playlist[index], playlist[index + 1]] = [playlist[index + 1], playlist[index]];
    if (window.playlistIndex === index) window.playlistIndex++;
    else if (window.playlistIndex === index + 1) window.playlistIndex--;
    
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
}

/**
 * addAndPlayNow
 * Injects an item at the end and triggers playback.
 */
function addAndPlayNow(el, item) {
    if (typeof window.currentPlaylist !== 'undefined') {
        window.currentPlaylist.push(item);
        window.playlistIndex = window.currentPlaylist.length - 1;
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof playAudio === 'function') playAudio(item);
        if (typeof switchPlayerMainView === 'function') switchPlayerMainView('now-playing');
    }
}

/**
 * resetAllFilters
 * Diagnostic recovery pulse.
 */
function resetAllFilters() {
    console.warn(">>> [Recovery] resetAllFilters triggered.");
    window.activeQueueFilter = 'all';
    window.__mwv_raw_mode = false;
    
    const filterSelect = document.getElementById('queue-type-filter');
    if (filterSelect) filterSelect.value = 'all';
    
    syncQueueWithLibrary();
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
    if (typeof renderVideoQueue === 'function') renderVideoQueue();
    
    if (typeof showToast === 'function') showToast("Alle Filter zurückgesetzt & Sync erzwungen.", "success");
}

/**
 * startAtomicHydrationWatcher
 * Health audit loop for the unified global queue.
 */
function startAtomicHydrationWatcher() {
    console.info(">>> [Diagnostic] Starting Atomic Hydration Watcher...");
    setInterval(() => {
        try {
            if (window.currentPlaylist.length === 0 && typeof allLibraryItems !== 'undefined' && allLibraryItems.length > 0) {
                console.warn("[Watcher] Queue is empty. Triggering automatic hydration...");
                syncQueueWithLibrary();
            }

            const initialCount = window.currentPlaylist.length;
            window.currentPlaylist = window.currentPlaylist.filter(item => item && (item.path || item.id) && item.path !== 'undefined');
            
            if (window.currentPlaylist.length !== initialCount) {
                console.error(`[Watcher] Purged ${initialCount - window.currentPlaylist.length} zombie items from queue.`);
                if (typeof renderAudioQueue === 'function') renderAudioQueue();
            }

            const hubStatus = document.getElementById('hub-sync-status');
            if (hubStatus) {
                hubStatus.innerText = `Synced (${window.currentPlaylist.length} items)`;
            }
        } catch (e) {
            console.error("[Watcher] Hydration failure:", e);
        }
    }, 30000); // 30s heartbeat
}

// Global Exports
window.syncQueueWithLibrary = syncQueueWithLibrary;
window.clearQueue = clearQueue;
window.addToQueue = addToQueue;
window.removeItem = removeItem;
window.moveItemUp = moveItemUp;
window.moveItemDown = moveItemDown;
window.addAndPlayNow = addAndPlayNow;
window.resetAllFilters = resetAllFilters;
window.startAtomicHydrationWatcher = startAtomicHydrationWatcher;

// Initialize Diagnostic Pulse
document.addEventListener('DOMContentLoaded', () => {
    startAtomicHydrationWatcher();
});
