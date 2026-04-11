/**
 * Forensic Recovery Engine (v1.46.03)
 * Standalone module for forced DOM injection and viewport auditing.
 * Used for "Repair-First" orchestration when standard hydration fails.
 */

const ForensicRecovery = {
    /**
     * Force-injects a fragment or raw HTML into a target container.
     * Bypasses FragmentLoader to verify basic rendering health.
     */
    async forceForensicInjection(targetId, source, options = {}) {
        const timestamp = new Date().toLocaleTimeString();
        this.log(`[PULSE] Initiating Force Injection on #${targetId}...`);

        const container = document.getElementById(targetId);
        if (!container) {
            this.log(`[ERROR] Target #${targetId} NOT FOUND. Recovery Aborted.`, 'error');
            return false;
        }

        try {
            // 1. Audit Current State
            const style = window.getComputedStyle(container);
            this.log(`[AUDIT] Current State: display=${style.display}, visibility=${style.visibility}, opacity=${style.opacity}`);

            // 2. Prepare Container
            container.innerHTML = `<div class="forensic-pulse-loader" style="padding: 20px; color: #ff9500; font-family: monospace;">[PULSE] REBUILDING...</div>`;
            container.style.display = options.display || 'flex';
            container.style.opacity = '1';

            // 3. Fetch or Inject Content
            let content = "";
            if (source.includes('.html')) {
                this.log(`[FETCH] Loading remote fragment: ${source}`);
                const response = await fetch(source);
                content = await response.text();
            } else {
                this.log(`[INJECT] Using raw manual content.`);
                content = source;
            }

            // 4. Force Swap
            container.innerHTML = content;
            this.log(`[SUCCESS] Content swapped. Bytes: ${content.length}`);

            // 5. Execute Scripts (Manual Discovery)
            const scripts = container.querySelectorAll('script');
            this.log(`[SCRIPTS] Found ${scripts.length} pulse-scripts. Executing...`);
            scripts.forEach((oldScript) => {
                const newScript = document.createElement("script");
                Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                newScript.appendChild(document.createTextNode(oldScript.innerHTML));
                oldScript.parentNode.replaceChild(newScript, oldScript);
            });

            // 6. Liveness Heartbeat
            setTimeout(() => {
                const liveness = container.querySelector('[data-liveness="ready"]') ? 'READY' : 'PENDING';
                this.log(`[HEARTBEAT] Liveness Signal: ${liveness}`, liveness === 'READY' ? 'success' : 'warn');
                if (liveness === 'READY') {
                    container.style.border = "2px solid #2ecc7133"; // Visual Confirmation
                }
            }, 500);

            return true;
        } catch (err) {
            this.log(`[CRITICAL] Injection Failed: ${err.message}`, 'error');
            return false;
        }
    },

    /**
     * Centralized logging to console and UI status dashboard.
     */
    log(msg, type = 'info') {
        const colors = {
            'info': '#00ffcc',
            'error': '#ff3366',
            'warn': '#ff9500',
            'success': '#2ecc71'
        };
        const color = colors[type] || colors.info;
        const timestamp = new Date().toLocaleTimeString();

        // Console output
        console.log(`%c[FORENSIC-RECOVERY] ${msg}`, `color: ${color}; font-weight: bold;`);

        // UI Dashboard Mirroring
        const dashboard = document.getElementById('sentinel-log-container-main') || document.getElementById('hydration-audit-logs');
        if (dashboard) {
            const entry = document.createElement('div');
            entry.style.marginBottom = '4px';
            entry.innerHTML = `<span style="opacity:0.4;">[${timestamp}]</span> <span style="color:${color}; font-weight:800;">${msg}</span>`;
            dashboard.prepend(entry);
        }
    }
};

window.ForensicRecovery = ForensicRecovery;
window.FR = ForensicRecovery; // Global Shorthand
