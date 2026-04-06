const SENTINEL_MAX_ENTRIES = 100;

/**
 * DIAGNOSTIC LAYER REGISTRY (v1.37.36)
 */
const DIAG_VIEW_INFO = {
    'health': { name: 'Command Center', desc: 'Global Health & Mission-Critical Readiness' },
    'log': { name: 'Forensic Logs', desc: 'Real-time System Event Streaming' },
    'hydration': { name: 'HYDRATION CHAIN', desc: 'Analyzes media flow from SQL to DOM.' },
    'item-track': { name: 'ITEM JOURNEY', desc: 'Traces a specific file across all layers.' },
    'sentinel': { name: 'SENTINEL LOG', desc: 'Live application event listener.' },
    'debug-db': { name: 'DATABASE OVERVIEW', desc: 'Raw SQLite index & Category statistics.' },
    'logs': { name: 'Forensic Logic', desc: 'Real-time Trace Engineering & Filtering' },
    'video-health': { name: 'Active Workers', desc: 'Process Runtime & Surgical Kill Matrix' },
    'recovery': { name: 'Database Resilience', desc: 'Tactical Restoration & Atomic Sync' },
    'environment': { name: 'System Health', desc: 'Resource Telemetry & Platform Audit' },
    'storage': { name: 'Volume Discovery', desc: 'FS Heuristics & Large Asset Audit' },
    'performance': { name: 'GUI Performance', desc: 'DOM Bloat & Rendering Decathlon' },
    'playlist': { name: 'Playlist Forensics', desc: 'Relational & Physical Collection Audit' },
    'state': { name: 'State Persistence', desc: 'LocalStorage vs. Configuration Master Audit' },
    'network': { name: 'RPC Performance', desc: 'Internal Bridge Latency & RTT Audit' },
    'process': { name: 'Worker Control', desc: 'Child Process & Zombie Workstation Audit' },
    'driver': { name: 'Hardware Accel', desc: 'GPU & Transcoder Capability Audit' },
    'security': { name: 'Authority Hub', desc: 'UID/GID & Filesystem Permission Audit' },
    'api': { name: 'Bridge Registry', desc: 'Internal API & Live Documentation Audit' }
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
        'health': 'diag-pane-health',
        'log': 'diag-pane-log',
        'hydration': 'diag-pane-hydration',
        'item-track': 'diag-pane-item-track',
        'sentinel': 'diag-pane-sentinel',
        'debug-db': 'diag-pane-debug-db',
        'logs': 'diag-pane-logs',
        'video-health': 'diag-pane-video-health',
        'recovery': 'diag-pane-db-resilience',
        'environment': 'diag-pane-environment',
        'storage': 'diag-pane-storage',
        'performance': 'diag-pane-performance',
        'playlist': 'diag-pane-playlist',
        'state': 'diag-pane-state',
        'network': 'diag-pane-network',
        'process': 'diag-pane-process',
        'driver': 'diag-pane-driver',
        'security': 'diag-pane-security',
        'api': 'diag-pane-api'
    };

    if (paneIds[viewId]) {
        if (viewId === 'health') runGlobalHealthAudit();
        
        const target = document.getElementById(paneIds[viewId]);
        if (target) target.style.display = 'block';

        // Trigger Data Fetchers
        if (viewId === 'hydration') runHydrationAuditProbe();
        if (viewId === 'item-track') renderItemTrackTab();
        if (viewId === 'debug-db' && typeof renderDebugDatabase === 'function') renderDebugDatabase();
        if (viewId === 'logs' && typeof refreshDebugLogs === 'function') refreshDebugLogs();
        if (viewId === 'video-health') runVideoWorkerAudit();
        if (viewId === 'environment') runEnvironmentAudit();
        if (viewId === 'storage') runStorageAudit();
        if (viewId === 'performance') runPerformanceAudit();
        if (viewId === 'playlist') runPlaylistAudit();
        if (viewId === 'state') runStateAudit();
        if (viewId === 'network') runNetworkAudit();
        if (viewId === 'process') runProcessAudit();
        if (viewId === 'driver') runHardwareAudit();
        if (viewId === 'security') runSecurityAudit();
        if (viewId === 'api') runApiAudit();

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
 * ITEM TRACKER: High-Performance Probe (Legacy JS-based UI removed in v1.37.15)
 */
function renderItemTrackTab() {
    // Search console is now native in diagnostics_sidebar.html fragment.
    // This function can now be used for specialized search-history or stats.
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

        renderForensicTimelineUI(item, stages, fe_normalized, dom_node);

    } catch (e) {
        results.innerHTML = `<div style="color:#e74c3c; font-size:10px;">Audit-Fehler: ${e.message}</div>`;
    }
}

/**
 * FORENSIC TIMELINE UI (v1.37.15)
 */
function renderForensicTimelineUI(item, stages, fe_memory, dom_node) {
    const results = document.getElementById('diag-item-audit-results');
    if (!results) return;

    sentinelPulse('TRACE', `Rendering Forensic Timeline for [${item.id}] ${item.name}`);

    results.innerHTML = `
        <div style="display:flex; flex-direction:column; gap:8px;">
            <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:8px;">
                <div style="font-size:12px; font-weight:900; color:#fff;">${item.name}</div>
                <div style="display:flex; gap:4px;">
                    <button onclick="triggerRawItemProbe(${item.id})" style="background:rgba(0,255,153,0.05); border:1px solid rgba(0,255,153,0.1); color:#00ff99; font-size:8px; padding:2px 6px; border-radius:4px; cursor:pointer; font-weight:900;" title="Deep ffprobe Header Audit">RAW</button>
                    <button onclick="bridgeToItemJSON(${item.id})" style="background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:#3498db; font-size:8px; padding:2px 6px; border-radius:4px; cursor:pointer; font-weight:900;">VIEW JSON</button>
                </div>
            </div>
            <div id="diag-item-raw-output" style="margin-bottom:10px;"></div>

            <div class="forensic-timeline-v137">
                <div class="f-step ${stages.db.status === 'ok' ? 'ok' : 'err'}">
                    <span class="f-icon">🗄️</span> 
                    <div class="f-meta">
                        <span class="f-label">SQL INDEX</span>
                        <span class="f-status">${stages.db.status.toUpperCase()}</span>
                    </div>
                </div>
                <div class="f-step ${stages.backend_filter.status === 'ok' ? 'ok' : 'err'}">
                    <span class="f-icon">⚙️</span>
                    <div class="f-meta">
                        <span class="f-label">B-FLTR CHAIN</span>
                        <span class="f-status">${stages.backend_filter.reason}</span>
                    </div>
                </div>
                <div class="f-step ${fe_memory ? 'ok' : 'err'}">
                    <span class="f-icon">🧠</span>
                    <div class="f-meta">
                        <span class="f-label">FRONTEND MEM</span>
                        <span class="f-status">${fe_memory ? 'HYDRATED' : 'MISSING'}</span>
                    </div>
                </div>
                <div class="f-step ${dom_node ? 'ok' : 'err'}">
                    <span class="f-icon">🖥️</span>
                    <div class="f-meta">
                        <span class="f-label">DOM VIEWPORT</span>
                        <span class="f-status">${dom_node ? 'RENDERED' : 'HIDDEN'}</span>
                    </div>
                </div>
                <div class="f-step ${item.last_played ? 'active' : 'idle'}">
                    <span class="f-icon">🎥</span>
                    <div class="f-meta">
                        <span class="f-label">PLAYBACK HIST.</span>
                        <span class="f-status">${item.last_played || 'NEVER PLAYED'}</span>
                    </div>
                </div>
            </div>
            
            <style>
                .forensic-timeline-v137 { display: flex; flex-direction: column; gap: 8px; border-left: 2px solid rgba(255,255,255,0.05); padding-left: 15px; margin-left: 10px; }
                .f-step { display: flex; align-items: center; gap: 12px; position: relative; }
                .f-step:before { content: ""; position: absolute; left: -19px; top: 50%; transform: translateY(-50%); width: 6px; height: 6px; border-radius: 50%; background: #444; }
                .f-icon { font-size: 14px; filter: grayscale(1); opacity: 0.5; }
                .f-meta { display: flex; flex-direction: column; flex: 1; }
                .f-label { font-size: 8px; opacity: 0.4; letter-spacing: 0.5px; text-transform: uppercase; }
                .f-status { font-size: 10px; font-weight: 800; font-family: 'JetBrains Mono', monospace; }
                
                .f-step.ok .f-icon { filter: grayscale(0); opacity: 1; }
                .f-step.ok .f-status { color: #2ecc71; }
                .f-step.ok:before { background: #2ecc71; box-shadow: 0 0 5px #2ecc71; }

                .f-step.err .f-icon { filter: grayscale(0); opacity: 1; }
                .f-step.err .f-status { color: #ff3366; }
                .f-step.err:before { background: #ff3366; }

                .f-step.active .f-icon { filter: grayscale(0); opacity: 1; }
                .f-step.active .f-status { color: #3498db; }
                .f-step.active:before { background: #3498db; }
            </style>
        </div>
    `;
}

