/**
 * gui_integrity.js (v1.35.51)
 * Handles visual verification and UI relocation.
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
        this.syncFooter();
        
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
            <div id="${this.hudId}" style="position: fixed; bottom: 85px; left: 20px; z-index: 10005; background: rgba(0,0,0,0.85); color: #00ff00; padding: 15px; border-radius: 8px; border: 1px solid #00ff00; font-family: 'JetBrains Mono', monospace; font-size: 11px; min-width: 240px; pointer-events: none; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.5);">
                <div style="font-weight: bold; margin-bottom: 8px; border-bottom: 1px solid #003300; padding-bottom: 5px; color: white;">MWV DATA-HUD (${window.MWV_VERSION || 'v1.35.x'})</div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>BOOT TIME:</span> <span id="hud-boot-time">...</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>BACKEND DB:</span> <span id="hud-db-count">...</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>FRONTEND ITEMS:</span> <span id="hud-ui-count">...</span></div>
                <div style="display: flex; justify-content: space-between; margin-bottom: 4px;"><span>SCAN STATUS:</span> <span id="hud-scan-status" style="color: #666;">IDLE</span></div>
                <div style="display: flex; justify-content: space-between; border-top: 1px solid #003300; margin-top: 8px; padding-top: 5px;"><span>SYSTEM STATUS:</span> <span id="hud-status" style="color: white;">SYNCING</span></div>
                <div style="margin-top: 10px;">
                    <button onclick="GUIIntegrity.verifyWithFFplay()" 
                            style="width: 100%; padding: 5px; background: rgba(0,255,0,0.1); border: 1px solid #00ff00; color: #00ff00; border-radius: 4px; font-size: 10px; cursor: pointer; font-weight: bold;">
                        VERIFY WITH FFPLAY
                    </button>
                </div>
            </div>
        `;
        document.body.insertAdjacentHTML('beforeend', hud);
    },

    updateHUD() {
        const dbCount = window.__mwv_last_db_count || 0;
        const uiCount = (window.allLibraryItems || []).length;
        const bootTime = (performance.now() - (window.MWV_BOOT_START || 0)).toFixed(0);
        
        const bootEl = document.getElementById('hud-boot-time');
        const dbEl = document.getElementById('hud-db-count');
        const uiEl = document.getElementById('hud-ui-count');
        const scanEl = document.getElementById('hud-scan-status');
        const statusEl = document.getElementById('hud-status');
        
        if (bootEl) bootEl.innerText = `${bootTime}ms`;
        if (dbEl) dbEl.innerText = dbCount;
        if (uiEl) uiEl.innerText = uiCount;
        
        if (scanEl) {
            const isScanning = window.__mwv_is_scanning === true;
            scanEl.innerText = isScanning ? "INDEXING..." : "IDLE";
            scanEl.style.color = isScanning ? "#00ff00" : "#666";
            if (isScanning) scanEl.style.textShadow = "0 0 5px #00ff00";
            else scanEl.style.textShadow = "none";
        }
        
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
        const version = window.MWV_VERSION || 'v1.35.x';
        document.body.insertAdjacentHTML('afterbegin', `
            <div id="recovery-test-header" style="
                position: fixed; 
                bottom: 74px; 
                right: 20px; 
                z-index: 10010; 
                background: rgba(231, 76, 60, 0.9); 
                color: white; 
                padding: 5px 15px; 
                font-weight: bold; 
                font-family: monospace; 
                font-size: 11px; 
                display: flex; 
                gap: 15px; 
                align-items: center;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.3);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255,255,255,0.2);
            ">
                <span>DIAGNOSTIC MODE: ${msg} (${version})</span>
                <div style="display: flex; gap: 8px;">
                   <button onclick="RecoveryManager.hydrateAll()" style="background: white; border: none; padding: 2px 8px; cursor: pointer; color: black; font-weight: bold; font-size: 10px; border-radius: 4px;">FORCE HYDRATION</button>
                   <button onclick="RecoveryManager.toggle()" style="background: black; color: white; border: none; padding: 2px 8px; cursor: pointer; font-size: 10px; border-radius: 4px;">DISABLE</button>
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
    },

    syncFooter() {
        const el = document.getElementById('mwv-footer-version');
        if (el && window.MWV_VERSION) {
            el.innerText = window.MWV_VERSION;
            el.style.color = "#00ff00";
            el.style.fontWeight = "bold";
        }
    },

    verifyWithFFplay() {
        const pipeline = document.getElementById('native-html5-audio-pipeline-element');
        if (!pipeline || !pipeline.src) {
             alert("Nothing playing (no source found in pipeline).");
             return;
        }

        const url = pipeline.src;
        console.log(">>> [INTEGRITY] Requesting native FFplay for:", url);
        if (typeof eel !== 'undefined' && typeof eel.run_ffplay === 'function') {
            eel.run_ffplay(url)((res) => {
                console.log("[INTEGRITY] FFplay Response:", res);
                if (res.status === 'success') {
                    if (typeof showToast === 'function') showToast("FFplay Launched", "success");
                } else {
                    alert("FFplay Error: " + res.message);
                }
            });
        } else {
            alert("Eel run_ffplay not exposed.");
        }
    }
};

// Initialize
document.addEventListener('DOMContentLoaded', () => GUIIntegrity.init());
window.GUIIntegrity = GUIIntegrity;
