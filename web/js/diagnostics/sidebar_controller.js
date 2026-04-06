const SENTINEL_MAX_ENTRIES = 100;

// View Information Mapping for the dynamic header
const DIAG_VIEW_INFO = {
    'hydration': { name: 'HYDRATION CHAIN', desc: 'Analyzes media flow from SQL to DOM.' },
    'item-track': { name: 'ITEM JOURNEY', desc: 'Traces a specific file across all layers.' },
    'sentinel': { name: 'SENTINEL LOG', desc: 'Live application event listener.' },
    'debug-db': { name: 'DATABASE OVERVIEW', desc: 'Raw SQLite index & Category statistics.' },
    'logs': { name: 'SYSTEM LOGS', desc: 'Backend console & terminal output stream.' },
    'video-health': { name: 'VIDEO PIPELINE', desc: 'Transcoding and remuxing status.' },
    'recovery': { name: 'NUCLEAR RECOVERY', desc: 'Emergency UI and filter resets.' }
};

function initDiagnosticsSidebar() {
    console.info("[DIAG-CTRL] Initializing Diagnostics Overlay...");
    
    // Default to hydration or stored state
    const lastView = localStorage.getItem('mwv_diag_view') || 'hydration';
    switchDiagnosticsSidebarTab(lastView);
    
    // Sentinel hook for system-wide tracing
    const originalTrace = window.mwv_trace;
    window.mwv_trace = function(tag, stage, data) {
        if (originalTrace) originalTrace(tag, stage, data);
        sentinelPulse(tag, `${stage} - ${JSON.stringify(data)}`);
    };

    sentinelPulse('SYSTEM', 'Diagnostics Overlay Core Loaded.');
    loadSentinelHistory(); // Re-hydrate forensic trace
}

/**
 * Enhanced Tab Switching with Modular & Legacy Support
 */
function switchDiagnosticsSidebarTab(viewId, btn) {
    const info = DIAG_VIEW_INFO[viewId] || { name: viewId.toUpperCase(), desc: '' };
    
    // 1. Update Header Information (Requested)
    const nameEl = document.getElementById('diag-active-view-name');
    const descEl = document.getElementById('diag-active-view-desc');
    if (nameEl) nameEl.innerText = info.name;
    if (descEl) descEl.innerText = info.desc;

    // 2. Update Tab Button Styles (Compact)
    document.querySelectorAll('#global-diagnostics-sidebar .side-reiter').forEach(el => {
        el.classList.remove('active');
        if (el.id === `reiter-${viewId}`) el.classList.add('active');
    });

    // 3. Coordinate Pane Visibility
    document.querySelectorAll('.diag-pane').forEach(p => p.style.display = 'none');
    
    const paneIds = {
        'hydration': 'diag-pane-hydration',
        'item-track': 'diag-pane-item-track',
        'sentinel': 'diag-pane-sentinel',
        'debug-db': 'diag-pane-debug-db',
        'logs': 'diag-pane-logs',
        'video-health': 'diag-pane-video-health',
        'recovery': 'diag-pane-db-resilience'
    };

    if (paneIds[viewId]) {
        const target = document.getElementById(paneIds[viewId]);
        if (target) target.style.display = 'block';

        // Trigger Data Fetchers
        if (viewId === 'hydration') runHydrationAuditProbe();
        if (viewId === 'item-track') renderItemTrackTab();
        if (viewId === 'debug-db' && typeof renderDebugDatabase === 'function') renderDebugDatabase();
        if (viewId === 'logs' && typeof refreshDebugLogs === 'function') refreshDebugLogs();

    } else {
        // Fallback for VID/REC using legacy logic
        const legacyPane = document.getElementById('diag-pane-legacy');
        if (legacyPane) {
            legacyPane.style.display = 'block';
            if (typeof switchDiagnosticsSubView === 'function') switchDiagnosticsSubView(viewId);
        }
    }
    
    localStorage.setItem('mwv_diag_view', viewId);
    sentinelPulse('UI-NAV', `Switched to ${viewId.toUpperCase()}`);
}

