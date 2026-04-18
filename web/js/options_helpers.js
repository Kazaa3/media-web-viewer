/**
 * options_helpers.js — Full Options Panel Logic (v1.34)
 * Manages all PARSER_CONFIG settings exposed in the Tools sub-tabs.
 */

/**
 * Comprehensive Options Hydration (v1.41.00 Standard)
 */
async function loadAllOptions() {
    if (typeof mwv_trace === 'function') mwv_trace('FLOW', 'LOAD-OPTIONS-START');
    
    try {
        const config = await eel.get_parser_config()();
        if (!config) return;

        // General
        safeCheck('config-auto-scan', config.auto_scan);
        safeCheck('config-fast-scan', config.fast_scan);
        safeCheck('config-hide-mocks', config.hide_mocks);
        safeCheck('config-debug-verbose', config.debug_verbose);
        safeValue('config-library-dir', config.library_dir);
        safeValue('config-browse-dir', config.browse_default_dir);

        // Feature Flags & Logging
        if (typeof loadFeatureFlags === 'function') loadFeatureFlags();
        if (typeof syncLogLevelUI === 'function')   syncLogLevelUI();

        // Sub-sections
        buildExtraDirsUI(config.additional_library_dirs || []);
        
        // Load sections if active
        const activeSubView = document.querySelector('.sub-tab-btn.options-subtab.active')?.id?.replace('opt-subtab-', '');
        if (activeSubView === 'environment') loadEnvironmentInfo();
        if (activeSubView === 'helpers')     loadStartupConfig();
        if (activeSubView === 'parser') {
            // Hydrate intensity
            if (config.intensity !== undefined) safeCheck('config-parser-intensity', config.intensity === 'full');
            // Hydrate chain
            if (typeof buildParserChainUI === 'function') buildParserChainUI(config.parser_chain || [], config.slow_parsers || []);
            // Hydrate dynamic settings
            if (typeof buildParserConfigurationUI === 'function') buildParserConfigurationUI(config.parser_settings || {});
        }

    } catch (e) {
        console.error('[Options] loadAllOptions failed:', e);
    }
}

/**
 * Environment & System Specs Hydration (SCR-003/006/007 Parity)
 */
async function loadEnvironmentInfo() {
    const container = document.getElementById('options-environment-view');
    if (!container || container.style.display === 'none') return;

    try {
        const info = await eel.get_sys_overview()();
        if (!info) return;

        // 1. System Specs
        safeInnerText('env-val-mediainfo', info.mediainfo || 'N/A');
        safeInnerText('env-val-ffmpeg',    info.ffmpeg || 'N/A');
        safeInnerText('env-val-python',    `${info.python_version} (${info.python_path})`);

        // 2. Core Packages Grid
        buildPackagesUI(info.core_packages || []);

        // 3. Requirements Status
        updateRequirementsStatus(info.requirements || {});

        // 4. Multi-Venv Matrix
        buildVenvGrid(info.venvs || []);
        buildVenvTree(info.venvs || []);

        // 5. App Mode & Toolchains (v1.41.00 Centralized)
        if (typeof buildHeadlessUI === 'function') buildHeadlessUI();
        if (typeof buildBrowserToolchainUI === 'function') buildBrowserToolchainUI();
        if (typeof buildTranscodingToolchainUI === 'function') buildTranscodingToolchainUI();
        if (typeof buildParsingToolchainUI === 'function') buildParsingToolchainUI();

    } catch (e) {
        console.error('[Options] loadEnvironmentInfo failed:', e);
    }
}

function buildPackagesUI(packages) {
    const grid = document.getElementById('env-core-packages-grid');
    if (!grid) return;
    grid.innerHTML = '';
    
    packages.forEach(pkg => {
        const badge = document.createElement('div');
        badge.className = 'diagnostic-value';
        badge.style.display = 'flex';
        badge.style.justifyContent = 'space-between';
        badge.innerHTML = `<span style="color:var(--text-secondary)">${pkg.name}</span> <span style="font-weight:800">${pkg.version}</span>`;
        grid.appendChild(badge);
    });
}

