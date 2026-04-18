/**
 * Common UI Utilities & Helpers
 * Extracted from app.html to improve modularity and avoid line-number drift.
 */

let CATEGORY_MAP = {};
let TECH_MAP = {};
let CONFIG = {}; // Centralized Flag & Env registry

/**
 * Syncs all core registries from the backend (Cat-Master, Tech-Markers, Global-Config).
 */
async function syncCoreRegistry() {
    if (typeof eel !== 'undefined' && typeof eel.get_category_master === 'function') {
        const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error("Timeout")), 2000));
        try {
            console.info(`[FE-AUDIT] STAGE 1: syncCoreRegistry triggered. Handshake initiated...`);
            // Parallel fetch with 2s safety timeout (v1.41.00-B)
            const [master, tech, config] = await Promise.race([
                Promise.all([
                    eel.get_category_master()(),
                    eel.get_tech_markers()(),
                    eel.get_global_config()()
                ]),
                timeout
            ]);

            if (master) {
                console.info("[FE-AUDIT] STAGE 1.1: Category Master received:", Object.keys(master).length, "keys.");
                CATEGORY_MAP = master;
                window.CATEGORY_MAP = master;
            }
            if (tech) {
                console.info("[FE-AUDIT] STAGE 1.2: Tech Markers received:", tech);
                TECH_MAP = tech;
            }
            if (config) {
                console.info("[FE-AUDIT] STAGE 1.3: Global Config received:", config);
                window.CONFIG = config;
                window.__mwv_raw_mode = config.raw_mode || false;
                window.__mwv_bypass_db = config.bypass_db || false;

                // Set sidebar default from config (v1.37 Restoration logic)
                const ui = config.ui_settings || {};
                if (ui.sidebar_visible !== undefined && localStorage.getItem('mwv_sidebar_visible') === null) {
                    console.info("[UI-NAV] Initializing Sidebar State (Default to CLOSED v1.37):", false);
                    window.sidebarVisible = false;
                    if (typeof applySidebarState === 'function') setTimeout(applySidebarState, 100);
                }
            }

            console.info("[FE-AUDIT] STAGE 1 COMPLETE: Forensic Handshake synchronized.");
            if (typeof renderAudioQueue === 'function') renderAudioQueue();
        } catch (e) {
            console.warn("[FE-AUDIT] STAGE 1 CRITICAL: Forensic Handshake stalling or failed.", e.message);
        }
    }
}

/**
 * Specialized Sync Wrappers for Module Compatibility (v1.41.00)
 */
async function syncCategoryMaster() { await syncCoreRegistry(); }
window.syncCategoryMaster = syncCategoryMaster;
async function syncTechMarkers() { await syncCoreRegistry(); }
async function syncGlobalConfig() { await syncCoreRegistry(); }

// Global initialization hook
document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit for Eel to initialize
    setTimeout(syncCoreRegistry, 500);
});

/**
 * Toggles a modal's visibility.
 */
function toggleModal(modalId, forceState) {
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.warn(`[UI] Cannot toggle modal: ${modalId} not found.`);
        return;
    }
    const newState = (forceState !== undefined) ? forceState : (modal.style.display === 'none' || modal.style.display === '');

    // Log the modal change
    if (typeof mwv_trace === 'function') {
        mwv_trace('MODAL', modalId, { newState });
    }

    modal.style.display = newState ? 'flex' : 'none';
}

/**
 * Appends a trace message to the UI and backend log.
 */
