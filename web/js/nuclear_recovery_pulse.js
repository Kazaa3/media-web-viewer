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

        // 1. Audit and Force Parent Chain
        const targetId = 'rebuild-stage';
        const target = document.getElementById(targetId);
        
        if (target) {
            this.shoutAtElement(target);
            this.ensureParentVisibility(target);
            
            // 2. Inject Forced Status Anchor (Proof of Life)
            this.injectForensicAnchor(target);
            
            if (this.iterations % 5 === 0) {
                this.auditLog(`NUCLEAR SHOUT [${this.iterations}] - Viewport Health: OK`);
            }
        } else {
            this.auditLog(`CRITICAL: #${targetId} NOT FOUND IN DOM`, 'error');
        }
    },

    /**
     * Forces standard visibility properties using !important.
     */
    shoutAtElement(el) {
        if (!el) return;
        
        // CSS Brute-Force
        el.style.setProperty('display', 'flex', 'important');
        el.style.setProperty('visibility', 'visible', 'important');
        el.style.setProperty('opacity', '1', 'important');
        el.style.setProperty('z-index', '999', 'important');
        
        // Ensure dimensions
        if (el.id === 'rebuild-stage') {
            el.style.setProperty('height', '100%', 'important');
            el.style.setProperty('width', '100%', 'important');
            el.style.setProperty('flex', '1', 'important');
        }
    },

    /**
     * Recursively shouts at all parents to ensure a visible path to root.
     */
    ensureParentVisibility(el) {
        let parent = el.parentElement;
        while (parent && parent.tagName !== 'BODY') {
            // Some parents (like split-containers) MUST be flex
            if (parent.classList.contains('main-split-container') || parent.id === 'main-content-area') {
                parent.style.setProperty('display', 'flex', 'important');
            } else {
                // Generic visible path
                if (window.getComputedStyle(parent).display === 'none') {
                    parent.style.setProperty('display', 'block', 'important');
                }
            }
            parent.style.setProperty('visibility', 'visible', 'important');
            parent.style.setProperty('opacity', '1', 'important');
            parent = parent.parentElement;
        }
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
