// --- Hoisted Global State (v1.41.00 Fix) ---
// Global state export for cross-module HUD and queue consistency (v1.41.00)
window.__mwv_all_library_items = [];
// Alias for internal module consistency (v1.41.00)
Object.defineProperty(window, 'allLibraryItems', {
    get: () => window.__mwv_all_library_items,
    set: (v) => { window.__mwv_all_library_items = v; }
});
let libraryStateLoaded = false;
let coverflowItems = [];
let coverflowIndex = 0;
let libraryFilter = 'all';
let librarySubFilter = 'all';
let libraryGenre = 'all';
let libraryYear = 'all';
let librarySearch = '';
let hasAutoScanned = false; // Prevent infinite scan loops
let librarySubTab = localStorage.getItem('mwv_library_sub_tab') || 'coverflow';

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
        // v1.41.00: Synchronize Category Master before requesting library
        // --- STAGE 1-3 AUDIT HANDSHAKE (v1.35.96) ---
        const auditStage = window.__mwv_audit_stage || 0;
        let library;
        
        try {
            // [v1.41.00-B] Stalling Protection: syncCategoryMaster with 2.5s timeout
            const syncTimeout = new Promise(resolve => setTimeout(() => resolve('timeout'), 2500));
            if (typeof syncCategoryMaster === 'function') {
                const syncResult = await Promise.race([syncCategoryMaster(), syncTimeout]);
                if (syncResult === 'timeout') console.warn("[DATA-LIB] syncCategoryMaster STALLED. Proceeding with hydration...");
            }

            const activeBranch = window.GLOBAL_CONFIG?.active_branch || null;
            library = await getLibrary(auditStage, activeBranch); 
        } catch (e) {
            console.error("[FE-BRIDGE-FAULT] CRITICAL: Calling getLibrary failed!", e);
            if (typeof appendUiTrace === 'function') appendUiTrace(`[Library] Bridge Fault: ${e.message}`, "ERROR");
            return;
        }
        
        const incomingCount = (library.media || []).length;
        const totalDbCount = library.db_count || incomingCount;
        const audit = library.audit || {};
        const fsSize = (audit.fs || {}).size || 0;
        
        // [v1.46.026] Forensic Handshake Audit (JS)
        const incomingStats = (library.media || []).reduce((acc, item) => {
            const cat = (item.category || item.type || 'unknown').toLowerCase();
            acc[cat] = (acc[cat] || 0) + 1;
            return acc;
        }, {});
        console.warn(`>>> [FE-AUDIT] Handshake Received. Stage: ${audit.stage || 'N/A'}. Stats:`, incomingStats);
        console.info(`[BD-AUDIT] Raw Payload: ${incomingCount} items (DB: {totalDbCount}). PID: ${audit.pid || '?'}`);
        
        // [v1.46.026] Extraction of Forensic DB Health
        const dbInfo = audit.db || {};
        window.__mwv_last_db_health = dbInfo.health || 'unknown';
        window.__mwv_last_db_size = dbInfo.size || 0;
        
        if (audit.path) console.info(`[BD-AUDIT] Backend Path: ${audit.path} | Health: ${window.__mwv_last_db_health}`);
        
        window.__mwv_last_db_count = totalDbCount;
        window.__mwv_debug_library = library; // Global for manual trace
        
        if (typeof updateSyncAnchor === 'function') updateSyncAnchor(totalDbCount, incomingCount, fsSize);
        if (typeof appendUiTrace === 'function') appendUiTrace(`[Sync] Stage ${audit.stage || 0} complete. Received ${incomingCount} items.`, "SUCCESS");
        
        // [v1.46.026] Forensic HUD Pulse
        if (typeof refreshForensicLeds === 'function') refreshForensicLeds();
        
        window.__mwv_all_library_items = library.media || [];
        console.warn(`[FE-AUDIT] STAGE 4 (HYDRATION): Memory filled with ${window.__mwv_all_library_items.length} items.`);
        if (window.__mwv_all_library_items.length > 0) {
            console.warn(`[FE-AUDIT] Sample Item:`, window.__mwv_all_library_items[0]);
        }
        
        // --- V1.35.43 Recovery: Modular Sync Handshake ---
        if (typeof RecoveryManager !== 'undefined') {
            RecoveryManager.checkAndHydrate();
        } else {
            // Minimal fallback if manager is missing
            const realItems = (window.__mwv_all_library_items || []).filter(i => !i.is_mock);
            if (realItems.length === 0) {
                window.__mwv_all_library_items = [{
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
            
            // v1.41.00 Detection: Trigger Reset if we still have 0 after sync
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
 * Triggers a full library refresh (v1.46.020 Aggressive Recovery).
 * Forces a "Nuclear Reset" of filters and hydration mode to fix visibility black holes.
 */
async function refreshLibrary() {
    console.info("[FE-AUDIT] User Reaction: refreshLibrary() triggered.");
    if (typeof mwv_trace === 'function') mwv_trace('FOOTER-UI', 'REFRESH-CLICK', { ts: Date.now() });

    if (typeof showToast === 'function') showToast("Bibliothek wird aktualisiert...", "info");
    
    // Recovery Pulse (v1.46.020)
    console.warn(">>> [Recovery] refreshLibrary: Forcing Filter & Hydration Reset...");
    if (typeof setHydrationMode === 'function') setHydrationMode('both');
    if (typeof resetAllFilters === 'function') resetAllFilters();
    
    await loadLibrary();
}

/**
 * The main UI update entry point for the Library tab.
 */
async function renderLibrary() {
    // [v1.46.023] Technical Pulse Governance
    if (window.CONFIG && window.CONFIG.render_library_enabled === false) {
        console.warn("[Pulse] renderLibrary blocked by GLOBAL_CONFIG.");
        return;
    }

    const renderStart = performance.now();

    if (typeof mwv_trace_render === 'function') mwv_trace_render('LIBRARY-UI', 'RENDER-START', { count: allLibraryItems.length });
    
    const track = document.getElementById('coverflow-track');
    if (!track) {
        if (typeof log_js_error === 'function') log_js_error(new Error("#coverflow-track missing"), 'LIBRARY-RENDER');
        return;
    }

    // --- PHASE 1: FILTERING (v1.41.00 Hardened) ---
    console.warn(`[FE-AUDIT] Starting Render for ${(window.__mwv_all_library_items || []).length} items. MainCat: ${libraryFilter}, SubCat: ${librarySubFilter}, Search: "${librarySearch}"`);
    if (typeof appendUiTrace === 'function') appendUiTrace(`[Library] Rendering ${window.__mwv_all_library_items.length} items (Filter: ${libraryFilter})...`, "INFO");
    
    // Start with all items (using global state export v1.41.00)
    let projectedItems = [...(window.__mwv_all_library_items || [])];
    const initialCount = projectedItems.length;
    
    // [FE-FORENSIC] Filter Stage 1: Preliminary Cleanup (v1.41.00)
    if (librarySearch) {
        const search = librarySearch.toLowerCase();
        projectedItems = projectedItems.filter(i => (i.name || '').toLowerCase().includes(search));
        console.log(`[FE-AUDIT] Filter Search (${search}): ${projectedItems.length}`);
    }
    const initialRaw = projectedItems.length;
    if (initialRaw === 0 && (window.__mwv_all_library_items || []).length > 0) {
        console.warn("[FE-FORENSIC] Early filter dropped all items. Check search/category sync.");
    }

    // 1. Hydration Mode Filter (Mock/Real/Both) - v1.46.012
    const hmode = window.__mwv_hydration_mode || localStorage.getItem('mwv_hydration_mode') || 'both';
    
    projectedItems = projectedItems.filter(item => {
        // [v1.46.012] Recovery Exemption: Safety items must always show
        if (item.is_recovery || (item.id && String(item.id).startsWith('recovery-'))) return true;
        
        const nameMock = item.name && item.name.startsWith('[MOCK]');
        const mockFlag = (item.is_mock === true || item.is_mock === 1 || nameMock);
        
        if (hmode === 'mock') return mockFlag;
        if (hmode === 'real') return !mockFlag;
        return true; // 'both'
    });

    // 2. HIDB (Diagnostic Hide) - Should usually be OFF
    if (window.__mwv_hide_db) {
        projectedItems = projectedItems.filter(i => i.is_mock || i.is_recovery);
        console.log(`[FE-AUDIT] HIDB active - showing only mock/recovery items.`);
    }

    // 2. Main Category Filter
    if (libraryFilter !== 'all') {
        const catInfo = (typeof CATEGORY_MAP !== 'undefined' ? CATEGORY_MAP[libraryFilter] : null);
        const allowedTypes = catInfo ? (catInfo.aliases || []) : [];
        
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

    // [v1.46.053] HIGH-VISIBILITY FORENSIC SCANNER DASHBOARD
    const realDbCount = window.__mwv_last_db_count || 0;
    const isMockOnly = coverflowItems.every(i => i.is_mock);

    if (realDbCount === 0 || (coverflowItems.length === 0)) {
        let noMediaHtml = "";
        
        // --- TIER A: TOTAL BLACK HOLE OR EMPTY REAL SET ---
        noMediaHtml = `
            <div class="forensic-scanner-dashboard" style="padding: 60px; color: var(--text-primary); text-align: center; width: 100%; max-width: 900px; margin: 40px auto; background: rgba(0,0,0,0.6); border: 2px solid #3498db; border-radius: 20px; box-shadow: 0 0 50px rgba(52, 152, 219, 0.3); backdrop-filter: blur(20px);">
                <div style="font-size: 48px; margin-bottom: 20px;">🕵️ Forensic Media Workstation</div>
                <div style="font-size: 14px; font-weight: 900; color: #3498db; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 25px; background: rgba(52, 152, 219, 0.1); padding: 8px 16px; display: inline-block; border-radius: 4px;">
                    STATUS: EMPTY_INDEX_DETECTED
                </div>
                
                <p style="color: var(--text-secondary); font-size: 16px; line-height: 1.8; margin-bottom: 40px; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Die Medien-Datenbank enthält aktuell keine Indizierung für reale Assets. 
                    Ein vollständiger System-Scan ist erforderlich, um die <span style="color: #3498db; font-weight: 700;">media/</span> Verzeichnisse zu erfassen.
                </p>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-bottom: 40px;">
                    <button onclick="if(window.scan) window.scan()" style="padding: 30px; background: linear-gradient(135deg, #3498db, #2980b9); color: white; border: none; border-radius: 12px; font-weight: 900; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 15px; box-shadow: 0 10px 20px rgba(52, 152, 219, 0.4); transiton: transform 0.2s;">
                        <span style="font-size: 32px;">🔍</span>
                        <div style="display: flex; flex-direction: column;">
                            <span style="font-size: 20px; letter-spacing: 1px;">START SYSTEM SCAN</span>
                            <span style="font-size: 10px; opacity: 0.7; font-weight: 400;">SCANS DIRECTORY: media/</span>
                        </div>
                    </button>
                    
                    <button onclick="if(window.setHydrationMode) window.setHydrationMode('mock')" style="padding: 30px; background: rgba(155, 89, 182, 0.1); color: #9b59b6; border: 2px dashed #9b59b6; border-radius: 12px; font-weight: 900; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 15px;">
                        <span style="font-size: 32px;">🧪</span>
                        <div style="display: flex; flex-direction: column;">
                            <span style="font-size: 20px; letter-spacing: 1px;">VIEW MOCKUPS</span>
                            <span style="font-size: 10px; opacity: 0.7; font-weight: 400;">PROVE RENDERING CAPABILITY</span>
                        </div>
                    </button>
                </div>

                <!-- Forensic Diagnostic Footer -->
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #3498db; opacity: 0.6; display: flex; justify-content: center; gap: 30px; border-top: 1px solid rgba(52, 152, 219, 0.2); padding-top: 20px;">
                    <span>FS_NODE: ONLINE</span>
                    <span>DB_ITEMS: 0</span>
                    <span>ACTIVE_BRANCH: ${window.GLOBAL_CONFIG?.active_branch || 'MULTIMEDIA'}</span>
                </div>
            </div>
        `;
            if (typeof sentinelPulse === 'function') sentinelPulse('ERROR', isRealEmpty ? 'Real set is empty.' : 'Total Black Hole Detected.');
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
    if (typeof eel !== 'undefined' && typeof eel.scan_media === 'function') {
        const res = await eel.scan_media(targetDir, clearDb)();
        if (res && res.status === 'ok') {
            await refreshLibrary();
        }
    }
}
/**
 * Reset All Filters (v1.41.00 Recovery)
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
 * Specialized View Initializers (v1.41.00 Standard)
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

// [v1.46.016] Global Orchestration Handshake
window.loadLibrary = loadLibrary;
window.refreshLibrary = refreshLibrary;
window.scan = scan;
window.renderLibrary = renderLibrary;

// Created with MWV v1.46.00-MASTER
