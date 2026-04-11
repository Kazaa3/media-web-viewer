/**
 * Forensic Window Manager (v1.37.52)
 * Centralized tracking and coordination for all UI viewports and fragments.
 * (v1.37.52 Master Rebuild starting with Audio Player)
 */

const WindowManager = {
    activeWindow: null,
    windows: new Map(), // name -> { shellId, fragmentId, fragmentPath, status, healthy, lastTick }
    onWindowChanged: null,

    /**
     * Registers a UI window/tab with the tracker.
     */
    register(name, config) {
        this.windows.set(name, {
            shellId: config.shellId,
            fragmentId: config.fragmentId || null,
            fragmentPath: config.fragmentPath || null,
            status: 'initialized',
            healthy: false,
            lastTick: Date.now(),
            onActivate: config.onActivate || null,
            onHydrate: config.onHydrate || null
        });
        console.log(`[WM] Registered forensic tracker for window: ${name}`);
        
        // Trigger initial audit bridge entry
        if (typeof window.auditFragmentHydration === 'function') {
            window.auditFragmentHydration(name, 'pending', config.fragmentPath || 'No Fragment');
        }
        if (typeof mwv_trace === 'function') {
            mwv_trace('WM', 'REGISTER', { name, fragmentId: config.fragmentId });
        }
    },

    /**
     * Activates a window, handles fragment loading, and updates the forensic audit trail.
     */
    async activate(name, force = false) {
        const win = this.windows.get(name);
        if (!win) {
            console.error(`[WM] CRITICAL: Attempted to activate untracked window: ${name}`);
            return false;
        }

        if (this.activeWindow === name && !force) {
            console.log(`[WM] Window ${name} already active. Skipping activation.`);
            return true;
        }

        console.info(`[WM] Stage 1: Activating ${name.toUpperCase()} (Shell: #${win.shellId})`);
        
        // 0. Update transition state
        document.body.style.cursor = 'wait';
        this.updateStatus(name, 'hydrating');
        
        if (typeof mwv_trace === 'function') {
            mwv_trace('WM', 'ACTIVATE-START', { name, force });
        }

        try {
            // [v1.45] FORENSIC STAGE REDIRECTION (Support for rebuild & test_ref)
            const evoMode = window.GLOBAL_CONFIG?.ui_evolution_mode || 'stable';
            const isRebuildMode = (evoMode === 'rebuild' || evoMode === 'test_ref');
            const stage = document.getElementById('rebuild-stage');

            if (isRebuildMode && stage && win.fragmentPath) {
                console.info(`[WM] REBUILD_MODE: Routing ${name} to Unified Stage...`);
                
                // Hide legacy shells
                this._hideAllShells();
                
                // Show and load stage
                stage.style.display = 'flex';
                stage.classList.add('active');
                
                // Atomic Fragment Load (v1.44)
                if (typeof FragmentLoader.loadAtomic === 'function') {
                    await FragmentLoader.loadAtomic('rebuild-stage', win.fragmentPath);
                } else {
                    await FragmentLoader.load('rebuild-stage', win.fragmentPath);
                }
                
                if (win.onHydrate) win.onHydrate();
            } else {
                // --- LEGACY STABLE PATH ---
                // 1. Hydrate Fragment if required
                if (win.fragmentId && win.fragmentPath) {
                    const container = document.getElementById(win.fragmentId);
                    const needsLoad = !container || container.getAttribute('data-loaded') !== 'true' || force;

                    if (needsLoad) {
                        console.info(`[WM] Stage 1.1: Loading fragment for ${name} -> ${win.fragmentPath}`);
                        await FragmentLoader.load(win.fragmentId, win.fragmentPath);
                        if (win.onHydrate) win.onHydrate();
                    }
                }

                // 2. Visibility Matrix Update (v1.41.116 Robust Refinement)
                this._hideAllShells();
                let shell = document.getElementById(win.shellId);
                if (!shell) {
                    // Fallback to domain lookup (v1.41.115 bridging)
                    shell = document.querySelector(`.tab-content[data-tab-domain="${name}"]`);
                    if (!shell) shell = document.querySelector(`.tab-content[data-tab-domain="media"]`);
                }

                if (shell) {
                    console.info(`[WM] Stage 1.2: Enforcing visibility on container: #${shell.id}`);
                    shell.style.display = 'flex';
                    shell.style.opacity = '1';
                    shell.classList.add('active');
                } else {
                    throw new Error(`Shell container #${win.shellId} not found in DOM.`);
                }
                if (win.onHydrate) win.onHydrate();
            }

            // [v1.45] MANDATORY HYDRATION HANDSHAKE
            if (typeof window.triggerModuleHydration === 'function') {
                await window.triggerModuleHydration(name);
            }

            // [v1.37.52] Force Global UI Logic Sync
            const categoryMap = { 'player': 'media', 'library': 'library', 'editor': 'edit', 'database': 'database' };
            const cat = categoryMap[name] || 'media';
            if (typeof refreshUIVisibility === 'function') refreshUIVisibility(cat);

            // 3. Mark as Healthy & Active
            this.activeWindow = name;
            this.updateStatus(name, 'success', { healthy: true, msg: 'Active & Tracked' });
            
            // 4. Trigger Post-Activation Logic
            if (win.onActivate) win.onActivate();
            
            // 5. Fire Global Event for other modules
            if (this.onWindowChanged) this.onWindowChanged(name);
            
            console.info(`[WM] Stage 2: ${name.toUpperCase()} Confirmed Healthy.`);
            return true;

        } catch (err) {
            console.error(`[WM] CRITICAL FAILURE while activating ${name}:`, err);
            this.updateStatus(name, 'error', { healthy: false, msg: err.message });
            return false;
        } finally {
            document.body.style.cursor = 'default';
        }
    },

    /**
     * Updates the status and health of a window in the registry.
     */
    updateStatus(name, status, details = {}) {
        const win = this.windows.get(name);
        if (win) {
            win.status = status;
            win.lastTick = Date.now();
            if (details.healthy !== undefined) win.healthy = details.healthy;
            
            // Sync with the visual Hydration Auditor in the sidebar
            if (typeof window.auditFragmentHydration === 'function') {
                window.auditFragmentHydration(name, status, details.msg || '');
            }
        }
    },

    /**
     * Internal: Resets all shell visibilities to avoid overlaps.
     */
    _hideAllShells() {
        document.querySelectorAll('.tab-content, .deck-view').forEach(el => {
            el.style.display = 'none';
            el.classList.remove('active');
        });
    },

    /**
     * Returns the current status of all tracked windows.
     */
    getAuditReport() {
        const report = {};
        this.windows.forEach((val, key) => { report[key] = val; });
        return report;
    }
};

window.WindowManager = WindowManager;
window.WM = WindowManager; // Global shorthand
