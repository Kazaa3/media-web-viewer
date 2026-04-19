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
    const tickMs = window.CONFIG?.technical_orchestrator?.watchdog?.tick_ms || 500;
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

            const maxTicks = window.CONFIG?.technical_orchestrator?.watchdog?.max_ticks || 12;
            if (phase === 'DATA-READY' || __mwv_boot_watchdog_ticks > maxTicks) {
                if (typeof mwv_trace === 'function') mwv_trace('BOOT-WATCHDOG', 'SUCCESS', { ticks: __mwv_boot_watchdog_ticks });

                // --- [v1.41.132] Emergency Auto-Hydration Fallback ---
                if (phase !== 'DATA-READY' && (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0)) {
                    console.warn("[Watchdog] DATA-TIMEOUT: Initiating Forensic Auto-Hydration...");
                    if (window.MWV_Diagnostics && typeof window.MWV_Diagnostics.forceHydrationTest === 'function') {
                        window.MWV_Diagnostics.forceHydrationTest();
                        if (typeof showToast === 'function') showToast("SAFETY HYDRATION ACTIVE", 5000);
                    }
                }

                clearInterval(__mwv_boot_watchdog_timer);
                __mwv_boot_watchdog_status = 'DONE';
            }
        } catch (e) {
            console.error("[Watchdog] Diagnostic Crash:", e);
        }
    }, tickMs);
}
// --- Heartbeat & Health Monitoring (v1.41.00) ---
let __mwv_heartbeat_timer = null;
function startHeartbeat() {
    if (typeof eel === 'undefined') return;
    console.log("[Health] Starting Heartbeat Service...");
    const heartbeatMs = window.CONFIG?.technical_orchestrator?.intervals?.heartbeat_pulse_ms || 5000;
    __mwv_heartbeat_timer = setInterval(async () => {
        try {
            await eel.heartbeat()();
        } catch (e) {
            console.warn("[Health] Heartbeat failed (Backend possibly busy/restarting)");
        }
    }, heartbeatMs); // Dynamic pulse
}

