/**
 * options_helpers.js — Full Options Panel Logic (v1.34)
 * Manages all PARSER_CONFIG settings exposed in the Tools sub-tabs.
 */

// ─── Knwn constants ───────────────────────────────────────────────────────────
const ALL_CATEGORIES = [
    'audio', 'video', 'images', 'documents', 'ebooks',
    'abbild', 'spiel', 'beigabe', 'supplements', 'games'
];

const ALL_PARSERS = [
    { id: 'filename',     label: 'Filename',     slow: false },
    { id: 'container',    label: 'Container',     slow: false },
    { id: 'mutagen',      label: 'Mutagen',       slow: false },
    { id: 'pymediainfo',  label: 'PyMediaInfo',   slow: false },
    { id: 'ffprobe',      label: 'FFprobe',       slow: false },
    { id: 'ffmpeg',       label: 'FFmpeg',        slow: false },
    { id: 'tinytag',      label: 'TinyTag',       slow: false },
    { id: 'eyed3',        label: 'EyeD3',         slow: false },
    { id: 'music_tag',    label: 'Music Tag',     slow: false },
    { id: 'isoparser',    label: 'ISOparser',     slow: true  },
    { id: 'pycdlib',      label: 'PyCDLib',       slow: true  },
    { id: 'ebml',         label: 'EBML',          slow: true  },
    { id: 'mkvparse',     label: 'MKVparse',      slow: true  },
    { id: 'enzyme',       label: 'Enzyme',        slow: true  },
    { id: 'pymkv',        label: 'PyMKV',         slow: true  },
];

const ALL_DEBUG_FLAGS = [
    'system', 'ui', 'lib', 'browser', 'edit', 'options', 'start',
    'parser', 'scan', 'player', 'db', 'tests', 'api', 'web',
    'i18n', 'websocket', 'performance', 'metadata', 'transcode',
    'file_ops', 'network'
];

const ALL_FEATURE_FLAGS = [
    { key: 'experimental_transcoding', label: 'Experimentelles Transcoding' },
    { key: 'verbose_parsing',          label: 'Verbose Parsing' },
    { key: 'show_test_tab',            label: 'Test-Tab anzeigen' },
    { key: 'analyse_mode',             label: 'Analyse-Modus' },
    { key: 'write_mode',               label: 'Schreib-Modus (Metadaten)' },
];

// ─── Sub-tab navigation ───────────────────────────────────────────────────────
function switchOptionsSubTab(tabId) {
    document.querySelectorAll('.options-sub-tab').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.options-sub-tab-btn').forEach(btn => btn.classList.remove('active'));

    const target = document.getElementById(tabId);
    if (target) target.style.display = 'flex';

    const btn = document.querySelector(`.options-sub-tab-btn[data-tab="${tabId}"]`);
    if (btn) btn.classList.add('active');

    localStorage.setItem('mwv_options_sub_tab', tabId);
}

// ─── Dynamic UI builders ───────────────────────────────────────────────────────
function buildParserChainUI(chain, slowParsers) {
    const container = document.getElementById('opt-parser-chain-list');
    if (!container) return;
    container.innerHTML = '';
    ALL_PARSERS.forEach(p => {
        const isSlow = p.slow || (slowParsers || []).includes(p.id);
        const isEnabled = (chain || []).includes(p.id);
        const div = document.createElement('div');
        div.style.cssText = 'display:flex; align-items:center; justify-content:space-between; padding:8px 12px; background:var(--bg-secondary); border-radius:8px;';
        div.innerHTML = `
            <div style="font-size:12px; font-weight:700; color:var(--text-primary);">
                ${isSlow ? '<span style="color:#e67e22;">●</span> ' : ''}${p.label}
                ${isSlow ? '<span style="font-size:9px; color:var(--text-secondary); font-weight:400;">(langsam)</span>' : ''}
            </div>
            <label class="switch sm"><input type="checkbox" id="parser-${p.id}" ${isEnabled ? 'checked' : ''} onchange="saveAllOptions()"><span class="slider"></span></label>
        `;
        container.appendChild(div);
    });
}

