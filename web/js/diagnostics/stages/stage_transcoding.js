/**
 * stage_transcoding.js (v1.35.44)
 * Stage 7: Format Stress & Transcoding Verification.
 * Verifies OGG, FLAC, and ALAC as abspielbare paths.
 */

const StageTranscoding = {
    id: 'stage-transcoding',
    name: 'Transcoding Focus (Stage 7)',
    items: [
        {
            id: 'diag-stage-7-ogg',
            name: 'AL_Cave_108_inci_CaveDist_02.ogg',
            path: 'media/AL_Cave_108_inci_CaveDist_02.ogg',
            title: '[S7] OGG Transcode Test',
            artist: 'Environment Ambient',
            category: 'Audio',
            tags: { title: '[S7] OGG Transcode Test', artist: 'Environment Ambient' },
            is_mock: false
        },
        {
            id: 'diag-stage-7-flac',
            name: '02 Aaliyah feat. Static - Loose Rap.flac',
            path: 'media/02 Aaliyah feat. Static - Loose Rap.flac',
            title: '[S7] FLAC Transcode Test',
            artist: 'Aaliyah (Lossless)',
            category: 'Audio',
            tags: { title: '[S7] FLAC Transcode Test', artist: 'Aaliyah (Lossless)' },
            is_mock: false
        },
        {
            id: 'diag-stage-7-alac',
            name: '01-05-Joan_Baez-Lowlands-LLS.m4a',
            path: 'media/01-05-Joan_Baez-Lowlands-LLS.m4a',
            title: '[S7] ALAC Transcode Test',
            artist: 'Joan Baez (Lossless M4A)',
            category: 'Audio',
            tags: { title: '[S7] ALAC Transcode Test', artist: 'Joan Baez (Lossless M4A)' },
            is_mock: false
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageTranscoding);
    }
});
