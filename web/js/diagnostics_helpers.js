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
