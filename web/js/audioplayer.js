/**
 * Audio Playback Module
 * Manages the HTML5 Audio Pipeline, playlists, and playback state.
 */

// --- Audio State (Now Anchored into window for Orchestration v1.45.110) ---
let isShuffle = false;
let isRepeat = 'off'; // 'off', 'all', 'one'
let shuffledPlaylist = [];
window.activeQueueFilter = 'all'; // v1.35.61 Filter state

// Local access shorthand (v1.45.110 Sync)
const currentPlaylist = window.currentPlaylist;
// Note: playlistIndex is accessed directly via window.playlistIndex to ensure SSOT.

/**
 * Empties the current player queue (v1.41.00).
 */
function clearQueue() {
    console.warn(">>> [Queue] Clearing all items.");
    window.currentPlaylist = [];
    window.playlistIndex = -1;
    
    // Stop playback if something is playing
    const pipeline = document.getElementById('native-html5-audio-pipeline-element');
    if (pipeline) {
        pipeline.pause();
        pipeline.src = "";
    }
    
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
    if (typeof showToast === 'function') showToast("Queue geleert", 1500);
}

let audioContext = null;
let analyser = null;
let dataArray = null;
let visualizerAnimationId = null;
let visualizerStyle = localStorage.getItem('mwv_visualizer_style') || 'bars'; // 'bars', 'circle', 'wave'

/**
 * Diagnostic Control Handlers (v1.35.65)
 */
function toggleDiagLibMode() {
    const isReal = localStorage.getItem('mwv_real_db_mode') === 'true';
    localStorage.setItem('mwv_real_db_mode', !isReal);
    
    // Update local UI
    const label = document.getElementById('diag-lib-label');
    const dot = document.getElementById('diag-lib-dot');
    if (label) label.innerText = !isReal ? 'REAL' : 'DIAG';
    if (dot) dot.style.left = !isReal ? '1px' : '11px';
    if (dot) dot.style.background = !isReal ? '#888' : 'var(--accent-color)';

    console.info(">>> [Recovery] Library mode switched to:", !isReal ? 'Real DB' : 'Diagnostics');
    if (typeof showToast === 'function') showToast(`Library: ${!isReal ? 'Real DB' : 'Diagnostics'}`, 1500);
    
    if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
}

function toggleForceNative() {
    const isForced = localStorage.getItem('mwv_force_native') === 'true';
    localStorage.setItem('mwv_force_native', !isForced);
    
    const label = document.getElementById('diag-native-label');
    const dot = document.getElementById('diag-native-dot');
    if (label) label.style.color = !isForced ? 'var(--accent-color)' : 'var(--text-secondary)';
    if (dot) dot.style.left = !isForced ? '11px' : '1px';
    if (dot) dot.style.background = !isForced ? 'var(--accent-color)' : '#888';

    console.warn(">>> [Video] Force Native Mode:", !isForced ? 'ON' : 'OFF');
    if (typeof showToast === 'function') showToast(`Native Force: ${!isForced ? 'ON' : 'OFF'}`, 1500);
}

// Ensure UI sync on load
document.addEventListener('DOMContentLoaded', () => {
    const isReal = localStorage.getItem('mwv_real_db_mode') === 'true';
    const label = document.getElementById('diag-lib-label');
    const dot = document.getElementById('diag-lib-dot');
    if (label) label.innerText = isReal ? 'REAL' : 'DIAG';
    if (dot) dot.style.left = isReal ? '1px' : '11px';
    
    const isForced = localStorage.getItem('mwv_force_native') === 'true';
    const nLabel = document.getElementById('diag-native-label');
    const nDot = document.getElementById('diag-native-dot');
    if (nLabel && isForced) nLabel.style.color = 'var(--accent-color)';
    if (nDot && isForced) nDot.style.left = '11px';
});

// --- Playback Controllers ---

/**
 * Initializes the audio pipeline and its events.
 */
function initAudioPipeline() {
    const pipeline = document.getElementById('native-html5-audio-pipeline-element');
    if (!pipeline) return;

    pipeline.onended = () => {
        if (isRepeat === 'one') {
            pipeline.play();
        } else {
            playNext();
        }
    };

    pipeline.ontimeupdate = () => {
        updatePlaybackProgress();
    };

    pipeline.onloadedmetadata = () => {
        updatePlaybackProgress();
    };

    const slider = document.getElementById('global-seek-slider');
    if (slider) {
        slider.oninput = () => {
            const duration = pipeline.duration || 0;
            if (duration > 0) {
                pipeline.currentTime = (slider.value / 100) * duration;
            }
        };
    }
}

function updatePlaybackProgress() {
    const pipeline = document.getElementById('native-html5-audio-pipeline-element');
    const slider = document.getElementById('global-seek-slider');
    const currentTimeEl = document.getElementById('player-time-current');
    const durationEl = document.getElementById('player-time-total');
    
    if (!pipeline || !slider) return;

    const currentTime = pipeline.currentTime;
    const duration = pipeline.duration || 0;

    if (duration > 0) {
        slider.value = (currentTime / duration) * 100;
    }

    if (currentTimeEl) currentTimeEl.innerText = formatTime(currentTime);
    if (durationEl && duration > 0) durationEl.innerText = formatTime(duration);
}

function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
}


/**
 * Main Audio Playback entry point.
 */