function appendUiTrace(message) {
    const timestamp = new Date().toLocaleTimeString();
    const logLine = `[UI-Trace ${timestamp}] ${message}`;
    console.warn(logLine);

    // No logic here, just placeholder for clean split

    const isErrorOrAlert = message.toLowerCase().includes('js-error') || message.toLowerCase().includes('alert');
    if (isErrorOrAlert) {
        const errorLog = document.getElementById('startup-error-log');
        if (errorLog) {
            if (errorLog.innerText.includes('Waiting for errors')) errorLog.innerText = '';
            errorLog.innerText += `\n${logLine}`;
            errorLog.scrollTop = errorLog.scrollHeight;
        }
    }

    try {
        if (typeof eel !== 'undefined' && typeof eel.ui_trace === 'function') {
            eel.ui_trace(logLine)();
        }
    } catch (e) { }

    const debugOutput = document.getElementById('debug-output');
    if (debugOutput) {
        const prefix = debugOutput.textContent && !debugOutput.textContent.endsWith('\n') ? '\n' : '';
        debugOutput.textContent += `${prefix}${logLine}\n`;
        debugOutput.scrollTop = debugOutput.scrollHeight;
    }

    // Restore real-time Debug Console (v1.34)
    if (typeof appendDebugLog === 'function') {
        appendDebugLog(logLine);
    }

    const resultsContainer = document.getElementById('test-results-container');
    const testOutput = document.getElementById('test-output');
    if (resultsContainer && testOutput && resultsContainer.style.display !== 'none') {
        const prefix = testOutput.textContent && !testOutput.textContent.endsWith('\n') ? '\n' : '';
        testOutput.textContent += `${prefix}${logLine}\n`;
        testOutput.scrollTop = testOutput.scrollHeight;
    }
}

// Expose appendUiTrace to Eel
if (typeof eel !== 'undefined' && typeof eel.expose === 'function') {
    eel.expose(appendUiTrace);
}

/**
 * Safety Utilities for DOM access.
 */
function safeStyle(id, prop, value) {
    const el = document.getElementById(id);
    if (el) el.style[prop] = value;
}

function safeText(id, text) {
    const el = document.getElementById(id);
    if (el) el.innerText = text;
}

function safeHtml(id, html) {
    const el = document.getElementById(id);
    if (el) el.innerHTML = html;
}

function safeValue(id, val) {
    const el = document.getElementById(id);
    if (el) el.value = val;
}

function readValue(id, fallback = '') {
    const el = document.getElementById(id);
    return el ? el.value : fallback;
}

function readText(id, fallback = '') {
    const el = document.getElementById(id);
    return el ? el.innerText : fallback;
}

/**
 * Updates the global application progress bar (Ladebalken).
 * v1.34 Master: Linked to top-fixed bar above sub-navigation.
 */
function update_progress(data) {
    const container = document.getElementById('app-progress-bar-container');
    const bar = document.getElementById('app-progress-bar');
    const text = document.getElementById('app-progress-text');

    if (!container || !bar) return;

    if (typeof data === 'string') {
        if (text) text.innerText = data;
        return;
    }

    if (data.progress !== undefined) {
        const p = Math.max(0, Math.min(100, Number(data.progress) || 0));
        bar.style.width = p + '%';
        if (text) text.innerText = `${data.status || 'Verarbeite...'} (${p}%)`;

        // Auto-show/hide based on activity
        container.style.display = (p > 0 && p < 100) ? 'block' : 'none';
        if (text) text.style.display = (p > 0 && p < 100) ? 'block' : 'none';
    }
}

/**
 * Global Context Menu Controller
 */
