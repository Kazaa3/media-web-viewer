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

/**
 * Switch Logbook Views (v1.41.00)
 */
window.switchLogbookSubView = function(viewId) {
    if (typeof mwv_trace === 'function') mwv_trace('SUBTAB-LOG', viewId);
    
    document.querySelectorAll('.log-view').forEach(el => el.style.display = 'none');
    document.querySelectorAll('#logbook-fragment .tab-btn').forEach(el => el.classList.remove('active'));
    
    const target = document.getElementById('log-view-' + viewId);
    if (target) {
        target.style.display = 'flex';
        const btn = document.getElementById('log-subtab-' + viewId);
        if (btn) btn.classList.add('active');
    }

    // Initialize logic per view
    if (viewId === 'project') {
        if (typeof loadLogbuchTab === 'function') loadLogbuchTab();
    }
}

function getLogbookStatusIcon(status) {
    const normalized = (status || 'ACTIVE').toUpperCase();
    let color = 'var(--accent-color)';
    if (normalized === 'COMPLETED') color = '#2ecc71';
    if (normalized === 'PLAN') color = '#3498db';
    if (normalized === 'DOCS') color = '#9b59b6';
    if (normalized === 'BUG') color = '#e74c3c';
    
    return `<span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: ${color}; box-shadow: 0 0 8px ${color}88;"></span>`;
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

    // Extract categories for filter if it's the first render
    if (categoryFilter && categoryFilter.options.length <= 1) {
        const cats = [...new Set(entries.map(e => e.category || 'Misc'))].sort();
        cats.forEach(c => {
            const opt = document.createElement('option');
            opt.value = c;
            opt.textContent = c;
            categoryFilter.appendChild(opt);
        });
    }

    // Filter entries
    const filteredEntries = entries.filter(e => {
        const cat = e.category || 'Misc';
        if (selectedCategory !== 'Alle' && cat !== selectedCategory) return false;
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
        btn.className = 'nav-item';
        btn.style.cssText = 'padding: 10px 14px; border-radius: 8px; cursor: pointer; transition: all 0.2s; margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center; border: 1px solid transparent; background: transparent;';
        
        const nameWrap = document.createElement('div');
        nameWrap.style.cssText = 'display: flex; align-items: center; gap: 8px; flex: 1; overflow: hidden;';

        const statusIcon = getLogbookStatusIcon(entry.status || 'ACTIVE');
        const iconContainer = document.createElement('span');
        iconContainer.innerHTML = statusIcon;
        nameWrap.appendChild(iconContainer);

        const nameEl = document.createElement('span');
        nameEl.innerText = entry.name.replace('.md', '');
        nameEl.style.cssText = 'white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 700; font-size: 12px; color: var(--text-primary);';
        nameWrap.appendChild(nameEl);
        btn.appendChild(nameWrap);

        btn.onmouseover = () => { btn.style.background = 'rgba(255,255,255,0.05)'; };
        btn.onmouseout = () => { if (!btn.classList.contains('active')) btn.style.background = 'transparent'; };

        btn.onclick = () => {
            document.querySelectorAll('#logbuch-entry-sidebar-items .nav-item').forEach(i => {
                i.classList.remove('active');
                i.style.background = 'transparent';
                i.style.borderColor = 'transparent';
            });
            btn.classList.add('active');
            btn.style.background = 'rgba(255,255,255,0.1)';
            btn.style.borderColor = 'var(--accent-color)';
            loadLogbuchContent(entry.name, entry.filename);
        };
        fragment.appendChild(btn);
    });
    list.appendChild(fragment);
}

/**
 * Entry point for the Logbook tab initialization.
 */
async function loadLogbuchTab() {
    console.log("[Logbook] Initializing Project Logbook...");
    try {
        const entries = await eel.get_logbook_entries()();
        currentLogbuchEntries = entries || [];
        renderLogbuchList(currentLogbuchEntries);
        
        // Load first entry if none selected
        if (currentLogbuchEntries.length > 0) {
            const first = currentLogbuchEntries[0];
            loadLogbuchContent(first.name, first.filename);
        }
    } catch (e) {
        console.error("[loadLogbuchTab] Error:", e);
    }
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
        footer.style.cssText = 'margin-top: 60px; padding-top: 30px; border-top: 1px solid var(--border-color); display: flex; justify-content: flex-end;';
        const editBtn = document.createElement('button');
        editBtn.innerHTML = (typeof t === 'function' ? t('edit_btn_edit', 'Bearbeiten') : 'Bearbeiten');
        editBtn.className = 'tab-btn active';
        editBtn.style.cssText = 'padding: 10px 24px; background: var(--bg-secondary); color: var(--text-primary); border-radius: var(--radius-pill); cursor: pointer; font-weight: 700; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; border: 1px solid var(--border-color);';
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

/**
 * LOGBOOK EDITOR: Activation (v1.41.00)
 */
async function openLogbookEditor(name = null) {
    const modal = document.getElementById('logbuch-editor-modal');
    if (!modal) return;

    // Reset fields
    document.getElementById('logbuch-editor-name').value = name || '';
    document.getElementById('logbuch-editor-category').value = '';
    document.getElementById('logbuch-editor-date').value = new Date().toISOString().split('T')[0];
    document.getElementById('logbuch-editor-title-de').value = '';
    document.getElementById('logbuch-editor-content').value = '';

    if (name) {
        try {
            const raw = await eel.get_logbook_entry(name, 'project')();
            // Basic parsing of frontmatter-like content if found
            document.getElementById('logbuch-editor-content').value = raw;
            // Extract title or category if needed
        } catch (e) { console.error('Failed to load entry for editing:', e); }
    }

    modal.style.display = 'block';
}

function closeLogbookEditor() {
    const modal = document.getElementById('logbuch-editor-modal');
    if (modal) modal.style.display = 'none';
}

async function saveLogbookEntry() {
    const name = document.getElementById('logbuch-editor-name').value.trim();
    const content = document.getElementById('logbuch-editor-content').value;
    
    if (!name) {
        if (typeof showToast === 'function') showToast('Bitte einen Namen angeben!', 'error');
        return;
    }

    try {
        if (typeof showToast === 'function') showToast('Speichere Eintrag...', 'info');
        const res = await eel.save_logbook_entry(name, content)();
        
        if (res && res.status === 'success') {
            if (typeof showToast === 'function') showToast('Logbucheintrag gespeichert ✓', 'success');
            closeLogbookEditor();
            // Refresh list
            if (typeof loadLogbuchTab === 'function') loadLogbuchTab();
        } else {
            console.error('Save failed:', res);
            if (typeof showToast === 'function') showToast('Fehler beim Speichern', 'error');
        }
    } catch (e) {
        console.error('Save error:', e);
        if (typeof showToast === 'function') showToast('Systemfehler beim Speichern', 'error');
    }
}



// Created with MWV v1.46.00-MASTER
