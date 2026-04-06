/**
 * System & Environment Helpers (v1.35.68 Centralized)
 */
let mwv_config = {
    start_page: 'player',
    app_mode: 'High-Performance',
    parser_mode: 'lightweight'
};

async function loadConfig() {
    try {
        // v1.35.68: Prioritize Global Config from backend
        if (window.CONFIG && window.CONFIG.parser_registry) {
            mwv_config = { ...mwv_config, ...window.CONFIG.parser_registry };
            console.log('[Sync] System config hydrated from Centralized Registry.');
            return;
        }
        
        const response = await fetch('config.json');
        if (response.ok) {
            const data = await response.json();
            mwv_config = { ...mwv_config, ...data };
            console.log('Global config loaded from config.json fallback:', mwv_config);
        }
    } catch (e) {
        console.warn('Failed to load config.json:', e);
    }
}

async function checkBackendReachability() {
    const statusText = document.getElementById('rtt-output');
    const container = document.getElementById('rtt-results-container');
    if (container) container.style.display = 'block';
    
    // v1.35.68: Centralized Network Discovery
    const host = window.CONFIG?.network_settings?.bind_address || '127.0.0.1';
    const port = window.location.port || window.CONFIG?.network_settings?.port || '8345';
    
    if (statusText) statusText.innerText = `[Network] Probing ${host}:${port} (Eel Port Bind Check)...`;
    
    try {
        const res = await eel.rtt_ping("localhost_check")();
        if (res && res.status === 'pong') {
            if (statusText) {
                statusText.innerText = `[SUCCESS] Connection to ${host}:${port} is active.\nStatus: Stable\nBackend ID: ${res.pid || 'running'}`;
                statusText.style.color = "#2a7";
            }
        } else {
            throw new Error("Invalid response from internal API");
        }
    } catch (err) {
        if (statusText) {
            statusText.innerText = `[FAILED] ${host}:${port} refused the connection (ERR_CONNECTION_REFUSED).\nError: ${err.message}\n\nTroubleshooting:\n- Backend process might have crashed.\n- Port ${port} is blocked by firewall.\n- Eel server failed to bind to ${host}.`;
            statusText.style.color = "#f44336";
        }
    }
}

async function discoverCastingDevices() {
    const status = document.getElementById('cast-scanner-status');
    const list = document.getElementById('cast-device-list');
    if (status) {
        status.innerText = "SCANNING...";
        status.style.color = "#9c27b0";
    }
    if (list) list.innerText = "Searching for Chromecast & DLNA nodes...";

    try {
        const res = await eel.discover_cast_devices()();
        if (status) {
            status.innerText = "IDLE (Complete)";
            status.style.color = "#2a7";
        }
        if (list) {
            const total = (res.chromecast ? res.chromecast.length : 0) + (res.dlna ? res.dlna.length : 0);
            if (total === 0) {
                list.innerText = "No devices detected in current network segment.";
            } else {
                let html = "<strong>Found Devices:</strong><br>";
                if (res.chromecast) res.chromecast.forEach(d => html += `<svg width="12" height="12"><use href="#icon-generic"></use></svg> Chromecast: ${d.name} (${d.ip})<br>`);
                if (res.dlna) res.dlna.forEach(d => html += `<svg width="12" height="12"><use href="#icon-tv"></use></svg> DLNA: ${d.name} (${d.ip})<br>`);
                list.innerHTML = html;
            }
        }
    } catch (e) {
        if (status) status.innerText = "ERROR";
        if (list) list.innerText = "Casting discovery failed: " + e;
    }
}

async function toggleSwyhRs(enabled) {
    try {
        const res = await eel.toggle_swyh_rs(enabled)();
        if (typeof showToast === 'function') {
            showToast(`SWYH-RS ${res.status === 'ok' ? 'TOGGLED' : 'ERROR'}`, 'info');
        }
    } catch (e) {
        console.error("Failed to toggle SWYH-RS:", e);
    }
}

async function startSpotifyBridge() {
    try {
        if (typeof eel.start_spotify_bridge === 'function') {
            const res = await eel.start_spotify_bridge()();
            showToast("Spotify Bridge Status: " + res.status.toUpperCase(), 'info');
        } else {
            showToast("Spotify Backend nicht verfügbar.", 'error');
        }
    } catch (e) {
        console.error("Spotify Bridge error:", e);
    }
}