function showContextMenu(e, item) {
    // [v1.41.147] Config & Registry Check
    const isEnabled = window.CONFIG && window.CONFIG.ui_settings && window.CONFIG.ui_settings.enable_context_menu !== false;
    if (!isEnabled) {
        console.warn("[Context-Menu] Disabled via Global Config.");
        return;
    }

    if (e) {
        e.preventDefault();
        e.stopPropagation();
    }

    // [v1.41.148] Multi-ID Bridge: Target primary centralized ID
    const menu = document.getElementById('context-menu');
    if (!menu) {
        console.warn("[Context-Menu] Target element #context-menu not found in DOM.");
        return;
    }

    if (typeof appendUiTrace === 'function') appendUiTrace(`[Context-Menu] Opening for: ${item.name}`);
    console.info(`>>> [Context-Menu] showContextMenu triggered for: ${item.name} at (${e.clientX}, ${e.clientY})`);

    let x = e.clientX;
    let y = e.clientY;

    if (x === 0 && y === 0) {
        console.warn("[Context-Menu] Caught zero-coordinate event. Bypassing reveal.");
        return;
    }

    // [v1.41.149] Clean Visibility Reveal
    menu.style.display = 'block';
    menu.style.zIndex = '100005'; // Ensure it survives above HUD and other fragments

    // Boundary check for window (v1.35 Hardened)
    const menuWidth = 240;
    const menuHeight = 350; // Increased safety margin for multi-entry menus

    if (x + menuWidth > window.innerWidth) x -= menuWidth;
    if (y + menuHeight > window.innerHeight) y -= (menuHeight / 2); // Intelligent lift for bottom clicks

    menu.style.left = x + 'px';
    menu.style.top = y + 'px';

    const isVideo = isVideoItem(item);

    const mediaType = getMediaTypeString(item);

    // Media Title Header
    const titleHeader = document.createElement('div');
    titleHeader.className = 'context-menu-header';
    titleHeader.innerHTML = `
        <div style="font-weight: 800; font-size: 11px; color: var(--accent-color); margin-bottom: 4px; border-bottom: 1px solid var(--border-color); padding-bottom: 6px; letter-spacing: 0.5px; text-transform: uppercase;">
            ${mediaType}
        </div>
        <div style="font-size: 13px; font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">
            ${item.name || 'Unknown Item'}
        </div>
    `;
    menu.appendChild(titleHeader);

    const options = [
        { label: isVideo ? 'Im Video Player abspielen' : 'Abspielen', icon: '▶️', action: () => { if (typeof playMediaObject === 'function') playMediaObject(item); } },
        { label: 'Zur Queue hinzufügen', icon: '➕', action: () => { if (typeof addToQueue === 'function') addToQueue(item); } }
    ];

    if (isVideo) {
        options.push({ label: 'Video analysieren (FFprobe)', icon: '🔍', action: () => { if (typeof eel !== "undefined") eel.analyze_media_item(item.path)(); } });
    }

    options.push({
        label: 'Metadaten Editieren', icon: '📝', action: () => {
            if (typeof switchTab === 'function') switchTab('edit');
            setTimeout(() => { if (typeof openEditForm === 'function') openEditForm(item); }, 200);
        }
    });

    options.push({ label: 'Im Dateisystem öffnen', icon: '📁', action: () => { if (typeof eel !== "undefined") eel.open_in_explorer(item.path)(); } });

    options.forEach(opt => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'context-menu-item';
        itemDiv.innerHTML = `<span style="margin-right:10px;">${opt.icon}</span> ${opt.label}`;
        itemDiv.onclick = (event) => {
            event.stopPropagation();
            opt.action();
            hideContextMenu();
        };
        menu.appendChild(itemDiv);
    });

    // Close on click elsewhere
    document.addEventListener('click', hideContextMenu, { once: true });
}

function hideContextMenu() {
    const menu = document.getElementById('context-menu');
    if (menu) menu.style.display = 'none';
}

window.addEventListener('click', hideContextMenu);
window.addEventListener('scroll', hideContextMenu, true);

/**
 * Common Splitter Initialization
 * Side: 'left', 'right', 'top', 'bottom'.
 */
function initSplitter(splitterId, targetPaneId, containerId, orientation = 'vertical', side = 'left') {
    const splitter = document.getElementById(splitterId);
    const targetPane = document.getElementById(targetPaneId);
    const container = document.getElementById(containerId);
    let isDragging = false;

    if (!splitter || !targetPane || !container) return;

    const isVertical = orientation === 'vertical';
    const storageKey = `mwv_splitter_${splitterId}`;

    let savedPos = localStorage.getItem(storageKey);
    if (savedPos && isVertical) {
        const numericPos = parseInt(savedPos);
        if (numericPos > 600) savedPos = "300";
    }

    if (savedPos) {
        if (isVertical) {
            targetPane.style.width = savedPos + 'px';
        } else {
            targetPane.style.height = savedPos + 'px';
        }
        targetPane.style.flex = 'none';
    }

    splitter.addEventListener('mousedown', (e) => {
        isDragging = true;
        splitter.classList.add('active');
        document.body.style.cursor = (isVertical ? 'col-resize' : 'ns-resize');
        e.preventDefault();
    });

    window.addEventListener('mousemove', (e) => {
        if (!isDragging) return;
        const rect = container.getBoundingClientRect();
        let size;

        if (isVertical) {
            if (side === 'left') {
                size = e.clientX - rect.left;
            } else {
                size = rect.right - e.clientX;
            }
            const minW = 150;
            const maxW = rect.width - 250;
            if (size < minW) size = minW;
            if (size > maxW) size = maxW;
            targetPane.style.width = size + 'px';
        } else {
            if (side === 'top' || side === 'left') {
                size = e.clientY - rect.top;
            } else {
                size = rect.bottom - e.clientY;
            }
            const minH = 100;
            const maxH = rect.height - 100;
            if (size < minH) size = minH;
            if (size > maxH) size = maxH;
            targetPane.style.height = size + 'px';
        }
        targetPane.style.flex = 'none';
        localStorage.setItem(storageKey, size);
    });

    window.addEventListener('mouseup', () => {
        if (!isDragging) return;
        isDragging = false;
        splitter.classList.remove('active');
        document.body.style.cursor = 'default';
    });
}