window.addEventListener('DOMContentLoaded', () => {
    try {
        startBootWatchdog();
        // Initialize Diagnostic Suite (v1.46.017 Handshake)
        if (window.MWV_Diagnostics && typeof window.MWV_Diagnostics.init === 'function') {
            window.MWV_Diagnostics.init();
        }
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

// --- Global Application State (Consolidated v1.45.110) ---
let activeAudioPipeline = document.getElementById('native-html5-audio-pipeline-element');
let currentVideoItem = null;
let currentVideoPath = null;
let vjsPlayer = null; // Defined as a shared global in Orchestrator

// [v1.46.026] SSOT: Shared Playback State
window.currentPlaylist = window.currentPlaylist || [];
window.playlistIndex = window.playlistIndex || 0;

/**
 * [v1.53.005] Phase 13 Diagnostic Visualization
 * Resolves technical quality classification for UI markers.
 */
window.getBitrateQualityClass = function(bitrateStr) {
    if (!bitrateStr || bitrateStr === '-') return '';
    const val = parseInt(bitrateStr.replace(/[^0-9]/g, ''));
    if (isNaN(val)) return '';
    
    // Fetch thresholds from Global Config (v1.54.002 SSOT)
    const thresholds = window.CONFIG?.bitrate_thresholds || {
        high: 1000, standard: 320, low: 192
    };

    if (val >= thresholds.high) return 'quality-high'; // Lossless/High-Res
    if (val >= thresholds.standard) return 'quality-high';
    if (val >= thresholds.low) return 'quality-std';
    return 'quality-low';
};

window.triggerWorkstationUpdate = async function(force = false) {
    const btn = document.getElementById('footer-btn-UPDT');
    if (btn) btn.classList.add('loading');
    
    console.info("🚀 [Governance] Initiating Workstation Update Cycle...");
    try {
        const result = await eel.trigger_workstation_update(force)();
        if (result.status === "ok") {
            console.info("✅ [Governance] Workstation Update Successful.");
            if (typeof triggerAuditPulse === 'function') triggerAuditPulse();
        } else {
            console.error("❌ [Governance] Workstation Update Failed:", result.message);
        }
    } catch (e) {
        console.error("❌ [Governance] RPC Error during update:", e);
    } finally {
        if (btn) btn.classList.remove('loading');
    }
};

window.triggerAuditPulse = function() {
    const sidebar = document.querySelector('.sidebar-lane') || document.querySelector('.workstation-lane-sidebar');
    if (!sidebar) return;
    
    sidebar.classList.add('audit-pulse-active');
    setTimeout(() => {
        sidebar.classList.remove('audit-pulse-active');
    }, 2000); // Standard Forensic Pulse Duration
};

/**
 * syncUiGeometry (v1.43)
 * Injects dimensions from GLOBAL_CONFIG into CSS variables.
 */
function syncUiGeometry(config) {
    if (!config || !config.ui_settings) return;
    const settings = config.ui_settings;
    const root = document.documentElement;

    console.info("[GEOMETRY] Synchronizing UI Dimensions...");

    // Level 1: Header
    root.style.setProperty('--nav-header-height', (settings.header_height || 48) + 'px');

    // Level 2: Sub-Nav (Neck)
    root.style.setProperty('--nav-sub-height', (settings.sub_nav_height || 35) + 'px');

    // Level 3: Module Tabs (Sub-Menu)
    root.style.setProperty('--nav-module-height', (settings.sub_menu_height || 32) + 'px');

    // Global: Sidebar
    root.style.setProperty('--sidebar-width', (settings.sidebar_width || 250) + 'px');

    if (typeof mwv_trace === 'function') {
        mwv_trace('DOM-UI', 'GEOMETRY-SYNC', {
            h1: settings.header_height,
            h2: settings.sub_nav_height,
            wS: settings.sidebar_width
        });
    }
}

/**
 * renderMasterNav (v1.43)
 * Redners Level 1 Menu from GLOBAL_CONFIG.
 */
function renderMasterNav(config) {
    const navBar = document.getElementById('master-header-container')?.querySelector('.nav-cluster');
    if (!navBar || !config?.navigation_orchestrator?.level_1) return;

    console.info("[NAV] Rendering Dynamic Master Navigation...");

    let items = config.navigation_orchestrator.level_1;
    const activeBranch = config.active_branch || 'multimedia';
    const activeCat = localStorage.getItem('mwv_active_category') || 'media';

    // [v1.45.300] Filter navigation based on active branch branch identity
    if (activeBranch === 'audio') {
        items = items.filter(i => ['audio', 'status', 'tools'].includes(i.id));
    } else if (activeBranch === 'multimedia') {
        items = items.filter(i => ['audio', 'multimedia', 'status', 'tools'].includes(i.id));
    }

    navBar.innerHTML = items.map(item => `
        <button id="nav-btn-${item.id}" 
                class="menu-item-btn ${activeCat === item.id ? 'active' : ''}" 
                style="${item.color ? 'color: ' + item.color + ';' : ''}"
                onclick="switchMainCategory('${item.action}', this)">
            ${item.id === 'status' ? '<svg width="12" height="12" style="margin-right: 6px;"><use href="#icon-sparkles"></use></svg>' : ''}
            ${item.label}
        </button>
    `).join('');
}

/**
 * triggerModuleHydration (v1.45)
 * Ensures that after a fragment load, the module-specific 
 * data hydration pipeline is triggered immediately.
 */
window.triggerModuleHydration = async function (name) {
    console.info(`[HYDRATION] Triggering handshake for: ${name.toUpperCase()}`);

    // Normalize name
    const module = name.toLowerCase();

    try {
        switch (module) {
            case 'media':
            case 'player':
                if (typeof syncQueueWithLibrary === 'function') await syncQueueWithLibrary();
                if (window.AudioPlayer && typeof window.AudioPlayer.refresh === 'function') window.AudioPlayer.refresh();
                if (typeof window.hydrateCategoryDropdown === 'function') window.hydrateCategoryDropdown(module);
                break;
            case 'library':
                if (typeof loadLibrary === 'function') await loadLibrary();
                if (typeof window.hydrateCategoryDropdown === 'function') window.hydrateCategoryDropdown(module);
                break;
            case 'edit':
            case 'editor':
                if (typeof loadEditItems === 'function') await loadEditItems();
                break;
            case 'status':
                if (window.Diagnostics && typeof window.Diagnostics.refresh === 'function') window.Diagnostics.refresh();
                break;
            case 'database':
            case 'explorer':
                if (typeof window.hydrateCategoryDropdown === 'function') window.hydrateCategoryDropdown('database');
                break;
        }

        // [v1.45.200] INJECT LIVENESS MARKER
        const win = window.WindowManager ? window.WindowManager.windows.get(name) : null;
        if (win && win.fragmentId) {
            const container = document.getElementById(win.fragmentId);
            if (container && container.innerHTML.trim() !== "") {
                container.setAttribute('data-liveness', 'ready');
                console.info(`[HYDRATION] LIVENESS MARKER INJECTED: ${name.toUpperCase()}`);
            }
        }

        if (typeof mwv_trace === 'function') {
            mwv_trace('STABILITY', 'HYDRATION-COMPLETE', { module: module });
        }
    } catch (err) {
        console.error(`[HYDRATION] Critical Failure in ${module}:`, err);
    }
};

/**
 * hydrateCategoryDropdown (v1.45.115)
 * Populates the 'Category Map' dropdown from backend config 
 * based on the ARCHITECTURE of the active branch.
 */
window.hydrateCategoryDropdown = function (branchId) {
    const selects = [
        document.getElementById('queue-type-filter'),          // Header Mount
        document.getElementById('queue-type-filter-sidebar')  // Side Menu Mount
    ].filter(el => el !== null);

    if (selects.length === 0) return;

    const ui = window.CONFIG?.ui_settings;
    const allCategories = ui?.library_category_map;
    const supportMap = ui?.branch_architecture_registry;
    const modeRegistry = ui?.library_filter_mode_registry;
    const hierarchy = ui?.library_category_hierarchy;

    const currentMode = window.activeLibraryFilterMode || 'route';
    console.log(`[HYDRATION] Synchronizing ${selects.length} dropdown mounts. Mode: ${currentMode.toUpperCase()}`);

    // [v1.53.001] Synchronize Toggle Button Labels
    document.querySelectorAll('.lib-filter-mode-toggle-btn').forEach(btn => {
        btn.innerText = currentMode.toUpperCase();
        btn.classList.toggle('active', currentMode === 'category');
    });

    // 1. Resolve supported IDs for this branch
    let targetBranch = branchId.toLowerCase();
    if (targetBranch === 'player') targetBranch = 'media';
    if (targetBranch === 'explorer') targetBranch = 'database';

    let supportedIds = supportMap ? (supportMap[targetBranch] || supportMap[window.CONFIG?.branch_id] || null) : null;
    if (!supportedIds) supportedIds = supportMap ? supportMap["multimedia"] : null;

    if (!allCategories || !Array.isArray(allCategories)) {
        console.warn("[HYDRATION] No library_category_map found in config.");
        return;
    }

    // 2. Filter by Branch Architecture THEN by Mode Registry
    let filtered = supportedIds
        ? allCategories.filter(cat => supportedIds.includes(cat.id))
        : allCategories;

    if (modeRegistry && modeRegistry[currentMode]) {
        const modeIds = modeRegistry[currentMode];
        filtered = filtered.filter(cat => modeIds.includes(cat.id));
    }

    // 3. Apply Hierarchical Labels (↳)
    const processed = filtered.map(item => {
        let label = item.label;
        if (['category', 'objects'].includes(currentMode) && hierarchy) {
            for (const [parent, children] of Object.entries(hierarchy)) {
                if (children.includes(item.id)) {
                    label = `↳ ${label}`;
                    break;
                }
            }
        }
        return { ...item, displayLabel: label };
    });

    // 4. Render Options to all mounts
    const optionsHtml = processed.map(item => `
        <option value="${item.id}">${item.displayLabel}</option>
    `).join('');

    selects.forEach(select => {
         const lastVal = select.value;
         select.innerHTML = optionsHtml;
         
         // Preserve selection if possible
         if (lastVal && select.querySelector(`option[value="${lastVal}"]`)) {
             select.value = lastVal;
         }

         // [v1.46.019] Attach Filter Pulse Listener
         select.onchange = (e) => {
             const newFilter = e.target.value;
             window.activeQueueFilter = newFilter;
             
             // Synchronize other mount points
             selects.forEach(s => { if(s !== select) s.value = newFilter; });

             console.info(`[UI-NAV] Filter Change: ${newFilter}. Triggering Pulse...`);
             if (typeof setLibraryFilter === 'function') setLibraryFilter(newFilter);
    });
};


/**
 * [v1.53.003] toggleLibraryFilterMode
 * Switches the active filter lens between FIVE forensic modes globally: 
 * route, category, items, objects, context.
 */
window.activeLibraryFilterMode = window.activeLibraryFilterMode || 'route';
window.toggleLibraryFilterMode = function() {
    // [v1.54.013] Forensic 6-Mode discovery Cycle
    const modes = ['item', 'release', 'object', 'route', 'category', 'context'];
    let idx = modes.indexOf(window.activeLibraryFilterMode);
    idx = (idx + 1) % modes.length;
    window.activeLibraryFilterMode = modes[idx];
    
    console.info(`[UI-NAV] Filter Mode Toggled: ${window.activeLibraryFilterMode.toUpperCase()} (Cycle ${idx+1}/6)`);
    
    // [v1.53.004] Trigger Phase 13 Visual Feedback
    if (typeof window.triggerAuditPulse === 'function') window.triggerAuditPulse();
    
    if (typeof window.hydrateCategoryDropdown === 'function') {
        const branchId = window.CONFIG?.active_branch || 'media';
        window.hydrateCategoryDropdown(branchId);
    }
};

/**
 * [v1.53.001] handleLibrarySearch
 * Global bridge for the forensic discovery search.
 */
window.handleLibrarySearch = function(query) {
    console.info(`[UI-NAV] Global Search Pulse: "${query}"`);
    window.activeLibrarySearchQuery = query;
    if (typeof updateLibrarySearch === 'function') {
        updateLibrarySearch(query);
    } else if (typeof renderLibrary === 'function') {
        renderLibrary();
    }
};

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

    const activeTab = document.body.getAttribute('data-mwv-tab') || 'player';

    const isVideo = isVideoItem(item);
    const isAudio = !isVideo && isAudioItem(item);
    const isImage = !isVideo && !isAudio && isImageItem(item);

    // [v1.46.096] Forensic Routing Pulse (Expanded Logs)
    console.info(`[Play-Routing] Handshake: ${item.name} | Type: ${isVideo ? 'VIDEO' : (isAudio ? 'AUDIO' : (isImage ? 'IMAGE' : 'UNKNOWN'))} | Cat: ${item.category}`);

    if (isVideo) {
        console.group("[Play-Routing] Video Pipeline");
        console.info("Path:", item.path);
        
        // [v1.46.088] Adaptive routing: if already on video tab, fire immediately
        if (activeTab === 'video') {
            console.debug("Already on Video tab. Immediate fire.");
            if (typeof playVideo === 'function') {
                playVideo(item, item.path);
            }
            console.groupEnd();
            return;
        }

        if (typeof switchTab === 'function') {
            switchTab('video', null, () => {
                if (typeof playVideo === 'function') {
                    playVideo(item, item.path);
                } else {
                    console.warn("[Play-Routing] Video fragment loaded, but playVideo() not found.");
                }
                console.groupEnd();
            }, true); // v1.35.65 Force Jump
        }
    } else if (isAudio) {
        console.group("[Play-Routing] Audio Pipeline");
        console.info("Path:", item.path);
        
        // [v1.46.087] Non-blocking queue injection
        addToQueue(item, true); // silent=true
        
        // [v1.46.088] Adaptive routing: avoid destructive reload if already on player
        if (activeTab === 'player') {
            console.debug("Already on Player tab. Direct fire playback.");
            if (typeof playAudio === 'function') {
                playAudio(item);
            } else {
                console.error("[Play-Routing] Critical: playAudio() not found.");
            }
            console.groupEnd();
            return;
        }

        if (typeof switchTab === 'function') {
            switchTab('player', null, () => {
                console.debug("[Play-Routing] App Context Switched. Executing playAudio...");
                if (typeof playAudio === 'function') {
                    playAudio(item);
                } else {
                    console.error("[Play-Routing] Critical: playAudio() not found in Player context.");
                }
                console.groupEnd();
            }, true); // v1.35.65 Force Jump
        }
    } else if (isImage) {
        console.info("[Play-Routing] Image detected. Toggling Preview notification.", item.path);
        if (typeof showToast === 'function') showToast(`Bild-Vorschau: ${item.name}`, "info");
        // Images don't trigger tab switches usually in forensic mode, just a notification/HUD update
        if (typeof refreshForensicLeds === 'function') refreshForensicLeds();
    } else {
        console.warn("[Play-Routing] Unknown / Mixed media type. Fallback to standard player:", item.path);
        addToQueue(item, true);
        if (typeof switchTab === 'function') switchTab('player');
    }

    // [v1.46.026] Broadcast State to Backend SSOT
    if (typeof eel !== 'undefined' && typeof eel.sync_playback_state === 'function') {
        eel.sync_playback_state({
            queueCount: window.currentPlaylist ? window.currentPlaylist.length : 0,
            index: window.playlistIndex || 0,
            path: item.path
        })();
    }
}

/**
 * Adds an item to the global currentPlaylist.
 * @param {Object} item - The media item to add.
 * @param {Boolean} silent - If true, suppresses "Already in queue" toasts (v1.46.087).
 */
function addToQueue(item, silent = false) {
    if (!item) return;
    
    // Ensure initialization (v1.46.026 Fixed 'const' crash)
    if (!window.currentPlaylist) window.currentPlaylist = [];
    let currentPlaylist = window.currentPlaylist;

    console.debug(`[QUEUE-PULSE] Analysis: ${item.name} | Silent: ${silent}`);

    // Avoid duplicates in the active queue if desired
    const existingIndex = currentPlaylist.findIndex(i => i.path === item.path);
    if (existingIndex === -1) {
        currentPlaylist.push(item);
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (!silent && typeof showToast === 'function') showToast(t('pl_added_to_queue') || "Added to queue");
        
        // [v1.46.026] Broadcast State to Backend SSOT
        if (typeof eel !== 'undefined' && typeof eel.sync_playback_state === 'function') {
            eel.sync_playback_state({
                queueCount: currentPlaylist.length,
                index: window.playlistIndex || 0,
                path: item.path
            })();
        }
    } else {
        if (!silent) {
            if (typeof showToast === 'function') showToast(t('pl_already_in_queue') || "Already in queue", "info");
        }
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
    if ((tabId === 'playlist' || tabId === 'player') && typeof renderAudioQueue === 'function') {
        renderAudioQueue();
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
 * Application Boot Notification (v1.42 Evolution Path)
 */
window.addEventListener('DOMContentLoaded', async () => {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('BOOT-WATCHDOG', 'DOM-READY');

    // --- [v1.42] GLOBAL EVOLUTION CHECK ---
    try {
        if (typeof eel !== 'undefined' && typeof eel.get_global_config === 'function') {
            const config = await eel.get_global_config()();
            window.GLOBAL_CONFIG = config;
            window.CONFIG = config; // Ensure legacy/standard references are also updated (v1.45.310 Sync)

            // [v1.46.067] Dynamic Identity Sync: Remove hardcoded ghost versions
            if (config.version) {
                document.body.setAttribute('data-mwv-version', config.version);
                console.info(`[ORCHESTRATOR] System Identity Sync: ${config.version}`);
            }

            // [v1.43] MASTER GEOMETRY SYNC
            syncUiGeometry(config);

            // [v1.43] MASTER NAVIGATION RENDER
            renderMasterNav(config);

            if (config.ui_evolution_mode === 'rebuild') {
                console.warn(">>> [ORCHESTRATOR] EVOLUTION MODE: REBUILD ACTIVE <<<");
                if (typeof FragmentLoader !== 'undefined') {
                    // Level 1: Master Header Rebuild
                    FragmentLoader.load('master-header-container', 'fragments/rebuild/menu_l1.html', () => {
                        console.log("[NAV] Level 1 Stage Ready.");
                    });

                    // Level 2: Sub-Nav Neck Rebuild
                    FragmentLoader.load('sub-nav-container', 'fragments/rebuild/menu_l2.html', () => {
                        console.log("[NAV] Level 2 Stage Ready. Syncing default category...");
                        const activeCat = localStorage.getItem('mwv_active_category') || 'media';
                        if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav(activeCat);
                    });
                }
            }
        }
    } catch (e) {
        console.error("[ORCHESTRATOR] Evolution Handshake Failed:", e);
    }

    console.log("Core Orchestrator: System checks passing. Initializing UI fragments...");

    // [v1.54.012] EMERGENCY BOOT WATCHDOG: Force Hydration on Hang
    setTimeout(() => {
        const evolutionMode = window.CONFIG?.ui_evolution_mode || 'stable';
        const needsRebuild = evolutionMode === 'rebuild';
        
        if (!window.__PLAYER_INITIALIZED__) {
            console.warn(`!!! [WATCHDOG] Player hydration HANG detected (Mode: ${evolutionMode}). Forcing manual injection...`);
            
            // 1. Force state visibility
            if (typeof switchMainCategory === 'function') {
                switchMainCategory('media');
            }
            
            // 2. Force fragment load if in rebuild mode
            if (needsRebuild && typeof FragmentLoader !== 'undefined') {
                FragmentLoader.load('player-main-viewport', 'fragments/player_queue.html', () => {
                    window.__PLAYER_INITIALIZED__ = true;
                    if (typeof switchPlayerView === 'function') switchPlayerView('warteschlange');
                    console.info("[WATCHDOG] PLAYER HYDRATION RECOVERED.");
                });
            } else {
                // Legacy fallback (v1.35)
                window.__PLAYER_INITIALIZED__ = true;
                const container = document.getElementById('player-panel-container');
                if (container) container.style.display = 'block';
            }
        }
    }, 4500); // 4.5s Forensic Grace Period

    try {
        if (typeof mwv_trace_render === 'function') mwv_trace_render('BOOT-WATCHDOG', 'INIT-START');

        let fragmentsNeeded = 4;
        let fragmentsLoaded = 0;

        const onFragmentDone = (name) => {
            fragmentsLoaded++;
            if (typeof window.auditFragmentHydration === 'function') {
                window.auditFragmentHydration(name, 'success');
            }
            if (fragmentsLoaded === fragmentsNeeded) mwv_finalize_boot();
        };

        const bootStartTime = Date.now();
        if (typeof FragmentLoader?.load === 'function') {
            FragmentLoader.load('modals-placeholder', 'fragments/modals_container.html', () => onFragmentDone('modals-res'));
            FragmentLoader.load('svg-icons-placeholder', 'fragments/icons.html?v=' + Date.now(), () => onFragmentDone('icons'));
            FragmentLoader.load('context-menu-placeholder', 'fragments/context_menu.html', () => onFragmentDone('menus'));
            FragmentLoader.load('diagnostics-overlay-container', 'fragments/diagnostics_sidebar.html', () => onFragmentDone('diags'));
        } else {
            mwv_finalize_boot();
        }

        async function mwv_finalize_boot() {
            console.log("Orchestrator: Finalizing boot sequence...");

            // 1. Backend Handshake (Critical for Watchdog)
            if (typeof eel !== "undefined" && typeof eel.report_spawn === 'function') {
                eel.report_spawn()(() => console.log("DOM: Backend sync complete."));
            }

            // 2. Initialize Shared Helpers
            if (typeof initDomWatchdog === 'function') initDomWatchdog();
            if (typeof initTranslations === 'function') initTranslations();
            if (typeof initAllSplitters === 'function') initAllSplitters();

            // 3. UI Start State (v1.40 Orchestrated)
            const startTab = window.CONFIG?.start_tab || 'player';
            const startCategory = (startTab === 'library') ? 'library' :
                (startTab === 'database') ? 'database' :
                    (startTab === 'edit') ? 'edit' : 'media';

            console.log(`UI: Booting into tab: ${startTab} (Category: ${startCategory})`);

            if (window.MWV_UI) {
                window.MWV_UI.apply(startCategory);
            }

            const WM = window.WindowManager;
            if (WM && typeof WM.activate === 'function') {
                WM.activate(startTab);
            } else if (typeof switchTab === 'function') {
                switchTab(startTab);
            }

            // 4. Data Sync
            console.log("Data: Triggering library sync...");
            if (typeof loadLibrary === 'function') await loadLibrary();
            if (typeof loadEditItems === 'function') await loadEditItems();

            // Start stats polling
            if (window.StatsOverlay && typeof window.StatsOverlay.init === 'function') {
                setInterval(() => {
                    if (typeof window.StatsOverlay.updateStats === 'function') {
                        const activeTab = localStorage.getItem('mwv_active_tab');
                        if (activeTab === 'video' || window.StatsOverlay.isVisible) {
                            window.StatsOverlay.updateStats();
                        }
                    }
                }, 2000);
            }
            // 5. Start Services
            if (typeof startHeartbeat === 'function') startHeartbeat();
        }

        // 3. Fetch and Display Startup Info (Atomic Bridge v1.41.107)
        setTimeout(async () => {
            if (typeof eel !== 'undefined' && typeof eel.get_startup_info === 'function') {
                try {
                    const info = await eel.get_startup_info()();
                    if (info) {
                        const pidEl = document.getElementById('diag-pid');
                        const bootEl = document.getElementById('diag-boot');
                        const upEl = document.getElementById('diag-up');

                        if (pidEl) pidEl.innerText = info.pid;
                        if (bootEl) bootEl.innerText = `${info.boot_duration_sec}s`;
                        if (upEl && info.uptime_str) upEl.innerText = info.uptime_str;

                        console.log(`[HUD] Telemetry synchronized. Boot: ${info.boot_duration_sec}s`);
                    }
                } catch (e) { console.warn("Failed to get startup info:", e); }
            }
        }, 300);

    } catch (e) {
        console.error("CRITICAL: Application boot sequence failed:", e);
    }
});

/**
 * Atomic Shell Registry (v1.41.167)
 * Immediate execution to prevent race conditions during boot.
 */
(() => {
    if (typeof WindowManager === 'undefined') {
        console.warn("[BOOT-AUDIT] WindowManager NOT FOUND at immediate execution phase.");
        return;
    }

    console.info("[BOOT-AUDIT] WindowManager found. Beginning Forensic Registration...");
    const WM = WindowManager;

    const safeReg = (name, config) => {
        try {
            console.log(`[FORENSIC-REG] Registering: ${name.toUpperCase()}...`);
            WM.register(name, config);
        } catch (e) {
            console.error(`[FORENSIC-REG] CRITICAL FAILURE registering ${name}:`, e);
        }
    };

    safeReg('player', {
        shellId: 'player-panel-container',
        fragmentId: 'player-main-viewport',
        fragmentPath: 'fragments/player_queue.html',
        onActivate: () => {
            if (typeof switchPlayerView === 'function') switchPlayerView('warteschlange');
            if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
            if (typeof renderAudioQueue === 'function') renderAudioQueue();
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('media');
        }
    });
    safeReg('library', {
        shellId: 'library-panel-container',
        fragmentId: 'library-main-viewport',
        fragmentPath: 'fragments/library_explorer.html',
        onActivate: () => {
            if (typeof renderLibrary === 'function') renderLibrary();
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('library');
        }
    });
    safeReg('database', {
        shellId: 'database-panel-container',
        fragmentId: 'database-main-viewport',
        fragmentPath: 'fragments/database_panel.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('status');
        }
    });
    safeReg('edit', {
        shellId: 'edit-panel-container',
        fragmentId: 'edit-main-viewport',
        fragmentPath: 'fragments/metadata_editor.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('edit');
        }
    });
    safeReg('debug', {
        shellId: 'debug-panel-container',
        fragmentId: 'debug-main-viewport',
        fragmentPath: 'fragments/status_panel.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('status');
            if (typeof runUiIntegrityCheck === 'function') runUiIntegrityCheck();
        }
    });
    safeReg('tools', {
        shellId: 'tools-panel-container',
        fragmentId: 'tools-view-transcoding',
        fragmentPath: 'fragments/tools_panel.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('tools');
        }
    });
    safeReg('options', {
        shellId: 'system-panel-container',
        fragmentId: 'options-main-viewport',
        fragmentPath: 'fragments/options_panel.html',
        onActivate: () => {
            if (typeof switchOptionsView === 'function') switchOptionsView('general');
        }
    });
    safeReg('reporting', {
        shellId: 'reporting-dashboard-container',
        fragmentId: 'reporting-dashboard-container',
        fragmentPath: 'fragments/reporting_dashboard.html',
        onActivate: () => {
            if (typeof updateAnalyticsDashboard === 'function') updateAnalyticsDashboard();
        }
    });
    safeReg('logbuch', {
        shellId: 'logbook-tab-container',
        fragmentId: 'logbook-tab-container',
        fragmentPath: 'fragments/logbuch_panel.html',
        onActivate: () => {
            if (typeof loadLogbuchTab === 'function') loadLogbuchTab();
        }
    });
    safeReg('parser', {
        shellId: 'parser-panel-container',
        fragmentId: 'parser-main-viewport',
        fragmentPath: 'fragments/parser_panel.html',
        onActivate: () => {
            if (typeof loadParserConfig === 'function') loadParserConfig();
        }
    });
    safeReg('system', {
        shellId: 'system-panel-container',
        fragmentId: 'options-main-viewport',
        fragmentPath: 'fragments/options_panel.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('system');
        }
    });
    safeReg('video', {
        shellId: 'video-panel-container',
        fragmentId: 'video-main-viewport',
        fragmentPath: 'fragments/video_cinema.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('video');
        }
    });
    safeReg('tools', {
        shellId: 'tools-panel-container',
        fragmentId: 'tools-main-viewport',
        fragmentPath: 'fragments/tools_dashboard.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('tools');
        }
    });
    safeReg('logbuch', {
        shellId: 'logbook-tab-container',
        fragmentId: 'logbook-main-viewport',
        fragmentPath: 'fragments/logbook_view.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('logbuch');
        }
    });
    safeReg('tests', {
        shellId: 'tests-panel-container',
        fragmentId: 'tests-main-viewport',
        fragmentPath: 'fragments/test_sentinel.html',
        onActivate: () => {
            if (typeof updateGlobalSubNav === 'function') updateGlobalSubNav('tests');
        }
    });

    console.info(`[BOOT-AUDIT] Forensic Registration Complete.`);
})();

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