function buildCategoryGrid(containerId, selectedCats) {
    const container = document.getElementById(containerId);
    if (!container) return;
    container.innerHTML = '';
    const labels = {
        audio: '🎵 Audio', video: '🎬 Video', images: '🖼 Bilder',
        documents: '📄 Dokumente', ebooks: '📚 E-Books', abbild: '💿 Abbilder',
        spiel: '🎮 Spiele', beigabe: '📦 Beigaben', supplements: '➕ Supplements', games: '🕹 Games'
    };
    ALL_CATEGORIES.forEach(cat => {
        const isChecked = (selectedCats || []).includes(cat);
        const div = document.createElement('div');
        div.style.cssText = 'display:flex; align-items:center; gap:8px; padding:8px 12px; background:var(--bg-secondary); border-radius:8px;';
        div.innerHTML = `
            <label class="switch sm"><input type="checkbox" id="${containerId}-${cat}" ${isChecked ? 'checked' : ''} onchange="saveAllOptions()"><span class="slider"></span></label>
            <div style="font-size:12px; font-weight:700; color:var(--text-primary);">${labels[cat] || cat}</div>
        `;
        container.appendChild(div);
    });
}

function buildDebugFlagsUI(flags) {
    const container = document.getElementById('opt-debug-flags');
    if (!container) return;
    container.innerHTML = '';
    ALL_DEBUG_FLAGS.forEach(flag => {
        const isOn = flags && flags[flag];
        const div = document.createElement('div');
        div.style.cssText = 'display:flex; align-items:center; gap:8px; padding:8px 10px; background:var(--bg-secondary); border-radius:8px;';
        div.innerHTML = `
            <label class="switch sm"><input type="checkbox" id="dbg-${flag}" ${isOn ? 'checked' : ''} onchange="saveAllOptions()"><span class="slider"></span></label>
            <div style="font-size:11px; font-weight:700; color:var(--text-primary); font-family:monospace;">${flag}</div>
        `;
        container.appendChild(div);
    });
}

function buildFeatureFlagsUI(flags) {
    const container = document.getElementById('opt-feature-flags');
    if (!container) return;
    container.innerHTML = '';
    ALL_FEATURE_FLAGS.forEach(f => {
        const isOn = flags && flags[f.key];
        const div = document.createElement('div');
        div.style.cssText = 'display:flex; align-items:center; justify-content:space-between; padding:10px 12px; background:var(--bg-secondary); border-radius:8px;';
        div.innerHTML = `
            <div style="font-size:12px; font-weight:700; color:var(--text-primary);">${f.label}</div>
            <label class="switch sm"><input type="checkbox" id="feat-${f.key}" ${isOn ? 'checked' : ''} onchange="saveAllOptions()"><span class="slider"></span></label>
        `;
        container.appendChild(div);
    });
}

function buildExtraDirsUI(dirs) {
    const container = document.getElementById('opt-extra-dirs-list');
    if (!container) return;
    container.innerHTML = '';
    (dirs || []).forEach((dir, idx) => {
        const div = document.createElement('div');
        div.style.cssText = 'display:flex; gap:8px; align-items:center;';
        div.innerHTML = `
            <div style="flex:1; padding:6px 10px; background:var(--bg-secondary); border-radius:6px; font-size:11px; font-family:monospace; color:var(--text-secondary); overflow:hidden; text-overflow:ellipsis; white-space:nowrap;">${dir}</div>
            <button onclick="removeExtraDir(${idx})" class="tab-btn sm" style="color:#e74c3c; border-color:rgba(231,76,60,0.3);">✕</button>
        `;
        container.appendChild(div);
    });
}