/**
 * Common Toast Notifications
 */
function showToast(message, duration = 3000) {
    if (typeof eel !== "undefined" && typeof eel.log_js_error === 'function') {
        eel.log_js_error({ type: 'TOAST', message: message });
    }
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.innerText = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.remove();
    }, duration + 300);
}

/**
 * Media Type Detection
 */
function isVideoItem(item) {
    if (!item) return false;
    const path = item.path || item.relpath || item.name || '';
    const cat = (item.category || '').toLowerCase();

    // 1. SSOT: Extension-First Priority (v1.46.026)
    const videoExtensions = window.CONFIG?.video_extensions || ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.ogv', '.ts'];
    const audioExtensions = window.CONFIG?.audio_extensions || ['.mp3', '.m4a', '.wav', '.flac', '.ogg', '.aac', '.m4p', '.wma'];

    const extMatch = path.match(/\.([a-z0-9_]+)$/i);
    const ext = extMatch ? "." + extMatch[1].toLowerCase() : "";

    // 2. [v1.46.031] AUDIO GUARD: If it looks like audio, it is NEVER video.
    if (ext && audioExtensions.includes(ext)) {
        if (typeof window.__mwv_audit_count === 'undefined') window.__mwv_audit_count = 0;
        if (window.__mwv_audit_count < 10) {
            console.debug(`[FILTER-AUDIT] PASS: ${item.name} matches Audio Extension. Guarding classification.`);
            window.__mwv_audit_count++;
        }
        return false;
    }

    // 3. Strict Video Extension Match
    if (ext && videoExtensions.includes(ext)) return true;

    // 4. Category Fallbacks (Legacy)
    const videoCategories = ['video', 'movie', 'serie', 'sh', 'sz', 'sp', 'sw', 'documentation'];
    if (videoCategories.includes(cat)) return true;

    // 5. Multimedia Ambiguity Resolution
    if (cat === 'multimedia') {
        // Since we already passed the Audio Guard above, if we are still here, it might be video
        // But for safety, we only return true if it's NOT explicitly an audio extension
        return true;
    }

    return false;
}

/**
 * [v1.46.025] Forensic Media Detector: Audio
 */
function isAudioItem(item) {
    if (!item) return false;
    const path = item.path || item.relpath || "";
    const cat = (item.category || '').toLowerCase();

    // 1. SSOT: Extension-First Priority (v1.46.026)
    const audioExtensions = window.CONFIG?.audio_extensions || ['.mp3', '.m4a', '.wav', '.flac', '.ogg', '.aac', '.m4p', '.wma', '.m4b', '.oga'];
    const extMatch = path.match(/\.([a-z0-9_]+)$/);
    const ext = extMatch ? "." + extMatch[1].toLowerCase() : "";

    // [v1.46.026] Forensic Logging
    if (typeof window.__mwv_audio_log_count === 'undefined') window.__mwv_audio_log_count = 0;
    if (window.__mwv_audio_log_count < 10) {
        console.debug(`[FE-AUDIT] Extension Match: ${item.name} | Ext: ${ext} | Result: AUDIO`);
        window.__mwv_audio_log_count++;
    }
    if (extMatch) return true;

// 2. Category Matching
const audioCategories = ['audio', 'music', 'album', 'podcast', 'audiobook', 'hörbuch', 'klassik', 'musik'];
if (audioCategories.includes(cat)) {
    if (typeof window.__mwv_audio_log_count === 'undefined') window.__mwv_audio_log_count = 0;
    if (window.__mwv_audio_log_count < 10) {
        console.debug(`[FE-AUDIT] Category Match: ${item.name} | Cat: ${cat} | Result: AUDIO`);
        window.__mwv_audio_log_count++;
    }
    return true;
}

// Forensic signature fallbacks
if (item.bitrate && !item.resolution && !isPhotoItem(item)) return true;
if (item.duration && !item.fps && !isPhotoItem(item) && !isVideoItem(item)) return true;

// [v1.46.026] Unknown items defaulting to Audio for visibility
const isVid = isVideoItem(item);
const isPic = isPhotoItem(item);
if (!isVid && !isPic && path) return true;

return false;
}