function playAudio(item, startTime = 0) {
    const pipeline = document.getElementById('native-html5-audio-pipeline-element');
    if (!pipeline || !item) return;

    // v1.35.35: Robust Path Handling
    const rawPath = item.path || item.name;
    if (!rawPath || rawPath === 'undefined') {
        mwv_trace('PLAYER-EVENT', 'PLAYBACK-CRITICAL', { message: "Item path is undefined", item: item });
        if (typeof showToast === 'function') showToast("Playback Impossible: File path is missing.", "error");
        return;
    }

    const ext = rawPath.slice(((rawPath.lastIndexOf(".") - 1) >>> 0) + 2).toLowerCase();
    const proxyUrl = "/media/" + encodeURIComponent(rawPath);
    const logMsg = `[Audio] Attempting to play: ${item.name || 'Unknown'} | Path: ${rawPath} | Proxy: ${proxyUrl}`;
    
    mwv_trace('PLAYER-EVENT', 'PLAYBACK-START', { name: item.name, path: rawPath, proxy: proxyUrl });
    if (typeof appendUiTrace === 'function') appendUiTrace(logMsg);
    
    pipeline.src = proxyUrl;
    
    // Logic: Resume for audiobooks, else start at 0
    const shouldResume = item.category === 'Audiobook' || item.category === 'Hörbruch';
    pipeline.currentTime = (shouldResume && startTime > 0) ? startTime : 0;

    pipeline.play().then(() => {
        setupVisualizer(pipeline);
    }).catch(e => {
        mwv_trace('PLAYER-EVENT', 'PLAYBACK-FAIL', { message: e.message, name: item.name });
        if (typeof showToast === 'function') showToast(`Playback Error: ${e.message}`, 'error');
    });
    
    // Sync All UI Metadata Elements (v1.34 Global Sync)
    const title = item.tags?.title || item.name || 'Unknown Title';
    const artist = item.tags?.artist || item.artist || item.author || 'Unknown Artist';
    const album = item.tags?.album || 'Unknown Album';
    const artworkUrl = `/cover/${encodeURIComponent(item.path || item.name)}`;

    // 1. Text Sync
    document.querySelectorAll('.synced-title').forEach(el => el.innerText = title);
    document.querySelectorAll('.synced-artist').forEach(el => el.innerText = artist);
    document.querySelectorAll('.synced-album').forEach(el => el.innerText = album);
    
    // 2. Artwork Sync
    document.querySelectorAll('.synced-artwork').forEach(el => {
        el.src = artworkUrl;
        el.onerror = () => { el.src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='; };
    });

    // 3. Tech Specs Sync (Codec, Bitrate, etc.)
    const codec = item.codec || (ext ? ext.slice(1).toUpperCase() : '-');
    document.querySelectorAll('.synced-specs span').forEach(el => {
        if (el.id.includes('codec')) el.innerText = codec;
        if (el.id.includes('bitrate')) el.innerText = item.bitrate || '-';
        if (el.id.includes('samplerate')) el.innerText = item.samplerate || '-';
        if (el.id.includes('bitdepth')) el.innerText = item.bitdepth || '-';
    });

    // 4. Chapter Sidebar (Restore Audiobook Chapters if applicable)
    if (item.category === 'Audiobook' || item.category === 'Hörbuch' || item.category === 'Album') {
        if (typeof renderAudiobookDetails === 'function') renderAudiobookDetails(item);
    } else {
        const chapterList = document.getElementById('player-chapters-list');
        if (chapterList) chapterList.innerHTML = '';
    }

    if (typeof eel !== "undefined" && typeof eel.log_gui_event === 'function') {
        eel.log_gui_event("PLAYBACK", "START", { name: item.name, path: item.path })();
    }
}


/**
 * Setup and start the Web Audio API visualizer.
 */
function setupVisualizer(audioElement) {
    if (!audioContext) {
        audioContext = new (window.AudioContext || window.webkitAudioContext)();
        const source = audioContext.createMediaElementSource(audioElement);
        analyser = audioContext.createAnalyser();
        analyser.fftSize = 256;
        source.connect(analyser);
        analyser.connect(audioContext.destination);
        
        const bufferLength = analyser.frequencyBinCount;
        dataArray = new Uint8Array(bufferLength);
    }
    
    if (audioContext.state === 'suspended') {
        audioContext.resume();
    }
    
    drawVisualizer();
}

/**
 * Animation loop for the audio visualizer.
 */
function drawVisualizer() {
    const canvas = document.getElementById('audio-visualizer-canvas');
    if (!canvas) return;
    
    const ctx = canvas.getContext('2d');
    const width = canvas.width = canvas.parentElement.clientWidth;
    const height = canvas.height = 300;
    
    cancelAnimationFrame(visualizerAnimationId);
    
    function animate() {
        if (!analyser) {
            ctx.clearRect(0, 0, width, height);
            ctx.fillStyle = 'rgba(128, 128, 128, 0.2)';
            ctx.font = '700 14px "Inter", sans-serif';
            ctx.textAlign = 'center';
            ctx.fillText('Warte auf Audio-Stream...', width / 2, height / 2);
            return;
        }

        visualizerAnimationId = requestAnimationFrame(animate);
        
        if (visualizerStyle === 'wave') {
            analyser.getByteTimeDomainData(dataArray);
        } else {
            analyser.getByteFrequencyData(dataArray);
        }
        
        ctx.clearRect(0, 0, width, height);

        if (visualizerStyle === 'bars') {
            const barWidth = (width / dataArray.length) * 2.5;
            let x = 0;
            for (let i = 0; i < dataArray.length; i++) {
                const barHeight = (dataArray[i] / 255) * height;
                const gradient = ctx.createLinearGradient(0, height, 0, height - barHeight);
                gradient.addColorStop(0, 'rgba(0, 122, 255, 0)');
                gradient.addColorStop(1, 'rgba(0, 122, 255, 0.4)');
                ctx.fillStyle = gradient;
                ctx.fillRect(x, height - barHeight, barWidth, barHeight);
                x += barWidth + 1;
            }
        } else if (visualizerStyle === 'circle') {
            const centerX = width / 2;
            const centerY = height / 2;
            const radius = 80;
            
            ctx.beginPath();
            ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
            ctx.strokeStyle = 'rgba(0, 122, 255, 0.2)';
            ctx.stroke();

            for (let i = 0; i < dataArray.length; i++) {
                const angle = (i / dataArray.length) * (Math.PI * 2);
                const val = (dataArray[i] / 255) * 60;
                const x1 = centerX + Math.cos(angle) * radius;
                const y1 = centerY + Math.sin(angle) * radius;
                const x2 = centerX + Math.cos(angle) * (radius + val);
                const y2 = centerY + Math.sin(angle) * (radius + val);
                
                ctx.beginPath();
                ctx.moveTo(x1, y1);
                ctx.lineTo(x2, y2);
                ctx.strokeStyle = `hsla(210, 100%, 50%, ${dataArray[i] / 255})`;
                ctx.lineWidth = 2;
                ctx.stroke();
            }
        } else if (visualizerStyle === 'wave') {
            ctx.lineWidth = 3;
            ctx.strokeStyle = 'rgba(0, 122, 255, 0.6)';
            ctx.beginPath();
            
            const sliceWidth = width / dataArray.length;
            let x = 0;
            for (let i = 0; i < dataArray.length; i++) {
                const v = dataArray[i] / 128.0;
                const y = v * height / 2;
                if (i === 0) ctx.moveTo(x, y);
                else ctx.lineTo(x, y);
                x += sliceWidth;
            }
            ctx.lineTo(width, height / 2);
            ctx.stroke();
        }
    }
    
    animate();
}

/**
 * Changes the active visualizer style.
 */
function setVisualizerStyle(style) {
    visualizerStyle = style;
    localStorage.setItem('mwv_visualizer_style', style);
    if (typeof showToast === 'function') showToast(`Visualizer: ${style}`, 'info');
}

/**
 * Updates the media sidebar with item information.
 */
function updateMediaSidebar(item, path) {
    const tags = item.tags || {};
    
    if (typeof safeText === 'function') {
        // Sync Sidebar
        safeText('sidebar-metadata-primary-string-renderer', tags.title || item.name);
        const artistStr = tags.albumartist && tags.albumartist !== tags.artist ? tags.artist + " (Album: " + tags.albumartist + ")" : (tags.artist || 'Unknown Artist');
        safeText('sidebar-metadata-secondary-string-renderer', artistStr);
        
        // Sync Legacy, Visualizer, and Queue Views
        const isDiag = localStorage.getItem('mwv_diagnostic_mode') === 'true';
        
        ['legacy', 'visualizer', 'warteschlange'].forEach(view => {
            safeText(`big-player-title-${view}`, tags.title || item.name);
            safeText(`big-player-artist-${view}`, tags.artist || 'Unknown Artist');
            
            // Core Tech Specs
            const fileExt = item.path ? item.path.split('.').pop().toUpperCase() : '-';
            safeText(`spec-filetype-${view}`, item.category || 'Audio');
            safeText(`spec-container-${view}`, tags.container || fileExt);
            safeText(`spec-codec-${view}`, tags.codec || fileExt);
            safeText(`spec-bitrate-${view}`, tags.bitrate || '-');
            
            if (view === 'legacy' || view === 'warteschlange') {
                safeText(`spec-bitdepth-${view}`, tags.bitdepth ? tags.bitdepth + ' Bit' : '16 Bit');
                safeText(`spec-samplerate-${view}`, tags.samplerate || '44.1 kHz');
                safeText(`spec-album-line-${view}`, tags.album || 'No Album');
                
                const trackStr = `${tags.year || '2026'} • ${tags.genre || 'General'} • Track ${tags.track ? tags.track.toString().padStart(2, '0') : '01'}`;
                safeText(`spec-track-details-${view}`, trackStr);
                
                // Sync New Premium Fields
                safeText('spec-year-badge', tags.year || '2026');
                safeText('spec-genre-badge', tags.genre || 'General');
                safeText('spec-size-warteschlange', item.size_human || item.size || '-');
                safeText('spec-disc-warteschlange', tags.disc ? `Disc ${tags.disc}` : '1');
                safeText('player-extended-comment', tags.comment || 'Kein Kommentar vorhanden.');

                // Diagnostic Visibility
                const pathEl = document.getElementById(`player-file-path-${view}`);
                if (pathEl) {
                    pathEl.innerText = path || item.path || 'Unknown Path';
                    pathEl.style.display = isDiag ? 'block' : 'none';
                }
            }
        });
        
        // Global Diagnostic Overlays
        const diagOverlays = document.querySelectorAll('.player-technical-diagnostic-overlay');
        diagOverlays.forEach(el => el.style.display = isDiag ? 'block' : 'none');
    }


    const coverUrl = "/cover/" + encodeURIComponent(item.name);
    const artworkIds = [
        'sidebar-artwork-raster-buffer', 
        'parser-mediainfo-artwork', 
        'footer-artwork-raster-buffer', 
        'big-player-artwork-visualizer',
        'big-player-artwork-warteschlange'
    ];
    
    artworkIds.forEach(id => {
        const img = document.getElementById(id);
        if (img) {
            img.src = coverUrl;
            img.style.opacity = "1";
            img.onerror = () => img.src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';
        }
    });

    const playingLabel = (typeof t === 'function' ? t('player_status_playing') : 'Playing: ') || 'Playing: ';
    const byLabel = (typeof t === 'function' ? t('player_status_by') : ' by ') || ' by ';
    if (typeof safeHtml === 'function') {
        safeHtml('active-orchestration-status-message-renderer', `${playingLabel} &nbsp; <strong>${tags.title || item.name}</strong> &nbsp; ${byLabel} &nbsp; ${tags.artist || 'Unknown'}`);
    }

    // Sync Lyrics (v1.35 Premium)
    const lyricsContainer = document.getElementById('player-lyrics-content');
    if (lyricsContainer) {
        lyricsContainer.innerText = tags.lyrics || item.lyrics || 'Keine Lyrics für diesen Titel gefunden.';
    }
}

// --- Playlist Control ---

function toggleShuffle() {
    isShuffle = !isShuffle;
    updateShuffleUI();

    if (isShuffle) {
        shuffledPlaylist = [...currentPlaylist];
        for (let i = shuffledPlaylist.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [shuffledPlaylist[i], shuffledPlaylist[j]] = [shuffledPlaylist[j], shuffledPlaylist[i]];
        }
        if (playlistIndex !== -1) {
            const currentItem = currentPlaylist[playlistIndex];
            playlistIndex = shuffledPlaylist.indexOf(currentItem);
        }
    } else {
        if (playlistIndex !== -1 && shuffledPlaylist.length > 0) {
            const currentItem = shuffledPlaylist[playlistIndex];
            playlistIndex = currentPlaylist.indexOf(currentItem);
        }
    }
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
}

function toggleRepeat() {
    if (isRepeat === 'off') isRepeat = 'all';
    else if (isRepeat === 'all') isRepeat = 'one';
    else isRepeat = 'off';
    updateRepeatUI();
}

function updateShuffleUI() {
    const btn = document.getElementById('btn-shuffle');
    const plBtn = document.getElementById('sequence-buffer-randomization-orchestrator');
    [btn, plBtn].forEach(b => {
        if (!b) return;
        b.classList.toggle('active', isShuffle);
    });
}

function updateRepeatUI() {
    const btn = document.getElementById('btn-repeat');
    if (!btn) return;
    btn.classList.toggle('active', isRepeat !== 'off');
}

async function playNext() {
    const list = isShuffle ? shuffledPlaylist : currentPlaylist;
    if (list.length === 0) return;

    playlistIndex++;
    if (playlistIndex >= list.length) {
        if (isRepeat === 'all') playlistIndex = 0;
        else { playlistIndex = list.length - 1; return; }
    }
    const item = list[playlistIndex];
    if (typeof playMediaObject === 'function') {
        playMediaObject(item);
    } else if (typeof playAudio === 'function') {
        playAudio(item, 0);
    }
}

async function playPrev() {
    const list = isShuffle ? shuffledPlaylist : currentPlaylist;
    if (list.length === 0) return;

    playlistIndex--;
    if (playlistIndex < 0) {
        if (isRepeat === 'all') playlistIndex = list.length - 1;
        else playlistIndex = 0;
    }
    const item = list[playlistIndex];
    if (typeof playMediaObject === 'function') {
        playMediaObject(item);
    } else if (typeof playAudio === 'function') {
        playAudio(item, 0);
    }
}

/**
 * Updates the active filter for the diagnostic queue and re-renders.
 */
function changeQueueFilter(filter) {
    console.info(">>> [Queue] Changing filter to:", filter);
    window.activeQueueFilter = filter;
    renderAudioQueue();
    if (typeof showToast === 'function') showToast(`Filter: ${filter.toUpperCase()}`, 1500);
}

/**
 * Renders the global playlist in the Playlist tab.
 */
/**
 * renderAudioQueue (v1.45.110)
 * Renders the audio-only portion of the unified global queue.
 */
function renderAudioQueue() {
    if (typeof mwv_trace_render === 'function') mwv_trace_render('PLAYER-QUEUE', 'RENDER-START', { count: window.currentPlaylist.length });
    
    const containers = [
        document.getElementById('playlist-content-render-target'),
        document.getElementById('active-queue-list-render-target'),
        document.getElementById('active-queue-list-render-target-legacy'),
        document.getElementById('active-queue-list-render-target-warteschlange')
    ].filter(Boolean);

    if (containers.length === 0) return;

    // 1. Unified State Access (v1.45.110 SSOT)
    let baseItems = [...(isShuffle ? shuffledPlaylist : window.currentPlaylist)];
    
    // 2. Branch-Aware Rendering Pruning (Audio Player only shows Audio)
    let filteredItems = baseItems.filter(item => !isVideoItem(item));

    // 3. Apply active sub-filters (v1.35.61)
    let isRaw = window.__mwv_raw_mode === true;
    if (window.activeQueueFilter !== 'all' && !isRaw) {
        const catInfo = CATEGORY_MAP[window.activeQueueFilter] || { aliases: [] };
        const allowedLower = (catInfo.aliases || []).map(l => l.toLowerCase());
        const markers = TECH_MAP[window.activeQueueFilter] || [];

        filteredItems = filteredItems.filter(item => {
            const rawCat = (item.category || "").toLowerCase();
            const filename = (item.name || "").toLowerCase();
            const hasMarker = markers.some(m => {
                if (m.startsWith('.')) return filename.endsWith(m);
                if (m.startsWith('_')) return filename.includes(m);
                return item[m] === true;
            });
            if (hasMarker) return true;
            return allowedLower.includes(rawCat);
        });
    }

    // 4. Update UI Counts
    const countEls = document.querySelectorAll('.synced-count');
    countEls.forEach(el => {
        el.innerText = `${filteredItems.length} Titel`;
        el.style.opacity = filteredItems.length === 0 ? '0.3' : '1';
    });
    
    ['queue-item-count', 'queue-item-count-warteschlange', 'queue-item-count-legacy'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.innerText = `${filteredItems.length} Titel`;
    });

    // 5. Build Item DOM
    containers.forEach(list => {
        list.innerHTML = '';
        list.ondragover = (e) => e.preventDefault();
        list.ondrop = (e) => {
            e.preventDefault();
            const data = e.dataTransfer.getData("text/plain");
            if (data) {
                try {
                    const item = JSON.parse(data);
                    window.currentPlaylist.push(item);
                    renderAudioQueue();
            } catch (err) { console.error("[Playlist] Drop error", err); }
        }
    };

        const activeList = filteredItems;
    if (activeList.length === 0) {
        let noMediaHtml = `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-secondary); text-align: center; padding: 60px; background: var(--bg-primary);">
                <div style="font-size: 64px; margin-bottom: 24px; opacity: 0.3; filter: grayscale(1);">🎵</div>
                <h3 style="margin: 0 0 12px 0; font-weight: 800; color: var(--text-primary); letter-spacing: -0.5px;">Warteschlange leer</h3>
                <p style="font-size: 0.95em; max-width: 280px; margin: 0 auto 30px auto; opacity: 0.7;">
                    Füge Lieder aus der Bibliothek hinzu oder ziehe Mediendateien hierher.
                </p>
                <button onclick="switchTab('multimedia')" class="tab-btn active" style="padding: 12px 30px;">
                    Zur Bibliothek
                </button>
            </div>
        `;

            noMediaHtml = `
                <div class="glass-card" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-primary); text-align: center; padding: 40px; background: rgba(0, 122, 255, 0.05); border: 2px dashed var(--accent-color); border-radius: 12px; margin: 20px;">
                    <div style="font-size: 48px; margin-bottom: 15px; filter: drop-shadow(0 0 10px var(--accent-color));">🌀</div>
                    <div style="font-weight: 800; color: var(--accent-color); margin-bottom: 10px; font-size: 1.1em; text-transform: uppercase; letter-spacing: 1px;">Queue Black Hole</div>
                    <p style="font-size: 0.9em; color: var(--text-secondary); max-width: 250px; margin: 0 auto 20px auto; line-height: 1.6;">
                        Deine Mediathek enthält Titel, aber die Warteschlange ist durch Filter blockiert oder nicht synchronisiert.
                    </p>
                    <button onclick="if(typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary()" class="tab-btn active" style="padding: 12px 30px; font-weight: 800;">SYNC & RESET FILTERS</button>
                </div>
            `;

        list.innerHTML = noMediaHtml;
    } else {
        activeList.forEach((item, index) => {
            const div = document.createElement('div');
            div.className = 'legacy-track-item';
            div.draggable = true;
            if (index === playlistIndex) div.classList.add('active');

            const isAvailable = item.available !== false;
            if (!isAvailable) div.classList.add('offline');

            const tags = item.tags || {};
            const stagePrefix = item.stage ? `[${item.stage}] ` : '';
            const titleDisplay = stagePrefix + (item.title || tags.title || item.name || item.id || 'System Recovery Item');
            const artistDisplay = item.artist || tags.artist || 'MWV Recovery';
            
            div.innerHTML = `
                <div style="display: flex; align-items: center; width: 100%; ${!isAvailable ? 'opacity: 0.4; filter: grayscale(1);' : ''}">
                <img class="legacy-track-thumb" src="/cover/${encodeURIComponent(item.name)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';" style="width: 38px; height: 38px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div class="legacy-track-info" style="flex: 1; padding-left: 12px; display: flex; flex-direction: column; justify-content: center; min-width: 0;">
                    <div class="legacy-track-title" style="font-weight: 700; font-size: 13px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">
                        ${titleDisplay}
                        ${!isAvailable ? ' <span style="font-size: 9px; color: #ff5252; font-weight: 900; background: rgba(255,82,82,0.1); padding: 1px 4px; border-radius: 3px; margin-left: 5px;">OFFLINE</span>' : ''}
                    </div>
                    <div class="legacy-track-meta" style="font-size: 11px; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; margin-top: 2px;">${artistDisplay} • <span style="opacity: 0.7;">${tags.album || 'No Album'}</span></div>
                </div>
                <div class="item-actions" style="display: flex; gap: 4px; align-items: center; opacity: 0; transition: opacity 0.2s;">
                    <button onclick="event.stopPropagation(); moveItemUp(${index})" title="Nach oben" style="background:transparent; border:none; padding: 6px; color: var(--text-secondary); cursor:pointer;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="18 15 12 9 6 15"/></svg>
                    </button>
                    <button onclick="event.stopPropagation(); moveItemDown(${index})" title="Nach unten" style="background:transparent; border:none; padding: 6px; color: var(--text-secondary); cursor:pointer;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="6 9 12 15 18 9"/></svg>
                    </button>
                    <button onclick="event.stopPropagation(); removeItem(${index})" title="Entfernen" style="background:transparent; border:none; padding: 6px; color: #ff5252; cursor:pointer;">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M3 6h18m-2 0v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6m3 0V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/></svg>
                    </button>
                </div>
            </div>
        `;

        div.onmouseenter = () => { div.querySelector('.item-actions').style.opacity = '1'; };
        div.onmouseleave = () => { div.querySelector('.item-actions').style.opacity = '0'; };

        div.onclick = () => {
            if (!isAvailable) {
                if (typeof showToast === 'function') showToast("Medium ist offline oder verschoben.", "warn");
                return;
            }
            playlistIndex = index;
            if (typeof playMediaObject === 'function') {
                playMediaObject(item);
            } else {
                playAudio(item, 0);
            }
            renderAudioQueue();
        };

        // Internal Sortable DnD
        div.ondragstart = (e) => {
            e.dataTransfer.setData("text/plain", JSON.stringify({ index: index, type: 'reorder' }));
            div.style.opacity = '0.4';
        };
        div.ondragend = () => { div.style.opacity = '1'; };
        
        div.ondragover = (e) => {
            e.preventDefault();
            div.style.borderTop = '2px solid var(--accent-color)';
        };
        div.ondragleave = () => {
            div.style.borderTop = '1px solid var(--border-color)';
        };
        div.ondrop = (e) => {
            e.preventDefault();
            div.style.borderTop = '1px solid var(--border-color)';
            try {
                const data = JSON.parse(e.dataTransfer.getData("text/plain"));
                if (data && data.type === 'reorder') {
                    const fromIndex = data.index;
                    const toIndex = index;
                    if (fromIndex === toIndex) return;
                    const movedItem = currentPlaylist.splice(fromIndex, 1)[0];
                    currentPlaylist.splice(toIndex, 0, movedItem);
                    renderAudioQueue();
                }
            } catch(err) {}
        };
        
        if (typeof showContextMenu === 'function') {
            div.addEventListener('contextmenu', (e) => {
                showContextMenu(e, item);
            });
        }
        
        list.appendChild(div);
        });
    }
    }); // v1.41.00 Final closing block
}

