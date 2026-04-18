/**
 * Forensic Hydration Bridge (v1.46.076)
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
        console.log("%c[HYDRATION-BRIDGE] ARMED. Version v1.46.076", "color: #ff9500; font-weight: 900;");
        this.auditLoop();
    },

    /**
     * Periodic audit to move through hydration stages.
     */
    auditLoop() {
        const auditMs = window.CONFIG?.technical_orchestrator?.intervals?.hydration_audit_ms || 2000;
        let auditTicks = 0;

        setInterval(() => {
            auditTicks++;
            const hasLib = (typeof allLibraryItems !== 'undefined' && Array.isArray(allLibraryItems) && allLibraryItems.length > 0);
            
            if (this.stage === 0) {
                // Stage 0 -> 1: Immediate Proof-of-Life Injection
                this.forceEmergencyHydration();
            } else if (this.stage === 1 && !this.isLocked) {
                const firstItem = (window.allLibraryItems && window.allLibraryItems.length > 0) ? window.allLibraryItems[0] : null;
                const isReal = firstItem && !firstItem.id?.toString().startsWith('emergency-');
                
                // [v1.46.079] Auto-Promotion: If real items detected OR if we've been in mock-state for 5+ seconds
                if (isReal || auditTicks > 3) {
                    console.log(`[HYDRATION-BRIDGE] Promoting to Stage 2. Reason: ${isReal ? "Real Data Detected" : "Audit Timeout (Synthetic Promotion)"}`);
                    this.transitionToRealData();
                }
            }
        }, auditMs);
    },

    /**
     * Stage 1: Explicitly injects 12 hardcoded recovery items into Library & Queue.
     */
    forceEmergencyHydration() {
        // [v1.46.056] Hardened Forensic Skip Logic
        const realDbCount = window.__mwv_last_db_count || 0;
        const hasRealItems = (window.__mwv_all_library_items && window.__mwv_all_library_items.length > 0 && !window.__mwv_all_library_items[0].id?.toString().startsWith('emergency-'));

        if (realDbCount > 0 || hasRealItems) {
            console.log(`[HYDRATION-BRIDGE] Skip Stage 1: Real Items verified. DB: ${realDbCount} | FE-Cache: ${hasRealItems}`);
            this.transitionToRealData();
            
            // [v1.46.057] Aggressive Restoration: Trigger real load immediately to break the mock loop
            if (typeof loadLibrary === 'function') loadLibrary();
            return;
        }

        this.stage = 1;

        // [v1.46.095] Full Centralized Consumption
        const config = window.CONFIG?.technical_orchestrator?.hydration || {};
        const emergencyMocks = config.emergency_mocks || [];

        console.warn(`[HYDRATION-BRIDGE] STAGE 1: Injecting ${emergencyMocks.length} Centralized Mocks...`);

        // Hydrate both states to prove rendering path
        window.allLibraryItems = emergencyMocks;
        window.__mwv_all_library_items = emergencyMocks; 
        window.currentPlaylist = [...emergencyMocks];
        
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof renderLibrary === 'function') renderLibrary();
        if (typeof updateLibraryUI === 'function') updateLibraryUI();

        // Sync Footer
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(realDbCount, emergencyMocks.length);
        }
    },

    /**
     * Stage 2: Handshake transitioning based on M/R/B Mode.
     */
    transitionToRealData() {
        if (this.isLocked) return;
        this.isLocked = true;
        this.stage = 2;
        
        let mode = window.__mwv_hydration_mode || localStorage.getItem('mwv_hydration_mode') || 'both';
        
        // [v1.46.085] Aggressive Hydration Hardening: If DB has items, force REAL mode
        const realDbCount = window.__mwv_last_db_count || 0;
        if (realDbCount > 0 && mode !== 'real') {
            console.warn(`[HYDRATION-BRIDGE] Real database content detected (${realDbCount} items). Forcing REAL mode to purge mocks.`);
            mode = 'real';
            window.__mwv_hydration_mode = 'real';
            localStorage.setItem('mwv_hydration_mode', 'real');
        }

        console.log(`%c[HYDRATION-BRIDGE] STAGE 2: Applying ${mode.toUpperCase()} Hydration Logic...`, "color: #2ecc71; font-weight: 900;");

        // Split current registry
        const allItems = window.allLibraryItems || [];
        let realItems = allItems.filter(it => it.id && !it.id.toString().startsWith('emergency-'));
        const mockItems = allItems.filter(it => it.id && it.id.toString().startsWith('emergency-'));

        // [v1.46.075] Synthetic Diagnostic Integration
        // If realItems is empty, try to pull from RecoveryManager stages (user-requested repair)
        if (realItems.length === 0 && typeof window.RecoveryManager !== 'undefined' && window.RecoveryManager.stages.length > 0) {
            console.warn("[HYDRATION-BRIDGE] Real items missing. Injecting Synthetic Diagnostic Stages...");
            let syntheticItems = [];
            window.RecoveryManager.stages.forEach(stage => {
                const typedItems = stage.items.map(item => ({
                    ...item,
                    is_diag: true,
                    is_mock: false, // Force real status for diagnostic samples
                    stage_id: stage.id,
                    stage_name: stage.name
                }));
                syntheticItems = [...syntheticItems, ...typedItems];
            });
            realItems = syntheticItems;
        }

        // If we still have 0 real items and the database has content, force a refresh
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
