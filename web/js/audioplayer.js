/**
 * Audio Playback Module
 * Manages the HTML5 Audio Pipeline, playlists, and playback state.
 */

// --- Audio State ---
let playlistIndex = -1;
let isShuffle = false;
let isRepeat = 'off'; // 'off', 'all', 'one'
let shuffledPlaylist = [];
let audioContext = null;
let analyser = null;
let dataArray = null;
let visualizerAnimationId = null;
let visualizerStyle = localStorage.getItem('mwv_visualizer_style') || 'bars'; // 'bars', 'circle', 'wave'

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
    const ext = item.path ? item.path.slice(((item.path.lastIndexOf(".") - 1) >>> 0) + 2).toLowerCase() : "";
    if (!pipeline) return;

    const proxyUrl = "/media/" + encodeURIComponent(item.path);
    const logMsg = `[Audio] Attempting to play: ${item.name} | Path: ${item.path} | Proxy: ${proxyUrl}`;
    mwv_trace('PLAYER-EVENT', 'PLAYBACK-START', { name: item.name, path: item.path, proxy: proxyUrl });
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
        
        // Sync Legacy & Visualizer Views
        ['legacy', 'visualizer'].forEach(view => {
            safeText(`big-player-title-${view}`, tags.title || item.name);
            safeText(`big-player-artist-${view}`, tags.artist || 'Unknown Artist');
            
            safeText(`spec-codec-${view}`, tags.codec || 'MP3');
            safeText(`spec-bitrate-${view}`, tags.bitrate || '320 kbps');
            
            if (view === 'legacy') {
                safeText('spec-bitdepth-legacy', tags.bitdepth ? tags.bitdepth + ' Bit' : '16 Bit');
                safeText('spec-samplerate-legacy', tags.samplerate || '44.1 kHz');
                safeText('spec-album-line-legacy', tags.album || 'No Album');
                
                const trackStr = `${tags.year || '2026'} • ${tags.genre || 'General'} • Track ${tags.track ? tags.track.toString().padStart(2, '0') : '01'}`;
                safeText('spec-track-details-legacy', trackStr);
                safeText('player-file-path-legacy', path || item.path || 'Unknown Path');
            }
        });
    }


    const coverUrl = "/cover/" + encodeURIComponent(item.name);
    const artworkIds = [
        'sidebar-artwork-raster-buffer', 
        'parser-mediainfo-artwork', 
        'footer-artwork-raster-buffer', 
        'big-player-artwork-legacy', 
        'big-player-artwork-visualizer'
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
    if (typeof renderPlaylist === 'function') renderPlaylist();
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
    if (typeof playAudio === 'function') playAudio(item, 0);
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
    if (typeof playAudio === 'function') playAudio(item, 0);
}

/**
 * Renders the global playlist in the Playlist tab.
 */
