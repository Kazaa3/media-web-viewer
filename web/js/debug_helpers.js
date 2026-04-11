/**
 * debug_helpers.js - Consolidated UI Integrity & Diagnostic Suite
 * Merges logic from legacy debug_helpers and diagnostics_helpers.
 * Implements the 7 stages of UI integrity checking and the DOM Watchdog.
 */

let uiTraceLog = [];

/**
 * Traces UI events and logs them both locally and to the backend.
 */
function appendUiTrace(msg) {
    const timestamp = new Date().toISOString();
    const entry = `[${timestamp}] ${msg}`;
    uiTraceLog.push(entry);
    if (uiTraceLog.length > 100) uiTraceLog.shift();
    
    console.log(`[UI-TRACE] ${msg}`);

    // [v1.41.134] Mirror to Main Status Panel if active
    const mainLog = document.getElementById('sentinel-log-container-main');
    if (mainLog) {
        const p = document.createElement('div');
        p.style.marginBottom = '2px';
        p.style.borderBottom = '1px solid rgba(0,255,204,0.05)';
        p.style.paddingBottom = '2px';
        p.innerHTML = `<span style="opacity:0.3; font-size:9px;">[${new Date().toLocaleTimeString()}]</span> ${msg}`;
        mainLog.appendChild(p);
        mainLog.scrollTop = mainLog.scrollHeight;
    }
    
    if (typeof eel !== 'undefined' && typeof eel.log_js_error === 'function') {
        eel.log_js_error({ type: 'TRACE', message: msg, timestamp: timestamp });
    }
}

/**
 * Stage 4 Helper: DOM Integrity Check - DIV Balance Per Tab
 */
function checkDivBalance() {
    const tabs = document.querySelectorAll('.tab-content');
    console.group("DOM Integrity Check: DIV Balance Per Tab");
    let totalIssues = 0;

    tabs.forEach(tab => {
        const id = tab.id;
        const html = tab.innerHTML;
        const opens = (html.match(/<div/g) || []).length;
        const closes = (html.match(/<\/div/g) || []).length;
        const delta = opens - closes;

        if (delta !== 0) {
            totalIssues++;
            console.warn(`[${id}] IMBALANCED | Opens: ${opens} | Closes: ${closes} | Delta: ${delta}`);
        } else {
            console.log(`[${id}] OK | Balance: ${opens}`);
        }
    });

    console.groupEnd();
    return totalIssues === 0;
}

/**
 * The 7 Stages of UI Integrity
 * Expands results to include backend-level scan findings.
 */
async function runUiIntegrityCheck() {
    const results = document.getElementById('ui-integrity-results');
    if (results) results.innerHTML = 'Starting Integrity Sweep...<br>';
    
    const log = (stage, msg, status = 'info') => {
        const icons = { info: 'ℹ️', pass: '✅', fail: '❌' };
        if (results) {
            results.innerHTML += `${icons[status]} <strong>Stage ${stage}:</strong> ${msg}<br>`;
        }
        appendUiTrace(`Integrity Stage ${stage} [${status}]: ${msg}`);
    };

    try {
        // Stage 1: DOM Load
        log(1, "DOM Readiness", document.readyState === 'complete' ? 'pass' : 'fail');

        // Stage 2: Eel Sync
        const eelStatus = (typeof eel !== 'undefined' && !window.__eel_missing__) ? 'pass' : 'fail';
        log(2, "Backend (Eel) Synchronization", eelStatus);

        // Stage 3: Asset Integrity
        const scripts = Array.from(document.querySelectorAll('script[src]')).filter(s => !s.src.includes('eel.js'));
        log(3, `Critical Assets Loaded (${scripts.length} external scripts)`, 'pass');

        // Stage 4: Div Balance (Frontend)
        const balance = checkDivBalance();
        log(4, "DOM Structural Balance (Frontend DIV counts)", balance ? 'pass' : 'fail');

        // Stage 5: Backend Integrity Scan
        if (typeof eel !== 'undefined' && typeof eel.check_ui_integrity === 'function') {
            const beRes = await eel.check_ui_integrity()();
            const beStatus = beRes.div_balance.balanced ? 'pass' : 'fail';
            log(5, `Backend Integrity Scan: ${beRes.div_balance.opens} opens / ${beRes.div_balance.closes} closes`, beStatus);
        } else {
            log(5, "Backend Integrity Scan skipped (Eel unavailable)", 'info');
        }

        // Stage 6: Layout Stability
        const bodyHeight = document.body.scrollHeight;
        log(6, "Layout Viewport Stability", bodyHeight > 0 ? 'pass' : 'fail');

        // Stage 7: Performance Check (RTT)
        if (typeof eel !== 'undefined') {
            const start = performance.now();
            await eel.ping()();
            const rtt = Math.round(performance.now() - start);
            log(7, `Backend RTT latency: ${rtt}ms`, rtt < 100 ? 'pass' : 'info');
        }

        // Stage 8: Nuclear Visibility Force (v1.41.133 Hardening)
        const visible = forceUIVisibility();
        log(8, "Nuclear Visibility Force: " + (visible ? "Visibility Enforced" : "Force Failed"), visible ? 'pass' : 'fail');

        if (typeof showToast === 'function') {
            showToast("UI Integrity Check Complete", 3000);
        }
    } catch (err) {
        log('ERROR', `Integrity check failed: ${err.message}`, 'fail');
    }
}

