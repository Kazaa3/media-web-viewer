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
        
        // Map backend env data to DOM elements
        const mappings = {
            'env-python-version': env.python_version,
            'env-venv-status': env.env_name,
            'env-platform': env.platform,
            'env-python-exec': env.python_executable,
            'env-venv-path': env.env_path,
            'env-main-pid': env.pid,
            'env-app-version': res.version || '-',
            'env-gui-status': 'Active (Eel)',
            'env-browser-pid': env.browser_pid || '-'
        };

        for (const [id, value] of Object.entries(mappings)) {
            const el = document.getElementById(id);
            if (el) el.textContent = value || '-';
        }

        // Special handling for PIDs and status icons
        const testbedPid = document.getElementById('env-testbed-pid');
        if (testbedPid) {
            testbedPid.textContent = (env.testbed_pid !== undefined && env.testbed_pid !== null) 
                ? env.testbed_pid : 'nicht aktiv';
        }

        const seleniumPid = document.getElementById('env-selenium-pid');
        if (seleniumPid) {
            seleniumPid.textContent = (env.selenium_pid !== undefined && env.selenium_pid !== null) 
                ? env.selenium_pid : 'nicht aktiv';
        }

        // gevent / bottle status
        if (typeof getGeventStatus === 'function') getGeventStatus();

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
