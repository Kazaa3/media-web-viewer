/**
 * gui_integrity.js (v1.35.42)
 * Handles visual verification and UI lockdown.
 */

const GUIIntegrity = {
    hudId: 'mwv-diag-hud',
    
    init() {
        if (!RecoveryManager.isActive) return;
        
        console.log(">>> [INTEGRITY] Monitoring UI Consistency...");
        this.applyNuclearStyles();
        this.startMutationWatch();
        this.injectHUD();
        this.injectHeader();
        
        // Start live sync monitor
        setInterval(() => this.updateHUD(), 1000);
    },

    applyNuclearStyles() {
        if (!RecoveryManager.isNuclear) return;
        console.log(">>> [INTEGRITY] Applying Nuclear Visibility Locks...");
        const style = document.createElement('style');
        style.id = 'mwv-nuclear-lock';
        style.innerHTML = `
            #player-main-viewport, 
            #player-tab-split-container, 
            .player-view-container, 
            #player-view-warteschlange {
                display: flex !important;
                opacity: 1 !important;
                visibility: visible !important;
                z-index: 5000 !important;
                min-height: 500px !important;
                border: 4px solid #00ff00 !important;
            }
            #recovery-test-header {
                display: block !important;
            }
        `;
        document.head.appendChild(style);
    },

    injectHUD() {
        if (document.getElementById(this.hudId)) return;
        const hud = `
            <div id="${this.hudId}" style="position: fixed; bottom: 85px; left: 20px; z-index: 10005; background: rgba(0,0,0,0.85); color: #00ff00; padding: 15px; border-radius: 8px; border: 1px solid #00ff00; font-family: 'JetBrains Mono', monospace; font-size: 11px; min-width: 220px; pointer-events: none; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #003300; padding-bottom: 5px; color: white;">MWV DATA-HUD</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>BACKEND DB:</span> <span id="hud-db-count">...</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>FRONTEND ITEMS:</span> <span id="hud-ui-count">...</span></div>
                <div style="display: flex; justify-content: space-between; border-top: 1px solid #003300; margin-top: 8px; padding-top: 5px;"><span>SYSTEM STATUS:</span> <span id="hud-status" style="color: white;">SYNCING</span></div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', hud);
    },

    updateHUD() {
        const dbCount = window.__mwv_last_db_count || 0;
        const uiCount = (window.allLibraryItems || []).length;
        
        const dbEl = document.getElementById('hud-db-count');
        const uiEl = document.getElementById('hud-ui-count');
        const statusEl = document.getElementById('hud-status');
        
        if (dbEl) dbEl.innerText = dbCount;
        if (uiEl) uiEl.innerText = uiCount;
        
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

    injectHeader() {
        if (document.getElementById('recovery-test-header')) return;
        const msg = RecoveryManager.isNuclear ? "NUCLEAR" : "ACTIVE";
        document.body.insertAdjacentHTML('afterbegin', `
            <div id="recovery-test-header" style="position: fixed; top: 0; left: 0; right: 0; z-index: 10010; background: rgba(255,0,0,0.9); color: white; padding: 5px 20px; font-weight: bold; font-family: monospace; font-size: 12px; display: flex; justify-content: space-between; align-items: center;">
                <span>DIAGNOSTIC MODE: ${msg} (v1.35.42)</span>
                <div>
                   <button onclick="RecoveryManager.hydrateAll()" style="background: white; border: none; padding: 2px 10px; cursor: pointer; color: black; font-weight: bold; margin-right: 10px;">FORCE HYDRATION</button>
                   <button onclick="RecoveryManager.toggle()" style="background: black; color: white; border: none; padding: 2px 10px; cursor: pointer;">DISABLE</button>
                </div>
            </div>
        `);
    },

    startMutationWatch() {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((m) => {
                if (m.attributeName === 'style' || m.attributeName === 'class') {
                    const display = window.getComputedStyle(m.target).display;
                    if (display === 'none' && (m.target.id === 'player-main-viewport')) {
                        m.target.style.display = 'flex';
                    }
                }
            });
        });
        observer.observe(document.body, { attributes: true, subtree: true });
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => GUIIntegrity.init());
window.GUIIntegrity = GUIIntegrity;
