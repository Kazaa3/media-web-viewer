/**
 * bibliothek.js
 * Unified Library management module.
 * Logic for Coverflow, Grid, Details, and Database views.
 */

// State
let allLibraryItems = [];
let coverflowItems = [];
let coverflowIndex = 0;
let libraryFilter = 'all';
// let librarySubFilter = 'all';
let libraryGenre = 'all';
let libraryYear = 'all';
let librarySearch = '';
// let librarySubTab = localStorage.getItem('mwv_library_sub_tab') || 'coverflow';

/**
 * Boots the library by fetching data from the DB.
 */
async function loadLibrary(retryCount = 0) {
    if (typeof appendUiTrace === 'function') appendUiTrace("[Library] Core initialization...");
    try {
        const library = await getLibrary();
        allLibraryItems = library.media || [];
        console.log(`[Library] Received ${allLibraryItems.length} items from backend.`);
        
        const mockEnabled = typeof eel !== 'undefined' ? await eel.get_mock_data_enabled() : false;
        if (!mockEnabled) {
            allLibraryItems = allLibraryItems.filter(i => !i.is_mock);
        }

        console.info(`[Library] Rendering ${allLibraryItems.length} items.`);
        renderLibrary();
    } catch (e) {
        console.error("[Library] Load error:", e);
        if (retryCount < 3) {
            setTimeout(() => loadLibrary(retryCount + 1), 1000);
        }
    }
}

/**
 * Triggers a full library refresh.
 */
async function refreshLibrary() {
    if (typeof showToast === 'function') showToast("Bibliothek wird aktualisiert...", "info");
    await loadLibrary();
}

/**
 * The main UI update entry point for the Library tab.
 */
async function renderLibrary() {
    const track = document.getElementById('coverflow-track');
    if (!track) return;

    // Local filter stage
    coverflowItems = allLibraryItems;
    console.debug(`[Library] renderLibrary starting with ${coverflowItems.length} items. Filter: ${libraryFilter}, Search: ${librarySearch}`);

    // Search
    if (librarySearch) {
        const q = librarySearch.toLowerCase();
        coverflowItems = coverflowItems.filter(i => 
            (i.name || '').toLowerCase().includes(q) || 
            (i.tags && i.tags.title && i.tags.title.toLowerCase().includes(q))
        );
    }

    // Genre
    if (libraryGenre !== 'all') {
        coverflowItems = coverflowItems.filter(i => i.tags && i.tags.genre === libraryGenre);
    }

    // Year
    if (libraryYear !== 'all') {
        coverflowItems = coverflowItems.filter(i => i.tags && i.tags.year === libraryYear);
    }

    // Main Category Filter
    if (libraryFilter !== 'all') {
        const allowedTypes = CATEGORY_MAP[libraryFilter] || [];
        coverflowItems = coverflowItems.filter(i => allowedTypes.includes(i.category));
    }

    // Update sub-category dropdown based on current set
    updateSubCategoryFilterOptions(coverflowItems);

    // Sub-Filter
    if (librarySubFilter !== 'all') {
        coverflowItems = coverflowItems.filter(i => (i.category || '').toLowerCase() === librarySubFilter.toLowerCase());
    }

    updateFilterOptions(coverflowItems);

    if (coverflowItems.length === 0) {
        const noMediaHtml = `<div style="padding: 100px; color: #999; text-align: center; width: 100%;" data-i18n="lib_no_media_warning">Keine Medien gefunden</div>`;
        if (typeof safeHtml === 'function') {
            safeHtml('coverflow-track', noMediaHtml);
            safeHtml('grid-container', noMediaHtml);
        } else {
            document.getElementById('coverflow-track').innerHTML = noMediaHtml;
            document.getElementById('grid-container').innerHTML = noMediaHtml;
        }
        return;
    }

    // Switch view rendering
    const views = {
        'coverflow': updateCoverflowDisplay,
        'grid': renderGridView,
        'details': renderDetailedView,
        'database': renderDatabaseView
    };
    if (views[librarySubTab]) views[librarySubTab]();
}

/**
 * Renders Grid View.
 */
