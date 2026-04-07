/**
 * fragment_loader.js - Dynamically loads HTML fragments into the DOM.
 * Supports caching and post-load initialization hooks.
 */

const FragmentLoader = {
    cache: new Map(),
    pendingLoads: new Map(), // Track in-flight requests (targetId -> Promise)

    /**
     * Loads an external HTML fragment into a container.
     * @param {string} targetId - The ID of the container element.
     * @param {string} fragmentPath - The path to the .html fragment.
     * @param {Function} callback - Optional callback after loading.
     */
    async load(targetId, fragmentPath, callback) {
        // --- v1.35 In-Flight Guard ---
        const pendingKey = `${targetId}:${fragmentPath}`;
        if (this.pendingLoads.has(pendingKey)) {
            console.debug(`[FL] Awaiting in-flight load: ${pendingKey}`);
            const result = await this.pendingLoads.get(pendingKey);
            if (callback) callback();
            return result;
        }

        const loadPromise = this._executeLoad(targetId, fragmentPath, callback);
        this.pendingLoads.set(pendingKey, loadPromise);

        try {
            return await loadPromise;
        } finally {
            this.pendingLoads.delete(pendingKey);
        }
    },

    async _executeLoad(targetId, fragmentPath, callback) {
        const container = document.getElementById(targetId);
        if (!container) {
            console.error(`[FragmentLoader] Container #${targetId} not found.`);
            return;
        }

        // --- v1.35 Path Sanitization ---
        // Ensure fragment paths are correctly relative to the web root.
        if (fragmentPath.startsWith('/')) fragmentPath = fragmentPath.substring(1);

        // Return if already loaded (unless we want to force reload)
        if (container.dataset.loaded === 'true') {
            if (callback) callback();
            return;
        }

        try {
            // [v1.37.47 Audit Bridge]
            const fragName = fragmentPath.split('/').pop().replace('.html', '');
            if (typeof window.auditFragmentHydration === 'function') {
                window.auditFragmentHydration(fragName, 'loading', fragmentPath);
            }

            console.log(`[FragmentLoader] Loading fragment: ${fragmentPath}`);
            let html;

            if (this.cache.has(fragmentPath)) {
                html = this.cache.get(fragmentPath);
            } else {
                const response = await fetch(fragmentPath);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                html = await response.text();
                this.cache.set(fragmentPath, html);
                if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'STAGE-1', { path: fragmentPath, status: 'fetched' });
                console.info(`[FL] STAGE 1: HTML Received (${fragmentPath})`);
            }

            if (!html || html.trim() === '') {
                throw new Error("Fragment content is empty or whitespace only.");
            }

            container.innerHTML = html;
            container.dataset.loaded = 'true';
            
            // [v1.37.47 Audit Bridge Success]
            if (typeof window.auditFragmentHydration === 'function') {
                const fragName = fragmentPath.split('/').pop().replace('.html', '');
                window.auditFragmentHydration(fragName, 'success');
            }

            if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'STAGE-2', { path: fragmentPath, targetId });
            console.info(`[FL] STAGE 2: DOM Injection Complete (#${targetId})`);

            // --- V1.34 Master: Manual Script Extraction & Execution ---
            const scripts = container.querySelectorAll('script');
            if (scripts.length > 0) {
                if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'STAGE-3', { path: fragmentPath, count: scripts.length });
                console.info(`[FL] STAGE 3: Processing ${scripts.length} internal scripts...`);
            }
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                
                // Copy all attributes (src, async, defer, type, etc.)
                Array.from(oldScript.attributes).forEach(attr => {
                    newScript.setAttribute(attr.name, attr.value);
                });

                // Copy internal content if not a src-based script
                if (oldScript.textContent) {
                    newScript.textContent = oldScript.textContent;
                }

                // Append and immediately remove to clean up DOM (execution still happens)
                document.head.appendChild(newScript);
                document.head.removeChild(newScript);
            });

            // Trigger translations for the new content
            if (typeof initTranslations === 'function') {
                initTranslations();
            }

            // Trigger splitters if any
            if (typeof initAllSplitters === 'function') {
                initAllSplitters();
            }

            if (callback) callback();
            if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'STAGE-4', { path: fragmentPath, status: 'ready' });
            console.info(`[FL] STAGE 4: Final READY (${fragmentPath})`);
            
            // Dispatch a custom event for module-specific listeners
            const event = new CustomEvent('fragmentLoaded', { 
                detail: { targetId, fragmentPath } 
            });
            document.dispatchEvent(event);

        } catch (error) {
            this.error(targetId, fragmentPath, error);
        }
    },

    /**
     * Error Feedback (v1.35)
     * Provides visual feedback in the viewport if a fragment cannot be reached.
     */
    error(targetId, fragmentPath, err) {
        console.error(`[FragmentLoader] Failed to load ${fragmentPath}:`, err);
        if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'ERROR', { path: fragmentPath, error: err.message || err });
        
        // --- v1.35 Safety: Release Global Navigation Lock ---
        if (typeof isNavigating !== 'undefined') {
            isNavigating = false;
            document.body.style.cursor = 'default';
        }

        const msg = `
            <div class="error-panel" style="padding: 40px; text-align: center; color: var(--text-primary); background: rgba(255, 0, 0, 0.05); border-radius: 12px; border: 1px dashed rgba(255, 0, 0, 0.3); margin: 20px; backdrop-filter: blur(10px);">
                <div style="font-size: 2.5rem; margin-bottom: 15px;">⚠️</div>
                <h2 style="margin-bottom: 10px; color: var(--accent-color, #e74c3c);">Fragment Load Failure</h2>
                <p>The UI module at <code>${fragmentPath}</code> could not be rendered.</p>
                <p style="opacity: 0.7; font-size: 0.9rem; margin-top: 15px;">Reason: ${err.message || err}</p>
                <button class="nav-btn active" style="margin-top: 20px; padding: 10px 20px; border-radius: 20px;" onclick="location.reload()">Retry Application Reload</button>
            </div>`;
        
        if (typeof safeHtml === 'function') {
            safeHtml(targetId, msg);
        } else {
            const container = document.getElementById(targetId);
            if (container) container.innerHTML = msg;
        }
    }
};

// Global accessor
window.FragmentLoader = FragmentLoader;
