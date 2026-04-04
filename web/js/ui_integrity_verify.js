/**
 * UI Integrity & Playback Diagnostic Suite (v1.34)
 * Performs automated "probe" tests from the frontend to verify DOM and Playback state.
 */

const UiIntegritySuite = {
    async runIntegrityCheck() {
        console.log("--- Starting UI Integrity Check ---");
        mwv_trace('DOM-TEST', 'START', { timestamp: new Date().toISOString() });

        try {
            // 1. Audit Duo-View Containers
            const views = ['legacy', 'visualizer'];
            for (const view of views) {
                const el = document.getElementById(`player-view-${view}`);
                if (!el) {
                    this.fail('DOM-AUDIT', `Container #player-view-${view} missing.`);
                } else {
                    this.pass('DOM-AUDIT', `Container #player-view-${view} detected.`);
                }
            }

            // 2. Audit Track Rendering
            const trackItems = document.querySelectorAll('.legacy-track-item');
            mwv_trace('DOM-TEST', 'TRACK-COUNT', { count: trackItems.length });
            
            if (trackItems.length === 0) {
                this.warn('DOM-AUDIT', 'No .legacy-track-item elements found. Is the library empty?');
                if (typeof eel !== 'undefined') eel.report_items_spawned(0, 'integrity-suite')();
            } else {
                this.pass('DOM-AUDIT', `Successfully rendered ${trackItems.length} track items.`);
                if (typeof eel !== 'undefined') eel.report_items_spawned(trackItems.length, 'integrity-suite')();
            }

            // 3. Playback Probe
            if (trackItems.length > 0) {
                await this.probePlayback(trackItems[0]);
            } else {
                this.info('PLAYBACK-PROBE', 'Skipping playback probe (No items found).');
            }

        } catch (err) {
            this.fail('CRITICAL', err.message);
        }

        console.log("--- UI Integrity Check Complete ---");
    },

    async probePlayback(firstItem) {
        console.log("Probing Playback...");
        mwv_trace('DOM-TEST', 'PROBE-PLAYBACK', { target: 'first-track' });

        // Trigger click on the first item
        firstItem.click();

        // Wait for pipeline state change
        await new Promise(r => setTimeout(r, 2000));

        const pipeline = document.getElementById('native-html5-audio-pipeline-element');
        if (!pipeline) {
            this.fail('PLAYBACK-PROBE', '#native-html5-audio-pipeline-element missing.');
            return;
        }

        const isPlaying = !pipeline.paused && pipeline.currentTime > 0;
        const currentSrc = pipeline.src;

        if (isPlaying) {
            this.pass('PLAYBACK-PROBE', `Playback successful. Source: ${currentSrc}`);
            if (typeof eel !== 'undefined') eel.report_playback_state(true, currentSrc, pipeline.currentTime)();
        } else {
            this.fail('PLAYBACK-PROBE', `Playback failed. src=${currentSrc}, paused=${pipeline.paused}, time=${pipeline.currentTime}`);
            if (typeof eel !== 'undefined') eel.report_playback_state(false, currentSrc, 0)();
        }
    },

    pass(cat, msg) {
        console.log(`[PASS] [${cat}] ${msg}`);
        mwv_trace('DOM-TEST', 'PASS', { category: cat, message: msg });
        if (typeof showToast === 'function') showToast(`PASS: ${cat}`, 'success');
    },

    warn(cat, msg) {
        console.warn(`[WARN] [${cat}] ${msg}`);
        mwv_trace('DOM-TEST', 'WARN', { category: cat, message: msg });
        if (typeof showToast === 'function') showToast(`WARN: ${cat}`, 'info');
    },

    fail(cat, msg) {
        console.error(`[FAIL] [${cat}] ${msg}`);
        mwv_trace('DOM-TEST', 'FAIL', { category: cat, message: msg });
        if (typeof showToast === 'function') showToast(`FAIL: ${cat}`, 'error');
    },

    info(cat, msg) {
        console.log(`[INFO] [${cat}] ${msg}`);
    }
};

window.runIntegrityCheck = () => UiIntegritySuite.runIntegrityCheck();
