/**
 * diagnostics_helpers.js - UI Diagnostic Suite & Lab Implementation
 * Manage system-health, latency profiling, and Database deep-probes.
 * (v1.34 restored for original Debug & DB layout)
 */

window.runLatencyDiagnostics = async function (payloadSize = 0, samples = 5) {
    const count = Math.max(1, Math.min(30, Number(samples) || 5));
    const size = Math.max(0, Math.min(200000, Number(payloadSize) || 0));

    const frontendSamples = [];
    const eelSamples = [];
    const bottleSamples = [];

    const measureFrame = () => new Promise((resolve) => {
        const start = performance.now();
        requestAnimationFrame(() => resolve(performance.now() - start));
    });

    const measureEel = async () => {
        const start = performance.now();
        if (typeof eel !== 'undefined' && eel.api_ping) {
            await eel.api_ping(Date.now(), size)();
        }
        return performance.now() - start;
    };

    const measureBottle = async () => {
        const start = performance.now();
        await fetch('/health', { cache: 'no-store' });
        return performance.now() - start;
    };

    for (let i = 0; i < count; i++) {
        frontendSamples.push(await measureFrame());
        if (typeof eel !== 'undefined') eelSamples.push(await measureEel());
        bottleSamples.push(await measureBottle());
    }

    const avg = (arr) => arr.length ? arr.reduce((a, b) => a + b, 0) / arr.length : 0;
    const p95 = (arr) => {
        if (!arr.length) return 0;
        const sorted = [...arr].sort((a, b) => a - b);
        const idx = Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95));
        return sorted[idx];
    };

    const result = {
        samples: count,
        payloadSize: size,
        frontend: { avgMs: Number(avg(frontendSamples).toFixed(2)), p95Ms: Number(p95(frontendSamples).toFixed(2)) },
        eelRoundtrip: { avgMs: Number(avg(eelSamples).toFixed(2)), p95Ms: Number(p95(eelSamples).toFixed(2)) },
        bottleHttp: { avgMs: Number(avg(bottleSamples).toFixed(2)), p95Ms: Number(p95(bottleSamples).toFixed(2)) },
        raw: { frontendSamples, eelSamples, bottleSamples },
    };

    console.info('[LatencyDiagnostics]', result);
    return result;
};

// --- TAB RENDERING: DEBUG DATABASE ---
// --- TAB RENDERING: DEBUG DATABASE ---
window.debugLogBuffer = []; // Store logs for filtering

/**
 * VS Code Dark Syntax Highlighter (v1.35.68)
 */
function syntaxHighlightJSON(json) {
    if (typeof json !== 'string') json = JSON.stringify(json, undefined, 2);
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        let cls = 'json-number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'json-key';
            } else {
                cls = 'json-string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'json-boolean';
        } else if (/null/.test(match)) {
            cls = 'json-null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

/**
 * Modern Database Overview Renderer (v1.35.68 Refined)
 * Restores the Category Breakdown requested by user.
 */
/**
 * Modern Database Overview Renderer (v1.35.68 Final Consolidation)
 * Restores the Category Breakdown requested by user.
 */
function renderDatabaseOverview() {
    const container = document.getElementById('debug-db-overview-content');
    if (!container) return;

    // Use live items or last known db count
    const items = window.allLibraryItems || [];
    const dbTotal = window.__mwv_last_db_count || 0;
    const guiTotal = items.length;
    
    // Group by category
    const cats = {};
    items.forEach(item => {
        const c = item.category || 'Uncategorized';
        cats[c] = (cats[c] || 0) + 1;
    });

    let catListHtml = Object.entries(cats).map(([cat, count]) => 
        `<li><span style="color: var(--text-primary); font-weight: 700;">${cat}:</span> ${count}</li>`
    ).join('');

    container.innerHTML = `
        <div style="display: flex; gap: 60px; align-items: flex-start;">
            <div style="flex: 0 0 auto;">
                <div style="font-size: 10px; font-weight: 900; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 5px;">Database Stats</div>
                <h4 style="margin: 0; font-size: 1.8em; color: var(--text-primary); font-weight: 900; letter-spacing: -1px;">Items: ${dbTotal}</h4>
            </div>
            <div style="flex: 1;">
                <div style="font-size: 10px; font-weight: 900; color: var(--text-secondary); text-transform: uppercase; margin-bottom: 5px;">Category Breakdown (GUI)</div>
                <ul style="margin: 0; padding-left: 15px; font-size: 12px; color: var(--text-secondary); line-height: 1.6; list-style: square;">
                    ${catListHtml || '<li>Warte auf Daten-Sync...</li>'}
                </ul>
            </div>
        </div>
    `;
}

window.renderDebugDatabase = async function() {
    console.log("[DebugDB] Querying Overview state...");
    const select = document.getElementById('debug-dict-select');
    const display = document.getElementById('debug-items-json');
    
    // 1. Update the Summary Card (with Categories)
    renderDatabaseOverview();

    // 2. Flags are now in their own tab, so we don't render them here anymore.

    if (!display) return;
    const type = select ? select.value : 'library';
    let data = {};

    try {
        if (type === 'library') {
            data = window.allLibraryItems || [];
        } else if (typeof eel !== 'undefined' && eel.get_debug_dict) {
            data = await eel.get_debug_dict(type)();
        }
    } catch (err) {
        console.error("renderDebugDatabase Error:", err);
        data = { error: err.message || "Failed to fetch source." };
    }

    // 3. Apply VS Code Highlighting
    display.innerHTML = syntaxHighlightJSON(data);
};

// --- Sub-Tab Hijack Restoration (v1.35.68 Final) ---
// --- Unified Sidebar Management (v1.37.03 Restoration) ---

/**
 * Global Sidebar View Switcher
 * Manages transitions between Details, Health, Recovery, and Media Tools.
 */
window.switchSidebarView = function(viewId) {
    if (typeof mwv_trace === 'function') mwv_trace('SIDEBAR', 'SWITCH-VIEW', { view: viewId });
    console.log(`[SIDEBAR] Switching view to: ${viewId}`);

    // 1. Update Reiters (Vertical Tabs)
    const reiters = document.querySelectorAll('.side-reiter');
    reiters.forEach(r => {
        r.classList.toggle('active', r.id === `reiter-${viewId}`);
    });

    // 2. Update View Panes
    const views = document.querySelectorAll('.sidebar-view-content');
    views.forEach(v => {
        v.style.display = 'none';
        v.classList.remove('active');
    });

    const target = document.getElementById(`sidebar-view-${viewId}`);
    if (target) {
        target.style.display = 'block';
        target.classList.add('active');
    }

    // 3. Specialized Tab Logic
    if (viewId === 'recovery') {
        console.warn("[RECOVERY] Suite active. Use 'CLEAR FILTERS' if 0 items are visible.");
    }
    
    if (viewId === 'diagnostics' || viewId === 'health') {
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(window.__mwv_last_db_count, undefined, undefined); 
        }
    }

    // 4. Legacy Bridge (v1.35.68)
    if (viewId === 'debug-db') {
        if (typeof renderDebugDatabase === 'function') renderDebugDatabase();
    } else if (viewId === 'tests') {
        if (typeof loadTestSuites === 'function') loadTestSuites();
    }
};

