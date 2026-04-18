/**
 * playlists.js - Unified Media Queue & Playlist Management (v1.45.120)
 * Decoupled from app_core.js and audioplayer.js for modular forensic work.
 */

// --- Global Queue State (Single Source of Truth) ---
window.currentPlaylist = [];
window.playlistIndex = -1;
window.activeQueueFilter = 'all'; // [v1.46.019] Initialized for Forensic Workstation Parity

/**
 * [v1.46.024] Atomic Clear Strategy
 * Centrally clears all shared queue list containers to prevent multi-pulse overwriting.
 */
function clearQueueContainers() {
    const targets = [
        'playlist-content-render-target',
        'active-queue-list-render-target',
        'active-queue-list-render-target-legacy',
        'active-queue-list-render-target-warteschlange',
        'player-active-queue-list',
        'player-playlist-container'
    ];
    targets.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '';
    });
    console.debug("[Pulse] Shared queue containers cleared for sync pulse.");
}

/**
 * syncQueueWithLibrary (v1.45.120 Centralized)
 * Hydrates the global currentPlaylist from the localized library cache.
 * Branch-aware filtering is primarily handled by the backend, this stage
 * performs final capability mapping and UI notification.
 */
function syncQueueWithLibrary() {
    if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
        console.warn("[Sync] Library empty. Initiating Forensic Auto-Rescan...");
        
        // [v1.46.056] Non-destructive Auto-Sync
        if (typeof eel !== 'undefined' && typeof eel.scan_media === 'function') {
            eel.scan_media(null, false)();
        }
        
        return;
    }

    const hmode = window.__mwv_hydration_mode || 'both';
    console.warn(`[Sync] Hydrating Global Queue... Mode: ${hmode}, Items: ${allLibraryItems ? allLibraryItems.length : 0}`);

    if (!Array.isArray(allLibraryItems)) {
        console.error("[Sync] allLibraryItems is NOT an array. Aborting.");
        return;
    }

    // --- Stage 0: Atomic Pulse Initialization (v1.46.024) ---
    // Clear containers once at the start of the pulse to prevent overwriting bugs.
    clearQueueContainers();

    // Stage 1: Local Filter Pulse (Mock/Real/Both + Category + Branch)
    const activeFilter = window.activeQueueFilter || 'all';
    
    // [v1.46.024] Branch Governance
    const config = window.CONFIG || {};
    const lockAudio = config.force_queue_audio_branch === true;
    const lockMulti = config.force_queue_multimedia_branch === true;
    const lockExt   = config.force_queue_extended_branch === true;

    console.info(`[Sync-Pulse] Starting sync for ${allLibraryItems.length} raw library items. Filter: ${activeFilter} | Mode: ${hmode}`);

    let filtered = allLibraryItems.filter(item => {
        const config = window.CONFIG || window.GLOBAL_CONFIG || {};
        const qConfig = config.queue_orchestration || {};

        // 1.1 Hydration Mode Filter
        const nameMock = item.name && item.name.startsWith('[MOCK]');
        const mockFlag = (item.is_mock === true || item.is_mock === 1 || nameMock);
        
        let passMode = true;
        if (hmode === 'mock') passMode = (mockFlag || !!item.stage);
        else if (hmode === 'real') passMode = (!mockFlag && !item.stage);

        // IMPORTANT
        // Hybrid Sync: When hybrid_sync_enabled is True, the queue will prioritize real media while keeping forensic mock items visible, regardless of the active hydration mode (M/R).
        if (qConfig.hybrid_sync_enabled && !mockFlag && !item.stage) {
            passMode = true; // Real items ALWAYS pass in Hybrid mode
        }
        
        // [v1.46.040] BLOCK PROTECTION
        if (qConfig.block_real_in_diagnostic === false && !mockFlag) {
            passMode = true; // explicitly forbidden to block real items
        }

        if (!passMode) return false;

        // 1.2 Category/Type Filter (v1.46.025 Inclusive)
        let passFilter = true;
        if (activeFilter !== 'all') {
            const itemCat = (item.category || item.type || 'unknown').toLowerCase();
            const isAudio = isAudioItem(item);
            const isVideo = isVideoItem(item);
            const isPhoto = isPhotoItem(item);
            
            if (activeFilter === 'audio') passFilter = isAudio;
            else if (activeFilter === 'video') passFilter = isVideo;
            else if (activeFilter === 'pictures' || activeFilter === 'images') passFilter = isPhoto;
            else {
                passFilter = (itemCat === activeFilter.toLowerCase() || itemCat.startsWith(activeFilter.toLowerCase()));
            }
        }
        if (!passFilter) return false;

        // 1.3 Branch Governance (v1.46.024)
        if (lockAudio && !isAudioItem(item)) return false;
        if (lockMulti && (!isAudioItem(item) && !isVideoItem(item) && !isPhotoItem(item))) return false;

        return true;
    });

    // --- [v1.46.040] EMERGENCY BYPASS PULSE ---
    // IMPORTANT
    // Emergency Bypass: If filtering results in 0 items but the library has data, the system will automatically bypass all filters (Category/Branch/Mode) to prevent a "Black Screen" state.
    const qConfig = (window.CONFIG || window.GLOBAL_CONFIG || {}).queue_orchestration || {};
    if (filtered.length === 0 && allLibraryItems.length > 0 && qConfig.emergency_bypass_enabled) {
        console.warn("%c[Sync-Bypass] 0 items after filter. Forcing Emergency Bypass...", "background: #c0392b; color: white; padding: 2px 5px;");
        filtered = allLibraryItems.filter(item => {
            const nameMock = item.name && item.name.startsWith('[MOCK]');
            const isMock = (item.is_mock === true || item.is_mock === 1 || nameMock);
            return hmode === 'mock' ? isMock : !isMock;
        });
        
        if (typeof showToast === 'function') {
            showToast("⚠️ Filter-Notaus: Alle Filter umgangen (0 Treffer)", "warning", 3000);
        }
    }

    console.debug(`[Sync-Pulse] Filtration Complete: ${filtered.length} items remain. (Syncing SSOT)`);

    // Stage 2: Shared State Injection
    window.currentPlaylist = filtered;
    
    // [v1.46.024] Category Audit Trace
    const catStats = filtered.reduce((acc, item) => {
        const cat = item.category || 'unknown';
        acc[cat] = (acc[cat] || 0) + 1;
        return acc;
    }, {});
    console.info(`[Sync] Global Queue ready: ${filtered.length} items. Distribution:`, catStats);

    // Stage 3: Multi-Module UI Refresh Pulse
    try {
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof renderVideoQueue === 'function') renderVideoQueue();
        if (typeof renderPhotoQueue === 'function') renderPhotoQueue();
    } catch (err) {
        console.error("[Sync] UI Refresh Pulse failed:", err);
    }
    
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
            const config = window.CONFIG || window.GLOBAL_CONFIG || {};
            const autoHydrate = config.queue_orchestration?.auto_hydration_enabled !== false;

            if (window.currentPlaylist.length === 0 && typeof allLibraryItems !== 'undefined' && allLibraryItems.length > 0) {
                if (autoHydrate) {
                    console.warn("[Watcher] Queue is empty. Triggering automatic hydration...");
                    syncQueueWithLibrary();
                } else {
                    console.info("[Watcher] Queue is empty, but auto-hydration is DISABLED per config.");
                }
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

/**
 * [v1.46.12] Hook for UI sub-navigation 'Playlist' tab.
 */
function refreshSavedPlaylists() {
    console.info("[Playlist] Refreshing saved playlists...");
    const container = document.getElementById('player-playlist-grid');
    if (container) {
        container.innerHTML = '<div style="padding: 40px; color: var(--text-secondary); text-align: center; opacity: 0.5;">KEINE GESPEICHERTEN PLAYLISTS GEFUNDEN</div>';
        
        // FUTURE: Connect to backend playlist fetch here
        if (typeof eel !== 'undefined' && typeof eel.get_playlists === 'function') {
            eel.get_playlists()((results) => {
                if (results && results.length > 0) {
                     console.log(`[Playlist] Loaded ${results.length} playlists.`);
                     // Render logic...
                }
            });
        }
    }
}

window.refreshSavedPlaylists = refreshSavedPlaylists;

// Initialize Diagnostic Pulse
document.addEventListener('DOMContentLoaded', () => {
    startAtomicHydrationWatcher();
});