/**
 * ITEM TRACKER: High-Performance Probe
 */
function renderItemTrackTab() {
    const container = document.getElementById('diag-item-track-content');
    if (!container || container.innerHTML.includes('diag-item-query')) return; // Already rendered

    container.innerHTML = `
        <div style="display:flex; gap:8px; margin-bottom:15px; background:rgba(255,255,255,0.05); padding:8px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
            <input type="text" id="diag-item-query" placeholder="Teil von Pfad oder Name..." 
                style="flex:1; background:transparent; border:none; color:white; font-size:11px; outline:none;"
                onkeypress="if(event.key==='Enter') performItemJourneyAudit()">
            <button onclick="performItemJourneyAudit()" style="background:#3498db; color:white; border:none; padding:4px 10px; border-radius:4px; font-size:9px; cursor:pointer; font-weight:800;">AUDIT</button>
        </div>
        <div id="diag-item-audit-results"></div>
    `;
}

async function performItemJourneyAudit() {
    const query = document.getElementById('diag-item-query').value;
    const results = document.getElementById('diag-item-audit-results');
    if (!query || !results) return;

    sentinelPulse('AUDIT', `Tracing journey for: ${query}`);
    results.innerHTML = '<div style="font-size:10px; opacity:0.6; padding:10px;">Backend-Probe läuft...</div>';

    try {
        const audit = await eel.audit_specific_item(query)();
        if (audit.status === 'not_found') {
            results.innerHTML = `<div style="color:#e74c3c; font-size:11px; padding:10px; background:rgba(231,76,60,0.1); border-radius:6px;">Fehlgeschlagen: Item nicht in DB gefunden.</div>`;
            return;
        }

        const stages = audit.stages;
        const item = audit.item;

        // Frontend Deep-Probe
        const fe_normalized = (window.allLibraryItems || []).find(i => i.path === item.path);
        const dom_node = document.querySelector(`.grid-item[title*="${item.name}"]`);

        results.innerHTML = `
            <div class="journey-v137">
                <div class="j-step ${stages.db.status === 'ok' ? 'ok' : 'err'}">🗄️ SQL: ${stages.db.status.toUpperCase()}</div>
                <div class="j-step ${stages.models.log.includes('OK') ? 'ok' : 'err'}">🏷️ SSOT: ${stages.models.log}</div>
                <div class="j-step ${stages.backend_filter.status === 'ok' ? 'ok' : 'err'}">⚙️ B-FLTR: ${stages.backend_filter.reason}</div>
                <div class="j-step ${fe_normalized ? 'ok' : 'err'}">🧠 MEM: ${fe_normalized ? 'HYDRATED' : 'MISSING'}</div>
                <div class="j-step ${dom_node ? 'ok' : 'err'}">🖥️ DOM: ${dom_node ? 'RENDERED' : 'HIDDEN'}</div>
            </div>
            <style>
                .journey-v137 { display: flex; flex-direction: column; gap: 4px; margin-top:5px; }
                .j-step { font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 8px; border-radius: 6px; background: rgba(255,255,255,0.02); border: 1px solid rgba(255,255,255,0.05); }
                .j-step.ok { color: #2ecc71; border-left: 3px solid #2ecc71; background: rgba(46,204,113,0.05); }
                .j-step.err { color: #e74c3c; border-left: 3px solid #e74c3c; background: rgba(231,76,60,0.05); }
            </style>
        `;
    } catch (e) {
        results.innerHTML = `<div style="color:#e74c3c; font-size:10px;">Kritischer Audit-Fehler: ${e.message}</div>`;
    }
}

/**
 * DEEP FFmpeg PIPELINE PROBE (v1.37.13)
 */