/**
 * Diagnostics Initialization (v1.37.02/03)
 */
function initDiagnostics() {
    if (typeof mwv_trace === 'function') mwv_trace('DIAG', 'INIT');
    console.log("Diagnostics: Initializing 7-point professional HUD logic...");
    
    // Start PID/Uptime polling
    if (typeof refreshStartupInfo === 'function') {
        refreshStartupInfo();
        setInterval(refreshStartupInfo, 10000);
    }
}

// Ensure init runs on load
window.addEventListener('DOMContentLoaded', initDiagnostics);

// Legacy Hijack Restoration
setTimeout(() => {
    if (typeof window.switchDiagnosticsView === 'function') {
        const originalSwitchDiagnosticsView = window.switchDiagnosticsView;
        window.switchDiagnosticsView = function(viewId) {
            window.switchSidebarView(viewId);
            if (typeof originalSwitchDiagnosticsView === 'function') {
                originalSwitchDiagnosticsView(viewId);
            }
        };
    }
}, 500);

/**
 * Real-time Console Log Stream for Debug Tab
 */
window.appendDebugLog = function(msg) {
    // Add to buffer
    window.debugLogBuffer.push(msg);
    if (window.debugLogBuffer.length > 1000) window.debugLogBuffer.shift();
    
    // Only update UI if we are in the Debug tab to save performance
    const consoleEl = document.getElementById('debug-console-output');
    if (consoleEl && consoleEl.offsetParent !== null) {
        updateLogFilters();
    }
};

window.updateLogFilters = function() {
    const consoleEl = document.getElementById('debug-console-output');
    const levelFilter = document.getElementById('debug-log-level-filter')?.value || 'ALL';
    const searchFilter = document.getElementById('debug-log-search')?.value.toLowerCase() || '';
    const counterEl = document.getElementById('debug-log-counter');
    
    if (!consoleEl) return;

    const filtered = window.debugLogBuffer.filter(msg => {
        const matchesLevel = (levelFilter === 'ALL') || (msg.includes(`[${levelFilter}]`));
        const matchesSearch = !searchFilter || msg.toLowerCase().includes(searchFilter);
        return matchesLevel && matchesSearch;
    });

    // Render filtered logs
    consoleEl.innerText = filtered.join('\n');
    consoleEl.scrollTop = consoleEl.scrollHeight;
    
    if (counterEl) {
        counterEl.innerText = `Visible: ${filtered.length} / ${window.debugLogBuffer.length}`;
    }
};

window.clearDebugConsole = function() {
    window.debugLogBuffer = [];
    updateLogFilters();
};

/**
 * Force-syncs the entire log history from the backend.
 */
window.refreshDebugLogs = async function() {
    try {
        if (typeof eel !== 'undefined' && eel.get_debug_console) {
            const logs = await eel.get_debug_console()();
            window.debugLogBuffer = logs.split('\n');
            updateLogFilters();
        }
    } catch (err) {
        console.error("refreshDebugLogs Error:", err);
    }
}

// --- SYSTEM HEALTH DIAGNOSTICS ---

/**
 * Run all automated tests for the System Health view.
 */
window.runAllTestsUI = async function() {
    clearDiagnosticsUI();
    const btn = document.getElementById('diag-main-action-btn');
    if (btn) {
        btn.disabled = true;
        btn.classList.add('loading');
    }

    try {
        await Promise.all([
            checkConnectivity(),
            checkMediaPipeline(),
            checkDatabaseHealth()
        ]);
        if (typeof showToast === 'function') showToast("Diagnose-Scan abgeschlossen.", "success");
    } catch (e) {
        console.error("runAllTestsUI Error:", e);
    } finally {
        if (btn) {
            btn.disabled = false;
            btn.classList.remove('loading');
        }
    }
};

window.clearDiagnosticsUI = function() {
    ['diag-conn-list', 'diag-playback-list', 'diag-fs-list'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerHTML = '';
    });
    const resultsPane = document.getElementById('diagnostics-results-pane');
    if (resultsPane) {
        resultsPane.innerHTML = '';
        resultsPane.style.display = 'none';
    }
};

