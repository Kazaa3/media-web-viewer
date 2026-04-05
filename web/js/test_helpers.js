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
 */
async function loadTestSuites(retryCount) {
    retryCount = retryCount || 0;
    const container = document.getElementById('test-suites-container');
    const scriptsList = document.getElementById('test-scripts-list');
    const routingList = document.getElementById('routing-test-scripts-list');
    if (!container) return;

    if (retryCount === 0) {
        const loadingHtml = `<div style="color: #999; font-style: italic;" data-i18n="test_loading">${typeof t === 'function' ? t('test_loading', 'Suites werden geladen...') : 'Suites werden geladen...'}</div>`;
        if (container) container.innerHTML = loadingHtml;
        if (scriptsList) scriptsList.innerHTML = loadingHtml;
        if (routingList) routingList.innerHTML = loadingHtml;
    }

    try {
        const res = await eel.get_test_suites()();
        let suites = res || [];

        // Append the GUI Test as a fake suite
        suites.push({
            id: 'gui_test_fake',
            name: 'GUI Tests (Selenium)',
            folder: '',
            isGuiTest: true,
            metadata: {
                category: "E2E Test",
                inputs: "Browser Interactions",
                outputs: "DOM State",
                files: "App HTML",
                comment: typeof t === 'function' ? t('test_gui_comment', 'Interaktive E2E Tests im Browser.') : 'Interaktive E2E Tests im Browser.'
            }
        });

        if (container) container.innerHTML = '';
        if (scriptsList) scriptsList.innerHTML = '';
        if (routingList) routingList.innerHTML = '';

        // Group by folder
        const groups = {};
        suites.forEach(suite => {
            let folder = suite.folder || 'Root';
            if (folder.toLowerCase().startsWith('ui')) folder = 'UI/' + folder.slice(2).replace(/^\/+/, '');
            if (!groups[folder]) groups[folder] = [];
            groups[folder].push(suite);
        });

        // Sort folders
        const sortedFolders = Object.keys(groups).sort((a, b) => {
            const isAUI = a.toLowerCase().startsWith('ui');
            const isBUI = b.toLowerCase().startsWith('ui');
            if (isAUI && !isBUI) return -1;
            if (!isAUI && isBUI) return 1;
            if (a === 'Root') return 1;
            if (b === 'Root') return -1;
            return a.localeCompare(b);
        });

        const fragContainer = document.createDocumentFragment();
        const fragScripts = document.createDocumentFragment();
        const fragRouting = document.createDocumentFragment();

        sortedFolders.forEach(folder => {
            const folderSuites = groups[folder].sort((a, b) => a.name.localeCompare(b.name));
            if (folderSuites.length === 0) return;

            const folderLabel = folder === 'Root' ? (typeof t === 'function' ? t('test_suites_root', 'Core Utilities & Tests') : 'Core Utilities & Tests') : folder;
            const isUI = folder.toLowerCase().startsWith('ui');
            const headerStyle = `grid-column: 1/-1; width: 100%; padding: 15px 5px 5px 5px; font-weight: bold; font-size: 1.1em; color: var(--text-primary); border-bottom: 2px solid var(--border-color); margin-top: 20px; display: flex; align-items: center; gap: 8px; background: ${isUI ? 'rgba(52, 152, 219, 0.1)' : 'var(--glass-bg)'}; backdrop-filter: blur(5px); position: sticky; top: 0; z-index: 100;`;
            header.style.cssText = headerStyle;
            header.innerHTML = `<span>${folder === 'Root' ? '<svg width="12" height="12"><use href="#icon-folder"></use></svg>' : (isUI ? '<svg width="12" height="12"><use href="#icon-tv"></use></svg>️' : '<svg width="12" height="12"><use href="#icon-folder"></use></svg>')}</span> ${folderLabel}`;

            fragContainer.appendChild(header.cloneNode(true));
            fragScripts.appendChild(header.cloneNode(true));
            if (folder.toLowerCase().includes('routing')) fragRouting.appendChild(header.cloneNode(true));

            folderSuites.forEach(suite => {
                const card = createTestCard(suite);
                fragContainer.appendChild(card.cloneNode(true));
                fragScripts.appendChild(card.cloneNode(true));
                if (folder.toLowerCase().includes('routing')) fragRouting.appendChild(card.cloneNode(true));
            });
        });

        if (container) container.appendChild(fragContainer);
        if (scriptsList) scriptsList.appendChild(fragScripts);
        if (routingList) routingList.appendChild(fragRouting);

        if (typeof syncVersionInfo === 'function') syncVersionInfo();

    } catch (e) {
        console.error('[loadTestSuites] Error:', e);
        const errorHtml = `<div style="color: #c33; padding: 20px;">${typeof t === 'function' ? t('test_error_loading', 'Fehler beim Laden der Tests: ') : 'Fehler beim Laden der Tests: '}${e}</div>`;
        if (container) container.innerHTML = errorHtml;
    }
}

