/**
 * fragment_loader.js - Dynamically loads HTML fragments into the DOM.
 * Supports caching and post-load initialization hooks.
 */

const FragmentLoader = {
    cache: new Map(),
    pendingLoads: new Map(), // Track in-flight requests (targetId -> Promise)

    /**
     * loadAtomic (v1.46.01 Upgrade)
     * Performs a 'True Atomic' shadow swap. Fetches HTML, injects into shadow stage,
     * executes scripts, waits for liveness marker [data-liveness="ready"],
     * and only then performs the DOM swap.
     */
    async loadAtomic(targetId, fragmentPath, callback) {
        const container = document.getElementById(targetId);
        if (!container) return;

        console.info(`[FL] ATOMIC START: ${fragmentPath} -> #${targetId}`);

        // 1. Create Shadow Stage (if missing)
        let shadow = document.getElementById('shadow-stage-buffer');
        if (!shadow) {
            shadow = document.createElement('div');
            shadow.id = 'shadow-stage-buffer';
            shadow.style.display = 'none';
            document.body.appendChild(shadow);
        }

        // Keep current view visible but slightly dimmed during prep
        container.style.opacity = '0.6';
        container.style.transition = 'opacity 0.3s ease';
        
        try {
            // 2. Fetch HTML
            let html;
            if (this.cache.has(fragmentPath)) {
                html = this.cache.get(fragmentPath);
            } else {
                const response = await fetch(fragmentPath);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                html = await response.text();
                this.cache.set(fragmentPath, html);
            }

            if (!html || html.trim() === "") throw new Error("Empty Fragment");

            // 3. Shadow Prep
            shadow.innerHTML = html;
            shadow.dataset.fragment = fragmentPath;
            shadow.dataset.liveness = 'pending';

            // 4. [v1.46.01] SCRIPT RECLAMATION (Execute scripts in shadow context)
            const scripts = shadow.querySelectorAll('script');
            scripts.forEach(oldScript => {
                const newScript = document.createElement('script');
                Array.from(oldScript.attributes).forEach(attr => newScript.setAttribute(attr.name, attr.value));
                if (oldScript.textContent) newScript.textContent = oldScript.textContent;
                document.head.appendChild(newScript);
                document.head.removeChild(newScript);
            });

            // 5. [v1.46.01] WAIT FOR HYDRATION (Liveness Polling)
            // We wait up to 3 seconds for the scripts to set [data-liveness="ready"]
            const startTime = Date.now();
            const POLL_TIMEOUT = 3000;
            
            const waitForReady = () => new Promise((resolve) => {
                const check = () => {
                    const isReady = shadow.querySelector('[data-liveness="ready"]') !== null || shadow.dataset.liveness === 'ready';
                    const elapsed = Date.now() - startTime;
                    
                    if (isReady) {
                        console.info(`[FL] ATOMIC HYDRATION READY after ${elapsed}ms`);
                        resolve(true);
                    } else if (elapsed > POLL_TIMEOUT) {
                        console.warn(`[FL] ATOMIC HYDRATION TIMEOUT (${fragmentPath}). Swapping anyway...`);
                        resolve(false);
                    } else {
                        requestAnimationFrame(check);
                    }
                };
                check();
            });

            await waitForReady();

            // 6. ATOMIC SWAP
            container.innerHTML = shadow.innerHTML;
            container.dataset.loaded = 'true';
            container.style.opacity = '1';
            
            // Cleanup Shadow
            shadow.innerHTML = '';
            
            console.info(`[FL] ATOMIC SWAP COMPLETE (#${targetId})`);
            if (callback) callback();
        } catch (e) {
            this.error(targetId, fragmentPath, e);
        }
    },

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

            if (typeof traceUiNav === 'function') traceUiNav('HYDRATION', 'START', { path: fragmentPath, targetId });

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

            if (typeof traceUiNav === 'function') traceUiNav('HYDRATION', 'SUCCESS', { path: fragmentPath, targetId });
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

            if (typeof mwv_trace === 'function') {
                mwv_trace('FRAGMENT', 'EXECUTION-COMPLETE', { path: fragmentPath, targetId });
            }

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
        if (typeof traceUiNav === 'function') traceUiNav('HYDRATION', 'ERROR', { path: fragmentPath, error: err.message || err });
        if (typeof mwv_trace === 'function') mwv_trace('FRAGMENT', 'ERROR', { path: fragmentPath, error: err.message || err });
        
        const fragName = fragmentPath.split('/').pop().replace('.html', '');
        if (typeof window.auditFragmentHydration === 'function') {
            window.auditFragmentHydration(fragName, 'error', err.message);
        }

        // --- [v1.41.161/163] AUTO-RESCUE FAILOVER ---
        const rescueEnabled = window.CONFIG?.ui_settings?.enable_rescue_failover !== false;
        if (rescueEnabled && fragmentPath !== 'fragments/diagnostic_rescue.html') {
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

// Created with MWV v1.46.00-MASTER
