/**
 * stage_ffmpeg_mock.js (v1.35.50)
 * Stage 9: Backend FFmpeg Pulse generation.
 * Generates dynamic audio streams via sine-wave oscillators.
 */

const StageFFmpegMock = {
    id: 'stage-ffmpeg-mock',
    name: 'FFmpeg Pulse (Stage 9)',
    items: [
        {
            id: 'diag-ffmpeg-pulse-440',
            name: 'pulse_440hz.mp3',
            path: 'diag/pulse/440.mp3',
            title: '[PULSE] 440Hz (Reference A4)',
            artist: 'Backend Oscillator',
            category: 'Audio',
            tags: { title: '[PULSE] 440Hz', artist: 'Oscillator' },
            is_mock: true,
            force_transcode: false // Backend handles this directly
        },
        {
            id: 'diag-ffmpeg-pulse-880',
            name: 'pulse_880hz.mp3',
            path: 'diag/pulse/880.mp3',
            title: '[PULSE] 880Hz (Reference A5)',
            artist: 'Backend Oscillator',
            category: 'Audio',
            tags: { title: '[PULSE] 880Hz', artist: 'Oscillator' },
            is_mock: true
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageFFmpegMock);
    }
});
