/**
 * sidebar_controller.js - v1.37.10
 * Orchestrates the modular Global Diagnostics Overlay Sidebar.
 */

const SENTINEL_MAX_ENTRIES = 100;

function initDiagnosticsSidebar() {
    console.info("[DIAG-CTRL] Initializing Sidebar Controller...");
    
    // Auto-populate hydration on init if that's the active tab
    if (typeof renderLogicAuditSummary === 'function') {
        renderLogicAuditSummary();
    }
    
    // Hook into mwv_trace if possible
    const originalTrace = window.mwv_trace;
    window.mwv_trace = function(tag, stage, data) {
        if (originalTrace) originalTrace(tag, stage, data);
        sentinelPulse(tag, `${stage} - ${JSON.stringify(data)}`);
    };

    sentinelPulse('SYSTEM', 'Sentinel Live-Trace Engine Initialized.');
}

/**
 * SENTINEL: The Listener
 * Pushes a live event into the SENTINEL log viewport.
 */
function sentinelPulse(tag, message) {
    const container = document.getElementById('sentinel-log-container');
    if (!container) return;

    const now = new Date();
    const ts = now.getHours().toString().padStart(2, '0') + ':' + 
               now.getMinutes().toString().padStart(2, '0') + ':' + 
               now.getSeconds().toString().padStart(2, '0') + '.' + 
               now.getMilliseconds().toString().padStart(3, '0');

    const entry = document.createElement('div');
    entry.className = 'sentinel-entry';
    entry.innerHTML = `
        <span class="sentinel-ts">[${ts}]</span>
        <span class="sentinel-tag">${tag}</span>
        <span class="sentinel-msg">${message}</span>
    `;

    container.appendChild(entry);

    // Auto-scroll logic
    container.scrollTop = container.scrollHeight;

    // Cap entries
    while (container.childNodes.length > SENTINEL_MAX_ENTRIES) {
        container.removeChild(container.firstChild);
    }
}

function clearSentinelLog() {
    const container = document.getElementById('sentinel-log-container');
    if (container) container.innerHTML = '<div style="opacity: 0.5;">[CLEAR] Log wiped by user.</div>';
}

// Global hook for external pulses (e.g. from main.py via eel)
window.sentinelPulse = sentinelPulse;

/**
 * Enhanced Tab Switching for Modular Layout
 */
function switchDiagnosticsSidebarTab(viewId, btn) {
    console.debug(`[DIAG-CTRL] Switching to: ${viewId}`);
    
    // 1. Update Buttons
    if (btn) {
        const nav = btn.parentElement;
        nav.querySelectorAll('.side-reiter').forEach(el => el.classList.remove('active'));
        btn.classList.add('active');
    }

    // 2. Hide all panes
    document.querySelectorAll('.diag-pane').forEach(p => p.style.display = 'none');

    // 3. Show target pane or handle legacy types
    const paneIds = {
        'hydration': 'diag-pane-hydration',
        'item-track': 'diag-pane-item-track',
        'sentinel': 'diag-pane-sentinel'
    };

    if (paneIds[viewId]) {
        const target = document.getElementById(paneIds[viewId]);
        if (target) target.style.display = 'block';

        // Lazy initialization per tab
        if (viewId === 'hydration' && typeof renderLogicAuditSummary === 'function') renderLogicAuditSummary();
        if (viewId === 'item-track' && typeof renderItemTrackTab === 'function') renderItemTrackTab();
    } else {
        // Fallback for original diagnostic views (legacy redirection)
        const legacyPane = document.getElementById('diag-pane-legacy');
        if (legacyPane) {
            legacyPane.style.display = 'block';
            if (typeof switchDiagnosticsSubView === 'function') {
               // This allows the user to still use original tabs (Overview, Logs, etc.)
               // if they are mapped to specific screens.
               // We keep them functional by delegating to the old ui_nav_helpers.
               switchDiagnosticsSubView(viewId);
            }
        }
    }
    
    // Persist view state
    localStorage.setItem('mwv_diag_view', viewId);
}

// Ensure global visibility
window.switchDiagnosticsSidebarTab = switchDiagnosticsSidebarTab;
window.clearSentinelLog = clearSentinelLog;
