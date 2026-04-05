console.log(">>> [RECOVERY] Injecting test header (v1.35.23 - ATOMIC)...");
document.body.insertAdjacentHTML('afterbegin', '<h1 id="recovery-test-header" style="color: red; position: fixed; top: 10px; left: 10px; z-index: 10005; background: white; padding: 10px; border: 5px solid red;">RECOVERY SUCCESS (v1.35.23)</h1>');

// Visibility Atomic Option
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
        min-height: 500px !important;
        border: 4px solid lime !important;
        background: rgba(0, 255, 0, 0.05) !important;
    }
    .loading-fragment {
        display: none !important;
    }
`;
document.head.appendChild(nuclearStyle);

// --- Mutation Stack Tracer ---
const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
        if (mutation.type === 'attributes' || mutation.type === 'childList') {
            const target = mutation.target.id || mutation.target.className || 'unknown';
            console.error(`>>> [MUTATION] Element '${target}' changed!`);
            console.error("Stack Trace:", new Error().stack);
        }
    });
});
observer.observe(document.body, { attributes: true, childList: true, subtree: true });

// --- Atomic Heartbeat (50ms) ---
setInterval(() => {
    const targets = ['player-main-viewport', 'player-view-warteschlange'];
    targets.forEach(id => {
        const el = document.getElementById(id);
        if (el && (el.style.display === 'none' || el.style.opacity === '0')) {
            console.error(`>>> [RECOVERY] UI '${id}' was suppressed! Forced restore.`);
            el.style.display = 'flex';
            el.style.opacity = '1';
            el.style.visibility = 'visible';
        }
    });
}, 50);

// Reachability Probe
setTimeout(() => {
    const queueTarget = document.getElementById('active-queue-list-render-target-warteschlange');
    if (queueTarget) {
        queueTarget.innerHTML = '<div id="atomic-signal" style="background: yellow; color: black; padding: 40px; font-weight: 900; text-align: center; border: 10px dashed black; font-size: 24px;">RECOVERY SIGNAL (v1.35.23): QUEUE VISIBLE</div>';
    }
}, 3000);
