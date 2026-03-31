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
function mwv_trace(category, action, details = {}) {
    const timestamp = new Date().toISOString();
    const detailsStr = typeof details === 'string' ? details : JSON.stringify(details);
    
    console.log(`[GWV-TRACE] [${category}] ${action} | ${detailsStr}`);
    
    if (typeof eel !== 'undefined' && typeof eel.log_gui_event === 'function') {
        // We wrap in a promise to not block the UI thread
        eel.log_gui_event(category, action, detailsStr)();
    }
}

/**
 * Attaches global logging to right-click events.
 */
document.addEventListener('contextmenu', (e) => {
    const target = e.target.closest('[id], [class]');
    mwv_trace('UI-INPUT', 'RIGHT-CLICK', {
        targetId: target ? target.id : 'unknown',
        targetClass: target ? target.className : 'none',
        x: e.clientX,
        y: e.clientY
    });
});

// Export for use in other modules if needed (optional)
window.mwv_trace = mwv_trace;
