/**
 * UI Navigation & Tab Switching Helpers
 * Extracted from app.html to improve modularity and maintainability.
 */

// Global Navigation Actions Registry (v1.35)
window.mwv_init_actions = {
    'player': () => {
        const runInit = () => {
            if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
            if (typeof renderPlaylist === 'function') renderPlaylist();
            if (typeof switchPlayerView === 'function') switchPlayerView('warteschlange');
        };

        // Atomic Init: Wait for library if empty (v1.35 Hardened)
        if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
            if (typeof mwv_trace_render === 'function') mwv_trace_render('PLAYER-NAV', 'WAIT-FOR-LIB');
            document.addEventListener('mwv_library_ready', runInit, { once: true });
        } else {
            runInit();
        }
    },
    'playlist': () => { if (typeof renderPlaylist === 'function') renderPlaylist(); },
    'library': () => { if (typeof renderLibrary === 'function') renderLibrary(); },
    'video': () => { if (typeof renderVideoQueue === 'function') renderVideoQueue(); },
    'file': () => { if (typeof fbNavigate === 'function') fbNavigate(typeof fbCurrentPath !== 'undefined' ? fbCurrentPath : '/'); },
    'edit': () => { if (typeof initEdit === 'function') initEdit(); },
    'parser': () => { if (typeof loadParserConfig === 'function') loadParserConfig(); },
    'tools': () => { if (typeof renderToolsDashboard === 'function') renderToolsDashboard(); },
    'options': () => {
        if (typeof switchOptionsView === 'function') switchOptionsView('general');
        if (typeof loadDebugFlags === 'function') loadDebugFlags();
    },
    'database': () => { if (typeof renderDatabaseView === 'function') renderDatabaseView(); },
    'cinema': () => { if (typeof initCinemaView === 'function') initCinemaView(); },
    'debug': () => { toggleDiagnosticsSidebar(true); switchDiagnosticsSidebarTab('debug-db'); },
    'reporting': () => { if (typeof updateAnalyticsDashboard === 'function') updateAnalyticsDashboard(); },
    'logbuch': () => { if (typeof loadLogbuchTab === 'function') loadLogbuchTab(); },
    'tests': () => { toggleDiagnosticsSidebar(true); switchDiagnosticsSidebarTab('sentinel'); },
    'diagnostics': () => { toggleDiagnosticsSidebar(true); }
};

// Global state variables
let librarySubTab = 'coverflow';
let librarySubFilter = 'all';
let currentMainCategory = 'media';

window.__mwv_ui_nav_loaded = true;

let sidebarVisible = false; // [v1.37.52] Default to CLOSED for Elite Restoration
let diagnosticsSidebarVisible = false; 
let isNavigating = false;   // Global lock for tab switching
let navTimeout = null;      // Safety timer for lock release
let menuSystemVisible = true; // Default to open for UI discovery

// Global Diagnostics Orchestration (v1.37.10 Modular)
const DIAGNOSTICS_SIDEBAR_STORAGE_KEY = 'mwv_diag_overlay_visible';
const DIAGNOSTICS_VIEW_STORAGE_KEY = 'mwv_active_diag_view';

function syncGlobalDiagnosticsNav(viewId) {
    if (typeof window.switchDiagnosticsSidebarTab === 'function') {
        window.switchDiagnosticsSidebarTab(viewId);
    }
}

function applyDiagnosticsSidebarState(isVisible) {
    const sb = document.getElementById('global-diagnostics-sidebar');
    const footerBtn = document.getElementById('footer-btn-diag-overlay');
    const headerBtn = document.getElementById('header-btn-diag-overlay');
    
    // Check if we need to load the module first
    if (!sb && isVisible) {
        console.info("[UI-NAV] Diagnostics Sidebar missing, triggering modular load...");
        if (typeof FragmentLoader !== 'undefined') {
            FragmentLoader.load('diagnostics-overlay-container', 'fragments/diagnostics_sidebar.html', () => {
                if (typeof initDiagnosticsSidebar === 'function') initDiagnosticsSidebar();
                applyDiagnosticsSidebarState(true);
            });
        }
        return false; 
    }

    if (!sb) return false;

    diagnosticsSidebarVisible = !!isVisible;
    if (diagnosticsSidebarVisible) {
        sb.style.display = 'flex';
        // Small delay for animation trigger
        setTimeout(() => sb.classList.add('active'), 10);
    } else {
        sb.classList.remove('active');
        setTimeout(() => { if (!diagnosticsSidebarVisible) sb.style.display = 'none'; }, 400);
    }

    // Sync Buttons
    if (footerBtn) footerBtn.classList.toggle('active', diagnosticsSidebarVisible);
    if (headerBtn) headerBtn.classList.toggle('active', diagnosticsSidebarVisible);

    localStorage.setItem(DIAGNOSTICS_SIDEBAR_STORAGE_KEY, diagnosticsSidebarVisible);
    return diagnosticsSidebarVisible;
}

/**
 * Toggles the global diagnostics overlay sidebar.
 */
function toggleDiagnosticsSidebar(forceState = null) {
    const sb = document.getElementById('global-diagnostics-sidebar');
    const nextState = (typeof forceState === 'boolean') ? forceState : !diagnosticsSidebarVisible;

    if (!sb && nextState) {
        console.info("[UI-NAV] Loading Modular Diagnostics Overlay...");
        if (typeof FragmentLoader !== 'undefined') {
            FragmentLoader.load('diagnostics-overlay-container', 'fragments/diagnostics_sidebar.html', () => {
                if (typeof initDiagnosticsSidebar === 'function') initDiagnosticsSidebar();
                applyDiagnosticsSidebarState(true);
            });
        }
        return true;
    }

    const isActive = applyDiagnosticsSidebarState(nextState);
    if (typeof traceUiNav === 'function') traceUiNav('DIAG-OVERLAY', isActive ? 'OPEN' : 'CLOSE');
    return isActive;
}

function switchDiagnosticsSidebarTab(viewId, btn) {
    if (!diagnosticsSidebarVisible) applyDiagnosticsSidebarState(true);
    
    // Explicit Pane Management
    document.querySelectorAll('.diag-pane').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.side-reiter').forEach(el => el.classList.remove('active'));

    const targetId = `diag-pane-${viewId}`;
    const target = document.getElementById(targetId);
    if (target) {
        target.style.display = 'block';
        if (btn) btn.classList.add('active');
        else {
            const reiter = document.getElementById(`reiter-${viewId}`);
            if (reiter) reiter.classList.add('active');
        }
    }

    // Dynamic Logic
    if (viewId === 'hydration-audit') {
        renderHydrationMatrix();
    }
    if (viewId === 'config') {
        renderConfigToggles();
    }
    if (viewId === 'boot') {
        renderBootTimeline();
    }
}

/**
 * Toggles the new Elite Technical HUD (Floating PID Pills)
 */
function toggleTechnicalHUD(forceState = null) {
    const hud = document.getElementById('header-technical-hud');
    const btn = document.getElementById('header-btn-status');
    if (!hud) return;

    const isVisible = (typeof forceState === 'boolean') ? forceState : (hud.style.display === 'none');
    hud.style.display = isVisible ? 'flex' : 'none';
    
    if (btn) btn.classList.toggle('active', isVisible);
    
    if (isVisible && typeof refreshStartupInfo === 'function') {
        refreshStartupInfo(); // Immediate refresh on open
    }
}
window.toggleTechnicalHUD = toggleTechnicalHUD;

async function toggleDiagnosticsFlag(flagId) {
    switch (flagId) {
        case 'DIAG':
            if (typeof Diagnostics !== 'undefined' && typeof Diagnostics.toggle === 'function') {
                Diagnostics.toggle();
            }
            return;
        case 'NATV':
            if (typeof toggleForceNative === 'function') toggleForceNative();
            const natvState = localStorage.getItem('mwv_force_native') === 'true';
            window.__mwv_force_native = natvState;
            window.__mwv_natv_mode = natvState;
            if (typeof notifyDiagnosticChange === 'function') notifyDiagnosticChange(null, 'NATV', natvState);
            break;
        case 'HIDB':
            if (typeof toggleHideDb === 'function') toggleHideDb();
            const hidbState = localStorage.getItem('mwv_hide_db') === 'true';
            window.__mwv_hide_db = hidbState;
            if (typeof notifyDiagnosticChange === 'function') notifyDiagnosticChange(null, 'HIDB', hidbState);
            break;
        case 'RAW':
            if (typeof toggleRawMode === 'function') await toggleRawMode();
            break;
        case 'BYPS':
            if (typeof toggleBypassDb === 'function') toggleBypassDb();
            break;
        case 'AUDIT':
            applyDiagnosticsSidebarState(true);
            switchDiagnosticsSubView('health');
            if (typeof runAutonomousSelfTest === 'function') await runAutonomousSelfTest();
            break;
        case 'TEST':
            applyDiagnosticsSidebarState(true);
            switchDiagnosticsSubView('tests');
            if (typeof loadTestSuites === 'function') loadTestSuites();
            break;
        default:
            return;
    }

    if (typeof syncDiagBtnStates === 'function') syncDiagBtnStates();
}

