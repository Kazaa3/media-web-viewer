/**
 * Forensic Hydration Bridge (v1.46.001)
 * Orchestrates the mandatory 0 -> 12 -> Real hydration handshake.
 * Proves rendering health via specific emergency mock stages.
 */

const ForensicHydrationBridge = {
    stage: 0, // 0: Empty, 1: Emergency Mock (12), 2: Real Hydration
    isLocked: false,
    mockCount: 12,

    /**
     * Initializes the bridge and monitors the boot state.
     */
    init() {
        console.log("%c[HYDRATION-BRIDGE] ARMED. Version v1.46.001", "color: #ff9500; font-weight: 900;");
        this.auditLoop();
    },

    /**
     * Periodic audit to move through hydration stages.
     */
    auditLoop() {
        const auditMs = window.CONFIG?.technical_orchestrator?.intervals?.hydration_audit_ms || 2000;
        setInterval(() => {
            const hasLib = (typeof allLibraryItems !== 'undefined' && Array.isArray(allLibraryItems) && allLibraryItems.length > 0);
            const queueLen = (typeof currentPlaylist !== 'undefined') ? currentPlaylist.length : 0;

            if (this.stage === 0) {
                // Stage 0 -> 1: Immediate Proof-of-Life Injection
                this.forceEmergencyHydration();
            } else if (this.stage === 1 && hasLib && !this.isLocked) {
                const firstItem = allLibraryItems[0];
                const isReal = firstItem && !firstItem.id?.startsWith('emergency-');
                if (isReal) {
                    // Stage 1 -> 2: Transition to Real Data
                    this.transitionToRealData();
                }
            }
        }, auditMs);
    },

    /**
     * Stage 1: Explicitly injects 12 hardcoded recovery items into Library & Queue.
     */
    forceEmergencyHydration() {
        // [v1.46.015] COLLISION GUARD: Do not inject mocks if we already have real items loaded
        const realDbCount = window.__mwv_last_db_count || 0;
        if (realDbCount > 0) {
            console.log("[HYDRATION-BRIDGE] Skip Stage 1: Real Items detected in registry.");
            this.transitionToRealData();
            return;
        }

        this.stage = 1;
        const mockCount = window.CONFIG?.technical_orchestrator?.hydration?.mock_count || 12;
        console.warn(`[HYDRATION-BRIDGE] STAGE 1: Injecting ${mockCount} Emergency Mocks...`);

        const emergencyMocks = [];
        for (let i = 1; i <= mockCount; i++) {
            emergencyMocks.push({
                id: `emergency-${i}`,
                filename: `mock_asset_${i}.wav`,
                path: `media/mock_asset_${i}.wav`,
                title: `Forensic Proof-of-Life ${i}`,
                artist: "System Sentinel",
                album: "Hydration Guard v1.46.003",
                category: "audio",
                is_mock: true,
                available: true
            });
        }

        // Hydrate both states to prove rendering path (v1.46.017 Fix: Dual-Variable Sync)
        window.allLibraryItems = emergencyMocks;
        window.__mwv_all_library_items = emergencyMocks; 
        window.currentPlaylist = [...emergencyMocks];
        
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof updateLibraryUI === 'function') updateLibraryUI();

        // Sync Footer (v1.46.014/015: Handshake with real DB count)
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(realDbCount, this.mockCount);
        }
    },

    /**
     * Stage 2: Handshake transitioning based on M/R/B Mode.
     */
    transitionToRealData() {
        if (this.isLocked) return;
        this.isLocked = true;
        this.stage = 2;
        
        const mode = window.__mwv_hydration_mode || 'both';
        console.log(`%c[HYDRATION-BRIDGE] STAGE 2: Applying ${mode.toUpperCase()} Hydration Logic...`, "color: #2ecc71; font-weight: 900;");

        // Split current registry
        const allItems = window.allLibraryItems || [];
        const realItems = allItems.filter(it => it.id && !it.id.toString().startsWith('emergency-'));
        const mockItems = allItems.filter(it => it.id && it.id.toString().startsWith('emergency-'));

        // If we have 0 real items despite transition trigger, we force a fallback mock set
        if (realItems.length === 0 && (window.__mwv_last_db_count || 0) > 0) {
            console.warn("[HYDRATION-BRIDGE] STAGE 2 Handshake Failed: Real items missing in registry. Forcing Backend Pulse.");
            if (typeof refreshLibrary === 'function') refreshLibrary();
            this.isLocked = false;
            return;
        }

        if (mode === 'real') {
            window.allLibraryItems = realItems;
        } else if (mode === 'both') {
            window.allLibraryItems = [...mockItems, ...realItems];
        } else {
            // Mode 'mock'
            window.allLibraryItems = mockItems;
        }

        // [v1.46.017] Sync SSOT Dual-Variable
        window.__mwv_all_library_items = window.allLibraryItems;

        // Surgical update of the active queue (Respect v1.46.039 Flag)
        const config = window.CONFIG || window.GLOBAL_CONFIG || {};
        const autoHydrate = config.queue_orchestration?.auto_hydration_enabled !== false;
        
        if (autoHydrate && typeof syncQueueWithLibrary === 'function') {
            syncQueueWithLibrary();
        } else {
            console.info("[HYDRATION-BRIDGE] Skipping Queue Sync: auto_hydration_enabled is FALSE.");
        }
        
        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof updateLibraryUI === 'function') updateLibraryUI();
        
        // Final Parity Flush (v1.46.004/014 Fix: Use Backend DB Count)
        if (typeof updateSyncAnchor === 'function') {
            const db_count = window.__mwv_last_db_count || realItems.length;
            updateSyncAnchor(db_count, window.allLibraryItems.length);
        }

        setTimeout(() => { this.isLocked = false; }, 3000);
    },
    
    /**
     * STRESS TEST: Inject High-Density Mock Data (v1.46.019)
     */
    injectStressSet(count = 100) {
        console.warn(`%c[HYDRATION-BRIDGE] TRIGGERING STRESS TEST: ${count} items`, "color: #ff3366; font-weight: 900;");
        
        const stressMocks = [];
        const categories = ['audio', 'video', 'album', 'podcast', 'series', 'bilder'];
        
        for (let i = 1; i <= count; i++) {
            const cat = categories[i % categories.length];
            stressMocks.push({
                id: `stress-${i}`,
                name: `[STRESS] forensic_media_file_${i}_hd.mp4`,
                path: `/stress/test/forensic_media_file_${i}_hd.mp4`,
                title: `Stress Probe #${i}`,
                artist: "Chaos Monkey Engine",
                album: "Hydration Stress v1.46.019",
                category: cat,
                is_mock: true,
                available: Math.random() > 0.1 // 10% chance of being 'offline'
            });
        }
        
        // Append to existing library
        if (!window.allLibraryItems) window.allLibraryItems = [];
        window.allLibraryItems = [...window.allLibraryItems, ...stressMocks];
        window.__mwv_all_library_items = window.allLibraryItems;
        
        if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
        if (typeof renderLibrary === 'function') renderLibrary();
        
        if (typeof showToast === 'function') showToast(`Stress Test: ${count} items injected.`, "info");
    }
};

// Created with MWV v1.46.004-MASTER

// Global Export
window.ForensicHydrationBridge = ForensicHydrationBridge;
window.FHB = ForensicHydrationBridge;

// Boot Trigger
document.addEventListener('DOMContentLoaded', () => {
    ForensicHydrationBridge.init();
});