function updateRequirementsStatus(req) {
    const title = document.getElementById('req-status-title');
    const list  = document.getElementById('req-missing-list');
    const btn   = document.getElementById('btn-install-reqs');
    
    if (title) title.innerText = `requirements.txt Status (${req.installed}/${req.total})`;
    
    if (req.missing && req.missing.length > 0) {
        list.innerHTML = '❌ Fehlend: ' + req.missing.join(', ');
        if (btn) btn.style.display = 'flex';
    } else {
        list.innerHTML = '✅ Alle Abhängigkeiten erfüllt.';
        if (btn) btn.style.display = 'none';
    }
}

function buildVenvGrid(venvs) {
    const grid = document.getElementById('env-workspace-grid');
    if (!grid) return;
    grid.innerHTML = '';

    venvs.forEach(venv => {
        const card = document.createElement('div');
        card.className = 'glass-card';
        card.style.padding = '15px';
        card.style.display = 'flex';
        card.style.justifyContent = 'space-between';
        card.style.alignItems = 'center';
        card.style.borderLeft = venv.active ? '4px solid #f1c40f' : '1px solid var(--border-color)';
        
        card.innerHTML = `
            <div>
                <div style="font-weight:800; font-size:13px;">${venv.active ? '⭐ ' : ''}${venv.name} <span style="opacity:0.5; font-weight:500">(${venv.version})</span></div>
                <div style="font-size:10px; color:var(--text-secondary); margin-top:2px; font-family:monospace;">${venv.path}</div>
            </div>
            <div style="font-size:10px; font-weight:700; text-transform:uppercase; color:var(--accent-color); background:rgba(10,132,255,0.1); padding:2px 8px; border-radius:4px;">
                ${venv.role || 'VAPP'}
            </div>
        `;
        grid.appendChild(card);
    });
}

function buildVenvTree(venvs) {
    const tree = document.getElementById('env-tree-view');
    if (tree) tree.innerHTML = venvs.map(v => `<div>└── ${v.name} (${v.version}) <span style="opacity:0.4">${v.path}</span></div>`).join('');
}

/**
 * v1.41.00: App Mode & Browser Toolchain Builders
 */
function buildHeadlessUI() {
    const container = document.getElementById('env-headless-registry');
    if (!container || !window.CONFIG?.headless_registry) return;
    
    const reg = window.CONFIG.headless_registry;
    const status = document.getElementById('env-app-mode-status');
    if (status) status.style.background = reg.is_headless ? 'rgba(46,204,113,0.1)' : 'rgba(231,76,60,0.1)';
    if (status) status.style.color = reg.is_headless ? '#2ecc71' : '#e74c3c';
    if (status) status.innerText = reg.is_headless ? 'HEADLESS' : 'WINDOWED';

    container.innerHTML = `
        <div class="diagnostic-row">
            <span class="diagnostic-label">Target URL:</span>
            <span class="diagnostic-value" style="color:var(--accent-color)">${reg.app_url}</span>
        </div>
        <div class="diagnostic-row">
            <span class="diagnostic-label">Window Size:</span>
            <span class="diagnostic-value">${reg.window_size}</span>
        </div>
        <div class="diagnostic-row">
            <span class="diagnostic-label">App Flags:</span>
            <div style="margin-top:4px; font-family:monospace; font-size:10px; opacity:0.7; background:rgba(255,255,255,0.05); padding:8px; border-radius:4px;">
                ${reg.app_mode_flags.join('<br>')}
            </div>
        </div>
    `;
}

function buildBrowserToolchainUI() {
    const grid = document.getElementById('env-browser-ladder');
    if (!grid || !window.CONFIG?.browsers) return;

    grid.innerHTML = window.CONFIG.browsers.map(b => `
        <div class="diagnostic-value" style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
            <span style="opacity:0.6">${b}</span>
            <span style="font-weight:700; color:var(--accent-color)">✓</span>
        </div>
    `).join('');

    // Add automation tools if available
    const tools = window.CONFIG.headless_tools;
    if (tools) {
        const container = document.getElementById('env-headless-registry');
        const toolsHtml = Object.entries(tools).map(([name, ver]) => `
            <div style="display:flex; justify-content:space-between; align-items:center; margin-top:5px; opacity:0.8;">
                <span style="text-transform:capitalize;">${name}</span>
                <span class="diagnostic-value" style="font-size:10px;">${ver}</span>
            </div>
        `).join('');
        if (container) container.innerHTML += `<div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">${toolsHtml}</div>`;
    }
}