/**
 * Toggles the main sidebar visibility.
 */
function toggleSidebar(forceState = null) {
    if (window.MWV_UI) {
        window.MWV_UI.toggleSidebar(forceState);
    } else {
        console.warn("[UI-NAV] MWV_UI not available for sidebar toggle.");
    }
}

/**
 * Applies the current sidebarVisible state to the DOM (v1.36.00 CSS-driven).
 */
function applySidebarState() {
    // Legacy stub - now handled by MWV_UI (v1.40)
    if (window.MWV_UI) {
        window.MWV_UI.updateGeometry();
    }
}

/**
 * Updates the default sidebar preference from Options.
 */
function updateSidebarDefault(enabled) {
    localStorage.setItem('mwv_sidebar_default_open', enabled);
    if (typeof showToast === 'function') showToast(`Default Sidebar: ${enabled ? 'Open' : 'Closed'}`, 'info');
}

/**
 * Initialize all application splitters.
 */
function initAllSplitters() {
    console.log("UI: Initializing splitters.");
    if (typeof initSplitter === 'function') {
        const splitters = [
            ['main-splitter', 'main-sidebar', 'main-split-container', 'vertical', 'left'],
            ['player-queue-splitter', 'player-deck-column', 'player-tab-split-container', 'vertical', 'left'],
            ['player-analytics-splitter', 'player-detailed-sidebar', 'player-main-viewport', 'vertical', 'left']
        ];

        splitters.forEach(params => {
            try {
                initSplitter(...params);
            } catch (e) {
                console.warn(`[Splitter] Failed to initialize ${params[0]}:`, e);
            }
        });
    }
}


/**
 * Traces UI navigation events to the backend log.
 */
function traceUiNav(category, target, details = {}) {
    const detailStr = (typeof details === 'string') ? details : JSON.stringify(details);
    const logMsg = `[JS-NAV] [${category}] ${target} ${detailStr !== '{}' ? detailStr : ''}`;
    console.log(logMsg);

    try {
        if (typeof eel !== 'undefined' && eel.log_ui_event) {
            eel.log_ui_event(category, target, detailStr)();
        }
    } catch (e) { }

    if (typeof appendUiTrace === 'function') {
        appendUiTrace(logMsg);
    }
}

/**
 * Switches between main application tabs.
 */