async function checkConnectivity() {
    const list = document.getElementById('diag-conn-list');
    if (!list) return;

    addDiagItem(list, 'Eel Backend', 'pending');
    addDiagItem(list, 'HTTP Server', 'pending');

    // 1. Eel Ping
    try {
        if (typeof eel !== 'undefined' && eel.api_ping) {
            await eel.api_ping(Date.now(), 0)();
            updateDiagItem(list, 'Eel Backend', 'success', 'Verbunden (WebSocket OK)');
        } else {
            updateDiagItem(list, 'Eel Backend', 'error', 'Eel nicht definiert');
        }
    } catch (e) {
        updateDiagItem(list, 'Eel Backend', 'error', e.message);
    }

    // 2. Bottle Ping
    try {
        const start = performance.now();
        const res = await fetch('/health', { cache: 'no-store' });
        const lat = (performance.now() - start).toFixed(1);
        if (res.ok) {
            updateDiagItem(list, 'HTTP Server', 'success', `Aktiv (${lat}ms)`);
        } else {
            updateDiagItem(list, 'HTTP Server', 'error', `HTTP ${res.status}`);
        }
    } catch (e) {
        updateDiagItem(list, 'HTTP Server', 'error', 'Offline / Connection Refused');
    }
}

async function checkMediaPipeline() {
    const list = document.getElementById('diag-playback-list');
    if (!list) return;

    addDiagItem(list, 'Video.js Engine', 'pending');
    addDiagItem(list, 'Audio Pipeline', 'pending');

    // 1. Video.js check
    if (typeof videojs !== 'undefined') {
        updateDiagItem(list, 'Video.js Engine', 'success', 'Version ' + (videojs.VERSION || '8.x'));
    } else {
        updateDiagItem(list, 'Video.js Engine', 'error', 'Nicht geladen (CDN fail?)');
    }

    // 2. Audio Pipeline
    const audio = document.getElementById('native-html5-audio-pipeline-element');
    if (audio) {
        const state = audio.readyState > 0 ? 'Bereit' : 'Initialisiert';
        updateDiagItem(list, 'Audio Pipeline', 'success', state);
    } else {
        updateDiagItem(list, 'Audio Pipeline', 'error', 'DOM Element fehlt');
    }
}

// UI Helpers for list items moved to sidebar_controller or kept as utility below

async function checkDatabaseHealth() {
    const list = document.getElementById('diag-fs-list');
    addDiagItem(list, 'SQLite Storage', 'pending');
    addDiagItem(list, 'Item Map Cache', 'pending');

    try {
        if (typeof eel !== 'undefined' && eel.get_debug_stats) {
            const stats = await eel.get_debug_stats()();
            updateDiagItem(list, 'SQLite Storage', 'success', `${stats.total_items || 0} Objekte indiziert`);
            updateDiagItem(list, 'Item Map Cache', 'success', stats.pid ? `Backend PID: ${stats.pid}` : 'Aktiv');
        } else {
            updateDiagItem(list, 'SQLite Storage', 'warn', 'Eel Backend antwortet nicht');
        }
    } catch (e) {
        updateDiagItem(list, 'SQLite Storage', 'error', e.message);
    }
}

/**
 * UI Helpers for list items
 */
function addDiagItem(list, name, status) {
    const item = document.createElement('div');
    item.className = 'diag-item';
    item.dataset.name = name;
    item.style.display = 'flex';
    item.style.justifyContent = 'space-between';
    item.style.fontSize = '12px';
    item.style.padding = '4px 0';
    item.innerHTML = `
        <span style="color: var(--text-secondary);">${name}</span>
        <span class="status-val" style="font-weight: 700; color: #777;">${status}...</span>
    `;
    list.appendChild(item);
}

function updateDiagItem(list, name, status, details) {
    const items = list.querySelectorAll('.diag-item');
    let target = null;
    items.forEach(i => { if (i.dataset.name === name) target = i; });
    
    if (target) {
        const statusEl = target.querySelector('.status-val');
        if (statusEl) {
            statusEl.innerText = details || status.toUpperCase();
            if (status === 'success') statusEl.style.color = '#2ecc71';
            else if (status === 'error') statusEl.style.color = '#e74c3c';
            else if (status === 'warn') statusEl.style.color = '#f1c40f';
        }
    }
}

// --- TAB RENDERING: TOOLS ---
window.renderToolsDashboard = function() {
    const container = document.getElementById('tools-dashboard-panel');
    if (container) console.log("Tools Dashboard: Initialized");
};

// Startup health check fallback
setTimeout(() => { 
    if (typeof eel !== "undefined" && typeof eel.report_spawn === 'function') {
        eel.report_spawn()(() => console.log("Diagnostics: Startup sync complete."));
    }
}, 5000);

// ==========================================
// DB FOOTER STATUS LIGHT & KONSOLE POPUP
// ==========================================

setInterval(() => {
    const light = document.getElementById('footer-db-light');
    const text = document.getElementById('footer-db-text');
    if (!light || !text) return;

    const dbItems = window.__mwv_last_db_count || 0;
    const uiItems = (window.allLibraryItems || []).length;
    
    if (dbItems > 0 && uiItems > 0) {
        light.style.backgroundColor = '#2ecc71';
        light.style.boxShadow = '0 0 5px #2ecc71';
        text.innerText = 'Synced';
        text.style.color = '#2ecc71';
    } else if (dbItems > 0 && uiItems === 0) {
        light.style.backgroundColor = '#f1c40f'; // Yellow
        light.style.boxShadow = '0 0 5px #f1c40f';
        text.innerText = 'Nicht Gemigriert';
        text.style.color = '#f1c40f';
    } else {
        light.style.backgroundColor = '#e74c3c'; // Red
        light.style.boxShadow = '0 0 5px #e74c3c';
        text.innerText = 'DB Leer';
        text.style.color = '#e74c3c';
    }
}, 1000);

