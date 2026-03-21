if ('mediaSession' in navigator) {
                        const updateMediaMetadata = (meta) => {
                            try {
                                const footerCover = document.getElementById('footer-artwork-raster-buffer');
                                const artworkSrc = footerCover && footerCover.src ? footerCover.src : '';
                                navigator.mediaSession.metadata = new MediaMetadata({
                                    title: meta.title || '',
                                    artist: meta.artist || '',
                                    album: meta.album || '',
                                    artwork: [{ src: artworkSrc, sizes: '96x96', type: 'image/png' }]
                                });
                            } catch (e) { console.warn('mediaSession metadata set failed', e); }
                        };

                        navigator.mediaSession.setActionHandler('play', () => { const p = document.getElementById('native-html5-audio-pipeline-element'); if (p && p.play) p.play(); });
                        navigator.mediaSession.setActionHandler('pause', () => { const p = document.getElementById('native-html5-audio-pipeline-element'); if (p && p.pause) p.pause(); });
                        navigator.mediaSession.setActionHandler('previoustrack', () => window.playPrev && window.playPrev());
                        navigator.mediaSession.setActionHandler('nexttrack', () => window.playNext && window.playNext());

                        const pipelineElement = document.getElementById('native-html5-audio-pipeline-element');
                        if (pipelineElement && pipelineElement.addEventListener) {
                            pipelineElement.addEventListener('play', () => updateMediaMetadata({ title: document.querySelector('#status') ? document.querySelector('#status').textContent : '' }));
                        }
                    }
                    function set_media_session(meta) {
                        try {
                            if (!('mediaSession' in navigator)) return;
                            const artwork = (meta.artwork && meta.artwork.length) ? meta.artwork[0].src : document.getElementById('footer-artwork-raster-buffer').src;
                            navigator.mediaSession.metadata = new MediaMetadata({
                                title: meta.title || '',
                                artist: meta.artist || '',
                                album: meta.album || '',
                                artwork: [{ src: artwork, sizes: '96x96', type: 'image/png' }]
                            });
                        } catch (e) {
                            console.warn('set_media_session failed', e);
                        }
                    }
                    window.set_media_session = set_media_session;