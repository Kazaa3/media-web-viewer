/**
 * Trace Helpers (v1.34)
 * Provides centralized GUI interaction logging to the backend.
 */

/**
 * Sends a trace event to the backend.
 * @param {string} category - Log category (e.g., 'NAV', 'MODAL', 'ACTION')
 * @param {string} action - The specific interaction
 * @param {object|string} [details] - Optional extra metadata
 */
/**
 * Sends a trace event to the backend and the local DOM console.
 * @param {string} category - Log category (e.g., 'NAV', 'MODAL', 'ACTION')
 * @param {string} action - The specific interaction
 * @param {object|string} [details] - Optional extra metadata
 */
function mwv_trace(category, action, details = {}) {
    const timestamp = new Date().toLocaleTimeString();
    let detailsStr = '';
    if (typeof details === 'string') {
        detailsStr = details;
    } else if (details && typeof details === 'object' && Object.keys(details).length > 0) {
        detailsStr = JSON.stringify(details);
    }
    // Log to Browser Console (compact if no details)
    if (detailsStr) {
        console.log(`[GWV-TRACE] [${category}] ${action} | ${detailsStr}`);
    } else {
        console.log(`[GWV-TRACE] [${category}] ${action}`);
    }
    // Log to DOM Console
    appendUiTrace(`[${timestamp}] [${category}] ${action}${detailsStr ? ': ' + detailsStr : ''}`, category);
    if (typeof eel !== 'undefined' && typeof eel.log_ui_event === 'function') {
        eel.log_ui_event(category, action, detailsStr)();
    }
}

/**
 * Appends a message to the on-screen debug console.
 */
function appendUiTrace(msg, category = 'INFO') {
    const container = document.getElementById('debug-trace-content');
    if (!container) return;

    const div = document.createElement('div');
    div.style.marginBottom = '4px';
    div.style.borderLeft = '2px solid rgba(255,255,255,0.1)';
    div.style.paddingLeft = '8px';
    
    // Color coding
    if (category.includes('ERROR') || category.includes('CRITICAL')) div.style.color = '#e74c3c';
    else if (category.includes('WARN')) div.style.color = '#f1c40f';
    else if (category.includes('SUCCESS')) div.style.color = '#2ecc71';
    else if (category.includes('UI')) div.style.color = '#3498db';
    else if (category.includes('DB')) div.style.color = '#9b59b6';

    div.innerText = msg;
    container.appendChild(div);
    container.scrollTop = container.scrollHeight;
}

/**
 * Global toggle for the debug console visibility.
 */
function toggleDebugConsole() {
    const overlay = document.getElementById('debug-trace-overlay');
    if (overlay) {
        const isHidden = overlay.style.display === 'none';
        overlay.style.display = isHidden ? 'flex' : 'none';
        if (isHidden) appendUiTrace("[System] Console Visibility: ON", "SUCCESS");
    }
}

/**
 * Clears the debug console content.
 */
function clearUiTrace() {
    const container = document.getElementById('debug-trace-content');
    if (container) container.innerHTML = '<div style="color: #9b59b6;">[System] Console Cleared.</div>';
}

// Expose to backend
if (typeof eel !== 'undefined') {
    eel.expose(appendUiTrace, 'append_debug_log');
}

/**
 * Attaches global logging to all click events.
 */
document.addEventListener('click', (e) => {
    const target = e.target.closest('button, a, .tab-btn, .nav-item, .sub-pill-btn, [id]');
    if (!target) return;

    const metadata = {
        id: target.id || 'anonymous',
        class: target.className || '',
        text: target.innerText ? target.innerText.trim().substring(0, 30) : '',
        tag: target.tagName,
        x: Math.round(e.clientX),
        y: Math.round(e.clientY)
    };

    mwv_trace('UI-INPUT', 'CLICK', metadata);
});

/**
 * Attaches global logging to right-click events.
 */
document.addEventListener('contextmenu', (e) => {
    const target = e.target.closest('[id], [class]');
    mwv_trace('UI-INPUT', 'RIGHT-CLICK', {
        targetId: target ? target.id : 'unknown',
        targetClass: target ? target.className : 'none',
        x: Math.round(e.clientX),
        y: Math.round(e.clientY)
    });
});

// Export for use in other modules if needed (optional)
window.mwv_trace = mwv_trace;

/**
 * Advanced Render Trace (v1.35)
 * Specialized logging for multi-stage DOM rendering.
 */
function mwv_trace_render(component, stage, metadata = {}) {
    const msg = `[UI-RENDER] [${component}] ${stage} | ${JSON.stringify(metadata)}`;
    console.info(msg);
    if (typeof mwv_trace === 'function') {
        mwv_trace('DOM-UI', stage, metadata);
    }
}

/**
 * Fragment Script Execution Guard (v1.35)
 * Call this from within fragments to report initialization success/failure.
 */
function log_js_error(error, context) {
    const msg = `[JS-ERROR] [${context}] ${error.message || error}`;
    console.error(msg);
    if (typeof mwv_trace === 'function') {
        mwv_trace('JS-ERROR', context, { message: error.message || error, stack: error.stack });
    }
}

window.log_js_error = log_js_error;
window.mwv_trace_render = mwv_trace_render;
