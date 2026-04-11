/**
 * VisibilitySentinel (v1.44)
 * Forensic background monitor that ensures the UI 'Stage' remains visible
 * and hydrated, preventing 'Black Hole' rendering failures.
 */
const VisibilitySentinel = {
    interval: null,
    stageId: 'rebuild-stage',
    lastCheck: Date.now(),

    /**
     * Starts the monitoring loop.
     */
    init() {
        console.info("[SENTINEL] Initializing Forensic Visibility Watchdog...");
        if (this.interval) clearInterval(this.interval);
        
        this.interval = setInterval(() => {
            this.audit();
        }, 1000); // 1s Heartbeat
    },

    /**
     * Performs a visual integrity check on the main stage.
     */
    audit() {
        const isRebuild = window.GLOBAL_CONFIG?.ui_evolution_mode === 'rebuild';
        if (!isRebuild) return;

        const stage = document.getElementById(this.stageId);
        if (!stage) return;

        // --- RULE 1: Visibility Enforcement ---
        const style = window.getComputedStyle(stage);
        if (style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0') {
            console.warn("[SENTINEL] CRITICAL: Active Stage is HIDDEN. Enforcing emergency visibility...");
            stage.style.display = 'flex';
            stage.style.visibility = 'visible';
            stage.style.opacity = '1';
            
            if (typeof mwv_trace === 'function') {
                mwv_trace('STABILITY', 'RESCUE-VISIBILITY', { stageId: this.stageId });
            }
        }

        // --- RULE 2: Hydration Enforcement ---
        if (stage.innerHTML.trim() === "" || stage.querySelector('.loading-fragment')) {
            // If empty for too long, trigger re-activation of current window
            const activeWin = window.WindowManager?.activeWindow;
            if (activeWin && Date.now() - this.lastCheck > 5000) {
                 console.warn(`[SENTINEL] Stage is EMPTY for 5s. Triggering emergency re-activation for: ${activeWin}`);
                 window.WindowManager.activate(activeWin, true);
                 this.lastCheck = Date.now();
            }
        } else {
            this.lastCheck = Date.now();
        }
    }
};

// Auto-init on load
window.addEventListener('DOMContentLoaded', () => {
    VisibilitySentinel.init();
});
