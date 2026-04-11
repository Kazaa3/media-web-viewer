/**
 * Test Suite & Diagnostics Helpers
 */

let __testOutputBuffer = '';
let isTestRunInProgress = false;
let currentEditingTestFile = null;
let videoTestHistory = [];

/**
 * Appends a chunk of text to the test output area, with overflow protection.
 */
function appendTestOutputChunk(chunk) {
    const resultsContainer = document.getElementById('test-results-container');
    const outputArea = document.getElementById('test-output');
    if (!outputArea) return;

    if (resultsContainer) {
        resultsContainer.style.display = 'block';
    }

    const maxOutputChars = 250000;
    const truncatedPrefix = '[Ausgabe gekürzt - nur die letzten Zeichen werden angezeigt]\n\n';
    __testOutputBuffer += chunk;
    if (__testOutputBuffer.length > maxOutputChars) {
        __testOutputBuffer = truncatedPrefix + __testOutputBuffer.slice(-maxOutputChars);
    }
    outputArea.textContent = __testOutputBuffer;
    outputArea.scrollTop = outputArea.scrollHeight;
}

// Expose to Eel for backend-driven test output
if (typeof eel !== 'undefined' && eel.expose) {
    eel.expose(append_test_output);
}

function append_test_output(message) {
    appendTestOutputChunk(String(message || ''));
}

/**
 * Loads available test suites from the backend and renders them.
 * v1.41.00 Final: Python only + Autonomous GUI Auditor (Virtual).
 */
async function loadTestSuites(retryCount) {
    retryCount = retryCount || 0;
    const container = document.getElementById('test-suites-container');
    const folderSelect = document.getElementById('test-folder-select');
    if (!container) return;

    if (retryCount === 0) {
        container.innerHTML = `<div style="color: var(--text-secondary); font-style: italic; padding: 20px;">Tests werden geladen...</div>`;
    }

    try {
        const res = await eel.get_test_suites()();
        // Filter: ONLY .py files (as requested)
        let suites = (res || []).filter(s => s.id.endsWith('.py'));

        // Inject Virtual "Autonomous GUI Auditor" (Selenium-free)
        const virtualAuditor = {
            id: 'gui_auditor_virtual',
            name: 'GUI Auditor (Autonomous)',
            folder: 'System',
            metadata: {
                category: 'INTEGRITY-AUDIT',
                inputs: 'DOM Snapshot, Session State',
                outputs: '10-Point Health Report',
                files: 'diagnostics_helpers.js',
                comment: 'Automatisierte Integritätsprüfung aller UI-Komponenten ohne Selenium/Playwright.'
            }
        };
        suites.unshift(virtualAuditor);

        // Populate Folder Dropdown
        if (folderSelect && (folderSelect.options.length <= 1 || retryCount === 0)) {
            const currentVal = folderSelect.value || 'all';
            folderSelect.innerHTML = '<option value="all">-- All Folders --</option>';
            const folders = [...new Set(suites.map(s => s.folder || 'root'))].sort();
            folders.forEach(f => {
                const opt = document.createElement('option');
                opt.value = f;
                opt.textContent = f;
                if (f === currentVal) opt.selected = true;
                folderSelect.appendChild(opt);
            });
        }

        const activeFolder = folderSelect ? folderSelect.value : 'all';
        const filteredSuites = activeFolder === 'all' 
            ? suites 
            : suites.filter(s => (s.folder || 'root') === activeFolder);

        container.innerHTML = '';
        if (filteredSuites.length === 0) {
            container.innerHTML = '<div style="padding: 40px; text-align: center; color: var(--text-secondary);">Keine Tests gefunden.</div>';
            return;
        }

        const frag = document.createDocumentFragment();
        filteredSuites.forEach(suite => {
            const card = createTestCard(suite);
            frag.appendChild(card);
        });
        container.appendChild(frag);

    } catch (e) {
        console.error('[loadTestSuites] Error:', e);
        container.innerHTML = `<div style="color: #ff5252; padding: 20px;">Fehler beim Laden: ${e}</div>`;
    }
}

/**
 * v1.3.2 Style Test Card (Restoration)
 */