function switchTab(tabId, btn, callback, force = false) {
    if (isNavigating && !force) return;

    // [v1.41.108] DOM Observability Handshake
    document.body.setAttribute('data-mwv-tab', tabId);
    console.log(`[UI-NAV] Tab Switch: [${tabId}] (Reflected in DOM)`);

    if (typeof WM !== 'undefined' && typeof WM.activate === 'function') {
        // Redraw active button state immediately for responsiveness
        if (btn) {
            document.querySelectorAll('.menu-item-btn, .nav-item, .tab-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        }

        // Delegate to Forensic Window Manager
        WM.activate(tabId, force).then(success => {
            if (success && typeof callback === 'function') callback();
        });
    } else {
        console.warn("[NAV] WindowManager not available. Falling back to legacy switch logic.");
        // (Legacy fallback could go here if needed, but we expect WM to be present)
    }
}

/**
 * UI Navigation Helpers
 * Manages tab switching, sidebar visibility, and layout orchestration.
 */

// --- Global UI State ---

function finishSwitchTab(tabId, targetId, btn) {
    // --- Safety Release (v1.35 Hardening) ---
    isNavigating = false;
    document.body.style.cursor = 'default';

    document.querySelectorAll('.tab-content').forEach(el => {
        el.style.display = 'none';
        el.classList.remove('active');
    });

    const panel = document.getElementById(targetId);
    if (panel) {
        panel.classList.add('active');
        const isFlex = ['player', 'library', 'grid', 'details', 'album', 'item', 'file', 'edit', 'options', 'parser', 'debug', 'tests', 'reporting', 'logbuch', 'playlist', 'vlc', 'video', 'tools'].includes(tabId);
        panel.style.display = isFlex ? 'flex' : 'block';

        // Library Sub-Tab Shorthands
        if (['grid', 'details', 'album'].includes(tabId)) {
            if (typeof switchLibrarySubTab === 'function') switchLibrarySubTab(tabId);
        }

        if (isFlex) {
            panel.style.flex = '1';
            panel.style.height = '100%';
            panel.style.width = '100%';
            panel.style.minWidth = '0';
        }

        // Library Domain Handling
        if (tabId === 'library' && typeof switchLibraryDomain === 'function') {
            // Only default to visual if no other domain is active
            const currentDomain = document.querySelector('.lib-domain-content.active');
            if (!currentDomain) switchLibraryDomain('visual');
        }
        if (tabId === 'file' && typeof switchLibraryDomain === 'function') {
            switchTab('library');
            // switchTab will call finishSwitchTab('library') again, 
            // so we need to make sure we don't loop or get overwritten.
            // The check above 'if(!currentDomain)' handles this.
            setTimeout(() => switchLibraryDomain('browse'), 50);
            return;
        }
        if (tabId === 'item' && typeof switchLibraryDomain === 'function') {
            switchTab('library');
            setTimeout(() => switchLibraryDomain('inventory'), 50);
            return;
        }

        // --- Global Sidebar Management (v1.37.06 Refactoring) ---
        // Sidebar visibility is now globally governed by sidebarVisible state,
        // no longer forced to display: none per-tab switch.
        applySidebarState();
    }

    // Update button states (Sidebar & Header)
    document.querySelectorAll('.tab-btn, .nav-btn, .nav-item, .sub-tab-btn').forEach(b => b.classList.remove('active'));

    if (btn) {
        btn.classList.add('active');
    } else {
        // Fallback: Find button by ID or onclick content
        const sidebarBtn = document.querySelector(`.nav-item[onclick*="'${tabId}'"]`);
        if (sidebarBtn) {
            sidebarBtn.classList.add('active');
        } else {
            const fallbackBtn = document.querySelector(`.nav-btn[onclick*="${tabId}"], .tab-btn[onclick*="${tabId}"], .sub-tab-btn[onclick*="${tabId}"]`);
            if (fallbackBtn) fallbackBtn.classList.add('active');
        }
    }

    localStorage.setItem('mwv_active_tab', tabId);

    // Context-specific actions (V1.35 Hardened Registry)
    try {
        const tabInit = window.mwv_init_actions[tabId];
        if (tabInit) {
            if (typeof mwv_trace_render === 'function') mwv_trace_render('NAV-INIT', 'EXECUTE', { tabId });
            tabInit();
            if (typeof mwv_trace_render === 'function') mwv_trace_render('NAV-INIT', 'SUCCESS', { tabId });
        } else {
            if (typeof mwv_trace_render === 'function') mwv_trace_render('NAV-INIT', 'NO-ACTION', { tabId });
        }
    } catch (err) {
        if (typeof log_js_error === 'function') log_js_error(err, `INIT-ACTION:${tabId}`);
        if (typeof mwv_trace_render === 'function') mwv_trace_render('NAV-INIT', 'FAIL', { tabId, error: err.message });
    }

    if (navTimeout) {
        clearTimeout(navTimeout);
        navTimeout = null;
    }
    isNavigating = false;
    document.body.style.cursor = 'default';
    console.info(`[NAV] Tab Switch SUCCESS: ${tabId}`);
}

/**
 * Toggles the top-level program menu bar.
 */
/**
 * Toggle the left settings sidebar inside the Tools/Options panel.
 * No-op when the sidebar element doesn't exist (other tabs).
 */
function toggleOptionsSidebar() {
    const sidebar = document.getElementById('parser-left-settings');
    if (!sidebar) return; // Only active in old tools panel layout

    const isHidden = sidebar.style.display === 'none';
    sidebar.style.display = isHidden ? '' : 'none';

    // Also hide/show the splitter
    const splitter = document.getElementById('parser-tab-splitter');
    if (splitter) splitter.style.display = isHidden ? '' : 'none';

    // Toggle button highlight
    const btn = document.getElementById('btn-sidebar-toggle');
    if (btn) btn.style.opacity = isHidden ? '0.7' : '1';

    localStorage.setItem('mwv_options_sidebar_visible', isHidden ? 'true' : 'false');
}

/**
 * UI Header Management: TOP MENU and SUB-MENU Bar (v1.37 Restoration)
 * These elements provide global control and contextual navigation.
 */
window.toggleZenMode = function(forceState = null) {
    const header = document.getElementById('master-header');
    if (!header) return;

    // Use forceState if provided, otherwise toggle
    const isNowHidden = (forceState !== null) ? forceState : !header.classList.contains('zen-mode-active');
    
    if (isNowHidden) {
        header.classList.add('zen-mode-active');
        header.style.display = 'none';
        header.setAttribute('data-manual-zen', 'true');
    } else {
        header.classList.remove('zen-mode-active');
        header.style.display = 'flex';
        header.removeAttribute('data-manual-zen');
    }
    
    console.log(`[UI] ZEN MODE: ${isNowHidden ? 'ACTIVE' : 'INACTIVE'}`);
    refreshViewportLayout();
};

window.toggleSubNav = function(forceState = null) {
    const pillNav = document.getElementById('contextual-pill-nav');
    if (!pillNav) return;

    const isNowHidden = (forceState !== null) ? forceState : !pillNav.classList.contains('pill-nav-hidden');

    if (isNowHidden) {
        pillNav.classList.add('pill-nav-hidden');
        pillNav.style.display = 'none';
        pillNav.setAttribute('data-manual-hide', 'true');
    } else {
        pillNav.classList.remove('pill-nav-hidden');
        pillNav.style.display = 'flex';
        pillNav.removeAttribute('data-manual-hide');
    }
    
    console.log(`[UI] SUB-NAV: ${isNowHidden ? 'HIDDEN' : 'VISIBLE'}`);
    refreshViewportLayout();
};

/**
 * Legacy Support: UI Header Management (v1.37 Restoration)
 */
function toggleMenuBar(forceState = null) {
    toggleZenMode(forceState);
    toggleSubNav(forceState);
}

/**
 * Refreshes the visibility of all global UI navigation components
 * based on the current active category and the UI Visibility Matrix.
 * (v1.41.104 Consolidated Orchestrator)
 */
async function refreshUIVisibility(categoryOverride = null) {
    console.time('[PERF] UI-Refresh');
    const category = categoryOverride || currentMainCategory || localStorage.getItem('mwv_active_category') || 'media';
    
    // 1. Trigger Orchestrator Matrix
    if (window.MWV_UI) {
        window.MWV_UI.apply(category);
    }

    // 2. Force Sub-Nav Population (v1.41.104 Critical Sync)
    updateGlobalSubNav(category);

    console.timeEnd('[PERF] UI-Refresh');
}
window.refreshUIVisibility = refreshUIVisibility;

/**
 * Dynamically updates CSS variables to adjust viewport height/top based on visible bars.
 * v1.37.52 Master Engine: Handles 0, 40, 32, or 72px total offset.
 */
function refreshViewportLayout() {
    if (window.MWV_UI) {
        window.MWV_UI.updateGeometry();
    }
}

/**
 * Recalculates and applies layout offsets for the main content area.
 * Ensures vertical alignment is maintained when header bars are toggled.
 */
function updateLayoutOffsets() {
    console.debug("[GEO-ENGINE] Delegating offsets to MWV_UI...");
    if (window.MWV_UI) window.MWV_UI.updateGeometry();
}

// --- Keyboard Shortcuts & Global Early Initialization ---
document.addEventListener('keydown', (e) => {
    // [v1.41.119/120] Forensic UI Toggles
    if (e.altKey && !e.shiftKey && !e.ctrlKey) {
        const key = e.key.toLowerCase();
        
        switch(key) {
            case 'h': // Alt+H: Toggle Header
                e.preventDefault();
                if (window.MWV_UI) window.MWV_UI.toggleHeader();
                break;
            case 'n': // Alt+N: Toggle Sub-Nav
                e.preventDefault();
                if (window.MWV_UI) window.MWV_UI.toggleSubNav();
                break;
            case 'm': // Alt+M: Toggle Module Tabs
                e.preventDefault();
                if (window.MWV_UI) window.MWV_UI.toggleModuleTabs();
                break;
            case 'f': // Alt+F: Toggle Footer
                e.preventDefault();
                if (window.MWV_UI) window.MWV_UI.toggleFooter();
                break;
            case 'r': // Alt+R: Toggle Header Right (System Cluster)
                e.preventDefault();
                if (window.MWV_UI) window.MWV_UI.toggleHeaderRight();
                break;
            case 's': // Alt+S: Toggle Sidebar
                e.preventDefault();
                if (window.MWV_UI) window.MWV_UI.toggleSidebar();
                break;
            case 'alt': // Simple Alt: Toggle legacy menu logic
                break;
        }
    }
});

/**
 * Switch Audio Player Sub-Views (Warteschlange, Mediengalerie, Visualizer)
 */
function switchPlayerView(viewId) {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('NAV-RELAY', 'PLAYER-VIEW', { viewId });

    // [v1.41.117] Persist active view state
    localStorage.setItem('mwv_active_player_view', viewId);

    // Hide all views
    document.querySelectorAll('.player-view-container').forEach(el => {
        el.style.display = 'none';
        el.classList.remove('active');
    });

    // Show target view
    const target = document.getElementById(`player-view-${viewId}`);
    if (target) {
        target.style.display = 'flex';
        target.classList.add('active');

        // Sync with sub-nav buttons
        document.querySelectorAll('.player-sub-nav-btn').forEach(btn => {
            btn.classList.remove('active');
            if (btn.dataset.target === viewId || (btn.getAttribute('onclick') || '').includes(viewId)) {
                btn.classList.add('active');
            }
        });

        // Trigger logic based on view
        if (viewId === 'warteschlange' && typeof renderPlaylist === 'function') renderPlaylist();
        if (viewId === 'visualizer' && typeof initVisualizer === 'function') initVisualizer();
        if (viewId === 'playlist' && typeof refreshSavedPlaylists === 'function') refreshSavedPlaylists();

        if (typeof mwv_trace_render === 'function') mwv_trace_render('NAV-RELAY', 'SUCCESS', { viewId });
    } else {
        if (typeof log_js_error === 'function') log_js_error(new Error(`View Target Missing: ${viewId}`), 'NAV-RELAY');
    }
}

// Restore menu state on load
document.addEventListener('DOMContentLoaded', () => {
    // Initial UI Setup handled by MWV_UI (v1.40)
    
    window.__mwv_force_native = localStorage.getItem('mwv_force_native') === 'true';
    diagnosticsSidebarVisible = localStorage.getItem(DIAGNOSTICS_SIDEBAR_STORAGE_KEY) === 'true';
    applyDiagnosticsSidebarState(diagnosticsSidebarVisible);
    syncGlobalDiagnosticsNav(localStorage.getItem(DIAGNOSTICS_VIEW_STORAGE_KEY) || 'debug-db');

    // Load static UI fragments (v1.35.65)
    if (typeof FragmentLoader !== 'undefined') {
        FragmentLoader.load('svg-icons-placeholder', 'fragments/icons.html');
        FragmentLoader.load('context-menu-placeholder', 'fragments/context_menu.html');
        FragmentLoader.load('dom-auditor-container', 'fragments/dom_auditor.html');
    }

    // Ensure library items are synced to player queue on startup
    setTimeout(() => {
        if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
    }, 1500);
});

/**
 * Technical Sidebar Orchestrator (v1.35.98)
 * Switches between 'Details' and 'Diagnostics' views within the player-detailed-sidebar.
 */
function switchSidebarView(viewId) {
    console.log(`[UI-NAV] Switching Sidebar View to ${viewId}`);
    
    // Toggle View Visibility
    document.querySelectorAll('.sidebar-view-content').forEach(el => {
        el.style.display = (el.id === `sidebar-view-${viewId}`) ? 'block' : 'none';
    });

    // Toggle Reiter (Tab) Active state
    document.querySelectorAll('.side-reiter').forEach(el => {
        el.classList.toggle('active', el.id === `reiter-${viewId}`);
    });
    
    // If switching to diagnostics, ensure sync button states are refreshed
    if (viewId === 'diagnostics' && typeof syncDiagBtnStates === 'function') {
        syncDiagBtnStates();
    }
}

window.switchSidebarView = switchSidebarView;
window.switchMainCategory = switchMainCategory;

/**
 * Switch top-level category and populate sub-navigation.
 */
function switchMainCategory(category, btn) {
    if (!category) return;

    // [v1.41.108] DOM Observability Handshake
    document.body.setAttribute('data-mwv-category', category);
    console.log(`[UI-NAV] Category Switch: [${category}] (Reflected in DOM)`);

    currentMainCategory = category;
    console.log(`UI: Main category changed to ${category}`);
    if (typeof traceUiNav === 'function') traceUiNav('CATEGORY-SWITCH', category);
    currentMainCategory = category;
    localStorage.setItem('mwv_active_category', category);

    traceUiNav('NAV-CATEGORY', category);
    mwv_trace('DOM-UI', 'NAV-CATEGORY', category);

    // [v1.41.01] Sync with central UI Orchestration Engine
    if (window.MWV_UI) {
        window.MWV_UI.apply(category);
    }
    
    // [v1.41.112] Force Pill Refresh for Legacy Shell
    if (typeof updateGlobalSubNav === 'function') {
        updateGlobalSubNav(category);
    }

    // [v1.41.114] Layout Orchestration: Full Bleed for Media
    const splitView = document.getElementById('main-split-container');
    if (splitView) {
        if (category === 'media') splitView.classList.add('shell-full-bleed');
        else splitView.classList.remove('shell-full-bleed');
    }

    // Update active state in header/sidebar
    document.querySelectorAll('.menu-item-btn, .nav-item').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    else {
        const headerBtn = document.querySelector(`.menu-item-btn[onclick*="'${category}'"]`);
        if (headerBtn) headerBtn.classList.add('active');
    }

    // Update status indicator
    const label = document.getElementById('current-category-label');
    if (label) label.innerText = category.toUpperCase();

    // Default tab mapping for categories
    const categoryDefaults = {
        'media': 'player',
        'library': 'library',
        'playlist': 'playlist',
        'video': 'video',
        'tools': 'tools',
        'logbuch': 'logbuch',
        'system': 'options',
        'diagnostics': 'debug',
        'status': 'debug',
        'edit': 'edit',
        'reporting': 'reporting',
        'debug': 'debug',
        'tests': 'tests',
        'file': 'file',
        'parser': 'parser'
    };

    if (categoryDefaults[category]) {
        switchTab(categoryDefaults[category], btn);
    }

    // Dynamically populate sub-navigation header pills (Atomic Engine v1.41.112 Hard-Trigger)
    updateGlobalSubNav(category);
    
    // [v1.41.112] Special Visibility Pass: Force-show the target panel (v1.41.115 Robust Lookup)
    let targetPanel = document.getElementById(`${category}-panel-container`);
    if (!targetPanel) {
        targetPanel = document.querySelector(`.tab-content[data-tab-domain="${category}"]`);
    }

    if (targetPanel) {
        console.log(`[DOM-UI] Forcing visibility for panel: ${category} (Found: ${targetPanel.id})`);
        document.querySelectorAll('.tab-content').forEach(p => p.style.display = 'none');
        targetPanel.style.display = 'flex';
        targetPanel.style.opacity = '1';
    }

    // [v1.37.06] Centralized Visibility Refresh
    refreshUIVisibility();
}

/**
 * Updates the global sub-navigation bar with contextual entries.
 * (v1.41.105 SSOT-REBORN: Registry is now fetched from Python backend).
 */
function updateGlobalSubNav(category) {
    const container = document.getElementById('sub-nav-container');
    if (!container) return;

    // [v1.37.06] Forensic category normalization
    let normalizedCategory = category || currentMainCategory || localStorage.getItem('mwv_active_category') || 'media';
    normalizedCategory = normalizedCategory.toLowerCase();
    
    console.log(`[UI-NAV] Population request for category: [${normalizedCategory}] (passed: ${category})`);

    // [v1.41.101] Alias Resolution
    const registryKey = SUB_NAV_ALIASES[normalizedCategory] || normalizedCategory;
    const entries = SUB_NAV_REGISTRY[registryKey];
    if (!entries) {
        console.warn(`[UI-NAV] No entry map for ${normalizedCategory}.`);
        console.log(`[UI-NAV] UNSPAWN: Sub-nav cleared for ${normalizedCategory}.`);
        return;
    }

    // [v1.37.29 Restoration] Track active pill state
    const activeSubTab = localStorage.getItem('mwv_active_player_view') || 
                        localStorage.getItem('mwv_active_library_subtab') || 
                        'warteschlange';

    // Render logic with explicit lifecycle markers
    console.info(`[MWV-UI] Populating Sub-Nav for: ${normalizedCategory} | Pills: ${entries.length}`);
    const prevContent = container.innerHTML;
    const newContent = entries.map(item => `
        <button id="sub-nav-pill-${item.id}" 
                class="sub-pill-btn ${activeSubTab === item.id ? 'active' : ''}" 
                onclick="${item.action}"
                title="${item.label}">
            ${item.label}
        </button>
    `).join('');

    if (newContent) {
        container.innerHTML = newContent;
    }

    if (container.innerHTML !== prevContent) {
        console.log(`[UI-NAV] STATE_CHANGE: Sub-Nav content updated for ${normalizedCategory}.`);
        console.log(`[UI-NAV] SPAWN_SUCCESS: Successfully spawned ${entries.length} pills for ${normalizedCategory}.`);
    } else {
        // Log even if content is identical during refresh pass
        console.log(`[UI-NAV] REFRESH_SUCCESS: Sub-Nav state verified for ${normalizedCategory}.`);
    }

    // Recalibrate layout after content changes might have triggered visibility shifts
    refreshViewportLayout();

    mwv_trace('DOM-UI', 'SUB-NAV-SPAWN', { category: normalizedCategory, count: entries.length });

    const mainBar = document.getElementById('program-menu-bar');
    if (menuSystemVisible && mainBar && mainBar.style.display === 'none') {
        toggleMenuBar(true);
    }

    if (typeof updateLayoutOffsets === 'function') updateLayoutOffsets();

    // Set initial active state based on category default
    const activeTab = localStorage.getItem('mwv_active_tab');
    if (typeof updateSubNavActiveState === 'function') updateSubNavActiveState(activeTab);
}

function switchMediaSubView(tabId) {
    if (tabId === 'audioplayer' || tabId === 'visualizer' || tabId === 'warteschlange' || tabId === 'mediengalerie') {
        switchTab('player', null, () => {
            if (typeof switchPlayerMainView === 'function') {
                switchPlayerMainView(tabId);
            }
            updateSubNavActiveState(tabId);
        });
    } else {
        switchTab(tabId);
        updateSubNavActiveState(tabId === 'video' ? 'video-cinema' : tabId);
    }
}

function switchReportingSubView(viewId) {
    switchTab('reporting', null, () => {
        if (typeof switchReportingView === 'function') {
            switchReportingView(viewId);
        }
        updateSubNavActiveState(viewId);
    });
}

function switchDiagnosticsSubView(viewId) {
    // Advanced Mapping for Global Sidebar (v1.37.08 - Hydration & Item Track)
    if (viewId === 'hydration' || viewId === 'item-track') {
        applyDiagnosticsSidebarState(true);
        
        // Toggle Panes
        const hydrationPane = document.getElementById('diag-pane-hydration');
        const itemTrackPane = document.getElementById('diag-pane-item-track');
        
        if (hydrationPane) hydrationPane.style.display = (viewId === 'hydration') ? 'block' : 'none';
        if (itemTrackPane) itemTrackPane.style.display = (viewId === 'item-track') ? 'block' : 'none';
        
        // Initialize view
        if (viewId === 'hydration' && typeof renderLogicAuditSummary === 'function') {
            renderLogicAuditSummary();
        }
        if (viewId === 'item-track' && typeof renderItemTrackTab === 'function') {
            renderItemTrackTab();
        }
        
        // Update tab buttons (in case called from elsewhere)
        document.querySelectorAll('#global-diagnostics-sidebar .side-reiter').forEach(el => {
            el.classList.toggle('active', el.id === 'reiter-' + viewId);
            if (el.classList.contains('active')) {
                el.style.background = 'rgba(255,51,102,0.2)';
                el.style.color = 'white';
            } else {
                el.style.background = 'transparent';
                el.style.color = 'rgba(255,255,255,0.5)';
            }
        });
        
        return;
    }

    if (viewId === 'logs') {
        syncGlobalDiagnosticsNav(viewId);
        applyDiagnosticsSidebarState(true);
        switchMainCategory('logbuch');
        return;
    }
    if (viewId === 'recovery') {
        syncGlobalDiagnosticsNav(viewId);
        applyDiagnosticsSidebarState(true);
        switchTab('options', null, () => {
             if (typeof switchOptionsView === 'function') switchOptionsView('recovery');
        });
        return;
    }

    // Both 'debug' and 'tests' load diagnostics_suite.html
    const masterTab = (viewId === 'debug-db' || viewId === 'debug' || viewId === 'health' || viewId === 'latency' || viewId === 'video-health') ? 'debug' : 'tests';
    switchTab(masterTab, null, () => {
        if (typeof switchDiagnosticsView === 'function') {
            switchDiagnosticsView(viewId);
        }
        updateSubNavActiveState(viewId);
        syncGlobalDiagnosticsNav(viewId);
    });
}

window.applyDiagnosticsSidebarState = applyDiagnosticsSidebarState;
window.toggleDiagnosticsSidebar = toggleDiagnosticsSidebar;
window.toggleDiagnosticsOverlay = toggleDiagnosticsOverlay;
window.switchDiagnosticsSidebarTab = switchDiagnosticsSidebarTab;
window.toggleDiagnosticsFlag = toggleDiagnosticsFlag;
window.syncGlobalDiagnosticsNav = syncGlobalDiagnosticsNav;

function switchEditSubView(viewId) {
    switchTab('edit', null, () => {
        if (typeof switchEditView === 'function') {
            switchEditView(viewId);
        }
        updateSubNavActiveState(viewId);
    });
}

function switchLibrarySubView(viewId) {
    switchTab('library', null, () => {
        if (typeof switchLibraryDomain === 'function') {
            switchLibraryDomain(viewId);
        }
        updateSubNavActiveState(viewId);
    });
}

function switchToolsSubView(viewId) {
    switchTab('tools', null, () => {
        if (typeof switchToolsView === 'function') {
            switchToolsView(viewId);
        }
        updateSubNavActiveState(viewId);
    });
}

// Logbook sub-view logic moved to logbook_helpers.js (v1.41.00 Consolidation)

function switchFileSubView(viewId) {
    switchTab('file', null, () => {
        // Handle specific logic for Browser sub-views (Local, Network, etc.)
        if (typeof fbNavigate === 'function') {
            const paths = { 'local': './media', 'network': '/mnt', 'mounted': '/media' };
            fbNavigate(paths[viewId] || './media');
        }
        updateSubNavActiveState(viewId);
    });
}

/**
 * Toggles sub-views within the Logbook category.
 */
// Redundant window.switchLogbookSubView removed to resolve conflict with logbook_helpers.js

function switchParserView(viewId) {
    switchTab('parser', null, () => {
        // Parser logic from legacy tools panel
        document.querySelectorAll('.parser-view').forEach(el => el.style.display = 'none');
        const target = document.getElementById('parser-' + viewId + '-view');
        if (target) target.style.display = 'block';
        updateSubNavActiveState(viewId);
    });
}

/**
 * Updates the active class on sub-nav pill buttons.
 */
function updateSubNavActiveState(activeId) {
    document.querySelectorAll('.sub-pill-btn').forEach(btn => {
        const matches = btn.id === `global-sub-nav-${activeId}`
            || btn.id.endsWith(`-${activeId}`)
            || (activeId === 'video' && btn.id.endsWith('-video-cinema'));
        btn.classList.toggle('active', matches);
    });
}

/**
 * Switches between sub-views in the Options (System) category.
 */
function switchOptionsView(viewId) {
    const target = document.getElementById('options-' + viewId + '-view');
    if (target) {
        target.style.display = 'block';
        const btn = document.getElementById('opt-subtab-' + viewId) || document.querySelector(`.options-subtab[onclick*="'${viewId}'"]`);
        if (btn) btn.classList.add('active');
    }
}

/**
 * Switches between sub-tabs in the Library panel.
 */
function switchLibrarySubTab(tabId) {
    traceUiNav('SUBTAB-LIB', tabId);
    librarySubTab = tabId;
    localStorage.setItem('mwv_library_sub_tab', tabId);

    document.querySelectorAll('#coverflow-library-panel button.options-subtab, #lib-nav-views-container .options-subtab').forEach(btn => btn.classList.remove('active'));
    const btn = document.getElementById(`lib-tab-btn-${tabId}`);
    if (btn) btn.classList.add('active');

    document.querySelectorAll('.library-sub-content').forEach(view => view.style.display = 'none');
    const view = document.getElementById(`lib-view-${tabId}`);
    if (view) view.style.display = 'block';

    if (typeof renderLibrary === 'function') renderLibrary();
}

/**
 * Switches between views in the Tools panel.
 */
function switchToolsView(viewId) {
    traceUiNav('SUBTAB-TOOLS', viewId);
    document.querySelectorAll('.tools-view').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.tools-nav-tabs .options-subtab').forEach(el => el.classList.remove('active'));

    const target = document.getElementById('tools-' + viewId + '-view');
    if (target) {
        target.style.display = 'block';
        const btn = document.getElementById('tools-subtab-' + viewId);
        if (btn) btn.classList.add('active');
    }
}

/**
 * Switches between Edit/Metadata sub-tabs.
 */
function switchEditView(viewId) {
    traceUiNav('SUBTAB-EDIT', viewId);
    document.querySelectorAll('.edit-view').forEach(el => el.style.display = 'none');
    document.querySelectorAll('#edit-main-content-pane .options-subtab').forEach(el => el.classList.remove('active'));

    const target = document.getElementById('edit-' + viewId + '-view');
    if (target) {
        target.style.display = 'block';
        const btn = document.getElementById('edit-subtab-' + viewId);
        if (btn) btn.classList.add('active');
    }

    if (viewId === 'ffprobe') {
        const currentItem = document.getElementById('edit-item-name')?.value || '';
        const ffprobeContent = document.getElementById('edit-ffprobe-content');
        if (currentItem && ffprobeContent && ffprobeContent.innerText.includes('Führe Media Analyse aus')) {
            ffprobeContent.innerText = 'Analysiere ' + currentItem + '...';
            if (typeof eel !== 'undefined') {
                eel.analyze_media_item(currentItem)(function (res) {
                    try {
                        if (res && res.ffprobe) {
                            ffprobeContent.innerText = JSON.stringify(res.ffprobe, null, 2);
                        } else {
                            ffprobeContent.innerText = "Keine FFprobe Daten verfügbar.\n" + JSON.stringify(res, null, 2);
                        }
                    } catch (e) {
                        ffprobeContent.innerText = "Fehler: " + e;
                    }
                });
            }
        }
    }
}

/**
 * Switches between Test sub-tabs.
 */
function switchTestView(view) {
    traceUiNav('SUBTAB-TESTS', view);
    document.querySelectorAll('#quality-assurance-regression-suite-panel .test-view-content').forEach(el => {
        el.style.display = 'none';
    });
    document.querySelectorAll('#quality-assurance-regression-suite-panel .options-subtab').forEach(el => {
        el.classList.remove('active');
    });

    const targetView = document.getElementById(`test-${view}-view`);
    if (targetView) targetView.style.display = 'block';

    const btn = document.querySelector(`#quality-assurance-regression-suite-panel .options-subtab[data-view="${view}"]`);
    if (btn) btn.classList.add('active');

    if ((view === 'scripts' || view === 'suite' || view === 'routing') && typeof loadTestSuites === 'function') {
        loadTestSuites();
    }
}

/**
 * Switches between sub-tabs in the Tools/Parser panel.
 */
function switchParserView(viewId) {
    traceUiNav('SUBTAB-PARSER', viewId);
    document.querySelectorAll('.parser-view').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.options-subtab').forEach(el => {
        if (el.id && el.id.startsWith('parser-subtab-')) {
            el.classList.remove('active');
        }
    });

    const target = document.getElementById('parser-' + viewId + '-view');
    if (target) {
        target.style.display = 'block';
        const btn = document.getElementById('parser-subtab-' + viewId);
        if (btn) btn.classList.add('active');
    }
}

