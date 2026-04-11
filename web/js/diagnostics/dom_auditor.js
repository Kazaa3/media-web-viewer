/**
 * MWV DOM Auditor Logic (v1.35.65)
 * Analyzes the 7-Point Health Check for UI integrity.
 */

window.runDomAudit = function() {
    console.info(">>> [Audit] Starting 7-Point DOM Health Scan...");
    const hud = document.getElementById('dom-auditor-hud');
    if (hud) hud.style.display = 'block';

    const results = document.getElementById('audit-results-list');
    if (!results) return;
    results.innerHTML = '';

    const auditPoints = [
        { id: 'V-1', label: 'Viewport Visibility', check: () => checkVisibility(['player-main-viewport', 'library-main-viewport', 'video-main-viewport']) },
        { id: 'S-2', label: 'Splitter Integrity', check: () => checkSplitters(['main-splitter', 'player-analytics-splitter']) },
        { id: 'C-3', label: 'Context Menu Stack', check: () => checkZIndex('context-menu', 100000) },
        { id: 'F-4', label: 'Fragment Load Status', check: () => checkFragmentLoad(['player_queue.html', 'video_player.html']) },
        { id: 'T-5', label: 'Tab Active Collision', check: () => checkTabCollision() },
        { id: 'L-6', label: 'Layout Offsets', check: () => checkLayoutHeight() },
        { id: 'M-7', label: 'Modal Layering', check: () => checkModalLayering() },
        { id: 'L-8', label: 'Library Parity Audit', check: () => checkLibrarySync() }
    ];

    let healthyCount = 0;
    auditPoints.forEach(point => {
        const res = point.check();
        const item = document.createElement('div');
        item.className = 'audit-item';
        item.innerHTML = `
            <div class="audit-label">${point.label}</div>
            <div class="audit-status ${res.class}">${res.text}</div>
        `;
        results.appendChild(item);
        if (res.healthy) healthyCount++;
    });

    const summary = document.getElementById('audit-summary-text');
    if (summary) {
        summary.innerText = `STATUS: ${healthyCount}/7 HEALTHY`;
        summary.style.color = (healthyCount === 7) ? '#00ff7f' : '#ffa500';
    }
};

function checkVisibility(ids) {
    let visibleCount = 0;
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el && (el.style.display !== 'none' && el.offsetParent !== null)) visibleCount++;
    });
    return visibleCount > 0 ? { text: 'VISUAL-OK', class: 'status-healthy', healthy: true } : { text: 'EMPTY-VIEW', class: 'status-warning', healthy: false };
}

function checkSplitters(ids) {
    let ok = true;
    ids.forEach(id => {
        const el = document.getElementById(id);
        if (el && el.offsetHeight === 0) ok = false;
    });
    return ok ? { text: 'SPLIT-OK', class: 'status-healthy', healthy: true } : { text: 'SPLIT-FAIL', class: 'status-warning', healthy: false };
}

function checkZIndex(id, min) {
    const el = document.getElementById(id);
    if (!el) return { text: 'MISSING', class: 'status-error', healthy: false };
    const z = parseInt(window.getComputedStyle(el).zIndex);
    return z >= min ? { text: 'STACK-OK', class: 'status-healthy', healthy: true } : { text: 'STACK-LOW', class: 'status-warning', healthy: false };
}

function checkFragmentLoad(paths) {
    // Check if any container has children for these paths
    const containers = document.querySelectorAll('.tab-content');
    let loaded = 0;
    containers.forEach(c => { if (c.children.length > 0) loaded++; });
    return loaded >= 1 ? { text: 'FRAG-OK', class: 'status-healthy', healthy: true } : { text: 'FRAG-EMPTY', class: 'status-error', healthy: false };
}

function checkTabCollision() {
    const activeTabs = document.querySelectorAll('.tab-content.active');
    return activeTabs.length === 1 ? { text: 'SYNC-OK', class: 'status-healthy', healthy: true } : { text: 'COLLISION', class: 'status-warning', healthy: false };
}

function checkLayoutHeight() {
    const container = document.getElementById('main-split-container');
    if (!container) return { text: 'NO-CONTAINER', class: 'status-error', healthy: false };
    const h = container.offsetHeight;
    return h > 100 ? { text: 'LAYOUT-OK', class: 'status-healthy', healthy: true } : { text: 'COLLAPSED', class: 'status-warning', healthy: false };
}

function checkModalLayering() {
    const modals = document.querySelectorAll('.modal');
    let visible = 0;
    modals.forEach(m => { if (m.style.display === 'flex') visible++; });
    return visible <= 1 ? { text: 'LAYER-OK', class: 'status-healthy', healthy: true } : { text: 'MODAL-STUCK', class: 'status-warning', healthy: false };
}

function checkLibrarySync() {
    const dbCount = window.__mwv_last_db_count || 0;
    const guiCount = (window.allLibraryItems || []).length;
    
    if (dbCount > 0 && guiCount === 0) {
        return { text: 'BLACK-HOLE', class: 'status-error', healthy: false };
    }
    if (dbCount > 0 && guiCount < dbCount) {
        return { text: `PARTIAL: ${guiCount}/${dbCount}`, class: 'status-warning', healthy: false };
    }
    return { text: `SYNC: ${guiCount}`, class: 'status-healthy', healthy: true };
}
