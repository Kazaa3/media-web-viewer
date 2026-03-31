/**
 * UI Navigation & Tab Switching Helpers
 * Extracted from app.html to improve modularity and maintainability.
 */

// Global state variables
let librarySubTab = 'coverflow';
let librarySubFilter = 'all';
let currentMainCategory = 'media';

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
    } catch (e) {}
    
    if (typeof appendUiTrace === 'function') {
        appendUiTrace(logMsg);
    }
}

/**
 * Switches between main application tabs.
 */
function switchTab(tabId, btn) {
    let librarySubTab = localStorage.getItem('mwv_active_tab') || 'player';
    const previousTab = localStorage.getItem('mwv_active_tab') || 'player';
    traceUiNav('TAB', tabId, {from: previousTab});
    
    // Define fragment mapping
    const fragmentMap = {
        'debug': { containerId: 'diagnostics-suite-container', path: 'fragments/diagnostics_suite.html' },
        'tests': { containerId: 'diagnostics-suite-container', path: 'fragments/diagnostics_suite.html' },
        'reporting': { containerId: 'reporting-dashboard-container', path: 'fragments/reporting_dashboard.html' },
        'file': { containerId: 'filesystem-crawler-directory-panel', path: 'fragments/filesystem_browser.html' },
        'library': { containerId: 'coverflow-library-panel', path: 'fragments/library_explorer.html' },
        'item': { containerId: 'indexed-sqlite-media-repository-panel', path: 'fragments/item_inventory.html' },
        'edit': { containerId: 'metadata-writer-crud-panel', path: 'fragments/metadata_editor.html' },
        'video': { containerId: 'multiplexed-media-player-orchestrator-panel', path: 'fragments/video_player.html' },
        'vlc': { containerId: 'multiplexed-media-player-orchestrator-panel', path: 'fragments/video_player.html' },
        'tools': { containerId: 'tools-panel-container', path: 'fragments/tools_panel.html' },
        'options': { containerId: 'options-panel-container', path: 'fragments/options_panel.html' },
        'logbuch': { containerId: 'logbook-panel-container', path: 'fragments/logbuch_panel.html' },
        'player': { containerId: 'state-orchestrated-active-queue-list-container', path: 'fragments/player_queue.html' },
        'playlist': { containerId: 'json-serialized-sequence-buffer-panel', path: 'fragments/playlist_manager.html' }
    };

    const tabMap = {
        'player': 'state-orchestrated-active-queue-list-container',
        'library': 'coverflow-library-panel',
        'item': 'indexed-sqlite-media-repository-panel',
        'file': 'filesystem-crawler-directory-panel',
        'edit': 'metadata-writer-crud-panel',
        'options': 'options-panel-container',
        'logbuch': 'logbook-panel-container',
        'tools': 'tools-panel-container',
        'playlist': 'json-serialized-sequence-buffer-panel',
        'video': 'multiplexed-media-player-orchestrator-panel',
        'vlc': 'multiplexed-media-player-orchestrator-panel'
    };

    const targetId = tabMap[tabId] || tabId;

    // Handle Fragment Loading
    if (fragmentMap[tabId]) {
        const frag = fragmentMap[tabId];
        FragmentLoader.load(frag.containerId, frag.path, () => {
            // Once fragment is loaded, recursive call to show the actual panel
            finishSwitchTab(tabId, targetId, btn);
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
        const isFlex = ['player', 'library', 'item', 'file', 'edit', 'options', 'parser', 'debug', 'tests', 'reporting', 'logbuch', 'playlist', 'vlc', 'video', 'tools'].includes(tabId);
        panel.style.display = isFlex ? 'flex' : 'block';
        
        if (typeof mwv_trace === 'function') {
            mwv_trace('NAV-TAB', tabId, { targetId });
        }

        if (isFlex) {
            panel.style.flex = '1';
            panel.style.height = '100%';
            panel.style.width = '100%';
            panel.style.minWidth = '0';
        }

        // --- Global Sidebar Management ---
        const sidebar = document.getElementById('main-sidebar');
        const splitter = document.getElementById('main-splitter');
        if (sidebar && splitter) {
            const sidebarVisibleTabs = ['player', 'video', 'vlc', 'playlist'];
            const shouldShow = sidebarVisibleTabs.includes(tabId);
            sidebar.style.display = shouldShow ? 'flex' : 'none';
            splitter.style.display = shouldShow ? 'block' : 'none';
        }
    }

    // Update button states
    document.querySelectorAll('.tab-btn, .nav-btn, .tab-link, .sub-tab-btn').forEach(b => b.classList.remove('active'));
    
    if (btn) {
        btn.classList.add('active');
    } else {
        const subNavBtn = document.querySelector(`#sub-nav-container .sub-tab-btn[onclick*="'${tabId}'"]`);
        if (subNavBtn) {
            subNavBtn.classList.add('active');
        } else {
            const fallbackBtn = document.querySelector(`.nav-btn[onclick*="${tabId}"], .tab-btn[onclick*="${tabId}"], .tab-link[data-tab="${tabId}"]`);
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
        'debug': () => { if (typeof renderDebugDatabase === 'function') renderDebugDatabase(); },
        'flags': () => { if (typeof loadDebugFlags === 'function') loadDebugFlags(); },
        'reporting': () => { if (typeof updateAnalyticsDashboard === 'function') updateAnalyticsDashboard(); },
        'logbuch': () => { if (typeof loadLogbuchTab === 'function') loadLogbuchTab(); },
        'tests': () => { if (typeof switchTestView === 'function') switchTestView('base'); }
    };

    if (initActions[tabId]) {
        requestAnimationFrame(() => {
            initActions[tabId]();
        });
    }
}

/**
 * Switch top-level category and populate sub-navigation.
 */
function switchMainCategory(category, btn) {
    currentMainCategory = category;
    
    // Log the category change
    if (typeof mwv_trace === 'function') {
        mwv_trace('NAV-CATEGORY', category);
    }
    
    document.querySelectorAll('#main-nav-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const subNav = document.getElementById('sub-nav-container');
    if (!subNav) return;

    subNav.style.display = 'flex';
    subNav.innerHTML = ''; // Clear existing

    const subTabs = {
        'media': [
            { id: 'player', label: 'Warteschlange', icon: '#icon-audio' },
            { id: 'playlist', label: 'Playlist Manager', icon: '#icon-playlist' }
        ],
        'library': [
            { id: 'item', label: 'Item', icon: '#icon-search' },
            { id: 'file', label: 'Datei', icon: '#icon-folder' },
            { id: 'edit', label: 'Edit', icon: '#icon-edit' },
            { id: 'parser', label: 'Parser', icon: '#icon-settings' },
            { id: 'tools', label: 'Tools', icon: '#icon-settings' }
        ],
        'video': [
            { id: 'video', label: 'Video Player', icon: '#icon-video' },
            { id: 'vlc', label: 'VLC Proxy', icon: '#icon-video' }
        ],
        'tools': [
            { id: 'parser', label: 'Parser Config', icon: '#icon-settings' },
            { id: 'tools', label: 'Advanced Tools', icon: '#icon-settings' }
        ],
        'system': [
            { id: 'options', label: 'Optionen', icon: '#icon-options' },
            { id: 'debug', label: 'Debug DB', icon: '#icon-debug' },
            { id: 'flags', label: 'Flags', icon: '#icon-settings' }
        ],
        'diagnostics': [
            { id: 'tests', label: 'Legacy Tests', icon: '#icon-test' },
            { id: 'reporting', label: 'Analytics', icon: '#icon-stats' },
            { id: 'logbuch', label: 'System Log', icon: '#icon-edit' }
        ]
    };

    const tabs = subTabs[category] || [];
    tabs.forEach(tab => {
        const button = document.createElement('button');
        button.className = 'sub-tab-btn';
        button.innerHTML = `
            <svg width="14" height="14"><use href="${tab.icon}"></use></svg>
            <span>${tab.label}</span>
        `;
        button.onclick = (e) => switchTab(tab.id, button);
        subNav.appendChild(button);
    });

    // Automatically switch to the first tab of the category if not already on one of them
    const activeTab = localStorage.getItem('mwv_active_tab');
    const isAlreadyInCategory = tabs.some(t => t.id === activeTab);
    
    if (!isAlreadyInCategory && tabs.length > 0) {
        switchTab(tabs[0].id, subNav.firstChild);
    } else if (isAlreadyInCategory) {
        // Just activate the button in sub-nav
        const searchStr = `'${activeTab}'`;
        for(let child of subNav.children) {
            if (child.onclick.toString().includes(searchStr)) {
                child.classList.add('active');
                break;
            }
        }
    }
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

function toggleMenuBar() {
    const bar = document.getElementById('program-menu-bar');
    if (!bar) return;
    menuBarVisible = !menuBarVisible;
    bar.style.display = menuBarVisible ? 'flex' : 'none';
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