window.showConsolePopup = async function() {
    console.log("[Konsole] Requesting konsole payload...");
    const oldModal = document.getElementById('konsole-modal');
    if (oldModal) oldModal.remove();

    const modal = document.createElement('div');
    modal.id = 'konsole-modal';
    modal.style.cssText = `
        position: fixed; top: 10vh; left: 10vw; width: 80vw; height: 80vh;
        background: rgba(10, 10, 12, 0.95); border-radius: 12px; border: 1px solid var(--border-color);
        z-index: 10000; box-shadow: 0 20px 50px rgba(0,0,0,0.8); backdrop-filter: blur(10px);
        display: flex; flex-direction: column; overflow: hidden;
    `;
    
    const header = document.createElement('div');
    header.style.cssText = 'padding: 15px 20px; background: rgba(255,255,255,0.05); display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--border-color);';
    header.innerHTML = `
        <h2 style="margin: 0; color: #fff; font-size: 1.2em; display: flex; align-items: center; gap: 10px;">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="4 17 10 11 4 5"/><line x1="12" y1="19" x2="20" y2="19"/></svg>
            System Konsole
        </h2>
        <button onclick="document.getElementById('konsole-modal').remove()" style="background: transparent; border: none; color: #fff; cursor: pointer; opacity: 0.7; font-size: 18px;">&times;</button>
    `;
    
    let logsCtn = null;

    if (window.MWV_VERSION) {
        logsCtn = document.getElementById('diagnostic-log-terminal');
    }

    const pre = document.createElement('pre');
    pre.id = 'konsole-logs-content';
    pre.style.cssText = 'padding: 20px; margin: 0; flex: 1; overflow: auto; color: #a0a0a0; font-family: "JetBrains Mono", monospace; font-size: 12px; white-space: pre-wrap; word-wrap: break-word; line-height: 1.4;';
    pre.innerText = "Lade Konsole...";
    
    modal.appendChild(header);
    modal.appendChild(pre);
    document.body.appendChild(modal);

    try {
        if (typeof eel !== 'undefined' && eel.get_konsole) {
            const res = await eel.get_konsole()();
            pre.innerText = res.logs || "Keine Logs vorhanden.";
            pre.scrollTop = pre.scrollHeight;
        } else {
            pre.innerText = "Error: eel.get_konsole not found.";
        }
    } catch(e) {
        pre.innerText = "Error loading konsole: " + e.message;
    }
};

/**
 * showFlagsModal() - Displays a interactive modal for backend debug flags.
 * Allows individual toggle and master ON/OFF controls.
 */
window.showFlagsModal = async function() {
    console.log("[Flags] Fetching current debug flags...");
    const oldModal = document.getElementById('flags-modal');
    if (oldModal) oldModal.remove();

    const modal = document.createElement('div');
    modal.id = 'flags-modal';
    modal.style.cssText = `
        position: fixed; top: 15vh; left: 25vw; width: 50vw; max-height: 70vh;
        background: rgba(15, 15, 20, 0.98); border-radius: 16px; border: 1px solid var(--border-color);
        z-index: 10001; box-shadow: 0 40px 100px rgba(0,0,0,0.9); backdrop-filter: blur(20px);
        display: flex; flex-direction: column; overflow: hidden;
    `;

    const header = document.createElement('div');
    header.style.cssText = 'padding: 20px 25px; background: rgba(233, 30, 99, 0.1); display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(233, 30, 99, 0.2);';
    header.innerHTML = `
        <h2 style="margin: 0; color: #e91e63; font-size: 1.3em; font-weight: 800; display: flex; align-items: center; gap: 12px;">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1z"/><line x1="4" y1="22" x2="4" y2="15"/></svg>
            Debug Flags Orchestrator
        </h2>
        <button onclick="document.getElementById('flags-modal').remove()" style="background: transparent; border: none; color: #fff; cursor: pointer; opacity: 0.6; font-size: 22px;">&times;</button>
    `;

    const content = document.createElement('div');
    content.style.cssText = 'padding: 25px; flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 12px;';

    const masterControls = document.createElement('div');
    masterControls.style.cssText = 'display: flex; gap: 10px; margin-bottom: 10px; padding-bottom: 15px; border-bottom: 1px solid rgba(255,255,255,0.05);';
    masterControls.innerHTML = `
        <button onclick="eel.set_all_debug_flags(true)(); showFlagsModal(); showStatusNotification('All Flags ENABLED', 'warn');" class="tab-btn active" style="background: #2ecc71; border: none; flex: 1; justify-content: center; font-size:11px; font-weight:800;">ENABLE ALL</button>
        <button onclick="eel.set_all_debug_flags(false)(); showFlagsModal(); showStatusNotification('All Flags DISABLED', 'info');" class="tab-btn" style="background: #e74c3c; border: none; flex: 1; justify-content: center; font-size:11px; font-weight:800; color:white;">DISABLE ALL</button>
    `;

    modal.appendChild(header);
    content.appendChild(masterControls);
    modal.appendChild(content);
    document.body.appendChild(modal);

    try {
        if (typeof eel !== 'undefined' && eel.get_debug_flags) {
            const flags = await eel.get_debug_flags()();
            Object.entries(flags).forEach(([key, val]) => {
                const row = document.createElement('div');
                row.style.cssText = 'display: flex; justify-content: space-between; align-items: center; padding: 12px 18px; background: rgba(255,255,255,0.03); border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);';
                row.innerHTML = `
                    <span style="font-size: 13px; font-weight: 700; color: var(--text-primary); text-transform: uppercase; letter-spacing: 0.5px;">${key.replace(/_/g, ' ')}</span>
                    <label class="switch sm" style="transform: scale(0.9);">
                        <input type="checkbox" ${val ? 'checked' : ''} onchange="eel.set_debug_flag('${key}', this.checked)(); showStatusNotification('Flag ${key} updated', 'info');">
                        <span class="slider"></span>
                    </label>
                `;
                content.appendChild(row);
            });
        }
    } catch(e) {
        content.innerHTML += `<div style="color: #ff5252; padding: 20px; font-weight: 700;">Error: ${e.message}</div>`;
    }
};

