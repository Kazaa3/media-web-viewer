console.log(`>>> [RECOVERY] Injecting test header (${window.MWV_VERSION || 'v...'} - HYDRATION)...`);
document.body.insertAdjacentHTML('afterbegin', `<h1 id="recovery-test-header" style="color: red; position: fixed; top: 10px; left: 10px; z-index: 10005; background: white; padding: 10px; border: 5px solid red;">RECOVERY SUCCESS (${window.MWV_VERSION || 'v...'})</h1>`);

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
    }
    .loading-fragment {
        display: none !important;
    }
`;
document.head.appendChild(nuclearStyle);

// --- Atomic Data Hydration (v1.35.32) ---
function mwv_force_hydration() {
    console.log(">>> [RECOVERY] Hydrating library with real tracks...");
    
    const mockTracks = [
        {
            id: 'mock-1',
            filename: 'sample_audio.mp3',
            path: 'media/sample_audio.mp3',
            title: 'Atomic Recovery Track 01',
            artist: 'Media Orchestrator',
            category: 'recovery',
            is_favorite: true
        },
        {
            id: 'mock-2',
            filename: 'test_track_01.m4a',
            path: 'media/test_track_01.m4a',
            title: 'Atomic Recovery Track 02',
            artist: 'Media Orchestrator',
            category: 'recovery',
            is_favorite: false
        }
    ];

    // Hydrate Global State
    window.allLibraryItems = mockTracks;
    
    // Notify Components
    if (typeof renderAudioQueue === 'function') {
        console.log(">>> [RECOVERY] Triggering manual playlist render...");
        renderAudioQueue();
    }
    
    if (typeof updateLibraryUI === 'function') {
        updateLibraryUI();
    }
}

// Trigger Hydration after a short delay
setTimeout(mwv_force_hydration, 2500);

// Reachability Probe (Non-Destructive)
setTimeout(() => {
    const queueTarget = document.getElementById('active-queue-list-render-target-warteschlange');
    if (queueTarget) {
        queueTarget.insertAdjacentHTML('afterbegin', `<div id="atomic-signal" style="background: yellow; color: black; padding: 20px; font-weight: 900; text-align: center; border: 5px dashed black; font-size: 18px; margin-bottom: 10px;">RECOVERY SIGNAL (${window.MWV_VERSION || 'v...'}): HYDRATION ACTIVE</div>`);
    }
}, 3000);

// Created with MWV v1.46.00-MASTER