/**
 * [v1.46.023] Forensic Photo Detection
 */
function isPhotoItem(item) {
    if (!item) return false;
    const photoCategories = ['bilder', 'images', 'pictures', 'multimedia'];
    const internalCat = (item.category || '').toLowerCase();

    // [v1.46.023] Branch-Aware multimedia check (only if non-audio/video)
    if (photoCategories.includes(internalCat)) {
        if (!isVideoItem(item) && !(item.path || "").match(/\.(mp3|wav|flac|m4a|ogg|mp4|mkv|avi|mov)$/i)) {
            return true;
        }
    }

    const path = item.path || item.relpath || item.name || "";
    const photoExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp', '.tiff', '.svg'];
    const extMatch = path.match(/\.([a-z0-9_]+)$/);
    const ext = extMatch ? "." + extMatch[1].toLowerCase() : "";

    return ext && photoExtensions.includes(ext);
}

/**
 * Robust Media Type Diagnostic String (v1.35.60)
 * Returns requested types: audio, audio transcoded, video native, video transcoded hd.
 */
function getMediaTypeString(item) {
    if (!item) return 'Unknown';
    const isVideo = isVideoItem(item);
    const path = (item.path || item.name || '').toLowerCase();

    if (isVideo) {
        if (path.includes('.iso') || path.includes('.mp4_transcoded')) return 'video transcoded hd';
        if (path.includes('.mp4_pass')) return 'video native (remux)';
        if (path.endsWith('.mp4')) return 'video native';
        return 'video transcoded hd'; // Default for MKV, etc.
    } else {
        if (path.includes('_transcoded')) return 'audio transcoded';
        return 'audio';
    }
}

/**
 * Library UI Badges
 */
function getCategoryBadgeHtml(item) {
    if (!item || !item.category) return '';
    const cat = item.category.toLowerCase();

    // SVG Sprite mapping (references assets/icons.svg)
    const iconMap = {
        'klassik': '#icon-klassik',
        'soundtrack': '#icon-soundtrack',
        'podcast': '#icon-podcast',
        'nfo': '#icon-nfo',
        'album': '#icon-album',
        'compilation': '#icon-compilation',
        'single': '#icon-single',
        'series': '#icon-series',
        'documentation': '#icon-documentation',
        'mix': '#icon-mix',
        'hörbuch': '#icon-hörbuch',
        'video_iso': '#icon-optical-folder'
    };

    const legacyIcons = {
        'film': '#icon-video',
        'bilder': '#icon-generic',
        'iso/image': '#icon-disk',
        'playlist': '#icon-generic'
    };

    const iconId = iconMap[cat] || legacyIcons[cat] || '';
    if (!iconId) return '';

    return `<div style="position:absolute; bottom:-4px; right:-4px; background:white; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:12px; box-shadow:0 1px 3px rgba(0,0,0,0.3); z-index:5; padding: 4px;" title="${item.category}">
        <svg width="12" height="12" style="color:var(--text-master);"><use href="assets/icons.svg${iconId}"></use></svg>
    </div>`;
}
/**
 * Updates the technical sync anchor in the footer (v1.41.00).
 * Format: [DB: X | GUI: Y]
 */
/**
 * Updates the technical sync anchor in footer, sidebar, and HUD (v1.46.03 Unified SSOT).
 * Format: [FS: Z | DB: X | GUI: Y]
 * Orchestrates parity across all technical diagnostic containers.
 */