/**
 * Global progress bar update from Eel.
 */
if (typeof eel !== 'undefined' && eel.expose) {
    try {
        eel.expose(update_progress);
    } catch (e) {
        console.warn('[Eel] update_progress already exposed or failed.');
    }
}

function update_progress(data) {
    const bar = document.getElementById('app-progress-bar');
    const container = document.getElementById('app-progress-bar-container');
    const text = document.getElementById('app-progress-text');

    if (container) container.style.display = 'block';
    if (text) {
        text.style.display = 'block';
        text.innerText = (data.task || 'Lade') + '...';
    }
    if (bar) {
        bar.style.width = (data.percent || 0) + '%';
        if (data.status === 'complete') {
            setTimeout(() => {
                if (container) container.style.display = 'none';
                if (text) text.style.display = 'none';
                bar.style.width = '0%';
            }, 1000);
            bar.style.background = '#2ecc71';
        } else if (data.status === 'error') {
            bar.style.background = '#e74c3c';
        } else {
            bar.style.background = '#2ecc71';
        }
    }
}

/**
 * Utility to identify if a media error is due to an unsupported codec in the browser.
 */
function isUnsupportedMediaError(reason) {
    if (!reason) return false;
    const msg = String(reason).toLowerCase();
    return msg.includes('not supported') || msg.includes('format') || msg.includes('missing');
}

