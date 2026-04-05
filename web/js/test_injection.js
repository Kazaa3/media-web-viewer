console.log(">>> [RECOVERY] Injecting test header...");
document.body.insertAdjacentHTML('afterbegin', '<h1 id="recovery-test-header" style="color: red; position: fixed; top: 10px; left: 10px; z-index: 9999; background: white; padding: 10px; border: 5px solid red;">RECOVERY SUCCESS (v1.35.15)</h1>');

// Force Theme & Visibility
document.documentElement.setAttribute('data-theme', 'dark');

// Reachability & Dimension Probe
setTimeout(() => {
    const queueTarget = document.getElementById('active-queue-list-render-target-warteschlange');
    const playerView = document.getElementById('player-view-warteschlange');
    const mainViewport = document.getElementById('player-main-viewport');
    
    if (playerView) {
        console.log(">>> [RECOVERY] Player View found. Style:", playerView.getAttribute('style'));
        playerView.style.display = "flex";
        playerView.style.opacity = "1";
        playerView.style.visibility = "visible";
        playerView.style.border = "5px solid lime"; // Nuclear marker
        playerView.style.zIndex = "5000";
    } else {
        console.warn(">>> [RECOVERY] Player View NOT FOUND in DOM!");
    }

    if (mainViewport) {
        console.log(">>> [RECOVERY] Main Viewport dims:", mainViewport.offsetWidth, "x", mainViewport.offsetHeight);
        mainViewport.style.background = "#111"; // Ensure it's reachable
    }

    if (queueTarget) {
        console.log(">>> [RECOVERY] Queue Target found. Injecting signal...");
        queueTarget.innerHTML = '<div style="background: yellow; color: black; padding: 40px; font-weight: 900; text-align: center; border: 10px dashed black; font-size: 24px;">RECOVERY SIGNAL: QUEUE VISIBLE</div>';
    }

    if (typeof allLibraryItems !== 'undefined') {
        console.log(">>> [RECOVERY] allLibraryItems exists. Count:", allLibraryItems.length);
        if (allLibraryItems.length === 0 && typeof bootstrapMockQueue === 'function') {
            bootstrapMockQueue();
        }
    }
}, 4000);