// ─── Load all options from backend ───────────────────────────────────────────
async function loadAllOptions() {
    try {
        let cfg = {};
        if (typeof eel !== 'undefined' && typeof eel.get_parser_config === 'function') {
            cfg = await eel.get_parser_config()() || {};
        }

        let slowParsers = [];
        try {
            if (typeof eel.get_slow_parsers === 'function') {
                slowParsers = await eel.get_slow_parsers()() || [];
            }
        } catch(e) {}

        // ── Tab 1: General
        const startSel = document.getElementById('opt-start-page');
        if (startSel) startSel.value = cfg.start_page || 'player';
        safeCheck('opt-auto-scan',      cfg.auto_scan);
        safeCheck('opt-debug-console',  cfg.debug_console_active);
        safeCheck('opt-hide-mocks',     cfg.hide_mocks);

        const libDir  = document.getElementById('opt-library-dir');
        const browDir = document.getElementById('opt-browse-dir');
        if (libDir)  libDir.value  = cfg.library_dir  || '';
        if (browDir) browDir.value = cfg.browse_default_dir || '';

        buildExtraDirsUI(cfg.additional_library_dirs || []);

        // App mode
        updateAppModeButtons(cfg.app_mode);

        // ── Tab 2: Parser
        buildParserChainUI(cfg.parser_chain || [], slowParsers);
        updateParserModeButtons(cfg.parser_mode);
        safeCheck('opt-fast-scan',            cfg.fast_scan_enabled);
        safeCheck('opt-mutagen-albumartist',   cfg.mutagen_prefer_albumartist);
        safeCheck('opt-mutagen-lyrics',        cfg.mutagen_extract_lyrics);
        safeCheck('opt-ffmpeg-deep',           cfg.ffmpeg_deep_analysis);
        safeCheck('opt-ffmpeg-thumbs',         cfg.ffmpeg_extract_thumbnails);

        // ── Tab 3: Player
        const pbMode  = document.getElementById('opt-playback-mode');
        const vPbMode = document.getElementById('opt-video-playback-mode');
        if (pbMode)  pbMode.value  = cfg.playback_mode  || 'chrome_native';
        if (vPbMode) vPbMode.value = cfg.video_playback_mode || 'chrome_native';
        safeCheck('opt-vlc-embedded', cfg.vlc_embedded);

        // ── Tab 4: Filter
        buildCategoryGrid('opt-indexed-cats',   cfg.indexed_categories   || ALL_CATEGORIES);
        buildCategoryGrid('opt-displayed-cats', cfg.displayed_categories || ALL_CATEGORIES);

        // ── Tab 5: Debug
        updateLogLevelButtons(cfg.log_level || 'INFO');
        buildFeatureFlagsUI(cfg.feature_flags || {});
        buildDebugFlagsUI(cfg.debug_flags || {});
        safeCheck('opt-debug-scan',   cfg.debug_scan);
        safeCheck('opt-debug-parser', cfg.debug_parser);

        // ── Tab 6: Startup
        await loadStartupConfig();

        // Restore last active sub-tab
        const lastTab = localStorage.getItem('mwv_options_sub_tab') || 'opt-general';
        switchOptionsSubTab(lastTab);

        console.log('[Options] Config loaded successfully.');
    } catch(e) {
        console.error('[Options] Error loading config:', e);
    }
}

// ─── Save all options to backend ───────────────────────────────────────────────
async function saveAllOptions() {
    try {
        // Collect parser chain
        const chain = ALL_PARSERS
            .filter(p => document.getElementById(`parser-${p.id}`)?.checked)
            .map(p => p.id);

        // Collect category filters
        const indexedCats   = ALL_CATEGORIES.filter(c => document.getElementById(`opt-indexed-cats-${c}`)?.checked);
        const displayedCats = ALL_CATEGORIES.filter(c => document.getElementById(`opt-displayed-cats-${c}`)?.checked);

        // Collect debug flags
        const debugFlags = {};
        ALL_DEBUG_FLAGS.forEach(f => {
            debugFlags[f] = !!document.getElementById(`dbg-${f}`)?.checked;
        });

        // Collect feature flags
        const featureFlags = {};
        ALL_FEATURE_FLAGS.forEach(f => {
            featureFlags[f.key] = !!document.getElementById(`feat-${f.key}`)?.checked;
        });

        const cfg = {
            start_page:              document.getElementById('opt-start-page')?.value || 'player',
            auto_scan:               !!document.getElementById('opt-auto-scan')?.checked,
            debug_console_active:    !!document.getElementById('opt-debug-console')?.checked,
            hide_mocks:              !!document.getElementById('opt-hide-mocks')?.checked,
            library_dir:             document.getElementById('opt-library-dir')?.value || '',
            browse_default_dir:      document.getElementById('opt-browse-dir')?.value || '',
            fast_scan_enabled:       !!document.getElementById('opt-fast-scan')?.checked,
            mutagen_prefer_albumartist: !!document.getElementById('opt-mutagen-albumartist')?.checked,
            mutagen_extract_lyrics:  !!document.getElementById('opt-mutagen-lyrics')?.checked,
            ffmpeg_deep_analysis:    !!document.getElementById('opt-ffmpeg-deep')?.checked,
            ffmpeg_extract_thumbnails: !!document.getElementById('opt-ffmpeg-thumbs')?.checked,
            playback_mode:           document.getElementById('opt-playback-mode')?.value || 'chrome_native',
            video_playback_mode:     document.getElementById('opt-video-playback-mode')?.value || 'chrome_native',
            vlc_embedded:            !!document.getElementById('opt-vlc-embedded')?.checked,
            debug_scan:              !!document.getElementById('opt-debug-scan')?.checked,
            debug_parser:            !!document.getElementById('opt-debug-parser')?.checked,
            parser_chain:            chain,
            indexed_categories:      indexedCats,
            displayed_categories:    displayedCats,
            debug_flags:             debugFlags,
            feature_flags:           featureFlags,
        };

        if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
            const result = await eel.update_parser_config(cfg)();
            if (result && result.status === 'ok') {
                if (typeof showToast === 'function') showToast('Einstellungen gespeichert ✓', 'success');
                // Sync legacy IDs for compatibility
                safeCheck('config-auto-scan',      cfg.auto_scan);
                safeCheck('config-debug-console',  cfg.debug_console_active);
                safeCheck('config-hide-mocks',     cfg.hide_mocks);
            } else {
                console.error('[Options] Save failed:', result);
                if (typeof showToast === 'function') showToast('Fehler beim Speichern', 'error');
            }
        }
    } catch(e) {
        console.error('[Options] Error saving config:', e);
    }
}

