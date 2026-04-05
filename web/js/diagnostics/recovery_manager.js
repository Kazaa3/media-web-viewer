/**
 * recovery_manager.js (v1.35.55)
 * The control file for the MWV Diagnostic & Recovery Engine.
 * Features: Nuclear Restart, Mock-Filtering, and Unified Hydration.
 */

const RecoveryManager = {
    isActive: localStorage.getItem('mwv_diagnostic_mode') === 'true',
    isNuclear: localStorage.getItem('mwv_nuclear_mode') === 'true',
    hideMocks: localStorage.getItem('mwv_hide_mocks') === 'true',
    stages: [],

    init() {
        console.log(">>> [MANAGER] Recovery Engine starting (Active:", this.isActive, ")");
        if (!this.isActive) return;

        // Auto-Hydration Fail-safe (v1.35.55)
        setTimeout(() => this.checkAndHydrate(), 500);
    },

    /**
     * Registers a new diagnostic stage.
     * @param {Object} stageDef - { id, name, type, items }
     */
    registerStage(stageDef) {
        if (!stageDef.id || !stageDef.items) {
            console.error("[MANAGER] Invalid Stage definition:", stageDef);
            return;
        }
        
        // Avoid duplicate stages
        if (this.stages.find(s => s.id === stageDef.id)) return;
        
        this.stages.push(stageDef);
        console.log(`>>> [MANAGER] Registered Stage: ${stageDef.name} (${stageDef.items.length} items)`);
        
        // RE-HYDRATE on every registration to ensure real-time count updates
        if (this.isActive) this.hydrateAll();
    },

    /**
     * Checks if real data is missing and populates from all registered stages.
     */
    checkAndHydrate() {
        if (!this.isActive) return;
        
        const realItems = (window.allLibraryItems || []).filter(i => !i.is_diag && !i.is_mock);
        if (realItems.length === 0) {
            console.warn(">>> [MANAGER] No real items found. Hydrating registered Stages...");
            this.hydrateAll();
        }
    },

    /**
     * Merges all registered stage items into the global library.
     */
    hydrateAll() {
        if (!this.isActive) return;

        let allDiagItems = [];
        this.stages.forEach(stage => {
            const typedItems = stage.items.map(item => ({
                ...item,
                is_diag: true,
                stage_id: stage.id,
                stage_name: stage.name
            }));
            allDiagItems = [...allDiagItems, ...typedItems];
        });

        // APPLY FILTERS
        if (this.hideMocks) {
            allDiagItems = allDiagItems.filter(item => item.is_mock === false);
            console.log(`>>> [MANAGER] Mock-Filtering Active: Showing ${allDiagItems.length} Real Assets.`);
        }

        // NON-DESTRUCTIVE MERGE
        const existing = window.allLibraryItems || [];
        const merged = [...existing.filter(i => !i.is_diag), ...allDiagItems];
        window.allLibraryItems = merged;

        // Sync Player Queue
        if (typeof window.currentPlaylist !== 'undefined') {
            window.currentPlaylist = [...merged];
        }

        // Trigger UI Refresh (v1.35.55)
        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof renderPlaylist === 'function') renderPlaylist();
        if (typeof window.renderQueue === 'function') window.renderQueue();
        if (typeof window.updateQueueDisplay === 'function') window.updateQueueDisplay();
    },

    toggleHideMocks() {
        this.hideMocks = !this.hideMocks;
        localStorage.setItem('mwv_hide_mocks', this.hideMocks);
        console.log(">>> [MANAGER] Toggle Hide Mocks:", this.hideMocks);
        this.hydrateAll();
    },

    toggle() {
        this.isActive = !this.isActive;
        localStorage.setItem('mwv_diagnostic_mode', this.isActive);
        location.reload();
    },

    /**
     * Nuclear Restart Bridge
     */
    nuclearRestart() {
        if (typeof eel !== 'undefined' && eel.nuclear_restart) {
            console.warn(">>> [MANAGER] NUCLEAR RESTART TRIGGERED!");
            if (typeof showToast === 'function') showToast("NUCLEAR RESTART: Backend disconnect...", "warning");
            eel.nuclear_restart();
        }
    }
};

/**
 * Eel Bridge for Scanning Status
 * @param {boolean} status 
 */
if (typeof eel !== 'undefined') {
    if (eel.expose) {
        eel.expose(js_set_scanning_status);
        function js_set_scanning_status(status) {
            console.log(">>> [MANAGER] Global Scan Status Update:", status);
            window.__mwv_is_scanning = status;
        }
    }
}

// Backward Compatibility for legacy calls
window.Diagnostics = {
    isActive: RecoveryManager.isActive,
    isNuclear: RecoveryManager.isNuclear,
    hideMocks: RecoveryManager.hideMocks,
    init: () => RecoveryManager.init(),
    toggle: () => RecoveryManager.toggle(),
    hydrate: () => RecoveryManager.hydrateAll(),
    restart: () => RecoveryManager.nuclearRestart(),
    toggleMocks: () => RecoveryManager.toggleHideMocks()
};

// Initialize
document.addEventListener('DOMContentLoaded', () => RecoveryManager.init());
window.RecoveryManager = RecoveryManager;
