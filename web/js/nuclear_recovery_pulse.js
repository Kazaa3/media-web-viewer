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
        this.interval = setInterval(() => this.pulse(), 1000);
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

        // 2. Pulse Indicators
        this.injectRecoveryBadge();
        this.injectForensicAnchor();

        if (this.iterations % 10 === 0 && typeof eel !== 'undefined' && eel.log_spawn_event) {
            eel.log_spawn_event('recovery-pulse', `surgical_pulse_iter_${this.iterations}`);
        }
    },

    /**
     * Injects a pulsing red "RECOVERY MODE" badge.
     */
    injectRecoveryBadge() {
        let badge = document.getElementById('recovery-mode-badge');
        if (!badge) {
            badge = document.createElement('div');
            badge.id = 'recovery-mode-badge';
            badge.style = `
                position: fixed; top: 12px; right: 280px; background: rgba(0, 255, 204, 0.2); 
                color: #00ffcc; border: 1px solid #00ffcc; padding: 4px 12px; 
                font-family: 'JetBrains Mono', monospace; font-size: 10px; 
                font-weight: 900; z-index: 999999; border-radius: 4px; pointer-events: none;
            `;
            document.body.appendChild(badge);
        }
        badge.innerHTML = `⚡ STABLE MODE ACTIVE [${this.iterations}]`;
    },

    /**
     * Injects high-visibility text markers into the specific splits.
     */
    injectForensicAnchor() {
        const deck = document.getElementById('player-deck-column');
        const queue = document.getElementById('player-playlist-column');
        const create = (id, label, color, pos, parent) => {
            if (!parent) return;
            let tag = document.getElementById(id);
            if (!tag) {
                tag = document.createElement('div');
                tag.id = id;
                tag.style = `position: absolute; ${pos}; background: ${color}; color: #000; font-family: monospace; font-size: 9px; font-weight: 800; padding: 1px 6px; z-index: 99999; border-radius: 2px; opacity: 0.6;`;
                parent.style.position = 'relative';
                parent.appendChild(tag);
            }
            tag.innerHTML = `${label} [${this.iterations}]`;
        };
        create('proof-deck-tag', 'DECK-LIFT', '#2ecc71', 'top: 5px; left: 5px;', deck);
        create('proof-queue-tag', 'QUEUE-LIFT', '#e67e22', 'top: 5px; right: 5px;', queue);
        
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
