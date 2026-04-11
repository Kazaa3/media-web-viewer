/**
 * video_helpers.js - Video Engine Selection & UI Orchestration
 * Extracted from app.html
 */

let currentVideoItem = null;
let currentVideoPath = null;

/**
 * Selects the main playback engine and updates the UI accordingly.
 */
function selectEngine(engine, btn) {
    // Update hidden input
    const playerTypeInput = document.getElementById('player-type');
    if (playerTypeInput) playerTypeInput.value = engine;

    // Style engine buttons
    document.querySelectorAll('.engine-btn').forEach(b => {
        b.style.border = '2px solid #ddd';
        b.style.background = '#fafafa';
    });
    
    if (btn) {
        const colors = { 
            auto: '#2a7', chrome: '#2a7', vlc: '#e67e22', 
            mtx: '#2980b9', pyplayer: '#8e44ad', 
            external: '#8e44ad', mpv: '#d32f2f' 
        };
        const bgs = { 
            auto: '#e8f8f0', chrome: '#e8f8f0', vlc: '#fff3e0', 
            mtx: '#eaf4fb', pyplayer: '#f5eafb', 
            external: '#f5eafb', mpv: '#ffebee' 
        };
        const targetColor = colors[engine] || '#2a7';
        const targetBg = bgs[engine] || '#e8f8f0';
        btn.style.border = `2px solid ${targetColor}`;
        btn.style.background = targetBg;
    }

    // Show/hide submode panels
    document.querySelectorAll('.submode-panel').forEach(p => p.style.display = 'none');
    const panel = document.getElementById(`submode-${engine}`);
    if (panel) panel.style.display = '';

    // Set default mode for the engine
    const defaults = { 
        auto: 'auto', chrome: 'chrome_direct', vlc: 'vlc_embedded', 
        mtx: 'mtx_hls', pyplayer: 'pyplayer_native', 
        external: 'external_stream', mpv: 'mpv_native' 
    };
    const modeInput = document.getElementById('video-mode');
    if (modeInput) modeInput.value = defaults[engine] || 'auto';

    // Show/hide open-with button
    const openWithBtn = document.getElementById('btn-open-with-video');
    if (openWithBtn) openWithBtn.style.display = currentVideoItem ? 'inline-block' : 'none';
    
    if (typeof traceUiNav === 'function') {
        traceUiNav('VIDEO-ENGINE', engine);
    }
}

/**
 * Selects a specific sub-mode (e.g. Transcode vs Direct) within an engine.
 */
function selectSubMode(mode, btn, engine) {
    // Update hidden input
    const modeInput = document.getElementById('video-mode');
    if (modeInput) modeInput.value = mode;

    // Style sibling submode buttons in same engine panel
    const panel = document.getElementById(`submode-${engine}`);
    if (panel) {
        panel.querySelectorAll('.submode-btn').forEach(b => {
            b.style.border = '1px solid #ddd';
            b.style.background = '#fafafa';
            b.style.fontWeight = '';
        });
    }
    
    if (btn) {
        const colors = { chrome: '#2a7', vlc: '#e67e22', mtx: '#2980b9', pyplayer: '#8e44ad', mpv: '#d32f2f' };
        const bgs = { chrome: '#e8f8f0', vlc: '#fff3e0', mtx: '#eaf4fb', pyplayer: '#f5eafb', mpv: '#ffebee' };
        btn.style.border = `1px solid ${colors[engine] || '#2a7'}`;
        btn.style.background = bgs[engine] || '#e8f8f0';
        btn.style.fontWeight = '600';
    }

    // Toggle extra inputs for VLC network/device
    const netInput = document.getElementById('vlc-submode-network-input');
    const devInput = document.getElementById('vlc-submode-device-input');
    if (netInput) netInput.style.display = mode === 'vlc_network' ? '' : 'none';
    if (devInput) devInput.style.display = mode === 'vlc_device' ? '' : 'none';

    // Update info strips based on engine
    updateEngineInfo(engine, mode);
    
    if (typeof traceUiNav === 'function') {
        traceUiNav('VIDEO-MODE', mode, {engine: engine});
    }
}

