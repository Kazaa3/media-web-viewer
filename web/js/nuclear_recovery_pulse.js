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
        console.log("%c[NUCLEAR-PULSE] DEEP SCAN MODE ACTIVE.", "color: #ff3131; font-weight: 900;");
        this.interval = setInterval(() => this.pulse(), 1000);
    },

    /**
     * The brute-force iteration pulse.
     */
    pulse() {
        if (!this.isActive) return;
        this.iterations++;

        // 1. PRIMARY PRIORITY: Proof of Life Badge
        this.injectRecoveryBadge();

        // 2. ULTRA-AGGRESSIVE DOM SWEEP
        const targets = document.querySelectorAll('#main-content-area, .tab-content.active, .player-view-container.active, #player-panel-container, #player-main-viewport');
        targets.forEach(el => {
            el.style.setProperty('display', 'flex', 'important');
            el.style.setProperty('visibility', 'visible', 'important');
            el.style.setProperty('opacity', '1', 'important');
            el.style.setProperty('min-height', '200px', 'important');
        });

        // 3. Child Visibility Pulse
        const splitContainer = document.getElementById('player-tab-split-container');
        if (splitContainer) {
            Array.from(splitContainer.children).forEach(child => {
                child.style.setProperty('display', 'flex', 'important');
                child.style.setProperty('visibility', 'visible', 'important');
            });
        }

        // 4. Split Anchors
        this.injectForensicAnchor();

        if (this.iterations % 5 === 0 && typeof eel !== 'undefined' && eel.log_spawn_event) {
            eel.log_spawn_event('recovery-pulse', `deep_scan_iter_${this.iterations}`);
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
                position: fixed; top: 10px; right: 151px; background: #ff3131; color: #fff;
                padding: 6px 16px; font-family: 'JetBrains Mono', monospace; font-size: 11px;
                font-weight: 900; z-index: 999999; border-radius: 4px; box-shadow: 0 0 20px rgba(255, 49, 49, 0.6);
                animation: recovery-pulse 0.8s infinite; pointer-events: none;
            `;
            const s = document.createElement('style');
            s.innerHTML = `@keyframes recovery-pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }`;
            document.head.appendChild(s);
            document.body.appendChild(badge);
        }
        badge.innerHTML = `☢️ EMERGENCY RECOVERY [${this.iterations}]`;
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
                tag.style = `position: absolute; ${pos}; background: ${color}; color: #000; font-family: monospace; font-size: 10px; font-weight: 900; padding: 2px 8px; z-index: 99999; border-radius: 2px;`;
                parent.style.position = 'relative';
                parent.appendChild(tag);
            }
            tag.innerHTML = `⚡ ${label} [${this.iterations}]`;
        };
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
