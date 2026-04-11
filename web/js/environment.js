/**
 * environment.js - Handles system environment information, versioning, 
 * and configuration logic.
 */

/**
 * Loads environment diagnostics from backend and updates the UI.
 */
async function loadEnvironmentInfo() {
    try {
        if (typeof eel === 'undefined') return;
        
        const res = await eel.get_konsole()();
        const env = res.env || {};
        const tbody = document.getElementById('env-details-table-body');
        
        if (!tbody) {
            console.warn('[Environment] env-details-table-body not found in DOM.');
            return;
        }

        // Clear existing rows
        tbody.innerHTML = '';

        const data = [
            { label: 'Programm-Version', value: res.version || window.MWV_VERSION || '-', icon: '#icon-info' },
            { label: 'Python Version', value: env.python_version || '-', icon: '#icon-generic' },
            { label: 'Venv Status', value: env.env_name || 'System', icon: '#icon-settings' },
            { label: 'Platform', value: env.platform || '-', icon: '#icon-generic' },
            { label: 'Executable', value: env.python_executable || '-', icon: '#icon-folder' },
            { label: 'Working Directory', value: env.cwd || '-', icon: '#icon-folder' },
            { label: 'Main PID', value: env.pid || '-', icon: '#icon-debug' },
            { label: 'Browser PID', value: env.browser_pid || '-', icon: '#icon-debug' },
            { label: 'Testbed PID', value: env.testbed_pid || 'nicht aktiv', icon: '#icon-test' },
            { label: 'Selenium PID', value: env.selenium_pid || 'nicht aktiv', icon: '#icon-test' }
        ];

        data.forEach(item => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td style="padding: 10px; border-bottom: 1px solid var(--border-color); color: var(--text-secondary); width: 220px;">
                    <svg width="12" height="12" style="margin-right: 8px; vertical-align: middle; opacity: 0.6;">
                        <use href="${item.icon}"></use>
                    </svg>
                    ${item.label}
                </td>
                <td style="padding: 10px; border-bottom: 1px solid var(--border-color); font-family: 'JetBrains Mono', monospace; font-size: 0.85em; color: var(--text-primary);">
                    ${item.value}
                </td>
            `;
            tbody.appendChild(row);
        });

        // Update other status elements if they exist
        const geventEl = document.getElementById('env-gevent-status');
        if (geventEl && typeof getGeventStatus === 'function') getGeventStatus();

    } catch (e) {
        console.error('[Environment] Failed to load info:', e);
    }
}

/**
 * Initializes the default media folder selection and browsing logic.
 */
async function initDefaultFolder() {
    try {
        if (typeof eel === 'undefined') return;

        const dir = await eel.get_default_media_dir()();
        const inputs = ['default-folder-input', 'default-folder-input-debug'];
        
        inputs.forEach(id => {
            const el = document.getElementById(id);
            if (el) el.value = dir;
        });

        // Wire up browse buttons
        setupBrowseButton("browse-folder-btn", "default-folder-input", "browse-results");
        setupBrowseButton("browse-folder-btn-debug", "default-folder-input-debug", "browse-results-debug");

        const scanDbg = document.getElementById('scan-btn-debug');
        if (scanDbg && typeof scan === 'function') {
            scanDbg.addEventListener('click', () => scan());
        }

    } catch (e) {
        console.error('[Environment] Could not init default folder:', e);
    }
}

/**
 * Generic helper to wire up browse folder functionality.
 */
function setupBrowseButton(btnId, inputId, resultsId) {
    const btn = document.getElementById(btnId);
    if (!btn) return;

    btn.addEventListener('click', async () => {
        const input = document.getElementById(inputId);
        const path = input ? input.value : null;
        
        try {
            const res = await eel.browse_dir(path)();
            const out = document.getElementById(resultsId);
            
            if (res.error) {
                if (out) out.value = `# Fehler: ${res.error}`;
                else alert(res.error);
            } else {
                if (out) {
                    const lines = (res.items && res.items.length > 0) 
                        ? res.items.map(it => `# ${it.name} [${it.type}] ${it.size ? '(' + it.size + ')' : ''}`)
                        : ['# Kein Inhalt im Verzeichnis'];
                    out.value = lines.join('\n');
                }
            }
        } catch (e) {
            console.error('[Environment] Browse failed:', e);
        }
    });
}

/**
 * Fetches gevent status from backend.
 */
async function getGeventStatus() {
    try {
        if (typeof eel === 'undefined' || typeof eel.get_gevent_status !== 'function') return;
        const res = await eel.get_gevent_status()();
        const el = document.getElementById('env-gevent-status');
        if (el) {
            el.textContent = res.active ? `Active (${res.version})` : 'Inactive';
            el.className = res.active ? 'status-active' : 'status-inactive';
        }
    } catch (e) {
        console.warn('[Environment] Gevent status check failed');
    }
}

// Global initialization hook for environment module
function initEnvironmentModule() {
    loadEnvironmentInfo();
    initDefaultFolder();
}

// Created with MWV v1.46.00-MASTER
