/**
 * Logbook & Documentation Helpers
 */

let currentLogbuchEntries = [];
let currentLogbookEditName = null;
let currentLogbookEditFilename = null;

function closeLogbookEditor() {
    const modal = document.getElementById('logbuch-editor-modal');
    if (modal) modal.style.display = 'none';
    currentLogbookEditName = null;
    currentLogbookEditFilename = null;
}

function getLogbookStatusIcon(status) {
    const normalized = (status || 'ACTIVE').toUpperCase();
    if (normalized === 'COMPLETED') return '<span class="icon-check" style="background-color: #2a7; width: 18px; height: 18px;"></span>';
    if (normalized === 'PLAN') return '<span class="icon-plan" style="background-color: #2980b9; width: 18px; height: 18px;"></span>';
    if (normalized === 'DOCS') return '<span class="icon-doc" style="background-color: #8e44ad; width: 18px; height: 18px;"></span>';
    if (normalized === 'BUG') return '<span class="icon-bug" style="background-color: #c0392b; width: 18px; height: 18px;"></span>';
    return '<span class="icon-dot" style="background-color: #27ae60; width: 18px; height: 18px;"></span>';
}

function extractLogbookMeta(markdown) {
    const getTag = (tag, fallback = '') => {
        const re = new RegExp(`<!--\\s*${tag}\\s*:\\s*([^>]+?)\\s*-->`, 'i');
        const m = (markdown || '').match(re);
        return m && m[1] ? m[1].trim() : fallback;
    };

    return {
        category: getTag('Category', 'Planung'),
        titleDe: getTag('Title_DE', ''),
        titleEn: getTag('Title_EN', ''),
        summaryDe: getTag('Summary_DE', ''),
        summaryEn: getTag('Summary_EN', ''),
        status: (getTag('Status', 'ACTIVE') || 'ACTIVE').toUpperCase(),
        date: getTag('Date', new Date().toISOString().slice(0, 10)),
        pinned: getTag('Pinned', 'false').toLowerCase() === 'true'
    };
}

async function loadSqlFiles() {
    const list = document.getElementById('sql-file-list');
    if (!list) return;
    const files = await eel.list_sql_files()();
    list.innerHTML = '';
    (files || []).forEach(file => {
        const btn = document.createElement('button');
        btn.className = 'tab-btn';
        btn.style.width = '100.0%';
        btn.style.textAlign = 'left';
        btn.style.marginBottom = '5px';
        btn.style.background = '#fff';
        btn.textContent = file;
        btn.onclick = () => loadSqlContent(file);
        list.appendChild(btn);
    });
}

async function loadSqlContent(filename) {
    const content = await eel.get_sql_content(filename)();
    safeHtml('sql-content-renderer', content);
    safeText('selected-sql-filename', filename);
}

function stripLogbookFixedTags(markdown) {
    const keys = ['Category', 'Title_DE', 'Title_EN', 'Summary_DE', 'Summary_EN', 'Status', 'Date', 'Pinned'];
    let cleaned = markdown || '';
    keys.forEach(k => {
        cleaned = cleaned.replace(new RegExp(`^\\s*<!--\\s*${k}\\s*:\\s*.*?-->\\s*\\n?`, 'gim'), '');
    });
    return cleaned.trimStart();
}

function buildLogbookFixedTagsBlock(meta) {
    const tags = [
        `<!-- Category: ${meta.category || 'Planung'} -->`,
        `<!-- Title_DE: ${meta.titleDe || ''} -->`,
        `<!-- Title_EN: ${meta.titleEn || ''} -->`,
        `<!-- Summary_DE: ${meta.summaryDe || ''} -->`,
        `<!-- Summary_EN: ${meta.summaryEn || ''} -->`,
        `<!-- Status: ${(meta.status || 'ACTIVE').toUpperCase()} -->`,
        `<!-- Date: ${meta.date || new Date().toISOString().slice(0, 10)} -->`
    ];
    if (meta.pinned) {
        tags.push(`<!-- Pinned: true -->`);
    }
    return tags.join('\n');
}