function resetAllFilters() {
    console.warn(">>> [Recovery] resetAllFilters triggered.");
    window.activeQueueFilter = 'all';
    window.__mwv_raw_mode = false;
    
    // Default the UI select if it exists
    const filterSelect = document.getElementById('queue-type-filter');
    if (filterSelect) filterSelect.value = 'all';
    
    if (typeof syncQueueWithLibrary === 'function') syncQueueWithLibrary();
    if (typeof renderAudioQueue === 'function') renderAudioQueue();
    
    if (typeof showToast === 'function') showToast("Alle Filter zurückgesetzt & Sync erzwungen.", "success");
}

function moveItemUp(index) {
    if (index <= 0) return;
    [currentPlaylist[index], currentPlaylist[index - 1]] = [currentPlaylist[index - 1], currentPlaylist[index]];
    if (playlistIndex === index) playlistIndex--;
    else if (playlistIndex === index - 1) playlistIndex++;
    renderAudioQueue();
}

function moveItemDown(index) {
    if (index >= currentPlaylist.length - 1) return;
    [currentPlaylist[index], currentPlaylist[index + 1]] = [currentPlaylist[index + 1], currentPlaylist[index]];
    if (playlistIndex === index) playlistIndex++;
    else if (playlistIndex === index + 1) playlistIndex--;
    renderAudioQueue();
}