async function runVideoForensicAudit() {
    const results = document.getElementById('diag-video-forensic-results');
    if (!results) return;

    sentinelPulse('AUDIT', 'Triggering Deep FFmpeg Pipeline Probe...');
    results.innerHTML = '<div style="font-size:10px; opacity:0.6; padding:10px;">Analysiere FFmpeg-Pipeline & Remuxer...</div>';

    try {
        const audit = await eel.run_video_transcode_diagnostic()();
        if (audit.status === 'error') {
            results.innerHTML = `<div style="color:#e74c3c; font-size:11px; padding:10px;">${audit.error}</div>`;
            return;
        }

        results.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:8px;">
                <div style="color:#2ecc71; font-weight:900;">PIPELINE: OK</div>
                <div style="font-size:10px; opacity:0.8; word-break:break-all;">Probe für: ${audit.path || 'Unknown'}</div>
                <div style="margin-top:5px; display:flex; flex-direction:column; gap:4px;">
                ${(audit.results || []).map(r => `
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:6px; border-radius:4px; font-size:10px; opacity:0.8;">
                        ${r.name}: <span style="color:#fff; font-weight:800;">${r.status.toUpperCase()}</span>
                    </div>
                `).join('')}
                </div>
            </div>
        `;
    } catch (e) {
        results.innerHTML = `<div style="color:#e74c3c; font-size:10px;">FFmpeg-Probe fehlgeschlagen: ${e.message}</div>`;
    }
}

/**
 * DATABASE RESILIENCE AUDIT (v1.37.13)
 */
async function runDatabaseResilienceAudit() {
    const results = document.getElementById('diag-db-resilience-results');
    if (!results) return;

    sentinelPulse('AUDIT', 'Executing SQLite PRAGMA Integrity Scan...');
    results.innerHTML = '<div style="font-size:10px; opacity:0.6; padding:10px;">Prüfe SQLite-Index & Integrity...</div>';

    try {
        const res = await eel.check_database_resilience()();
        results.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:8px;">
                <div style="color:#2ecc71; font-weight:800;">SQL HEALTH: ${res.sqlite_health.toUpperCase()}</div>
                <div style="font-size:10px; opacity:0.8;">Gesamte Library: <span style="color:#fff;">${res.fs_parity.total_items} Items</span></div>
                <div style="font-size:10px; opacity:0.8; color:${res.fs_parity.ghost_count > 0 ? '#f1c40f' : '#2ecc71'}">GHOST ITEMS: ${res.fs_parity.ghost_count}</div>
            </div>
        `;
    } catch (e) {
        results.innerHTML = `<div style="color:#e74c3c; font-size:10px;">Integritäts-Audit fehlgeschlagen: ${e.message}</div>`;
    }
}

async function runFSParityAudit() {
    const results = document.getElementById('diag-db-resilience-results');
    if (!results) return;

    sentinelPulse('AUDIT', 'Scanning for Ghost References (FS Parity)...');
    results.innerHTML = '<div style="font-size:10px; opacity:0.6; padding:10px;">Scanne Dateisystem-Parität...</div>';

    try {
        const res = await eel.check_database_resilience()();
        if (res.fs_parity.ghost_count === 0) {
            results.innerHTML = `<div style="color:#2ecc71; font-weight:800; font-size:11px; padding:10px;">100% PARITY OK. Alle DB-Einträge auf Disk vorhanden.</div>`;
            return;
        }

        results.innerHTML = `
            <div style="display:flex; flex-direction:column; gap:6px;">
                <div style="color:#f1c40f; font-weight:900;">${res.fs_parity.ghost_count} GHOSTS DETECTED</div>
                <div style="max-height:200px; overflow-y:auto; background:rgba(0,0,0,0.4); border-radius:6px; padding:8px; display:flex; flex-direction:column; gap:8px;">
                    ${res.fs_parity.ghost_items.map(i => `
                        <div style="font-size:9px;">
                            <div style="font-weight:900; color:#ff3366;">${i.name}</div>
                            <div style="opacity:0.4; word-break:break-all;">${i.path}</div>
                        </div>
                    `).join('')}
                </div>
                <div style="font-size:8px; opacity:0.4; margin-top:5px; text-align:center;">Manuelle Bereinigung empfohlen.</div>
            </div>
        `;
    } catch (e) {
        results.innerHTML = `<div style="color:#e74c3c; font-size:10px;">FS-Parity Scan fehlgeschlagen: ${e.message}</div>`;
    }
}

