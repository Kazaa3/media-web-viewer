/**
 * bibliothek_stages.js (v1.35.43)
 * Stage 5: Layout Stress (Grid/Coverflow Alignment).
 * Stage 6: Metadata Resilience (Missing/Long data).
 */

const BibliothekStages = {
    id: 'stage-bibliothek',
    name: 'Bibliothek Diagnostics (Stage 5-6)',
    items: [
        {
            id: 'diag-stage-5-audio',
            name: 'Stress Audio.mp3',
            path: 'media/stress_audio.mp3',
            title: '[S5] Audio Layout Test',
            artist: 'Layout Master',
            category: 'Audio',
            tags: { title: '[S5] Audio Layout Test', artist: 'Layout Master' },
            is_mock: true
        },
        {
            id: 'diag-stage-5-video',
            name: 'Stress Video.mp4',
            path: 'media/stress_video.mp4',
            title: '[S5] Video Layout Test',
            artist: 'Cinephile Mock',
            category: 'Video',
            tags: { title: '[S5] Video Layout Test', artist: 'Cinephile Mock' },
            is_mock: true
        },
        {
            id: 'diag-stage-5-film',
            name: 'Inception.mkv',
            path: 'media/inception.mkv',
            title: '[S5] Film Badge Test',
            artist: 'Nolan Sim',
            category: 'Film',
            tags: { title: '[S5] Film Badge Test', artist: 'Nolan Sim' },
            is_mock: true
        },
        {
            id: 'diag-stage-6-broken',
            name: 'Broken Metadata Item.wav',
            path: 'media/broken.wav',
            title: '', // EMPTY TITLE TEST
            artist: '', // EMPTY ARTIST TEST
            category: 'Audio',
            tags: {}, // EMPTY TAGS TEST
            is_mock: true
        },
        {
            id: 'diag-stage-6-long',
            name: 'Extremely Long Filename That Should Be Truncated In The UI To Prevent Breakouts.mp3',
            path: 'media/long_name.mp3',
            title: '[S6] Overflow Test Track With Many Words',
            artist: 'The Truncator Extraordinaire',
            category: 'Audio',
            tags: { title: '[S6] Overflow Test Track With Many Words', artist: 'The Truncator Extraordinaire' },
            is_mock: true
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(BibliothekStages);
    }
});
