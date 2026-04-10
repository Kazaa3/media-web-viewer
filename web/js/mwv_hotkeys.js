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

            switch (key) {
                case 'y': // Alt+H: Level 1 - MASTER MENU / HEADER
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleHeader();
                    break;
                case 'x': // Alt+M: Level 2 - SUB-MENU / MODULE TABS
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleSubMenu();
                    break;
                case 'c': // Alt+N: Level 3 - TERTIARY SUB-NAV
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleSubNav();
                    break;
                case 'v': // Alt+F: Toggle Footer
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleFooter();
                    break;
                case 'b': // Alt+R: Toggle Header Right (System Cluster)
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleHeaderRight();
                    break;
                case 'n': // Alt+S: Toggle Sidebar
                    e.preventDefault();
                    if (window.MWV_UI) window.MWV_UI.toggleSidebar();
                    break;
                case 'm': // Alt+D: [v1.41.122] Forensic Hydration Test (Emergency)
                    e.preventDefault();
                    if (window.MWV_Diagnostics) window.MWV_Diagnostics.forceHydrationTest();
                    break;
                case 'alt': // Simple Alt
                    break;
            }
        }
    });

})();
