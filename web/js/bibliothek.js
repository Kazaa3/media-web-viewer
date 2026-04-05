console.log(">>> [JS-LOAD] bibliothek.js initialized.");
window.allLibraryItems = allLibraryItems;
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
let hasAutoScanned = false; // Prevent infinite scan loops
let librarySubTab = localStorage.getItem('mwv_library_sub_tab') || 'coverflow';

/**
 * Boots the library by fetching data from the DB.
 */
async function loadLibrary(retryCount = 0) {
        window.__mwv_lib_loaded = true;
    if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'STAGE-LOAD-START');
    console.log('[DATA-LIB] STAGE-LOAD-START: loadLibrary() called.');
    if (typeof appendUiTrace === 'function') appendUiTrace(`[Library] Phase 1: Requesting from backend...`, "DB-INFO");
    try {
        const library = await getLibrary();
        console.warn(`>>> [Handshake] Backend returned media array (type: ${typeof library.media}).`);
        allLibraryItems = library.media || [];
        
        if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'BACKEND-RAW', { count: allLibraryItems.length });
        
        // --- V1.35 Recovery: Force Mock Item if Empty ---
        const realItems = allLibraryItems.filter(i => !i.is_mock);
        if (realItems.length === 0) {
            const mockFallback = {
                id: 'mock-item-recovery',
                name: '[MOCK] System Test Audio',
                artist: 'Media Viewer Core',
                album: 'Recovery Module',
                path: 'media/test_mock_item.mp3',
                category: 'Audio',
                is_mock: true,
                tags: { title: 'Recovery Success', artist: 'Antigravity Diagnostic' }
            };
            allLibraryItems = [mockFallback];
            if (typeof appendUiTrace === 'function') appendUiTrace("[Recovery] Injected diagnostic mock item.", "WARN");
            if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'STAGE-MOCK', { item: mockFallback.name });
            // Auto-scan only if not done yet
            if (!hasAutoScanned) {
                hasAutoScanned = true;
                if (typeof scan === 'function') scan('./media', true);
            }
        }

        // --- Phase 2: Metadata & UI Refresh ---
        if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'STAGE-BROADCAST', { count: allLibraryItems.length });
        
        // Ensure main UI rendering
        if (typeof renderLibrary === 'function') renderLibrary();
        
        // Ensure Queue synchronization (Playback Chain Start)
        if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();

        document.dispatchEvent(new CustomEvent('mwv_library_ready', { detail: { count: allLibraryItems.length } }));

    } catch (e) {
        if (typeof log_js_error === 'function') log_js_error(e, 'DATA-LIB-LOAD');
        if (retryCount < 3) {
            setTimeout(() => loadLibrary(retryCount + 1), 2000);
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
        // Instrumentation: Log item counts
        if (typeof mwv_trace_render === 'function') {
            mwv_trace_render('LIBRARY', 'RENDER', {
                raw: allLibraryItems.length,
                filtered: coverflowItems.length
            });
        }
    if (typeof mwv_trace_render === 'function') mwv_trace_render('LIBRARY-UI', 'RENDER-START', { count: allLibraryItems.length });
    
    const track = document.getElementById('coverflow-track');
    if (!track) {
        if (typeof log_js_error === 'function') log_js_error(new Error("#coverflow-track missing"), 'LIBRARY-RENDER');
        return;
    }

    // Local filter stage
    coverflowItems = allLibraryItems;
    console.log(`[Library] Rendering ${coverflowItems.length} items (Filter: ${libraryFilter})...`);
    mwv_trace('DOM-UI', 'RENDER-LIBRARY', { count: coverflowItems.length, filter: libraryFilter, search: librarySearch });

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

    // --- Recovery Bypass: Unconditionally include Mock items (v1.35) ---
    if (allLibraryItems.some(i => i.is_mock)) {
        coverflowItems = allLibraryItems.filter(i => 
            i.is_mock || 
            ( (librarySearch ? (i.name||'').toLowerCase().includes(librarySearch.toLowerCase()) : true) &&
              (libraryGenre !== 'all' ? (i.tags && i.tags.genre === libraryGenre) : true) )
        );
    }

    if (typeof mwv_trace_render === 'function') mwv_trace_render('LIBRARY-UI', 'STAGE-PROJECTED', { raw: allLibraryItems.length, projected: coverflowItems.length });
    
    if (coverflowItems.length === 0) {
        const noMediaHtml = `<div style="padding: 100px; color: #999; text-align: center; width: 100%;" data-i18n="lib_no_media_warning">Keine Medien gefunden</div>`;
        if (typeof safeHtml === 'function') {
            safeHtml('coverflow-track', noMediaHtml);
            safeHtml('grid-container', noMediaHtml);
        } else {
            const t1 = document.getElementById('coverflow-track');
            const t2 = document.getElementById('grid-container');
            if (t1) t1.innerHTML = noMediaHtml;
            if (t2) t2.innerHTML = noMediaHtml;
        }
        return;
    }

    // Switch view rendering
    const currentView = librarySubTab || 'coverflow';
    const views = {
        'coverflow': updateCoverflowDisplay,
        'grid': renderGridView,
        'details': renderDetailedView,
        'database': renderDatabaseView
    };
    if (views[currentView]) views[currentView]();
}

/**
 * Renders Grid View.
 */
function renderGridView() {
    const container = document.getElementById('grid-container');
    if (!container) return;

    container.innerHTML = '';
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

    if (stats) stats.innerText = `${coverflowItems.length} Medien in der Ansicht`;

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
 * Switching library domains (Visual vs Browse vs Inventory).
 */
function switchLibraryDomain(domain) {
    if (typeof mwv_trace === 'function') {
        mwv_trace('NAV-LIB', 'SWITCH-DOMAIN', { domain });
    }
    console.log(`[Library] Switching domain to: ${domain}`);
    
    document.querySelectorAll('.lib-domain-content').forEach(el => {
        el.style.display = 'none';
        el.classList.remove('active');
    });

    const target = document.getElementById(`lib-domain-${domain}`);
    if (target) {
        target.style.display = 'flex';
        target.classList.add('active');
    }

    // Update buttons
    document.querySelectorAll('.sub-nav-bar .sub-tab-btn').forEach(btn => {
        btn.classList.toggle('active', btn.id === `lib-domain-btn-${domain}`);
    });

    // Lazy load fragments if needed
    if (domain === 'browse') {
        if (typeof FragmentLoader !== 'undefined') {
            FragmentLoader.load('lib-browse-mount-point', 'fragments/filesystem_browser.html', () => {
                if (typeof fbNavigate === 'function') fbNavigate(typeof fbCurrentPath !== 'undefined' ? fbCurrentPath : '/');
            });
        }
    } else if (domain === 'inventory') {
        if (typeof FragmentLoader !== 'undefined') {
            FragmentLoader.load('lib-inventory-mount-point', 'fragments/item_inventory.html', () => {
                if (typeof loadEditItems === 'function') loadEditItems();
            });
        }
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
 * Coverflow Logic (Modern 3D v1.34).
 */
function updateCoverflowDisplay() {
    if (typeof window.initCoverflow === 'function') {
        window.initCoverflow(coverflowItems);
    } else {
        console.warn("[Library] Coverflow controller not ready.");
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

    const typeFilter = document.getElementById('gallery-type-filter')?.value || 'all';
    
    // Sort and Filter Logic
    let filteredItems = [...coverflowItems];
    
    if (typeFilter !== 'all') {
        filteredItems = filteredItems.filter(item => {
            const ext = (item.path || '').split('.').pop().toLowerCase();
            if (typeFilter === 'audio') return ['mp3', 'flac', 'm4a', 'wav', 'ogg'].includes(ext);
            if (typeFilter === 'video') return ['mp4', 'mkv', 'avi', 'mov', 'webm'].includes(ext);
            if (typeFilter === 'iso') return ext === 'iso' || item.category === 'ISO';
            return true;
        });
    }

    const cols = ['Name', 'Category', 'Type', 'Path'];
    header.innerHTML = cols.map(c => `<th>${c}</th>`).join('');

    const html = filteredItems.map((item, idx) => `
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
