/**
 * MWV_DOM_HUD: Real-time DOM Integrity Monitoring (v1.41)
 */
window.MWV_DOM_HUD = (() => {
    let hudElement = null;
    let timer = null;

    function init() {
        createHUD();
        startMonitoring();
        console.info("[MWV-DOM-HUD] DOM Monitor Active.");
    }

    function createHUD() {
        // Integrate into footer or floating pill
        const footer = document.querySelector('.layout-footer') || document.body;
        
        hudElement = document.createElement('div');
        hudElement.id = 'mwv-dom-hud';
        hudElement.style.cssText = `
            font-size: 9px; color: #aaa; padding: 0 10px;
            display: flex; gap: 8px; align-items: center;
            border-left: 1px solid rgba(255,255,255,0.1);
        `;
        
        // Add to footer before tool cluster
        const iconCluster = document.querySelector('.footer-icon-cluster');
        if (iconCluster && iconCluster.parentElement === footer) {
            footer.insertBefore(hudElement, iconCluster);
        } else {
            // Fallback: Absolute bottom-right
            hudElement.style.position = 'fixed';
            hudElement.style.bottom = '50px';
            hudElement.style.right = '20px';
            document.body.appendChild(hudElement);
        }
    }

    function startMonitoring() {
        timer = setInterval(updateStats, 2000);
    }

    function updateStats() {
        const elCount = document.querySelectorAll('*').length;
        const hiddenCount = Array.from(document.querySelectorAll('*')).filter(el => el.style.display === 'none').length;
        const viewportHeight = window.innerHeight;
        
        hudElement.innerHTML = `
            <span>DOM: <b style="color: var(--accent-color);">${elCount}</b></span>
            <span style="opacity: 0.3;">|</span>
            <span>HIDDEN: <b>${hiddenCount}</b></span>
            <span style="opacity: 0.3;">|</span>
            <span>VH: <b>${viewportHeight}px</b></span>
        `;
    }

    return { init };
})();

document.addEventListener('DOMContentLoaded', () => MWV_DOM_HUD.init());