/**
 * Toggles the top program menu bar.
 */
function toggleMenuBar() {
    const bar = document.getElementById('program-menu-bar');
    if (!bar) return;
    menuBarVisible = !menuBarVisible;
    bar.style.display = menuBarVisible ? 'flex' : 'none';

    // Add margin to header if bar is visible to prevent overlap
    const header = document.querySelector('.header-container');
    if (header) header.style.marginTop = menuBarVisible ? '32px' : '0';
}

/**
 * Maps menu clicks to the main category switcher.
 */
function showMainCategory(cat) {
    const btn = document.querySelector(`.tab-btn[data-category="${cat}"]`);
    if (typeof switchMainCategory === 'function') {
        switchMainCategory(cat, btn);
    }
    // Auto-hide menu bar after selection for a cleaner feel
    toggleMenuBar();
}

// Listen for Alt key to toggle menu
window.addEventListener('keydown', (e) => {
    if (e.key === 'Alt') {
        e.preventDefault();
        toggleMenuBar();
    }
});

/**
 * Core Tab Switching Logic.
 */
let contextMenuItem = null;

function hideContextMenu() {
    const menu = document.getElementById('custom-context-menu');
    if (menu) menu.style.display = 'none';
}

async function handleContextMenuAction(mode) {
    if (!contextMenuItem) return;
    const item = contextMenuItem;

    // Hide context menu on switch
    hideContextMenu();

    if (mode === 'resume') {
        const pos = item.playback_position || 0;
        if (typeof isVideoItem === 'function' && isVideoItem(item)) {
            if (typeof playVideo === 'function') await playVideo(item, item.path, pos);
            switchTab('video');
        } else if (typeof playAudio === 'function') {
            playAudio(item, pos);
            switchTab('player');
        }
        return;
    }

    if (mode === 'audio_direct' && typeof playAudio === 'function') {
        playAudio(item);
        switchTab('player');
        return;
    }

    if ((mode === 'vlc_embedded' || mode === 'vlc_interactive') && typeof eel.open_video === 'function') {
        if (typeof showToast === 'function') showToast('Starte VLC HLS zu MSE...', 2000);
        const res = await eel.open_video(item.path, 'vlc', 'vlc_embedded')();
        if (res && res.status === 'play') {
            if (typeof startEmbeddedVideo === 'function') startEmbeddedVideo(item, res.path, 0, res.type);
            if (res.control_port) window._vlc_control_port = res.control_port;
            switchTab('video');
        } else if (typeof showToast === 'function') {
            showToast(res.error || "VLC Error");
        }
        return;
    }

    if (typeof eel.open_video === 'function') {
        const res = await eel.open_video(item.path, 'auto', mode)();
        if (res && res.status === 'play') {
            const embeddedModes = ['mediamtx', 'mediamtx_webrtc', 'chrome_native', 'chrome_direct', 'chrome_hls', 'chrome_fragmp4', 'ffmpeg_browser', 'chrome_remux', 'chrome_transcode', 'transcode'];
            if (embeddedModes.includes(res.mode) || embeddedModes.includes(mode)) {
                if (typeof startEmbeddedVideo === 'function') startEmbeddedVideo(item, res.path, 0, res.type);
                switchTab('video');
            }
        } else if (res && res.status === 'error' && typeof showToast === 'function') {
            showToast(res.error);
        }
    }
}

