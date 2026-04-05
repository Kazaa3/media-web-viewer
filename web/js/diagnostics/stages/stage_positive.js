/**
 * stage_positive.js (v1.35.68)
 * Stage 3 & 4: Positive Playback verification.
 * Restores 2 items for positive test coverage.
 */

const StagePositive = {
    id: 'stage-positive',
    name: 'Positive Playback (Stage 3-4)',
    items: [
        {
            id: 'diag-stage-3-healthy',
            name: 'healthy_mp3_01.mp3',
            path: 'media/healthy_mp3_01.mp3',
            title: '[S3] Healthy MP3 Test',
            artist: 'Baseline Success',
            category: 'Audio',
            tags: { title: '[S3] Healthy MP3 Test', artist: 'Baseline Success' },
            is_mock: false
        },
        {
            id: 'diag-stage-4-opus',
            name: 'opus_test_01.opus',
            path: 'media/opus_test_01.opus',
            title: '[S4] Healthy OPUS Test',
            artist: 'Opus Baseline',
            category: 'Audio',
            tags: { title: '[S4] Healthy OPUS Test', artist: 'Opus Baseline' },
            is_mock: false
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StagePositive);
    }
});