/**
 * SENTINEL: Live Trace Engine (Forensic Upgrade v1.37.12)
 */
function sentinelPulse(tag, message, skipStorage = false) {
    const container = document.getElementById('sentinel-log-container');
    if (!container) return;

    const entryData = {
        ts: new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' }),
        tag: tag,
        msg: message
    };

    // 1. Storage Persistence
    if (!skipStorage) {
        const history = JSON.parse(localStorage.getItem('mwv_sentinel_trace') || '[]');
        history.push(entryData);
        if (history.length > SENTINEL_MAX_ENTRIES) history.shift();
        localStorage.setItem('mwv_sentinel_trace', JSON.stringify(history));
    }

    // 2. DOM Rendering
    renderSentinelEntry(entryData, container);
}

function renderSentinelEntry(data, container) {
    const entry = document.createElement('div');
    entry.style.cssText = 'border-bottom:1px solid rgba(0,255,204,0.05); padding:3px 0; display:flex; gap:8px; align-items:flex-start;';
    
    entry.innerHTML = `
        <span style="opacity:0.3; flex-shrink:0;">[${data.ts}]</span> 
        <span style="font-weight:900; color:#00ffcc; flex-shrink:0; min-width:40px;">${data.tag}</span> 
        <span style="opacity:0.8; word-break:break-all;">${data.msg}</span>
    `;

    container.appendChild(entry);
    container.scrollTop = container.scrollHeight;
    while (container.childNodes.length > SENTINEL_MAX_ENTRIES) container.removeChild(container.firstChild);
}

function loadSentinelHistory() {
    const container = document.getElementById('sentinel-log-container');
    if (!container) return;
    
    container.innerHTML = ''; // Clear for re-hydration
    const history = JSON.parse(localStorage.getItem('mwv_sentinel_trace') || '[]');
    history.forEach(entry => renderSentinelEntry(entry, container));
    
    sentinelPulse('SENTINEL', `History recovered: ${history.length} entries.`, true);
}

