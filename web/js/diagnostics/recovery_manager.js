/**
 * recovery_manager.js (v1.35.42)
 * The control file for the MWV Diagnostic & Recovery Engine.
 * Manages Stage registration and orchestrates data hydration.
 */

const RecoveryManager = {
    isActive: localStorage.getItem('mwv_diagnostic_mode') === 'true',
    isNuclear: localStorage.getItem('mwv_nuclear_mode') === 'true',
    stages: [],

    init() {
        console.log(">>> [MANAGER] Recovery Engine starting (Active:", this.isActive, ")");
        if (!this.isActive) return;

        // Auto-Hydration Fail-safe (2.5s after boot)
        setTimeout(() => this.checkAndHydrate(), 2500);
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
        this.stages.push(stageDef);
        console.log(`>>> [MANAGER] Registered Stage: ${stageDef.name} (${stageDef.items.length} items)`);
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

        // NON-DESTRUCTIVE MERGE
        const existing = window.allLibraryItems || [];
        const merged = [...existing.filter(i => !i.is_diag), ...allDiagItems];
        window.allLibraryItems = merged;

        // Sync Player Queue
        if (typeof window.currentPlaylist !== 'undefined') {
            window.currentPlaylist = [...merged];
        }

        // Trigger UI Refresh
        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof renderPlaylist === 'function') renderPlaylist();

        if (typeof showToast === 'function') {
             showToast(`Handled Recovery: ${this.stages.length} Stages Hydrated`, "success");
        }
    },

    toggle() {
        this.isActive = !this.isActive;
        localStorage.setItem('mwv_diagnostic_mode', this.isActive);
        location.reload();
    }
};

// Backward Compatibility for legacy calls
window.Diagnostics = {
    isActive: RecoveryManager.isActive,
    isNuclear: RecoveryManager.isNuclear,
    init: () => RecoveryManager.init(),
    toggle: () => RecoveryManager.toggle(),
    hydrate: () => RecoveryManager.hydrateAll()
};

// Initialize
document.addEventListener('DOMContentLoaded', () => RecoveryManager.init());
window.RecoveryManager = RecoveryManager;
