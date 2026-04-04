/**
 * UI Navigation & Tab Switching Helpers
 * Extracted from app.html to improve modularity and maintainability.
 */

// Global state variables
let librarySubTab = 'coverflow';
let librarySubFilter = 'all';
let currentMainCategory = 'media';

window.__mwv_ui_nav_loaded = true;

let sidebarVisible = false; // Default to closed for Classic v1.34 Restoration

/**
 * Toggles the main sidebar visibility.
 */
function toggleSidebar() {
    const sidebar = document.getElementById('main-sidebar');
    const splitter = document.getElementById('main-splitter');
    if (!sidebar) return;

    sidebarVisible = !sidebarVisible;
    applySidebarState();

    // Persist only if user explicitly toggles it? 
    // Or just store it. Let's store it.
    localStorage.setItem('mwv_sidebar_visible', sidebarVisible);

    console.log(`UI: Sidebar toggled. Visible: ${sidebarVisible}`);
}

/**
 * Applies the current sidebarVisible state to the DOM.
 */
function applySidebarState() {
    const sidebar = document.getElementById('main-sidebar');
    const splitter = document.getElementById('main-splitter');
    if (!sidebar) return;

    sidebar.style.width = sidebarVisible ? '300px' : '0px';
    sidebar.style.minWidth = sidebarVisible ? '200px' : '0px';
    sidebar.style.opacity = sidebarVisible ? '1' : '0';
    sidebar.style.pointerEvents = sidebarVisible ? 'all' : 'none';

    if (splitter) splitter.style.display = sidebarVisible ? 'block' : 'none';

    // Update toggle button state if it exists
    const toggleBtn = document.getElementById('sidebar-toggle-btn');
    if (toggleBtn) toggleBtn.classList.toggle('active', sidebarVisible);
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
            ['edit-splitter', 'edit-sidebar-left', 'edit-split-container', 'vertical', 'left'],
            ['lib-splitter', 'lib-sidebar-left', 'lib-split-container', 'vertical', 'left'],
            ['main-splitter', 'main-sidebar', 'main-split-container', 'vertical', 'left'],
            ['parser-tab-splitter', 'parser-left-settings', 'parser-tab-split-container', 'vertical', 'left'],
            ['debug-splitter', 'debug-settings-pane', 'debug-flag-persistence-panel', 'vertical', 'right'],
            ['logbuch-splitter', 'logbuch-sidebar', 'logbuch-split-container', 'vertical', 'right'],
            ['player-analytics-splitter', 'video-queue-pane', 'player-tab-split-container', 'vertical', 'right'],
            ['browser-tab-splitter', 'browser-left-sidebar', 'filesystem-crawler-directory-panel', 'vertical', 'left']
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
function switchTab(tabId, btn, callback) {
    const previousTab = localStorage.getItem('mwv_active_tab') || 'player';
    traceUiNav('TAB', tabId, { from: previousTab });

    // Define fragment mapping
    const fragmentMap = {
        'debug': { containerId: 'diagnostics-suite-container', path: 'fragments/diagnostics_suite.html' },
        'tests': { containerId: 'diagnostics-suite-container', path: 'fragments/diagnostics_suite.html' },
        'diagnostics': { containerId: 'diagnostics-suite-container', path: 'fragments/diagnostics_suite.html' },
        'reporting': { containerId: 'reporting-dashboard-container', path: 'fragments/reporting_dashboard.html' },
        'file': { containerId: 'filesystem-crawler-directory-panel', path: 'fragments/filesystem_browser.html' },
        'library': { containerId: 'coverflow-library-panel', path: 'fragments/library_explorer.html' },
        'grid': { containerId: 'coverflow-library-panel', path: 'fragments/library_explorer.html' },
        'details': { containerId: 'coverflow-library-panel', path: 'fragments/library_explorer.html' },
        'album': { containerId: 'coverflow-library-panel', path: 'fragments/library_explorer.html' },
        'item': { containerId: 'indexed-sqlite-media-repository-panel', path: 'fragments/item_inventory.html' },
        'edit': { containerId: 'metadata-writer-crud-panel', path: 'fragments/metadata_editor.html' },
        'video': { containerId: 'multiplexed-media-player-orchestrator-panel', path: 'fragments/video_player.html' },
        'vlc': { containerId: 'multiplexed-media-player-orchestrator-panel', path: 'fragments/video_player.html' },
        'tools': { containerId: 'tools-panel-container', path: 'fragments/tools_panel.html' },
        'options': { containerId: 'options-panel-container', path: 'fragments/options_panel.html' },
        'logbuch': { containerId: 'logbook-tab-container', path: 'fragments/logbook_panel.html' },
        'player': { containerId: 'state-orchestrated-active-queue-list-container', path: 'fragments/player_queue.html' },
        'playlist': { containerId: 'json-serialized-sequence-buffer-panel', path: 'fragments/playlist_manager.html' }
    };

    const tabMap = {
        'player': 'state-orchestrated-active-queue-list-container',
        'library': 'coverflow-library-panel',
        'grid': 'coverflow-library-panel',
        'details': 'coverflow-library-panel',
        'album': 'coverflow-library-panel',
        'item': 'indexed-sqlite-media-repository-panel',
        'file': 'filesystem-crawler-directory-panel',
        'edit': 'metadata-writer-crud-panel',
        'options': 'options-panel-container',
        'logbuch': 'logbook-tab-container',
        'tools': 'tools-panel-container',
        'playlist': 'json-serialized-sequence-buffer-panel',
        'video': 'multiplexed-media-player-orchestrator-panel',
        'vlc': 'multiplexed-media-player-orchestrator-panel',
        'debug': 'diagnostics-suite-container',
        'tests': 'diagnostics-suite-container',
        'diagnostics': 'diagnostics-suite-container',
        'reporting': 'reporting-dashboard-container',
        'tools': 'tools-panel-container'
    };

    const targetId = tabMap[tabId] || tabId;
    const target = document.getElementById(targetId);

    // [DEBUG-TRUNCATED v1.34]
    // if (typeof mwv_trace === 'function') {
    //     mwv_trace('NAV', 'SWITCH-TAB', { tabId, targetId: target ? target.id : 'unknown' });
    // }

    // Handle Fragment Loading
    if (fragmentMap[tabId]) {
        const frag = fragmentMap[tabId];
        FragmentLoader.load(frag.containerId, frag.path, () => {
            // Once fragment is loaded, recursive call to show the actual panel
            finishSwitchTab(tabId, targetId, btn);
            if (typeof callback === 'function') callback();
        });
        // Show the container immediately (it might have a loader)
        const container = document.getElementById(frag.containerId);
        if (container) {
            document.querySelectorAll('.tab-content').forEach(el => {
                el.style.display = 'none';
                el.classList.remove('active');
            });
            container.style.display = 'flex';
            container.classList.add('active');
        }
    } else {
        finishSwitchTab(tabId, targetId, btn);
        if (typeof callback === 'function') callback();
    }
}

/**
 * UI Navigation Helpers
 * Manages tab switching, sidebar visibility, and layout orchestration.
 */

// --- Global UI State ---
let menuBarVisible = false;
function finishSwitchTab(tabId, targetId, btn) {
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

        // if (typeof mwv_trace === 'function') {
        //     mwv_trace('NAV-TAB', tabId, { targetId });
        // }

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

        // --- Global Sidebar Management ---
        const sidebar = document.getElementById('main-sidebar');
        const splitter = document.getElementById('main-splitter');
        if (sidebar && splitter) {
            const sidebarVisibleTabs = ['player', 'video', 'vlc', 'playlist', 'edit', 'reporting', 'debug', 'tests', 'diagnostics', 'library', 'tools', 'logbuch', 'system'];
            const shouldShow = sidebarVisibleTabs.includes(tabId);
            sidebar.style.display = shouldShow ? 'flex' : 'none';
            splitter.style.display = shouldShow ? 'block' : 'none';
        }
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

    // Context-specific actions
    const initActions = {
        'player': () => { if (typeof renderPlaylist === 'function') renderPlaylist(); },
        'playlist': () => { if (typeof renderPlaylist === 'function') renderPlaylist(); },
        'library': () => {
            if (typeof renderPlaylist === 'function') renderPlaylist();
            if (typeof renderLibrary === 'function') renderLibrary();
        },
        'video': () => { if (typeof renderVideoQueue === 'function') renderVideoQueue(); },
        'vlc': () => { if (typeof renderVideoQueue === 'function') renderVideoQueue(); },
        'file': () => { if (typeof fbNavigate === 'function') fbNavigate(typeof fbCurrentPath !== 'undefined' ? fbCurrentPath : '/'); },
        'item': () => { if (typeof refreshLibrary === 'function') refreshLibrary(); },
        'edit': () => { if (typeof initEdit === 'function') initEdit(); },
        'parser': () => { if (typeof loadParserConfig === 'function') loadParserConfig(); },
        'tools': () => { if (typeof renderToolsDashboard === 'function') renderToolsDashboard(); },
        'options': () => {
            if (typeof loadDebugFlags === 'function') loadDebugFlags();
            if (typeof loadEnvironmentInfo === 'function') loadEnvironmentInfo();
        },
        'debug': () => {
            if (typeof switchDiagnosticsView === 'function') {
                switchDiagnosticsView('debug-db');
            } else if (typeof renderDebugDatabase === 'function') {
                renderDebugDatabase();
            }
        },
        'flags': () => { if (typeof loadDebugFlags === 'function') loadDebugFlags(); },
        'reporting': () => { if (typeof updateAnalyticsDashboard === 'function') updateAnalyticsDashboard(); },
        'logbuch': () => { if (typeof loadLogbuchTab === 'function') loadLogbuchTab(); },
        'tests': () => {
            if (typeof switchDiagnosticsView === 'function') {
                switchDiagnosticsView('health');
            }
        },
        'diagnostics': () => {
            if (typeof switchDiagnosticsView === 'function') {
                switchDiagnosticsView('debug-db');
            }
        }
    };
    if (initActions[tabId]) {
        requestAnimationFrame(() => {
            initActions[tabId]();
        });
    }
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

function toggleMenuBar() {
    const bar = document.getElementById('program-menu-bar');
    const subBar = document.getElementById('sub-nav-container');
    if (!bar) return;
    
    const isVisible = !bar.classList.contains('visible');
    bar.classList.toggle('visible', isVisible);
    
    // Total header height logic for v1.34 (40px main + 32px sub = 72px)
    const headerHeight = isVisible ? (subBar && subBar.style.display !== 'none' ? 72 : 40) : 0;
    
    if (subBar) {
        subBar.classList.toggle('visible', isVisible);
        // Position subBar directly under the main bar
        subBar.style.top = '40px'; 
    }
    
    // Offset the main content area to prevent overlap ("abgehackt" fix)
    const container = document.getElementById('main-split-container');
    if (container) {
        container.style.marginTop = `${headerHeight}px`;
        container.style.height = headerHeight > 0 ? `calc(100vh - ${75 + headerHeight}px)` : 'calc(100vh - 75px)';
    }
    
    localStorage.setItem('mwv_menu_bar_visible', isVisible);
}

// --- Keyboard Shortcuts & Global Early Initialization ---
document.addEventListener('keydown', (e) => {
    // Alt key toggles the modern menu bar
    if (e.altKey && !e.shiftKey && !e.ctrlKey) {
        e.preventDefault();
        toggleMenuBar();
    }
});

/**
 * Switch Audio Player Sub-Views (Warteschlange, Mediengalerie, Visualizer)
 */
function switchPlayerView(viewId) {
    console.log(`[NAV] Switching player view to: ${viewId}`);
    
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
    }
    
    // Update sub-nav buttons
    document.querySelectorAll('.player-sub-nav-btn').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.target === viewId) btn.classList.add('active');
    });

    // Save preference
    localStorage.setItem('mwv_player_sub_view', viewId);
}

