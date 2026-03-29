/**
 * System & Diagnostic Helpers
 * Extracted from app.html to improve modularity and avoid line-number drift.
 */

/**
 * Runs a Round Trip Time (RTT) test between the UI and the backend.
 */
async function runRTTTest(testType = 'ping') {
    const statusEl = document.getElementById('rtt-status-text');
    const footerLatency = document.getElementById('footer-latency');
    const btns = document.querySelectorAll('#options-sync-view .action-btn, #test-base-view .tab-btn');
    const resContainer = document.getElementById('rtt-results-container');

    if (resContainer) resContainer.style.display = 'block';
    if (statusEl) statusEl.innerText = (testType === 'complex' ? "Complex RTT Testing..." : "Ping Testing...");
    btns.forEach(btn => btn.disabled = true);

    try {
        let testData;
        if (testType === 'ping') {
            testData = {
                stage1: { key: "normal_dict" },
                stage2: { nested: { a: 1, b: 2 } },
                stage3: [{ id: 1, val: "list_of_dicts" }, { id: 2, val: "item" }]
            };
        } else {
            testData = {
                id: "test-rtt-" + Date.now(),
                title: "RTT Test Item (Music)",
                artist: "Frontend Sync Test",
                album: "Latency Benchmarks",
                genre: "Diagnostic",
                duration: "3:45",
                extension: "flac",
                codec: "FLAC",
                type: "file",
                timestamp: new Date().toISOString(),
                complex: { a: 1, b: [1, 2, 3], c: { d: "nested" } }
            };
        }

        // appendUiTrace is assumed to be in common_helpers.js
        if (typeof appendUiTrace === 'function') appendUiTrace(`RTT [${testType}]: Sending data to backend...`);
        
        const start = performance.now();
        const response = await eel.rtt_ping(testData)();
        const end = performance.now();
        const rtt = (end - start).toFixed(2);

        if (typeof appendUiTrace === 'function') appendUiTrace(`RTT [${testType}]: Backend responded in ${rtt}ms. Status: ${response.status}`);

        // Confirm Receipt
        if (typeof eel !== 'undefined' && typeof eel.confirm_receipt === 'function') {
            await eel.confirm_receipt(testType === 'complex' ? "ITEM_RTT_RECEIVED" : "RTT_PONG_RECEIVED")();
        }

        if (statusEl) {
            statusEl.innerHTML = `${testType.toUpperCase()}: <strong style="color: #2a7;">${rtt}ms</strong> (Sync OK)`;
        }
        if (footerLatency) footerLatency.innerText = rtt + 'ms';
    } catch (e) {
        if (typeof appendUiTrace === 'function') appendUiTrace(`RTT [${testType}] Error: ${e}`);
        if (statusEl) statusEl.innerText = "Error: " + e;
    } finally {
        btns.forEach(btn => btn.disabled = false);
    }
}

/**
 * Runs a WebSocket stress test with multiple concurrent pings.
 */
async function runWebSocketStressTest() {
    const statusEl = document.getElementById('rtt-status-text');
    const btns = document.querySelectorAll('#options-sync-view .action-btn');
    const count = 100;
    let successes = 0;
    let totalTime = 0;

    if (statusEl) statusEl.innerText = `Starting Stress Test (0/${count})...`;
    btns.forEach(btn => btn.disabled = true);

    try {
        if (typeof appendUiTrace === 'function') appendUiTrace(`[Stress] Starting WebSocket stress test: ${count} pings...`);
        const startTotal = performance.now();

        const batchSize = 10;
        for (let i = 0; i < count; i += batchSize) {
            const batchPromises = [];
            for (let j = 0; j < batchSize && (i + j) < count; j++) {
                const idx = i + j;
                const start = performance.now();
                batchPromises.push(eel.rtt_stress_ping(idx, count)().then(res => {
                    const end = performance.now();
                    totalTime += (end - start);
                    successes++;
                    if (statusEl && successes % 5 === 0) {
                        statusEl.innerText = `Stress Test (${successes}/${count})...`;
                    }
                }));
            }
            await Promise.all(batchPromises);
            await new Promise(resolve => setTimeout(resolve, 50));
        }

        const endTotal = performance.now();
        const avgRtt = (totalTime / count).toFixed(2);
        const totalDuration = (endTotal - startTotal).toFixed(0);

        if (typeof appendUiTrace === 'function') appendUiTrace(`[Stress] Finished: ${successes}/${count} OK. Avg RTT: ${avgRtt}ms. Total: ${totalDuration}ms`);

        if (statusEl) {
            statusEl.innerHTML = `STRESS: <strong style="color: #2a7;">${successes}/${count} OK</strong> (Avg: ${avgRtt}ms, Total: ${totalDuration}ms)`;
        }
    } catch (e) {
        if (typeof appendUiTrace === 'function') appendUiTrace(`[Stress] Error: ${e}`);
        if (statusEl) statusEl.innerText = "Stress Error: " + e;
    } finally {
        btns.forEach(btn => btn.disabled = false);
    }
}

