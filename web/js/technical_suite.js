/**
 * Technical Suite Helper
 * Handles the high-density diagnostic data for the Options and Tools panels.
 */

async function refreshEnvironmentInfo() {
    const viewport = document.getElementById('options-view-env');
    if (!viewport) return;

    viewport.innerHTML = '<div class="loading-fragment">Frage Python-Backend ab...</div>';

    try {
        const info = await eel.get_environment_info()();
        viewport.innerHTML = `
            <div class="glass-card" style="margin-bottom: 20px;">
                <h3 class="diagnostic-section-title">System-Umgebung</h3>
                <div class="diagnostic-label">Python Version</div>
                <div class="diagnostic-value">${info.python_version}</div>
                
                <div class="diagnostic-label">Ausführungsdatei</div>
                <div class="diagnostic-value">${info.python_executable}</div>
                
                <div class="diagnostic-label">Venv / Conda</div>
                <div class="diagnostic-value">${info.env_type} (${info.env_path})</div>
            </div>
            <div id="venv-summary-container">
                <!-- Injected via refreshVenvSummary -->
                <button onclick="refreshVenvSummary()" class="tab-btn" style="width: 100%; margin-top: 10px;">Lade Venv Details...</button>
            </div>
        `;
    } catch (e) {
        viewport.innerHTML = `<div class="error-msg">Fehler beim Laden der Umgebung: ${e}</div>`;
    }
}

async function refreshPipPackages() {
    const viewport = document.getElementById('options-view-pkgs');
    if (!viewport) return;

    viewport.innerHTML = `
        <div style="padding: 20px;">
            <input type="text" id="pip-search" placeholder="Pakete suchen..." oninput="filterPipPackages(this.value)" 
                   style="width: 100%; padding: 12px; border-radius: 8px; background: var(--bg-secondary); border: 1px solid var(--border-color); color: var(--text-primary); margin-bottom: 20px;">
            <div id="pip-list-container" class="loading-fragment">Lade PIP-Liste...</div>
        </div>
    `;

    try {
        const pkgs = await eel.get_pip_packages()();
        window.allPipPackages = pkgs; // Cache for filtering
        renderPipList(pkgs);
    } catch (e) {
        document.getElementById('pip-list-container').innerHTML = `<div class="error-msg">Fehler: ${e}</div>`;
    }
}

function renderPipList(pkgs) {
    const container = document.getElementById('pip-list-container');
    if (!container) return;

    if (pkgs.length === 0) {
        container.innerHTML = 'Keine Pakete gefunden.';
        return;
    }

    container.innerHTML = `
        <table style="width: 100%; border-collapse: collapse; font-size: 12px;">
            <thead style="text-align: left; opacity: 0.6;">
                <tr>
                    <th style="padding: 8px; border-bottom: 1px solid var(--border-color);">Name</th>
                    <th style="padding: 8px; border-bottom: 1px solid var(--border-color);">Version</th>
                </tr>
            </thead>
            <tbody>
                ${pkgs.map(p => `
                    <tr>
                        <td style="padding: 10px 8px; border-bottom: 1px solid var(--border-color); font-weight: 700;">${p.name}</td>
                        <td style="padding: 10px 8px; border-bottom: 1px solid var(--border-color); font-family: monospace;">${p.version}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

function filterPipPackages(query) {
    const filtered = window.allPipPackages.filter(p => p.name.toLowerCase().includes(query.toLowerCase()));
    renderPipList(filtered);
}

async function refreshVenvSummary() {
    const container = document.getElementById('venv-summary-container');
    if (!container) return;

    try {
        if (typeof eel !== 'undefined' && eel.get_venv_summary) {
            const summary = await eel.get_venv_summary()();
            container.innerHTML = `
                <div class="glass-card" style="margin-top: 20px; border-color: var(--accent-color);">
                    <h3 class="diagnostic-section-title">Backend Venv Summary</h3>
                    <pre style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-secondary); white-space: pre-wrap;">${summary}</pre>
                </div>
            `;
        }
    } catch (e) {
        container.innerHTML = `<div class="error-msg">Venv-Fehler: ${e}</div>`;
    }
}

// Initial hooks
document.addEventListener('DOMContentLoaded', () => {
    // Check if we are starting on a specific technical tab
});

// Created with MWV v1.46.00-MASTER