function buildTranscodingToolchainUI() {
    const container = document.getElementById('env-transcode-ladder');
    if (!container || !window.CONFIG?.transcoding_toolchain) return;

    const tools = window.CONFIG.transcoding_toolchain;
    container.innerHTML = Object.entries(tools).map(([name, ver]) => {
        const isUnknown = ver === 'Unknown' || ver === 'N/A' || !ver;
        return `
            <div class="diagnostic-value" style="display:flex; justify-content:space-between; font-size:11px; margin-bottom:4px;">
                <span style="opacity:0.6; text-transform:capitalize;">${name}</span>
                <span style="font-weight:700; color:${isUnknown ? '#e74c3c' : 'var(--accent-color)'}">${isUnknown ? '✖' : ver}</span>
            </div>
        `;
    }).join('');
    
    // Add Hardware Encoder Info
    if (encoders.length > 0) {
        const gpuHtml = `
            <div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.1); padding-top:10px;">
                <div style="font-size:10px; font-weight:800; color:var(--text-secondary); text-transform:uppercase; margin-bottom:8px;">HW Encoders Detectiert:</div>
                <div style="display:flex; flex-wrap:wrap; gap:5px;">
                    ${encoders.map(e => `<span style="background:rgba(46,204,113,0.1); color:#2ecc71; padding:2px 6px; border-radius:3px; font-size:9px; font-weight:800; text-transform:uppercase;">${e}</span>`).join('')}
                </div>
            </div>
        `;
        container.innerHTML += gpuHtml;
    }
}

function buildParsingToolchainUI() {
    const grid = document.getElementById('env-parser-ladder');
    if (!grid || !window.CONFIG?.parsing_toolchain) return;

    const tools = window.CONFIG.parsing_toolchain;
    grid.innerHTML = Object.entries(tools).map(([name, ver]) => {
        const isUnknown = ver === 'Unknown' || ver === 'N/A' || !ver;
        return `
            <div class="diagnostic-value" style="display:flex; justify-content:space-between; font-size:11px; padding: 6px 12px; background:rgba(255,255,255,0.03); border-radius:4px;">
                <span style="opacity:0.6; text-transform:capitalize;">${name}</span>
                <span style="font-weight:700; color:${isUnknown ? '#e74c3c' : 'var(--accent-color)'}">${isUnknown ? '✖' : ver}</span>
            </div>
        `;
    }).join('');
}

async function installMissingPackages() {
    const term = document.getElementById('pip-terminal-container');
    const out  = document.getElementById('pip-terminal-output');
    if (term) term.style.display = 'block';
    if (out) out.innerHTML = '<div style="color:#aaa">Initializing installer...</div>';

    try {
        // Fetch missing packages first
        const info = await eel.get_sys_overview()();
        const missing = info.requirements?.missing || [];
        
        if (missing.length === 0) {
            out.innerHTML += '<div>✅ Nothing to install.</div>';
            return;
        }

        out.innerHTML += `<div>🚀 Starting installation for: ${missing.join(', ')}</div>`;
        const result = await eel.pip_install_packages(missing)();
        
        if (result.status === 'ok') {
            out.innerHTML += `<div style="color:#4caf50; margin-top:10px;">SUCCESS: ${result.message}</div>`;
            out.innerHTML += `<pre style="font-size:10px; opacity:0.8;">${result.output}</pre>`;
            loadEnvironmentInfo(); // Refresh
        } else {
            out.innerHTML += `<div style="color:#f44336; margin-top:10px;">ERROR: ${result.message}</div>`;
            if (result.error) out.innerHTML += `<pre style="color:#ff8a80; font-size:10px;">${result.error}</pre>`;
        }
    } catch (e) {
        out.innerHTML += `<div style="color:#f44336">Critical Failure: ${e.message}</div>`;
    }
}

function safeInnerText(id, val) {
    const el = document.getElementById(id);
    if (el) el.innerText = val;
}

