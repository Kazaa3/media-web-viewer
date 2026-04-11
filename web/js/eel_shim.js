/**
 * Eel Placeholder Shim
 * Provides a robust Proxy-based fallback for the Eel backend when running 
 * in connectionless mode (--n) or when the backend is unavailable.
 */
(function() {
    if (typeof window.eel !== 'undefined' && !window.__eel_missing__) return;

    window.__eel_missing__ = true;

    /**
     * Define default return values for known backend methods to ensure UI stability.
     */
    const backendDefaults = {
        ping: { status: 'offline', message: 'no-backend' },
        get_version: 'offline (shim)',
        get_language: 'de',
        set_language: { status: 'ok' },
        get_library: { media: [] },
        get_db_stats: { total_items: 0, categories: {} },
        get_parser_config: {
            parser_chain: ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"],
            parser_mode: 'lightweight',
            scan_dirs: []
        },
        get_debug_flags: {},
        get_debug_logs: [],
        get_test_suites: [],
        get_test_results: [],
        list_logbook_entries: [],
        list_sql_files: [],
        get_all_parser_info: {},
        get_konsole: { logs: "" },
        get_hardware_info: {},
        report_spawn: () => { console.log('[Eel-Shim] report_spawn called'); },
        report_items_spawned: (count, source) => { console.log(`[Eel-Shim] ${count} items spawned from ${source}`); },
        log_js_error: (err) => { console.error('[Eel-Shim] JS Error Logged:', err); }
    };

    /**
     * Builds a mock result for a given method name.
     */
    function buildMockResult(methodName) {
        if (methodName in backendDefaults) {
            const val = backendDefaults[methodName];
            return (typeof val === 'function') ? val() : val;
        }

        return {
            status: 'error',
            message: `Backend not available in connectionless mode (--n): ${methodName}`
        };
    }

    /**
     * Wraps a mock result in the nested function structure expected by Eel.
     * Eel usage: eel.method_name(args)(callback)
     */
    function buildMockCall(methodName) {
        return function() {
            const args = Array.from(arguments);
            console.debug(`[Eel-Shim] Method called: ${methodName}`, args);
            
            return async function(callback) {
                const result = buildMockResult(methodName);
                if (typeof callback === 'function') {
                    try {
                        callback(result);
                    } catch (e) {
                        console.warn(`[Eel-Shim] Callback execution failed for ${methodName}:`, e);
                    }
                }
                return result;
            };
        };
    }

    /**
     * Create the global Eel proxy.
     */
    window.eel = new Proxy({
        expose: function(fn, name) { 
            console.log(`[Eel-Shim] Function exposed: ${name || fn.name}`); 
        }
    }, {
        get(target, prop) {
            if (prop in target) return target[prop];
            if (prop === 'then') return undefined; // Avoid identifying as promise
            return buildMockCall(String(prop));
        }
    });

    console.warn('[Mode-N] backend not available - running frontend fallback shim.');
})();

// Created with MWV v1.46.00-MASTER
