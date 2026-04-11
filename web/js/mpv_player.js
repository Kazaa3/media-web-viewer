/**
 * @file mpv-player.js
 * @brief Frontend Bridge for libmpv via WASM (libmpv zu Canvas)
 * @details Handles initialization, file loading, and event bridging for interactive ISO playback.
 * 
 * [AI-READINESS: High Level Context]
 * This module provides a high-performance WASM-to-Canvas bridge for libmpv.
 * Core Class: MpvWasmPlayer
 * Main Entry: window.mpvPlayer.play(filePath)
 * Complexity: High (WASM Memory Management & Event Bridging)
 */

class MpvPlayer {
    constructor(canvasId, overlayId) {
        this.canvas = document.getElementById(canvasId);
        this.overlay = document.getElementById(overlayId);
        this.mpv = null;
        this.worker = null;
        this.isInitialized = false;
        this.currentPath = null;
    }

    /**
     * Initializes the WASM environment and MPV instance.
     * Requires COOP/COEP headers to be enabled on the server.
     */
    async init() {
        if (this.isInitialized) return;

        console.log("[MPV-WASM] Initializing libmpv bridge...");
        
        try {
            // we expect mpv.js and mpv.wasm to be in /js/mpv-wasm/
            // Note: This is an architectural skeleton. Actual implementation depends on the specific mpv-wasm build used.
            const { createMPV } = await import('./mpv-wasm/mpv.js');
            
            this.mpv = await createMPV({
                canvas: this.canvas,
                workerPath: './js/mpv-wasm/mpv-worker.js',
                wasmPath: './js/mpv-wasm/mpv.wasm',
                arguments: [
                    '--vo=gpu',
                    '--gpu-api=webgl2',
                    '--hwdec=auto',
                    '--idle=yes',
                    '--keep-open=yes',
                    '--osd-level=1'
                ]
            });

            this.setupEvents();
            this.isInitialized = true;
            console.log("[MPV-WASM] libmpv successfully initialized.");
        } catch (err) {
            console.error("[MPV-WASM] Initialization failed:", err);
            if (typeof showToast === 'function') {
                showToast("<svg width='14' height='14' style='vertical-align:middle;margin-right:4px;'><use href='#icon-delete'></use></svg> MPV WASM Init Fehler (Fehlende Binaries?)", 5000);
            }
            throw err;
        }
    }

    setupEvents() {
        if (!this.mpv) return;

        // Bridge MPV events to UI
        this.mpv.addEventListener('property-change', (node) => {
            if (node.name === 'idle-active' && node.data === true) {
                // Return to normal UI or handle idle
            }
        });

        // Key bridging for DVD Menus
        window.addEventListener('keydown', (e) => {
            if (this.canvas && this.canvas.style.display !== 'none') {
                this.handleKey(e);
            }
        });
    }

    handleKey(e) {
        if (!this.mpv) return;
        
        const keyMap = {
            'ArrowUp': 'up',
            'ArrowDown': 'down',
            'ArrowLeft': 'left',
            'ArrowRight': 'right',
            'Enter': 'enter',
            'Escape': 'menu'
        };

        const mpvKey = keyMap[e.key];
        if (mpvKey) {
            this.mpv.command('keypress', mpvKey);
            e.preventDefault();
        }
    }

    async play(filePath) {
        if (!this.isInitialized) await this.init();

        this.currentPath = filePath;
        if (this.canvas) this.canvas.style.display = 'block';
        if (this.overlay) this.overlay.style.display = 'flex';

        // Get the local streaming URL from the backend
        const streamUrl = await eel.get_iso_stream_url(filePath)();
        console.log("[MPV-WASM] Loading stream:", streamUrl);

        await this.mpv.command('loadfile', streamUrl);
        await this.mpv.command('set_property', 'pause', false);
    }

    stop() {
        if (this.mpv) {
            this.mpv.command('stop');
        }
        if (this.canvas) this.canvas.style.display = 'none';
        if (this.overlay) this.overlay.style.display = 'none';
    }

    destroy() {
        if (this.mpv) {
            this.mpv.destroy();
            this.mpv = null;
        }
        this.isInitialized = false;
    }
}

// Export a singleton instance
window.mpvPlayer = new MpvPlayer('mpv-canvas', 'mpv-menu-overlay');

// Created with MWV v1.46.00-MASTER
