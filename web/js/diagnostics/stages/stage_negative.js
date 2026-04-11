/**
 * stage_negative.js (v1.41.00)
 * Stage 1 & 2: Error Handling & Missing File Simulation.
 * Restores 2 items for negative test coverage.
 */

const StageNegative = {
    id: 'stage-negative',
    name: 'Negative Recovery (Stage 1-2)',
    items: [
        {
            id: 'diag-stage-1-missing',
            name: 'missing_file_01.mp3',
            path: 'media/missing_file_01.mp3',
            title: '[S1] Missing File Test',
            artist: 'Broken Path',
            category: 'Audio',
            tags: { title: '[S1] Missing File Test', artist: 'Broken Path' },
            is_mock: true
        },
        {
            id: 'diag-stage-2-corrupt',
            name: 'corrupt_metadata.wav',
            path: 'media/corrupt_metadata.wav',
            title: '[S2] Corrupt Metadata Test',
            artist: 'Broken ID3',
            category: 'Audio',
            tags: { title: '', artist: '' }, // Purposefully empty
            is_mock: true
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageNegative);
    }
});