function createTestCard(suite) {
    const card = document.createElement('div');
    card.style.cssText = 'background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 20px; display: flex; flex-direction: column; position: relative; box-shadow: 0 2px 8px rgba(0,0,0,0.05); transition: transform 0.2s;';
    
    // Left highlight bar based on category
    const isIntegration = (suite.metadata.category || "").toLowerCase().includes('integration');
    card.style.borderLeft = isIntegration ? '5px solid #1565c0' : '5px solid #e0e0e0';

    const m = suite.metadata || {};
    const categoryHtml = m.category && m.category !== '-' ? `<span style="background: #e3f2fd; color: #1565c0; padding: 4px 10px; border-radius: 4px; font-size: 10px; font-weight: 800; text-transform: uppercase;">${m.category}</span>` : '';

    const isInteractiveBrowserTest = (suiteId) => {
        const name = String(suiteId || '').toLowerCase();
        const patterns = ['test_route', 'test_network', 'run_app', 'pyautogui', 'selenium', 'gui_test'];
        return patterns.some(pattern => name.includes(pattern));
    };
    const checkedAttr = isInteractiveBrowserTest(suite.id) ? '' : 'checked';

    card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <input type="checkbox" class="test-suite-checkbox" value="${suite.id}" ${checkedAttr} style="width: 18px; height: 18px; cursor: pointer;">
                <h3 style="margin: 0; font-size: 1.1em; color: #333; font-weight: 800;">${suite.name.replace('.py', '')}</h3>
            </div>
            <div class="test-card-actions" style="display: flex; align-items: center; gap: 10px;">
                <!-- Buttons injected below -->
                ${categoryHtml}
            </div>
        </div>
        
        <div style="display: grid; grid-template-columns: 80px 1fr; gap: 8px; font-size: 12px; line-height: 1.4; color: #555; margin-bottom: 15px;">
            <strong>Inputs:</strong> <span style="color: #333;">${m.inputs || '-'}</span>
            <strong>Outputs:</strong> <span style="color: #333;">${m.outputs || '-'}</span>
            <strong>Test Files:</strong> <span style="font-family: monospace; color: var(--accent-color);">${m.files || '-'}</span>
        </div>

        <div style="margin-top: auto; padding-top: 12px; border-top: 1px solid #eee; font-size: 11px; color: #777; font-style: italic;">
            ${m.comment || 'Kein Kommentar vorhanden.'}
        </div>
    `;

    // Action Buttons (Edit/Trash) in top right
    const actionsArea = card.querySelector('.test-card-actions');
    
    // Edit Button (Icon)
    const editBtn = document.createElement('button');
    editBtn.innerHTML = '✎';
    editBtn.style.cssText = 'border: none; background: transparent; color: #777; cursor: pointer; padding: 4px; font-size: 14px;';
    editBtn.title = 'Test bearbeiten';
    editBtn.onclick = (e) => { e.stopPropagation(); openTestEditModal(suite); };
    
    // Delete Button (Icon)
    const delBtn = document.createElement('button');
    delBtn.innerHTML = '🗑';
    delBtn.style.cssText = 'border: none; background: transparent; color: #ff5252; cursor: pointer; padding: 4px; font-size: 14px; opacity: 0.7;';
    delBtn.title = 'Test löschen';
    delBtn.onclick = (e) => {
        e.stopPropagation();
        if (confirm(`Test "${suite.name}" wirklich löschen?`)) deleteTest(suite.id);
    };

    actionsArea.prepend(delBtn);
    actionsArea.prepend(editBtn);

    return card;
}

async function runSelectedTests() {
    if (isTestRunInProgress) return;

    const checkboxes = document.querySelectorAll('.test-suite-checkbox:checked');
    const selectedFiles = Array.from(checkboxes).map(cb => cb.value);
    const runBtn = document.getElementById('run-selected-tests-btn');
    
    if (selectedFiles.length === 0) {
        if (typeof showStatusNotification === 'function') showStatusNotification('Bitte mindestens einen Test auswählen.', 'warn');
        return;
    }

    isTestRunInProgress = true;
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.style.opacity = '0.6';
    }

    const resultsContainer = document.getElementById('test-results-container');
    const outputArea = document.getElementById('test-output');
    const summaryBadge = document.getElementById('test-run-summary');

    if (resultsContainer) {
        resultsContainer.style.display = 'flex';
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    if (outputArea) outputArea.textContent = '';
    if (summaryBadge) summaryBadge.style.display = 'none';

    appendTestOutputChunk(`[RUN] Test-Lauf gestartet um ${new Date().toLocaleTimeString()}...\n`);

    try {
        // Handle Virtual GUI Auditor separately
        if (selectedFiles.includes('gui_auditor_virtual')) {
            appendTestOutputChunk(`\n[SELF-TEST] Starte Autonomous GUI Auditor (10-Point Audit)...\n`);
            if (typeof window.runAutonomousSelfTest === 'function') {
                await window.runAutonomousSelfTest();
                appendTestOutputChunk(`[SELF-TEST] Audit abgeschlossen. Ergebnisse in der Console und Status-Leiste detailiert einsehbar.\n`);
            } else {
                appendTestOutputChunk(`[ERROR] runAutonomousSelfTest nicht gefunden!\n`);
            }
        }

        // Filter out virtual IDs before sending to backend
        const pythonTests = selectedFiles.filter(id => id !== 'gui_auditor_virtual');

        if (pythonTests.length > 0) {
            appendTestOutputChunk(`\n[BACKEND] Sende ${pythonTests.length} Python-Tests an Engine...\n`);
            const result = await eel.run_tests(pythonTests)();
            
            if (result.error) {
                appendTestOutputChunk(`[ERROR] ${result.error}\n`);
            } else {
                appendTestOutputChunk(`\n[RESULTS] Python Exit Code: ${result.exit_code}\n`);
                appendTestOutputChunk(`Pass: ${result.passes || 0} | Fail: ${result.fails || 0}\n`);
                
                if (summaryBadge) {
                    summaryBadge.style.display = 'inline-block';
                    summaryBadge.textContent = `${result.passes || 0} Pass, ${result.fails || 0} Fail`;
                    summaryBadge.style.background = (result.fails || 0) > 0 ? 'rgba(255, 82, 82, 0.2)' : 'rgba(46, 204, 113, 0.2)';
                    summaryBadge.style.color = (result.fails || 0) > 0 ? '#ff5252' : '#2ecc71';
                }
            }
        }

        appendTestOutputChunk(`\n[FINISH] Alle ausgewählten Aufgaben beendet.\n`);

    } catch (e) {
        appendTestOutputChunk(`\n[SYSTEM ERROR] ${e}\n`);
    } finally {
        isTestRunInProgress = false;
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.style.opacity = '1';
        }
    }
}

function openTestEditModal(suite) {
    currentEditingTestFile = suite.id;
    const label = typeof t === 'function' ? t('test_meta_file_label') : 'File: ';
    if (typeof safeText === 'function') safeText('test-edit-filename', `${label}tests/${suite.id}`);
    if (typeof safeValue === 'function') {
        safeValue('test-edit-category', suite.metadata.category || '-');
        safeValue('test-edit-inputs', suite.metadata.inputs || '-');
        safeValue('test-edit-outputs', suite.metadata.outputs || '-');
        safeValue('test-edit-files', suite.metadata.files || '-');
        safeValue('test-edit-comment', suite.metadata.comment || '-');
    }
    if (typeof safeStyle === 'function') safeStyle('test-edit-modal', 'display', 'flex');
}

function closeTestEditModal() {
    if (typeof safeStyle === 'function') safeStyle('test-edit-modal', 'display', 'none');
}

async function saveTestMetadata() {
    if (!currentEditingTestFile) return;

    const metadata = {
        category: typeof readValue === 'function' ? readValue('test-edit-category') : null,
        inputs: typeof readValue === 'function' ? readValue('test-edit-inputs') : null,
        outputs: typeof readValue === 'function' ? readValue('test-edit-outputs') : null,
        files: typeof readValue === 'function' ? readValue('test-edit-files') : null,
        comment: typeof readValue === 'function' ? readValue('test-edit-comment') : null
    };

    const res = await eel.update_test_metadata(currentEditingTestFile, metadata)();
    if (res.status === 'ok') {
        closeTestEditModal();
        loadTestSuites();
        if (typeof t === 'function') alert(t("test_save_success"));
    } else {
        const err = typeof t === 'function' ? t("common_error") : "Error: ";
        alert(err + res.error);
    }
}

async function createNewTest() {
    const nameLabel = typeof t === 'function' ? t('test_new_prompt_name') : 'Test name:';
    const name = prompt(nameLabel);
    if (!name) return;
    const res = await eel.create_new_test(name)();
    if (res.status === 'ok') {
        loadTestSuites();
    } else {
        const err = typeof t === 'function' ? t('common_error') : "Error: ";
        alert(err + (res.message || res.error));
    }
}

async function deleteTest(filename) {
    const res = await eel.delete_test(filename)();
    if (res.status === 'ok') {
        loadTestSuites();
    } else {
        const err = typeof t === 'function' ? t('common_error') : "Error: ";
        alert(err + (res.message || res.error));
    }
}

/**
 * Specialized Validation Tools
 */
async function runFfmpegPipelineSuite() {
    let relpath = document.getElementById('pipeline-test-path')?.value;
    if (!relpath) {
        relpath = "*.mp4";
        const el = document.getElementById('pipeline-test-path');
        if (el) el.value = relpath;
    }

    const resultsContainer = document.getElementById('pipeline-results');
    const cardsContainer = document.getElementById('pipeline-cards');
    if (resultsContainer) resultsContainer.style.display = 'block';
    if (cardsContainer) cardsContainer.innerHTML = '<div style="grid-column: 1/-1; padding: 20px; text-align: center;">Tests laufen...</div>';

    try {
        const res = await eel.run_ffmpeg_pipeline_test(relpath)();
        if (res.status === 'ok' && cardsContainer) {
            cardsContainer.innerHTML = '';
            res.results.forEach(test => {
                const card = document.createElement('div');
                const statusColor = test.status === 'pass' ? '#2a7' : '#d32f2f';
                card.style = `background: white; border: 1px solid #eee; border-radius: 10px; padding: 15px; border-left: 5px solid ${statusColor}; box-shadow: 0 2px 8px rgba(0,0,0,0.02);`;
                card.innerHTML = `
                    <div style="font-weight: bold; margin-bottom: 5px; color: #333;">${test.name}</div>
                    <div style="font-size: 0.85em; color: #666; word-break: break-all;">${test.details}</div>
                    <div style="margin-top: 10px; font-size: 0.75em; font-weight: bold; color: ${statusColor}; text-transform: uppercase;">${test.status}</div>
                `;
                cardsContainer.appendChild(card);
            });
        }
    } catch (err) {
        if (cardsContainer) cardsContainer.innerHTML = `<div style="grid-column: 1/-1; color: #d32f2f; padding: 20px; text-align: center;">Error: ${err.message}</div>`;
    }
}