/**
 * showStatusNotification(msg, type) - Shows a brief notification pill in the footer.
 */
window.showStatusNotification = function(msg, type = 'info') {
    const anchor = document.getElementById('footer-status-pills');
    if (!anchor) return;

    const pill = document.createElement('div');
    pill.style.cssText = `
        padding: 4px 12px; border-radius: 20px; font-size: 10px; font-weight: 800;
        text-transform: uppercase; letter-spacing: 0.5px; animation: slideUp 0.3s ease-out;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3); white-space: nowrap;
    `;

    if (type === 'success') { pill.style.background = '#2ecc71'; pill.style.color = '#fff'; }
    else if (type === 'warn') { pill.style.background = '#f1c40f'; pill.style.color = '#000'; }
    else if (type === 'error') { pill.style.background = '#e74c3c'; pill.style.color = '#fff'; }
    else { pill.style.background = 'var(--accent-color)'; pill.style.color = '#fff'; }

    pill.innerText = msg;
    anchor.appendChild(pill);

    setTimeout(() => {
        pill.style.opacity = '0';
        pill.style.transform = 'translateY(10px)';
        pill.style.transition = 'all 0.5s ease-in';
        setTimeout(() => pill.remove(), 500);
    }, 3000);
};
/**
 * Sync Anchor Orchestrator (v1.35.99 Unified technical layer)
 * Updates both the minimal footer (total count) and the detailed sidebar (full parity).
 */
function updateSyncAnchor(dbCount, guiCount, fsSize = null) {
    const sidebarAnchor = document.getElementById('sb-parity-anchor');
    const footerDbCount = document.getElementById('footer-db-count');
    
    // Persist counts for redundant updates
    if (dbCount !== undefined) window.__mwv_last_db_count = dbCount;
    if (guiCount !== undefined) window.__mwv_last_gui_count = guiCount;
    if (fsSize !== null) window.__mwv_last_fs_size = fsSize;

    const finalDb = window.__mwv_last_db_count || 0;
    const finalGui = (guiCount !== undefined) ? guiCount : (typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : 0);
    const finalFsSize = window.__mwv_last_fs_size || 0;

    // Formatting filesystem size for the detailed sidebar
    let sizeStr = "--";
    if (finalFsSize > 0) {
        if (finalFsSize > 1024 * 1024) sizeStr = (finalFsSize / (1024 * 1024)).toFixed(1) + "MB";
        else if (finalFsSize > 1024) sizeStr = (finalFsSize / 1024).toFixed(1) + "KB";
        else sizeStr = finalFsSize + "B";
    }

    const fullParity = `[FS: ${sizeStr} | DB: ${finalDb} | GUI: ${finalGui}]`;

    // 1. Sidebar: High-resolution parity audit (v1.37.01)
    if (sidebarAnchor) {
        sidebarAnchor.innerText = fullParity;
        const isParityError = (parseInt(finalDb) !== parseInt(finalGui));
        sidebarAnchor.style.color = isParityError ? '#e74c3c' : 'var(--accent-color)';
    }

    // 1b. Global Diagnostics Sidebar Sync (v1.37.05)
    const sbDbCount = document.getElementById('diag-db-count-sidebar');
    const sbGuiCount = document.getElementById('diag-gui-count-sidebar');
    if (sbDbCount) sbDbCount.innerText = finalDb;
    if (sbGuiCount) sbGuiCount.innerText = finalGui;

    // 2. Footer: Minimalist DB indicator
    if (footerDbCount) {
        footerDbCount.innerText = finalDb;
    }

    // 3. HUD LED Logic & 7-Point Hover Metrics (v1.37.16 Pulsar Upgrade)
    const hudFe = document.getElementById('hud-fe');
    const hudBe = document.getElementById('hud-be');
    const hudDb = document.getElementById('hud-db');

    const lastSync = new Date().toLocaleTimeString();
    const pid = window.__mwv_last_pid || '--';
    const upTime = window.__mwv_last_uptime || '--';

    // Helper: Get high-density trace for tooltip
    const getModuleTrace = (moduleKey) => {
        const cache = (window.__sentinel_module_cache && window.__sentinel_module_cache[moduleKey]) || [];
        if (cache.length === 0) return "No forensic events captured.";
        return cache.map(line => `> ${line}`).join('\n');
    };

    if (hudFe) {
        const isFeHealthy = (finalGui > 0);
        const trace = getModuleTrace('FE');
        hudFe.className = `hud-group ${isFeHealthy ? 'active' : 'error'}`;
        hudFe.setAttribute('data-hud-metrics', 
            `[FRONTEND FORENSICS]\n` +
            `PID: ${pid} | UP: ${upTime}\n` +
            `STATUS: ${isFeHealthy ? 'Synchronized' : 'Empty'}\n` +
            `ITEMS: ${finalGui} (GUI)\n` +
            `------------------------\n` +
            `LAST TRACE EVENTS:\n${trace}`
        );
    }

    if (hudBe) {
        const isBeHealthy = (typeof eel !== 'undefined');
        const trace = getModuleTrace('BE');
        hudBe.className = `hud-group ${isBeHealthy ? 'active' : 'error'}`;
        hudBe.setAttribute('data-hud-metrics', 
            `[BACKEND FORENSICS]\n` +
            `PID: ${pid} | UP: ${upTime}\n` +
            `STATUS: ${isBeHealthy ? 'Socket Alive' : 'Disconnected'}\n` +
            `SOCKET: Established (Eel)\n` +
            `------------------------\n` +
            `LAST TRACE EVENTS:\n${trace}`
        );
    }

    if (hudDb) {
        const isDbHealthy = (finalDb > 0);
        const dbCache = (window.__sentinel_module_cache && window.__sentinel_module_cache.DB) || [];
        const isScanning = dbCache.some(l => l.includes('SCAN') || l.includes('SYNC') || l.includes('RECOVER'));
        
        const trace = getModuleTrace('DB');
        let stateClass = isDbHealthy ? 'active' : 'warning';
        if (isScanning) stateClass = 'scanning';
        
        hudDb.className = `hud-group ${stateClass}`;
        hudDb.setAttribute('data-hud-metrics', 
            `[DATABASE FORENSICS]\n` +
            `PID: ${pid} | UP: ${upTime}\n` +
            `STATUS: ${isScanning ? 'Active Scan/Sync' : (isDbHealthy ? 'SQLite Online' : 'No Data')}\n` +
            `ROWS: ${finalDb} (DB)\n` +
            `------------------------\n` +
            `LAST TRACE EVENTS:\n${trace}`
        );
    }
}