function updateSyncAnchor(dbCount, guiCount, fsSize = null) {
    // 1. Capture and Persist Metrics
    if (dbCount !== undefined) window.__mwv_last_db_count = dbCount;
    if (guiCount !== undefined) window.__mwv_last_gui_count = guiCount;
    if (fsSize !== null) window.__mwv_last_fs_size = fsSize;

    const finalDb = (window.__mwv_last_db_count !== undefined) ? window.__mwv_last_db_count : '--';
    const finalGui = (guiCount !== undefined) ? guiCount : (typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : '--');
    const finalFs = window.__mwv_last_fs_size || 0;

    // Formatting filesystem size
    let sizeStr = "--";
    if (finalFs > 0) {
        if (finalFs > 1024 * 1024) sizeStr = (finalFs / (1024 * 1024)).toFixed(1) + "MB";
        else if (finalFs > 1024) sizeStr = (finalFs / 1024).toFixed(1) + "KB";
        else sizeStr = finalFs + "B";
    }

    // 2. PRIMARY: Footer Minimalist Anchor
    const footerAnchor = document.getElementById('footer-sync-anchor');
    if (footerAnchor) {
        footerAnchor.innerText = `[FS: ${sizeStr} | DB: ${finalDb} | GUI: ${finalGui}]`;
        const isParity = (finalDb !== '--' && finalGui !== '--' && parseInt(finalDb) === parseInt(finalGui));
        footerAnchor.style.color = isParity ? '#2ecc71' : '#f1c40f';
        footerAnchor.style.borderColor = isParity ? 'rgba(46, 204, 113, 0.4)' : 'rgba(241, 196, 15, 0.4)';

        // [v1.46.015] Manual Sync Trigger
        if (!footerAnchor.onclick) {
            footerAnchor.style.cursor = 'pointer';
            footerAnchor.title = "Click to force Manual Hydration Pulse";
            footerAnchor.onclick = () => {
                console.warn("[UI-SYNC] Manual Pulse Triggered from Footer Anchor.");
                if (typeof refreshLibrary === 'function') refreshLibrary();
            };
        }
    }

    // 3. SECONDARY: Diagnostics Sidebar Metrics
    const sidebarAnchor = document.getElementById('sb-parity-anchor');
    const sbDbCount = document.getElementById('diag-db-count-sidebar');
    const sbGuiCount = document.getElementById('diag-gui-count-sidebar');

    if (sidebarAnchor) {
        sidebarAnchor.innerText = `[FS: ${sizeStr} | DB: ${finalDb} | GUI: ${finalGui}]`;
        const isParityError = (parseInt(finalDb) !== parseInt(finalGui));
        sidebarAnchor.style.color = isParityError ? '#e74c3c' : 'var(--accent-color)';
    }
    if (sbDbCount) sbDbCount.innerText = finalDb;
    if (sbGuiCount) sbGuiCount.innerText = finalGui;

    // 4. TERTIARY: Footer DB Status Cluster
    const footerDbDisp = document.getElementById('footer-db-count');
    const libCountLabel = document.getElementById('lib-count-label');
    if (footerDbDisp) footerDbDisp.innerText = finalDb;
    if (libCountLabel) libCountLabel.innerText = finalGui;

    // 5. TRACE: Periodic parity audit log
    if (window.iterations % 20 === 0) {
        console.debug(`[SYNC-AUDIT] Parity check: DB(${finalDb}) vs GUI(${finalGui})`);
    }
}

/**
 * Application Performance Mode Controller.
 */
function setAppModeUI(mode) {
    if (typeof eel !== 'undefined' && typeof eel.set_app_mode === 'function') {
        eel.set_app_mode(mode)();
    }
    localStorage.setItem('mwv_app_mode', mode);
    if (typeof showToast === 'function') showToast(`App Mode: ${mode}`, 1500);

    // Update Sidebar Buttons if they exist
    document.querySelectorAll('.nav-item').forEach(btn => {
        if (btn.innerText.includes(mode)) btn.classList.add('active');
        else if (btn.innerText.includes('Performance') || btn.innerText.includes('Bandwidth')) {
            btn.classList.remove('active');
        }
    });
}

/**
 * Hydration Mode Controller (v1.41.00).
 * Controls whether the UI shows Mock, Real DB, or Both items.
 * M: Mock | R: Real | B: Both
 */