async function testMediaQualityScore() {
    const relpath = document.getElementById('pipeline-test-path')?.value;
    if (!relpath) return typeof showToast === 'function' ? showToast("Pfad fehlt.") : null;
    const info = await eel.analyze_media(relpath)();
    if (typeof showToast === 'function') {
        showToast(`Quality: ${info.quality_score}/100 | Mode: ${info.recommended_mode.toUpperCase()}`, 5000);
    }
}

async function generateTestMatrix() {
    if (typeof showToast === 'function') showToast('Erstelle Test-Pattern Matrix...');
    const res = await eel.run_video_matrix_test()();
    if (res.status === 'ok' && typeof showToast === 'function') {
        showToast(`${res.matrix.length} Test-Files erstellt.`);
    }
}

async function populateTestVideoSelector() {
    const selector = document.getElementById('test-video-selector');
    if (!selector) return;

    const currentVal = selector.value;
    selector.innerHTML = '<option value="">-- Kein Video ausgewählt --</option>';

    const options = [];
    if (typeof allLibraryItems !== 'undefined') {
        allLibraryItems.forEach(v => {
            const path = (v.path || "").toLowerCase();
            if (path.endsWith('.mp4') || path.endsWith('.mkv') || path.endsWith('.avi')) {
                options.push({ value: v.path, text: v.name });
            }
        });
    }

    options.forEach(opt => {
        const el = document.createElement('option');
        el.value = opt.value;
        el.textContent = opt.text;
        if (opt.value === currentVal) el.selected = true;
        selector.appendChild(el);
    });
}