/**
 * Periodically refreshes backend startup info (PID, Boot, Uptime)
 * v1.37.01 Restoration
 */
window.refreshStartupInfo = function() {
    if (typeof eel === 'undefined') return;
    
    eel.get_startup_info()((data) => {
        if (!data) return;
        const pidEl = document.getElementById('diag-pid');
        const bootEl = document.getElementById('diag-boot');
        const upEl = document.getElementById('diag-up');

        window.__mwv_last_pid = data.pid;
        if (pidEl) pidEl.innerText = data.pid || '--';
        if (bootEl) bootEl.innerText = `${data.boot_duration_sec}s` || '--s';
        
        // Calculate uptime string
        if (upEl) {
            const sec = Math.floor(data.boot_duration_sec);
            const m = Math.floor(sec / 60);
            const h = Math.floor(m / 60);
            const upStr = h > 0 ? `${h}h ${m % 60}m` : `${m}m ${sec % 60}s`;
            upEl.innerText = upStr;
            window.__mwv_last_uptime = upStr;
        }
    });
};

// Auto-start polling
setInterval(window.refreshStartupInfo, 10000);
setTimeout(window.refreshStartupInfo, 1000);

// Expose to window
window.updateSyncAnchor = updateSyncAnchor;

/**
 * Diagnostic: Hide DB Toggle (v1.35.68 Recovery)
 */
window.__mwv_hide_db = false;
function toggleHideDb() {
    window.__mwv_hide_db = !window.__mwv_hide_db;
    const msg = `[DIAG] Hide DB Items: ${window.__mwv_hide_db ? 'ON' : 'OFF'}`;
    console.warn(msg);
    if (typeof showStatusNotification === 'function') showStatusNotification(msg, 'info');
    if (typeof renderLibrary === 'function') renderLibrary();
}

// Expose to window
window.toggleHideDb = toggleHideDb;

/**
 * Diagnostic: Notify Change (v1.35.68 Overhaul)
 * Provides explicit, non-abbreviated labels for all diagnostic controls.
 */
function notifyDiagnosticChange(btnId, type, state) {
    let label = type;
    let desc = "";

    switch(type) {
        case 'DIAG': 
            label = "Nuclear Recovery Suite"; 
            desc = " (S1-S15 Stages)"; 
            break;
        case 'NATV': 
            label = "Native Player-Engine"; 
            desc = " (Kein Transcoding)"; 
            break;
        case 'HIDB': 
            label = "Hide Real DB Items"; 
            desc = " (Mock Flow Test)"; 
            break;
        case 'RAW':  
            label = "Rohdaten-Modus";    
            desc = " (Kategorie-Filter deaktiviert)"; 
            break;
        case 'BYPS': 
            label = "DB-Bypass";         
            desc = " (Test-Mocks aktiv)"; 
            break;
    }

    const msg = `${label}${desc}: ${state ? 'AKTIVIERT' : 'DEAKTIVIERT'}`;
    if (typeof showStatusNotification === 'function') {
        showStatusNotification(msg, state ? 'success' : 'info');
    }
}
window.notifyDiagnosticChange = notifyDiagnosticChange;

/**
 * Diagnostic: Raw Mode Toggle
 */
async function toggleRawMode() {
    const newState = !window.CONFIG.raw_mode;
    window.CONFIG.raw_mode = newState;
    window.__mwv_raw_mode = newState; // Keep legacy compat
    localStorage.setItem('mwv_raw_mode', newState);
    
    notifyDiagnosticChange(null, 'RAW', newState);
    
    if (typeof eel !== 'undefined' && eel.set_global_config) {
        eel.set_global_config('raw_mode', newState)();
    }
    
    if (typeof loadLibrary === 'function') {
        loadLibrary(0, newState);
    }
}
window.toggleRawMode = toggleRawMode;

/**
 * Diagnostic: DB Bypass Toggle
 */
function toggleBypassDb() {
    const newState = !window.CONFIG.bypass_db;
    window.CONFIG.bypass_db = newState;
    window.__mwv_bypass_db = newState; // Keep legacy compat
    localStorage.setItem('mwv_bypass_db', newState);
    
    notifyDiagnosticChange(null, 'BYPS', newState);
    
    if (typeof eel !== 'undefined' && eel.set_global_config) {
        eel.set_global_config('bypass_db', newState)();
    }
    
    if (newState) {
        if (typeof bootstrapMockQueue === 'function') bootstrapMockQueue();
    } else {
        if (typeof loadLibrary === 'function') loadLibrary();
    }
}
window.toggleBypassDb = toggleBypassDb;