function removeItem(index) {
    currentPlaylist.splice(index, 1);
    if (playlistIndex === index) playlistIndex = -1;
    else if (playlistIndex > index) playlistIndex--;
    renderAudioQueue();
}

// --- Player Dashboard Logic (v1.34) ---
let playerLibrarySearch = '';
let playerMainView = 'now-playing';

function switchPlayerMainView(viewId) {
    // legacy mapping for v1.33 compatibility
    if (viewId === 'audioplayer') viewId = 'warteschlange';
    
    playerMainView = viewId;
    document.querySelectorAll('.player-view-container').forEach(el => el.style.display = 'none');
    document.querySelectorAll('.player-view-container').forEach(el => el.classList.remove('active'));
    
    const target = document.getElementById(`player-view-${viewId}`);
    if (target) {
        target.style.display = 'flex';
        setTimeout(() => target.classList.add('active'), 10);
    }

    if (viewId === 'warteschlange') renderAudioQueue();
}


function handlePlayerLibrarySearch(val) {
    playerLibrarySearch = val;
    renderFullLibraryInPlayer();
}

/**
 * Renders the full indexed library inside the player tab (v1.33 style Restoration).
 */

function addToQueue(idx) {
    if (typeof allLibraryItems !== 'undefined' && allLibraryItems[idx]) {
        currentPlaylist.push(allLibraryItems[idx]);
        renderAudioQueue();
        if (typeof showToast === 'function') showToast("Zur Warteschlange hinzugefügt", "success");
    }
}

