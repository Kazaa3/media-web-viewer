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
            
            // --- v1.41.160 WILL_SPAWN Event ---
            if (typeof window.auditFragmentHydration === 'function') {
                window.auditFragmentHydration(fragName, 'will_spawn', fragmentPath, targetId);
            }

            console.log(`[FragmentLoader] Loading fragment: ${fragmentPath}`);
            let html;
            
            // ... (rest of loading logic)
            if (this.cache.has(fragmentPath)) {
                html = this.cache.get(fragmentPath);
            } else {
                // --- [v1.41.141] Forensic Timeout Guard ---
                const controller = new AbortController();
                const timeoutId = setTimeout(() => {
                    controller.abort();
                    console.error(`[FL] CRITICAL: Fragment FETCH TIMEOUT after 3500ms (${fragmentPath})`);
                }, 3500);

                try {
                    const response = await fetch(fragmentPath, { signal: controller.signal });
                    clearTimeout(timeoutId);
                    
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    html = await response.text();
                    this.cache.set(fragmentPath, html);
                    if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'STAGE-1', { path: fragmentPath, status: 'fetched' });
                    console.info(`[FL] STAGE 1: HTML Received (${fragmentPath})`);
                } catch (fetchErr) {
                    clearTimeout(timeoutId);
                    throw fetchErr;
                }
            }

            if (!html || html.trim() === '') {
                throw new Error("Fragment content is empty or whitespace only.");
            }

            container.innerHTML = html;
            container.dataset.loaded = 'true';
            
            // [v1.37.47 Audit Bridge Success]
            if (typeof window.auditFragmentHydration === 'function') {
                window.auditFragmentHydration(fragName, 'success', fragmentPath, targetId);
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
     * Localized Visual Integrity Test (v1.41.160)
     * Hard-writes integrity info into a specific container.
     */
    injectLocalizedIntegrityTest(targetId) {
        const container = document.getElementById(targetId);
        if (!container) return;
        
        console.warn(`[DIAGNOSTICS] Injecting Localized Integrity Test into #${targetId}`);
        
        container.style.position = 'relative';
        container.innerHTML = `
            <div style="width:100%; height:100%; display:flex; flex-direction:column; align-items:center; justify-content:center; background:rgba(0,255,153,0.1); border:2px dashed #00ff99; box-sizing:border-box; color:#00ff99; font-family:'JetBrains Mono', monospace; padding:20px; text-align:center;">
                <div style="font-size:24px; font-weight:900; margin-bottom:10px;">LOCAL INTEGRITY OK</div>
                <div style="font-size:10px; opacity:0.7; letter-spacing:1px; margin-bottom:20px;">CONTAINER: #${targetId}</div>
                <div style="font-size:14px; font-weight:700; background:rgba(0,0,0,0.4); padding:5px 15px; border-radius:30px;">
                    ${new Date().toLocaleTimeString()}
                </div>
                <button onclick="this.parentElement.remove(); document.getElementById('${targetId}').dataset.loaded='false';" 
                    style="margin-top:20px; background:transparent; border:1px solid #00ff99; color:#00ff99; padding:5px 15px; border-radius:4px; font-size:10px; cursor:pointer;">
                    CLEAR TEST
                </button>
            </div>
        `;
    },

    /**
     * Error Feedback (v1.35)
     * Provides visual feedback in the viewport if a fragment cannot be reached.
     */
    error(targetId, fragmentPath, err) {
        console.error(`[FragmentLoader] Failed to load ${fragmentPath}:`, err);
        if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'ERROR', { path: fragmentPath, error: err.message || err });
        
        const fragName = fragmentPath.split('/').pop().replace('.html', '');
        if (typeof window.auditFragmentHydration === 'function') {
            window.auditFragmentHydration(fragName, 'error', err.message);
        }

        // --- [v1.41.161] AUTO-RESCUE FAILOVER ---
        if (fragmentPath !== 'fragments/diagnostic_rescue.html') {
            console.warn(`[FragmentLoader] TRIGGERING AUTO-RESCUE for #${targetId} (Source: ${fragmentPath})`);
            this._executeLoad(targetId, 'fragments/diagnostic_rescue.html');
            return;
        }
        
        // --- v1.35 Safety: Release Global Navigation Lock ---
        if (typeof isNavigating !== 'undefined') {
            isNavigating = false;
            document.body.style.cursor = 'default';
        }

        const msg = `
            <div class="error-panel" style="padding: 40px; text-align: center; color: var(--text-primary); background: rgba(255, 0, 0, 0.05); border-radius: 12px; border: 1px dashed rgba(255, 0, 0, 0.3); margin: 20px; backdrop-filter: blur(10px);">
                <div style="font-size: 2.5rem; margin-bottom: 15px;">⚠️</div>
                <h2 style="margin-bottom: 10px; color: var(--accent-color, #e74c3c);">Critical Rescue Failure</h2>
                <p>The Rescue UI at <code>${fragmentPath}</code> also failed.</p>
                <p style="opacity: 0.7; font-size: 0.9rem; margin-top: 15px;">Reason: ${err.message || err}</p>
                <button class="nav-btn active" style="margin-top: 20px; padding: 10px 20px; border-radius: 20px;" onclick="location.reload()">Emergency Reload</button>
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
