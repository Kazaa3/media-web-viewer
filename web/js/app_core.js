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
    const tickInterval = window.CONFIG?.sleep_times?.watchdog_tick * 1000 || 500;
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

            const maxTicks = window.CONFIG?.boot_watchdog_max_ticks || 12;
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
    }, tickInterval);
}
// --- Heartbeat & Health Monitoring (v1.41.00) ---
let __mwv_heartbeat_timer = null;
function startHeartbeat() {
    if (typeof eel === 'undefined') return;
    console.log("[Health] Starting Heartbeat Service...");
    __mwv_heartbeat_timer = setInterval(async () => {
        try {
            await eel.heartbeat()();
        } catch (e) {
            console.warn("[Health] Heartbeat failed (Backend possibly busy/restarting)");
        }
    }, 5000); // 5s pulse
}

window.addEventListener('DOMContentLoaded', () => {
    try {
        startBootWatchdog();
        // Initialize Diagnostic Suite if available
        if (window.Diagnostics && typeof window.Diagnostics.init === 'function') {
            window.Diagnostics.init();
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

// --- Global Application State ---
let activeAudioPipeline = document.getElementById('native-html5-audio-pipeline-element');
// let currentLogbuchEntries = [];
let currentPlaylist = []; // Shared across Audio/Video modules
let currentVideoItem = null;
let currentVideoPath = null;
let vjsPlayer = null; // Defined as a shared global in Orchestrator

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
    
    const items = config.navigation_orchestrator.level_1;
    const activeCat = localStorage.getItem('mwv_active_category') || 'media';

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
window.triggerModuleHydration = async function(name) {
    console.info(`[HYDRATION] Triggering handshake for: ${name.toUpperCase()}`);
    
    // Normalize name
    const module = name.toLowerCase();

    try {
        switch(module) {
            case 'media':
            case 'player':
                if (typeof syncQueueWithLibrary === 'function') await syncQueueWithLibrary();
                if (window.AudioPlayer && typeof window.AudioPlayer.refresh === 'function') window.AudioPlayer.refresh();
                if (typeof window.hydrateCategoryDropdown === 'function') window.hydrateCategoryDropdown();
                break;
            case 'library':
                if (typeof loadLibrary === 'function') await loadLibrary();
                break;
            case 'edit':
            case 'editor':
                if (typeof loadEditItems === 'function') await loadEditItems();
                break;
            case 'status':
                if (window.Diagnostics && typeof window.Diagnostics.refresh === 'function') window.Diagnostics.refresh();
                break;
        }

        if (typeof mwv_trace === 'function') {
            mwv_trace('STABILITY', 'HYDRATION-COMPLETE', { module: module });
        }
    } catch (err) {
        console.error(`[HYDRATION] Critical Failure in ${module}:`, err);
    }
};

/**
 * hydrateCategoryDropdown (v1.45.100)
 * Populates the 'Category Map' dropdown from backend config.
 */
window.hydrateCategoryDropdown = function() {
    const select = document.getElementById('queue-type-filter');
    if (!select) return;

    const map = window.CONFIG?.ui_settings?.library_category_map;
    if (!map || !Array.isArray(map)) {
        console.warn("[HYDRATION] No library_category_map found in config.");
        return;
    }

    console.log(`[HYDRATION] Populating Category Map with ${map.length} entries.`);
    
    // Preserve existing selection if possible
    const currentVal = select.value;
    
    // Clear and Fill
    select.innerHTML = map.map(item => `
        <option value="${item.id}">${item.label}</option>
    `).join('');

    if (currentVal && select.querySelector(`option[value="${currentVal}"]`)) {
        select.value = currentVal;
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
    
    const isVideo = isVideoItem(item);
    if (isVideo) {
        console.info("[Play-Routing] Video detected, forcing switch to Video Player tab:", item.path);
        if (typeof switchTab === 'function') {
            switchTab('video', null, () => {
                 if (typeof playVideo === 'function') {
                     playVideo(item, item.path);
                 } else {
                     console.warn("[Play-Routing] Video fragment loaded, but playVideo() not found.");
                 }
            }, true); // v1.35.65 Force Jump
        }
    } else {
        console.info("[Play-Routing] Audio detected, switching to Audio Player tab:", item.path);
        addToQueue(item);
        if (typeof switchTab === 'function') {
            switchTab('player', null, () => {
                if (typeof playAudio === 'function') {
                    playAudio(item);
                }
            }, true); // v1.35.65 Force Jump
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
 * Application Boot Notification (v1.42 Evolution Path)
 */
window.addEventListener('DOMContentLoaded', async () => {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('BOOT-WATCHDOG', 'DOM-READY');
    
    // --- [v1.42] GLOBAL EVOLUTION CHECK ---
    try {
        if (typeof eel !== 'undefined' && typeof eel.get_global_config === 'function') {
            const config = await eel.get_global_config()();
            window.GLOBAL_CONFIG = config;
            
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
            FragmentLoader.load('svg-icons-placeholder', 'fragments/icons.html', () => onFragmentDone('icons'));
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
            if (typeof renderPlaylist === 'function') renderPlaylist(); 
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
window.showStartupDashboard = showStartupDashboard;
