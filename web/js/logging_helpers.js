/**
 * Logging & Error Handling Helpers
 * Centralizes all frontend error capture, UI diagnostics, and 
 * backend log synchronization.
 */
(function() {
    /**
     * Log an error to the dashboard console and the backend.
     * @param {Object} errObj - Unified error object.
     */
    function logToBackend(errObj) {
        console.error('[GUI-INTEGRITY] Uncaught Error detected:', errObj);
        
        if (typeof eel !== 'undefined' && typeof eel.log_js_error === 'function') {
            try {
                eel.log_js_error(errObj);
            } catch (e) {
                console.warn('[Logging] Backend synchronization failed:', e);
            }
        }
    }

    /**
     * Unified error handler for window.onerror.
     */
    window.onerror = function (msg, url, line, col, error) {
        const err = {
            message: msg,
            source: url,
            lineno: line,
            colno: col,
            stack: error ? error.stack : 'no-stack',
            ua: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        logToBackend(err);
        return false;
    };

    /**
     * Unified promise rejection handler.
     */
    window.onunhandledrejection = function (event) {
        const err = {
            message: event.reason ? event.reason.message : 'Unhandled Rejection',
            source: 'promise',
            stack: event.reason ? event.reason.stack : 'no-stack',
            ua: navigator.userAgent,
            timestamp: new Date().toISOString()
        };
        logToBackend(err);
    };

    /**
     * Exposed Logger interface for manual application logs.
     */
    window.Logger = {
        info: (msg, details) => { console.log(`[INFO] ${msg}`, details); },
        warn: (msg, details) => { console.warn(`[WARN] ${msg}`, details); },
        error: (msg, details) => { 
            const err = { message: msg, details, source: 'app', timestamp: new Date().toISOString() };
            logToBackend(err);
        }
    };

    console.log('[Logging] Error & diagnostics layer initialized.');
})();

// Created with MWV v1.46.00-MASTER