/**
 * [DIAGNOSTICS] Startup Performance Dashboard (v1.41.00)
 * Visualizes the bootstrap timeline and phase durations.
 */
async function showStartupDashboard() {
    if (typeof eel === 'undefined') return;
    try {
        const report = await eel.get_startup_report()();
        console.table(report.checkpoints);

        // Create modal overlay if it doesn't exist
        let modal = document.getElementById('startup-diag-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'startup-diag-modal';
            modal.className = 'modal-overlay';
            modal.style.display = 'flex';
            modal.innerHTML = `
                <div class="modal-container" style="max-width: 800px; max-height: 80vh; overflow-y: auto; background: #0a0a0f; color: #fff; border: 1px solid #1a1a2f; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
                    <div class="modal-header" style="border-bottom: 1px solid #1a1a2f; padding-bottom: 15px;">
                        <h2 style="margin:0; font-family: 'JetBrains Mono', monospace; font-size: 1.2rem; color: #00ffcc;">BOOTSTRAP PERFORMANCE ANALYTICS</h2>
                        <button onclick="document.getElementById('startup-diag-modal').remove()" style="background:none; border:none; color:#ff3366; font-size:1.5rem; cursor:pointer;">&times;</button>
                    </div>
                    <div class="modal-body" id="startup-diag-body" style="padding: 20px 0;">
                        <div style="font-family: monospace; font-size: 11px; color: #888; margin-bottom: 20px;">
                            VERSION: ${report.system_info.python} | PLATFORM: ${report.system_info.platform} | PID: ${report.system_info.pid}
                        </div>
                        <h3 style="font-size: 0.9rem; color: #aaa; margin-bottom: 15px; border-left: 3px solid #007aff; padding-left: 10px;">TOTAL BOOT: <span style="color: #fff;">${report.total_boot_sec}s</span></h3>
                        
                        <div id="startup-timeline" style="display: flex; flex-direction: column; gap: 8px;">
                            ${Object.entries(report.phases).map(([name, data]) => `
                                <div style="background: rgba(255,255,255,0.03); border-radius: 6px; padding: 10px; display: flex; justify-content: space-between; align-items: center; border: 1px solid rgba(255,255,255,0.05);">
                                    <div style="display: flex; flex-direction: column;">
                                        <span style="font-weight: 700; color: #eee; font-size: 12px;">${name}</span>
                                        <span style="font-size: 10px; color: #666;">Start: ${data.start.toFixed(2)}</span>
                                    </div>
                                    <div style="text-align: right;">
                                        <span style="font-family: 'JetBrains Mono', monospace; color: ${data.duration > 1.0 ? '#ff9500' : '#2ecc71'}; font-weight: 900;">${data.duration ? data.duration.toFixed(3) + 's' : 'Running...'}</span>
                                    </div>
                                </div>
                            `).join('')}
                        </div>

                        <h3 style="font-size: 0.9rem; color: #aaa; margin: 25px 0 15px; border-left: 3px solid #ff3366; padding-left: 10px;">CHECKPOINTS</h3>
                        <div style="font-family: monospace; font-size: 10px; color: #999; line-height: 1.6; background: rgba(0,0,0,0.3); padding: 15px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                            ${report.checkpoints.map(c => `
                                <div style="display: grid; grid-template-columns: 60px 1fr; gap: 10px; border-bottom: 1px solid rgba(255,255,255,0.02); padding: 4px 0;">
                                    <span style="color: #555;">${c.elapsed.toFixed(3)}s</span>
                                    <span>${c.msg} <span style="opacity: 0.3; font-size: 8px;">[${c.tag}]</span></span>
                                </div>
                            `).join('')}
                        </div>
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }
    } catch (e) {
        console.error("Failed to show startup dashboard:", e);
    }
}

// Map globally for sidebar access
/**
 * triggerModuleHydration (v1.45.100)
 * Mandatory bridge for the WindowManager to ensure data integrity during window swaps.
 */
async function triggerModuleHydration(name) {
    console.info(`[HYDRATION] Pulse triggered for module: ${name.toUpperCase()}`);
    
    // 1. Ensure Library is loaded if targeting data-heavy views
    if (['player', 'library', 'explorer'].includes(name)) {
        if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
            console.warn(`[HYDRATION] Library empty during ${name} activation. Forcing loadLibrary...`);
            if (typeof loadLibrary === 'function') {
                await loadLibrary();
            }
        }
    }

    // 2. Specific Module Sync
    if (name === 'player' || name === 'audioplayer') {
        if (typeof syncQueueWithLibrary === 'function') {
            await syncQueueWithLibrary();
        }
    } else if (name === 'library' || name === 'multimedia') {
        if (typeof renderLibrary === 'function') {
            renderLibrary();
        }
    }

    console.log(`[HYDRATION] Pulse complete for: ${name}`);
}

window.triggerModuleHydration = triggerModuleHydration;
window.showStartupDashboard = showStartupDashboard;

// Created with MWV v1.46.004-MASTER
