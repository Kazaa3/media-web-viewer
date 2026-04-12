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
     * Stage 1: Explicitly injects 12 hardcoded recovery items.
     */
    forceEmergencyHydration() {
        this.stage = 1;
        console.warn("[HYDRATION-BRIDGE] STAGE 1: Injecting 12 Emergency Mocks...");

        const emergencyMocks = [];
        for (let i = 1; i <= this.mockCount; i++) {
            emergencyMocks.push({
                id: `emergency-${i}`,
                name: `[RECOVERY] Forensic Asset ${i}`,
                artist: "System Sentinel",
                album: "Hydration Guard v1.46.001",
                category: "audio",
                path: "",
                available: true,
                is_mock: true,
                stage: "PROVENANCE"
            });
        }

        window.currentPlaylist = emergencyMocks;
        if (typeof renderAudioQueue === 'function') {
            renderAudioQueue();
        }

        // Sync Footer (v1.46.001 Integration)
        if (typeof updateSyncAnchor === 'function') {
            updateSyncAnchor(0, this.mockCount);
        }
    },

    /**
     * Stage 2: Sync from allLibraryItems once real data arrives.
     */
    transitionToRealData() {
        this.isLocked = true;
        this.stage = 2;
        console.log("%c[HYDRATION-BRIDGE] STAGE 2: Real Data Detected. Performing Surgical Swap...", "color: #2ecc71; font-weight: 900;");
        
        if (typeof syncQueueWithLibrary === 'function') {
            syncQueueWithLibrary();
        }
        
        setTimeout(() => { this.isLocked = false; }, 5000); // Lock for 5s to stabilize
    }
};

// Global Export
window.ForensicHydrationBridge = ForensicHydrationBridge;
window.FHB = ForensicHydrationBridge;

// Boot Trigger
document.addEventListener('DOMContentLoaded', () => {
    ForensicHydrationBridge.init();
});