// VLC Interactive Remote Bridge
document.addEventListener('keydown', async (e) => {
    if (!window._vlc_control_port) return;
    const activeTab = localStorage.getItem('mwv_active_tab');
    if (activeTab !== 'video') return;

    // let vjsPlayer = null;
    let vlcKey = null;
    switch (e.key) {
        case 'ArrowUp': vlcKey = 'key-up'; break;
        case 'ArrowDown': vlcKey = 'key-down'; break;
        case 'ArrowLeft': vlcKey = 'key-left'; break;
        case 'ArrowRight': vlcKey = 'key-right'; break;
        case 'Enter': vlcKey = 'key-enter'; break;
        case 'Escape': vlcKey = 'key-nav-activate'; break;
    }

    if (vlcKey && typeof eel.vlc_remote_control === 'function') {
        eel.vlc_remote_control(window._vlc_control_port, vlcKey)();
    }
});


/**
 * Toggles the Impressum (Imprint) modal.
 */
function toggleImpressum() {
    console.log("UI: Toggling Impressum.");
    const modal = document.getElementById('impressum-modal');
    if (modal) {
        modal.style.display = (modal.style.display === 'none' || modal.style.display === '') ? 'flex' : 'none';
    } else {
        console.warn("[UI] impressum-modal element not found. Ensure fragment is loaded.");
    }
}

// Window listeners for menu dismissal
window.addEventListener('click', () => hideContextMenu());
window.addEventListener('scroll', () => hideContextMenu(), true);

/**
 * Global UI Initialization for v1.37 Restoration (Professional Logic)
 */
window.addEventListener('DOMContentLoaded', async () => {
    // [v1.37.29 Restoration] Sub-Nav Mutation Guard (Prevents accidental wiping)
    const pillNav = document.getElementById('sub-nav-container');
    if (pillNav) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.type === 'childList' && pillNav.innerHTML.trim() === '') {
                    console.warn("[UI-FIX] Sub-nav cleared unexpectedly! Re-hydrating...");
                    updateGlobalSubNav(currentMainCategory || 'media');
                }
            });
        });
        observer.observe(pillNav, { childList: true });
    }

    // --- [v1.41.12] SUB-NAV HEALTH GUARDIAN ---
    // Every 3 seconds, we ensure the sub-nav isn't empty if the category is active.
    setInterval(() => {
        const body = document.body;
        const pillNav = document.getElementById('sub-nav-container');
        const isHidden = body.classList.contains('mwv-hide-subnav');
        
        if (!isHidden && pillNav && pillNav.children.length === 0) {
            console.warn("[UI-GUARDIAN] Sub-nav is empty but visible. Forcing Re-hydration...");
            updateGlobalSubNav(currentMainCategory || 'media');
        }
    }, 3000);

// ==========================================
// FRAGMENT HYDRATION AUDITOR (v1.37.46)
// ==========================================

const FRAGMENT_HYDRATION_REGISTRY = {
    'modals': { id: 'diagnostics-overlay-container', path: 'fragments/diagnostics_sidebar.html', status: 'pending', time: 0 },
    'modals-res': { id: 'modals-placeholder', path: 'fragments/modals_container.html', status: 'pending', time: 0 },
    'player-tabs': { id: 'player-sub-nav-shell', path: 'app.html (inline)', status: 'pending', time: 0 },
    'player-engine': { id: 'player-main-viewport', path: 'fragments/player_queue.html', status: 'pending', time: 0 },
    'player-sidebar': { id: 'player-detailed-sidebar', path: 'app.html (inline)', status: 'pending', time: 0 },
    'player-view-lyrics': { id: 'player-view-lyrics', path: 'fragments/player_queue.html', status: 'pending', time: 0 },
    'library': { id: 'library-main-viewport', path: 'fragments/library_explorer.html', status: 'pending', time: 0 },
    'database': { id: 'database-panel-container', path: 'fragments/database_panel.html', status: 'pending', time: 0 },
    'editor': { id: 'metadata-writer-crud-panel', path: 'fragments/metadata_editor.html', status: 'pending', time: 0 },
    'icons': { id: 'svg-icons-placeholder', path: 'fragments/icons.html', status: 'pending', time: 0 },
    'menus': { id: 'context-menu-placeholder', path: 'fragments/context_menu.html', status: 'pending', time: 0 }
};

window.auditFragmentHydration = function(name, status, details = '') {
    const entry = FRAGMENT_HYDRATION_REGISTRY[name];
    if (!entry) {
        // Dynamic registration for unknown fragments
        if (status === 'spawn') {
            FRAGMENT_HYDRATION_REGISTRY[name] = { id: 'unknown', path: details, status: 'loading', time: Date.now() };
        } else return;
    }

    const item = FRAGMENT_HYDRATION_REGISTRY[name];
    item.status = status;
    if (status === 'success') {
        item.time = Date.now();
        console.info(`[HYD-AUDIT] Fragment '${name}' CONFIRMED.`);
    }

    // Log to Forensic Hub
    const logEl = document.getElementById('hydration-audit-logs');
    if (logEl) {
        const timestamp = new Date().toLocaleTimeString();
        const msg = `<div style="margin-bottom:2px;"><span style="opacity:0.4;">[${timestamp}]</span> <span style="color:${status === 'success' ? '#2ecc71' : (status === 'error' ? '#ff3366' : '#ff9500')}">${name.toUpperCase()}</span>: ${status.toUpperCase()} ${details}</div>`;
        logEl.innerHTML = msg + logEl.innerHTML;
        if (logEl.children.length > 50) logEl.lastElementChild.remove();
    }

    renderHydrationMatrix();
};