// Restore menu state on load
document.addEventListener('DOMContentLoaded', () => {
    const savedMenuState = localStorage.getItem('mwv_menu_bar_visible') === 'true';
    if (savedMenuState) toggleMenuBar();
    
    // Ensure library items are synced to player queue on startup
    setTimeout(() => {
        if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
    }, 1500);
});

/**
 * Switch top-level category and populate sub-navigation.
 */
function switchMainCategory(category, btn) {
    console.log(`UI: Main category changed to ${category}`);
    if (typeof traceUiNav === 'function') traceUiNav('CATEGORY-SWITCH', category);
    currentMainCategory = category;
    localStorage.setItem('mwv_active_category', category);

    traceUiNav('NAV-CATEGORY', category);

    // Update active state in header/sidebar
    document.querySelectorAll('.tab-btn, .nav-item').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');
    else {
        const headerBtn = document.querySelector(`.tab-btn[onclick*="'${category}'"]`);
        if (headerBtn) headerBtn.classList.add('active');
    }

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
        'edit': 'edit',
        'reporting': 'reporting',
        'debug': 'debug',
        'tests': 'tests'
    };

    if (categoryDefaults[category]) {
        switchTab(categoryDefaults[category], btn);
    }

    // Dynamically populate sub-navigation header pills
    updateGlobalSubNav(category);
}

