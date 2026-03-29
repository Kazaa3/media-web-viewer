/**
 * browse.js
 * File Browser & Filesystem Navigation Module.
 * Focused strictly on the "File" tab.
 */

let fbCurrentPath = null;
let fbParentPath = null;

/**
 * Navigates to a specific directory.
 */
async function fbNavigate(dirPath, retryCount = 0) {
    if (typeof eel === 'undefined') return;
    try {
        if (typeof appendUiTrace === 'function') appendUiTrace(`[FileBrowser] Navigating to: ${dirPath || "root"}`);
        let result = await eel.browse_dir(dirPath || null)();
        
        if (result.error) {
            console.error("[FileBrowser] Error:", result.error);
            const list = document.getElementById('fb-list');
            if (list) list.innerHTML = `<p style="color: #c33;">Error: ${result.error}</p>`;
            return;
        }

        fbCurrentPath = result.path;
        fbParentPath = result.parent;
        
        // Update UI elements
        if (typeof safeValue === 'function') safeValue('fb-path-input', result.path);
        else document.getElementById('fb-path-input').value = result.path;

        const pathDisplay = document.getElementById('path-display');
        if (pathDisplay) pathDisplay.innerText = result.path;

        const backBtn = document.getElementById('fb-back');
        if (backBtn) backBtn.disabled = !result.parent;

        renderFileList(result.items);
        
    } catch (e) {
        console.error("[FileBrowser] Navigation failed:", e);
        if (retryCount < 3) {
            setTimeout(() => fbNavigate(dirPath, retryCount + 1), 1000);
        }
    }
}

/**
 * Renders the file list inside the file browser.
 */
function renderFileList(items) {
    const list = document.getElementById('fb-list');
    if (!list) return;

    if (!items || items.length === 0) {
        list.innerHTML = `<div style="padding: 20px; color: #999; text-align: center;">Directory is empty</div>`;
        return;
    }

    const html = items.map(item => {
        const isFolder = item.type === 'folder';
        const icon = isFolder ? 'folder' : 'audio'; // Simplified, could be more granular
        const size = isFolder ? '' : `<span style="color: #999; font-size: 0.85em;">${item.size}</span>`;
        
        return `
            <div class="fb-row" onclick="${isFolder ? `fbNavigate('${item.path.replace(/'/g, "\\'")}')` : `addAndRefresh('${item.path.replace(/'/g, "\\'")}', this)`}"
                 style="display: flex; align-items: center; padding: 10px 15px; border-bottom: 1px solid #f5f5f5; cursor: pointer; transition: background 0.1s; border-radius: 6px; margin-bottom: 4px;">
                <span style="font-size: 1.3em; margin-right: 15px;">
                    <svg width="20" height="20"><use href="#icon-${icon}"></use></svg>
                </span>
                <span style="flex: 1; font-size: 0.95em; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;" title="${item.name}">${item.name}</span>
                ${size}
            </div>
        `;
    }).join('');

    list.innerHTML = html;
}

/**
 * Adds a file and refreshes the library.
 */
async function addAndRefresh(path, element) {
    if (typeof addFileToLibrary === 'function') {
        const statusEl = element.querySelector('span:last-child');
        const originalText = statusEl ? statusEl.innerText : '';
        if (statusEl) statusEl.innerText = 'adding...';
        
        const res = await addFileToLibrary(path);
        if (res && (res.status === 'added' || res.status === 'exists')) {
            if (statusEl) {
                statusEl.innerText = res.status === 'added' ? 'Added' : 'Exists';
                statusEl.style.color = res.status === 'added' ? '#2a7' : '#c90';
            }
            if (typeof refreshLibrary === 'function') refreshLibrary();
        } else {
            if (statusEl) statusEl.innerText = originalText;
        }
    }
}

/**
 * Navigates to the parent directory.
 */
function fbBack() {
    if (fbParentPath) fbNavigate(fbParentPath);
}

/**
 * Opens the system folder picker.
 */
async function fbPickFolder() {
    if (typeof eel === 'undefined') return;
    const folder = await eel.pick_folder()();
    if (folder) {
        if (typeof switchTab === 'function') {
            switchTab('file', document.querySelector('.tab-btn[onclick*="file"]'));
        }
        fbNavigate(folder);
    }
}

/**
 * Context menu management for files.
 */
let contextMenuItem = null;

function showContextMenu(e, item) {
    e.preventDefault();
    contextMenuItem = item;
    const menu = document.getElementById('custom-context-menu');
    if (!menu) return;

    // Logic to determine which items to show based on type
    const ext = (item.name || '').toLowerCase().split('.').pop();
    const isVideo = ['mp4', 'mkv', 'webm', 'mov', 'avi', 'ts', 'm2ts', 'vob'].includes(ext);
    
    const videoSect = document.getElementById('ctx-video-section');
    if (videoSect) videoSect.style.display = isVideo ? 'block' : 'none';

    menu.style.display = 'block';
    menu.style.left = e.clientX + 'px';
    menu.style.top = e.clientY + 'px';
}

function hideContextMenu() {
    const menu = document.getElementById('custom-context-menu');
    if (menu) menu.style.display = 'none';
}

window.addEventListener('click', hideContextMenu);
window.addEventListener('scroll', hideContextMenu, true);