/**
 * [v1.41.104 Sync] Legacy point removed to prevent Cross-Effect collision.
 */

window.toggleProbeFlow = function() {
    if (!window.CONFIG || !window.CONFIG.ui_settings) return;
    
    // Toggle the value
    window.CONFIG.ui_settings.probe_data_flow_enabled = !window.CONFIG.ui_settings.probe_data_flow_enabled;
    const isActive = window.CONFIG.ui_settings.probe_data_flow_enabled;
    
    // Update UI button
    const btn = document.getElementById('footer-btn-probe-flow');
    if (btn) {
        btn.classList.toggle('active', isActive);
        btn.style.borderColor = isActive ? '#00f2ff' : '';
        btn.style.color = isActive ? '#00f2ff' : '';
    }

    console.log(`[FORENSIC] PROBE DATA FLOW: ${isActive ? 'ENABLED (Handshake)' : 'DISABLED (Direct)'}`);
    
    // Refresh Audit Panel if open
    if (typeof refreshForensicAudit === 'function') refreshForensicAudit();
};

/**
 * Initializes the Forensic 7++ State on Boot
 */
window.initForensicUI = function() {
    const config = (window.CONFIG && window.CONFIG.ui_settings) ? window.CONFIG.ui_settings : {};
    
    // 1. Apply Elite HUD if enabled
    if (config.elite_hud_enabled) {
        document.body.classList.add('forensic-elite');
        console.log("[FORENSIC] ELITE HUD: INITIALIZED");
    }

    // 2. Apply Global Forensic Lockdown
    const forensicsAllowed = (typeof config.forensics_enabled !== 'undefined') ? config.forensics_enabled : true;
    if (!forensicsAllowed) {
        console.log("[FORENSIC] LOCKDOWN: Hiding technical interfaces.");
        const techControls = document.getElementById('footer-technical-controls');
        if (techControls) techControls.style.display = 'none';
        
        const pulsarIcon = document.getElementById('footer-pulsar-icon');
        if (pulsarIcon) pulsarIcon.style.display = 'none';
    }

    // 3. Initial Sync
    const probeBtn = document.getElementById('footer-btn-probe-flow');
    if (probeBtn && config.probe_data_flow_enabled) {
        probeBtn.classList.add('active');
        probeBtn.style.borderColor = '#00f2ff';
        probeBtn.style.color = '#00f2ff';
    }
};

// Auto-Init on load
window.addEventListener('load', () => {
    setTimeout(window.initForensicUI, 500);
});

window.renderHydrationMatrix = function() {
    const matrix = document.getElementById('hydration-fragment-matrix');
    const summary = document.getElementById('hydration-audit-summary');
    const counter = document.getElementById('hydration-audit-counter');
    if (!matrix) return;

    let successCount = 0;
    const entries = Object.entries(FRAGMENT_HYDRATION_REGISTRY);

    matrix.innerHTML = entries.map(([name, data]) => {
        let color = '#444'; // Pending
        if (data.status === 'loading') color = '#ff9500';
        if (data.status === 'success') {
            color = '#2ecc71';
            successCount++;
        }
        if (data.status === 'error') color = '#ff3366';

        return `
            <div style="display: flex; align-items: center; gap: 10px; background: rgba(255,255,255,0.03); padding: 8px 12px; border-radius: 8px; border-left: 3px solid ${color};">
                <div style="width: 8px; height: 8px; border-radius: 50%; background: ${color}; box-shadow: 0 0 5px ${color};"></div>
                <div style="flex: 1;">
                    <div style="font-size: 10px; font-weight: 800; color: #fff;">${name.toUpperCase()}</div>
                    <div style="font-size: 8px; opacity: 0.5;">${data.path}</div>
                </div>
                <div style="font-size: 9px; font-family: 'JetBrains Mono', monospace; color: ${color}; font-weight: 900;">${data.status.toUpperCase()}</div>
            </div>
        `;
    }).join('');

    if (summary) {
        if (successCount === entries.length) {
            summary.innerText = "SYSTEM HYDRATED";
            summary.style.color = "#2ecc71";
        } else {
            summary.innerText = "HYDRATION IN PROGRESS...";
            summary.style.color = "#ff9500";
        }
    }

    if (counter) {
        counter.innerText = `Progress: ${successCount} / ${entries.length} Ready`;
    }
};

    // 1. Sync Base State
    const savedCategory = localStorage.getItem('mwv_active_category') || 'media';
    currentMainCategory = savedCategory;

    // 2. Initial Visibility Refresh (Immediate Fallback)
    refreshUIVisibility();
    
    // [v1.37.06] Hard-Force Sub-menu for Player on start
    if (currentMainCategory === 'media') {
        console.log("[UI-INIT] Hard-injecting Player sub-menu pills...");
        updateGlobalSubNav('media');
        // [v1.37.29 Restoration] Delayed check to ensure fragment loading didn't wipe us
        setTimeout(() => {
            if (pillNav && pillNav.innerHTML.trim() === '') {
                console.warn("[UI-INIT-HOTFIX] Sub-nav detected empty after boot, re-injecting.");
                updateGlobalSubNav('media');
            }
        }, 800);
    }

    // 3. Wait for Backend sync (v1.37.06 Hardening)
    if (typeof eel !== 'undefined') {
        try {
            await refreshUIVisibility();
            console.log("[UI-INIT] Backend Sync Complete.");
        } catch (e) {
            console.warn("[UI-INIT] Backend not ready yet, using static defaults.");
        }
    }

    // 4. Restore Menu System visibility
    const savedMenuState = localStorage.getItem('mwv_menu_system_visible');
    if (savedMenuState !== null) {
        menuSystemVisible = (savedMenuState === 'true');
    }

    // Apply initial visibility (Hardened Persistence)
    if (typeof toggleMenuBar === 'function') {
        toggleMenuBar(menuSystemVisible);
    }

    // 5. Reset Sidebar State (Professional Workspace Default: Hidden)
    const savedSidebar = localStorage.getItem('mwv_sidebar_visible');
    if (savedSidebar !== null) {
        sidebarVisible = (savedSidebar === 'true');
    } else {
        const config = (window.CONFIG && window.CONFIG.ui_settings) ? window.CONFIG.ui_settings : {};
        sidebarVisible = config.sidebar_visible || false;
    }
    
    applySidebarState();
    
    // 6. Initialize Splitters (v1.37 Restoration)
    initAllSplitters();

    // 7. Initial Viewport Geometery Pass
    refreshViewportLayout();
    
    window.__mwv_ui_nav_loaded = true;
    console.info("[UI-INIT] UI Orchestration Layer Ready.");
});

window.toggleProbeFlow = function() {
    if (!window.CONFIG || !window.CONFIG.ui_settings) return;
    
    // Toggle the value
    window.CONFIG.ui_settings.probe_data_flow_enabled = !window.CONFIG.ui_settings.probe_data_flow_enabled;
    const isActive = window.CONFIG.ui_settings.probe_data_flow_enabled;
    
    // Update UI button
    const btn = document.getElementById('footer-btn-probe-flow');
    if (btn) {
        btn.classList.toggle('active', isActive);
        btn.style.borderColor = isActive ? '#00f2ff' : '';
        btn.style.color = isActive ? '#00f2ff' : '';
    }

    console.log(`[FORENSIC] PROBE DATA FLOW: ${isActive ? 'ENABLED (Handshake)' : 'DISABLED (Direct)'}`);
    
    // Refresh Audit Panel if open
    if (typeof refreshForensicAudit === 'function') refreshForensicAudit();
};

/**
 * Initializes the Forensic 7++ State on Boot
 */
window.initForensicUI = function() {
    const config = (window.CONFIG && window.CONFIG.ui_settings) ? window.CONFIG.ui_settings : {};
    
    // 1. Apply Elite HUD if enabled
    if (config.elite_hud_enabled) {
        document.body.classList.add('forensic-elite');
        console.log("[FORENSIC] ELITE HUD: INITIALIZED");
    }

    // 2. Apply Global Forensic Lockdown
    const forensicsAllowed = (typeof config.forensics_enabled !== 'undefined') ? config.forensics_enabled : true;
    if (!forensicsAllowed) {
        console.log("[FORENSIC] LOCKDOWN: Hiding technical interfaces.");
        const techControls = document.getElementById('footer-technical-controls');
        if (techControls) techControls.style.display = 'none';
        
        const pulsarIcon = document.getElementById('footer-pulsar-icon');
        if (pulsarIcon) pulsarIcon.style.display = 'none';
    }

    // 3. Initial Sync
    const probeBtn = document.getElementById('footer-btn-probe-flow');
    if (probeBtn && config.probe_data_flow_enabled) {
        probeBtn.classList.add('active');
        probeBtn.style.borderColor = '#00f2ff';
        probeBtn.style.color = '#00f2ff';
    }
};