/**
 * Hydration Mode Controller (v1.45.105).
 * Controls whether the UI shows Mock, Real DB, or Both items.
 * Centralized in common_helpers.js as the SSOT for hydration state.
 */
function refreshForensicLeds() {
    const mode = window.__mwv_hydration_mode || localStorage.getItem('mwv_hydration_mode') || 'both';

    ['M', 'R', 'B', 'DB'].forEach(id => {
        const targetIds = [`hydr-btn-${id}`, `hud-btn-${id}`];

        targetIds.forEach(elId => {
            const btn = document.getElementById(elId);
            if (!btn) return;

            // Health/Mode Determination
            const isActive = (mode === 'mock' && id === 'M') ||
                (mode === 'real' && id === 'R') ||
                (mode === 'both' && id === 'B') ||
                (id === 'DB');

            if (id === 'DB') {
                const health = window.__mwv_last_db_health || 'unknown';
                let healthColor = '#f1c40f'; // Default: Yellow
                let healthShadow = 'none';

                if (health === 'ok') {
                    healthColor = '#2ecc71'; // Green
                    healthShadow = '0 0 10px rgba(46, 204, 113, 0.4)';
                } else if (health.includes('error') || health.includes('corrupt') || health === 'red') {
                    healthColor = '#e74c3c'; // Red
                    healthShadow = '0 0 15px rgba(231, 76, 60, 0.6)';
                }

                btn.style.color = healthColor;
                btn.style.boxShadow = healthShadow;
                btn.style.opacity = '1';
                btn.title = `Database Status: ${health.toUpperCase()} | Size: ${window.__mwv_last_db_size || 0} bytes`;
            } else {
                btn.style.opacity = isActive ? '1' : '0.3';
                btn.style.color = isActive ? 'var(--accent-color)' : 'var(--text-dim)';
            }
        });
    });
}

/**
 * Hydration Mode Controller (v1.45.105)
 */
function setHydrationMode(mode) {
    if (!mode) return;

    // [v1.46.026] UI Performance Guard (Debouncing)
    if (window.__mwv_hydration_in_progress) {
        console.warn("[Hydration] Sync already in progress. Blocking redundant request.");
        if (typeof showToast === 'function') showToast("Synchronisierung läuft...", 500);
        return;
    }
    window.__mwv_hydration_in_progress = true;

    // [FE-AUDIT] Technical User Reaction Log
    console.info(`[FE-AUDIT] Interaction: setHydrationMode -> ${mode.toUpperCase()}`);
    if (typeof mwv_trace === 'function') mwv_trace('FOOTER-UI', 'HYD-CHANGE', { mode });

    window.__mwv_hydration_mode = mode;
    localStorage.setItem('mwv_hydration_mode', mode);

    if (typeof refreshForensicLeds === 'function') refreshForensicLeds();
    if (typeof showToast === 'function') showToast(`HYDRATION: ${mode.toUpperCase()}`, 1000);

    // 3. TRIGGER ATOMIC RE-HYDRATION PULSE (v1.45.105)
    const runPulse = () => {
        console.info(`>>> [Forensic-Hydration] Pulse Complete. Triggering UI Sync...`);
        if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
        if (typeof renderLibrary === 'function') renderLibrary();
        setTimeout(() => { window.__mwv_hydration_in_progress = false; }, 500);
    };

    const triggerLoad = () => {
        if (typeof loadLibrary === 'function') {
            console.debug(`[Hydration] Loading Library (M/R/B Sync)...`);
            const result = loadLibrary();
            if (result instanceof Promise) {
                result.then(runPulse);
            } else {
                setTimeout(runPulse, 300);
            }
        } else {
            runPulse();
        }
    };

    // 1. Sync Backend ALWAYS BEFORE triggerLoad() to prevent race conditions (v1.46.037)
    if (typeof eel !== 'undefined' && typeof eel.set_hydration_mode === 'function') {
        console.debug(`[Hydration] Syncing backend...`);
        eel.set_hydration_mode(mode)(() => {
            console.info(`[Hydration] Backend ACK received. Triggering library fetch.`);
            triggerLoad();
        });
    } else {
        triggerLoad();
    }
}

