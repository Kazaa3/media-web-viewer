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
        
        console.log("%c[NUCLEAR-PULSE] ACTIVATING... Iterating every 1000ms.", "color: #ff3366; font-weight: 900; background: #000; padding: 5px;");
        
        this.interval = setInterval(() => {
            this.pulse();
        }, 1000);
    },

    /**
     * The brute-force iteration pulse.
     */
    pulse() {
        if (!this.isActive) return;
        this.iterations++;

        // 1. Audit and Force ALL content areas
        const targets = ['player-panel-container', 'player-main-viewport', 'rebuild-stage', 'main-content-area'];
        targets.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                this.shoutAtElement(el);
                this.forceRecursiveFlex(el);
            }
        });

        // 2. Localized Split Visibility
        const deck = document.getElementById('player-deck-column');
        const queue = document.getElementById('player-playlist-column');
        if (deck) this.shoutAtElement(deck);
        if (queue) this.shoutAtElement(queue);

        // 3. Inject Recovery Badge (Global Visibility Indicator)
        this.injectRecoveryBadge();

        // 4. Inject Forensic Anchors
        this.injectForensicAnchor();

        if (this.iterations % 10 === 0 && typeof eel !== 'undefined' && eel.log_spawn_event) {
            eel.log_spawn_event('recovery-pulsar', `ultra_pulse_active_iter_${this.iterations}`);
        }
    },

    /**
     * Deep recursion to force flex layout on all children.
     */
    forceRecursiveFlex(root) {
        if (!root) return;
        const children = root.children;
        for (let i = 0; i < children.length; i++) {
            const child = children[i];
            if (child.classList.contains('player-view-container') || child.classList.contains('tab-content')) {
                if (child.classList.contains('active')) {
                    child.style.setProperty('display', 'flex', 'important');
                    child.style.setProperty('visibility', 'visible', 'important');
                    child.style.setProperty('opacity', '1', 'important');
                }
            }
            if (child.id === 'player-tab-split-container' || child.id === 'player-main-viewport') {
                this.forceRecursiveFlex(child);
            }
        }
    },

    /**
     * Forces standard visibility properties using !important.
     */
    shoutAtElement(el) {
        if (!el) return;
        
        // CSS Brute-Force
        if (el.classList.contains('active') || el.id === 'main-content-area' || el.id.includes('panel-container')) {
            el.style.setProperty('display', 'flex', 'important');
        }
        el.style.setProperty('visibility', 'visible', 'important');
        el.style.setProperty('opacity', '1', 'important');
        
        // Ensure dimensions for root containers
        if (el.id === 'main-content-area' || el.id.includes('viewport')) {
            el.style.setProperty('height', '100%', 'important');
            el.style.setProperty('width', '100%', 'important');
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
                position: fixed;
                top: 60px;
                right: 20px;
                background: #ff3366;
                color: #fff;
                padding: 5px 15px;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                font-weight: 900;
                z-index: 999999;
                border-radius: 20px;
                box-shadow: 0 0 20px rgba(255, 51, 102, 0.5);
                animation: recovery-pulse 1.5s infinite;
                pointer-events: none;
            `;
            
            const style = document.createElement('style');
            style.innerHTML = `
                @keyframes recovery-pulse {
                    0% { transform: scale(1); opacity: 1; }
                    50% { transform: scale(1.1); opacity: 0.7; }
                    100% { transform: scale(1); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
            document.body.appendChild(badge);
        }
        badge.innerHTML = `☢️ RECOVERY MODE ACTIVE [${this.iterations}]`;
    },

    /**
     * Injects high-visibility text markers into the specific splits.
     */
    injectForensicAnchor(container) {
        // [v1.46.05] Localized Splits Detection
        const deck = document.getElementById('player-deck-column');
        const queue = document.getElementById('player-playlist-column');

        const createSplitTag = (id, label, color, position) => {
            let tag = document.getElementById(id);
            if (!tag) {
                tag = document.createElement('div');
                tag.id = id;
                tag.style = `
                    position: absolute;
                    ${position};
                    background: ${color};
                    color: #000;
                    font-family: 'JetBrains Mono', monospace;
                    font-size: 9px;
                    font-weight: 900;
                    padding: 2px 8px;
                    z-index: 100002;
                    border-radius: 4px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.5);
                    pointer-events: none;
                `;
                const parent = (id === 'proof-split-deck') ? deck : queue;
                if (parent) {
                    if (window.getComputedStyle(parent).position === 'static') parent.style.position = 'relative';
                    parent.appendChild(tag);
                }
            }
            if (tag) {
                tag.innerHTML = `⚡ ${label} [${this.iterations}]`;
            }
        };

        if (deck) createSplitTag('proof-deck-tag', 'FORENSIC-DECK', '#2ecc71', 'top: 10px; left: 10px;');
        if (queue) createSplitTag('proof-queue-tag', 'FORENSIC-QUEUE', '#e67e22', 'top: 10px; right: 10px;');

        // Standard diagnostic heartbeats (v1.46.06 Integrated)
        if (this.iterations % 10 === 0 && typeof eel !== 'undefined' && eel.log_spawn_event) {
            eel.log_spawn_event('diagnostic-pulsar', `pulsing_active_iter_${this.iterations}`);
        }

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