// ─── Knwn constants ───────────────────────────────────────────────────────────
const ALL_CATEGORIES = [
    'audio', 'video', 'pictures', 'documents', 'ebooks',
    'disk_images', 'spiel', 'beigabe', 'supplements', 'games'
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
    { id: 'vlc',          label: 'VLC Lib',       slow: false },
    { id: 'cvlc',         label: 'VLC Binary',    slow: false }
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
    const container = document.getElementById('parser-chain-grid-options');
    if (!container) return;
    container.innerHTML = '';
    ALL_PARSERS.forEach(p => {
        const isSlow = p.slow || (slowParsers || []).includes(p.id);
        const isEnabled = (chain || []).includes(p.id);
        const btn = document.createElement('div');
        btn.className = 'parser-item-btn';
        btn.setAttribute('data-parser', p.id);
        btn.onclick = (e) => {
            if (e.target.tagName !== 'INPUT') selectParserDetail(p.id);
        };
        
        btn.innerHTML = `
            <div style="display:flex; align-items:center; gap:10px;">
                <div style="font-size:12px; font-weight:800;">
                    ${isSlow ? '<span style="color:#e67e22; margin-right:4px;">●</span>' : ''}
                    ${p.label}
                </div>
            </div>
            <label class="switch sm" onclick="event.stopPropagation()">
                <input type="checkbox" id="parser-${p.id}" ${isEnabled ? 'checked' : ''} onchange="saveAllOptions()">
                <span class="slider"></span>
            </label>
        `;
        container.appendChild(btn);
    });

    // Also trigger dynamic settings build if container exists
    if (document.getElementById('parser-dynamic-settings-root')) {
        buildParserConfigurationUI();
    }
}

/**
 * Dynamic Parser Parameter Hub (v1.35.70)
 * Renders a VS Code-style property grid based on parser schemas.
 */
async function buildParserConfigurationUI(storedSettings = null) {
    const root = document.getElementById('parser-dynamic-settings-root');
    if (!root) return;

    try {
        const registry = await eel.get_parser_registry()();
        if (!registry) return;

        root.innerHTML = '';
        
        // If storedSettings is null, we might be calling from buildParserChainUI, 
        // in which case we should try to get it from the global window.CONFIG or similar.
        const settings = storedSettings || window.CONFIG?.parser_settings || {};

        Object.entries(registry).forEach(([id, info]) => {
            if (!info.settings_schema || Object.keys(info.settings_schema).length === 0) return;

            const card = document.createElement('div');
            card.className = 'glass-card';
            card.style.padding = '15px';
            card.style.background = 'rgba(255,255,255,0.02)';
            card.style.border = '1px solid rgba(255,255,255,0.05)';
            
            const title = info.capabilities?.name || id;
            let html = `<div style="font-size:11px; font-weight:800; color:var(--accent-color); text-transform:uppercase; margin-bottom:12px; border-bottom:1px solid rgba(155,89,182,0.2); padding-bottom:5px;">${title}</div>`;
            
            Object.entries(info.settings_schema).forEach(([key, schema]) => {
                const currentVal = (settings[id] && settings[id][key] !== undefined) ? settings[id][key] : (schema.default !== undefined ? schema.default : '');
                const inputId = `parser-cfg-${id}-${key}`;
                
                html += `
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div style="flex:1;">
                            <div style="font-size:12px; font-weight:700; color:var(--text-primary);">${key}</div>
                            <div style="font-size:10px; color:var(--text-secondary); opacity:0.7;">${schema.description || ''}</div>
                        </div>
                        <div style="margin-left:15px;">
                `;

                if (typeof schema.default === 'boolean' || schema.type === 'boolean') {
                    html += `
                        <label class="switch sm">
                            <input type="checkbox" id="${inputId}" ${currentVal ? 'checked' : ''} onchange="saveParserSetting('${id}', '${key}', this.checked)">
                            <span class="slider"></span>
                        </label>
                    `;
                } else if (schema.type === 'integer' || typeof schema.default === 'number') {
                    html += `<input type="number" id="${inputId}" value="${currentVal}" class="action-btn sm" style="width:60px; text-align:center; padding:4px 8px;" onchange="saveParserSetting('${id}', '${key}', this.value)">`;
                } else {
                    html += `<input type="text" id="${inputId}" value="${currentVal}" class="action-btn sm" style="width:100px; padding:4px 8px;" onchange="saveParserSetting('${id}', '${key}', this.value)">`;
                }

                html += `</div></div>`;
            });

            card.innerHTML = html;
            root.appendChild(card);
        });

    } catch (e) {
        console.error('[Options] buildParserConfigurationUI failed:', e);
    }
}

/**
 * Persists granular parser settings to the backend.
 */
