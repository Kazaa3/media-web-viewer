(function () {
            if (typeof window.eel !== 'undefined') return;

            window.__eel_missing__ = true;

            function buildResult(methodName) {
                const defaults = {
                    ping: { status: 'offline', message: 'no-backend' },
                    get_version: 'offline',
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
                    list_logbook_entries: []
                };

                if (methodName in defaults) {
                    return defaults[methodName];
                }

                return {
                    status: 'error',
                    message: `Backend not available in connectionless mode (--n): ${methodName}`
                };
            }

            function buildCall(methodName) {
                return function () {
                    return async function (callback) {
                        const result = buildResult(methodName);
                        if (typeof callback === 'function') {
                            try {
                                callback(result);
                            } catch (_) {
                                // Ignore callback errors in fallback mode
                            }
                        }
                        return result;
                    };
                };
            }

            window.eel = new Proxy({
                expose: function () { }
            }, {
                get(target, prop) {
                    if (prop in target) return target[prop];
                    return buildCall(String(prop));
                }
            });

            console.warn('[Mode-N] eel.js/backend not available - running frontend fallback shim.');
        })();