/**
 * Renders the full indexed library inside the player tab.
 */
function renderFullLibraryInPlayer() {
    const container = document.getElementById('player-library-grid');
    if (!container) return;

    if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
        container.innerHTML = '<div style="padding: 40px; color: var(--text-secondary);">No indexed items found. Refresh library in the Library tab.</div>';
        return;
    }

    let items = allLibraryItems;
    if (playerLibrarySearch) {
        const q = playerLibrarySearch.toLowerCase();
        items = items.filter(i => (i.name || '').toLowerCase().includes(q) || (i.tags?.title || '').toLowerCase().includes(q));
    }

    container.innerHTML = items.map((item, idx) => {
        const artwork = `/cover/${encodeURIComponent(item.name)}`;
        const title = item.tags?.title || item.name;
        const artist = item.tags?.artist || 'Unknown Artist';
        
        return `
            <div class="grid-item" onclick="addAndPlayNow(this, ${JSON.stringify(item).replace(/"/g, '&quot;')})" style="animation: fadeIn 0.3s ease forwards;">
                <div class="grid-cover" style="background-image: url('${artwork}')"></div>
                <div class="grid-info">
                    <div class="grid-title">${title}</div>
                    <div class="grid-meta">${artist}</div>
                </div>
            </div>
        `;
    }).join('');
}

