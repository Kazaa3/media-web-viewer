/**
 * Visualizer Engine (v1.46.10)
 * Decoupled High-Fidelity Rendering System
 */

let audioContext = null;
let analyser = null;
let dataArray = null;
let visualizerAnimationId = null;

// Initial style fallback
let visualizerStyle = (window.GLOBAL_CONFIG && window.GLOBAL_CONFIG.visualizer_orchestration && window.GLOBAL_CONFIG.visualizer_orchestration.default_style) 
    ? (localStorage.getItem('mwv_visualizer_style') || window.GLOBAL_CONFIG.visualizer_orchestration.default_style)
    : (localStorage.getItem('mwv_visualizer_style') || 'bars');

/**
 * Setup and start the Web Audio API visualizer.
 */
function setupVisualizer(audioElement) {
    // [v1.46.10] Check Global Orchestration
    const config = window.GLOBAL_CONFIG || {};
    const vizCfg = config.visualizer_orchestration || { animation_enabled: true };
    
    if (vizCfg.animation_enabled === false) {
        console.warn("[Visualizer] Animation globally disabled in config.");
        return;
    }

    if (!audioContext) {
        try {
            audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const source = audioContext.createMediaElementSource(audioElement);
            analyser = audioContext.createAnalyser();
            analyser.fftSize = 256;
            source.connect(analyser);
            analyser.connect(audioContext.destination);
            
            const bufferLength = analyser.frequencyBinCount;
            dataArray = new Uint8Array(bufferLength);
        } catch (err) {
            console.error("[Visualizer] Initialization failed:", err);
            return;
        }
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
    const mainCanvas = document.getElementById('audio-visualizer-canvas');
    const sideCanvas = document.getElementById('sidebar-visualizer-canvas');
    if (!mainCanvas && !sideCanvas) return;
    
    const canvases = [mainCanvas, sideCanvas].filter(Boolean);
    const ctxs = canvases.map(c => {
        // High-DPI support or standard resize
        const parentW = c.parentElement.clientWidth;
        const parentH = c.id.includes('sidebar') ? 150 : 300;
        if (c.width !== parentW) c.width = parentW;
        if (c.height !== parentH) c.height = parentH;
        return c.getContext('2d');
    });
    
    if (visualizerAnimationId) cancelAnimationFrame(visualizerAnimationId);
    
    function animate() {
        if (!analyser) {
            ctxs.forEach((ctx, i) => {
                ctx.clearRect(0, 0, canvases[i].width, canvases[i].height);
                ctx.fillStyle = 'rgba(128, 128, 128, 0.2)';
                ctx.font = '700 14px "Inter", sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Warte auf Audio-Stream...', canvases[i].width / 2, canvases[i].height / 2);
            });
            return;
        }

        visualizerAnimationId = requestAnimationFrame(animate);
        
        if (visualizerStyle === 'wave') {
            analyser.getByteTimeDomainData(dataArray);
        } else {
            analyser.getByteFrequencyData(dataArray);
        }
        
        ctxs.forEach((ctx, idx) => {
            const w = canvases[idx].width;
            const h = canvases[idx].height;
            ctx.clearRect(0, 0, w, h);

            // [v1.46.10] Color Orchestration
            const vizCfg = (window.GLOBAL_CONFIG && window.GLOBAL_CONFIG.visualizer_orchestration) || {};
            let accentColor = vizCfg.accent_color || '#007aff';
            if (vizCfg.use_ui_accent) {
                accentColor = getComputedStyle(document.documentElement).getPropertyValue('--accent-color').trim() || accentColor;
            }

            if (visualizerStyle === 'bars') {
                const barWidth = (w / dataArray.length) * 2.5;
                let x = 0;
                for (let i = 0; i < dataArray.length; i++) {
                    const barHeight = (dataArray[i] / 255) * h;
                    const gradient = ctx.createLinearGradient(0, h, 0, h - barHeight);
                    gradient.addColorStop(0, 'rgba(0, 122, 255, 0)');
                    gradient.addColorStop(1, accentColor + '66');
                    ctx.fillStyle = gradient;
                    ctx.fillRect(x, h - barHeight, barWidth, barHeight);
                    x += barWidth + 1;
                }
            } else if (visualizerStyle === 'circle' && !canvases[idx].id.includes('sidebar')) {
                const centerX = w / 2;
                const centerY = h / 2;
                const radius = 80;
                ctx.beginPath();
                ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
                ctx.strokeStyle = accentColor + '33';
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
                    ctx.strokeStyle = accentColor;
                    ctx.lineWidth = 2;
                    ctx.stroke();
                }
            } else {
                ctx.lineWidth = 3;
                ctx.strokeStyle = accentColor + '99';
                ctx.beginPath();
                const sliceWidth = w / dataArray.length;
                let x = 0;
                for (let i = 0; i < dataArray.length; i++) {
                    const v = dataArray[i] / 128.0;
                    const y = v * h / 2;
                    if (i === 0) ctx.moveTo(x, y);
                    else ctx.lineTo(x, y);
                    x += sliceWidth;
                }
                ctx.lineTo(w, h / 2);
                ctx.stroke();
            }
        });
    }
    
    animate();
}

/**
 * Switch visualizer style and persist.
 */
function setVisualizerStyle(style) {
    visualizerStyle = style;
    localStorage.setItem('mwv_visualizer_style', style);
    if (typeof showToast === 'function') showToast(`Visualizer: ${style.toUpperCase()}`, 1500);
}

window.setupVisualizer = setupVisualizer;
window.setVisualizerStyle = setVisualizerStyle;