async function triggerRawItemProbe(itemId) {
    const output = document.getElementById('diag-item-raw-output');
    if (!output) return;

    sentinelPulse('PROBE', `Executing Raw Header Probe for Item ID: ${itemId}`);
    output.innerHTML = '<div style="font-size:9px; color:#00ff99; opacity:0.6; text-align:center; padding:10px; background:rgba(0,255,153,0.05); border-radius:6px; border:1px solid rgba(0,255,153,0.1);">Executing ffprobe Raw Header Audit...</div>';

    try {
        const res = await eel.run_raw_media_probe(itemId)();
        if (res.status === 'success') {
            sentinelPulse('SUCCESS', `Deep Header Audit Complete for ID: ${itemId}`);
            
            // Render high-density JSON with workstation syntax highlighting
            output.innerHTML = `
                <div style="background:#000; border:1px solid rgba(0,255,153,0.2); border-radius:8px; padding:10px; max-height:300px; overflow-y:auto; position:relative;">
                    <div style="position:sticky; top:0; background:#000; font-size:8px; font-weight:900; color:#00ff99; margin-bottom:8px; padding-bottom:5px; border-bottom:1px solid rgba(0,255,153,0.1);">RAW_FFPROBE_PAYLOAD_V137</div>
                    <pre style="margin:0; font-size:9px; font-family:'JetBrains Mono', monospace; line-height:1.4; color:#d4d4d4;">${syntaxHighlightForensicJSON(res.data)}</pre>
                </div>
            `;
        } else {
            sentinelPulse('ERROR', `Probe Failed: ${res.message}`);
            output.innerHTML = `<div style="color:#ff3366; font-size:10px; padding:10px; background:rgba(255,51,102,0.1); border-radius:6px;">Probe Failed: ${res.message}</div>`;
        }
    } catch (e) {
        sentinelPulse('ERROR', `Probe Bridge Fault: ${e.message}`);
        output.innerHTML = `<div style="color:#ff3366; font-size:10px; padding:10px;">Bridge Fault: ${e.message}</div>`;
    }
}

function syntaxHighlightForensicJSON(json) {
    if (typeof json !== 'string') {
        json = JSON.stringify(json, null, 2);
    }
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
 * v1.37.15 TELEPORTATION BRIDGE
 */
function bridgeToItemJSON(id) {
    sentinelPulse('BRIDGE', `Teleporting to JSON DB for Item ID: ${id}`);
    
    // 1. Switch Tab
    switchDiagnosticsSidebarTab('debug-db');
    
    // 2. Perform Specialized Search in DB
    setTimeout(() => {
        const dbSearch = document.getElementById('debug-items-json');
        if (dbSearch && window.debug_library_dict) {
            const itemMatch = window.debug_library_dict.find(i => i.id === id);
            if (itemMatch) {
                dbSearch.innerHTML = `<span style="color:#3498db; font-weight:900;">// TELEPORT SUCCESS [ID:${id}]</span>\n` + JSON.stringify(itemMatch, null, 2);
            }
        }
    }, 100);
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

        const ghostIds = res.fs_parity.ghost_items.map(i => i.id);

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
                <button onclick='triggerGhostPruning(${JSON.stringify(ghostIds)})' 
                    style="margin-top:10px; background:#e74c3c; color:white; border:none; padding:8px; border-radius:6px; font-size:10px; font-weight:900; cursor:pointer;"
                    title="Safe Bulk-Deletion of verified dead references">
                    PRUNE ALL ${res.fs_parity.ghost_count} GHOSTS
                </button>
            </div>
        `;
    } catch (e) {
        results.innerHTML = `<div style="color:#e74c3c; font-size:10px;">FS-Parity Scan fehlgeschlagen: ${e.message}</div>`;
    }
}

async function triggerGhostPruning(ghostIds) {
    const status = document.getElementById('diag-db-prune-status');
    if (!status || !ghostIds || ghostIds.length === 0) return;

    if (!confirm(`FORENSIC CLEANUP: Prune ${ghostIds.length} verified dead references from SQLite? This cannot be undone.`)) return;

    sentinelPulse('PRUNE', `Executing Atomic Bulk Deletion for ${ghostIds.length} IDs...`);
    status.innerHTML = '<div style="font-size:9px; color:#f1c40f; text-align:center;">Pruning Ghost References...</div>';

    try {
        const res = await eel.prune_ghost_items(ghostIds)();
        if (res.status === 'success') {
            sentinelPulse('SUCCESS', `Pruning Complete: Removed ${res.count} records.`);
            status.innerHTML = `<div style="font-size:9px; color:#2ecc71; text-align:center;">SUCCESS: ${res.count} Records Pruned.</div>`;
            addForensicRecAction('GHOST PRUNE', 'SUCCESS', `Removed ${res.count} items.`);
            setTimeout(() => {
                status.innerHTML = '';
                runFSParityAudit(); // Refresh the list
            }, 2000);
        } else {
            sentinelPulse('ERROR', `Pruning Failed: ${res.message}`);
            status.innerHTML = `<div style="color:#ff3366; font-size:9px;">Pruning Failed: ${res.message}</div>`;
            addForensicRecAction('GHOST PRUNE', 'ERROR', res.message);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Pruning Bridge Fault: ${e.message}`);
        status.innerHTML = `<div style="color:#ff3366; font-size:9px;">Bridge Fault: ${e.message}</div>`;
    }
}