// ─── Mode setters ─────────────────────────────────────────────────────────────
function setAppMode(mode) {
    updateAppModeButtons(mode);
    saveAllOptions();
}

function setParserMode(mode) {
    updateParserModeButtons(mode);
    // Store in a hidden field for saveAllOptions to pick up
    window._currentParserMode = mode;
    if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
        eel.update_parser_config({ parser_mode: mode })();
    }
}

function setLogLevel(level) {
    updateLogLevelButtons(level);
    if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
        eel.update_parser_config({ log_level: level })();
    }
    if (typeof showToast === 'function') showToast(`Log-Level: ${level}`, 'info');
}

function setAllDebugFlags(value) {
    ALL_DEBUG_FLAGS.forEach(f => {
        const el = document.getElementById(`dbg-${f}`);
        if (el) el.checked = value;
    });
    saveAllOptions();
}

// ─── UI state updaters ────────────────────────────────────────────────────────
function updateAppModeButtons(mode) {
    ['mode-perf', 'mode-bw'].forEach(id => {
        const el = document.getElementById(id);
        if (el) { el.classList.remove('active'); el.style.background = ''; }
    });
    const target = (mode === 'Low-Bandwidth') ? 'mode-bw' : 'mode-perf';
    const el = document.getElementById(target);
    if (el) el.classList.add('active');
}

function updateParserModeButtons(mode) {
    ['pm-light', 'pm-full', 'pm-ult'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active');
    });
    const map = { lightweight: 'pm-light', full: 'pm-full', ultimate: 'pm-ult' };
    const el = document.getElementById(map[mode] || 'pm-light');
    if (el) el.classList.add('active');
}

function updateLogLevelButtons(level) {
    ['ll-debug', 'll-info', 'll-warning', 'll-error'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active');
    });
    const map = { DEBUG: 'll-debug', INFO: 'll-info', WARNING: 'll-warning', ERROR: 'll-error' };
    const el = document.getElementById(map[level]);
    if (el) el.classList.add('active');
}

// ─── Path picker helpers ───────────────────────────────────────────────────────
async function pickDir(inputId) {
    if (typeof eel !== 'undefined' && typeof eel.pick_folder === 'function') {
        try {
            const dir = await eel.pick_folder()();
            if (dir) {
                const el = document.getElementById(inputId);
                if (el) el.value = dir;
                saveAllOptions();
            }
        } catch(e) { console.warn('[Options] pickDir error:', e); }
    } else {
        const val = prompt('Pfad eingeben:');
        if (val) {
            const el = document.getElementById(inputId);
            if (el) el.value = val;
            saveAllOptions();
        }
    }
}