window.renderHydrationMatrix = function() {
    console.debug("[HYD-AUDIT] Matrix Refresh triggered.");
    // UI update logic for hydration cells
};

// Auto-Init on load
window.addEventListener('load', () => {
    setTimeout(window.initForensicUI, 500);
});

/**
 * [v1.38.05] Renders the Config Master toggles in the Diagnostics Sidebar.
 */
async function renderConfigToggles() {
    const modulesContainer = document.getElementById('config-module-matrix');
    const fragmentsContainer = document.getElementById('config-fragment-matrix');
    if (!modulesContainer || !fragmentsContainer) return;

    modulesContainer.innerHTML = '<div style="font-size: 8px; opacity: 0.5;">Loading config...</div>';
    fragmentsContainer.innerHTML = '';

    try {
        const config = await eel.get_global_config()();
        const ui = config.ui_settings || {};
        const fragments = ui.ui_fragments || {};

        // 1. Functional Modules
        const moduleKeys = [
            { key: 'audio_engine_enabled', label: 'Audio Engine' },
            { key: 'video_engine_enabled', label: 'Video Engine' },
            { key: 'queue_panel_enabled', label: 'Queue Panel' },
            { key: 'lyrics_panel_enabled', label: 'Lyrics/Metadata' },
            { key: 'sidebar_allowed', label: 'Sidebar Global' }
        ];

        modulesContainer.innerHTML = moduleKeys.map(m => `
            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); padding: 6px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                <span style="font-size: 9px; font-weight: 600; color: #ccc;">${m.label}</span>
                <input type="checkbox" ${ui[m.key] ? 'checked' : ''} onchange="updateUIConfigToggle('ui_settings.${m.key}', this.checked)" style="accent-color: #ff3366; cursor: pointer;">
            </div>
        `).join('');

        // 2. UI Fragments
        fragmentsContainer.innerHTML = Object.keys(fragments).map(key => `
            <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255,255,255,0.02); padding: 6px 10px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.05);">
                <span style="font-size: 8px; color: #aaa;">${key.toUpperCase()}</span>
                <input type="checkbox" ${fragments[key] ? 'checked' : ''} onchange="updateUIConfigToggle('ui_fragments.${key}', this.checked)" style="accent-color: #ff3366; scale: 0.8; cursor: pointer;">
            </div>
        `).join('');

    } catch (e) {
        console.error("[UI-CONFIG] Failed to render toggles:", e);
        modulesContainer.innerHTML = '<div style="color: red; font-size: 8px;">Error loading config</div>';
    }
}

/**
 * Updates a configuration value via Eel and refreshes the UI (v1.38.05).
 */
async function updateUIConfigToggle(key, value) {
    console.log(`[UI-CONFIG] Toggling ${key} to ${value}`);
    try {
        const success = await eel.set_ui_config_value(key, value)();
        if (success) {
            // Hot-reload visibility if it's a UI flag
            if (key.includes('ui_') || key.includes('visible')) {
                if (typeof refreshUIVisibility === 'function') refreshUIVisibility();
            }
            if (typeof showToast === 'function') showToast(`${key} -> ${value}`, 'success');
        }
    } catch (e) {
        console.error("[UI-CONFIG] Toggle failed:", e);
    }
}


/**
 * [v1.38.07] Renders the Startup Timeline (Boot Profile).
 */
async function renderBootTimeline() {
    const container = document.getElementById('boot-timeline-container');
    if (!container) return;

    try {
        const report = await eel.get_startup_report()();
        const phases = report.phases || [];
        
        if (phases.length === 0) {
            container.innerHTML = '<div style="font-size: 8px; opacity: 0.4;">NO BOOT DATA AVAILABLE</div>';
            return;
        }

        const maxDuration = Math.max(...phases.map(p => p.duration || 0.1));
        
        container.innerHTML = phases.map(p => {
            const width = Math.max(5, (p.duration / maxDuration) * 100);
            const color = p.duration > 1.0 ? '#ff3366' : (p.duration > 0.3 ? '#ff9500' : '#00ffcc');
            return `
                <div style="margin-bottom: 4px;">
                    <div style="display: flex; justify-content: space-between; font-size: 8px; margin-bottom: 2px;">
                        <span>${p.phase}</span>
                        <span style="font-weight: 800; color: ${color};">${(p.duration * 1000).toFixed(0)}ms</span>
                    </div>
                    <div style="height: 3px; background: rgba(255,255,255,0.05); border-radius: 2px; overflow: hidden;">
                        <div style="width: ${width}%; height: 100%; background: ${color}; border-radius: 2px;"></div>
                    </div>
                </div>
            `;
        }).join('');

        // [v1.38.08] Populate Sentinel Audit
        const auditContainer = document.getElementById('sentinel-audit-container');
        if (auditContainer && window.UISentinel) {
            const audit = window.UISentinel.getAuditReport();
            const checks = window.UISentinel.checks;
            
            auditContainer.innerHTML = checks.map(c => {
                const res = audit[c.id] || { exists: false, visible: false };
                const dotColor = res.exists ? (res.visible ? '#00ffcc' : '#ff9500') : '#ff3366';
                const statusText = res.exists ? (res.visible ? 'ACTIVE' : 'HIDDEN') : 'MISSING';
                return `
                    <div style="display: flex; justify-content: space-between; font-size: 7px; align-items: center; background: rgba(255,255,255,0.03); padding: 4px 6px; border-radius: 4px;">
                        <span style="opacity: 0.7;">${c.label}</span>
                        <div style="display: flex; align-items: center; gap: 4px;">
                            <span style="color: ${dotColor}; font-weight: 800;">${statusText}</span>
                            <div style="width: 4px; height: 4px; border-radius: 50%; background: ${dotColor};"></div>
                        </div>
                    </div>
                `;
            }).join('');
        }

    } catch (e) {
        console.error("[UI-BOOT] Failed to render timeline:", e);
        container.innerHTML = '<div style="color: red; font-size: 8px;">Error loading boot profile</div>';
    }
}


/**
 * [v1.38.08] UI Sentinel: System-level monitor for fragment integrity.
 * Ensures critical elements are never stuck in "Black Hole" or "Missing" states.
 */
const UISentinel = {
    checks: [
        { id: 'player-sub-nav-shell', label: 'Audio Sub-Menu', critical: true, registryKey: 'player-tabs' },
        { id: 'main-splitter', label: 'Layout Splitter', critical: false },
        { id: 'player-detailed-sidebar', label: 'Premium Sidebar', critical: false, registryKey: 'player-sidebar' },
        { id: 'player-main-viewport', label: 'Audio Engine Canvas', critical: true, registryKey: 'player-engine' }
    ],

    audit: {},

    validate: function() {
        console.log(">>> [Sentinel] Performing Integrity Audit...");
        this.checks.forEach(check => {
            const el = document.getElementById(check.id);
            const exists = !!el;
            let visible = false;
            if (exists) {
                const style = window.getComputedStyle(el);
                visible = style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
                
                // --- AUTO-FIX: Force visibility for critical dead-zones ---
                if (check.critical && !visible && window.__mwv_ui_nav_loaded) {
                    console.warn(`[Sentinel] CRITICAL FIX: Restoring visibility for ${check.label} (#${check.id})`);
                    el.style.setProperty('display', 'flex', 'important');
                    el.style.setProperty('opacity', '1', 'important');
                }
            }
            this.audit[check.id] = { exists, visible };

            // [v1.38.08] Sync with Hydration Registry for BOOT diagnostics
            if (exists && visible && check.registryKey) {
                if (typeof window.auditFragmentHydration === 'function') {
                    window.auditFragmentHydration(check.registryKey, 'success');
                }
            }
        });
        
        // Sync results to the BOOT tab if open
        if (typeof renderBootTimeline === 'function') {
            const bootPane = document.getElementById('diag-pane-boot');
            if (bootPane && bootPane.style.display !== 'none') renderBootTimeline();
        }
    },

    getAuditReport: function() {
        return this.audit;
    }
};

window.UISentinel = UISentinel;

// Register Sentinel start
window.addEventListener('load', () => {
    setTimeout(() => UISentinel.validate(), 500);  // Initial fast check
    setTimeout(() => UISentinel.validate(), 2000); // Deferred check after background items load
});

window.renderConfigToggles = renderConfigToggles;
window.updateUIConfigToggle = updateUIConfigToggle;
window.renderBootTimeline = renderBootTimeline;