/**
 * Video Player Triggers
 */
async function triggerVLCPlay() {
    if (typeof currentVideoItem !== 'undefined' && typeof eel.open_vlc === 'function') {
        return await eel.open_vlc(currentVideoItem.path)();
    }
}

async function triggerWebMTranscode() {
    if (typeof currentVideoItem !== 'undefined' && typeof eel.trigger_webm_transcode === 'function') {
        return await eel.trigger_webm_transcode(currentVideoItem.path)();
    }
}

async function triggerFFmpegPlay() {
    if (typeof currentVideoItem !== 'undefined' && typeof eel.trigger_ffmpeg_stream === 'function') {
        return await eel.trigger_ffmpeg_stream(currentVideoItem.path)();
    }
}

async function triggerFragMP4Play() {
    if (typeof currentVideoItem !== 'undefined' && typeof eel.start_mp4frag_conversion === 'function') {
        return await eel.start_mp4frag_conversion(currentVideoItem.path, "")();
    }
}

async function runMtxValidation() {
    const path = document.getElementById('mtx-test-path')?.value || "";
    if (!path) return;

    const resultsDiv = document.getElementById('mtx-validation-results');
    const cardsDiv = document.getElementById('mtx-status-cards');
    if (resultsDiv) resultsDiv.style.display = 'block';
    
    try {
        const report = await eel.run_mtx_validation(path)();
        if (cardsDiv) {
            cardsDiv.innerHTML = '';
            const items = [
                { label: 'Server Up', ok: report.server_up },
                { label: 'HLS Push', ok: report.hls_push_ok },
                { label: 'HLS Read', ok: report.hls_read_ok }
            ];
            items.forEach(it => {
                const card = document.createElement('div');
                card.style.background = it.ok ? '#e8f5e9' : '#ffebee';
                card.style.padding = '10px';
                card.style.borderRadius = '6px';
                card.innerText = it.label;
                cardsDiv.appendChild(card);
            });
        }
    } catch (e) {
        console.error(e);
    }
}

