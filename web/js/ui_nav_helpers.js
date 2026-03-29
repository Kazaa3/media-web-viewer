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
            ['main-splitter', 'main-sidebar', 'main-split-container', 'vertical', 'left'],
            ['parser-tab-splitter', 'parser-left-settings', 'parser-tab-split-container', 'vertical', 'left'],
            ['debug-splitter', 'debug-settings-pane', 'debug-flag-persistence-panel', 'vertical', 'right'],
            ['logbuch-splitter', 'logbuch-sidebar', 'logbuch-split-container', 'vertical', 'right'],
            ['player-analytics-splitter', 'video-queue-pane', 'player-tab-split-container', 'vertical', 'right'],
            ['browser-tab-splitter', 'browser-top-pane', 'filesystem-crawler-directory-panel', 'horizontal', 'top']
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
    let librarySubTab = localStorage.getItem('mwv_library_sub_tab') || 'coverflow';
    const previousTab = localStorage.getItem('mwv_active_tab') || 'player';
    traceUiNav('TAB', tabId, {from: previousTab});
    
    document.querySelectorAll('.tab-content').forEach(el => {
        el.style.display = 'none';
        el.classList.remove('active');
    });
    
    const tabMap = {
        'player': 'state-orchestrated-active-queue-list-container',
        'library': 'coverflow-library-panel',
        'item': 'indexed-sqlite-media-repository-panel',
        'file': 'filesystem-crawler-directory-panel',
        'edit': 'metadata-writer-crud-panel',
        'options': 'system-configuration-persistence-panel',
        'parser': 'regex-provider-chain-orchestrator-panel',
        'debug': 'telemetry-inspector-tab-trigger', 
        'tests': 'quality-assurance-regression-suite-panel',
        'reporting': 'reporting-dashboard-panel',
        'logbuch': 'localized-markdown-documentation-journal-panel',
        'playlist': 'json-serialized-sequence-buffer-panel',
        'video': 'multiplexed-media-player-orchestrator-panel',
        'vlc': 'multiplexed-media-player-orchestrator-panel',
        'tools': 'tools-tab',
        'flags': 'debug-flag-persistence-panel'
    };

    const targetId = tabMap[tabId] || tabId;
    const panel = document.getElementById(targetId);
    if (panel) {
        panel.classList.add('active');
        const isFlex = ['player', 'library', 'item', 'file', 'edit', 'options', 'parser', 'debug', 'tests', 'reporting', 'logbuch', 'playlist', 'vlc', 'video', 'tools'].includes(tabId);
        panel.style.display = isFlex ? 'flex' : 'block';
        
        if (isFlex) {
            panel.style.flex = '1';
            panel.style.height = '100%';
            panel.style.width = '100%';
            panel.style.minWidth = '0';
            panel.style.flexDirection = 'column';
        }
    }

    // Update button states in both main and sub nav
    document.querySelectorAll('.tab-btn, .nav-btn, .tab-link, .sub-tab-btn').forEach(b => b.classList.remove('active'));
    
    if (btn) {
        btn.classList.add('active');
    } else {
        // Try to find the button in the sub-nav-container first
        const subNavBtn = document.querySelector(`#sub-nav-container .sub-tab-btn[onclick*="'${tabId}'"]`);
        if (subNavBtn) {
            subNavBtn.classList.add('active');
        } else {
            const fallbackBtn = document.querySelector(`.nav-btn[onclick*="${tabId}"], .tab-btn[onclick*="${tabId}"], .tab-link[data-tab="${tabId}"]`);
            if (fallbackBtn) fallbackBtn.classList.add('active');
        }
    }

    localStorage.setItem('mwv_active_tab', tabId);

    // Context-specific actions (Repairing all tabs)
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
        'debug': () => { if (typeof renderDebugTelemetrie === 'function') renderDebugTelemetrie(); },
        'flags': () => { if (typeof loadDebugFlags === 'function') loadDebugFlags(); },
        'reporting': () => { if (typeof renderReportingDashboard === 'function') renderReportingDashboard(); },
        'logbuch': () => { if (typeof renderLogbuch === 'function') renderLogbuch(); },
        'tests': () => { if (typeof renderVideoTestSuite === 'function') renderVideoTestSuite(); }
    };

    if (initActions[tabId]) {
        // Use requestAnimationFrame to ensure the DOM is updated before rendering
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
    traceUiNav('MAIN-CAT', category);
    
    document.querySelectorAll('#main-nav-tabs .tab-btn').forEach(b => b.classList.remove('active'));
    if (btn) btn.classList.add('active');

    const subNav = document.getElementById('sub-nav-container');
    if (!subNav) return;

    subNav.style.display = 'flex';
    subNav.innerHTML = ''; // Clear existing

    const subTabs = {
        'media': [
            { id: 'player', label: 'Player', icon: '#icon-audio' },
            { id: 'library', label: 'Bibliothek', icon: '#icon-folder' },
            { id: 'playlist', label: 'Playlist', icon: '#icon-playlist' }
        ],
        'video': [
            { id: 'video', label: 'Video Player', icon: '#icon-video' }
        ],
        'management': [
            { id: 'item', label: 'Item', icon: '#icon-search' },
            { id: 'file', label: 'Datei', icon: '#icon-folder' },
            { id: 'edit', label: 'Edit', icon: '#icon-edit' },
            { id: 'parser', label: 'Parser', icon: '#icon-settings' },
            { id: 'tools', label: 'Tools', icon: '#icon-settings' }
        ],
        'governance': [
            { id: 'options', label: 'Optionen', icon: '#icon-options' },
            { id: 'debug', label: 'Debug DB', icon: '#icon-debug' },
            { id: 'flags', label: 'Flags', icon: '#icon-settings' }
        ],
        'diagnostics': [
            { id: 'tests', label: 'Tests', icon: '#icon-test' },
            { id: 'reporting', label: 'Reporting', icon: '#icon-stats' },
            { id: 'logbuch', label: 'Logbuch', icon: '#icon-edit' }
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

/**
 * Context Menu Logic
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
    const existing = document.getElementById('impressum-modal');
    if (existing) {
        existing.style.display = (existing.style.display === 'none') ? 'flex' : 'none';
    } else {
        // Create simple modal if not in HTML
        const modal = document.createElement('div');
        modal.id = 'impressum-modal';
        modal.className = 'glass-panel';
        modal.style = "position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.8); z-index:9999; display:flex; align-items:center; justify-content:center; backdrop-filter:blur(10px);";
        modal.onclick = () => modal.style.display = 'none';
        modal.innerHTML = `
            <div style="background:white; padding:40px; border-radius:12px; max-width:500px; color:#333; position:relative;">
                <h2>Impressum</h2>
                <p>Media Web Viewer v1.35</p>
                <p>Created for Advanced Media Management.</p>
                <button class="tab-btn" style="margin-top:20px;">Schließen</button>
            </div>
        `;
        document.body.appendChild(modal);
    }
}

// Window listeners for menu dismissal
window.addEventListener('click', () => hideContextMenu());
window.addEventListener('scroll', () => hideContextMenu(), true);
