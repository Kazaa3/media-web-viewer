/**
 * Media Session API Helpers
 * Manages playback, metadata, and action handlers for the browser's 
 * global media session (OS-level integration).
 */
(function() {
    if (!('mediaSession' in navigator)) {
        console.warn('Media Session API not supported in this browser.');
        return;
    }

    /**
     * Updates the global media session with metadata from a media item.
     * @param {Object} meta - Media metadata (title, artist, album, artwork).
     */
    function updateMediaSession(meta) {
        if (!meta) return;

        try {
            const footerCover = document.getElementById('footer-artwork-raster-buffer');
            const artworkSrc = (meta.artwork && meta.artwork.length) ? meta.artwork[0].src : (footerCover && footerCover.src ? footerCover.src : '');

            navigator.mediaSession.metadata = new MediaMetadata({
                title: meta.title || 'Unknown Title',
                artist: meta.artist || 'Unknown Artist',
                album: meta.album || 'Unknown Album',
                artwork: artworkSrc ? [{ src: artworkSrc, sizes: '96x96', type: 'image/png' }] : []
            });
            console.debug('[MediaSession] Metadata updated:', meta.title);
        } catch (e) { 
            console.warn('[MediaSession] Metadata update failed:', e); 
        }
    }

    /**
     * Registers default action handlers for the media session.
     */
    function registerMediaSessionHandlers() {
        const handlers = {
            'play': () => { 
                const p = document.getElementById('native-html5-audio-pipeline-element'); 
                if (p && p.play) p.play(); 
            },
            'pause': () => { 
                const p = document.getElementById('native-html5-audio-pipeline-element'); 
                if (p && p.pause) p.pause(); 
            },
            'previoustrack': () => { if (typeof window.playPrev === 'function') window.playPrev(); },
            'nexttrack': () => { if (typeof window.playNext === 'function') window.playNext(); },
            'seekbackward': (details) => {
                const p = document.getElementById('native-html5-audio-pipeline-element');
                if (p) p.currentTime = Math.max(p.currentTime - (details.seekOffset || 10), 0);
            },
            'seekforward': (details) => {
                const p = document.getElementById('native-html5-audio-pipeline-element');
                if (p) p.currentTime = Math.min(p.currentTime + (details.seekOffset || 10), p.duration);
            }
        };

        Object.entries(handlers).forEach(([action, handler]) => {
            try {
                navigator.mediaSession.setActionHandler(action, handler);
            } catch (e) {
                console.warn(`[MediaSession] Action handler for "${action}" failed to register:`, e);
            }
        });
    }

    /**
     * Initialization: Initialize session and expose to global scope.
     */
    registerMediaSessionHandlers();
    window.updateMediaSession = updateMediaSession;

    // Legacy support for set_media_session
    window.set_media_session = (meta) => {
        updateMediaSession(meta);
    };

    console.log('[MediaSession] Helpers initialized.');
})();