async function triggerPipelineRecovery() {
    const status = document.getElementById('diag-video-recovery-status');
    if (status) status.innerHTML = '<div style="font-size:9px; color:#f1c40f; text-align:center;">Executing Pipeline Purge...</div>';
    
    sentinelPulse('RECOVER', "Executing Pipeline Purge (FFmpeg/MKVMerge)...");
    try {
        const res = await eel.super_kill_pipeline()();
        if (res.status === 'ok') {
            sentinelPulse('SUCCESS', `Tactical Purge Complete: Removed ${res.count} processes.`);
            if (status) status.innerHTML = `<div style="font-size:9px; color:#2ecc71; text-align:center;">SUCCESS: ${res.count} Processes Purged.</div>`;
            addForensicRecAction('PIPELINE PURGE', 'SUCCESS', `Removed ${res.count} workers.`);
        } else {
            sentinelPulse('ERROR', `Purge Failed: ${res.message}`);
            if (status) status.innerHTML = `<div style="color:#ff3366; font-size:9px;">Purge Failed: ${res.message}</div>`;
            addForensicRecAction('PIPELINE PURGE', 'ERROR', res.message);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Pipeline Bridge Fault: ${e.message}`);
        if (status) status.innerHTML = `<div style="color:#ff3366; font-size:9px;">Bridge Fault: ${e.message}</div>`;
    }
}

/**
 * SENTINEL: Live Trace Engine (Forensic Upgrade v1.37.16)
 */
function sentinelPulse(tag, message, skipStorage = false) {
    const container = document.getElementById('sentinel-log-container');
    
    // Module Cache Initialization (v1.37.16)
    if (!window.__sentinel_module_cache) {
        window.__sentinel_module_cache = { FE: [], BE: [], DB: [] };
    }

    const ts = new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const entryData = { ts, tag, msg: message };

    // 1. Storage Persistence
    if (!skipStorage) {
        const history = JSON.parse(localStorage.getItem('mwv_sentinel_trace') || '[]');
        history.push(entryData);
        if (history.length > (window.SENTINEL_MAX_ENTRIES || 500)) history.shift();
        localStorage.setItem('mwv_sentinel_trace', JSON.stringify(history));
    }

    // 2. Module Forensic Routing
    const tagUpper = tag.toUpperCase();
    let targetModule = null;
    
    if (['SQL', 'SCAN', 'SYNC', 'NUCLEAR', 'DB'].some(k => tagUpper.includes(k))) targetModule = 'DB';
    else if (['API', 'EEL', 'PIPE', 'STALL', 'VID', 'BE'].some(k => tagUpper.includes(k))) targetModule = 'BE';
    else if (['DOM', 'VIEW', 'GUI', 'THEME', 'FE', 'SYSTEM', 'SUCCESS'].some(k => tagUpper.includes(k))) targetModule = 'FE';

    if (targetModule) {
        const cache = window.__sentinel_module_cache[targetModule];
        cache.push(`[${ts}] ${tag}: ${message}`);
        if (cache.length > 3) cache.shift();
    }

    // 3. DOM Rendering (vibrant fragment)
    if (container) {
        const entry = renderSentinelEntry(entryData, container);
        
        // Live Filter Check (v1.37.23)
        if (window.__sentinel_search_query) {
            const query = window.__sentinel_search_query.toLowerCase();
            const text = (tag + " " + message).toLowerCase();
            if (!text.includes(query)) entry.style.display = 'none';
        }
    }
}

function filterSentinelTrace(query) {
    window.__sentinel_search_query = query;
    const container = document.getElementById('sentinel-log-container');
    if (!container) return;

    const entries = container.querySelectorAll('.sentinel-entry-v137');
    const lowerQuery = query.toLowerCase();

    entries.forEach(entry => {
        const text = entry.innerText.toLowerCase();
        entry.style.display = text.includes(lowerQuery) ? 'flex' : 'none';
    });
}

function renderSentinelEntry(data, container) {
    const entry = document.createElement('div');
    entry.className = 'sentinel-entry-v137'; // Tagged for triage
    entry.style.cssText = 'border-bottom:1px solid rgba(0,255,204,0.05); padding:3px 0; display:flex; gap:8px; align-items:flex-start;';
    
    entry.innerHTML = `
        <span style="opacity:0.3; flex-shrink:0;">[${data.ts}]</span> 
        <span style="font-weight:900; color:#00ffcc; flex-shrink:0; min-width:40px;">${data.tag}</span> 
        <span style="opacity:0.8; word-break:break-all;">${data.msg}</span>
    `;

    container.appendChild(entry);
    container.scrollTop = container.scrollHeight;
    while (container.childNodes.length > SENTINEL_MAX_ENTRIES) container.removeChild(container.firstChild);

    return entry;
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
            addForensicRecAction('DIRECT SCAN', 'SUCCESS', `Discovered ${res.items_found} items.`);
            if (typeof renderLibrary === 'function') eel.get_library()((itms) => renderLibrary(itms));
        }
    } catch (e) {
        sentinelPulse('ERROR', `Direct Scan Failed: ${e.message}`);
        addForensicRecAction('DIRECT SCAN', 'ERROR', e.message);
    }
}

async function triggerMasterSync() {
    sentinelPulse('COMMAND', 'Triggering Atomic SQLite Sync...');
    try {
        const res = await eel.sync_library_atomic()();
        if (res.status === 'success') {
            sentinelPulse('SYSTEM', `Sync Complete: Hydrated ${res.count} items.`);
            addForensicRecAction('ATOMIC SYNC', 'SUCCESS', `Hydrated ${res.count} items.`);
            if (typeof renderLibrary === 'function') renderLibrary(res.items);
            runHydrationAuditProbe(); // Auto-refresh audit
        }
    } catch (e) {
        sentinelPulse('ERROR', `Atomic Sync Failed: ${e.message}`);
        addForensicRecAction('ATOMIC SYNC', 'ERROR', e.message);
    }
}

async function triggerNuclearRecovery() {
    sentinelPulse('NUCLEAR', 'BYPASSING ALL FILTERS (Core Recovery)...');
    try {
        const result = await eel.force_sync_all()();
        if (result && result.media) {
            if (typeof renderLibrary === 'function') renderLibrary(result.media);
            sentinelPulse('SUCCESS', `RECOVERED ${result.media.length} items via bypass.`);
            addForensicRecAction('NUCLEAR RECOVERY', 'SUCCESS', `Recovered ${result.media.length} items.`);
            runHydrationAuditProbe(); 
        }
    } catch (e) {
        sentinelPulse('ERROR', `Nuclear Recovery Failed: ${e.message}`);
        addForensicRecAction('NUCLEAR RECOVERY', 'ERROR', e.message);
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
window.bridgeToItemJSON = bridgeToItemJSON;
window.triggerMasterScan = triggerMasterScan;
window.triggerMasterSync = triggerMasterSync;
window.triggerNuclearRecovery = triggerNuclearRecovery;
async function runHydrationParityAudit() {
    const container = document.getElementById('diag-hydration-parity-matrix');
    const content = document.getElementById('parity-matrix-content');
    if (!container || !content) return;

    container.style.display = 'block';
    content.innerHTML = '<div style="font-size:9px; opacity:0.6; text-align:center; padding:10px;">Querying Full-Stack Parity...</div>';
    sentinelPulse('AUDIT', 'Executing Four-Stage Hydration Parity Scan...');

    try {
        // 1. Backend Probe (DB & Cache)
        const backend = await eel.get_hydration_stats()();
        
        // 2. Frontend Memory Probe
        const frontend_count = (window.allLibraryItems || []).length;
        
        // 3. Browser DOM Probe
        const dom_count = document.querySelectorAll('.grid-item').length;

        const stages = [
            { id: 'DB', name: 'SQL INDEX', count: backend.db_index || 0, icon: '🗄️' },
            { id: 'CACHE', name: 'B-CACHE', count: backend.backend_cache || 0, icon: '⚙️' },
            { id: 'MEM', name: 'FE-MEM', count: frontend_count, icon: '🧠' },
            { id: 'DOM', name: 'VIEWPORT', count: dom_count, icon: '🖥️' }
        ];

        let html = '<div style="display:flex; flex-direction:column; gap:4px;">';
        
        stages.forEach((s, idx) => {
            const prevCount = idx > 0 ? stages[idx-1].count : s.count;
            const isLoss = s.count < prevCount;
            const statusColor = isLoss ? '#ff3366' : '#00ff99';
            const diff = s.count - prevCount;

            html += `
                <div style="display:flex; align-items:center; gap:8px; background:rgba(255,255,255,0.03); padding:6px 10px; border-radius:6px; border:1px solid ${isLoss ? 'rgba(255,51,102,0.2)' : 'rgba(255,255,255,0.05)'};">
                    <span style="font-size:12px; filter:${isLoss ? 'none' : 'grayscale(1) opacity(0.5)'};">${s.icon}</span>
                    <div style="flex:1; display:flex; flex-direction:column;">
                        <span style="font-size:7px; opacity:0.4; font-weight:900; letter-spacing:0.5px;">${s.name}</span>
                        <span style="font-size:11px; font-weight:900; font-family:'JetBrains Mono', monospace; color:${statusColor};">${s.count} Items</span>
                    </div>
                    ${isLoss ? `<span style="font-size:8px; font-weight:900; color:#ff3366; background:rgba(255,51,102,0.1); padding:2px 4px; border-radius:3px;">DROP: ${diff}</span>` : ''}
                </div>
            `;
        });

        html += '</div>';

        // Summary Alert
        if (dom_count < backend.db_index) {
            html += `
                <div style="margin-top:10px; padding:8px; background:rgba(231,76,60,0.1); border:1px solid rgba(231,76,60,0.2); border-radius:6px; font-size:9px; color:#e74c3c; line-height:1.3; font-weight:700;">
                    ⚠️ DISCREPANCY DETECTED: Pipeline loss of ${backend.db_index - dom_count} items. 
                    Check filters or execution logs.
                </div>
            `;
        } else {
            html += `
                <div style="margin-top:10px; padding:8px; background:rgba(46,204,113,0.1); border:1px solid rgba(46,204,113,0.2); border-radius:6px; font-size:9px; color:#2ecc71; text-align:center; font-weight:900;">
                    ✓ DATA PIPELINE 100% PARITY
                </div>
            `;
        }

        content.innerHTML = html;
        sentinelPulse('SUCCESS', `Parity Audit Complete. DOM: ${dom_count} / DB: ${backend.db_index}`);

    } catch (e) {
        content.innerHTML = `<div style="color:#ff3366; font-size:10px; padding:10px;">Audit Bridge Fault: ${e.message}</div>`;
        sentinelPulse('ERROR', `Parity Audit Failed: ${e.message}`);
    }
}

async function runVideoWorkerAudit() {
    const container = document.getElementById('diag-video-worker-viewport');
    const content = document.getElementById('video-worker-matrix-content');
    if (!container || !content) return;

    container.style.display = 'block';
    content.innerHTML = '<div style="font-size:9px; opacity:0.6; text-align:center; padding:10px;">Forensic Process Scan in progress...</div>';
    sentinelPulse('AUDIT', 'Executing Video Worker Forensic Audit...');

    try {
        const res = await eel.get_active_video_workers()();
        if (res.status === 'error') {
            content.innerHTML = `<div style="color:#ff3366; font-size:9px;">Audit Fault: ${res.message}</div>`;
            return;
        }

        const workers = res.workers || [];
        if (workers.length === 0) {
            content.innerHTML = '<div style="font-size:9px; opacity:0.4; text-align:center; padding:10px;">No Active Transcoding Workers.</div>';
            return;
        }

        let html = '<div style="display:flex; flex-direction:column; gap:4px;">';
        workers.forEach(w => {
            const statusColor = w.is_workspace ? '#2ecc71' : '#f1c40f'; // Green for our processes, yellow for others
            html += `
                <div style="display:flex; align-items:center; gap:8px; background:rgba(255,255,255,0.03); padding:6px 10px; border-radius:6px; border:1px solid rgba(255,255,255,0.05);">
                    <div style="flex:1; display:flex; flex-direction:column; gap:2px; overflow:hidden;">
                        <div style="display:flex; gap:6px; align-items:center;">
                            <span style="font-size:10px; font-weight:900; color:${statusColor}; font-family:'JetBrains Mono', monospace;">PID: ${w.pid}</span>
                            <span style="font-size:9px; font-weight:700; color:#fff; opacity:0.8;">[${w.name}]</span>
                        </div>
                        <span style="font-size:8px; opacity:0.4; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${w.command}">${w.command}</span>
                    </div>
                    <button onclick="surgicalTerminateWorker('${w.pid}')" style="background:rgba(231,76,60,0.1); border:1px solid rgba(231,76,60,0.2); color:#e74c3c; font-size:8px; font-weight:900; padding:4px 8px; border-radius:4px; cursor:pointer;" onmouseover="this.style.background='rgba(231,76,60,0.2)'" onmouseout="this.style.background='rgba(231,76,60,0.1)'">KILL</button>
                </div>
            `;
        });
        html += '</div>';
        content.innerHTML = html;
        sentinelPulse('SUCCESS', `Worker Audit Complete. Found ${workers.length} active workers.`);

    } catch (e) {
        content.innerHTML = `<div style="color:#ff3366; font-size:9px; padding:10px;">Audit Bridge Fault: ${e.message}</div>`;
        sentinelPulse('ERROR', `Video Worker Audit Failed: ${e.message}`);
    }
}

async function surgicalTerminateWorker(pid) {
    if (!confirm(`Are you sure you want to SURGICALLY TERMINATE worker PID: ${pid}?`)) return;
    
    sentinelPulse('KILL', `Attempting surgical termination of PID: ${pid}`);
    try {
        const res = await eel.terminate_video_worker(pid)();
        if (res.status === 'ok') {
            sentinelPulse('SUCCESS', `Surgical Kill complete for PID: ${pid}`);
            addForensicRecAction('SURGICAL KILL', 'SUCCESS', `Terminated PID: ${pid}`);
            runVideoWorkerAudit(); // Refresh the list
        } else {
            sentinelPulse('ERROR', `Surgical Kill failed for PID: ${pid}: ${res.message}`);
            addForensicRecAction('SURGICAL KILL', 'ERROR', `PID: ${pid} - ${res.message}`);
            alert(`Surgical Termination Failed: ${res.message}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Surgical Kill Bridge Fault for PID: ${pid}: ${e.message}`);
    }
}

window.runVideoWorkerAudit = runVideoWorkerAudit;
window.surgicalTerminateWorker = surgicalTerminateWorker;
window.runHydrationParityAudit = runHydrationParityAudit;
window.runHydrationAuditProbe = runHydrationAuditProbe;

/**
 * RECOVERY ACTION LOG (v1.37.26)
 */
window.__mwv_rec_actions_history = [];

function addForensicRecAction(name, status, details) {
    const viewport = document.getElementById('diag-rec-history-viewport');
    if (!viewport) return;

    // Remove placeholder if it exists
    if (viewport.innerText.includes('Keine Forensic-Aktionen')) {
        viewport.innerHTML = '';
    }

    const ts = new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    const isSuccess = status === 'SUCCESS';
    const color = isSuccess ? '#2ecc71' : '#e74c3c';

    // Persist to history for Snapshot (v1.37.27)
    window.__mwv_rec_actions_history.push({ ts, name, status, details });

    const entry = document.createElement('div');
    entry.style.cssText = `background:rgba(255,255,255,0.03); border-left:2px solid ${color}; padding:6px 10px; border-radius:4px; font-family:'JetBrains Mono', monospace; display:flex; flex-direction:column; gap:2px;`;
    
    entry.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:10px; font-weight:900; color:#fff;">${name}</span>
            <span style="font-size:8px; opacity:0.4;">${ts}</span>
        </div>
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <span style="font-size:8px; opacity:0.6; color:${color}; font-weight:900;">${status}</span>
            <span style="font-size:9px; opacity:0.8; color:#fff;">${details}</span>
        </div>
    `;

    viewport.prepend(entry);
    viewport.scrollTop = 0;
}

/**
 * UNIFIED FORENSIC SNAPSHOT (v1.37.27)
 */
async function generateForensicSnapshot() {
    sentinelPulse('AUDIT', 'Generating Unified Forensic Snapshot...');
    
    try {
        // Parallel Forensic Fetch
        const [forensics, hydration, workers] = await Promise.all([
            eel.get_library_forensics()(),
            eel.get_hydration_stats()(),
            eel.get_active_video_workers()()
        ]);

        const ts = new Date().toLocaleString('de-DE');
        let report = `MWV FORENSIC SNAPSHOT - ${ts}\n`;
        report += `==========================================\n\n`;

        // DB Stats
        report += `[1] DATABASE FORENSICS\n`;
        report += `------------------------------------------\n`;
        report += `Total Indexed: ${forensics.total}\n`;
        report += `Duplicates:    ${forensics.duplicates}\n`;
        report += `Categories:    ${JSON.stringify(forensics.categories, null, 2)}\n`;
        report += `Formats:       ${JSON.stringify(forensics.formats, null, 2)}\n\n`;

        // Hydration Parity
        report += `[2] HYDRATION PARITY AUDIT\n`;
        report += `------------------------------------------\n`;
        report += `SQLite Count:  ${hydration.sqlite_count}\n`;
        report += `Cache Count:   ${hydration.cache_count}\n`;
        report += `GUI Parity:    ${window.allLibraryItems ? window.allLibraryItems.length : 'N/A'}\n\n`;

        // Active Workers
        report += `[3] ACTIVE TRANSCODING WORKERS\n`;
        report += `------------------------------------------\n`;
        if (workers.workers && workers.workers.length > 0) {
            workers.workers.forEach(w => {
                report += `PID: ${w.pid} | Name: ${w.name} | Workspace: ${w.is_workspace}\n`;
            });
        } else {
            report += `No active workers detected.\n`;
        }
        report += `\n`;

        // Recovery Actions
        report += `[4] SESSION RECOVERY HISTORY\n`;
        report += `------------------------------------------\n`;
        if (window.__mwv_rec_actions_history.length > 0) {
            window.__mwv_rec_actions_history.forEach(a => {
                report += `[${a.ts}] ${a.name} | ${a.status} | ${a.details}\n`;
            });
        } else {
            report += `No forensic actions recorded this session.\n`;
        }

        report += `\n--- END OF FORENSIC SNAPSHOT ---`;

        // Atomic Download
        const blob = new Blob([report], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `mwv_forensic_snapshot_${new Date().getTime()}.txt`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);

        sentinelPulse('SUCCESS', 'Unified Forensic Snapshot Generated and Downloaded.');
    } catch (e) {
        console.error('Snapshot Error:', e);
        sentinelPulse('ERROR', `Snapshot Generation Failed: ${e.message}`);
        alert(`Forensic Snapshot Failed: ${e.message}`);
    }
}

/**
 * ENVIRONMENT FORENSIC AUDIT (v1.37.29)
 */
async function runEnvironmentAudit() {
    const details = document.getElementById('diag-env-details');
    const cpuEl = document.getElementById('diag-env-cpu');
    const ramEl = document.getElementById('diag-env-ram');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Auditing Environment...</div>';
    
    sentinelPulse('AUDIT', 'Executing System Environment Audit...');
    
    try {
        const res = await eel.get_system_environment()();
        if (res.status === 'ok') {
            const t = res.telemetry;
            const p = res.platform;
            
            if (cpuEl) cpuEl.innerText = t.cpu;
            if (ramEl) ramEl.innerText = t.ram;
            
            const portColor = t.port_8345 === 'active' ? '#2ecc71' : '#e74c3c';
            
            if (details) {
                details.innerHTML = `
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="opacity:0.5;">UPTIME</span>
                        <span style="font-family:monospace;">${t.uptime}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="opacity:0.5;">PORT 8345</span>
                        <span style="font-family:monospace; color:${portColor}; font-weight:800;">${t.port_8345.toUpperCase()}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px; border-top:1px solid rgba(255,255,255,0.05); padding-top:5px; margin-top:5px;">
                        <span style="opacity:0.5;">PYTHON</span>
                        <span>${p.python}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="opacity:0.5;">EEL</span>
                        <span>${p.eel}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                        <span style="opacity:0.5;">OS</span>
                        <span style="font-size:8px;">${p.os}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; border-top:1px solid rgba(255,255,255,0.05); padding-top:5px; margin-top:5px;">
                        <span style="opacity:0.5;">PID</span>
                        <span style="font-family:monospace; color:#f1c40f;">${res.pid}</span>
                    </div>
                `;
            }
            sentinelPulse('SUCCESS', `Environment Audit Complete. CPU: ${t.cpu}, RAM: ${t.ram}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Env Audit Failed: ${e.message}`);
        if (details) details.innerHTML = `<div style="color:#e74c3c; font-size:9px; text-align:center; padding:20px;">Audit Failed: ${e.message}</div>`;
    }
}

/**
 * STORAGE FORENSIC AUDIT (v1.37.30)
 */
async function runStorageAudit() {
    const details = document.getElementById('diag-str-details');
    const sizeEl = document.getElementById('diag-str-total-size');
    const filesEl = document.getElementById('diag-str-files');
    const foldersEl = document.getElementById('diag-str-folders');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Auditing volume...</div>';
    
    sentinelPulse('AUDIT', 'Executing Storage Volume Audit...');
    
    try {
        const res = await eel.get_storage_forensics()();
        if (res.status === 'ok') {
            if (sizeEl) sizeEl.innerText = res.total_size_human;
            if (filesEl) filesEl.innerText = res.total_files;
            if (foldersEl) foldersEl.innerText = res.total_folders;
            
            if (details) {
                let html = `
                    <div style="margin-bottom:10px; border-bottom:1px solid rgba(255,255,255,0.05); padding-bottom:5px;">
                        <span style="font-weight:900; color:#f39c12; font-size:9px;">TOP 10 LARGE ASSETS</span>
                    </div>
                    <div style="display:flex; flex-direction:column; gap:6px;">
                `;
                
                res.largest_files.forEach((f, i) => {
                    html += `
                        <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02); border-left:2px solid #f39c12; padding:4px 8px; border-radius:4px;">
                            <div style="display:flex; flex-direction:column; max-width:70%;">
                                <span style="font-size:9px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;" title="${f.path}">${f.name}</span>
                                <span style="font-size:7px; opacity:0.4;">${f.path}</span>
                            </div>
                            <span style="font-family:monospace; font-size:9px; font-weight:800;">${f.size_human}</span>
                        </div>
                    `;
                });
                
                html += `</div>`;
                
                html += `
                    <div style="margin-top:15px; background:rgba(0,0,0,0.2); padding:10px; border-radius:6px; border:1px dashed rgba(255,255,255,0.05);">
                        <div style="font-size:8px; opacity:0.5; margin-bottom:4px;">DEEPEST PATH (Level ${res.deepest_level})</div>
                        <div style="font-family:monospace; font-size:8px; word-break:break-all; color:#fff;">${res.deepest_path || '/'}</div>
                    </div>
                `;
                
                if (res.broken_paths.length > 0) {
                    html += `
                        <div style="margin-top:10px; color:#e74c3c; font-size:8px;">
                            ⚠️ Found ${res.broken_paths.length} broken filesystem paths.
                        </div>
                    `;
                }
                
                details.innerHTML = html;
            }
            sentinelPulse('SUCCESS', `Storage Audit Complete. Volume: ${res.total_size_human}, Files: ${res.total_files}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Storage Audit Failed: ${e.message}`);
        if (details) details.innerHTML = `<div style="color:#e74c3c; font-size:9px; text-align:center; padding:20px;">Audit Failed: ${e.message}</div>`;
    }
}

/**
 * GUI PERFORMANCE AUDIT (v1.37.31)
 */
function runPerformanceAudit() {
    const details = document.getElementById('diag-per-details');
    const latencyEl = document.getElementById('diag-per-latency');
    const bloatEl = document.getElementById('diag-per-bloat');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Auditing GUI...</div>';
    
    sentinelPulse('AUDIT', 'Executing GUI Performance Audit...');
    
    setTimeout(() => {
        const domNodes = document.querySelectorAll('*').length;
        const renderTime = window.__mwv_last_render_ms || 0;
        const images = document.querySelectorAll('img').length;
        
        if (latencyEl) latencyEl.innerText = `${renderTime.toFixed(1)}ms`;
        if (bloatEl) bloatEl.innerText = domNodes;
        
        // Color mapping for bloat
        const bloatColor = domNodes > 2000 ? '#e74c3c' : (domNodes > 1000 ? '#f1c40f' : '#2ecc71');
        if (bloatEl) bloatEl.style.color = bloatColor;
        
        if (details) {
            details.innerHTML = `
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <span style="opacity:0.5;">ASSET DENSITY</span>
                    <span style="font-family:monospace;">${images} Active Assets</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px;">
                    <span style="opacity:0.5;">EVENT REGISTRY</span>
                    <span style="font-family:monospace; opacity:0.8;">~${domNodes * 0.15 | 0} Listeners (Est.)</span>
                </div>
                <div style="display:flex; justify-content:space-between; margin-bottom:5px; border-top:1px solid rgba(255,255,255,0.05); padding-top:5px; margin-top:5px;">
                    <span style="opacity:0.5;">RENDER ENGINE</span>
                    <span style="color:#9b59b6; font-weight:800;">REACTIVE_V1_LITE</span>
                </div>
                <div style="margin-top:10px; font-size:8px; line-height:1.4; color:var(--text-secondary); opacity:0.6;">
                    ${domNodes > 1500 ? '⚠️ High DOM complexity detected. Consider fragment unloading.' : '✅ DOM complexity is within workstation limits.'}
                </div>
                <button onclick="renderLibrary()" style="width:100%; margin-top:10px; background:rgba(255,255,255,0.05); color:white; border:1px solid rgba(255,255,255,0.1); padding:6px; border-radius:4px; font-size:9px; cursor:pointer;">FORCE RE-RENDER AUDIT</button>
            `;
        }
        sentinelPulse('SUCCESS', `Performance Audit Complete. Nodes: ${domNodes}, Latency: ${renderTime.toFixed(1)}ms`);
    }, 100);
}

window.runPerformanceAudit = runPerformanceAudit;
window.runStorageAudit = runStorageAudit;
window.runEnvironmentAudit = runEnvironmentAudit;
window.generateForensicSnapshot = generateForensicSnapshot;

/**
 * PLAYLIST FORENSIC AUDIT (v1.37.32)
 */
async function runPlaylistAudit() {
    const details = document.getElementById('diag-ply-details');
    const countEl = document.getElementById('diag-ply-count');
    const orphansEl = document.getElementById('diag-ply-orphans');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Auditing collections...</div>';
    
    sentinelPulse('AUDIT', 'Executing Playlist Forensic Audit...');
    
    try {
        const res = await eel.get_playlist_forensics()();
        if (res.status === 'ok') {
            if (countEl) countEl.innerText = res.count;
            
            let totalOrphans = 0;
            res.playlists.forEach(pl => totalOrphans += pl.relational_orphans + pl.physical_missing);
            if (orphansEl) orphansEl.innerText = totalOrphans;
            
            if (details) {
                let html = '<div style="display:flex; flex-direction:column; gap:8px;">';
                if (res.playlists.length === 0) {
                    html += '<div style="opacity:0.4; text-align:center; padding:10px;">Keine Playlists in DB gefunden.</div>';
                }

                res.playlists.forEach(pl => {
                    const score = pl.integrity_score;
                    const scoreColor = score > 90 ? '#2ecc71' : (score > 60 ? '#f1c40f' : '#ff3366');
                    
                    html += `
                        <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:8px; border-radius:6px; display:flex; flex-direction:column; gap:4px;">
                            <div style="display:flex; justify-content:space-between; align-items:center;">
                                <span style="font-weight:900; color:#fff; font-size:10px;">${pl.name}</span>
                                <span style="font-size:9px; font-weight:800; color:${scoreColor}">${score}% INTEGRITY</span>
                            </div>
                            <div style="display:flex; gap:10px; font-size:8px; opacity:0.6;">
                                <span>ITEMS: ${pl.item_count}</span>
                                <span style="${pl.relational_orphans > 0 ? 'color:#ff3366; font-weight:900;' : ''}">ORPHANS: ${pl.relational_orphans}</span>
                                <span style="${pl.physical_missing > 0 ? 'color:#ff3366; font-weight:900;' : ''}">MISSING: ${pl.physical_missing}</span>
                            </div>
                            ${pl.broken_paths.length > 0 ? `
                                <div style="margin-top:5px; padding:4px; background:rgba(255,51,102,0.1); border-radius:4px; font-size:7px; color:#ff3366; max-height:40px; overflow:hidden; text-overflow:ellipsis;">
                                    BROKEN: ${pl.broken_paths[0]}${pl.broken_paths.length > 1 ? ' ...' : ''}
                                </div>
                            ` : ''}
                        </div>
                    `;
                });
                html += '</div>';
                details.innerHTML = html;
            }
            sentinelPulse('SUCCESS', `Playlist Audit Complete. Sets: ${res.count}, Total Orphans: ${totalOrphans}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Playlist Audit Failed: ${e.message}`);
        if (details) details.innerHTML = `<div style="color:#ff3366; font-size:9px; text-align:center; padding:20px;">Audit Failed: ${e.message}</div>`;
    }
}

window.runPlaylistAudit = runPlaylistAudit;

/**
 * PLAYLIST REPAIR SUITE (v1.37.32)
 */
async function triggerPlaylistPruningAll() {
    if (!confirm("FORENSIC REPAIR: Prune all relational orphans from ALL playlists? This cannot be undone.")) return;

    sentinelPulse('PRUNE', 'Executing Global Playlist Relational Clean-up...');
    try {
        const forensic = await eel.get_playlist_forensics()();
        if (forensic.status !== 'ok') {
            sentinelPulse('ERROR', 'Global Pruning failed: Could not fetch initial forensics.');
            return;
        }

        let totalPruned = 0;
        for (const pl of forensic.playlists) {
            if (pl.relational_orphans > 0) {
                const res = await eel.prune_playlist_orphans(pl.id)();
                if (res.status === 'success') totalPruned += res.count;
            }
        }

        sentinelPulse('SUCCESS', `Global Pruning Complete. Removed ${totalPruned} dead references.`);
        if (typeof addForensicRecAction === 'function') {
            addForensicRecAction('PLAYLIST PRUNE', 'SUCCESS', `Removed ${totalPruned} items across sessions.`);
        }
        
        // Refresh the audit metrics immediately
        runPlaylistAudit();

    } catch (e) {
        console.error("[Forensic-PLY] Pruning failed:", e);
        sentinelPulse('ERROR', `Global Pruning failed: ${e.message}`);
    }
}

window.triggerPlaylistPruningAll = triggerPlaylistPruningAll;

/**
 * STATE PERSISTENCE AUDIT (v1.37.33)
 */
async function runStateAudit() {
    const details = document.getElementById('diag-sta-details');
    const healthEl = document.getElementById('diag-sta-health');
    const driftEl = document.getElementById('diag-sta-drift');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Auditing application state...</div>';
    
    sentinelPulse('AUDIT', 'Executing Forensic State Audit...');
    
    try {
        const res = await eel.get_state_forensics()();
        if (res.status === 'ok') {
            const requiredKeys = ['mwv_diagnostic_mode', 'mwv_force_native', 'mwv_diag_view', 'mwv_sentinel_trace'];
            let driftCount = 0;
            let healthyCount = 0;
            
            let html = '<div style="display:flex; flex-direction:column; gap:6px;">';
            
            // Check LocalStorage Keys
            requiredKeys.forEach(key => {
                const val = localStorage.getItem(key);
                const exists = val !== null;
                if (!exists) driftCount++;
                else healthyCount++;
                
                html += `
                    <div style="display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.02); padding:4px 8px; border-radius:4px;">
                        <span style="font-family:monospace; font-size:8px; opacity:0.7;">${key}</span>
                        <span style="font-size:8px; font-weight:800; color:${exists ? '#2ecc71' : '#ff3366'}">${exists ? 'SYNC' : 'MISSING'}</span>
                    </div>
                `;
            });
            
            // Backend Parity Check
            const backendMatch = (res.diag_mode === (localStorage.getItem('mwv_diagnostic_mode') === 'true'));
            if (!backendMatch) driftCount++;
            
            html += `
                <div style="margin-top:8px; border-top:1px solid rgba(255,255,255,0.05); padding-top:8px;">
                    <div style="display:flex; justify-content:space-between; font-size:8px;">
                        <span style="opacity:0.5;">BACKEND_VER</span>
                        <span>${res.backend_version}</span>
                    </div>
                    <div style="display:flex; justify-content:space-between; font-size:8px;">
                        <span style="opacity:0.5;">PARSE_MODE</span>
                        <span>${res.app_mode}</span>
                    </div>
                </div>
            `;
            
            const healthScore = Math.floor((healthyCount / (requiredKeys.length + 1)) * 100);
            if (healthEl) healthEl.innerText = `${healthScore}%`;
            if (driftEl) driftEl.innerText = driftCount;
            
            html += '</div>';
            if (details) details.innerHTML = html;
            
            sentinelPulse('SUCCESS', `State Audit Complete. Health: ${healthScore}%, Drift: ${driftCount}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `State Audit Failed: ${e.message}`);
    }
}

async function forcePersistenceSync() {
    sentinelPulse('SYNC', 'Forcing state persistence alignment...');
    try {
        const res = await eel.get_state_forensics()();
        if (res.status === 'ok') {
            localStorage.setItem('mwv_diagnostic_mode', res.diag_mode);
            // Add more sync logic as needed
            sentinelPulse('SUCCESS', 'State persistence synchronized with backend master.');
            runStateAudit();
        }
    } catch (e) {
        sentinelPulse('ERROR', `Sync failed: ${e.message}`);
    }
}

window.runStateAudit = runStateAudit;
window.forcePersistenceSync = forcePersistenceSync;

/**
 * NETWORK & RPC LATENCY AUDIT (v1.37.34)
 */
async function runNetworkAudit() {
    const details = document.getElementById('diag-net-details');
    const avgEl = document.getElementById('diag-net-avg');
    const qualityEl = document.getElementById('diag-net-quality');
    const throughputEl = document.getElementById('diag-net-throughput');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Measuring bridge latency...</div>';
    
    sentinelPulse('AUDIT', 'Executing Forensic Network Audit...');
    
    const latencies = [];
    const pings = 5;
    
    try {
        for (let i = 0; i < pings; i++) {
            const start = performance.now();
            const res = await eel.get_net_ping()();
            const end = performance.now();
            
            if (res.status === 'ok') {
                latencies.push(end - start);
                // Mini delay between pings to avoid overwhelming
                await new Promise(r => setTimeout(r, 50));
            }
        }
        
        if (latencies.length > 0) {
            const avg = latencies.reduce((a, b) => a + b, 0) / latencies.length;
            const max = Math.max(...latencies);
            const min = Math.min(...latencies);
            const jitter = max - min;
            
            // Color mapping
            const color = avg < 20 ? '#2ecc71' : (avg < 60 ? '#f1c40f' : '#ff3366');
            if (avgEl) {
                avgEl.innerText = `${avg.toFixed(1)}ms`;
                avgEl.style.color = color;
            }
            
            const quality = Math.max(0, 100 - (avg * 0.5) - (jitter * 2));
            if (qualityEl) qualityEl.innerText = `${Math.floor(quality)}%`;
            
            if (details) {
                details.innerHTML = `
                    <div style="display:flex; flex-direction:column; gap:6px;">
                        <div style="display:flex; justify-content:space-between; font-size:9px;">
                            <span style="opacity:0.5;">MIN_RTT</span>
                            <span>${min.toFixed(2)}ms</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:9px;">
                            <span style="opacity:0.5;">MAX_RTT</span>
                            <span>${max.toFixed(2)}ms</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; font-size:9px;">
                            <span style="opacity:0.5;">JITTER_VAR</span>
                            <span style="${jitter > 10 ? 'color:#f1c40f' : ''}">${jitter.toFixed(2)}ms</span>
                        </div>
                        <div style="margin-top:5px; padding-top:5px; border-top:1px solid rgba(255,255,255,0.05); font-size:8px; opacity:0.6;">
                            Bridge: EEL_WEBSOCKET_RPC<br>
                            Samples: ${latencies.length} (Burst)
                        </div>
                    </div>
                `;
            }
            
            // Simple throughput bars
            if (throughputEl) {
                throughputEl.innerHTML = '';
                latencies.forEach(l => {
                    const h = Math.max(2, 30 - l);
                    const bar = document.createElement('div');
                    bar.style.cssText = `flex:1; height:${h}px; background:${color}; opacity:0.6; border-radius:1px;`;
                    throughputEl.appendChild(bar);
                });
            }
            
            sentinelPulse('SUCCESS', `Network Audit Complete. Avg Latency: ${avg.toFixed(1)}ms, Quality: ${Math.floor(quality)}%`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Network Audit Failed: ${e.message}`);
    }
}

window.runNetworkAudit = runNetworkAudit;

/**
 * PROCESS CONTROL & ZOMBIE AUDIT (v1.37.35)
 */
async function runProcessAudit() {
    const details = document.getElementById('diag-prc-details');
    const activeEl = document.getElementById('diag-prc-active');
    const zombieEl = document.getElementById('diag-prc-zombies');
    
    if (details) details.innerHTML = '<div style="opacity: 0.4; font-size: 9px; text-align: center; padding: 20px;">Scanning process tree...</div>';
    
    sentinelPulse('AUDIT', 'Executing Forensic Process Audit...');
    
    try {
        const res = await eel.get_process_forensics()();
        if (res.status === 'ok') {
            if (activeEl) activeEl.innerText = res.active_workers;
            if (zombieEl) {
                zombieEl.innerText = res.zombie_count;
                zombieEl.style.color = res.zombie_count > 0 ? '#ff3366' : '#2ecc71';
            }
            
            let html = '<div style="display:flex; flex-direction:column; gap:8px;">';
            if (res.processes.length === 0) {
                html += '<div style="opacity:0.4; text-align:center; padding:10px;">No child workers detected.</div>';
            }
            
            res.processes.forEach(p => {
                const isZombie = p.status.includes('ZOMBIE');
                html += `
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:8px; border-radius:6px; display:flex; flex-direction:column; gap:4px;">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:900; color:#fff; font-size:10px;">${p.name.toUpperCase()}</span>
                            <span style="font-size:8px; font-weight:800; color:${isZombie ? '#ff3366' : '#2ecc71'}">${p.status}</span>
                        </div>
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <div style="display:flex; gap:10px; font-size:8px; opacity:0.6; font-family:monospace;">
                                <span>PID: ${p.pid}</span>
                                <span>CPU: ${p.cpu_percent.toFixed(1)}%</span>
                                <span>MEM: ${p.memory_percent.toFixed(1)}%</span>
                            </div>
                            <button onclick="terminateProcess(${p.pid})" style="background:rgba(255,51,102,0.1); color:#ff3366; border:1px solid rgba(255,51,102,0.2); padding:2px 6px; border-radius:3px; font-size:7px; cursor:pointer;">KILL</button>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
            if (details) details.innerHTML = html;
            
            sentinelPulse('SUCCESS', `Process Audit Complete. Workers: ${res.active_workers}, Zombies: ${res.zombie_count}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Process Audit Failed: ${e.message}`);
    }
}

async function terminateProcess(pid) {
    if (!confirm(`Surgical Termination: Are you sure you want to kill PID ${pid}?`)) return;
    
    sentinelPulse('KILL', `Terminating worker PID ${pid}...`);
    try {
        const res = await eel.terminate_worker_process(pid)();
        if (res.status === 'success') {
            sentinelPulse('SUCCESS', `Terminated PID ${pid}.`);
            runProcessAudit();
        } else {
            sentinelPulse('ERROR', `Kill failed: ${res.message}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Termination Error: ${e.message}`);
    }
}

async function purgeZombieWorkers() {
    sentinelPulse('PURGE', 'Scanning for relational zombies...');
    try {
        const res = await eel.get_process_forensics()();
        if (res.status === 'ok') {
            const zombies = res.processes.filter(p => p.status.includes('ZOMBIE'));
            if (zombies.length === 0) {
                sentinelPulse('SUCCESS', 'No zombies identified for purging.');
                return;
            }
            
            for (const z of zombies) {
                await eel.terminate_worker_process(z.pid)();
            }
            
            sentinelPulse('SUCCESS', `Atomic Purge Complete. Removed ${zombies.length} zombies.`);
            runProcessAudit();
        }
    } catch (e) {
        sentinelPulse('ERROR', `Purge failed: ${e.message}`);
    }
}

window.runProcessAudit = runProcessAudit;
window.terminateProcess = terminateProcess;
window.purgeZombieWorkers = purgeZombieWorkers;

/**
 * GLOBAL HEALTH & MISSION-CRITICAL SUMMARY (HLT) [v1.37.36]
 */
async function runGlobalHealthAudit() {
    const scoreEl = document.getElementById('diag-hlt-score');
    const levelEl = document.getElementById('diag-hlt-level');
    const dbEl = document.getElementById('diag-hlt-db');
    const sysEl = document.getElementById('diag-hlt-sys');
    const spinner = document.getElementById('hlt-btn-spinner');
    const tiles = document.querySelectorAll('.h-tile');
    
    if (spinner) spinner.style.display = 'block';
    
    sentinelPulse('AUDIT', 'Initiating Master Technical Audit...');
    
    try {
        const res = await eel.get_global_health_audit()();
        if (res.status === 'ok') {
            if (scoreEl) {
                scoreEl.innerText = `${res.readiness_score}%`;
                const scoreColor = res.readiness_score >= 90 ? '#2ecc71' : (res.readiness_score >= 60 ? '#f1c40f' : '#ff3366');
                scoreEl.style.color = scoreColor;
            }
            
            if (levelEl) {
                levelEl.innerText = res.level;
                levelEl.style.color = res.readiness_score >= 75 ? '#2ecc71' : (res.readiness_score >= 50 ? '#f1c40f' : '#ff3366');
            }
            
            if (dbEl) dbEl.innerText = res.metrics.db;
            if (sysEl) sysEl.innerText = res.metrics.sys;
            
            // Activate Radar Tiles (Simulated activity across domains)
            tiles.forEach((t, i) => {
                setTimeout(() => {
                    t.classList.add('active');
                }, i * 50);
            });
            
            sentinelPulse('SUCCESS', `Master Audit Complete. Readiness: ${res.level} (${res.readiness_score}%)`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Master Audit Failed: ${e.message}`);
    } finally {
        if (spinner) spinner.style.display = 'none';
    }
}

window.runGlobalHealthAudit = runGlobalHealthAudit;

/**
 * UNIFIED DRIVER & HARDWARE AUDIT (v1.37.37)
 */
async function runHardwareAudit() {
    const gpuTypeEl = document.getElementById('diag-drv-gpu-type');
    const gpuUsageEl = document.getElementById('diag-drv-gpu-usage');
    const encodersEl = document.getElementById('diag-drv-encoders');
    const diskTypeEl = document.getElementById('diag-drv-disk-type');
    const pcieEl = document.getElementById('diag-drv-pcie');
    const matrixEl = document.getElementById('diag-codec-matrix');
    
    sentinelPulse('AUDIT', 'Scanning Hardware Transcoding Hub...');
    
    try {
        const res = await eel.get_hardware_forensics()();
        if (res.status === 'ok') {
            const hw = res.hardware;
            if (gpuTypeEl) gpuTypeEl.innerText = hw.gpu_type.toUpperCase();
            if (gpuUsageEl) gpuUsageEl.innerText = `${hw.gpu_usage.toFixed(1)}%`;
            
            // Render Encoders
            if (encodersEl) {
                if (hw.encoders && hw.encoders.length > 0) {
                    encodersEl.innerHTML = hw.encoders.map(e => `
                        <span style="font-size: 8px; padding: 2px 8px; background: rgba(241, 196, 15, 0.2); border: 1px solid rgba(241, 196, 15, 0.4); border-radius: 4px; color: #f1c40f; font-weight: 800;">${e.toUpperCase()}</span>
                    `).join('');
                } else {
                    encodersEl.innerHTML = '<span style="font-size: 8px; opacity:0.4;">SOFTWARE ONLY</span>';
                }
            }
            
            if (diskTypeEl) diskTypeEl.innerText = hw.disk_type;
            if (pcieEl) pcieEl.innerText = hw.pcie_gen;
            
            // Render Codec Matrix
            if (matrixEl) {
                const codecs = [
                    { name: 'H.264', status: hw.encoders.some(e => e.includes('h264') || e.includes('nvenc') || e.includes('vaapi') || e.includes('qsv')) },
                    { name: 'HEVC', status: hw.encoders.some(e => e.includes('hevc')) },
                    { name: 'AV1', status: hw.encoders.some(e => e.includes('av1')) },
                    { name: 'VP9', status: hw.encoders.some(e => e.includes('vp9')) }
                ];
                
                matrixEl.innerHTML = codecs.map(c => `
                    <div style="display:flex; justify-content:space-between; align-items:center; border-bottom:1px solid rgba(255,255,255,0.03); padding:2px 0;">
                        <span>${c.name}</span>
                        <span style="color:${c.status ? '#2ecc71' : 'rgba(255,255,255,0.2)'}; font-weight:900;">${c.status ? '✓' : '✗'}</span>
                    </div>
                `).join('');
            }
            
            sentinelPulse('SUCCESS', `Hardware Audit Complete. GPU: ${hw.gpu_type}, Encoders: ${hw.encoders.join(',')}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Hardware Audit Failed: ${e.message}`);
    }
}

window.runHardwareAudit = runHardwareAudit;

/**
 * SECURITY & FORENSIC AUTHORITY AUDIT (v1.37.38)
 */
async function runSecurityAudit() {
    const authEl = document.getElementById('diag-sec-auth');
    const identityEl = document.getElementById('diag-sec-identity');
    const dbPermEl = document.getElementById('diag-sec-db-perm');
    const libPermEl = document.getElementById('diag-sec-lib-perm');
    const platformEl = document.getElementById('diag-sec-platform');
    
    sentinelPulse('AUDIT', 'Scanning Forensic Authority Hub...');
    
    try {
        const res = await eel.get_security_forensics()();
        if (res.status === 'ok') {
            const sec = res.security;
            if (authEl) {
                authEl.innerText = sec.is_root ? 'ROOT / SUDO AUTHORITY' : 'STANDARD USER AUTHORITY';
                authEl.style.color = sec.is_root ? '#e74c3c' : '#2ecc71';
            }
            if (identityEl) identityEl.innerText = `UID: ${sec.uid} | GID: ${sec.gid} | ROOT: ${sec.is_root ? 'YES' : 'NO'}`;
            
            if (dbPermEl) {
                dbPermEl.innerText = sec.db_authority.write ? 'READ/WRITE (OK)' : 'READ-ONLY (LOCKED)';
                dbPermEl.style.color = sec.db_authority.write ? '#2ecc71' : '#e74c3c';
            }
            if (libPermEl) {
                libPermEl.innerText = sec.library_authority.write ? 'READ/WRITE (OK)' : 'READ-ONLY (LOCKED)';
                libPermEl.style.color = sec.library_authority.write ? '#2ecc71' : '#e74c3c';
            }
            if (platformEl) platformEl.innerText = `Platform: ${sec.platform}`;
            
            sentinelPulse('SUCCESS', `Security Audit Complete. Authority: ${sec.is_root ? 'ROOT' : 'USER'}`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `Security Audit Failed: ${e.message}`);
    }
}

window.runSecurityAudit = runSecurityAudit;

/**
 * INTERNAL API REGISTRY & DOCUMENTATION AUDIT (v1.37.39)
 */
async function runApiAudit() {
    const countEl = document.getElementById('diag-api-count');
    const registryEl = document.getElementById('diag-api-registry');
    
    sentinelPulse('AUDIT', 'Reflecting Backend Bridge Registry...');
    
    try {
        const res = await eel.get_api_forensics()();
        if (res.status === 'ok') {
            if (countEl) countEl.innerText = res.total_endpoints;
            
            let html = '<div style="display:flex; flex-direction:column; gap:10px;">';
            res.registry.forEach(bridge => {
                html += `
                    <div style="background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05); padding:8px; border-radius:6px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <span style="font-weight:900; color:var(--accent-color); font-size:10px;">${bridge.name.toUpperCase()}</span>
                            <span style="font-size:7px; opacity:0.5; padding:1px 5px; background:rgba(255,255,255,0.05); border-radius:3px;">${bridge.status}</span>
                        </div>
                        <div style="font-size:9px; color:rgba(255,255,255,0.7); line-height:1.4;">${bridge.desc}</div>
                    </div>
                `;
            });
            html += '</div>';
            if (registryEl) registryEl.innerHTML = html;
            
            sentinelPulse('SUCCESS', `API Audit Complete. Mapped ${res.total_endpoints} critical bridges.`);
        }
    } catch (e) {
        sentinelPulse('ERROR', `API Audit Failed: ${e.message}`);
    }
}

window.runApiAudit = runApiAudit;
