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
        'logs': 'diag-pane-logs'
    };

    if (paneIds[viewId]) {
        const target = document.getElementById(paneIds[viewId]);
        if (target) target.style.display = 'block';

        // Trigger Data Fetchers
        if (viewId === 'hydration' && typeof renderLogicAuditSummary === 'function') renderLogicAuditSummary();
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
 * SENTINEL: Live Trace Engine
 */
function sentinelPulse(tag, message) {
    const container = document.getElementById('sentinel-log-container');
    if (!container) return;

    const entry = document.createElement('div');
    entry.style.cssText = 'border-bottom:1px solid rgba(0,255,204,0.05); padding:3px 0; display:flex; gap:8px; align-items:flex-start;';
    
    const ts = new Date().toLocaleTimeString('de-DE', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    entry.innerHTML = `
        <span style="opacity:0.3; flex-shrink:0;">[${ts}]</span> 
        <span style="font-weight:900; color:#00ffcc; flex-shrink:0; min-width:40px;">${tag}</span> 
        <span style="opacity:0.8; word-break:break-all;">${message}</span>
    `;

    container.appendChild(entry);
    container.scrollTop = container.scrollHeight;
    while (container.childNodes.length > SENTINEL_MAX_ENTRIES) container.removeChild(container.firstChild);
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
window.performItemJourneyAudit = performItemJourneyAudit;
window.initDiagnosticsSidebar = initDiagnosticsSidebar;