async function addExtraDir() {
    let dir = null;
    if (typeof eel !== 'undefined' && typeof eel.pick_folder === 'function') {
        try { dir = await eel.pick_folder()(); } catch(e) {}
    }
    if (!dir) dir = prompt('Pfad des zusätzlichen Scan-Verzeichnisses:');
    if (!dir) return;

    if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
        // Read current list
        const cfg = await eel.get_parser_config()() || {};
        const dirs = cfg.additional_library_dirs || [];
        if (!dirs.includes(dir)) {
            dirs.push(dir);
            await eel.update_parser_config({ additional_library_dirs: dirs })();
            buildExtraDirsUI(dirs);
        }
    }
}

async function removeExtraDir(idx) {
    if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
        const cfg = await eel.get_parser_config()() || {};
        const dirs = cfg.additional_library_dirs || [];
        dirs.splice(idx, 1);
        await eel.update_parser_config({ additional_library_dirs: dirs })();
        buildExtraDirsUI(dirs);
    }
}

// ─── Legacy compat: existing callers ──────────────────────────────────────────
function saveParserChainUI() { saveAllOptions(); }
function loadOptionsUI()     { loadAllOptions(); }

// ─── Startup config (reusing existing functions) ───────────────────────────────
async function loadStartupConfig() {
    try {
        const config = await eel.get_startup_config()();
        if (config) {
            if (config.browser_choice) safeValue('startup-browser-choice', config.browser_choice);
            if (config.browser_flags)  safeValue('startup-browser-flags',  (config.browser_flags || []).join('\n'));
            if (config.env_vars) {
                let envStr = '';
                for (const [k, v] of Object.entries(config.env_vars)) envStr += `${k}=${v}\n`;
                safeValue('startup-env-vars', envStr.trim());
            }
        }
    } catch(e) { console.warn('[Options] loadStartupConfig error:', e); }
}

async function saveStartupConfig() {
    try {
        const choice   = readValue('startup-browser-choice', 'auto');
        const flagsRaw = readValue('startup-browser-flags', '');
        const envRaw   = readValue('startup-env-vars', '');
        const flags    = flagsRaw.split('\n').map(f => f.trim()).filter(Boolean);
        const envVars  = {};
        envRaw.split('\n').forEach(line => {
            const parts = line.split('=');
            if (parts.length >= 2) {
                const key = parts[0].trim();
                const val = parts.slice(1).join('=').trim();
                if (key) envVars[key] = val;
            }
        });
        const result = await eel.update_startup_config({ browser_choice: choice, browser_flags: flags, env_vars: envVars })();
        if (result && result.status === 'success') {
            if (typeof showToast === 'function') showToast('Startup-Konfig gespeichert! Neustart erforderlich.', 'success');
        }
    } catch(e) { console.error('[Options] saveStartupConfig error:', e); }
}

// ─── Mock data toggle (legacy compat) ─────────────────────────────────────────
async function loadMockDataConfig() {
    try {
        const enabled = await eel.get_mock_data_enabled()();
        safeCheck('config-mock-data-toggle', enabled);
    } catch(e) {}
}

async function toggleMockData(enabled) {
    try {
        await eel.set_mock_data_enabled(enabled)();
        if (typeof showToast === 'function') showToast(enabled ? 'Mock-Daten aktiviert' : 'Mock-Daten deaktiviert', 'info');
        if (typeof renderLibrary === 'function') renderLibrary();
    } catch(e) {}
}

// ─── Helpers ──────────────────────────────────────────────────────────────────
function safeCheck(id, val) {
    const el = document.getElementById(id);
    if (el) el.checked = !!val;
}

function safeValue(id, val) {
    const el = document.getElementById(id);
    if (el) el.value = val;
}

function readValue(id, fallback) {
    const el = document.getElementById(id);
    return el ? el.value : fallback;
}

// ─── Auto-load when the tools tab is switched to ───────────────────────────────
const _origSwitchTab = window.switchTab;
window.switchTab = function(tabId) {
    if (typeof _origSwitchTab === 'function') _origSwitchTab(tabId);
    if (tabId === 'tools') {
        setTimeout(loadAllOptions, 100);
    }
};
