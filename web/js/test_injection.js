console.log(">>> [RECOVERY] Injecting test header...");
document.body.insertAdjacentHTML('afterbegin', '<h1 id="recovery-test-header" style="color: red; position: fixed; top: 10px; left: 10px; z-index: 10005; background: white; padding: 10px; border: 5px solid red;">RECOVERY SUCCESS (v1.35.18)</h1>');

// Visibility Nuclear Option
const nuclearStyle = document.createElement('style');
nuclearStyle.innerHTML = `
    #player-main-viewport, 
    #player-tab-split-container, 
    .player-view-container, 
    #player-view-warteschlange {
        display: flex !important;
        opacity: 1 !important;
        visibility: visible !important;
        z-index: 5000 !important;
        min-height: 200px !important;
        border: 2px solid lime !important;
    }
    .loading-fragment {
        display: none !important;
    }
    #active-queue-list-render-target-warteschlange {
        min-height: 100px !important;
        background: rgba(255, 255, 0, 0.1) !important;
    }
`;
document.head.appendChild(nuclearStyle);

// Force Theme & Visibility
document.documentElement.setAttribute('data-theme', 'dark');

// Reachability & Dimension Probe
setTimeout(() => {
    const queueTarget = document.getElementById('active-queue-list-render-target-warteschlange');
    const playerView = document.getElementById('player-view-warteschlange');
    
    if (playerView) {
        console.log(">>> [RECOVERY] Player View found. Dimensions:", playerView.offsetWidth, "x", playerView.offsetHeight);
    }

    if (queueTarget) {
        console.log(">>> [RECOVERY] Queue Target found. Injecting signal...");
        queueTarget.innerHTML = '<div id="diagnostic-nucleus" style="background: yellow; color: black; padding: 40px; font-weight: 900; text-align: center; border: 10px dashed black; font-size: 24px; z-index: 6000; position: relative;">RECOVERY SIGNAL: QUEUE VISIBLE</div>';
    }

    if (typeof allLibraryItems !== 'undefined') {
        if (allLibraryItems.length === 0 && typeof bootstrapMockQueue === 'function') {
            console.log(">>> [RECOVERY] Triggering bootstrapMockQueue...");
            bootstrapMockQueue();
        }
    }
}, 3000);
