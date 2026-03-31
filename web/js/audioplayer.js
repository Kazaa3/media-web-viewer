/**
 * Audio Playback Module
 * Manages the HTML5 Audio Pipeline, playlists, and playback state.
 */

// --- Audio State ---
let playlistIndex = -1;
let isShuffle = false;
let isRepeat = 'off'; // 'off', 'all', 'one'
let shuffledPlaylist = [];

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
}


/**
 * Main Audio Playback entry point.
 */
function playAudio(item, startTime = 0) {
    const pipeline = document.getElementById('native-html5-audio-pipeline-element');
    if (!pipeline) return;

    const proxyUrl = "/media/" + encodeURIComponent(item.path);
    const logMsg = `[Audio] Attempting to play: ${item.name} | Path: ${item.path} | Proxy: ${proxyUrl}`;
    console.log(logMsg);
    if (typeof appendUiTrace === 'function') appendUiTrace(logMsg);
    
    pipeline.src = proxyUrl;
    
    // Logic: Resume for audiobooks, else start at 0
    const shouldResume = item.category === 'Audiobook' || item.category === 'Hörbruch';
    pipeline.currentTime = (shouldResume && startTime > 0) ? startTime : 0;

    pipeline.play().catch(e => {
        console.error('Audio playback failed:', e);
        if (typeof showToast === 'function') showToast(`Playback Error: ${e.message}`, 'error');
    });
    
    if (typeof eel !== "undefined" && typeof eel.log_playback_event === 'function') {
        eel.log_playback_event("START", item.name);
        eel.play_media(item.path)();
    }

    // Persist position for audiobooks
    pipeline.ontimeupdate = () => {
        const now = pipeline.currentTime;
        if (Math.abs(now - (pipeline.lastPersist || 0)) > 10) {
            pipeline.lastPersist = now;
            if (typeof eel !== 'undefined' && typeof eel.update_playback_position === 'function') {
                eel.update_playback_position(item.name, now)();
            }
        }
    };
    
    if (typeof updateMediaSidebar === 'function') updateMediaSidebar(item, item.path);
}

/**
 * Updates the media sidebar with item information.
 */
function updateMediaSidebar(item, path) {
    const tags = item.tags || {};
    
    if (typeof safeText === 'function') {
        safeText('sidebar-metadata-primary-string-renderer', tags.title || item.name);
        const artistStr = tags.albumartist && tags.albumartist !== tags.artist ? tags.artist + " (Album: " + tags.albumartist + ")" : (tags.artist || 'Unknown');
        safeText('sidebar-metadata-secondary-string-renderer', artistStr);
        safeText('parser-mediainfo-primary', tags.title || item.name);
        safeText('parser-mediainfo-secondary', artistStr);
    }

    const coverUrl = "/cover/" + encodeURIComponent(item.name);
    ['sidebar-artwork-raster-buffer', 'parser-mediainfo-artwork', 'footer-artwork-raster-buffer', 'big-player-artwork'].forEach(id => {
        const img = document.getElementById(id);
        if (img) {
            img.src = coverUrl;
            img.style.opacity = "1";
            img.onerror = () => img.src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';
        }
    });

    if (typeof safeText === 'function') {
        safeText('big-player-title', tags.title || item.name);
        safeText('big-player-artist', tags.artist || 'Unknown');
        safeText('big-bitrate-display', tags.bitrate || '-');
        safeText('big-samplerate-display', tags.samplerate || '-');
    }

    // Tech Details
    let badgeText = [tags.codec, tags.bitdepth, tags.samplerate, tags.bitrate].filter(Boolean).join(' | ');
    if (item.is_transcoded) badgeText = '[TRANSCODED] ' + badgeText;

    if (typeof safeText === 'function') {
        if (badgeText) {
            safeText('sidebar-status-tag-visualizer', badgeText);
            safeStyle('sidebar-status-tag-visualizer', 'display', 'inline-block');
        } else {
            safeStyle('sidebar-status-tag-visualizer', 'display', 'none');
        }
    }

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
        document.getElementById('active-queue-list-render-target')
    ].filter(el => el !== null);

    const countEl = document.getElementById('queue-item-count');
    if (countEl) countEl.innerText = `${currentPlaylist.length} Items`;

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
                    Füge Lieder aus der Bibliothek hinzu oder ziehe Dateien hierher.
                </p>
                <button onclick="switchTab('library')" class="tab-btn active" style="padding: 12px 30px;">
                    Zur Bibliothek
                </button>
            </div>
        `;
        return;
    }

    activeList.forEach((item, index) => {
        let div = document.createElement('div');
        div.className = 'implementation-encapsulated-state-buffer-node';
        if (index === playlistIndex) div.classList.add('playing');

        let tags = item.tags || {};
        let titleDisplay = tags.title || item.name || (typeof t === 'function' ? t('lib_unknown_title') : 'Unknown');
        let artistDisplay = tags.artist || (typeof t === 'function' ? t('lib_unknown_artist') : 'Unknown');
        let badgeHtml = (typeof getCategoryBadgeHtml === 'function') ? getCategoryBadgeHtml(item) : '';

        div.innerHTML = `
            <div style="position:relative; display:inline-block; margin-right:12px; flex-shrink:0;">
                <img class="media-cover" style="margin-right:0;" src="/cover/${encodeURIComponent(item.name)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='; this.style.backgroundColor='transparent';" alt="">
                ${badgeHtml}
            </div>
            <div class="media-info" style="flex: 1;">
                <strong style="font-size: 0.9em;">${titleDisplay}</strong>
                <span style="font-size: 0.8em;">${artistDisplay}</span>
            </div>
            <div style="display: flex; align-items: center; gap: 8px; margin-left: auto; padding-right: 10px;">
                <div class="playlist-controls" style="display: flex; gap: 5px;">
                    <button onclick="event.stopPropagation(); moveItemUp(${index})" title="${typeof t === 'function' ? t('pl_move_up') : 'Up'}"
                        ${isShuffle ? 'disabled style="opacity:0.3; cursor:default;"' : 'style="background:transparent; border:none; cursor:pointer;"'}>
                        ⬆️
                    </button>
                    <button onclick="event.stopPropagation(); moveItemDown(${index})" title="${typeof t === 'function' ? t('pl_move_down') : 'Down'}"
                        ${isShuffle ? 'disabled style="opacity:0.3; cursor:default;"' : 'style="background:transparent; border:none; cursor:pointer;"'}>
                        ⬇️
                    </button>
                    <button onclick="event.stopPropagation(); removeItem(${index})" title="${typeof t === 'function' ? t('pl_remove') : 'Remove'}" style="background:transparent; border:none; cursor:pointer; color: #c0392b;">
                        <svg width="12" height="12"><use href="#icon-delete"></use></svg>
                    </button>
                </div>
            </div>
        `;

        div.onclick = () => {
            playlistIndex = index;
            if (typeof playAudio === 'function') playAudio(item, 0);
            renderPlaylist();
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

// Initialize
window.addEventListener('DOMContentLoaded', initAudioPipeline);
