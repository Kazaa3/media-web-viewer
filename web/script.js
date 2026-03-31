/**
 * script.js - Legacy application entry point (Modularization in progress)
 */

async function loadMedia() {
    try {
        if (typeof eel === 'undefined') return;
        const result = await eel.scan_media()();
        const list = document.getElementById("media-list");
        if (list) {
            list.innerHTML = "";
            for (const item of result.media) {
                const li = document.createElement("li");
                li.textContent = item.name;
                list.appendChild(li);
            }
        }
    } catch (e) {
        console.error("Fehler beim Medien-Laden: " + e.message);
    }
}

/**
 * Unified Initialization Hook
 */
window.addEventListener('DOMContentLoaded', function () {
    // Initialize Environment Module
    if (typeof initEnvironmentModule === 'function') {
        initEnvironmentModule();
    } else {
        // Fallback if environment.js is not yet loaded or failed
        if (typeof initDefaultFolder === 'function') initDefaultFolder();
        if (typeof loadEnvironmentInfo === 'function') loadEnvironmentInfo();
    }

    // Diagnostics & Debug
    if (typeof loadDebugLogs === 'function') {
        loadDebugLogs();
    }
});
