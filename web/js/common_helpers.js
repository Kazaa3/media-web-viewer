/**
 * Common UI Utilities & Helpers
 * Extracted from app.html to improve modularity and avoid line-number drift.
 */

/**
 * Toggles a modal's visibility.
 */
function toggleModal(modalId, forceState) {
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.warn(`[UI] Cannot toggle modal: ${modalId} not found.`);
        return;
    }
    // traceUiNav is assumed to be in ui_nav_helpers.js
    if (typeof traceUiNav === 'function') {
        traceUiNav('MODAL', modalId, {force: forceState});
    }
    
    const newState = (forceState !== undefined) ? forceState : (modal.style.display === 'none' || modal.style.display === '');
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
 * Global Splitter Initialization
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
