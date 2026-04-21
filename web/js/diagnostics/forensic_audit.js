/**
 * Forensic DOM Audit Tool (v1.37.29)
 * Performs a deep audit of the UI state and reports to the backend.
 * Run this from the browser console or via an automated trigger.
 */

(function runForensicAudit() {
    console.warn(">>> [FORENSIC-AUDIT] Starting Deep UI Integrity Check...");
    const report = {
        timestamp: new Date().toISOString(),
        containers: {},
        counts: {},
        errors: []
    };

    // 1. Container Audit
    const criticalContainers = [
        'master-header-container',
        'main-sidebar',
        'layout-container',
        'coverflow-track',
        'grid-container',
        'footer-persistent-player'
    ];

    criticalContainers.forEach(id => {
        const el = document.getElementById(id);
        if (!el) {
            report.containers[id] = "MISSING";
            report.errors.push(`CRITICAL: Container #${id} is missing from DOM.`);
        } else {
            const style = window.getComputedStyle(el);
            report.containers[id] = {
                display: style.display,
                visibility: style.visibility,
                opacity: style.opacity,
                rect: el.getBoundingClientRect()
            };
            if (style.display === 'none') {
                report.errors.push(`WARNING: Container #${id} is hidden (display: none).`);
            }
        }
    });

    // 2. Data Hydration Audit
    report.counts.library_memory = (window.__mwv_all_library_items || []).length;
    report.counts.coverflow_items = document.querySelectorAll('.coverflow-item').length;
    report.counts.grid_items = document.querySelectorAll('.grid-item').length;
    
    if (report.counts.library_memory > 0 && report.counts.coverflow_items === 0 && report.counts.grid_items === 0) {
        report.errors.push("CRITICAL: Data exists in memory but NOT in the DOM. Render failure likely.");
    }

    // 3. Global State Audit
    report.state = {
        category_map_ready: (typeof CATEGORY_MAP !== 'undefined' && Object.keys(CATEGORY_MAP).length > 0),
        eel_bridge: (typeof eel !== 'undefined'),
        current_filter: (typeof libraryFilter !== 'undefined' ? libraryFilter : 'N/A')
    };

    console.table(report.containers);
    console.log("[AUDIT-REPORT]", report);

    // Report back to backend via eel.ui_trace if available
    if (typeof eel !== 'undefined' && typeof eel.ui_trace === 'function') {
        eel.ui_trace(`[FORENSIC-AUDIT] Result: ${report.errors.length} errors found. ${report.counts.library_memory} items in memory.`)();
    }

    return report;
})();
