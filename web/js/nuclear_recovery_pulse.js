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
     * Injects a high-visibility text marker into the viewport top.
     */
    injectForensicAnchor(container) {
        let anchor = document.getElementById('nuclear-forensic-anchor');
        if (!anchor) {
            anchor = document.createElement('div');
            anchor.id = 'nuclear-forensic-anchor';
            anchor.style = `
                position: absolute;
                top: 0; left: 0; right: 0;
                background: linear-gradient(to right, #ff3366, #ff9500);
                color: white;
                font-family: 'JetBrains Mono', monospace;
                font-size: 10px;
                font-weight: 800;
                padding: 4px 15px;
                z-index: 100001;
                pointer-events: none;
                display: flex;
                justify-content: space-between;
                box-shadow: 0 4px 10px rgba(0,0,0,0.3);
            `;
            container.appendChild(anchor);
        }
        const activeTab = document.body.getAttribute('data-mwv-tab') || 'unknown';
        anchor.innerHTML = `
            <span>☢️ NUCLEAR RECOVERY PULSE ACTIVE</span>
            <span>V1.46.04 | TAB: ${activeTab.toUpperCase()} | PULSE: ${this.iterations}</span>
        `;
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