/**
 * Updates the global sub-navigation bar with contextual entries.
 */
function updateGlobalSubNav(category) {
    const container = document.getElementById('sub-nav-container');
    if (!container) return;

    // Sub-nav configuration for each category
    const subNavMap = {
        'media': [
            { id: 'warteschlange', label: 'Queue', action: "switchMediaSubView('warteschlange')" },
            { id: 'mediengalerie', label: 'Mediengalerie', action: "switchMediaSubView('mediengalerie')" },
            { id: 'playlist', label: 'Playlist Manager', action: "switchMediaSubView('playlist')" },
            { id: 'visualizer', label: 'Visualizer', action: "switchMediaSubView('visualizer')" },
            { id: 'video-cinema', label: 'Video Cinema', action: "switchMediaSubView('video')" }
        ],
        'reporting': [
            { id: 'dashboard', label: 'Dashboard', action: "switchReportingSubView('dashboard')" },
            { id: 'database', label: 'Database', action: "switchReportingSubView('database')" },
            { id: 'video-health', label: 'Video Health', action: "switchReportingSubView('video-health')" },
            { id: 'audio-health', label: 'Audio Health', action: "switchReportingSubView('audio-health')" }
        ],
        'tests': [
            { id: 'health', label: 'System Health', action: "switchDiagnosticsSubView('health')" },
            { id: 'video-health', label: 'Video Health', action: "switchDiagnosticsSubView('video-health')" },
            { id: 'debug-db', label: 'Debug DB', action: "switchDiagnosticsSubView('debug-db')" },
            { id: 'latency', label: 'Latency Profile', action: "switchDiagnosticsSubView('latency')" }
        ],
        'system': [
            { id: 'general', label: 'Settings', action: "switchOptionsView('general')" },
            { id: 'transcoding', label: 'Transcoding', action: "switchOptionsView('transcoding')" },
            { id: 'parser', label: 'Parser Chain', action: "switchOptionsView('parser')" },
            { id: 'appearance', label: 'Appearance', action: "switchOptionsView('appearance')" },
            { id: 'environment', label: 'Environment', action: "switchOptionsView('environment')" }
        ],
        'edit': [
            { id: 'tags', label: 'Metadata Tags', action: "switchEditSubView('tags')" },
            { id: 'artwork', label: 'Artwork Lab', action: "switchEditSubView('artwork')" },
            { id: 'ffprobe', label: 'Media Analysis', action: "switchEditSubView('ffprobe')" }
        ],
        'library': [
            { id: 'visual', label: 'Mediathek', action: "switchLibrarySubView('visual')" },
            { id: 'browse', label: 'Dateibrowser', action: "switchLibrarySubView('browse')" },
            { id: 'inventory', label: 'Inventar & DB', action: "switchLibrarySubView('inventory')" }
        ],
        'logbuch': [
            { id: 'journal', label: 'Journal', action: "switchLogbookSubView('journal')" },
            { id: 'docs', label: 'Documentation', action: "switchLogbookSubView('docs')" }
        ]
    };

    const entries = subNavMap[category];
    if (!entries) {
        container.style.display = 'none';
        return;
    }

    // Populate the container
    container.innerHTML = entries.map(item => `
        <button id="global-sub-nav-${item.id}" 
                class="sub-pill-btn" 
                onclick="${item.action}; updateSubNavActiveState('${item.id}')">
            ${item.label}
        </button>
    `).join('');

    container.style.display = 'flex';

    // Set initial active state based on category default
    const activeTab = localStorage.getItem('mwv_active_tab');
    updateSubNavActiveState(activeTab);
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
    // Both 'debug' and 'tests' load diagnostics_suite.html
    const masterTab = (viewId === 'debug-db' || viewId === 'debug' || viewId === 'health' || viewId === 'latency') ? 'debug' : 'tests';
    switchTab(masterTab, null, () => {
        if (typeof switchDiagnosticsView === 'function') {
            switchDiagnosticsView(viewId);
        }
        updateSubNavActiveState(viewId);
    });
}

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

function switchLogbookSubView(viewId) {
    switchTab('logbuch', null, () => {
        // High-level scroll or sub-view switching for Logbook
        if (viewId === 'docs' && typeof window.scrollLogbookToDocs === 'function') {
            window.scrollLogbookToDocs();
        }
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
 * Switches between sub-tabs in the Options panel.
 */
function switchOptionsView(viewId) {
    traceUiNav('SUBTAB-OPTIONS', viewId);
    document.querySelectorAll('.options-view').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.options-nav-tabs .options-subtab, #options-settings-pane .options-subtab, .options-subtab').forEach(el => {
        if (el.getAttribute('onclick') && (el.getAttribute('onclick').includes('switchOptionsView') || el.id && (el.id.startsWith('opt-subtab-') || el.id.startsWith('options-subtab-')))) {
            el.classList.remove('active');
        }
    });

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
