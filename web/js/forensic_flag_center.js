/**
 * Forensic Flag Center (v1.46.011)
 * Centralized steering overlay for all internal system flags and HUDs.
 */

const ForensicFlagCenter = {
    visible: false,
    registry: null,

    /**
     * Initializes the Flag Center and binds the UI entry points.
     */
    init() {
        console.log("%c[FLAG-CENTER] ARMED. Version v1.46.011", "color: #00f2ff; font-weight: 900;");
        this.registry = window.CONFIG?.ui_flag_registry || null;
        this.bindEvents();
    },

    /**
     * Binds internal events and global listeners.
     */
    bindEvents() {
        // Close on ESC
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && this.visible) this.toggle();
    toggle() {
        if (this.visible) this.hide();
        else this.show();
    },

    /**
     * Forces the Flag Center to become visible.
     */
    show() {
        const overlay = document.getElementById('forensic-flag-center');
        if (!overlay) {
            this.render();
            return this.show();
        }
        this.visible = true;
        overlay.style.display = 'flex';
        console.log("[FLAG-CENTER] UI Steering Active.");
        this.refreshToggles();
    },

    /**
     * Forces the Flag Center to hide.
     */
    hide() {
        const overlay = document.getElementById('forensic-flag-center');
        if (!overlay) return;
        this.visible = false;
        overlay.style.display = 'none';
        console.log("[FLAG-CENTER] UI Steering Hibernated.");
    },

    /**
     * Renders the Flag Center container into the DOM.
     */
    render() {
        if (document.getElementById('forensic-flag-center')) return;

        const overlay = document.createElement('div');
        overlay.id = 'forensic-flag-center';
        overlay.className = 'forensic-overlay glass-morphic';
        overlay.style.display = 'none';

        const content = `
            <div class="flag-center-modal">
                <div class="flag-center-header">
                    <div class="f2c-header">
                        <div class="f2c-title">
                            FORENSIC FLAG CENTER <span class="v-tag">v1.46.011</span>
                        </div>
                        <button class="f2c-reset-btn" onclick="ForensicFlagCenter.factoryReset()">
                            RESTORE DEFAULTS
                        </button>
                        <button class="f2c-close" onclick="ForensicFlagCenter.hide()">&times;</button>
                    </div>
                </div>
                <div class="flag-center-body" id="flag-center-grid">
                    <!-- Categories will be injected here -->
                </div>
                <div class="flag-center-footer">
                    <div class="flag-center-hint">Real-Time Steering Active | Changes Persisted to Backend</div>
                    <button class="flag-center-btn-apply" onclick="window.location.reload()">FULL RECONSTRUCT</button>
                </div>
            </div>
        `;

        overlay.innerHTML = content;
        document.body.appendChild(overlay);

        this.injectCategories();
    },

    /**
     * Dynamically injects categories and toggles from the registry.
     */
    injectCategories() {
        const grid = document.getElementById('flag-center-grid');
        if (!grid || !this.registry) return;

        grid.innerHTML = ""; // Clear

        Object.keys(this.registry).forEach(catId => {
            const category = this.registry[catId];
            const section = document.createElement('div');
            section.className = 'flag-section';
            
            section.innerHTML = `<div class="flag-section-title">${catId.toUpperCase()}</div>`;
            const list = document.createElement('div');
            list.className = 'flag-list';

            Object.keys(category).forEach(key => {
                const label = category[key];
                const item = document.createElement('div');
                item.className = 'flag-item';
                
                // Get current value from window.CONFIG or deep lookup
                const currentValue = this.getConfigValue(key);

                item.innerHTML = `
                    <span class="flag-label">${label}</span>
                    <label class="forensic-switch">
                        <input type="checkbox" id="flag-check-${key.replace('.', '-')}" 
                            ${currentValue ? 'checked' : ''} 
                            onchange="ForensicFlagCenter.handleToggle('${key}', this.checked)">
                        <span class="forensic-slider"></span>
                    </label>
                `;
                list.appendChild(item);
            });

            section.appendChild(list);
            grid.appendChild(section);
        });
    },

    /**
     * Refreshes all toggle states based on current in-memory config.
     */
    refreshToggles() {
        if (!this.registry) return;
        Object.keys(this.registry).forEach(catId => {
            const category = this.registry[catId];
            Object.keys(category).forEach(key => {
                const val = this.getConfigValue(key);
                const check = document.getElementById(`flag-check-${key.replace('.', '-')}`);
                if (check) check.checked = val;
            });
        });
    },

    /**
     * Deep lookup for nested config keys (e.g., 'ui_fragments.player').
     */
    getConfigValue(key) {
        if (!window.CONFIG) return false;
        if (!key.includes('.')) return !!window.CONFIG[key];
        
        const parts = key.split('.');
        let cur = window.CONFIG;
        for (const p of parts) {
            if (cur && cur[p] !== undefined) cur = cur[p];
            else return false;
        }
        return !!cur;
    },

    /**
     * Handles the toggle event, updates backend and local UI.
     */
    handleToggle(key, isEnabled) {
        console.log(`[FLAG-CENTER] Steering: ${key} -> ${isEnabled}`);
        
        // 1. Backend Sync (Eel)
        if (typeof eel !== 'undefined' && typeof eel.set_ui_config_value === 'function') {
            eel.set_ui_config_value(key, isEnabled);
        }

        // 2. Local Config Memory Update
        this.setConfigValue(key, isEnabled);

        // 3. Local UI Pulse (Hide/Show logic)
        if (typeof applySystemFlags === 'function') {
            applySystemFlags();
        }
        
        // 4. Trace
        if (typeof mwv_trace === 'function') {
            mwv_trace('STEERING', 'FLAG-PULSE', { key: key, state: isEnabled });
        }
    },

    /**
     * Updates the local window.CONFIG memory.
     */
    setConfigValue(key, value) {
        if (!window.CONFIG) return;
        if (!key.includes('.')) {
            window.CONFIG[key] = value;
            return;
        }
        
        const parts = key.split('.');
        let cur = window.CONFIG;
        for (let i = 0; i < parts.length - 1; i++) {
            cur = cur[parts[i]];
        }
        cur[parts[parts.length - 1]] = value;
    },

    /**
     * Resets all configuration flags to system defaults (v1.46.010).
     */
    async factoryReset() {
        if (!confirm("RESTORE ALL DEFAULTS? This will reset all visibility flags and layout presets.")) return;
        
        console.warn("[FLAG-CENTER] Initiating Factory Reset...");
        try {
            if (typeof eel !== 'undefined' && typeof eel.reset_config === 'function') {
                const result = await eel.reset_config()();
                console.log("[FLAG-CENTER] Backend Reset Result:", result);
                
                // Re-sync local config
                if (typeof syncCoreRegistry === 'function') {
                    await syncCoreRegistry();
                }
                
                // Force UI Pulse
                if (typeof applySystemFlags === 'function') {
                    applySystemFlags();
                }
                
                this.injectCategories(); // Refresh UI
                if (typeof showToast === 'function') showToast("Workstation Restored", 2000);
            }
        } catch (e) {
            console.error("[FLAG-CENTER] Reset Failed:", e);
        }
    }
};

// Global Export
window.ForensicFlagCenter = ForensicFlagCenter;

// Boot
document.addEventListener('DOMContentLoaded', () => {
    ForensicFlagCenter.init();
});

// Created with MWV v1.46.010-MASTER
