/**
 * Nuclear Recovery Pulse (v1.46.04)
 * High-frequency DOM brute-force engine to eliminate black-screen failures.
 */

const NuclearPulsar = {
    interval: null,
    iterations: 0,
    isActive: true,

    /**
     * Starts the periodic nuclear shout.
     */
    start() {
        if (this.interval) clearInterval(this.interval);
        console.log("%c[NUCLEAR-PULSE] SURGICAL STABILIZATION ACTIVE.", "color: #00ffcc; font-weight: 900;");
        const pulseMs = window.CONFIG?.technical_orchestrator?.intervals?.recovery_pulse_ms || 1000;
        this.interval = setInterval(() => this.pulse(), pulseMs);
    },

    /**
     * The brute-force iteration pulse.
     */
    pulse() {
        if (!this.isActive) return;
        this.iterations++;

        // 1. NON-DESTRUCTIVE Visibility Enforcement
        const targets = ['player-panel-container', 'player-main-viewport', 'main-content-area', 'player-deck-column', 'player-playlist-column'];
        targets.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                // Only enforce flex if it's the main container or an active tab
                if (el.id === 'main-content-area' || el.classList.contains('active') || el.id.includes('panel')) {
                    el.style.setProperty('display', 'flex', 'important');
                }
                el.style.setProperty('visibility', 'visible', 'important');
                el.style.setProperty('opacity', '1', 'important');
            }
        });

        // 2. HYDRATION SENTINEL (v1.46.12)
        this.enforceHydration();

        // 3. Pulse Indicators
        this.injectRecoveryBadge();
        this.injectForensicAnchor();

        if (this.iterations % 10 === 0 && typeof eel !== 'undefined' && eel.log_spawn_event) {
            eel.log_spawn_event('recovery-pulse', `surgical_pulse_iter_${this.iterations}`);
        }
    },

    /**
     * Enforces that the Global Queue is populated if the Library is hydrated.
     */
    enforceHydration() {
        const hasLibrary = (typeof allLibraryItems !== 'undefined' && Array.isArray(allLibraryItems) && allLibraryItems.length > 0);
        const queueEmpty = (typeof currentPlaylist !== 'undefined' && Array.isArray(currentPlaylist) && currentPlaylist.length === 0);
        
        if (hasLibrary && queueEmpty) {
            console.warn(`[NUCLEAR-PULSE] HYDRATION GAP DETECTED. Library: ${allLibraryItems.length} | Queue: 0. Forcing Sync...`);
            
            // v1.46.001 COORDINATION
            if (window.FHB && window.FHB.stage === 0) {
                window.FHB.forceEmergencyHydration();
            } else if (typeof syncQueueWithLibrary === 'function') {
                syncQueueWithLibrary();
            }
        }

        // DOM Rendering Watchdog
        const renderTarget = document.getElementById('active-queue-list-render-target-warteschlange');
        const hasItemsInState = (typeof currentPlaylist !== 'undefined' && currentPlaylist.length > 0);
        
        if (renderTarget && hasItemsInState && renderTarget.children.length === 0) {
            console.error("[NUCLEAR-PULSE] RENDERING BLACKOUT. Queue has items but DOM is empty. Forcing Render...");
            if (typeof renderAudioQueue === 'function') {
                renderAudioQueue();
            }
        }
    },

    /**
     * Injects a pulsing red "RECOVERY MODE" badge.
     */
    injectRecoveryBadge() {
        // v1.46.01 Configuration Steering
        const config = window.CONFIG?.ui_settings?.technical_overlay;
        if (config && config.stable_mode_visible === false) {
            const existing = document.getElementById('recovery-mode-badge');
            if (existing) existing.remove();
            return;
        }

        let badge = document.getElementById('recovery-mode-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'recovery-mode-badge';
            const pos = config?.stable_mode_position || { top: 12, right: 280 };
            badge.style = `
                position: fixed; top: ${pos.top}px; right: ${pos.right}px; background: rgba(0, 255, 204, 0.2); 
                color: #00ffcc; border: 1px solid #00ffcc; padding: 4px 12px; 
                font-family: 'JetBrains Mono', monospace; font-size: 10px; 
                font-weight: 900; z-index: 999999; border-radius: 4px; pointer-events: none;
                transition: top 0.3s ease, right 0.3s ease;
            `;
            document.body.appendChild(badge);
        }
        badge.innerHTML = `⚡ STABLE MODE ACTIVE [${this.iterations}]`;
    },

    /**
     * Injects high-visibility text markers into the specific splits.
     */
    injectForensicAnchor() {
        const config = window.CONFIG?.ui_settings?.technical_overlay;
        
        // Master override: If global forensic anchors are hidden
        if (config && config.forensic_anchors_visible === false) {
            ['proof-deck-tag', 'proof-queue-tag'].forEach(id => {
                const el = document.getElementById(id);
                if (el) el.remove();
            });
            return;
        }

        const deck = document.getElementById('player-deck-column');
        const queue = document.getElementById('player-playlist-column');

        /**
         * create (v1.46.02 Extension)
         * Rebuilds or updates technical proof tags based on config.
         */
        const create = (id, label, color, posObj, parent, visible) => {
            if (!parent || visible === false) {
                const existing = document.getElementById(id);
                if (existing) existing.remove();
                return;
            }

            let tag = document.getElementById(id);
            if (!tag) {
                tag = document.createElement('div');
                tag.id = id;
                tag.className = 'forensic-proof-tag pulse-indicator';
                parent.style.position = 'relative';
                parent.appendChild(tag);
            }

            // Calculate coordinates (Support for both absolute units and defaults)
            const top = posObj?.top !== undefined ? `${posObj.top}px` : '5px';
            const left = posObj?.left !== undefined ? `${posObj.left}px` : 'auto';
            const right = posObj?.right !== undefined ? `${posObj.right}px` : 'auto';

            tag.style = `
                position: absolute; 
                top: ${top}; 
                left: ${left}; 
                right: ${right}; 
                background: ${color}; 
                color: #000; 
                font-family: 'JetBrains Mono', monospace; 
                font-size: 9px; 
                font-weight: 900; 
                padding: 1px 6px; 
                z-index: 99999; 
                border-radius: 2px; 
                opacity: 0.6;
                box-shadow: 0 2px 4px rgba(0,0,0,0.3);
                pointer-events: none;
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            `;
            tag.innerHTML = `${label} [${this.iterations}]`;
        };

        // Create/Update Deck and Queue Tags independently
        create('proof-deck-tag', 'DECK-LIFT', '#2ecc71', config?.deck_tag_position, deck, config?.deck_tag_visible);
        create('proof-queue-tag', 'QUEUE-LIFT', '#e67e22', config?.queue_tag_position, queue, config?.queue_tag_visible);
        
        // Remove the legacy global bar if it exists
        const globalBar = document.getElementById('nuclear-forensic-anchor');
        if (globalBar) globalBar.remove();
    },

    /**
     * Logs to centralized monitor.
     */
    auditLog(msg, type = 'info') {
        const dashboard = document.getElementById('sentinel-log-container-main') || document.getElementById('hydration-audit-logs');
        if (dashboard) {
            const timestamp = new Date().toLocaleTimeString();
            const color = type === 'error' ? '#ff3366' : '#00ffcc';
            const entry = `<div style="margin-bottom:2px;"><span style="opacity:0.3;">[${timestamp}]</span> <span style="color:${color};">NUCLEAR:</span> ${msg}</div>`;
            dashboard.innerHTML = entry + dashboard.innerHTML;
            if (dashboard.children.length > 30) dashboard.lastElementChild.remove();
        }
    }
};

// Start the Pulsar on Load
window.addEventListener('DOMContentLoaded', () => {
    NuclearPulsar.start();
});

window.NuclearPulsar = NuclearPulsar;
