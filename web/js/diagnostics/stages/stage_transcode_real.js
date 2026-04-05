/**
 * stage_transcode_real.js (v1.35.56)
 * Stage 11: Real Audio Transcoding (ALAC, WMA).
 * Forces the backend to perform on-the-fly conversion.
 */

const StageTranscodeReal = {
    id: 'stage-transcode-real',
    name: 'Real Transcode (Stage 11)',
    items: [
        {
            id: 'diag-transcode-real-alac',
            name: '11 - All This and More.alac.flac_transcoded',
            path: '11 - All This and More.alac.flac_transcoded',
            title: '[TRANSCODE] ALAC (Apple Lossless) -> FLAC',
            artist: 'Transcode Verification',
            category: 'Audio',
            tags: { title: '[TRANSCODE] ALAC to FLAC', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-transcode-real-wma',
            name: '2-09 - Good Old Days.wma.opus_transcoded',
            path: '2-09 - Good Old Days.wma.opus_transcoded',
            title: '[TRANSCODE] WMA (Windows Media) -> OPUS',
            artist: 'Transcode Verification',
            category: 'Audio',
            tags: { title: '[TRANSCODE] WMA to OPUS', artist: 'MWV' },
            is_mock: false
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageTranscodeReal);
    }
});