/**
 * Loads the application's environment information from the backend.
 */
async function loadEnvironmentInfo(forceRefresh = false) {
    if (typeof appendUiTrace === 'function') appendUiTrace(`[Env] Loading environment info (force: ${forceRefresh})...`);
    try {
        const info = await eel.get_environment_info(forceRefresh)();
        if (!info) return;

        // Populate fields (Mapping depends on backend response keys)
        safeText('env-app-version', info.app_version);
        safeText('env-python-version', info.python_version);
        safeText('env-python-exec', info.python_executable);
        safeText('env-venv-path', info.venv_path);
        safeText('env-main-pid', info.main_pid);
        safeText('env-browser-pid', info.browser_pid);
        
        // Mediaplayers
        safeText('env-mediaplayer-status', (info.player_status || []).join(', '));
        safeText('env-ffmpeg-status', info.ffmpeg_version);
        safeText('env-ffprobe-status', info.ffprobe_version);
        
        // Sync with hardware discovery view if needed
        if (info.hardware) {
            safeText('hardware-disk-type', info.hardware.disk || '-');
            safeText('hardware-gpu-type', info.hardware.gpu || '-');
        }

        if (typeof appendUiTrace === 'function') appendUiTrace(`[Env] Environment info loaded successfully.`);
    } catch (err) {
        console.error("Error loading environment info:", err);
    }
}

/**
 * Resets the application's backend state.
 */
async function resetBackend() {
    if (!confirm("Möchtest du das Backend wirklich zurücksetzen? Alle Caches werden gelöscht.")) return;
    
    if (typeof appendUiTrace === 'function') appendUiTrace("[System] Triggering Backend Reset...");
    try {
        const res = await eel.reset_backend()();
        if (res && res.status === 'ok') {
            if (typeof showToast === 'function') showToast("Backend erfolgreich zurückgesetzt. Die App wird neu geladen.", "success");
            setTimeout(() => location.reload(), 2000);
        } else {
            if (typeof showToast === 'function') showToast("Fehler beim Zurücksetzen: " + (res.message || 'unbekannt'), "error");
        }
    } catch (err) {
        if (typeof showToast === 'function') showToast("Kritischer Fehler beim Reset: " + err, "error");
    }
}

/**
 * Runs Selenium session integrity tests in the browser.
 */
async function runSeleniumSessionTests() {
    const outputEl = document.getElementById('selenium-output');
    const container = document.getElementById('selenium-results-container');
    const options = {
        verbose: document.getElementById('selenium-flag-verbose')?.checked,
        trace: document.getElementById('selenium-flag-trace')?.checked,
        pp_mode: document.getElementById('selenium-flag-pp-mode')?.checked,
        dom_control: document.getElementById('selenium-flag-dom-control')?.checked,
        no_sandbox: document.getElementById('selenium-flag-nosandbox')?.checked
    };

    if (!outputEl || !container) return;

    container.style.display = 'block';
    outputEl.innerText = "[Status] Initializing Selenium Test Runner (Attach Mode)...\nConnecting to 127.0.0.1:9222...";
    outputEl.style.color = "#d4d4d4";

    try {
        const res = await eel.run_selenium_session_tests(options)();
        if (res.status === 'ok') {
            outputEl.innerText = res.output;
            if (res.exit_code !== 0) {
                outputEl.innerText += "\n\n[ERROR] Test Suite exited with code " + res.exit_code;
                outputEl.style.color = "#ff6b6b";
            } else {
                outputEl.style.color = "#b9f6ca";
            }
        } else {
            outputEl.innerText = "Error: " + res.message;
            outputEl.style.color = "#ff6b6b";
        }
    } catch (err) {
        outputEl.innerText = "Fatal Error: " + err;
        outputEl.style.color = "#ff6b6b";
    }
}