let parserSaveTimeout = null;
async function saveParserSetting(parserId, key, value) {
    if (typeof mwv_trace === 'function') mwv_trace('CONFIG', `UP-PARSER: ${parserId}.${key}=${value}`);
    
    // Immediate local feedback (optional)
    if (typeof showToast === 'function') {
        clearTimeout(parserSaveTimeout);
        parserSaveTimeout = setTimeout(() => showToast(`${parserId} Parameter aktualisiert ✓`, 'success'), 500);
    }

    try {
        await eel.update_parser_setting(parserId, key, value)();
    } catch (e) {
        console.error(`[Options] saveParserSetting failed for ${parserId}.${key}:`, e);
    }
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
        div.style.cssText = 'display:flex; align-items:center; gap:8px; padding:10px 14px; background:var(--bg-secondary); border-radius:8px; cursor:pointer;';
        div.innerHTML = `
            <label class="switch sm"><input type="checkbox" id="${containerId}-${cat}" ${isChecked ? 'checked' : ''} onchange="saveAllOptions()"><span class="slider"></span></label>
            <div style="font-size:13px; font-weight:700; color:var(--text-primary);">${labels[cat] || cat}</div>
        `;
        container.appendChild(div);
    });
}

function buildDebugFlagsUI(flags) {
    const container = document.getElementById('debug-flags-container');
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
    const container = document.getElementById('options-feature-flags');
    if (!container) return;
    container.innerHTML = '';
    ALL_FEATURE_FLAGS.forEach(f => {
        const isOn = flags && flags[f.key];
        const div = document.createElement('div');
        div.style.cssText = 'display:flex; align-items:center; justify-content:space-between; padding:12px 16px; background:var(--bg-secondary); border-radius:8px;';
        div.innerHTML = `
            <div style="font-size:13px; font-weight:700; color:var(--text-primary);">${f.label}</div>
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
        const startSel = document.getElementById('start-page-select');
        if (startSel) startSel.value = cfg.start_page || 'player';
        safeCheck('config-auto-scan',      cfg.auto_scan);
        safeCheck('config-debug-console',  cfg.debug_console_active);
        safeCheck('config-hide-mocks',     cfg.hide_mocks);
        safeCheck('config-fast-scan',      cfg.fast_scan_enabled);
        safeCheck('config-debug-scan',     cfg.debug_scan);
        safeCheck('config-debug-parser',   cfg.debug_parser);

        const libDir  = document.getElementById('config-library-dir');
        const browDir = document.getElementById('config-browse-dir');
        if (libDir)  libDir.value  = cfg.library_dir  || '';
        if (browDir) browDir.value = cfg.browse_default_dir || '';

        buildExtraDirsUI(cfg.additional_library_dirs || []);

        // App mode
        updateAppModeButtons(cfg.app_mode);

        // ── Parser mode
        buildParserChainUI(cfg.parser_chain || [], slowParsers);
        updateParserModeButtons(cfg.parser_mode);
        safeCheck('config-parser-intensity',     cfg.parser_intensity);
        if (cfg.parser_intensity) {
             const lbl = document.getElementById('parser-intensity-label');
             if (lbl) { lbl.innerText = 'Ultimate-Modus'; lbl.style.color = '#f1c40f'; }
        }
        
        safeCheck('config-mutagen-albumartist',  cfg.mutagen_prefer_albumartist);
        safeCheck('config-mutagen-lyrics',       cfg.mutagen_extract_lyrics);
        safeCheck('config-ffmpeg-deep',          cfg.ffmpeg_deep_analysis);
        safeCheck('config-ffmpeg-thumbs',        cfg.ffmpeg_extract_thumbnails);

        // ── Player
        const pbMode  = document.getElementById('config-playback-mode');
        if (pbMode)  pbMode.value  = cfg.playback_mode  || 'chrome_native';
        safeCheck('config-vlc-embedded', cfg.vlc_embedded);

        // ── Filter
        buildCategoryGrid('indexed-cats-grid',   cfg.indexed_categories   || ALL_CATEGORIES);
        buildCategoryGrid('displayed-cats-grid', cfg.displayed_categories || ALL_CATEGORIES);

        // ── Debug
        updateLogLevelButtons(cfg.log_level || 'INFO');
        buildFeatureFlagsUI(cfg.feature_flags || {});
        buildDebugFlagsUI(cfg.debug_flags || {});

        // ── v1.41.00 High-Fidelity (localStorage based)
        safeCheck('config-diagnostic-mode', localStorage.getItem('mwv_diagnostic_mode') === 'true');
        safeCheck('config-force-native',     localStorage.getItem('mwv_force_native') === 'true');
        safeCheck('config-dom-auditor',      localStorage.getItem('mwv_dom_auditor_visible') !== 'false'); // Default TRUE

        // ── Startup
        await loadStartupConfig();

        console.log('[Options] Config loaded successfully.');
    } catch(e) {
        console.error('[Options] Error loading config:', e);
    }
}

// ─── Save all options to backend ───────────────────────────────────────────────
async function saveAllOptions() {
    try {
        // Collect v1.41.00 High-Fidelity
        const diagMode = !!document.getElementById('config-diagnostic-mode')?.checked;
        const native   = !!document.getElementById('config-force-native')?.checked;
        const auditor  = !!document.getElementById('config-dom-auditor')?.checked;

        localStorage.setItem('mwv_diagnostic_mode', diagMode);
        localStorage.setItem('mwv_force_native', native);
        localStorage.setItem('mwv_dom_auditor_visible', auditor);

        // Notify managers if present
        if (typeof RecoveryManager !== 'undefined') RecoveryManager.checkAndHydrate();
        const hud = document.getElementById('dom-auditor-hud');
        if (hud) hud.style.display = auditor ? 'block' : 'none';

        // Collect parser chain
        const chain = ALL_PARSERS
            .filter(p => document.getElementById(`parser-${p.id}`)?.checked)
            .map(p => p.id);

        // Collect category filters
        const indexedCats   = ALL_CATEGORIES.filter(c => document.getElementById(`indexed-cats-grid-${c}`)?.checked);
        const displayedCats = ALL_CATEGORIES.filter(c => document.getElementById(`displayed-cats-grid-${c}`)?.checked);

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
            start_page:              document.getElementById('start-page-select')?.value || 'player',
            auto_scan:               !!document.getElementById('config-auto-scan')?.checked,
            debug_console_active:    !!document.getElementById('config-debug-console')?.checked,
            hide_mocks:              !!document.getElementById('config-hide-mocks')?.checked,
            fast_scan_enabled:       !!document.getElementById('config-fast-scan')?.checked,
            debug_scan:              !!document.getElementById('config-debug-scan')?.checked,
            debug_parser:            !!document.getElementById('config-debug-parser')?.checked,
            library_dir:             document.getElementById('config-library-dir')?.value || '',
            browse_default_dir:      document.getElementById('config-browse-dir')?.value || '',
            mutagen_prefer_albumartist: !!document.getElementById('config-mutagen-albumartist')?.checked,
            mutagen_extract_lyrics:  !!document.getElementById('config-mutagen-lyrics')?.checked,
            ffmpeg_deep_analysis:    !!document.getElementById('config-ffmpeg-deep')?.checked,
            ffmpeg_extract_thumbnails: !!document.getElementById('config-ffmpeg-thumbs')?.checked,
            playback_mode:           document.getElementById('config-playback-mode')?.value || 'chrome_native',
            vlc_embedded:            !!document.getElementById('config-vlc-embedded')?.checked,
            parser_chain:            chain,
            parser_mode:             window._currentParserMode || 'full',
            parser_intensity:        !!document.getElementById('config-parser-intensity')?.checked,
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
    window._currentParserMode = mode;
    
    // Update intensity toggle if applicable
    const intensityToggle = document.getElementById('config-parser-intensity');
    if (intensityToggle) {
        intensityToggle.checked = (mode === 'ultimate' || mode === 'full');
        const label = document.getElementById('parser-intensity-label');
        if (label) label.innerText = (mode === 'ultimate') ? 'Ultimate-Modus' : 'Effizienz-Modus';
    }

    if (typeof eel !== 'undefined' && typeof eel.update_parser_config === 'function') {
        eel.update_parser_config({ parser_mode: mode })();
    }
}

/**
 * Parser Panel Logic (v1.41.00)
 */
function toggleParserIntensity(enabled) {
    const mode = enabled ? 'ultimate' : 'lightweight';
    const label = document.getElementById('parser-intensity-label');
    if (label) {
        label.innerText = enabled ? 'Ultimate-Modus' : 'Effizienz-Modus';
        label.style.color = enabled ? '#f1c40f' : '#2ecc71';
    }
    
    // Auto-enable/disable deep flags
    safeCheck('config-mutagen-lyrics', enabled);
    safeCheck('config-ffmpeg-thumbs', enabled);
    
    setParserMode(mode);
    if (typeof showToast === 'function') {
        showToast(`Parser Intensität: ${enabled ? 'ULTIMATE' : 'EFFICIENCY'}`, 'info');
    }
}

function selectParserDetail(id) {
    console.log(`[Parser] Selecting detail for: ${id}`);
    
    // Update Sidebar Selection UI
    document.querySelectorAll('.parser-item-btn').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-parser') === id);
    });

    const title = document.getElementById('parser-detail-title');
    const desc = document.getElementById('parser-detail-desc');
    const opts = document.getElementById('parser-detail-options');
    if (!title || !desc || !opts) return;

    const parser = ALL_PARSERS.find(p => p.id === id) || { label: id, id: id };
    title.innerText = `Konfiguration: ${parser.label}`;
    
    let detailHtml = '';
    if (id === 'filename') {
        desc.innerText = 'Extrahiert Informationen direkt aus dem Pfad und Dateinamen. Ideal für standardisierte Benennungen.';
        detailHtml = `
            <div class="glass-card sm">
                <div style="font-size:11px; margin-bottom:5px; opacity:0.6;">RegEx Pattern</div>
                <input type="text" value="S(?<season>\\d+)E(?<episode>\\d+)" style="width:100%; background:transparent; border:1px solid var(--border-color); color:var(--text-primary); font-family:monospace; font-size:12px; padding:5px;">
            </div>
        `;
    } else if (id === 'mutagen') {
        desc.innerText = 'Leistungsstarker Tag-Extraktor für Audio-Formate. Unterstützt ID3v2, Vorbis, FLAC und MP4.';
        detailHtml = `
            <div style="grid-column:1/-1; display:flex; flex-direction:column; gap:10px;">
                <label style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:13px;">Deep Cover Flow Extraction</span>
                    <input type="checkbox" checked onchange="saveAllOptions()">
                </label>
                <label style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:13px;">Fallback encoding (Latin-1)</span>
                    <input type="checkbox" onchange="saveAllOptions()">
                </label>
            </div>
        `;
    } else {
        desc.innerText = `Detaillierte Analyse-Einstellungen für den ${parser.label} Parser sind für diesen Dateityp aktiv.`;
        detailHtml = `<div style="opacity:0.4; font-size:11px;">Keine spezifischen Parameter verfügbar.</div>`;
    }
    
    opts.innerHTML = detailHtml;
}

function resetParserChain() {
    const defaults = ['filename', 'container', 'mutagen', 'ffprobe'];
    ALL_PARSERS.forEach(p => {
        const el = document.getElementById(`parser-${p.id}`);
        if (el) el.checked = defaults.includes(p.id);
    });
    if (typeof showToast === 'function') showToast('Parser Kette zurückgesetzt', 'info');
    saveAllOptions();
}

function clearParserLogs() {
    const term = document.getElementById('parser-log-terminal');
    if (term) term.innerHTML = '<div style="opacity:0.4;">[System] Tracer cleared. Awaiting parse events...</div>';
}

function setLogLevel(level) {
    updateLogLevelButtons(level);
    if (typeof eel !== 'undefined') {
        if (typeof eel.update_parser_config === 'function') {
            eel.update_parser_config({ log_level: level })();
        }
        if (typeof eel.set_log_level === 'function') {
            eel.set_log_level(level)();
        }
    }
    if (typeof showToast === 'function') showToast(`Log-Level: ${level}`, 'info');
}

/**
 * Diagnostic Hub Handlers (v1.41.00)
 */
async function triggerDirectScan() {
    if (typeof eel === 'undefined' || typeof eel.run_direct_scan !== 'function') {
        alert('Eel/Backend not available.');
        return;
    }
    if (typeof showToast === 'function') showToast('Scanner gestartet (Deep Hydration)...', 'info');
    try {
        const res = await eel.run_direct_scan()();
        if (res && res.status === 'success') {
            if (typeof showToast === 'function') showToast(`Deep Hydration vollständig! ${res.items_found || 0} Items indiziert.`, 'success');
            if (typeof renderLibrary === 'function') renderLibrary();
        }
    } catch(e) {
        console.error('[Diagnostic] Scan failed:', e);
    }
}

async function triggerDeepSync() {
    console.info("[FE-AUDIT] User Reaction: triggerDeepSync() triggered.");
    if (typeof mwv_trace === 'function') mwv_trace('FOOTER-UI', 'SYNC-CLICK', { ts: Date.now() });
    if (typeof eel === 'undefined' || typeof eel.sync_library_atomic !== 'function') {
        // Fallback to simple hydration if atomic is missing
        if (typeof force_rehydration === 'function') {
            force_rehydration();
            return;
        }
        alert('Deep Sync currently unavailable.');
        return;
    }
    if (typeof showToast === 'function') showToast('Atomic Sync wird ausgeführt...', 'info');
    try {
        const res = await eel.sync_library_atomic()();
        if (res && res.status === 'success') {
            if (typeof showToast === 'function') showToast('Atomic Sync erfolgreich ✓', 'success');
            if (typeof renderLibrary === 'function') renderLibrary();
        }
    } catch(e) { console.error('[Diagnostic] Atomic Sync failed:', e); }
}

/**
 * Real-time Diagnostic Log Terminal (v1.41.00)
 * Receives granular logs from the backend and scrolls into view.
 */
if (typeof eel !== 'undefined') {
    eel.expose(append_debug_log);
}

function append_debug_log(msg, category = 'INFO') {
    // 1. Broadcast to advanced Diagnostic Suite buffer (v1.41.00)
    if (typeof window.appendDebugLog === 'function') {
        const timestamp = new Date().toLocaleTimeString();
        window.appendDebugLog(`${timestamp} [${category}] ${msg}`);
    }

    // 2. Render locally in Options Terminal
    const term = document.getElementById('diagnostic-log-terminal');
    if (!term) return;

    if (term.children.length > 500) term.innerHTML = ''; // Cap scrollback
    
    const timeStr = new Date().toLocaleTimeString();
    const line = document.createElement('div');
    line.style.marginBottom = '2px';
    
    let color = '#0f0';
    if (category.includes('WARN')) color = '#ff9800';
    if (category.includes('ERROR')) color = '#f44336';
    if (category.includes('DB')) color = '#2196f3';
    
    line.innerHTML = `
        <span style="color: #666; font-size: 9px;">[${timeStr}]</span> 
        <span style="color: ${color}; font-weight: 700;">[${category}]</span> 
        ${msg}
    `;
    
    term.appendChild(line);
    term.scrollTop = term.scrollHeight; // Auto-scroll
}

function clearDiagnosticLog() {
    const term = document.getElementById('diagnostic-log-terminal');
    if (term) term.innerHTML = '<div style="opacity: 0.5;">[System] Log cleared. Awaiting new scan...</div>';
}

function setAllDebugFlags(value) {
    ALL_DEBUG_FLAGS.forEach(f => {
        const el = document.getElementById(`dbg-${f}`);
        if (el) el.checked = value;
    });
    saveAllOptions();
}
// Expose to window
window.resetAllFilters = resetAllFilters;

/**
 * Specialized View Initializers (Proxy to internal fragment controllers)
 * This ensures the UI doesn't crash during async fragment loading.
 */
function initFilmsView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-FILMS');
    libraryFilter = 'film'; 
    renderLibrary(); 
}

function initSeriesView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-SERIES');
    libraryFilter = 'serie'; 
    renderLibrary(); 
}

function initAlbumsView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-ALBUMS');
    libraryFilter = 'album'; 
    renderLibrary(); 
}

function initAudiobooksView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-AUDIOBOOKS');
    libraryFilter = 'audiobook'; 
    renderLibrary(); 
}

// Global Exports
window.initFilmsView = initFilmsView;
window.initSeriesView = initSeriesView;
window.initAlbumsView = initAlbumsView;
window.initAudiobooksView = initAudiobooksView;

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
    if (tabId === 'options' || tabId === 'tools' || tabId === 'parser') {
        setTimeout(() => {
            loadAllOptions();
            const verEl = document.getElementById('options-version');
            if (verEl && window.MWV_VERSION) {
                verEl.innerText = window.MWV_VERSION;
            }
        }, 100);
    }
};

// ─── Fresh Refresh Stability (v1.41.00 Repair) ──────────────────────────────────
function initParserHydration() {
    const activeTab = localStorage.getItem('mwv_active_tab');
    if (activeTab === 'parser' || activeTab === 'options') {
        console.log(`[Parser] Active tab '${activeTab}' detected on refresh. Hydrating settings...`);
        setTimeout(loadAllOptions, 250); // Delay to ensure fragment mount
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initParserHydration);
} else {
    initParserHydration();
}

// Created with MWV v1.46.00-MASTER