function renderGridView() {
    const container = document.getElementById('grid-container');
    if (!container) return;

    const html = coverflowItems.map((item, idx) => {
        const artwork = `/cover/${encodeURIComponent(item.name)}`;
        const title = item.tags && item.tags.title ? item.tags.title : (item.name || 'Unknown');
        const artist = item.tags && item.tags.artist ? item.tags.artist : '';
        const displayTitle = artist ? `${artist} - ${title}` : title;

        let seriesInfo = '';
        if (item.category === 'Serie' && item.tags && item.tags.season !== undefined) {
            const s = String(item.tags.season).padStart(2, '0');
            const e = String(item.tags.episode || 0).padStart(2, '0');
            seriesInfo = `<span style="color: #e74c3c; font-weight: bold; margin-left: 5px;">S${s}E${e}</span>`;
        }

        return `
            <div class="grid-item" onclick="playMediaObject(coverflowItems[${idx}])" oncontextmenu="showContextMenu(event, coverflowItems[${idx}])">
                <div class="grid-cover" style="background-image: url('${artwork}')">
                    ${item.is_chrome_native ? `<div class="native-badge" title="Chrome Native support">DIRECT</div>` : ''}
                    ${typeof getCategoryBadgeHtml === 'function' ? getCategoryBadgeHtml(item) : ''}
                </div>
                <div class="grid-info">
                    <div class="grid-title" title="${item.name}">${displayTitle}${seriesInfo}</div>
                    <div class="grid-meta">${item.category || ''} | ${item.type || ''}</div>
                </div>
            </div>
        `;
    }).join('');

    if (typeof safeHtml === 'function') safeHtml('grid-container', html);
    else container.innerHTML = html;
}

/**
 * Renders database-style table view.
 */
function renderDatabaseView() {
    const body = document.getElementById('lib-db-table-body');
    const stats = document.getElementById('lib-db-stats');
    if (!body) return;

    if (stats) stats.innerText = `${coverflowItems.length} Objekte in der Ansicht`;

    const html = coverflowItems.map((item, idx) => {
        const artist = item.tags && item.tags.artist ? item.tags.artist : '-';
        return `
            <tr>
                <td style="color: #999;">${idx + 1}</td>
                <td style="font-family: monospace; font-size: 0.85em; color: #2196F3;">${item.id || '---'}</td>
                <td><span class="badge-${(item.type || 'unknown').toLowerCase()}">${item.type || '---'}</span></td>
                <td>${item.category || '---'}</td>
                <td style="font-weight: 500;">${item.name || '---'}</td>
                <td>${artist}</td>
                <td style="font-size: 0.8em; color: #666; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${item.path}">${item.path}</td>
                <td oncontextmenu="showContextMenu(event, coverflowItems[${idx}])">
                    <button class="icon-btn" onclick="playMediaObject(coverflowItems[${idx}])">▶️</button>
                    <button class="icon-btn" onclick="openEditFormByName('${item.name.replace(/'/g, "\\'")}')">Edit</button>
                </td>
            </tr>
        `;
    }).join('');

    if (typeof safeHtml === 'function') safeHtml('lib-db-table-body', html || '<tr><td colspan="8">Keine Einträge</td></tr>');
    else body.innerHTML = html || '<tr><td colspan="8">Keine Einträge</td></tr>';
}

/**
 * Filter Management.
 */
function setLibraryFilter(cat) {
    libraryFilter = cat;
    librarySubFilter = 'all';
    coverflowIndex = 0;
    document.querySelectorAll('#coverflow-library-panel .filter-chip').forEach(btn => {
        const btnCat = btn.getAttribute('data-cat');
        btn.classList.toggle('active', btnCat === cat);
    });
    renderLibrary();
}

function handleLibrarySearch(val) {
    librarySearch = val;
    renderLibrary();
}

function setLibraryGenreFilter(val) {
    libraryGenre = val;
    renderLibrary();
}

function setLibraryYearFilter(val) {
    libraryYear = val;
    renderLibrary();
}

function setLibrarySubFilter(val) {
    librarySubFilter = val;
    renderLibrary();
}

function updateFilterOptions(media) {
    const genreSelect = document.getElementById('library-genre-filter');
    const yearSelect = document.getElementById('library-year-filter');
    if (!genreSelect || !yearSelect) return;

    const genres = new Set();
    const years = new Set();

    media.forEach(item => {
        if (item.tags) {
            if (item.tags.genre) genres.add(item.tags.genre);
            if (item.tags.year) years.add(item.tags.year);
        }
    });

    let genreHtml = '<option value="all">Alle Genres</option>';
    [...genres].sort().forEach(g => {
        genreHtml += `<option value="${g}" ${libraryGenre === g ? 'selected' : ''}>${g}</option>`;
    });
    genreSelect.innerHTML = genreHtml;

    let yearHtml = '<option value="all">Alle Jahre</option>';
    [...years].sort((a, b) => b - a).forEach(y => {
        yearHtml += `<option value="${y}" ${libraryYear === y ? 'selected' : ''}>${y}</option>`;
    });
    yearSelect.innerHTML = yearHtml;
}

