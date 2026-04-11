/**
 * stage_video_universal.js (v1.35.59)
 * Stage 12-15: Precision Video Cinema (Native, HD-Pass, Legacy, ISO).
 * Matches the user-requested sequence for exhaustive video testing.
 */

const StageVideoUniversal = {
    id: 'stage-video-universal',
    name: 'Universal Video (Stage 12-15)',
    items: [
        // 1. Native Player (MP4 Direct)
        {
            id: 'diag-video-native-720p',
            name: '30. Pleisweiler Gespräch... (720p).mp4',
            path: '30. Pleisweiler Gespräch - Vortrag - Prof. Dr. Gertraud Teuchert-Noodt - 21. Oktober 2018 (720p_30fps_H264-192kbit_AAC).mp4',
            title: '[DIRECT] Native HD MP4 (No Transcoding)',
            artist: 'Cinema Verify',
            category: 'Video',
            tags: { title: '[DIRECT] Native 720p', artist: 'MWV' },
            is_mock: false
        },
        // 2. HD Pass-through (Remuxing)
        {
            id: 'diag-video-hd-remux',
            name: 'Stargate Continuum (2008) - PAL.mkv.mp4_pass',
            path: 'Stargate Continuum (2008) - PAL.mkv.mp4_pass',
            title: '[PASS] HD MKV -> MP4 Remux (Zero Loss)',
            artist: 'Cinema Verify',
            category: 'Video',
            tags: { title: '[PASS] HD Remux', artist: 'MWV' },
            is_mock: false
        },
        // 3. Legacy PAL/NTSC (Full Transcode)
        {
            id: 'diag-video-mkv-legacy',
            name: 'Set It Off (1996) - DirCut - PAL.mkv.mp4_transcoded',
            path: 'Set It Off (1996) - Director\'s Cut - PAL.mkv.mp4_transcoded',
            title: '[TRANSCODE] Legacy MKV -> MP4 (H264 Conversion)',
            artist: 'Cinema Verify',
            category: 'Video',
            tags: { title: '[TRANSCODE] Legacy Cinema', artist: 'MWV' },
            is_mock: false
        },
        // 4. ISO DVD
        {
            id: 'diag-video-iso-dvd',
            name: '4_KOENIGE.iso.mp4_transcoded',
            path: '4 Könige (2015) - DVD/4_KOENIGE.iso.mp4_transcoded',
            title: '[ISO] DVD Image -> MP4 Transcode',
            artist: 'Cinema Verify',
            category: 'Video',
            tags: { title: '[ISO] DVD Verify', artist: 'MWV' },
            is_mock: false
        },
        // 5. ISO Blu-ray
        {
            id: 'diag-video-iso-bd',
            name: 'RUSHHOUR3_D2.ISO.mp4_transcoded',
            path: 'Rush Hour 3 (2007) - Bonus BD/RUSHHOUR3_D2_EIV_12173.ISO.mp4_transcoded',
            title: '[ISO] Blu-ray Image -> MP4 Transcode',
            artist: 'Cinema Verify',
            category: 'Video',
            tags: { title: '[ISO] BD Verify', artist: 'MWV' },
            is_mock: false
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageVideoUniversal);
    }
});