function openLogbookEditor(name, filename, content) {
    currentLogbookEditName = name;
    currentLogbookEditFilename = filename;
    const modal = document.getElementById('logbuch-editor-modal');
    if (!modal) {
        console.error("Modal 'logbuch-editor-modal' not found!");
        return;
    }
    const nameInput = document.getElementById('logbuch-editor-name');
    const contentInput = document.getElementById('logbuch-editor-content');
    const statusInput = document.getElementById('logbuch-editor-status');
    const categoryInput = document.getElementById('logbuch-editor-category');
    const titleDeInput = document.getElementById('logbuch-editor-title-de');
    const titleEnInput = document.getElementById('logbuch-editor-title-en');
    const summaryDeInput = document.getElementById('logbuch-editor-summary-de');
    const summaryEnInput = document.getElementById('logbuch-editor-summary-en');
    const dateInput = document.getElementById('logbuch-editor-date');
    const title = document.getElementById('logbuch-editor-title');

    if (name) {
        const meta = extractLogbookMeta(content || '');
        title.innerText = `Edit: ${name}`;
        nameInput.value = name;
        contentInput.value = stripLogbookFixedTags(content || '');
        if (statusInput) statusInput.value = meta.status;
        if (categoryInput) categoryInput.value = meta.category;
        if (titleDeInput) titleDeInput.value = meta.titleDe;
        if (titleEnInput) titleEnInput.value = meta.titleEn;
        if (summaryDeInput) summaryDeInput.value = meta.summaryDe;
        if (summaryEnInput) summaryEnInput.value = meta.summaryEn;
        if (dateInput) dateInput.value = meta.date;
        nameInput.disabled = false;
    } else {
        title.innerText = 'New Entry';
        nameInput.value = '';
        contentInput.value = '# Neuer Eintrag\n\n';
        if (statusInput) statusInput.value = 'ACTIVE';
        if (categoryInput) categoryInput.value = 'Planung';
        if (titleDeInput) titleDeInput.value = '';
        if (titleEnInput) titleEnInput.value = '';
        if (summaryDeInput) summaryDeInput.value = '';
        if (summaryEnInput) summaryEnInput.value = '';
        if (dateInput) dateInput.value = new Date().toISOString().slice(0, 10);
        nameInput.disabled = false;
    }

    modal.style.display = 'flex';
    modal.style.zIndex = "4000";
}

/**
 * Renders the sidebar list of logbook entries with filtering and sorting.
 */
function renderLogbuchList(entries) {
    const list = document.getElementById('logbuch-entry-sidebar-items');
    const categoryFilter = document.getElementById('logbuch-category-filter');
    const statusFilter = document.getElementById('logbuch-status-filter');

    const selectedCategory = categoryFilter ? categoryFilter.value : 'Alle';
    const selectedStatus = statusFilter ? statusFilter.value : 'ALL';

    if (!list) return;
    list.innerHTML = '';

    // Filter entries
    const filteredEntries = entries.filter(e => {
        const cat = e.category || 'Misc';
        const catKey = `cat_${cat.toLowerCase()}`;
        const localizedCat = (typeof t === 'function' && t(catKey) !== catKey) ? t(catKey) : cat;

        if (selectedCategory !== 'Alle' && localizedCat !== selectedCategory) return false;
        if (selectedStatus !== 'ALL' && (e.status || 'ACTIVE').toUpperCase() !== selectedStatus) return false;
        return true;
    });

    // Sort: Pinned first, then alphanumeric
    filteredEntries.sort((a, b) => {
        if (a.pinned && !b.pinned) return -1;
        if (!a.pinned && b.pinned) return 1;
        return (a.name || '').localeCompare(b.name || '', undefined, { numeric: true, sensitivity: 'base' });
    });

    const fragment = document.createDocumentFragment();
    filteredEntries.forEach(entry => {
        const btn = document.createElement('div');
        btn.style.cssText = 'padding: 10px 12px; background: #f5f5f5; border-radius: 6px; cursor: pointer; transition: all 0.2s; margin-bottom: 4px; position: relative; display: flex; justify-content: space-between; align-items: center; border: 1px solid transparent;';
        
        const nameWrap = document.createElement('div');
        nameWrap.style.cssText = 'display: flex; align-items: center; gap: 8px; flex: 1; overflow: hidden;';

        if (entry.pinned) {
            const pin = document.createElement('span');
            pin.innerHTML = '<svg width="12" height="12"><use href="#icon-generic"></use></svg>';
            nameWrap.appendChild(pin);
        }

        const nameEl = document.createElement('span');
        nameEl.innerText = entry.name;
        nameEl.style.cssText = 'white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500;';
        nameWrap.appendChild(nameEl);
        btn.appendChild(nameWrap);

        const statusWrap = document.createElement('div');
        statusWrap.style.cssText = 'display: flex; align-items: center; gap: 10px; margin-left: 10px;';

        const iconEl = document.createElement('span');
        iconEl.innerHTML = getLogbookStatusIcon(entry.status || 'ACTIVE');
        statusWrap.appendChild(iconEl);

        const deleteBtn = document.createElement('button');
        deleteBtn.innerHTML = '<svg width="12" height="12"><use href="#icon-delete"></use></svg>';
        deleteBtn.style.cssText = 'background: none; border: none; cursor: pointer; padding: 4px; opacity: 0.3; transition: opacity 0.2s;';
        deleteBtn.onclick = (e) => {
            e.stopPropagation();
            const msg = (typeof t === 'function' ? t('logbook_delete_confirm') : 'Löschen?').replace('{name}', entry.name);
            if (confirm(msg)) deleteLogbookEntry(entry.filename);
        };
        statusWrap.appendChild(deleteBtn);
        btn.appendChild(statusWrap);

        btn.onclick = () => loadLogbuchContent(entry.name, entry.filename);
        fragment.appendChild(btn);
    });
    list.appendChild(fragment);
}

