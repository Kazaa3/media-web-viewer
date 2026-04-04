/**
 * Options & Configuration Helpers
 * Extracted from app.html to improve modularity and avoid line-number drift.
 */

/**
 * Loads the startup configuration (browser, flags, env vars).
 */
async function loadStartupConfig() {
    try {
        const config = await eel.get_startup_config()();
        if (config) {
            if (config.browser_choice) {
                safeValue('startup-browser-choice', config.browser_choice);
            }
            if (config.browser_flags) {
                const flags = config.browser_flags || [];
                safeValue('startup-browser-flags', flags.join('\n'));
            }
            if (config.env_vars) {
                let envStr = "";
                for (const [k, v] of Object.entries(config.env_vars)) {
                    envStr += `${k}=${v}\n`;
                }
                safeValue('startup-env-vars', envStr.trim());
            }
        }
    } catch (err) {
        console.error("Error loading startup config:", err);
    }
}

/**
 * Saves the startup configuration.
 */
async function saveStartupConfig() {
    try {
        const choice = readValue('startup-browser-choice', 'default');
        const flagsRaw = readValue('startup-browser-flags', '');
        const envRaw = readValue('startup-env-vars', '');

        const flags = flagsRaw.split('\n').map(f => f.trim()).filter(f => f.length > 0);
        const envVars = {};
        envRaw.split('\n').forEach(line => {
            const parts = line.split('=');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                const value = parts.slice(1).join('=').trim();
                if (key) envVars[key] = value;
            }
        });

        const result = await eel.update_startup_config({
            "browser_choice": choice,
            "browser_flags": flags,
            "env_vars": envVars
        })();

        if (result && result.status === "success") {
            if (typeof showToast === "function") {
                showToast("Startup-Konfiguration gespeichert! Bitte die App neustarten.", "success");
            } else {
                alert("Startup-Konfiguration gespeichert! Bitte die App neustarten.");
            }
        } else {
            alert("Fehler beim Speichern der Konfiguration: " + (result ? result.message : 'Unknown'));
        }
    } catch (err) {
        console.error("Error saving startup config:", err);
        alert("Kritischer Fehler beim Speichern: " + err);
    }
}

/**
 * Loads mock data configuration.
 */
async function loadMockDataConfig() {
    try {
        const enabled = await eel.get_mock_data_enabled()();
        const toggle = document.getElementById('config-mock-data-toggle');
        if (toggle) toggle.checked = enabled;
    } catch (err) {
        console.error("Error loading mock data config:", err);
    }
}

/**
 * Toggles mock data availability.
 */
async function toggleMockData(enabled) {
    try {
        await eel.set_mock_data_enabled(enabled)();
        if (typeof showToast === 'function') {
            showToast(enabled ? "Mock-Daten aktiviert" : "Mock-Daten deaktiviert", "info");
        }
        if (typeof renderLibrary === 'function') renderLibrary();
    } catch (err) {
        console.error("Error toggling mock data:", err);
        if (typeof showToast === 'function') showToast("Fehler beim Ändern der Mock-Daten", "error");
    }
}

/**
 * Saves the parser chain configuration and mode.
 */