function renderPlaylist() {
    const containers = [
        document.getElementById('playlist-content-render-target'),
        document.getElementById('active-queue-list-render-target'),
        document.getElementById('active-queue-list-render-target-legacy'),
        document.getElementById('active-queue-list-render-target-warteschlange')
    ].filter(Boolean);

    const countEls = document.querySelectorAll('.synced-count');
    countEls.forEach(el => el.innerText = `${currentPlaylist.length} Titel`);
    
    const countEl = document.getElementById('queue-item-count');
    if (countEl) countEl.innerText = `${currentPlaylist.length} Titel`;

    console.log(`[Audio] Rendering playlist on ${containers.length} containers. Items: ${currentPlaylist.length}`);
    if (containers.length === 0) return;

    containers.forEach(list => {
        list.innerHTML = ''; // Clear existing

        list.ondragover = (e) => e.preventDefault();
    list.ondrop = (e) => {
        e.preventDefault();
        const data = e.dataTransfer.getData("text/plain");
        if (data) {
            try {
                const item = JSON.parse(data);
                currentPlaylist.push(item);
                renderPlaylist();
            } catch (err) { console.error("[Playlist] Drop error", err); }
        }
    };

    const activeList = isShuffle ? shuffledPlaylist : currentPlaylist;
    if (activeList.length === 0) {
        list.innerHTML = `
            <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; color: var(--text-secondary); text-align: center; padding: 60px; background: var(--bg-primary);">
                <div style="font-size: 64px; margin-bottom: 24px; opacity: 0.3; filter: grayscale(1);">🎵</div>
                <h3 style="margin: 0 0 12px 0; font-weight: 800; color: var(--text-primary); letter-spacing: -0.5px;">Warteschlange leer</h3>
                <p style="font-size: 0.95em; max-width: 280px; margin: 0 auto 30px auto; opacity: 0.7;">
                    Füge Lieder aus der Bibliothek hinzu oder ziehe Mediendateien hierher.
                </p>
                <button onclick="switchTab('library')" class="tab-btn active" style="padding: 12px 30px;">
                    Zur Bibliothek
                </button>
            </div>
        `;
        return;
    }

    activeList.forEach((item, index) => {
        const div = document.createElement('div');
        div.className = 'legacy-track-item';
        div.draggable = true;
        if (index === playlistIndex) div.classList.add('active');

        const tags = item.tags || {};
        const titleDisplay = tags.title || item.name || 'Unknown Title';
        const artistDisplay = tags.artist || 'Unknown Artist';
        
        div.innerHTML = `
            <div style="display: flex; align-items: center; width: 100%;">
                <img class="legacy-track-thumb" src="/cover/${encodeURIComponent(item.name)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';" style="width: 38px; height: 38px; border-radius: 4px; object-fit: cover; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <div class="legacy-track-info" style="flex: 1; padding-left: 12px; display: flex; flex-direction: column; justify-content: center; min-width: 0;">
                    <div class="legacy-track-title" style="font-weight: 700; font-size: 13px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; line-height: 1.2;">${titleDisplay}</div>
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
            playlistIndex = index;
            playAudio(item, 0);
            renderPlaylist();
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
                    renderPlaylist();
                }
            } catch(err) {}
        };
        
        if (typeof showContextMenu === 'function') {
            div.oncontextmenu = (e) => showContextMenu(e, item);
        }
        
        list.appendChild(div);
    });
});
}

function moveItemUp(index) {
    if (index <= 0) return;
    [currentPlaylist[index], currentPlaylist[index - 1]] = [currentPlaylist[index - 1], currentPlaylist[index]];
    if (playlistIndex === index) playlistIndex--;
    else if (playlistIndex === index - 1) playlistIndex++;
    renderPlaylist();
}

function moveItemDown(index) {
    if (index >= currentPlaylist.length - 1) return;
    [currentPlaylist[index], currentPlaylist[index + 1]] = [currentPlaylist[index + 1], currentPlaylist[index]];
    if (playlistIndex === index) playlistIndex++;
    else if (playlistIndex === index + 1) playlistIndex--;
    renderPlaylist();
}

function removeItem(index) {
    currentPlaylist.splice(index, 1);
    if (playlistIndex === index) playlistIndex = -1;
    else if (playlistIndex > index) playlistIndex--;
    renderPlaylist();
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

    if (viewId === 'mediengalerie') renderItemGallery();
    if (viewId === 'warteschlange') renderPlaylist();
}

let gallerySource = 'media';
function setGallerySource(source) {
    gallerySource = source;
    if (source === 'custom') {
        if (typeof eel !== 'undefined' && eel.pick_directory) {
            eel.pick_directory()((res) => {
                if (res) {
                    if (typeof scan === 'function') scan(res, true);
                }
            });
        }
    } else {
        renderItemGallery();
    }
}

function handlePlayerLibrarySearch(val) {
    playerLibrarySearch = val;
    renderFullLibraryInPlayer();
}

/**
 * Renders the full indexed library inside the player tab (v1.33 style Restoration).
 */
window.renderItemGallery = function() {
    const container = document.getElementById('player-gallery-render-target');
    if (!container) {
        console.warn("[Gallery] Gallery container 'player-gallery-render-target' not found in DOM.");
        if (typeof appendUiTrace === 'function') appendUiTrace("[Gallery] CRITICAL: Container missing!", "DB-ERROR");
        return;
    }

    if (typeof appendUiTrace === 'function') {
        appendUiTrace(`[Gallery] renderItemGallery() called. allLibraryItems=${typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : 'undefined'}`, "UI-INFO");
    }

    if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
        container.innerHTML = `
            <div style="padding: 60px; text-align: center; color: var(--text-secondary);">
                <div style="font-size: 48px; opacity: 0.2; margin-bottom: 20px;">📂</div>
                <div style="font-weight: 700; color: var(--text-primary); margin-bottom: 8px;">Galerie ist leer</div>
                <p style="font-size: 11px; margin-bottom: 20px;">Keine indizierten Elemente gefunden.</p>
                <button onclick="scan('./media', true)" class="tab-btn sm" style="padding: 8px 20px;">Media Scan starten</button>
            </div>
        `;
        return;
    }

    // ── Broadened categories: allow all by default ──
    let items = allLibraryItems;

    if (typeof appendUiTrace === 'function') {
        appendUiTrace(`[Gallery] After audio filter: ${items.length} / ${allLibraryItems.length} items.`, "UI-INFO");
    }

    // Source Filtering
    if (gallerySource === 'media') {
        items = items.filter(i => (i.path || '').includes('/media/'));
    }

    const countEl = document.getElementById('gallery-item-count');
    if (countEl) countEl.innerText = `${items.length} Lieder`;

    container.innerHTML = '';
    
    if (items.length === 0) {
        container.innerHTML = '<div style="padding: 40px; text-align: center; opacity: 0.5;">Keine Lieder in dieser Quelle gefunden.</div>';
        return;
    }

    items.forEach((item, idx) => {
        const div = document.createElement('div');
        div.className = 'legacy-track-item';
        
        const tags = item.tags || {};
        const titleDisplay = tags.title || item.name || 'Unknown Title';
        const artistDisplay = tags.artist || 'Unknown Artist';
        
        div.innerHTML = `
            <img class="legacy-track-thumb" src="/cover/${encodeURIComponent(item.name)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';" style="width: 32px; height: 32px; border-radius: 4px; object-fit: cover;">
            <div class="legacy-track-info" style="flex: 1; padding-left: 12px; display: flex; flex-direction: column; justify-content: center; min-width: 0;">
                <div class="legacy-track-title" style="font-weight: 700; font-size: 12px; color: var(--text-primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${titleDisplay}</div>
                <div class="legacy-track-meta" style="font-size: 10px; color: var(--text-secondary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${artistDisplay} • <span style="opacity: 0.7;">${tags.album || 'No Album'}</span></div>
            </div>
            <button onclick="event.stopPropagation(); addToQueue(${idx})" class="item-action-pill" style="opacity: 0; transition: opacity 0.2s;">+</button>
        `;

        div.onmouseenter = () => { div.querySelector('.item-action-pill').style.opacity = '1'; };
        div.onmouseleave = () => { div.querySelector('.item-action-pill').style.opacity = '0'; };

        div.onclick = () => {
            playAudio(item, 0);
        };
        
        container.appendChild(div);
    });

    if (typeof appendUiTrace === 'function') {
        appendUiTrace(`[Gallery] ✓ ${items.length} items appended to DOM!`, "SUCCESS");
    }
    if (typeof eel !== 'undefined' && eel.report_items_spawned) {
        eel.report_items_spawned(items.length, 'mediengalerie');
    }
}

function addToQueue(idx) {
    if (typeof allLibraryItems !== 'undefined' && allLibraryItems[idx]) {
        currentPlaylist.push(allLibraryItems[idx]);
        renderPlaylist();
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
        if (typeof renderPlaylist === 'function') renderPlaylist();
        if (typeof playAudio === 'function') playAudio(item);
        // Switch back to now playing to show the progress
        switchPlayerMainView('now-playing');
    }
}

/**
 * Synchronizes the player queue with the current library state.
 */
function syncQueueWithLibrary() {
    if (typeof allLibraryItems === 'undefined' || allLibraryItems.length === 0) {
        console.warn("[Audio] syncQueueWithLibrary: No library items found to sync.");
        return;
    }
    
    console.log(`[Audio] Syncing queue with ${allLibraryItems.length} items...`);
    const audioItems = allLibraryItems.filter(i => 
        i.category === 'Audio' || 
        i.category === 'Album' || 
        i.category === 'Hörbuch' ||
        i.category === 'Klassik' ||
        i.category === 'Podcast' ||
        i.category === 'Compilation' ||
        i.category === 'Single' ||
        i.category === 'Radio'
    );
    
    if (audioItems.length > 0) {
        currentPlaylist = [...audioItems];
        if (playlistIndex === -1) playlistIndex = 0;
        if (typeof renderPlaylist === 'function') renderPlaylist();
        if (typeof renderFullLibraryInPlayer === 'function') renderFullLibraryInPlayer();
    }
}

// Initialize
window.addEventListener('DOMContentLoaded', () => {
    initAudioPipeline();
    
    // Sync with library if already loaded
    if (typeof allLibraryItems !== 'undefined' && allLibraryItems.length > 0) {
        syncQueueWithLibrary();
    }
});
// --- Initialize on module load ---
document.addEventListener('DOMContentLoaded', () => {
    initAudioPipeline();
    // Register global playback probe hook
    window._probe_playback = (index = 0) => {
        const items = document.querySelectorAll('.legacy-track-item');
        if (items[index]) items[index].click();
    };
});

// v1.34 Auto-Sync: Populate queue when library settles
document.addEventListener('mwv_library_ready', (e) => {
    console.log(`[Audio] Library Ready Event: ${e.detail.count} items. Syncing queue...`);
    syncQueueWithLibrary();
});

/**
 * Stage 0: Mock Bootstrap Fail-safe (Diagnostic Utility)
 * Ensures the GUI can be verified even without real files.
 */
window.bootstrapMockQueue = function() {
    if (currentPlaylist.length > 0) return;
    
    console.warn("[Audio] [Debug] Bootstrapping mock queue for GUI verification...");
    const mockItems = [
        {
            name: "01 - Anfangsstadium RMX.mp3",
            category: "Audio",
            is_mock: true,
            tags: {
                title: "Anfangsstadium RMX",
                artist: "Megaloh",
                album: "Auf Ewig Mixtape",
                year: "2013",
                genre: "Hip-Hop",
                track: "01"
            }
        },
        {
            name: "01 - Einfach & Leicht.mp3",
            category: "Audio",
            is_mock: true,
            tags: {
                title: "Einfach & Leicht",
                artist: "Benjie",
                album: "Schatten & Licht",
                year: "2015",
                genre: "Dancehall",
                track: "01"
            }
        },
        {
            name: "Absolute Beginner - Hammerhart.m4a",
            category: "Audio",
            is_mock: true,
            tags: {
                title: "Hammerhart (Denyo77 remix)",
                artist: "Absolute Beginner feat. D-Flame & Illo 77",
                album: "Boombule: Bambule Remixed",
                year: "2000",
                genre: "Deutschrap/Hip-Hop",
                track: "01"
            }
        }
    ];
    
    currentPlaylist = [...mockItems];
    renderPlaylist();
    
    if (typeof appendUiTrace === 'function') {
        appendUiTrace("[Debug] Audio Queue Bootstrapped with 3 mock items.");
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
        trackDiv.style = `
            display: flex; justify-content: space-between; align-items: center; 
            padding: 8px 12px; border-radius: 8px; cursor: pointer; 
            background: ${isActive ? 'var(--accent-color)' : 'rgba(0,0,0,0.03)'}; 
            color: ${isActive ? 'white' : 'var(--text-primary)'}; 
            font-size: 12px; font-weight: ${isActive ? '700' : '500'};
            transition: all 0.2s;
            margin-bottom: 4px;
        `;
        
        trackDiv.innerHTML = `
            <span style="overflow: hidden; text-overflow: ellipsis; white-space: nowrap; margin-right: 10px;">
                ${track.tags?.track ? track.tags.track + '. ' : ''}${track.tags?.title || track.name}
            </span>
            <span style="font-size: 10px; opacity: 0.7;">${durationStr}</span>
        `;
        
        trackDiv.onclick = (e) => {
            e.stopPropagation();
            if (typeof playAudio === 'function') playAudio(track);
        };

        // Hover effect via JS
        trackDiv.onmouseover = () => { if(!isActive) trackDiv.style.background = 'rgba(0,122,255,0.1)'; };
        trackDiv.onmouseout = () => { if(!isActive) trackDiv.style.background = 'rgba(0,0,0,0.03)'; };

        chapterList.appendChild(trackDiv);
    });
}