/**
 * Loads and renders the content of a specific logbook entry.
 */
async function loadLogbuchContent(name, filename) {
    const header = document.getElementById('logbuch-viewer-header');
    const metaContainer = document.getElementById('logbuch-entry-meta');
    const scrollContainer = document.getElementById('logbuch-scroll-container');
    const contentEl = document.getElementById('logbuch-tab-content');

    if (header) header.style.display = 'block';
    if (typeof safeText === 'function') safeText('logbuch-tab-title', name);
    if (metaContainer) metaContainer.innerHTML = '';
    if (typeof safeHtml === 'function') safeHtml('logbuch-tab-content', `<div style="color:#999; text-align:center; padding-top:40px;">Laden...</div>`);
    if (scrollContainer) scrollContainer.scrollTop = 0;

    try {
        const markdown = await eel.get_logbook_entry(name)();
        if (!markdown) {
            if (typeof safeHtml === 'function') safeHtml('logbuch-tab-content', `<p style="color: #f44; text-align:center;">Fehler beim Laden.</p>`);
            return;
        }
        const meta = extractLogbookMeta(markdown || '');
        const visibleBody = stripLogbookFixedTags(markdown || '');

        if (metaContainer) {
            metaContainer.innerHTML = `
                <span title="Kategorie"><svg width="12" height="12"><use href="#icon-folder"></use></svg> ${meta.category || '-'}</span>
                <span title="Status">${getLogbookStatusIcon(meta.status)} ${(meta.status || 'active').toUpperCase()}</span>
                <span title="Datum"><svg width="12" height="12"><use href="#icon-generic"></use></svg> ${meta.date || '-'}</span>
            `;
        }

        let html;
        if (typeof marked !== 'undefined') {
            marked.setOptions({ breaks: true, gfm: true });
            html = marked.parse(visibleBody);
        } else {
            html = visibleBody.replace(/\n\n/g, '<br><br>');
        }

        if (typeof safeHtml === 'function') safeHtml('logbuch-tab-content', html);

        // Add edit button
        const footer = document.createElement('div');
        footer.style.cssText = 'margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; display: flex; justify-content: flex-end;';
        const editBtn = document.createElement('button');
        editBtn.innerText = (typeof t === 'function' ? t('edit_btn_edit', 'Bearbeiten') : 'Bearbeiten');
        editBtn.className = 'tab-btn active';
        editBtn.style.cssText = 'padding: 8px 20px; background: #2a7; color: white; border-radius: 6px; cursor: pointer;';
        editBtn.onclick = () => openLogbookEditor(name, filename, markdown);
        footer.appendChild(editBtn);
        if (contentEl) contentEl.appendChild(footer);

    } catch (e) {
        console.error('[loadLogbuchContent] Error:', e);
    }
}