/**
 * Autonomous Self-Test Engine (v1.35.68)
 * Performs a 7-point integrity check using Sync Anchors.
 */
async function runAutonomousSelfTest() {
    // --- ADDED v1.35.68 Stage 10: Queue Parity Audit ---
    const libCount = (typeof allLibraryItems !== 'undefined') ? allLibraryItems.length : 0;
    const queueCount = (typeof currentPlaylist !== 'undefined') ? currentPlaylist.length : 0;
    const isRaw = window.__mwv_raw_mode === true;
    
    if (isRaw && queueCount === libCount && libCount > 0) {
        mwv_trace_render('DIAG-AUDIT', 'PASS', { stage: 10, title: "Queue Parity", detail: "JS-to-Queue Sync SUCCESS." });
    } else if (isRaw && queueCount < libCount) {
        mwv_trace_render('DIAG-AUDIT', 'WARN', { stage: 10, title: "Queue Parity", detail: `Mismatch! Lib: ${libCount}, Queue: ${queueCount}. Check filters.` });
    } else {
        mwv_trace_render('DIAG-AUDIT', 'INFO', { stage: 10, title: "Queue Parity", detail: `Status: ${queueCount} in Queue.` });
    }

    console.info(">>> [Self-Test] Completed 10-Point Audit.");

    console.warn(">>> [Self-Test] Initiating 7-Point Integrity Audit...");
    if (typeof showStatusNotification === 'function') {
        showStatusNotification('SELF-TEST: Audit gestartet...', 'info');
    }

    const results = { pass: 0, fail: 0, details: [] };
    const dbCount = window.__mwv_last_db_count || 0;

    // Check 1: Parity (Black Hole Check)
    if (dbCount > 0 && guiCount === 0 && !window.__mwv_hide_db) {
        results.fail++;
        results.details.push("KRITISCH: Datenbank hat Daten, aber GUI ist leer (BLACK HOLE)!");
    } else {
        results.pass++;
    }

    // Check 2: Bypass Stability
    if (window.__mwv_bypass_db && queueCount !== 3) {
        results.fail++;
        results.details.push("WARNUNG: Bypass ist an, aber Queue hat keine 3 Mocks.");
    } else {
        results.pass++;
    }

    // Check 3: Raw Mode Parity
    if (window.__mwv_raw_mode && guiCount !== dbCount) {
        results.fail++;
        results.details.push("FEHLER: Raw Mode aktiv, aber GUI/DB Parität fehlt.");
    } else {
        results.pass++;
    }

    // Check 4: Anchor Sync
    const anchor = document.getElementById('footer-sync-anchor');
    if (!anchor || anchor.innerText.includes('--')) {
        results.fail++;
        results.details.push("STALL: Sync Anker ist eingefroren.");
    } else {
        results.pass++;
    }

    // Final Report
    const status = results.fail === 0 ? 'success' : 'error';
    const msg = `AUDIT ABGESCHLOSSEN: ${results.pass}/4 Pass. ${results.details[0] || 'System Nominal'}`;
    
    if (typeof showStatusNotification === 'function') {
        showStatusNotification(msg, status);
    }
    console.log(`[Self-Test] Results:`, results);
}
window.runAutonomousSelfTest = runAutonomousSelfTest;

/**
 * Background Sync Watchdog
 * Monitors parity every 30s.
 */
function checkSyncParity() {
    const dbCount = window.__mwv_last_db_count || 0;
    const guiCount = (typeof allLibraryItems !== 'undefined') ? allLibraryItems.length : 0;
    const light = document.getElementById('footer-db-light');
    
    if (!light) return;

    if (dbCount > 0 && guiCount === 0 && !window.__mwv_hide_db && !window.__mwv_bypass_db) {
        light.style.background = '#e74c3c'; // Red (CRITICAL)
        light.title = "CRITICAL: Sync Parity Lost (Black Hole)";
    } else if (window.__mwv_bypass_db || window.__mwv_raw_mode) {
        light.style.background = '#f1c40f'; // Yellow (Diag Mode)
        light.title = "Diagnostic Mode Active";
    } else {
        light.style.background = '#2ecc71'; // Green (Healthy)
        light.title = "Sync Parity Healthy";
    }
}
setInterval(checkSyncParity, 30000);
setTimeout(checkSyncParity, 2000); 

/**
 * Sync Anchor Initializer
 * Ensures the anchor shows something other than '--' even if sync hangs.
 */
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(window.__mwv_last_db_count || 0, (typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : 0));
        }
    }, 1000);
});
/**
 * Deep Data Flow Probe (v1.35.68 Recovery)
 */
async function probeDataFlow() {
    // Stage 1 (Mock) is the starting baseline
    await auditSwitchStage(1);
}
window.probeDataFlow = probeDataFlow;

/**
 * Audit Orchestrator (v1.35.97 Overhaul)
 * Allows cycling through stages: 1=Mock, 2=Raw, 3=Filtered
 */