async function loadScanDirs() {
    const container = document.getElementById('scan-dirs-list');
    if (!container) return;
    const config = await eel.get_parser_config()();
    const dirs = config.scan_dirs || [];
    const defaultMediaDir = await eel.get_default_media_dir()();

    container.innerHTML = '';
    if (dirs.length === 0) {
        container.innerHTML = `<div style="color: #999; font-style: italic; font-size: 0.9em; padding: 10px; background: #f9f9f9; border-radius: 6px; border: 1px dashed #ddd;">No dirs configured</div>`;
        return;
    }

    dirs.forEach(path => {
        const row = document.createElement('div');
        row.style.cssText = 'display: flex; align-items: center; justify-content: space-between; padding: 10px; background: #f9f9f9; border: 1px solid #eee; border-radius: 6px; font-size: 0.9em;';

        const pathEl = document.createElement('span');
        pathEl.style.cssText = 'font-family: monospace; color: #444; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; margin-right: 10px;';
        pathEl.innerText = path;

        const removeBtn = document.createElement('button');
        removeBtn.innerHTML = 'Remove';
        removeBtn.onclick = async () => {
            const res = await eel.remove_scan_dir(path)();
            if (res.status === 'ok') loadScanDirs();
        };

        row.appendChild(pathEl);
        row.appendChild(removeBtn);
        container.appendChild(row);
    });
}

async function addScanDirUI() {
    const res = await eel.add_scan_dir()();
    if (res.status === 'ok') {
        loadScanDirs();
    }
}

let lastSyncState = 'unknown';

/**
 * Periodically checks the connection to the Eel backend.
 */
async function checkConnection() {
    const indicator = document.getElementById('sync-indicator');
    const dot = document.getElementById('sync-dot');
    const text = document.getElementById('sync-text');

    if (typeof eel === 'undefined' || (window && window.__eel_missing__ === true)) {
        if (typeof safeStyle === 'function') {
            safeStyle('sync-dot', 'background', '#f44');
            safeStyle('sync-indicator', 'background', '#ffebee');
            safeStyle('sync-text', 'color', '#c62828');
        }
        if (typeof safeText === 'function') safeText('sync-text', typeof t === 'function' ? t('sync_offline_no_backend') : 'OFFLINE');
        
        if (lastSyncState !== 'missing-backend') {
            if (typeof appendUiTrace === 'function') appendUiTrace('sync-state: missing backend');
        }
        lastSyncState = 'missing-backend';
        return;
    }

    try {
        const res = await eel.ping()();
        if (res && res.status === 'ok') {
            if (typeof safeStyle === 'function') {
                safeStyle('sync-dot', 'background', '#4CAF50');
                safeStyle('sync-dot', 'boxShadow', '0 0 8px #4CAF50');
                safeStyle('sync-indicator', 'background', '#e8f5e9');
                safeStyle('sync-text', 'color', '#2e7d32');
                safeStyle('vsync-field', 'display', 'block');
            }
            if (typeof safeText === 'function') safeText('sync-text', typeof t === 'function' ? t('sync_synchronized') : 'Synchronized');
            
            if (lastSyncState !== 'ok') {
                if (typeof appendUiTrace === 'function') appendUiTrace('sync-state: synchronized');
            }
            lastSyncState = 'ok';
        } else {
            throw new Error("Invalid response");
        }
    } catch (e) {
        if (typeof safeStyle === 'function') {
            safeStyle('sync-dot', 'background', '#ff9800');
            safeStyle('sync-indicator', 'background', '#fff3e0');
            safeStyle('sync-text', 'color', '#e65100');
        }
        if (typeof safeText === 'function') safeText('sync-text', typeof t === 'function' ? t('sync_connection_lost') : 'Connection Lost');
        
        if (lastSyncState !== 'lost') {
            if (typeof appendUiTrace === 'function') appendUiTrace(`sync-state: connection lost (${e.message || e})`);
        }
        lastSyncState = 'lost';
    }
}

/**
 * Synchronizes version information from the backend to the UI.
 */
async function syncVersionInfo() {
    try {
        if (typeof eel.get_version === 'function') {
            const version = await eel.get_version()();
            const footerVersion = document.getElementById('footer-version');
            if (footerVersion) footerVersion.innerText = `v${version}`;
            const envAppVersionEl = document.getElementById('env-app-version');
            if (envAppVersionEl) envAppVersionEl.textContent = version;
        }
    } catch (err) {
        console.warn('[syncVersionInfo] Failed to fetch version:', err);
    }
}
