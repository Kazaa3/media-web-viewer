/**
 * MWV_Hotkeys: Global Keyboard Interaction Layer (v1.41.122)
 * Centralizes all forensic UI toggles and navigation shortcuts.
 */
(() => {
    console.info("[MWV-HOTKEYS] Initializing Keyboard Interaction Layer.");

    document.addEventListener('keydown', (e) => {
        // [v1.41.119 - 122] Forensic UI Toggles
        if (e.altKey && !e.shiftKey && !e.ctrlKey) {
            const key = e.key.toLowerCase();
            
            switch(key) {
                case 'h': // Alt+H: Toggle Header
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleHeader();
                    break;
                case 'n': // Alt+N: Toggle Sub-Nav
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleSubNav();
                    break;
                case 'm': // Alt+M: Toggle Module Tabs
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleModuleTabs();
                    break;
                case 'f': // Alt+F: Toggle Footer
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleFooter();
                    break;
                case 'r': // Alt+R: Toggle Header Right (System Cluster)
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleHeaderRight();
                    break;
                case 's': // Alt+S: Toggle Sidebar
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleSidebar();
                    break;
                case 'd': // Alt+D: [v1.41.122] Forensic Hydration Test (Emergency)
                    e.preventDefault();
                    if (window.MWV_Diagnostics) window.MWV_Diagnostics.forceHydrationTest();
                    break;
                case 'alt': // Simple Alt
                    break;
            }
        }
    });

})();
