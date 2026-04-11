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
        countEls.forEach(el => el.innerText = `${count} Titel gefunden`);
        
        renderEditList(library.media);
    }
}

/**
 * Renders the inventory list.
 */
function renderEditList(items) {
    const sidebar = document.getElementById('item-category-list');
    const mainList = document.getElementById('item-list');
    if (!sidebar || !mainList) return;

    if (!items || items.length === 0) {
        mainList.innerHTML = `<div style="padding: 20px; color: #999; text-align: center;" data-i18n="item_no_entries">Keine Einträge</div>`;
        return;
    }

    // 1. Render Categories in Sidebar
    const categories = [...new Set(items.map(i => i.category || 'Unknown'))].sort();
    sidebar.innerHTML = `
        <div class="inventory-category active" onclick="filterByCategory('all', this)" style="padding: 10px 16px; border-radius: 8px; cursor: pointer; font-weight: 700; font-size: 13px; margin-bottom: 4px;">Alle Medien <span style="float: right; opacity: 0.5;">${items.length}</span></div>
    ` + categories.map(cat => {
        const catCount = items.filter(i => i.category === cat).length;
        return `<div class="inventory-category" onclick="filterByCategory('${cat}', this)" style="padding: 10px 16px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 13px; margin-bottom: 4px; color: var(--text-secondary);">${cat} <span style="float: right; opacity: 0.5;">${catCount}</span></div>`;
    }).join('');

    // 2. Render Items in Main List
    renderItemsInMainPane(items);
}

function renderItemsInMainPane(items) {
    const mainList = document.getElementById('item-list');
    if (!mainList) return;

    mainList.innerHTML = items.map(item => {
        const title = item.tags && item.tags.title ? item.tags.title : (item.name || 'Unknown');
        const artist = item.tags && item.tags.artist ? item.tags.artist : (item.category || '');
        const badge = typeof getCategoryBadgeHtml === 'function' ? getCategoryBadgeHtml(item) : '';
        
        return `
            <div class="inventory-item-row" onclick="openEditFormByName('${item.name.replace(/'/g, "\\'")}')" 
                 style="display: flex; align-items: center; padding: 14px 20px; border-bottom: 1px solid var(--border-color); cursor: pointer; transition: background 0.1s; gap: 15px;">
                <div style="width: 32px; height: 32px; background: var(--bg-secondary); border-radius: 6px; display: flex; align-items: center; justify-content: center; font-size: 16px; position: relative;">
                    ${badge}
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div style="font-weight: 700; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: var(--text-primary);" title="${item.name}">${title}</div>
                    <div style="font-size: 11px; color: var(--text-secondary); font-weight: 500;">${artist} • <span style="opacity: 0.7;">${item.type || 'Media'}</span></div>
                </div>
                <div style="font-size: 10px; font-weight: 800; color: var(--accent-color); text-transform: uppercase;">Edit</div>
            </div>
        `;
    }).join('');
}

async function filterByCategory(cat, btn) {
    document.querySelectorAll('.inventory-category').forEach(b => {
        b.classList.remove('active');
        b.style.color = 'var(--text-secondary)';
        b.style.background = 'transparent';
    });
    btn.classList.add('active');
    btn.style.color = 'var(--text-primary)';
    btn.style.background = 'var(--bg-secondary)';

    const library = await getLibrary();
    const items = library.media || [];
    const filtered = cat === 'all' ? items : items.filter(i => i.category === cat);
    renderItemsInMainPane(filtered);
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

// Created with MWV v1.46.00-MASTER
