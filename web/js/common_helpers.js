/**
 * Common UI Utilities & Helpers
 * Extracted from app.html to improve modularity and avoid line-number drift.
 */

const CATEGORY_MAP = {
    "audio": ["Audio", "Album", "Hörbuch", "Klassik", "Compilation", "Single", "Podcast", "Radio", "Soundtrack", "Playlist", "Music", "Song"],
    "video": ["Video", "Film", "Serie", "ISO/Image", "Musikvideos", "Animes", "Cartoons", "Movie", "TV Show"],
    "film": ["Film", "Film Object"],
    "serie": ["Serie"],
    "album": ["Album"],
    "soundtrack": ["Soundtrack"],
    "compilation": ["Compilation"],
    "single": ["Single"],
    "klassik": ["Klassik"],
    "playlist": ["Playlist"],
    "podcast": ["Podcast"],
    "images": ["Bilder"],
    "documents": ["Dokument"],
    "ebooks": ["E-Book"],
    "abbild": ["Abbild", "ISO/Image", "Disk Image", "PAL DVD", "NTSC DVD", "Blu-ray", "PAL DVD (Abbild)", "NTSC DVD (Abbild)", "DVD (Abbild)", "Blu-ray (Abbild)", "Audio-CD (Abbild)", "CD-ROM (Abbild)", "Disk-Abbild", "DVD Object"],
    "spiel": ["PC Spiel", "PC Spiel (Index)", "Digitales Spiel (Steam)", "Spiel"],
    "beigabe": ["Supplement", "Beigabe", "Software"]
};

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
 * Updates a progress bar or text.
 */
function update_progress(data) {
    if (typeof data === 'string') {
        safeText('status-info', data);
        return;
    }
    if (data.progress !== undefined) {
        const bar = document.getElementById('progress-bar-inner');
        if (bar) bar.style.width = data.progress + '%';
        safeText('progress-percent', data.progress + '%');
    }
    if (data.status) {
        safeText('status-info', data.status);
    }
}

/**
 * Global Context Menu Controller
 */
function showContextMenu(e, item) {
    e.preventDefault();
    const menu = document.getElementById('context-menu');
    if (!menu) return;

    if (typeof appendUiTrace === 'function') appendUiTrace(`[Context-Menu] Opening for: ${item.name}`);

    // Log context menu opening
    if (typeof mwv_trace === 'function') {
        mwv_trace('UI-INPUT', 'CONTEXT-MENU-OPEN', { itemName: item.name });
    }

    menu.innerHTML = '';
    menu.style.display = 'block';
    
    // Position menu at cursor
    let x = e.pageX;
    let y = e.pageY;
    
    // Boundary check for window
    if (x + 200 > window.innerWidth) x -= 200;
    if (y + 150 > window.innerHeight) y -= 150;
    
    menu.style.left = x + 'px';
    menu.style.top = y + 'px';

    const options = [
        { label: 'Abspielen', icon: '▶️', action: () => playMediaObject(item) },
        { label: 'Warteschlange', icon: '➕', action: () => addToQueue(item) },
        { label: 'Metadaten Editieren', icon: '📝', action: () => openEditForm(item) },
        { label: 'Im Dateisystem öffnen', icon: '📁', action: () => { if (typeof eel !== "undefined") eel.open_in_explorer(item.path)(); } }
    ];

    options.forEach(opt => {
        const itemDiv = document.createElement('div');
        itemDiv.className = 'context-menu-item';
        itemDiv.innerHTML = `<span style="margin-right:10px;">${opt.icon}</span> ${opt.label}`;
        itemDiv.onclick = () => {
            opt.action();
            hideContextMenu();
        };
        menu.appendChild(opt.forEach ? opt : itemDiv);
    });

    // Close on click elsewhere
    document.addEventListener('click', hideContextMenu, { once: true });
}

function hideContextMenu() {
    const menu = document.getElementById('context-menu');
    if (menu) menu.style.display = 'none';
}

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
    // 1. Check Category
    const videoCategories = ['Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos', 'Animes', 'Cartoons', 'Movie', 'TV Show'];
    if (item.category && videoCategories.includes(item.category)) return true;

    // 2. Check Extension
    const path = item.path || item.relpath || "";
    const videoExtensions = ['.mp4', '.mkv', '.iso', '.webm', '.avi', '.mov', '.ts', '.m2ts', '.vob', '.m4v', '.mpg', '.mpeg', '.flv', '.wmv'];
    const ext = path.toLowerCase().slice(((path.lastIndexOf(".") - 1) >>> 0) + 2);
    if (ext && videoExtensions.includes("." + ext)) return true;

    return false;
}

/**
 * Library UI Badges
 */
function getCategoryBadgeHtml(item) {
    if (!item || !item.category) return '';
    const specialCategories = ['H\u00f6rbuch', 'Compilation', 'Serie', 'Film', 'E-Book', 'Dokument', 'Bilder', 'ISO/Image', 'Soundtrack', 'Playlist'];
    if (!specialCategories.includes(item.category)) return '';

    let catIcon = '';
    if (item.category === 'H\u00f6rbuch') catIcon = '<svg width="12" height="12"><use href="#icon-audio"></use></svg>';
    else if (item.category === 'Film') catIcon = '<svg width="12" height="12"><use href="#icon-video"></use></svg>';
    else if (item.category === 'Serie') catIcon = '<svg width="12" height="12"><use href="#icon-tv"></use></svg>';
    else if (item.category === 'Dokument') catIcon = '<svg width="12" height="12"><use href="#icon-generic"></use></svg>';
    else if (item.category === 'E-Book') catIcon = '<svg width="12" height="12"><use href="#icon-generic"></use></svg>';
    else if (item.category === 'Bilder') catIcon = '<svg width="12" height="12"><use href="#icon-generic"></use></svg>️';
    else if (item.category === 'ISO/Image') catIcon = '<svg width="12" height="12"><use href="#icon-disk"></use></svg>';
    else if (item.category === 'Compilation') catIcon = '<svg width="12" height="12"><use href="#icon-save"></use></svg>';
    else if (item.category === 'Soundtrack') catIcon = '<svg width="12" height="12"><use href="#icon-audio"></use></svg>';
    else if (item.category === 'Playlist') catIcon = '<svg width="12" height="12"><use href="#icon-generic"></use></svg>';

    if (!catIcon) return '';
    return `<div style="position:absolute; bottom:-4px; right:-4px; background:white; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:12px; box-shadow:0 1px 3px rgba(0,0,0,0.3); z-index:5;" title="${item.category}">${catIcon}</div>`;
}
