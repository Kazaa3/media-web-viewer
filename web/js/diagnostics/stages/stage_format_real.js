/**
 * stage_format_real.js (v1.35.52)
 * Stage 10: Real Format Verification (MP3, OPUS, FLAC, WAV).
 * Points to actual physical files in the /media/ directory.
 */

const StageFormatReal = {
    id: 'stage-format-real',
    name: 'Real Format Verify (Stage 10)',
    items: [
        {
            id: 'diag-format-real-mp3',
            name: '01 - Anfangsstadium RMX.mp3',
            path: '01 - Anfangsstadium RMX.mp3',
            title: '[REAL] MP3: Anfangsstadium RMX',
            artist: 'Real Library Asset',
            category: 'Audio',
            tags: { title: '[REAL] MP3 Test', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-format-real-opus',
            name: 'Youth Of The Nation - P.O.D.opus',
            path: 'Youth Of The Nation - P.O.D.opus',
            title: '[REAL] OPUS: Youth Of The Nation',
            artist: 'Real Library Asset',
            category: 'Audio',
            tags: { title: '[REAL] OPUS Test', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-format-real-flac',
            name: '02 Pledging My Time.flac',
            path: '02 Pledging My Time.flac',
            title: '[REAL] FLAC: Pledging My Time',
            artist: 'Real Library Asset',
            category: 'Audio',
            tags: { title: '[REAL] FLAC Test', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-format-real-wav',
            name: '20-The Emerald Abyss.wav',
            path: '20-The Emerald Abyss.wav',
            title: '[REAL] WAV: The Emerald Abyss',
            artist: 'Real Library Asset',
            category: 'Audio',
            tags: { title: '[REAL] WAV Test', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-format-real-m4a',
            name: '02 We the People….m4a',
            path: '02 We the People….m4a',
            title: '[REAL] M4A: We the People',
            artist: 'Real Library Asset',
            category: 'Audio',
            tags: { title: '[REAL] M4A Test', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-format-real-m4b',
            name: 'Adrienne Herbert - Power Hour.m4b',
            path: 'Adrienne Herbert - Power Hour.m4b',
            title: '[REAL] M4B: Power Hour',
            artist: 'Audiobook Asset',
            category: 'Audio',
            tags: { title: '[REAL] M4B Test', artist: 'MWV' },
            is_mock: false
        },
        {
            id: 'diag-format-real-aac',
            name: 'Heinz Strunk - Fleisch ist mein Gemüse (Komplettes Hörbuch).aac',
            path: 'Heinz Strunk - Fleisch ist mein Gemüse (Komplettes Hörbuch).aac',
            title: '[REAL] AAC: Fleisch ist mein Gemüse',
            artist: 'Audiobook Asset',
            category: 'Audio',
            tags: { title: '[REAL] AAC Test', artist: 'MWV' },
            is_mock: false
        }
    ]
};

// Auto-register with Manager
document.addEventListener('DOMContentLoaded', () => {
    if (typeof RecoveryManager !== 'undefined') {
        RecoveryManager.registerStage(StageFormatReal);
    }
});