function updateSubCategoryFilterOptions(media) {
    const subFilterSelect = document.getElementById('library-subcategory-filter');
    if (!subFilterSelect) return;

    const currentVal = subFilterSelect.value;
    const categories = [...new Set(media.map(i => i.category))].filter(Boolean).sort();

    let optionsHtml = `<option value="all">Alle Unterkategorien</option>`;
    categories.forEach(cat => {
        optionsHtml += `<option value="${cat.toLowerCase()}">${cat}</option>`;
    });

    subFilterSelect.innerHTML = optionsHtml;
    // Restore or reset selection
    if (categories.map(c => c.toLowerCase()).includes(currentVal.toLowerCase())) {
        subFilterSelect.value = currentVal;
    } else {
        subFilterSelect.value = 'all';
        librarySubFilter = 'all';
    }
}

/**
 * Switching library display modes (Coverflow, Grid, etc.).
 */
function switchLibrarySubTab(tab) {
    librarySubTab = tab;
    localStorage.setItem('mwv_library_sub_tab', tab);
    
    // UI update
    document.querySelectorAll('.options-subtab').forEach(btn => {
        btn.classList.toggle('active', btn.id === `lib-tab-btn-${tab}`);
    });
    
    document.querySelectorAll('.library-sub-content').forEach(pane => {
        pane.style.display = (pane.id === `lib-view-${tab}`) ? 'block' : 'none';
    });

    renderLibrary();
}

/**
 * Coverflow Logic (restored from legacy).
 */
function updateCoverflowDisplay() {
    const track = document.getElementById('coverflow-track');
    if (!track) return;

    const html = coverflowItems.map((item, idx) => {
        const artwork = `/cover/${encodeURIComponent(item.name)}`;
        const title = item.tags && item.tags.title ? item.tags.title : (item.name || 'Unknown');
        const artist = item.tags && item.tags.artist ? item.tags.artist : '-';
        
        let classes = 'coverflow-item';
        if (idx === coverflowIndex) classes += ' active';
        else if (idx < coverflowIndex) classes += ' left';
        else classes += ' right';

        return `
            <div class="${classes}" style="background-image: url('${artwork}')" 
                 onclick="selectCoverflowItem(${idx})" oncontextmenu="showContextMenu(event, coverflowItems[${idx}])">
                <div class="info">
                    <div class="title">${title}</div>
                    <div class="meta">${artist} | ${item.category}</div>
                </div>
            </div>
        `;
    }).join('');

    if (typeof safeHtml === 'function') safeHtml('coverflow-track', html);
    else track.innerHTML = html;

    const activeEl = track.querySelector('.coverflow-item.active');
    if (activeEl) {
        const offset = activeEl.offsetLeft + (activeEl.offsetWidth / 2);
        const containerHalf = track.parentElement.offsetWidth / 2;
        track.style.transform = `translateX(${containerHalf - offset}px)`;
    }
}

function selectCoverflowItem(idx) {
    if (idx === coverflowIndex) {
        if (typeof playMediaObject === 'function') playMediaObject(coverflowItems[idx]);
    } else {
        coverflowIndex = idx;
        updateCoverflowDisplay();
    }
}

// Restore legacy Detail View Rendering
function renderDetailedView() {
    const header = document.getElementById('details-table-header');
    const body = document.getElementById('details-table-body');
    if (!header || !body) return;

    const cols = ['Name', 'Category', 'Type', 'Path'];
    header.innerHTML = cols.map(c => `<th>${c}</th>`).join('');

    const html = coverflowItems.map((item, idx) => `
        <tr onclick="playMediaObject(coverflowItems[${idx}])">
            <td>${item.name || '---'}</td>
            <td>${item.category || '---'}</td>
            <td>${item.type || '---'}</td>
            <td title="${item.path}">${item.path}</td>
        </tr>
    `).join('');

    body.innerHTML = html;
}

/**
 * Initiates Library Scan.
 */
async function scan(targetDir = null, clearDb = true) {
    if (typeof scanMedia === 'function') {
        const res = await scanMedia(targetDir, clearDb);
        if (res && res.status === 'ok') {
            await refreshLibrary();
        }
    }
}