/**
 * Updates the descriptive info text for various engines and modes.
 */
function updateEngineInfo(engine, mode) {
    const infoMaps = {
        'chrome': {
            chrome_direct: 'Direct Play: MP4/WebM werden nativ im Browser abgespielt — keine Transkodierung.',
            chrome_remux: 'mkvmerge Remux: MKV-Dateien werden via Pipe-Kit für Chrome kompatibel gemacht.',
            chrome_fragmp4: 'FFmpeg fMP4 zu HLS: Universelle Echtzeit-Transkodierung über fMP4 (HLS) für alle Formate.',
            chrome_hls: 'Internal HLS: Experimentelles HLS-Streaming über das interne Backend.'
        },
        'vlc': {
            vlc_embedded: 'Embedded HLS: VLC streamt das Video als HLS-Stream direkt in diesen Tab.',
            vlc_browser: 'Standalone VLC: Öffnet die Datei in einer separaten VLC-Instanz (extern).',
            vlc_dvd: 'VLC DVD Mode: Optimierte Wiedergabe für DVD-Strukturen und ISO-Images.',
            vlc_network: 'VLC Network: Streamen von einer Netzwerk-URL oder einem Device.',
            vlc_device: 'VLC Device: Direkte Wiedergabe von physikalischen Datenträgern.'
        },
        'mtx': {
            mtx_hls: 'MediaMTX HLS: Stabiles HTTP Live Streaming (benötigt MediaMTX Server).',
            mtx_webrtc: 'MediaMTX WebRTC: Ultra-Low-Latency Wiedergabe (<100ms Verzögerung).',
            mtx_rtsp: 'MediaMTX RTSP: Forwarding an einen RTSP-Stream-Endpunkt.',
            mtx_rtmp: 'MediaMTX RTMP: Forwarding an einen RTMP-Stream-Endpunkt.'
        },
        'pyplayer': {
            pyplayer_native: 'pyvidplayer2: Nutzt die Python-Bibliothek für eine native Overlay-Wiedergabe.',
            pyplayer_mpv: 'mpv Standalone: Startet den mächtigen mpv-Player als separaten Prozess.',
            pyplayer_mini: 'Mini-Overlay: Kompakte Wiedergabe in einem schwebenden Fenster.'
        },
        'external': {
            external_stream: 'Network Stream: Direkte Wiedergabe von URLs (HLS, RTSP, RTMP) im Browser-Player oder VLC.',
            external_dnd: 'Drag & Drop: Ziehe lokale Dateien hierher, um sie sofort abzuspielen.'
        }
    };

    const infoStrip = document.getElementById(`${engine}-info-strip`);
    if (infoStrip && infoMaps[engine] && infoMaps[engine][mode]) {
        infoStrip.textContent = infoMaps[engine][mode];
    }
}

/**
 * Legacy: kept for backward compat, delegates to selectEngine
 */
function updateVideoModes() {
    const type = document.getElementById('player-type');
    if (type) {
        const btn = document.querySelector(`.engine-btn[data-engine="${type.value}"]`);
        selectEngine(type.value, btn);
    }
}

/**
 * Switches the UI to the "Embedded Player" view.
 */
function orchestrateVideoPlaybackMode() {
    const dndPanel = document.getElementById('orchestrator-ingress-drag-drop-buffer');
    const embedded = document.getElementById('coordinated-media-renderer-pipeline-viewport');
    if (dndPanel) dndPanel.style.display = 'none';
    if (embedded) embedded.style.display = 'flex';
}

/**
 * Formats seconds into HH:MM:SS or MM:SS
 */
function formatTime(seconds) {
    if (isNaN(seconds)) return '00:00';
    const h = Math.floor(seconds / 3600);
    const m = Math.floor((seconds % 3600) / 60);
    const s = Math.floor(seconds % 60);
    if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
    return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
}

// Created with MWV v1.45.100-EVO-REBUILD