function addAndPlayNow(el, item) {
    if (typeof currentPlaylist !== 'undefined') {
        currentPlaylist.push(item);
        playlistIndex = currentPlaylist.length - 1;
        if (typeof renderAudioQueue === 'function') renderAudioQueue();
        if (typeof playAudio === 'function') playAudio(item);
        // Switch back to now playing to show the progress
        switchPlayerMainView('now-playing');
    }
}

/**
 * Synchronizes the player queue with the current library state (v1.45.110).
 * Populates window.currentPlaylist with branch-aut/**
 * renderGlobalPlaylist (Wrapper for compatibility)
 */
function renderGlobalPlaylist() {
    renderAudioQueue();
}

window.renderGlobalPlaylist = renderGlobalPlaylist;
window.renderAudioQueue = renderAudioQueue;
 renderAudioQueue();
            if (typeof appendUiTrace === 'function') {
                appendUiTrace(`[Debug] Audio Queue Bootstrapped with ${currentPlaylist.length} items.`);
            }
        }
    } catch (err) {
        console.error("[Audio] [Debug] Failed to fetch mock stage 3:", err);
    }
}

// [v1.34 REMOVED: Automatic timeout relocated to Quick Sign-off Test script]

/**
 * Premium Sidebar: Chapters/Tracks Renderer (v1.34)
 * Populates the player-chapters-list with tracks from the same album or parent directory.
 */