function createTestCard(suite) {
    const card = document.createElement('div');
    card.className = 'glass-card';
    card.style.cssText = 'padding: 20px; display: flex; flex-direction: column; position: relative; transition: transform 0.2s, box-shadow 0.2s;';
    
    const isInteractiveBrowserTest = (suiteId) => {
        const name = String(suiteId || '').toLowerCase();
        const patterns = ['test_route', 'test_network', 'run_app', 'pyautogui', 'selenium', 'gui_test'];
        return patterns.some(pattern => name.includes(pattern));
    };

    let checkboxHtml = '';
    if (suite.isGuiTest) {
        checkboxHtml = `<input type="checkbox" id="test-gui" style="width: 20px; height: 20px; cursor: pointer;">`;
    } else {
        const checkedAttr = isInteractiveBrowserTest(suite.id) ? '' : 'checked';
        checkboxHtml = `<input type="checkbox" class="test-suite-checkbox" value="${suite.id}" ${checkedAttr} style="width: 20px; height: 20px; cursor: pointer;">`;
    }

    const m = suite.metadata || {};
    const categoryHtml = m.category && m.category !== '-' ? `<span style="background: #e3f2fd; color: #1565c0; padding: 4px 8px; border-radius: 4px; font-size: 0.75em; font-weight: bold;">${m.category}</span>` : '';

    card.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                ${checkboxHtml}
                <h3 style="margin: 0; font-size: 1.1em; color: var(--text-primary);">${suite.name}</h3>
            </div>
            <div class="test-card-actions" style="display: flex; align-items: center; gap: 8px;">
                ${categoryHtml}
            </div>
        </div>
        <div style="display: grid; grid-template-columns: auto 1fr; gap: 8px 15px; font-size: 0.85em; color: var(--text-secondary); margin-bottom: 15px;">
            <strong style="color: var(--text-primary);">${typeof t === 'function' ? t('test_meta_inputs') : 'Inputs'}:</strong> <span>${m.inputs || '-'}</span>
            <strong style="color: var(--text-primary);">${typeof t === 'function' ? t('test_meta_outputs') : 'Outputs'}:</strong> <span>${m.outputs || '-'}</span>
            <strong style="color: var(--text-primary);">${typeof t === 'function' ? t('test_meta_files') : 'Files'}:</strong> <span style="font-family: monospace; background: var(--bg-secondary); color: var(--accent-color); padding: 2px 4px; border-radius: 3px;">${m.files || '-'}</span>
        </div>
        <div style="margin-top: auto; padding-top: 15px; border-top: 1px solid var(--border-color); font-size: 0.85em; color: var(--text-secondary); font-style: italic; opacity: 0.8;">
            ${m.comment || '-'}
        </div>
    `;

    if (!suite.isGuiTest) {
        const editBtn = document.createElement('button');
        editBtn.innerText = typeof t === 'function' ? t('test_btn_edit') : 'Edit';
        editBtn.style.cssText = 'border: none; background: var(--bg-secondary); color: var(--text-primary); border-radius: 6px; padding: 4px 12px; font-size: 0.85em; cursor: pointer; transition: all 0.2s;';
        editBtn.onclick = (e) => { e.stopPropagation(); openTestEditModal(suite); };
        
        const delBtn = document.createElement('button');
        delBtn.innerHTML = '<svg width="12" height="12" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg>';
        delBtn.style.cssText = 'border: none; background: transparent; color: #ff5252; border-radius: 4px; padding: 4px 6px; cursor: pointer; opacity: 0.6; transition: all 0.2s;';
        delBtn.onclick = (e) => {
            e.stopPropagation();
            if (confirm(typeof t === 'function' ? t('confirm_delete') : 'Delete?')) deleteTest(suite.id);
        };
        
        const actionsArea = card.querySelector('.test-card-actions');
        if (actionsArea) {
            actionsArea.prepend(editBtn);
            actionsArea.appendChild(delBtn);
        }
    }

    return card;
}

async function runSelectedTests() {
    if (isTestRunInProgress) return;

    const checkboxes = document.querySelectorAll('.test-suite-checkbox:checked');
    const selectedFiles = Array.from(checkboxes).map(cb => cb.value);
    const guiTest = document.getElementById('test-gui') && document.getElementById('test-gui').checked;
    const runBtn = document.getElementById('run-selected-tests-btn');
    
    isTestRunInProgress = true;
    if (runBtn) {
        runBtn.disabled = true;
        runBtn.style.opacity = '0.65';
        runBtn.style.cursor = 'wait';
    }

    const resultsContainer = document.getElementById('test-results-container');
    const outputArea = document.getElementById('test-output');
    const summaryBadge = document.getElementById('test-run-summary');

    if (!outputArea || !summaryBadge) return;

    if (resultsContainer) {
        resultsContainer.style.display = 'block';
        resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }

    __testOutputBuffer = '';
    appendTestOutputChunk(`${typeof t === 'function' ? t('test_run_starting') : 'Starting test run...'}\n`);
    summaryBadge.style.display = 'none';

    let totalPasses = 0;
    let totalFails = 0;

    try {
        if (selectedFiles.length > 0) {
            const result = await eel.run_tests(selectedFiles)();
            if (result.error) {
                appendTestOutputChunk(`${typeof t === 'function' ? t('test_run_error') : 'Error: '}${result.error}\n`);
            } else {
                appendTestOutputChunk(`\n[Python Tests - Exit Code: ${result.exit_code}]\n`);
                if (result.passes !== undefined) totalPasses += result.passes;
                if (result.fails !== undefined) totalFails += result.fails;
            }
        }

        if (guiTest) {
            try {
                const guiRes = await eel.run_gui_tests()();
                appendTestOutputChunk(`\n\n[GUI-Tests] ${guiRes.message}`);
            } catch (e) {
                appendTestOutputChunk(`\n\n[GUI-Tests] Error: ${e}`);
            }
        }

        if (selectedFiles.length > 0) {
            summaryBadge.style.display = 'inline-block';
            if (totalFails > 0) {
                summaryBadge.textContent = `${totalFails} Failed, ${totalPasses} Passed`;
                summaryBadge.style.background = 'rgba(255, 82, 82, 0.15)';
                summaryBadge.style.color = '#ff5252';
            } else {
                summaryBadge.textContent = `Alle ${totalPasses} Tests Passed`;
                summaryBadge.style.background = 'rgba(46, 204, 113, 0.15)';
                summaryBadge.style.color = '#2ecc71';
            }
        }
    } catch (e) {
        appendTestOutputChunk(`System Error: ${e}\n`);
    } finally {
        isTestRunInProgress = false;
        if (runBtn) {
            runBtn.disabled = false;
            runBtn.style.opacity = '1';
            runBtn.style.cursor = 'pointer';
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
