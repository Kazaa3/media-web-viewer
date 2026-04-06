// --- Hoisted Global State (v1.35.68 Fix) ---
// Global state export for cross-module HUD and queue consistency (v1.35.68)
window.__mwv_all_library_items = [];
let libraryStateLoaded = false;
let coverflowItems = [];
let coverflowIndex = 0;
let libraryFilter = 'all';
// let librarySubFilter = 'all';
let libraryGenre = 'all';
let libraryYear = 'all';
let librarySearch = '';
let hasAutoScanned = false; // Prevent infinite scan loops
let librarySubTab = localStorage.getItem('mwv_library_sub_tab') || 'coverflow';

window.allLibraryItems = allLibraryItems;
console.log(">>> [Eel-Status] Bridge found:", (typeof eel !== 'undefined'));
console.log(">>> [JS-LOAD] bibliothek.js initialized.");
if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'STAGE-INIT');

/**
 * Boots the library by fetching data from the DB.
 */
async function loadLibrary(retryCount = 0, forceRaw = false) {
        window.__mwv_lib_loaded = true;
    if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'STAGE-LOAD-START');
    console.log(`[DATA-LIB] STAGE-LOAD-START: loadLibrary(forceRaw=${forceRaw}) called.`);
    if (typeof updateSyncAnchor === 'function') updateSyncAnchor('...', '...'); 
    if (typeof appendUiTrace === 'function') appendUiTrace(`[Library] Phase 1: Requesting from backend...`, "DB-INFO");
    try {
        // v1.35.68: Synchronize Category Master before requesting library
        if (typeof syncCategoryMaster === 'function') await syncCategoryMaster();

        // --- STAGE 1-3 AUDIT HANDSHAKE (v1.35.96) ---
        const auditStage = window.__mwv_audit_stage || 0;
        const library = await getLibrary(auditStage); 
        
        const incomingCount = (library.media || []).length;
        const totalDbCount = library.db_count || incomingCount;
        const audit = library.audit || {};
        const fsSize = (audit.fs || {}).size || 0;
        
        console.warn(`[BD-AUDIT] Handshake Received. Stage: ${audit.stage || 'N/A'}. Count: ${incomingCount}/${totalDbCount}. PID: ${audit.pid || '?'}`);
        if (audit.path) console.info(`[BD-AUDIT] Backend Path: ${audit.path} | FS Size: ${fsSize}`);
        
        window.__mwv_last_db_count = totalDbCount;
        window.__mwv_debug_library = library; // Global for manual trace
        
        if (typeof updateSyncAnchor === 'function') updateSyncAnchor(totalDbCount, incomingCount, fsSize);
        if (typeof appendUiTrace === 'function') appendUiTrace(`[Sync] Stage ${audit.stage || 0} complete. Received ${incomingCount} items.`, "SUCCESS");
        
        window.__mwv_all_library_items = library.media || [];
        console.warn(`[FE-AUDIT] STAGE 4 (HYDRATION): Memory filled with ${window.__mwv_all_library_items.length} items.`);
        
        // --- V1.35.43 Recovery: Modular Sync Handshake ---
        if (typeof RecoveryManager !== 'undefined') {
            RecoveryManager.checkAndHydrate();
        } else {
            // Minimal fallback if manager is missing
            const realItems = allLibraryItems.filter(i => !i.is_mock);
            if (realItems.length === 0) {
                allLibraryItems = [{
                    id: 'fallback-emergency',
                    name: '[ERROR] RecoveryManager Missing',
                    category: 'Audio',
                    is_mock: true
                }];
            }
        }
        
        // Auto-scan only if not done yet
        if (!hasAutoScanned && allLibraryItems.filter(i => !i.is_mock).length === 0) {
            hasAutoScanned = true;
            if (typeof scan === 'function') scan('./media', true);
        }

        // --- Phase 2: Metadata & UI Refresh ---
        if (typeof mwv_trace_render === 'function') mwv_trace_render('DATA-LIB', 'STAGE-BROADCAST', { count: allLibraryItems.length });
        
        // Ensure main UI rendering
        if (typeof renderLibrary === 'function') renderLibrary();
        
        // Ensure Queue synchronization (Playback Chain Start)
        if (typeof syncQueueWithLibrary === 'function') {
            syncQueueWithLibrary();
            
            // v1.35.68 Detection: Trigger Reset if we still have 0 after sync
            if (typeof currentPlaylist !== 'undefined' && currentPlaylist.length === 0 && allLibraryItems.length > 0) {
                console.warn("[DATA-LIB] EMPTY QUEUE DETECTED. Forcing Filter Reset...");
                if (typeof resetAllFilters === 'function') resetAllFilters();
            }
        }

        document.dispatchEvent(new CustomEvent('mwv_library_ready', { detail: { count: allLibraryItems.length } }));

    } catch (e) {
        console.error("[DATA-LIB] CRITICAL LOAD ERROR:", e);
        if (typeof updateSyncAnchor === 'function') updateSyncAnchor('ERR', '!');
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
    const renderStart = performance.now();

    if (typeof mwv_trace_render === 'function') mwv_trace_render('LIBRARY-UI', 'RENDER-START', { count: allLibraryItems.length });
    
    const track = document.getElementById('coverflow-track');
    if (!track) {
        if (typeof log_js_error === 'function') log_js_error(new Error("#coverflow-track missing"), 'LIBRARY-RENDER');
        return;
    }

    // --- PHASE 1: FILTERING (v1.35.68 Hardened) ---
    console.warn(`[FE-AUDIT] Starting Render for ${allLibraryItems.length} items. MainCat: ${libraryFilter}, SubCat: ${librarySubFilter}, Search: "${librarySearch}"`);
    
    // Start with all items (using global state export v1.35.68)
    let projectedItems = [...(window.__mwv_all_library_items || [])];
    
    // [FE-FORENSIC] Aggressive Audit (v1.35.68)
    const initialRaw = projectedItems.length;
    if (initialRaw === 0) {
        console.error("[FE-FORENSIC] Library Memory is EMPTY. Stage Load Fault?");
    }

    // 1. Hydration Mode Filter (Mock/Real/Both) - v1.35.68
    const hmode = window.__mwv_hydration_mode || localStorage.getItem('mwv_hydration_mode') || 'both';
    projectedItems = projectedItems.filter(i => {
        if (hmode === 'mock') return i.is_mock === true;
        if (hmode === 'real') return !i.is_mock;
        return true; // 'both'
    });

    // 2. HIDB (Diagnostic Hide) - Should usually be OFF
    if (window.__mwv_hide_db) {
        projectedItems = projectedItems.filter(i => i.is_mock);
        console.log(`[FE-AUDIT] HIDB active - showing only mock items.`);
    }

    // 2. Main Category Filter
    if (libraryFilter !== 'all') {
        const allowedTypes = (typeof CATEGORY_MAP !== 'undefined' ? CATEGORY_MAP[libraryFilter] : []) || [];
        projectedItems = projectedItems.filter(i => {
            if (i.is_mock) return true; // Keep mocks during diagnostics
            const cat = String(i.category || 'all').toLowerCase();
            // Special handling for images
            if (libraryFilter === 'pictures' && (cat === 'multimedia' || cat === 'bilder' || cat === 'pictures')) return true;
            return allowedTypes.some(at => at.toLowerCase() === cat);
        });
    }

    // 3. Sub-Category Filter
    if (typeof librarySubFilter !== 'undefined' && librarySubFilter !== 'all') {
        projectedItems = projectedItems.filter(i => i.is_mock || (i.category || '').toLowerCase() === librarySubFilter.toLowerCase());
    }

    // 4. Genre & Year
    if (libraryGenre !== 'all') {
        projectedItems = projectedItems.filter(i => i.is_mock || (i.tags && i.tags.genre === libraryGenre));
    }
    if (libraryYear !== 'all') {
        projectedItems = projectedItems.filter(i => i.is_mock || (i.tags && i.tags.year === libraryYear));
    }

    // 5. Search (Final Pass)
    if (librarySearch) {
        const q = librarySearch.toLowerCase();
        projectedItems = projectedItems.filter(i => 
            i.is_mock || 
            (i.name || '').toLowerCase().includes(q) || 
            (i.tags && i.tags.title && i.tags.title.toLowerCase().includes(q)) ||
            (i.path || '').toLowerCase().includes(q)
        );
    }

    coverflowItems = projectedItems;
    console.log(`[FE-AUDIT] Final Projection: ${coverflowItems.length} items.`);

    if (typeof mwv_trace_render === 'function') {
        mwv_trace_render('LIBRARY-UI', 'STAGE-PROJECTED', { 
            raw: allLibraryItems.length, 
            projected: coverflowItems.length,
            filter: libraryFilter,
            sub: librarySubFilter
        });
    }

    if (coverflowItems.length === 0) {
        let noMediaHtml = "";
        
        if (allLibraryItems.length === 0) {
            // --- TIER A: TOTAL BLACK HOLE (v1.37.28) ---
            noMediaHtml = `
                <div style="padding: 60px; color: var(--text-primary); text-align: center; width: 100%; max-width: 800px; margin: 40px auto; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.4);">
                    <div style="font-size: 32px; margin-bottom: 20px;">🛡️ Hydration Guard</div>
                    <div style="font-size: 14px; font-weight: 700; color: #ff3366; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px;">Forensic Error: empty_index_detected</div>
                    <p style="color: var(--text-secondary); opacity: 0.8; margin-bottom: 30px; line-height: 1.6;">
                        Deine Medien-Datenbank ist aktuell vollständig leer. <br>
                        Verwende die folgenden taktischen Werkzeuge, um dein System zu rehydrieren.
                    </p>
                    
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px;">
                        <button onclick="if(window.triggerMasterScan) window.triggerMasterScan()" style="padding: 15px; background: #3498db; color: white; border: none; border-radius: 10px; font-weight: 900; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                            <span style="font-size: 18px;">📂</span>
                            <span style="font-size: 11px;">DIRECT SCAN</span>
                        </button>
                        <button onclick="if(window.triggerMasterSync) window.triggerMasterSync()" style="padding: 15px; background: #2ecc71; color: white; border: none; border-radius: 10px; font-weight: 900; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                            <span style="font-size: 18px;">🔄</span>
                            <span style="font-size: 11px;">ATOMIC SYNC</span>
                        </button>
                        <button onclick="if(window.triggerNuclearRecovery) window.triggerNuclearRecovery()" style="padding: 15px; background: #e74c3c; color: white; border: none; border-radius: 10px; font-weight: 900; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 5px;">
                            <span style="font-size: 18px;">☢️</span>
                            <span style="font-size: 11px;">NUCLEAR RECOVERY</span>
                        </button>
                    </div>

                    <div style="font-size: 10px; color: var(--text-secondary); opacity: 0.5; font-family: 'JetBrains Mono', monospace; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 15px;">
                        MWV_WORKSTATION_VERSION_1.37.28 | STATUS: STANDBY
                    </div>
                </div>
            `;
            if (typeof sentinelPulse === 'function') sentinelPulse('ERROR', 'Total Black Hole Detected: Library is empty.');
        } else {
            // --- TIER B: FILTERED BLACK HOLE (v1.37.28) ---
            const dbCount = allLibraryItems.filter(i => !i.is_mock).length;
            noMediaHtml = `
                <div style="padding: 60px; color: var(--text-primary); text-align: center; width: 100%; max-width: 800px; margin: 40px auto; background: rgba(52, 152, 219, 0.05); border: 1px solid rgba(52, 152, 219, 0.2); border-radius: 16px;">
                    <div style="font-size: 28px; margin-bottom: 20px;">🔍 Filter-Blockade erkannt</div>
                    <div style="font-weight: 800; color: #3498db; font-size: 18px; margin-bottom: 10px;">${dbCount} Medien in der DB, aber 0 in der Anzeige!</div>
                    <p style="color: var(--text-secondary); margin-bottom: 25px; line-height: 1.6;">
                        Deine Suche, Kategorie-Filter oder der HIDB-Status verhindern die Anzeige deiner Medien.
                    </p>
                    <button onclick="resetAllFilters()" style="padding: 15px 40px; background: #3498db; color: white; border: none; border-radius: 10px; font-weight: 900; cursor: pointer; font-size: 14px; letter-spacing: 1px;">JETZT FILTER ZURÜCKSETZEN</button>
                    
                    <div style="margin-top: 25px; display: flex; justify-content: center; gap: 15px;">
                        <div style="background: rgba(0,0,0,0.2); padding: 8px 15px; border-radius: 6px; font-size: 11px; font-family: 'JetBrains Mono', monospace;">
                            <span style="opacity: 0.5;">DB_TOTAL:</span> ${window.__mwv_last_db_count}
                        </div>
                        <div style="background: rgba(0,0,0,0.2); padding: 8px 15px; border-radius: 6px; font-size: 11px; font-family: 'JetBrains Mono', monospace;">
                            <span style="opacity: 0.5;">VIEWPORT:</span> 0
                        </div>
                    </div>
                </div>
            `;
            if (typeof sentinelPulse === 'function') sentinelPulse('WARNING', `Filtered Black Hole: ${dbCount} hidden items.`);
        }
        
        if (typeof safeHtml === 'function') {
            safeHtml('coverflow-track', noMediaHtml);
            safeHtml('grid-container', noMediaHtml);
        } else {
            const t1 = document.getElementById('coverflow-track');
            const t2 = document.getElementById('grid-container');
            if (t1) t1.innerHTML = noMediaHtml;
            if (t2) t2.innerHTML = noMediaHtml;
        }
        window.__mwv_last_render_ms = performance.now() - renderStart;
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
    
    // Update the sync anchor with the final rendered count
    if (typeof updateSyncAnchor === 'function') updateSyncAnchor(undefined, coverflowItems.length);
    
    window.__mwv_last_render_ms = performance.now() - renderStart;
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
            if (typeFilter === 'disk_images') return ext === 'iso' || item.category === 'disk_images';
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
/**
 * Reset All Filters (v1.35.68 Recovery)
 * Clears all local storage and UI filter states to show all 541+ items.
 */
function resetAllFilters() {
    console.warn("[RECOVERY] Resetting all frontend filters to clear the 'Black Hole'...");
    
    // Clear State
    libraryFilter = 'all';
    libraryGenre = 'all';
    libraryYear = 'all';
    librarySearch = '';
    if (typeof librarySubFilter !== 'undefined') librarySubFilter = 'all';
    
    // Reset UI Elements
    safeValue('queue-type-filter', 'all');
    safeValue('library-search-input', '');
    safeValue('genre-filter', 'all');
    safeValue('year-filter', 'all');
    
    // Clear Persistent Storage (if used)
    localStorage.removeItem('mwv_library_filter');
    localStorage.removeItem('mwv_library_genre');
    localStorage.removeItem('mwv_library_search');
    
    if (typeof showStatusNotification === 'function') {
        showStatusNotification('Alle Filter zurückgesetzt', 'success');
    }
    
    // Re-render
    renderLibrary();
}

// Expose to window
window.resetAllFilters = resetAllFilters;

/**
 * Specialized View Initializers (v1.35.68 Standard)
 * These ensure categorized data flows correctly when a fragment is loaded.
 */
function initFilmsView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-FILMS');
    libraryFilter = 'film'; 
    renderLibrary(); 
}

function initSeriesView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-SERIES');
    libraryFilter = 'serie'; 
    renderLibrary(); 
}

function initAlbumsView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-ALBUMS');
    libraryFilter = 'album'; 
    renderLibrary(); 
}

function initAudiobooksView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-AUDIOBOOKS');
    libraryFilter = 'audiobook'; 
    renderLibrary(); 
}

function initCinemaView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-CINEMA');
    libraryFilter = 'video'; 
    renderLibrary(); 
}

function initPicturesView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-PICTURES');
    libraryFilter = 'pictures'; 
    renderLibrary(); 
}

function initDocumentsView() { 
    if (typeof mwv_trace === 'function') mwv_trace('NAV-LIB', 'INIT-DOCUMENTS');
    libraryFilter = 'documents'; 
    renderLibrary(); 
}

// Global Exports for fragment callbacks
window.initFilmsView = initFilmsView;
window.initSeriesView = initSeriesView;
window.initAlbumsView = initAlbumsView;
window.initAudiobooksView = initAudiobooksView;
window.initCinemaView = initCinemaView;
window.initPicturesView = initPicturesView;
window.initDocumentsView = initDocumentsView;
