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
                // Restore the "Item DB (Übersicht)" style from screenshot
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
                            <!-- Additional info can go here -->
                        </div>
                    </div>
                `;
            }
            
            if (pidEl) pidEl.innerText = stats.pid || '--';

            const dictType = document.getElementById('debug-dict-select')?.value || 'library';
            const dictData = await eel.get_debug_dict(dictType)();
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
window.debugLogEntries = [];
window.appendDebugLog = function(msg) {
    const consoleEl = document.getElementById('debug-console-output');
    if (!consoleEl) return;

    const entry = document.createElement('div');
    entry.style.marginBottom = '2px';
    
    // Simple color coding based on level
    if (msg.includes('[INFO]')) entry.style.color = '#00ff41';
    else if (msg.includes('[WARN]')) entry.style.color = '#ffcc00';
    else if (msg.includes('[ERROR]')) entry.style.color = '#ff5252';
    else if (msg.includes('[DEBUG]')) entry.style.color = '#00bcff';
    else entry.style.color = '#dcdccc';

    entry.innerText = msg;
    consoleEl.appendChild(entry);
    
    // Auto-scroll to bottom
    consoleEl.scrollTop = consoleEl.scrollHeight;
    
    // Limit buffer
    if (consoleEl.children.length > 500) {
        consoleEl.removeChild(consoleEl.firstChild);
    }
};

window.clearDebugConsole = function() {
    const consoleEl = document.getElementById('debug-console-output');
    if (consoleEl) consoleEl.innerHTML = '';
};

/**
 * Force-syncs the entire log history from the backend.
 */
window.refreshDebugLogs = async function() {
    const consoleEl = document.getElementById('debug-console-output');
    if (!consoleEl) return;
    
    try {
        if (typeof eel !== 'undefined' && eel.get_debug_console) {
            const logs = await eel.get_debug_console()();
            consoleEl.innerText = logs; // Entire history as string
            consoleEl.scrollTop = consoleEl.scrollHeight;
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