async function auditSwitchStage(stage) {
    console.warn(`[BD-AUDIT] Switching to Stage ${stage}...`);
    window.__mwv_audit_stage = stage;
    
    // Auto-Navigation to Diagnostics Tab for visibility (v1.35.97)
    if (typeof switchMainCategory === 'function') {
        const diagBtn = document.querySelector('.nav-item[onclick*="diagnostics"]');
        switchMainCategory('diagnostics', diagBtn);
    }
    
    if (typeof loadLibrary === 'function') {
        await loadLibrary();
        
        // After load, check the audit metadata for Stage 2 & 3 specifically (v1.35.99)
        const lib = window.__mwv_debug_library || {};
        const audit = lib.audit || {};
        const fs = audit.fs || {};
        
        // Update both Footer (DB Count) and Sidebar (Full Parity)
        const reasonsViewport = document.getElementById('sb-dropped-reasons-viewport');
        if (reasonsViewport) {
            const la = audit.logic_audit || {};
            const dr = la.dropped_reasons || {};
            
            if (Object.keys(dr).length > 0 && la.dropped_total > 0) {
                let html = `<div style="color: #e74c3c; font-weight: 800; margin-bottom: 5px;">DROPPED: ${la.dropped_total} Items</div>`;
                for (const [reason, count] of Object.entries(dr)) {
                    if (count > 0) {
                        html += `<div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(0,0,0,0.05); padding: 2px 0;">
                                    <span>${reason.replace('_mismatch', '')}</span>
                                    <span style="font-weight: 800;">${count}</span>
                                 </div>`;
                    }
                }
                reasonsViewport.innerHTML = html;
            } else {
                reasonsViewport.innerHTML = `<div style="color: #2ecc71;">PASS: All ${lib.db_count || 0} items kept.</div>`;
            }
        }

        if (fs.exists !== undefined) {
            const fsMsg = `[FS-AUDIT] Path: ${audit.path} | Exists: ${fs.exists} | Size: ${fs.size} bytes | PID: ${audit.pid}`;
// ... Log it ...
            console.warn(fsMsg);
            if (fs.size === 0) console.error("[FS-AUDIT] CRITICAL: DB FILE IS EMPTY (0 bytes)!");
            if (fs.size === -1) console.error("[FS-AUDIT] CRITICAL: DB FILE NOT FOUND!");
        }

        if (typeof showStatusNotification === 'function') {
            const labels = { 
                1: "STAGE 1: MOCKS (GUI TEST)", 
                2: "STAGE 2: SQLite ACCESS (RAW)", 
                3: "STAGE 3: NORMALIZATION (FILTERED)" 
            };
            showStatusNotification(`AUDIT: ${labels[stage]}`, 'warn');
        }
    }
}

/**
 * Visual feedback for relocated diagnostic buttons (v1.35.97)
 */
function updateDiagBtnState(btn, isActive) {
    if (!btn) return;
    btn.style.background = isActive ? 'var(--accent-color)' : 'var(--bg-secondary)';
    btn.style.color = isActive ? '#fff' : 'var(--text-secondary)';
    btn.style.borderColor = isActive ? 'var(--accent-color)' : 'var(--border-color)';
    btn.classList.toggle('active', isActive);
}

// Initial state sync for buttons (v1.37.06 Persistence)
function syncDiagBtnStates() {
    const flags = {
        'DIAG': (localStorage.getItem('mwv_diagnostic_mode') === 'true' || (typeof RecoveryManager !== 'undefined' && RecoveryManager.isNuclear)),
        'HIDB': (localStorage.getItem('mwv_hide_db') === 'true' || window.__mwv_hide_db),
        'RAW': (localStorage.getItem('mwv_raw_mode') === 'true' || window.__mwv_raw_mode),
        'BYPS': (localStorage.getItem('mwv_bypass_db') === 'true' || window.__mwv_bypass_db),
        'NATV': (localStorage.getItem('mwv_force_native') === 'true' || window.__mwv_natv_mode),
        'TEST': false // Placeholder
    };
    
    // Push back into runtime config if missing
    if (flags.RAW) { window.CONFIG.raw_mode = true; window.__mwv_raw_mode = true; }
    if (flags.BYPS) { window.CONFIG.bypass_db = true; window.__mwv_bypass_db = true; }

    Object.entries(flags).forEach(([key, active]) => {
        // Sync Player Sidebar Buttons (Classic)
        updateDiagBtnState(document.getElementById(`sb-diag-btn-${key}`), active);
        updateDiagBtnState(document.getElementById(`diag-btn-${key}`), active);
        
        // Sync Global Overlay Buttons (v1.37.05)
        const overlayBtn = document.getElementById(`flag-btn-${key}`);
        if (overlayBtn) {
            overlayBtn.classList.toggle('active', active);
        }

        // Sync Footer HUD Buttons (v1.37.06)
        const footerBtn = document.getElementById(`footer-btn-${key}`);
        if (footerBtn) {
            footerBtn.classList.toggle('active', active);
            footerBtn.style.color = active ? 'var(--accent-color)' : '#eee';
            footerBtn.style.borderColor = active ? 'var(--accent-color)' : 'rgba(255,255,255,0.1)';
        }
    });
}

// Modularized into sidebar_controller.js (v1.37.14)
// function renderLogicAuditSummary(logicAudit) { ... }

/**
 * Emergency recovery: Bypasses all backend filters to hydrate the library.
 */
async function forceSyncAll() {
    if (typeof showStatusNotification === 'function') {
        showStatusNotification('Nuclear Recovery: Bypassing Filters...', 'warn');
    }

    try {
        const result = await eel.force_sync_all()();
        if (result && result.status === 'raw-recovery') {
            // Manually inject into library state
            if (typeof renderLibrary === 'function') {
                renderLibrary(result.media);
            }
            
            // Update sidebar counts
            updateSyncAnchor(result.db_count, result.media.length);
            
            if (typeof showStatusNotification === 'function') {
                showStatusNotification(`RECOVERED: ${result.media.length} items found!`, 'success');
            }
            console.log("[RECOVERY] Filter bypass success:", result.media.length, "items.");
        }
    } catch (e) {
        console.error("[RECOVERY] Force Sync Failed:", e);
    }
}

window.renderLogicAuditSummary = renderLogicAuditSummary;
window.forceSyncAll = forceSyncAll;
window.auditSwitchStage = auditSwitchStage;
window.updateDiagBtnState = updateDiagBtnState;
window.syncDiagBtnStates = syncDiagBtnStates;

// Sync buttons on load
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(syncDiagBtnStates, 2000);
});