async function runVideoPlayerTest(mode) {
    const selector = document.getElementById('test-video-selector');
    const videoPath = selector?.value;
    if (!videoPath) return;

    const startTime = performance.now();
    const entry = {
        id: Date.now(),
        date: new Date().toLocaleTimeString(),
        name: selector.options[selector.selectedIndex].text,
        mode: mode,
        status: 'running',
        time: '...',
        details: 'Test läuft...'
    };
    videoTestHistory.unshift(entry);
    updateTestResultsTable();

    try {
        if (mode === 'direct') {
            if (typeof switchTab === 'function') switchTab('video');
            if (typeof playVideo === 'function') await playVideo({path: videoPath}, videoPath);
            const res = await monitorVjsPlayback();
            entry.status = res.status;
            entry.details = res.details;
        } else if (mode === 'vlc') {
            await triggerVLCPlay();
            entry.status = 'pass';
        }
        entry.time = ((performance.now() - startTime) / 1000).toFixed(2) + 's';
    } catch (err) {
        entry.status = 'fail';
        entry.details = err.message;
    }
    updateTestResultsTable();
}

function monitorVjsPlayback(timeoutMs = 15000) {
    return new Promise((resolve, reject) => {
        if (typeof vjsPlayer === 'undefined') return reject("Video.js Player nicht initialisiert.");
        const startTime = Date.now();
        const checker = setInterval(() => {
            if (vjsPlayer.currentTime() > 0.1 && !vjsPlayer.paused()) {
                clearInterval(checker);
                resolve({ status: 'pass', details: 'Playback OK', time: ((Date.now() - startTime) / 1000).toFixed(2) });
            }
            if (Date.now() - startTime > timeoutMs) {
                clearInterval(checker);
                reject("Timeout");
            }
        }, 500);
    });
}

function updateTestResultsTable() {
    const body = document.getElementById('video-test-results-body');
    if (!body) return;
    body.innerHTML = videoTestHistory.map(e => `
        <tr>
            <td>${e.date}</td>
            <td>${e.name}</td>
            <td>${e.mode}</td>
            <td>${e.status}</td>
            <td>${e.time}</td>
            <td>${e.details}</td>
        </tr>
    `).join('');
}

function clearTestHistory() {
    videoTestHistory = [];
    updateTestResultsTable();
}

async function runCodecMatrix() {
    try {
        const res = await eel.run_video_matrix_test()();
        if (res.status === 'ok' && typeof showToast === 'function') showToast("Matrix Erfolg");
    } catch (err) {
        console.error(err);
    }
}

// Created with MWV v1.46.00-MASTER