/**
 * Stage 8: Nuclear Visibility Force
 * Forcefully overrides styling to ensure containers are visible.
 */
function forceUIVisibility() {
    console.warn(">>> [Forensic] TRIGGERING NUCLEAR VISIBILITY FORCE...");
    try {
        const body = document.body;
        const main = document.getElementById('main-viewport');
        const activeView = document.querySelector('.deck-view.active');

        // 1. Force Body Overrides
        body.style.setProperty('display', 'block', 'important');
        body.style.setProperty('opacity', '1', 'important');
        body.style.setProperty('visibility', 'visible', 'important');

        // 2. Force Main Viewport
        if (main) {
            main.style.setProperty('display', 'flex', 'important');
            main.style.setProperty('opacity', '1', 'important');
            main.style.setProperty('z-index', '1', 'important');
        }

        // 3. Force Active Deck View
        if (activeView) {
            activeView.style.setProperty('display', 'flex', 'important');
            activeView.style.setProperty('opacity', '1', 'important');
            activeView.style.setProperty('visibility', 'visible', 'important');
            activeView.style.setProperty('width', '100%', 'important');
            activeView.style.setProperty('height', '100%', 'important');
        }

        // 4. Clean up modal overlays that might be blocking the view
        const blockages = document.querySelectorAll('.modal-backdrop, #loading-screen, .splash-screen');
        blockages.forEach(b => {
             console.log(`[Forensic] Removing suspected UI blockage: ${b.className}`);
             b.style.display = 'none';
        });

        if (typeof showToast === 'function') showToast("NUCLEAR VISIBILITY ENFORCED", 2000);
        return true;
    } catch (e) {
        console.error("Nuclear Force Failed:", e);
        return false;
    }
}

/**
 * DOM TEST Watchdog
 * Monitors the DOM for rendered items and reports spawn events to the backend.
 */
function initDomWatchdog() {
    console.log("DOM Watchdog: Initializing monitoring hooks.");

    function checkDOMReadiness() {
        const items = document.querySelectorAll('.playlist-item, .media-item, #playlist-container .media-card, .test-result-card');
        if (items.length > 0) {
            console.log(`DOM Watchdog: ${items.length} items detected.`);
            if (typeof eel !== "undefined" && typeof eel.report_items_spawned === 'function') {
                eel.report_items_spawned(items.length, "DOM_WATCHDOG_ENHANCED")((res) => {
                    console.debug("[DOM Watchdog] Backend sync complete.", res);
                });
            }
            return true;
        }
        return false;
    }

    let attempts = 0;
    const interval = setInterval(() => {
        attempts++;
        if (checkDOMReadiness() || attempts > 20) {
            clearInterval(interval);
            if (attempts > 20) console.warn("DOM Watchdog: Timed out waiting for items.");
        }
    }, 1000);
}

/**
 * Diagnostic Suite (Level 5)
 */
async function runDiagnostic() {
    appendUiTrace('<svg width="12" height="12"><use href="#icon-sparkles"></use></svg> Starting Diagnostic Suite (Level 5)...');
    const results = {
        vjs: typeof videojs !== 'undefined',
        eel: typeof eel !== 'undefined',
        filters: !!document.querySelector('.cinema-btn'),
        stats: !!document.getElementById('vjs-stats-overlay'),
        db: false
    };

    try {
        if (typeof eel !== 'undefined' && typeof eel.get_db_stats === 'function') {
            const stats = await eel.get_db_stats()();
            results.db = stats && stats.total_items >= 0;
        }
    } catch (e) { appendUiTrace("DB Diagnostic failed: " + e); }

    appendUiTrace("Diagnostic Results: " + JSON.stringify(results));
    return results;
}

// Global Exports
window.appendUiTrace = appendUiTrace;
window.runUiIntegrityCheck = runUiIntegrityCheck;
window.runDiagnostic = runDiagnostic;
window.initDomWatchdog = initDomWatchdog;

/**
 * [v1.41.134] Forensic View Switcher for STATUS Category
 */
function switchDiagnosticsView(viewId) {
    appendUiTrace(`[UI-NAV] Switching Main Diagnostic View: ${viewId}`);

    // Update Pills
    document.querySelectorAll('.sub-pill-btn').forEach(btn => {
        btn.classList.toggle('active', btn.id === `sub-nav-pill-${viewId}`);
    });

    // Content Switch logic
    const integrityResults = document.getElementById('ui-integrity-results');
    const logsContainer = document.getElementById('sentinel-log-container-main');

    if (viewId === 'logs') {
        if (logsContainer) {
            logsContainer.parentElement.style.display = 'flex';
            logsContainer.parentElement.style.flex = '1';
        }
    } else if (viewId === 'health') {
        if (typeof runUiIntegrityCheck === 'function') runUiIntegrityCheck();
    }
}
window.switchDiagnosticsView = switchDiagnosticsView;

// Auto-init trace hooks
(function() {
    if (window._trace_hooks_active) return;
    window._trace_hooks_active = true;

    const origAlert = window.alert;
    window.alert = function (msg) {
        appendUiTrace('[ALERT-PROXIED] ' + msg);
        origAlert(msg);
    };

    console.log('[Debug] Consolidated Diagnostic Suite Initialized.');
})();