function downloadSentinelTrace() {
    const history = JSON.parse(localStorage.getItem('mwv_sentinel_trace') || '[]');
    if (!history.length) return alert('No trace data to export.');

    const content = history.map(e => `[${e.ts}] ${e.tag.padEnd(10)} | ${e.msg}`).join('\n');
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = `mwv_sentinel_trace_${new Date().toISOString().slice(0,19).replace(/:/g,'-')}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    
    sentinelPulse('SYSTEM', 'Trace log exported successfully.', true);
}

function clearSentinelLog() {
    localStorage.removeItem('mwv_sentinel_trace');
    const container = document.getElementById('sentinel-log-container');
    if (container) container.innerHTML = '';
    sentinelPulse('SYSTEM', 'Trace log cleared by user.', false);
}

/**
 * Global Bridge Functions
 */
function toggleDiagnosticsFlag(flagId) {
    sentinelPulse('FLAG', `Toggle requested: ${flagId}`);
    if (typeof window.toggleDiagnosticsFlag === 'function') {
        window.toggleDiagnosticsFlag(flagId);
    }
}

// Removed redundant window re-definitions causing circular recursion
window.switchDiagnosticsSidebarTab = switchDiagnosticsSidebarTab;
window.toggleDiagnosticsFlag = toggleDiagnosticsFlag; 
window.sentinelPulse = sentinelPulse;
/**
 * HYDRATION MASTER CONSOLE (v1.37.14)
 */
async function triggerMasterScan() {
    sentinelPulse('COMMAND', 'Triggering Deep Direct Scan (Re-Index)...');
    try {
        const res = await eel.run_direct_scan()();
        if (res.status === 'success') {
            sentinelPulse('SYSTEM', `Scan Complete: Found ${res.items_found} items.`);
            if (typeof renderLibrary === 'function') eel.get_library()((itms) => renderLibrary(itms));
        }
    } catch (e) {
        sentinelPulse('ERROR', `Direct Scan Failed: ${e.message}`);
    }
}

async function triggerMasterSync() {
    sentinelPulse('COMMAND', 'Triggering Atomic SQLite Sync...');
    try {
        const res = await eel.sync_library_atomic()();
        if (res.status === 'success') {
            sentinelPulse('SYSTEM', `Sync Complete: Hydrated ${res.count} items.`);
            if (typeof renderLibrary === 'function') renderLibrary(res.items);
            runHydrationAuditProbe(); // Auto-refresh audit
        }
    } catch (e) {
        sentinelPulse('ERROR', `Atomic Sync Failed: ${e.message}`);
    }
}

async function triggerNuclearRecovery() {
    sentinelPulse('NUCLEAR', 'BYPASSING ALL FILTERS (Core Recovery)...');
    try {
        const result = await eel.force_sync_all()();
        if (result && result.status === 'raw-recovery') {
            if (typeof renderLibrary === 'function') renderLibrary(result.media);
            sentinelPulse('SUCCESS', `RECOVERED ${result.media.length} items via bypass.`);
            runHydrationAuditProbe(); 
        }
    } catch (e) {
        sentinelPulse('ERROR', `Nuclear Recovery Failed: ${e.message}`);
    }
}

/**
 * NATIVE FLOW AUDITOR (7-Stage Visualization)
 */
async function runHydrationAuditProbe() {
    const viewport = document.getElementById('diag-logic-audit-viewport');
    if (!viewport) return;

    viewport.innerHTML = '<div style="font-size:10px; opacity:0.6; text-align:center; padding:15px;">Scanning Backend Flow...</div>';
    
    try {
        let audit = null;
        if (typeof eel.perform_system_logic_audit === 'function') {
            audit = await eel.perform_system_logic_audit()();
        }

        if (!audit) {
            viewport.innerHTML = '<div style="font-size:10px; opacity:0.4; text-align:center; padding:15px;">Backend Flow Sensor not available.</div>';
            return;
        }

        renderNativeHydrationReport(audit, viewport);
    } catch (e) {
        viewport.innerHTML = `<div style="color:#e74c3c; font-size:10px;">Audit-Fehler: ${e.message}</div>`;
    }
}

function renderNativeHydrationReport(audit, viewport) {
    const dr = audit.dropped_reasons || {};
    const total = audit.dropped_total || 0;
    const kept = audit.kept || 0;

    let html = `
        <div style="border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom:8px; margin-bottom:8px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <span style="font-size:9px; font-weight:900; color:#2ecc71;">KEPT: ${kept}</span>
                <span style="font-size:9px; font-weight:900; color:#ff3366;">DROPPED: ${total}</span>
            </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:4px;">
    `;

    for (const [reason, count] of Object.entries(dr)) {
        if (count > 0) {
            const label = reason.replace('_mismatch', '').toUpperCase();
            html += `
                <div style="display:flex; justify-content:space-between; font-size:10px; background:rgba(255,51,102,0.05); padding:4px 8px; border-radius:4px; border:1px solid rgba(255,51,102,0.1);">
                    <span style="opacity:0.7;">${label}</span>
                    <span style="color:#ff3366; font-weight:900;">${count}</span>
                </div>
            `;
        }
    }

    if (total === 0) {
        html += '<div style="font-size:10px; color:#2ecc71; text-align:center; padding:10px;">100% FILTER PASS OK</div>';
    }

    html += `</div>`;
    viewport.innerHTML = html;
}

window.performItemJourneyAudit = performItemJourneyAudit;
window.initDiagnosticsSidebar = initDiagnosticsSidebar;
window.downloadSentinelTrace = downloadSentinelTrace;
window.clearSentinelLog = clearSentinelLog;
window.runVideoForensicAudit = runVideoForensicAudit;
window.runDatabaseResilienceAudit = runDatabaseResilienceAudit;
window.runFSParityAudit = runFSParityAudit;
window.triggerMasterScan = triggerMasterScan;
window.triggerMasterSync = triggerMasterSync;
window.triggerNuclearRecovery = triggerNuclearRecovery;
window.runHydrationAuditProbe = runHydrationAuditProbe;