/**
 * Feature Status Modal Logic
 */
async function loadFeatureStatus() {
    const container = document.getElementById('feature-list-container');
    if (!container) return;
    container.innerHTML = `<div style="text-align: center; color: #888; padding: 20px;">Laden...</div>`;

    try {
        const entries = await eel.list_feature_modal_items()();
        container.innerHTML = '';

        let allItems = entries.filter(e => e.summary && e.summary.trim() !== "");
        const allSorted = [...allItems].sort((a, b) => (b.modified_ts || 0) - (a.modified_ts || 0));
        const latest = allSorted.slice(0, 3);
        const latestNames = latest.map(l => l.name);

        renderFeatureSection(container, 'Neueste Updates', latest, true);
        renderFeatureSection(container, 'Offene Features', allItems.filter(f => f.status !== 'COMPLETED' && !latestNames.includes(f.name)));
        renderFeatureSection(container, 'Abgeschlossen', allItems.filter(f => f.status === 'COMPLETED' && !latestNames.includes(f.name)));
    } catch (e) {
        console.error("Error loading features:", e);
    }
}

function renderFeatureSection(container, title, items, highlight = false) {
    if (items.length === 0) return;

    const header = document.createElement('div');
    header.style.cssText = "font-weight: bold; color: #555; font-size: 0.85em; text-transform: uppercase; margin: 15px 0 8px 5px; border-bottom: 2px solid #eee; padding-bottom: 4px;";
    if (highlight) header.style.color = "#2a7";
    header.innerText = title;
    container.appendChild(header);

    items.forEach(feat => {
        const featDiv = document.createElement('div');
        featDiv.style.cssText = "display: flex; align-items: flex-start; gap: 12px; cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s;";
        featDiv.onclick = () => openLogbook(feat.name, feat.source || 'logbuch', feat.filename || feat.name);
        
        let badgeBg = "#eee", badgeColor = "#555";
        if (feat.status === "COMPLETED") { badgeBg = "#e8f5e9"; badgeColor = "#2e7d32"; }
        else if (feat.status === "ACTIVE") { badgeBg = "#e3f2fd"; badgeColor = "#1565c0"; }

        const displayTitle = (typeof currentLanguage !== 'undefined' && currentLanguage === 'de') ? feat.title_de : feat.title_en;

        featDiv.innerHTML = `
            <div style="background: ${badgeBg}; color: ${badgeColor}; padding: 4px 8px; border-radius: 4px; font-size: 0.7em; font-weight: bold; min-width: 85px; text-align: center;">
                ${feat.status}
            </div>
            <div style="flex: 1;">
                <div style="font-weight: 600; color: #111; font-size: 0.95em;">${displayTitle || feat.name}</div>
            </div>
        `;
        container.appendChild(featDiv);
    });
}

function toggleFeatureStatus() {
    const modal = document.getElementById('feature-status-modal');
    if (!modal) return;
    if (modal.style.display === 'none') {
        modal.style.display = 'block';
        loadFeatureStatus();
    } else {
        modal.style.display = 'none';
    }
}

async function openLogbook(featureName, source = 'logbuch', filename = null) {
    const modal = document.getElementById('logbook-modal');
    const titleElement = document.getElementById('logbook-title');
    const contentElement = document.getElementById('logbook-content');

    if (titleElement) titleElement.innerText = `Logbuch: ${featureName}`;
    if (contentElement) contentElement.innerHTML = '<div class="spinner" style="margin: 20px auto;"></div>';
    if (modal) modal.style.display = 'block';

    try {
        const entryRef = source === 'root' ? (filename || featureName) : featureName;
        let markdown = await eel.get_logbook_entry(entryRef, source)();

        if (markdown.includes('<!-- lang-split -->')) {
            const parts = markdown.split('<!-- lang-split -->');
            markdown = (typeof currentLanguage !== 'undefined' && currentLanguage === 'de') ? parts[0] : (parts[1] || parts[0]);
        }

        let html = markdown.replace(/\n\n/g, '<br><br>');
        if (contentElement) contentElement.innerHTML = html;
    } catch (e) {
        if (contentElement) contentElement.innerHTML = `<p style="color: #f44;">Fehler.</p>`;
    }
}