// Initial UI Sync for Hydration Mode
document.addEventListener('DOMContentLoaded', () => {
    const savedMode = localStorage.getItem('mwv_hydration_mode') || 'both';
    setTimeout(() => setHydrationMode(savedMode), 1000);
});

// Global Export
window.updateSyncAnchor = updateSyncAnchor;
window.setHydrationMode = setHydrationMode;
window.setAppModeUI = setAppModeUI;

/**
 * Forcefully terminates the application (v1.41.164/165).
 */
async function exitApplication() {
    console.warn("☢️ [APP-EXIT] Triggering Nuclear Shutdown...");

    // 1. Immediate Visual Feedback
    const overlay = document.createElement('div');
    overlay.id = 'shutdown-nuclear-overlay';
    overlay.style.cssText = `
        position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
        background: rgba(0,0,0,0.95); z-index: 999999;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        color: #ff3366; font-family: monospace; font-weight: 900;
        backdrop-filter: blur(10px); text-align: center;
    `;
    overlay.innerHTML = `
        <div style="font-size: 3em; margin-bottom: 20px;">☢️</div>
        <div style="font-size: 1.5em; letter-spacing: 2px;">SHUTDOWN IN PROGRESS</div>
        <div style="margin-top: 10px; opacity: 0.6; font-size: 0.8em;">Purging process tree & releasing locks...</div>
    `;
    document.body.appendChild(overlay);

    // 2. Trigger Backend Exit
    if (typeof eel !== 'undefined' && typeof eel.shutdown_backend === 'function') {
        try {
            // No await needed, backend will kill itself mid-flight
            eel.shutdown_backend()();
        } catch (e) {
            console.error("[APP-EXIT] RPC Failed:", e);
        }
    }

    // 3. Last Resort: Close Window (after 500ms grace period for RPC)
    setTimeout(() => {
        window.close();
        // If window.close() is blocked, we still leave the overlay up.
    }, 500);
}

window.exitApplication = exitApplication;

/**
 * UI Flag Pulse (v1.46.005)
 * Applies all global system flags to the DOM instantly.
 */
function applySystemFlags() {
    const config = window.CONFIG;
    if (!config) return;

    console.log("[UI-PULSE] Applying System Visibility Flags...");

    // Map: Config Key -> Selector List
    const flagMap = {
        // Technical HUDs
        "enable_technical_hud": [".header-pills-container"],
        "enable_diagnostics_hud": ["#header-sync-anchor", "#header-btn-status"],
        "enable_dom_auditor": [".footer-diag-cluster"],
        "enable_sync_anchor": ["#footer-sync-anchor"],
        "enable_footer_hud_cluster": [".footer-hud-cluster"],
        "enable_footer_db_status": [".footer-db-status"],
        "enable_header_power_button": ["#header-btn-power-exit"],
        "enable_zen_mode": ["header", "footer"],

        // Overlays & Tags
        "technical_overlay.stable_mode_visible": [".stable-mode-overlay"],
        "technical_overlay.deck_tag_visible": ["#proof-deck-tag"],
        "technical_overlay.queue_tag_visible": ["#proof-queue-tag"],

        // Fragments (Sidebars)
        "ui_fragments.player": ["#main-sidebar"],
        "ui_fragments.video": ["#video-cinema-container"],
        "ui_fragments.library": ["#library-container"]
    };

    Object.keys(flagMap).forEach(key => {
        const isEnabled = getConfigDeepValue(config, key);
        const selectors = flagMap[key];

        selectors.forEach(sel => {
            const el = document.querySelector(sel);
            if (el) {
                if (isEnabled) el.classList.remove('mwv-flag-hidden');
                else el.classList.add('mwv-flag-hidden');
            }
        });
    });

    if (typeof mwv_trace === 'function') {
        mwv_trace('UI', 'PULSED', { ts: Date.now() });
    }
}

/**
 * Helper for deep lookup in config object.
 */
function getConfigDeepValue(obj, path) {
    if (!path.includes('.')) return !!obj[path];
    return path.split('.').reduce((prev, curr) => (prev && prev[curr] !== undefined) ? prev[curr] : undefined, obj);
}

// Global Export
window.applySystemFlags = applySystemFlags;
window.getConfigDeepValue = getConfigDeepValue;

// Created with MWV v1.46.005-MASTER