function renderAudiobookDetails(item) {
    const chapterList = document.getElementById('player-chapters-list');
    if (!chapterList) return;

    chapterList.innerHTML = '<div style="font-size: 11px; color: var(--text-secondary); opacity: 0.5;">Suche Kapitel...</div>';

    // 1. Determine "same context" (Album name or Parent Directory)
    const albumName = item.tags?.album || item.album;
    const parentDir = item.path ? item.path.substring(0, item.path.lastIndexOf('/')) : null;

    if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
        chapterList.innerHTML = '<div style="font-size: 11px; color: var(--text-secondary);">Mediathek nicht geladen.</div>';
        return;
    }

    // 2. Filter tracks
    let tracks = allLibraryItems.filter(i => {
        if (albumName && i.tags?.album === albumName) return true;
        if (parentDir && i.path && i.path.startsWith(parentDir)) return true;
        return false;
    });

    // Sort by track number or filename
    tracks.sort((a, b) => {
        const ta = parseInt(a.tags?.track || 0);
        const tb = parseInt(b.tags?.track || 0);
        if (ta && tb) return ta - tb;
        return a.name.localeCompare(b.name);
    });

    // 3. Render
    chapterList.innerHTML = '';
    
    if (tracks.length === 0) {
        chapterList.innerHTML = '<div style="font-size: 11px; color: var(--text-secondary);">Keine weiteren Kapitel gefunden.</div>';
        return;
    }

    tracks.forEach(track => {
        const isActive = track.path === item.path;
        const durationStr = track.duration ? formatTime(track.duration) : '--:--';
        
        const trackDiv = document.createElement('div');
        trackDiv.className = `chapter-item ${isActive ? 'active' : ''}`;
        trackDiv.onclick = () => {
             if (typeof playMediaObject === 'function') playMediaObject(track);
             else playAudio(track, 0);
        };
        
        trackDiv.innerHTML = `
            <div style="display: flex; align-items: center; gap: 10px; min-width: 0;">
                <div class="chapter-index" style="opacity: 0.5; font-size: 10px; font-weight: 800; min-width: 18px;">
                    ${track.tags?.track ? track.tags.track.toString().padStart(2, '0') : '•'}
                </div>
                <div class="chapter-title" style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-size: 12px;">
                    ${track.tags?.title || track.name}
                </div>
            </div>
            <div class="chapter-duration" style="opacity: 0.5; font-size: 10px; margin-left: 8px;">
                ${durationStr}
            </div>
        `;
        
        chapterList.appendChild(trackDiv);
    });
}
/**
 * Updates the 'Detailed Mode' diagnostic sidebar with technical metadata and parser times.
 */
