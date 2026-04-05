/**
 * MWV Diagnostic Suite (v1.35.34)
 * Formalized recovery and visibility toolset.
 */

const Diagnostics = {
    isActive: localStorage.getItem('mwv_diagnostic_mode') === 'true',
    isNuclear: localStorage.getItem('mwv_nuclear_mode') === 'true',

    init() {
        console.log(">>> [DIAGNOSTICS] Suite initialized. Active:", this.isActive);
        if (this.isActive) {
            this.applyNuclearStyles();
            this.startMutationWatch();
            this.injectHeader();
            this.injectHUD(); // New: Persistent Visibility HUD
        }

        // Sync UI Buttons
        this.syncUI();

        // Auto-Hydration Fail-safe (2.5s after boot)
        setTimeout(() => this.checkAndHydrate(), 2500);
        
        // Start live sync monitor
        setInterval(() => this.updateHUD(), 1000);
    },

    injectHUD() {
        if (document.getElementById('mwv-diag-hud')) return;
        const hud = `
            <div id="mwv-diag-hud" style="position: fixed; bottom: 80px; left: 20px; z-index: 10005; background: rgba(0,0,0,0.85); color: #00ff00; padding: 15px; border-radius: 8px; border: 1px solid #00ff00; font-family: 'JetBrains Mono', monospace; font-size: 11px; min-width: 220px; pointer-events: none; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #003300; padding-bottom: 5px; color: white;">MWV DATA-HUD</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>BACKEND DB:</span> <span id="hud-db-count">...</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>FRONTEND ITEMS:</span> <span id="hud-ui-count">...</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>DOM ELEMENTS:</span> <span id="hud-dom-count">...</span></div>
                <div style="display: flex; justify-content: space-between; border-top: 1px solid #003300; margin-top: 8px; padding-top: 5px;"><span>SYSTEM STATUS:</span> <span id="hud-status" style="color: white;">SYNCING</span></div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', hud);
    },

    updateHUD() {
        if (!this.isActive) return;
        const dbCount = window.__mwv_last_db_count || 0;
        const uiCount = (window.allLibraryItems || []).length;
        const domCount = document.querySelectorAll('.legacy-track-item, .library-item').length;
        
        const dbEl = document.getElementById('hud-db-count');
        const uiEl = document.getElementById('hud-ui-count');
        const domEl = document.getElementById('hud-dom-count');
        const statusEl = document.getElementById('hud-status');
        
        if (dbEl) dbEl.innerText = dbCount;
        if (uiEl) uiEl.innerText = uiCount;
        if (domEl) domEl.innerText = domCount;
        
        if (statusEl) {
            if (dbCount > 0 && uiCount === 0) {
                statusEl.innerText = "DATA LEAK (0 UI)";
                statusEl.style.color = "#ff4444";
            } else if (dbCount === 0) {
                statusEl.innerText = "EMPTY DB";
                statusEl.style.color = "#ffaa00";
            } else {
                statusEl.innerText = "STABLE SYNC";
                statusEl.style.color = "#00ff00";
            }
        }
    },

    syncUI() {
        // ... (previous buttons logic)
    },

    // ... (toggle, applyNuclearStyles, injectHeader, startMutationWatch same as before)

    checkAndHydrate() {
        const libCount = (window.allLibraryItems || []).length;
        // v1.35.40: More intelligent check. Don't hydrate if we have real items.
        const realItems = (window.allLibraryItems || []).filter(i => !i.is_diag && !i.is_mock);
        if (realItems.length === 0) {
            console.warn(">>> [DIAGNOSTICS] No real items found after 2.5s. Triggering Multi-Stage Hydration...");
            this.hydrate();
        }
    },

    hydrate() {
        console.log(">>> [DIAGNOSTICS] Multi-Stage Atomic Hydration starting...");
        
        const tracks = [
            {
                id: 'diag-stage-1',
                name: 'sample_audio_missing.mp3',
                path: 'media/sample_audio_missing.mp3',
                title: '[STAGE 1] Missing File Test',
                artist: 'MWV Discovery (Simulation)',
                tags: { title: '[STAGE 1] Missing File Test', artist: 'MWV Discovery (Simulation)' },
                is_diag: true,
                is_mock: true
            },
            {
                id: 'diag-stage-2',
                name: 'test_track_missing.m4a',
                path: 'media/test_track_missing.m4a',
                title: '[STAGE 2] Missing File Test',
                artist: 'MWV Discovery (Simulation)',
                tags: { title: '[STAGE 2] Missing File Test', artist: 'MWV Discovery (Simulation)' },
                is_diag: true,
                is_mock: true
            },
            {
                id: 'diag-stage-3',
                name: '01 - Einfach & Leicht.mp3',
                path: 'media/01 - Einfach & Leicht.mp3',
                title: '[STAGE 3] Real File - Happy Path',
                artist: 'MWV Discovery (Real Asset)',
                tags: { title: '[STAGE 3] Real File - Happy Path', artist: 'MWV Discovery (Real Asset)' },
                is_diag: true,
                is_mock: false
            },
            {
                id: 'diag-stage-4',
                name: 'Coldplay - Viva La Vida.opus',
                path: 'media/Coldplay - Viva La Vida.opus',
                title: '[STAGE 4] Real File - Happy Path',
                artist: 'MWV Discovery (Real Asset)',
                tags: { title: '[STAGE 4] Real File - Happy Path', artist: 'MWV Discovery (Real Asset)' },
                is_diag: true,
                is_mock: false
            }
        ];

        // v1.35.40: NON-DESTRUCTIVE MERGE
        const existing = window.allLibraryItems || [];
        const merged = [...existing.filter(i => !i.is_diag), ...tracks];
        window.allLibraryItems = merged;

        if (typeof window.currentPlaylist !== 'undefined') {
            window.currentPlaylist = [...merged];
        }

        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof renderPlaylist === 'function') renderPlaylist();

        if (typeof showToast === 'function') showToast("Multi-Stage Recovery Battery Active", "success");
    }
};

// Initialize on load
document.addEventListener('DOMContentLoaded', () => Diagnostics.init());
window.Diagnostics = Diagnostics;
