/**
 * VisibilitySentinel (v1.45)
 * Forensic background monitor that ensures the UI 'Stage' remains visible
 * and hydrated, preventing 'Black Hole' rendering failures.
 */
const VisibilitySentinel = {
    interval: null,
    lastCheck: Date.now(),
    recoveryCounter: 0,

    /**
     * Starts the monitoring loop.
     */
    init() {
        console.info("[SENTINEL] Initializing Forensic Visibility Watchdog...");
        if (this.interval) clearInterval(this.interval);
        
        this.interval = setInterval(() => {
            this.audit();
        }, 2000); // 2s Forensic Pulse
    },

    /**
     * Performs a visual integrity check on the main stage and active shells.
     */
    audit() {
        if (!window.WindowManager) return;
        
        const activeWin = window.WindowManager.activeWindow;
        if (!activeWin) return;
        
        const winConfig = window.WindowManager.windows.get(activeWin);
        if (!winConfig) return;

        // --- RULE 1: Shell Visibility Enforcement ---
        const shell = document.getElementById(winConfig.shellId) || document.querySelector(`.tab-content[data-tab-domain="${activeWin}"]`);
        if (shell) {
            const style = window.getComputedStyle(shell);
            const isHidden = style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0' || style.opacity < 0.1;
            
            if (isHidden && shell.classList.contains('active')) {
                console.warn(`[SENTINEL] CRITICAL: Active Shell (${activeWin}) is HIDDEN. Enforcing emergency visibility...`);
                shell.style.display = 'flex';
                shell.style.visibility = 'visible';
                shell.style.opacity = '1';
                
                if (typeof mwv_trace === 'function') {
                    mwv_trace('STABILITY', 'RESCUE-VISIBILITY', { activeWin, shellId: winConfig.shellId });
                }
            }
        }

        // --- RULE 2: Fragment Hydration Enforcement ---
        const fragContainer = document.getElementById(winConfig.fragmentId);
        if (fragContainer) {
            const html = fragContainer.innerHTML.trim();
            const isStuck = html === "" || html.includes('loading-fragment') || html.includes('Lade...');
            
            if (isStuck) {
                if (Date.now() - this.lastCheck > 4000) {
                    console.warn(`[SENTINEL] Active Fragment (${activeWin}) is STUCK or EMPTY for 4s. Triggering recovery pulse...`);
                    this.recoveryCounter++;
                    
                    if (this.recoveryCounter > 3) {
                        console.error("[SENTINEL] Recovery loop detected. Attempting Atomic Emergency Reload.");
                        setTimeout(() => location.reload(), 1000);
                        return;
                    }

                    window.WindowManager.activate(activeWin, true); // Force re-activation
                    this.lastCheck = Date.now();
                    
                    if (typeof showToast === 'function') {
                        showToast(`RECOVERY: RESTORING ${activeWin.toUpperCase()}`, 3000);
                    }
                }
            } else {
                this.lastCheck = Date.now();
                this.recoveryCounter = 0;
            }
        }

        // --- RULE 3: Unified Rebuild-Stage (Legacy Support) ---
        const stage = document.getElementById('rebuild-stage');
        if (stage && window.getComputedStyle(stage).display === 'flex') {
             if (stage.innerHTML.trim() === "") {
                 console.warn("[SENTINEL] Rebuild-Stage is EMPTY. Triggering failover.");
                 window.WindowManager.activate(activeWin, true);
             }
        }
    }
};

// Auto-init on load
window.addEventListener('DOMContentLoaded', () => {
    VisibilitySentinel.init();
});
