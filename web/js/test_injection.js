console.log(">>> [RECOVERY] Injecting test header (v1.35.22)...");
document.body.insertAdjacentHTML('afterbegin', '<h1 id="recovery-test-header" style="color: red; position: fixed; top: 10px; left: 10px; z-index: 10005; background: white; padding: 10px; border: 5px solid red;">RECOVERY SUCCESS (v1.35.22)</h1>');

// Visibility Nuclear Option (Expanded)
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
        min-height: 400px !important;
        border: 4px solid lime !important;
    }
    .loading-fragment {
        display: none !important;
    }
`;
document.head.appendChild(nuclearStyle);

// --- Mutation Watcher (Catch the Hiding Script) ---
const observeTarget = document.getElementById('player-main-viewport') || document.body;
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' && mutation.attributeName === 'style') {
            console.warn(">>> [RECOVERY] Style mutation detected on:", mutation.target.id || mutation.target.className);
            console.warn("New style:", mutation.target.getAttribute('style'));
        }
    });
});
observer.observe(observeTarget, { attributes: true, subtree: true });

// --- Persistent Heartbeat (Force Visibility) ---
setInterval(() => {
    const el = document.getElementById('player-main-viewport');
    if (el && el.style.display === 'none') {
        console.error(">>> [RECOVERY] UI was hidden! Re-applying visibility...");
        el.style.display = 'flex';
        el.style.opacity = '1';
    }
}, 500);

// Force Theme & Visibility
document.documentElement.setAttribute('data-theme', 'dark');

// Reachability Probe
setTimeout(() => {
    const queueTarget = document.getElementById('active-queue-list-render-target-warteschlange');
    if (queueTarget) {
        console.log(">>> [RECOVERY] Queue Target found. Injecting signal...");
        queueTarget.innerHTML = '<div id="diagnostic-nucleus" style="background: yellow; color: black; padding: 40px; font-weight: 900; text-align: center; border: 10px dashed black; font-size: 24px;">RECOVERY SIGNAL (v1.35.22): QUEUE VISIBLE</div>';
    }
}, 3000);
