/**
 * MWV_UI: Central UI Orchestration Engine (v1.41.00)
 * Strictly enforces configuration-driven visibility and geometry.
 */
window.MWV_UI = (() => {
    const registry = {
        config: null,
        activeCategory: 'media',
        isInitialized: false,
        sidebarVisible: false
    };

    const CONSTANTS = {
        HEADER_HEIGHT: 38,
        SUBNAV_HEIGHT: 30,
        FOOTER_HEIGHT: 48,
        SIDEBAR_WIDTH: 250
    };

    /**
     * Initializes the UI Engine.
     */
    async function init() {
        console.info("[MWV-UI] Orchestrator Initializing...");
        
        // --- 1. Fetch Config with 2s Safety Timeout (v1.41.08 Safe-Boot) ---
        try {
            const fetchConfig = async () => {
                if (typeof eel !== 'undefined' && typeof eel.get_ui_settings === 'function') {
                    return await eel.get_ui_settings()();
                } else if (window.CONFIG && window.CONFIG.ui_settings) {
                    return window.CONFIG.ui_settings;
                }
                return null;
            };

            const timeoutPromise = new Promise((_, reject) => 
                setTimeout(() => reject(new Error("Backend Timeout")), 2000)
            );

            registry.config = await Promise.race([fetchConfig(), timeoutPromise]);
            console.log("[MWV-UI] Config loaded successfully.");
        } catch (e) {
            console.warn("[MWV-UI] Handshake stalled or failed, falling back to Safe Mode:", e.message);
            registry.config = registry.config || window.CONFIG?.ui_settings || {
                ui_visibility_matrix: { "media": { "master_header": true, "contextual_pill_nav": true, "footer_visible": true } },
                force_sub_nav_visible: true // v1.41.08 Force sub-nav in safe-mode
            };
        }

        // --- 2. Emergency Reveal Watchdog (v1.41.08) ---
        // After 5 seconds, we remove all loading overlays NO MATTER WHAT.
        setTimeout(() => {
            if (!registry.isInitialized) {
                console.warn("[MWV-UI] Emergency Unlock triggered after 5s stall!");
                hideAllLoadingOverlays();
                apply(registry.activeCategory || 'media');
            }
        }, 5000);

        // 3. Set Startup Category
        registry.activeCategory = localStorage.getItem('mwv_active_category') || 'media';
        
        // 4. Mark Initialized
        registry.isInitialized = true;
        
        // 5. Initial Apply
        apply(registry.activeCategory);
        
        console.info("[MWV-UI] Orchestrator Ready.");
    }

    function hideAllLoadingOverlays() {
        document.querySelectorAll('.loading-fragment').forEach(el => {
            el.style.display = 'none';
        });
        document.body.style.opacity = '1';
    }

    /**
     * Applies the visibility matrix for a specific category.
     */
    function apply(category) {
        if (!registry.isInitialized || !registry.config) return;
        
        registry.activeCategory = category;
        const matrix = registry.config.ui_visibility_matrix || {};
        const settings = matrix[category] || { 
            master_header: true, 
            contextual_pill_nav: true,
            sidebar_visible: false 
        };

        console.log(`[MWV-UI] Applying Matrix for [${category}]:`, settings);

        // --- Visibility Enforcement (Class-Based) ---
        const body = document.body;
        
        // 1. Header
        body.classList.toggle('mwv-hide-header', settings.master_header === false);
        
        // 2. Sub-Nav (contextual_pill_nav) - v1.41.06 Master Override Sync
        const forceSubNav = !!(registry.config.force_sub_nav_visible || registry.config.ui_settings?.force_sub_nav_visible);
        const shouldShowSubNav = forceSubNav || (settings.contextual_pill_nav !== false);
        body.classList.toggle('mwv-hide-subnav', !shouldShowSubNav);
        
        // 3. Footer
        body.classList.toggle('mwv-hide-footer', settings.footer_visible === false);

        // 4. Sidebar (Config-Driven Startup State)
        registry.sidebarVisible = !!settings.sidebar_visible;
        syncSidebar();

        // --- Geometry Recalculation ---
        updateGeometry();
    }

    /**
     * Toggles the main sidebar at runtime and syncs with central flags.
     */
    async function toggleSidebar(forceState = null) {
        const nextState = (forceState !== null) ? forceState : !registry.sidebarVisible;
        
        // Optimistic UI update
        registry.sidebarVisible = nextState;
        syncSidebar();
        updateGeometry();

        // Sync with central flags
        await setSetting(`ui_visibility_matrix.${registry.activeCategory}.sidebar_visible`, nextState);
    }

    /**
     * Updates a setting in the central flags (backend) and re-applies UI.
     */
    async function setSetting(key, value) {
        console.info(`[MWV-UI] Syncing flag: ${key} -> ${value}`);
        try {
            if (typeof eel !== 'undefined' && typeof eel.set_ui_config_value === 'function') {
                const success = await eel.set_ui_config_value(key, value)();
                if (success) {
                    // Re-fetch config to ensure parity
                    const newConfig = await eel.get_ui_settings()();
                    if (newConfig) registry.config = newConfig;
                }
            }
        } catch (e) {
            console.error("[MWV-UI] Backend sync failed:", e);
        }
    }

    /**
     * Syncs sidebar classes and splitter visibility.
     */
    function syncSidebar() {
        document.body.classList.toggle('mwv-sidebar-collapsed', !registry.sidebarVisible);
        
        // Update toggle icons
        const headerToggle = document.getElementById('header-btn-sidebar-toggle');
        if (headerToggle) headerToggle.classList.toggle('active', registry.sidebarVisible);
    }

    /**
     * Recalculates CSS variables based on visible components.
     */
    function updateGeometry() {
        const root = document.documentElement;
        const body = document.body;

        const h = body.classList.contains('mwv-hide-header') ? 0 : CONSTANTS.HEADER_HEIGHT;
        const s = body.classList.contains('mwv-hide-subnav') ? 0 : CONSTANTS.SUBNAV_HEIGHT;
        const f = body.classList.contains('mwv-hide-footer') ? 0 : CONSTANTS.FOOTER_HEIGHT;

        root.style.setProperty('--active-header-height', `${h}px`);
        root.style.setProperty('--active-sub-nav-height', `${s}px`);
        root.style.setProperty('--footer-height', `${f}px`);
        root.style.setProperty('--total-top-offset', `${h + s}px`);
        
        const sw = registry.sidebarVisible ? CONSTANTS.SIDEBAR_WIDTH : 0;
        root.style.setProperty('--sidebar-width', `${sw}px`);

        console.log(`[MWV-UI] Geometry Updated: H:${h} S:${s} F:${f} TotalTop:${h+s}`);
    }

    // Export API
    return {
        init,
        apply,
        toggleSidebar,
        updateGeometry,
        getConstants: () => ({ ...CONSTANTS }),
        getState: () => ({ ...registry })
    };
})();

// Auto-init on script load if DOM is ready, or wait
if (document.readyState === 'complete' || document.readyState === 'interactive') {
    MWV_UI.init();
} else {
    document.addEventListener('DOMContentLoaded', () => MWV_UI.init());
}
