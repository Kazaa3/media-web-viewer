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

        // ── v1.35.68 High-Fidelity (localStorage based)
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
        // Collect v1.35.68 High-Fidelity
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
 * Parser Panel Logic (v1.35.68)
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
 * Diagnostic Hub Handlers (v1.35.68)
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
 * Real-time Diagnostic Log Terminal (v1.35.68)
 * Receives granular logs from the backend and scrolls into view.
 */
if (typeof eel !== 'undefined') {
    eel.expose(append_debug_log);
}

function append_debug_log(msg, category = 'INFO') {
    // 1. Broadcast to advanced Diagnostic Suite buffer (v1.35.68)
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
// Legacy alias used in options_panel.html
const setAllFlags = setAllDebugFlags;

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
    if (tabId === 'options' || tabId === 'tools') {
        setTimeout(() => {
            loadAllOptions();
            const verEl = document.getElementById('options-version');
            if (verEl && window.MWV_VERSION) {
                verEl.innerText = window.MWV_VERSION;
            }
        }, 100);
    }
};
