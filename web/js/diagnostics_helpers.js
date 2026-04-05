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

window.renderDebugDatabase = async function() {
    const statsEl = document.getElementById('debug-db-overview-content');
    const dictEl = document.getElementById('debug-items-json');
    const pidEl = document.getElementById('debug-python-pid');
    
    if (statsEl) statsEl.innerHTML = '<span style="color: var(--accent-color);">Refreshing Database Stats...</span>';
    if (dictEl) dictEl.innerHTML = '<span style="color: #6a1;">Loading Python Dictionary...</span>';

    try {
        if (typeof eel !== 'undefined' && eel.get_debug_stats) {
            const stats = await eel.get_debug_stats()();
            if (statsEl) {
                let categoryHtml = '';
                if (stats.categories) {
                    categoryHtml = Object.entries(stats.categories).map(([k, v]) => `<li>${k}: ${v}</li>`).join('');
                }

                statsEl.innerHTML = `
                    <div style="display: flex; gap: 40px;">
                        <div>
                            <h4 style="margin: 0 0 10px 0; font-size: 1.1em;">Entries: ${stats.total_items || 0}</h4>
                            <ul style="padding-left: 20px; color: var(--text-secondary); line-height: 1.6;">
                                ${categoryHtml || '<li>Keine Daten</li>'}
                            </ul>
                        </div>
                        <div style="min-width: 150px;">
                            <h4 style="margin: 0 0 10px 0; font-size: 1.1em;">Categories:</h4>
                            <div style="font-size: 11px; opacity: 0.7;">DB Health: Synchronized</div>
                        </div>
                    </div>
                `;
            }
            
            if (pidEl) pidEl.innerText = stats.pid || '--';

            const dictType = document.getElementById('debug-dict-select')?.value || 'library';
            let dictData = null;

            // Handle different probe types
            if (dictType === 'env' && eel.get_environment_info) {
                dictData = await eel.get_environment_info()();
            } else if (dictType === 'formats' && eel.get_format_utils_exts) {
                dictData = await eel.get_format_utils_exts()();
            } else if (eel.get_debug_dict) {
                dictData = await eel.get_debug_dict(dictType)();
            }

            if (dictEl) dictEl.innerText = JSON.stringify(dictData, null, 2);
        }
    } catch (err) {
        if (statsEl) statsEl.innerHTML = `<span style="color: #f44;">Error: ${err.message}</span>`;
        console.error("renderDebugDatabase Error:", err);
    }
};

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

async function checkDatabaseHealth() {
    const list = document.getElementById('diag-fs-list');
    if (!list) return;

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
 * Sync Anchor Orchestrator (v1.35.68 Recovery) 
 * Updates the global footer anchor [DB: X | GUI: X] to identify data drops.
 */
function updateSyncAnchor(dbCount, guiCount) {
    const el = document.getElementById('footer-sync-anchor');
    const light = document.getElementById('sync-status');
    if (!el) return;

    // Use current state if not provided
    const finalDb = (dbCount !== undefined) ? dbCount : (window.__mwv_last_db_count || 0);
    const finalGui = (guiCount !== undefined) ? guiCount : (typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : 0);

    el.innerText = `[DB: ${finalDb} | GUI: ${finalGui}]`;

    // Visual Cue: Yellow if 0 items in GUI but items in DB
    if (finalGui === 0 && finalDb > 0) {
        el.style.color = '#f1c40f'; // Warning
        el.style.background = 'rgba(241, 196, 15, 0.1)';
        el.style.borderColor = 'rgba(241, 196, 15, 0.2)';
        if (light) light.style.color = '#f1c40f';
    } else if (finalGui > 0) {
        el.style.color = '#2ecc71'; // Healthy
        el.style.background = 'rgba(46, 204, 113, 0.1)';
        el.style.borderColor = 'rgba(46, 204, 113, 0.2)';
        if (light) light.style.color = '#2ecc71';
    }
}

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
