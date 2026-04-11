/**
 * Forensic Workstation Bridge (v1.45.150)
 * Orchestrates the 3-column workstation layout and dynamic player injection.
 */

window.MWV_Workstation = {
    active: false,
    
    /**
     * Activates the workstation environment.
     */
    async activate() {
        console.info("[WORKSTATION] Activating Forensic Environment...");
        const stage = document.getElementById('rebuild-stage');
        if (!stage) return;

        // 1. Show Rebuild Stage
        stage.style.display = 'flex';
        stage.classList.add('rebuild-stage-active');
        
        // 2. Load Workstation Layout Fragment (if not already loaded)
        if (!document.getElementById('forensic-workstation-root')) {
            await window.loadFragment('/fragments/rebuild/forensic_workstation.html', 'rebuild-stage');
        }

        this.active = true;
        this.syncInventory();
        console.log("[WORKSTATION] Environment Ready.");
    },

    /**
     * Injects the appropriate player engine into the central stage.
     */
    async injectPlayer(type, item = null) {
        console.info(`[WORKSTATION] Injecting Player Engine: ${type.toUpperCase()}`);
        const anchor = document.getElementById('workstation-player-anchor');
        if (!anchor) return;

        const fragmentPath = (type === 'audio') 
            ? '/fragments/rebuild/audioplayer.html' 
            : '/fragments/video_player.html';

        // Clear anchor and load new atomic player
        anchor.innerHTML = '<div class="loading-fragment">Swapping Engines...</div>';
        await window.loadFragment(fragmentPath, 'workstation-player-anchor');

        console.log(`[WORKSTATION] ${type.toUpperCase()} Engine Active.`);
        
        // Trigger specific engine init
        if (item) {
            if (type === 'audio' && window.AudioPlayer) window.AudioPlayer.load(item);
            if (type === 'video' && typeof window.loadVideo === 'function') window.loadVideo(item);
        }
    },

    /**
     * Synchronizes the right inventory lane with the global library state.
     */
    syncInventory() {
        const list = document.getElementById('workstation-inventory-list');
        if (!list) return;

        console.log("[WORKSTATION] Syncing Inventory Lane...");
        const items = window.allLibraryItems || [];
        
        if (items.length === 0) {
            list.innerHTML = '<div style="padding:40px; text-align:center; opacity:0.5; font-size:11px;">NO ASSETS INDEXED</div>';
            return;
        }

        list.innerHTML = items.slice(0, 100).map(item => `
            <div class="inventory-item-pill" onclick="MWV_Workstation.handleItemClick(${JSON.stringify(item).replace(/"/g, '&quot;')})" 
                 style="padding: 8px 12px; background: rgba(255,255,255,0.03); border: 1px solid var(--border-glass); border-radius: 6px; cursor: pointer; transition: all 0.2s;">
                <div style="font-size: 11px; font-weight: 800; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.name}</div>
                <div style="font-size: 9px; color: var(--text-secondary); display: flex; justify-content: space-between;">
                    <span>${item.category.toUpperCase()}</span>
                    <span>${item.extension.toUpperCase()}</span>
                </div>
            </div>
        `).join('');

        const countLabel = document.getElementById('workstation-inventory-count');
        if (countLabel) countLabel.innerText = `${items.length} ITEMS`;
    },

    /**
     * Handles item clicks by routing to the correct player engine.
     */
    handleItemClick(item) {
        console.log("[WORKSTATION] Item Selection:", item.name);
        const type = (item.category === 'audio' || item.category === 'audiobook') ? 'audio' : 'video';
        this.injectPlayer(type, item);
    }
};

// Auto-register styles for inventory pills if needed
const style = document.createElement('style');
style.textContent = `
    .inventory-item-pill:hover {
        background: rgba(0, 122, 255, 0.15) !important;
        border-color: var(--accent-primary) !important;
        transform: translateY(-1px);
    }
`;
document.head.appendChild(style);

// Created with MWV v1.45.100-EVO-REBUILD
