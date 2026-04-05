/**
 * stage_real.js (v1.35.45)
 * The Golden Sample: Real MP3 Asset Verification.
 * This stage uses ACTUAL files from the /media/ directory.
 */

const StageReal = {
    id: 'stage-real',
    name: 'Golden Sample (Real Playback)',
    items: [
        {
            id: 'diag-real-1',
            name: '01 - Einfach & Leicht.mp3',
            path: 'media/01 - Einfach & Leicht.mp3',
            title: '[REAL-PLAY] 01 - Einfach & Leicht.mp3',
            artist: 'MWV Asset Verification',
            category: 'Audio',
            tags: { title: '[REAL-PLAY] Einfach & Leicht', artist: 'MWV Asset Verification' },
            is_mock: false // IMPORTANT: This tells the player it's a REAL asset.
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageReal);
    }
});