function updateDetailedDiagnostics() {
    const sidebar = document.getElementById('player-detailed-sidebar');
    if (!sidebar || !sidebar.classList.contains('active')) return;

    // Get current item from global state (assumed available as currentMetadata/currentItem)
    const item = (typeof currentMetadata !== 'undefined') ? currentMetadata : (typeof currentItem !== 'undefined') ? currentItem : null;
    if (!item) return;

    // 1. Media Info Header
    const primaryEl = document.getElementById('diag-media-primary');
    if (primaryEl) {
        primaryEl.innerHTML = `
            <div style="font-weight: 800; color: var(--accent-color); margin-bottom: 4px;">${item.name || 'Kein Titel'}</div>
            <div style="font-size: 10px; opacity: 0.7;">${item.path || '-'}</div>
        `;
    }

    // 2. Parser Times (JSON-based mapping)
    const metricsEl = document.getElementById('diag-parser-metrics');
    if (metricsEl && item.parser_times) {
        const pt = item.parser_times;
        metricsEl.innerHTML = `
            <div style="display: flex; justify-content: space-between;"><span>filename:</span> <span style="color: var(--accent-color)">${pt.filename || '0.0ms'}</span></div>
            <div style="display: flex; justify-content: space-between;"><span>container:</span> <span style="color: var(--accent-color)">${pt.container || '0.0ms'}</span></div>
            <div style="display: flex; justify-content: space-between;"><span>mutagen:</span> <span style="color: var(--accent-color)">${pt.mutagen || '0.0ms'}</span></div>
            <div style="display: flex; justify-content: space-between;"><span>pymediainfo:</span> <span style="color: var(--accent-color)">${pt.pymediainfo || '0.0ms'}</span></div>
            <div style="display: flex; justify-content: space-between;"><span>ffprobe:</span> <span style="color: var(--accent-color)">${pt.ffprobe || '0.0ms'}</span></div>
            <div style="display: flex; justify-content: space-between;"><span>ffmpeg:</span> <span style="color: var(--accent-color)">${pt.ffmpeg || '0.0ms'}</span></div>
        `;
    }

    // 3. Transcoding / Pipeline Status
    const transcodeEl = document.getElementById('diag-transcode-status');
    if (transcodeEl) {
        const isTranscoded = item.is_transcoded || (item.path && (item.path.endsWith('.flac') || item.path.endsWith('.wav')));
        transcodeEl.innerHTML = isTranscoded 
            ? `<span style="color: #ff9800; font-weight: 800;">Realtime FLAC -> Browser/MSE</span>`
            : `<span style="color: #4caf50; font-weight: 800;">Direct Stream (Native)</span>`;
    }
}

// Hook into playback start
if (typeof playAudio === 'function') {
    const originalPlayAudio = playAudio;
    playAudio = function(item, startTime) {
        originalPlayAudio(item, startTime);
        setTimeout(updateDetailedDiagnostics, 200); // Small delay to ensure item is loaded
    };
}

/**
 * Atomic Hydration Watcher (v1.41.00)
 * Ensures the player queue remains synchronized with the backend library.
 * Periodically checks for "zombie" items and triggers hydration if the queue is empty.
 */
function startAtomicHydrationWatcher() {
    console.info(">>> [Diagnostic] Starting Atomic Hydration Watcher...");
    setInterval(() => {
        try {
            // 1. Hydration Check: If queue is empty but library has items, sync up.
            if (currentPlaylist.length === 0 && typeof allLibraryItems !== 'undefined' && allLibraryItems.length > 0) {
                console.warn("[Watcher] Queue is empty. Triggering automatic hydration...");
                syncQueueWithLibrary();
            }

            // 2. Health Check: Remove items with undefined/null paths (Zombies)
            const initialCount = currentPlaylist.length;
            currentPlaylist = currentPlaylist.filter(item => item && (item.path || item.id) && item.path !== 'undefined');
            
            if (currentPlaylist.length !== initialCount) {
                console.error(`[Watcher] Purged ${initialCount - currentPlaylist.length} zombie items from queue.`);
                renderAudioQueue();
            }

            // 3. UI Status Sync (Optional extension for Diagnostic Hub)
            const hubStatus = document.getElementById('hub-sync-status');
            if (hubStatus) {
                hubStatus.innerText = `Synced (${currentPlaylist.length} items)`;
            }
        } catch (e) {
            console.error("[Watcher] Hydration failure:", e);
        }
    }, 30000); // 30s heartbeat
}

// Start on load
document.addEventListener('DOMContentLoaded', () => {
    startAtomicHydrationWatcher();
});

// Created with MWV v1.45.100-EVO-REBUILD
