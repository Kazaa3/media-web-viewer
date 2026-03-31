/**
 * item.js
 * Item-specific logic and UI helpers.
 * Handles category badges, inventory list rendering, and detail views.
 */

/**
 * Returns consistent badge HTML for an item's category.
 */
function getCategoryBadgeHtml(item) {
    if (!item || !item.category) return '';
    const cat = (item.category || '').toLowerCase();
    let color = '#ccc';
    if (CATEGORY_MAP.audio.includes(item.category)) color = '#3498db';
    if (CATEGORY_MAP.video.includes(item.category)) color = '#e74c3c';
    if (CATEGORY_MAP.film.includes(item.category)) color = '#f39c12';
    if (CATEGORY_MAP.serie.includes(item.category)) color = '#e74c3c';
    if (CATEGORY_MAP.spiel.includes(item.category)) color = '#2ecc71';

    return `<span class="category-badge" style="background: ${color}; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.75em; font-weight: bold;">${item.category}</span>`;
}

/**
 * Loads and renders the inventory side-list in the Item/Edit tab.
 */
async function loadEditItems() {
    if (typeof appendUiTrace === 'function') appendUiTrace("[Item] Loading inventory for Item/Edit tabs...");
    const library = await getLibrary();
    if (library && library.media) {
        // Update both inventory-count and total-library-count if they exist
        const count = library.media.length;
        const countEls = document.querySelectorAll('#inventory-count, #total-library-count');
        countEls.forEach(el => el.innerText = `${count} Entries found`);
        
        renderEditList(library.media);
    }
}

/**
 * Renders the inventory list.
 */
function renderEditList(items) {
    const container = document.getElementById('item-category-list');
    if (!container) return;

    if (!items || items.length === 0) {
        container.innerHTML = `<div style="padding: 20px; color: #999; text-align: center;" data-i18n="item_no_entries">Keine Einträge</div>`;
        return;
    }

    const html = items.map(item => {
        const title = item.tags && item.tags.title ? item.tags.title : (item.name || 'Unknown');
        const artist = item.tags && item.tags.artist ? item.tags.artist : (item.category || '');
        
        return `
            <div class="inventory-item" onclick="openEditFormByName('${item.name.replace(/'/g, "\\'")}')" 
                 style="padding: 12px 16px; border-bottom: 1px solid var(--border-color); cursor: pointer; transition: background 0.1s; border-radius: 8px; margin-bottom: 4px;">
                <div style="font-weight: 700; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--text-primary);" title="${item.name}">${title}</div>
                <div style="font-size: 11px; color: var(--text-secondary); font-weight: 500;">${artist}</div>
            </div>
        `;
    }).join('');

    if (typeof safeHtml === 'function') safeHtml('item-category-list', html);
    else container.innerHTML = html;
}

/**
 * Filters the inventory side-list based on input.
 */
function filterEditList(val) {
    const query = val.toLowerCase();
    const rows = document.querySelectorAll('#item-category-list .inventory-item');
    rows.forEach(row => {
        const text = row.innerText.toLowerCase();
        row.style.display = text.includes(query) ? 'block' : 'none';
    });
}

/**
 * Bridge for opening the edit form by item name.
 */
async function openEditFormByName(name) {
    if (typeof appendUiTrace === 'function') appendUiTrace(`[Item] Fetching details for ${name} to edit...`);
    const library = await getLibrary();
    const item = library.media.find(i => i.name === name);
    if (item && typeof openEditForm === 'function') {
        openEditForm(item);
    }
}
