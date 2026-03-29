/**
 * UI Navigation & Tab Switching Helpers
 * Extracted from app.html to improve modularity and maintainability.
 */

// Global state variables
let librarySubTab = 'coverflow';
let librarySubFilter = 'all';

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
        'debug': 'debug-flag-persistence-panel',
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

    document.querySelectorAll('.tab-btn, .nav-btn, .tab-link').forEach(b => b.classList.remove('active'));
    if (btn) {
        btn.classList.add('active');
    } else {
        const fallbackBtn = document.querySelector(`.nav-btn[onclick*="${tabId}"], .tab-btn[onclick*="${tabId}"], .tab-link[data-tab="${tabId}"]`);
        if (fallbackBtn) fallbackBtn.classList.add('active');
    }

    localStorage.setItem('mwv_active_tab', tabId);

    if (tabId === 'library' && typeof renderLibrary === 'function') renderLibrary();
    if (tabId === 'item' && typeof refreshLibrary === 'function') refreshLibrary();
    if (tabId === 'options') {
        if (typeof loadDebugFlags === 'function') loadDebugFlags();
        if (typeof loadEnvironmentInfo === 'function') loadEnvironmentInfo();
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
 * Switches between views in the Reporting panel.
 */
function switchReportingView(view) {
    traceUiNav('SUBTAB-REPORT', view);
    const views = {
        'dashboard': document.getElementById('reporting-dashboard-view'),
        'database': document.getElementById('reporting-database-view'),
        'video-streaming': document.getElementById('reporting-video-streaming-view'),
        'audio-streaming': document.getElementById('reporting-audio-streaming-view'),
        'parser': document.getElementById('reporting-parser-view'),
        'model-analysis': document.getElementById('reporting-model-analysis-view'),
        'routing-suite': document.getElementById('reporting-routing-suite-view')
    };

    for (const [key, el] of Object.entries(views)) {
        if (el) el.style.display = (view === key) ? 'block' : 'none';
    }

    document.querySelectorAll('.reporting-subtab').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-view') === view);
    });

    if (view === 'database' && typeof loadSqlFiles === 'function') loadSqlFiles();
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
