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
        }, 2000);
    },

    /**
     * Stage 1: Explicitly injects 12 hardcoded recovery items into Library & Queue.
     */
    forceEmergencyHydration() {
        this.stage = 1;
        console.warn("[HYDRATION-BRIDGE] STAGE 1: Injecting 12 Emergency Mocks...");

        const emergencyMocks = [];
        for (let i = 1; i <= this.mockCount; i++) {
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

        // Hydrate both states to prove rendering path (v1.46.003)
        window.allLibraryItems = emergencyMocks;
        window.currentPlaylist = [...emergencyMocks];
        
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof updateLibraryUI === 'function') updateLibraryUI();

        // Sync Footer (v1.46.003 Format [FS|DB|GUI])
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(0, this.mockCount);
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
        const realItems = [...window.allLibraryItems].filter(it => !it.id.toString().startsWith('emergency-'));
        const mockItems = [...window.allLibraryItems].filter(it => it.id.toString().startsWith('emergency-'));

        if (mode === 'real') {
            window.allLibraryItems = realItems;
        } else if (mode === 'both') {
            window.allLibraryItems = [...mockItems, ...realItems];
        } else {
            // Mode 'mock'
            window.allLibraryItems = mockItems;
        }

        // Surgical update of the active queue
        if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
        if (typeof updateLibraryUI === 'function') updateLibraryUI();
        
        // Final Parity Flush
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(realItems.length, window.allLibraryItems.length);
        }

        setTimeout(() => { this.isLocked = false; }, 3000);
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