function saveParserChainUI() {
    const listItems = document.getElementById('parser-list')?.querySelectorAll('.parser-item') || [];
    const newChain = [];

    listItems.forEach(item => {
        const isActive = item.querySelector('.parser-toggle')?.checked;
        if (isActive) {
            newChain.push(item.dataset.id);
        }
    });

    const modeToggle = document.getElementById('toggle-parser-mode');
    const newMode = (modeToggle && modeToggle.checked) ? "full" : "lightweight";

    // Immediate UI Feedback for Mode
    const statusText = document.getElementById('parser-mode-status');
    if (statusText) {
        // t() is assumed to be the translation helper
        statusText.innerText = newMode === "full" ? (typeof t === 'function' ? t('parser_mode_full') : "Intensiv") : (typeof t === 'function' ? t('parser_mode_light') : "Schnell");
        statusText.style.color = newMode === "full" ? "#e67e22" : "#2a7";
    }

    const indexedCats = [];
    if (typeof cats !== 'undefined') {
        cats.forEach(cat => {
            const cb = document.getElementById('cat-' + cat);
            if (cb && cb.checked) indexedCats.push(cat);
        });
    }

    const finalConfig = {
        ...(typeof currentParserOptions !== 'undefined' ? currentParserOptions : {}),
        "parser_chain": newChain,
        "parser_mode": newMode,
        "indexed_categories": indexedCats,
        "minimal_player_view": (typeof mwv_config !== 'undefined' ? mwv_config.minimal_player_view : false),
        "auto_scan": document.getElementById('config-auto-scan')?.checked || false,
        "debug_console_active": document.getElementById('config-debug-console')?.checked || false,
        "hide_mocks": document.getElementById('config-hide-mocks')?.checked || false
    };

    if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
        eel.update_parser_config(finalConfig)((result) => {
            if (result && result.status === 'ok') {
                const statusSpan = document.getElementById('parser-save-status');
                if (statusSpan) {
                    statusSpan.style.display = 'inline';
                    setTimeout(() => { statusSpan.style.display = 'none'; }, 3000);
                }
            } else {
                console.error("Save failed:", result);
            }
        });
    }
}

/**
 * Updates UI buttons based on app mode.
 */
function updateAppModeButtons() {
    if (typeof mwv_config === 'undefined') return;
    const mode = mwv_config.app_mode || 'High-Performance';
    document.querySelectorAll('[id^="mode-"]').forEach(el => {
        el.style.background = 'var(--bg-secondary)';
        el.style.color = 'var(--text-primary)';
    });
    const target = mode === 'High-Performance' ? 'mode-perf' : 'mode-bw';
    const el = document.getElementById(target);
    if (el) {
        el.style.background = 'var(--accent-color)';
        el.style.color = 'white';
    }
}

/**
 * Updates UI buttons based on parser mode.
 */
function updateParserModeButtons() {
    if (typeof mwv_config === 'undefined') return;
    const mode = mwv_config.parser_mode || 'lightweight';
    document.querySelectorAll('[id^="pm-"]').forEach(el => {
        el.style.background = 'var(--bg-secondary)';
        el.style.color = 'var(--text-primary)';
    });
    let target = 'pm-light';
    if (mode === 'full') target = 'pm-full';
    if (mode === 'ultimate') target = 'pm-ult';
    const el = document.getElementById(target);
    if (el) {
        el.style.background = 'var(--accent-color)';
        el.style.color = 'white';
    }
}

/**
 * Loads the current UI preferences into the Options panel.
 */
function loadOptionsUI() {
    // Sidebar default
    const sidebarDefault = localStorage.getItem('mwv_sidebar_default_open') !== 'false';
    const sidebarToggle = document.getElementById('toggle-sidebar-default');
    if (sidebarToggle) sidebarToggle.checked = sidebarDefault;

    // Visualizer style
    const vizStyle = localStorage.getItem('mwv_visualizer_style') || 'bars';
    const vizSelect = document.getElementById('visualizer-style-select');
    if (vizSelect) vizSelect.value = vizStyle;

    // System & Debug (from global config proxy if available)
    if (typeof PARSER_CONFIG !== 'undefined') {
        safeCheck('config-auto-scan', PARSER_CONFIG.auto_scan);
        safeCheck('config-debug-console', PARSER_CONFIG.debug_console_active);
        safeCheck('config-hide-mocks', PARSER_CONFIG.hide_mocks);
    }
}

/**
 * Helper to safely check a checkbox by id.
 */
function safeCheck(id, val) {
    const el = document.getElementById(id);
    if (el) el.checked = !!val;
}

// Hook into fragment loading or switchTab to initialize options
const originalSwitchOptionsView = window.switchOptionsView;
window.switchOptionsView = function(viewId) {
    if (typeof originalSwitchOptionsView === 'function') originalSwitchOptionsView(viewId);
    loadOptionsUI();
};
