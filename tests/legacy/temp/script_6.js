// Pre-define critical functions to avoid "not defined" errors on button clicks
        let activeAudioPipeline;
        let currentLogbuchEntries = [];
        let currentLogbookEditName = null;
        let currentLogbookEditFilename = null;
        let lastSyncState = null;

        function appendUiTrace(message) {
            const timestamp = new Date().toLocaleTimeString();
            const line = `[UI-Trace ${timestamp}] ${message}`;
            console.warn(line);

            try {
                if (typeof eel !== 'undefined' && typeof eel.ui_trace === 'function') {
                    eel.ui_trace(line)();
                }
            } catch (e) {
                // Keep tracing non-blocking
            }

            const debugOutput = document.getElementById('debug-output');
            if (debugOutput) {
                const prefix = debugOutput.textContent && !debugOutput.textContent.endsWith('\n') ? '\n' : '';
                debugOutput.textContent += `${prefix}${line}\n`;
                debugOutput.scrollTop = debugOutput.scrollHeight;
            }

            const resultsContainer = document.getElementById('test-results-container');
            const testOutput = document.getElementById('test-output');
            if (resultsContainer && testOutput && resultsContainer.style.display !== 'none') {
                const prefix = testOutput.textContent && !testOutput.textContent.endsWith('\n') ? '\n' : '';
                testOutput.textContent += `${prefix}${line}\n`;
                testOutput.scrollTop = testOutput.scrollHeight;
            }
        }
        eel.expose(appendUiTrace);

        function getTabButton(tabId) {
            const btn = document.querySelector(`.tab-btn[onclick*="switchTab('${tabId}')"]`);
            if (btn) return btn;
            // Fallback Mapping for robust ID-based lookup
            const idMap = {
                'player': 'active-queue-tab-trigger',
                'library': 'coverflow-library-tab-trigger',
                'item': 'indexed-sqlite-repository-tab-trigger',
                'file': 'filesystem-crawler-tab-trigger',
                'edit': 'crud-metadata-tab-trigger',
                'options': 'system-registry-tab-trigger',
                'parser': 'chain-config-tab-trigger',
                'debug': 'telemetry-inspector-tab-trigger',
                'tests': 'qa-validation-tab-trigger',
                'reporting': 'reporting-dashboard-tab-trigger',
                'logbuch': 'documentation-journal-tab-trigger',
                'playlist': 'sequential-buffer-tab-trigger',
                'vlc': 'media-orchestrator-tab-trigger'
            };
            return document.getElementById(idMap[tabId]);
        }

        let mwv_config = {
            start_page: 'player',
            app_mode: 'High-Performance',
            parser_mode: 'lightweight'
        };

        async function loadConfig() {
            try {
                const response = await fetch('config.json');
                if (response.ok) {
                    mwv_config = await response.json();
                    console.log('Global config loaded:', mwv_config);
                }
            } catch (e) {
                console.warn('Failed to load config.json:', e);
            }
        }

        // Safety Utilities for DOM access
        function safeStyle(id, prop, value) {
            const el = document.getElementById(id);
            if (el) el.style[prop] = value;
        }

        function safeText(id, text) {
            const el = document.getElementById(id);
            if (el) el.innerText = text;
        }

        function safeHtml(id, html) {
            const el = document.getElementById(id);
            if (el) el.innerHTML = html;
        }

        function safeValue(id, val) {
            const el = document.getElementById(id);
            if (el) el.value = val;
        }

        function readValue(id, fallback = '') {
            const el = document.getElementById(id);
            return el ? el.value : fallback;
        }

        function readText(id, fallback = '') {
            const el = document.getElementById(id);
            return el ? el.innerText : fallback;
        }

        function restoreLastActiveTab() {
            try {
                // Default to 'player' or global config unless explicitly saved and not 'playlist'
                let savedTab = localStorage.getItem('mwv_active_tab');
                if (!savedTab || savedTab === 'playlist') {
                    savedTab = mwv_config.start_page || 'player';
                }
                const savedBtn = getTabButton(savedTab);
                if (savedBtn) {
                    switchTab(savedTab, savedBtn);
                } else {
                    // Fallback if button not found
                    switchTab('player', getTabButton('player'));
                }
            } catch (e) {
                // Ignore storage/access errors
            }
        }

        function switchTab(tabId, btn) {
            const previousTab = localStorage.getItem('mwv_active_tab') || 'player';
            appendUiTrace(`switchTab: ${previousTab} → ${tabId}`);

            // Reset all tabs
            document.querySelectorAll('.tab-content').forEach(el => {
                el.classList.remove('active');
                el.style.display = 'none';
            });
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));

            const tabMap = {
                'player': 'state-orchestrated-active-queue-list-container',
                'library': 'coverflow-library-panel',
                'item': 'indexed-sqlite-media-repository-panel',
                'file': 'filesystem-crawler-directory-panel',
                'edit': 'metadata-writer-crud-panel',
                'options': 'system-configuration-persistence-panel',
                'parser': 'regex-provider-chain-orchestrator-panel',
                'debug': 'debug-flag-persistence-panel',
                'tests': 'quality-assurance-regression-suite-panel',
                'reporting': 'reporting-dashboard-panel',
                'logbuch': 'localized-markdown-documentation-journal-panel',
                'playlist': 'json-serialized-sequence-buffer-panel',
                'vlc': 'multiplexed-media-player-orchestrator-panel',
                'video': 'multiplexed-media-player-orchestrator-panel',
                'tools': 'tools-tab'
            };

            const targetId = tabMap[tabId];
            if (targetId) {
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.classList.add('active');
                    // Ensure block display for library and file tabs, flex for debug/edit, block for others
                    if (tabId === 'debug' || tabId === 'edit') {
                        targetEl.style.display = 'flex';
                    } else if (tabId === 'file') {
                        targetEl.style.display = 'flex';
                        loadLibraryFolders();
                    } else if (tabId === 'reporting') {
                        targetEl.style.display = 'block';
                        switchReportingView('dashboard');
                        loadSqlFiles();
                        refreshReportingData(); // Auto-refresh for user convenience
                    } else if (tabId === 'tests') {
                        targetEl.style.display = 'flex';
                        switchTestView('base');
                    } else if (tabId === 'options') {
                        targetEl.style.display = 'block';
                        switchOptionsView('general');
                    } else if (tabId === 'parser') {
                        targetEl.style.display = 'block';
                    } else {
                        targetEl.style.display = 'block';
                    }

                    if (tabId === 'library') renderLibrary();
                    if (tabId === 'item') refreshLibrary();
                    if (tabId === 'parser') loadParserPerformance('parser-tab-perf-container');
                    // The loadLibraryFolders for 'file' tab is now handled in the display logic above
                    // The loadSqlFiles for 'reporting' tab is now handled in the display logic above
                } else {
                    console.warn(`[UI] Target element not found for tab: ${tabId} (id: ${targetId})`);
                }
            }
            if (btn) {
                btn.classList.add('active');
            }

            try {
                localStorage.setItem('mwv_active_tab', tabId);
            } catch (e) {
                // Ignore storage/access errors
            }

            const sidebar = document.querySelector('.sidebar');
            const splitter = document.getElementById('main-splitter');
            if (sidebar) sidebar.style.display = (tabId === 'player' || tabId === 'vlc' || tabId === 'video') ? '' : 'none';
            if (splitter) splitter.style.display = (tabId === 'player' || tabId === 'vlc' || tabId === 'video') ? '' : 'none';

            if (tabId === 'player') {
                if (typeof loadLibrary === 'function') loadLibrary();
            }
            if (tabId === 'file' && !fbCurrentPath) {
                if (typeof fbNavigate === 'function') fbNavigate();
            }
            if (tabId === 'library') {
                if (typeof refreshLibrary === 'function') refreshLibrary();
            }
            if (tabId === 'options') {
                if (typeof loadDebugFlags === 'function') loadDebugFlags();
                if (typeof loadEnvironmentInfo === 'function') loadEnvironmentInfo();
                loadScanDirs();
            }
            if (tabId === 'edit') {
                if (typeof loadEditItems === 'function') loadEditItems();
            }
            if (tabId === 'debug') {
                if (typeof loadDebugLogs === 'function') loadDebugLogs();
                // Start auto-refresh for logs
                if (!window._debugLogInterval) {
                    window._debugLogInterval = setInterval(() => {
                        const activeTab = localStorage.getItem('mwv_active_tab');
                        if (activeTab === 'debug') {
                            loadDebugLogs();
                        } else {
                            clearInterval(window._debugLogInterval);
                            window._debugLogInterval = null;
                        }
                    }, 2000);
                }
            } else {
                if (window._debugLogInterval) {
                    clearInterval(window._debugLogInterval);
                    window._debugLogInterval = null;
                }
            }
            if (tabId === 'logbuch') {
                if (typeof loadLogbuchTab === 'function') loadLogbuchTab();
            }
            if (tabId === 'tests') {
                if (typeof loadTestSuites === 'function') loadTestSuites();
            }
        }

        async function runRTTTest(testType = 'ping') {
            const statusEl = document.getElementById('rtt-status-text');
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

                appendUiTrace(`RTT [${testType}]: Sending data to backend...`);
                const start = performance.now();
                const response = await eel.rtt_ping(testData)();
                const end = performance.now();
                const rtt = (end - start).toFixed(2);

                appendUiTrace(`RTT [${testType}]: Backend responded in ${rtt}ms. Status: ${response.status}`);

                // Confirm Receipt
                await eel.confirm_receipt(testType === 'complex' ? "ITEM_RTT_RECEIVED" : "RTT_PONG_RECEIVED")();

                if (statusEl) {
                    statusEl.innerHTML = `${testType.toUpperCase()}: <strong style="color: #2a7;">${rtt}ms</strong> (Sync OK)`;
                }
            } catch (e) {
                appendUiTrace(`RTT [${testType}] Error: ${e}`);
                if (statusEl) statusEl.innerText = "Error: " + e;
            } finally {
                btns.forEach(btn => btn.disabled = false);
            }
        }

        async function runWebSocketStressTest() {
            const statusEl = document.getElementById('rtt-status-text');
            const btns = document.querySelectorAll('#options-sync-view .action-btn');
            const count = 100;
            let successes = 0;
            let totalTime = 0;

            if (statusEl) statusEl.innerText = `Starting Stress Test (0/${count})...`;
            btns.forEach(btn => btn.disabled = true);

            try {
                appendUiTrace(`[Stress] Starting WebSocket stress test: ${count} pings...`);
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
                    // Add a small delay between batches to prevent socket congestion
                    await new Promise(resolve => setTimeout(resolve, 50));
                }

                const endTotal = performance.now();
                const avgRtt = (totalTime / count).toFixed(2);
                const totalDuration = (endTotal - startTotal).toFixed(0);

                appendUiTrace(`[Stress] Finished: ${successes}/${count} OK. Avg RTT: ${avgRtt}ms. Total: ${totalDuration}ms`);

                if (statusEl) {
                    statusEl.innerHTML = `STRESS: <strong style="color: #2a7;">${successes}/${count} OK</strong> (Avg: ${avgRtt}ms, Total: ${totalDuration}ms)`;
                }
            } catch (e) {
                appendUiTrace(`[Stress] Error: ${e}`);
                if (statusEl) statusEl.innerText = "Stress Error: " + e;
            } finally {
                btns.forEach(btn => btn.disabled = false);
            }
        }

        function switchOptionsView(viewId) {
            console.log("Switching options view to:", viewId);
            document.querySelectorAll('.options-view').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.options-subtab').forEach(el => el.classList.remove('active'));

            const target = document.getElementById('options-' + viewId + '-view');
            if (target) {
                target.style.display = (viewId === 'general' || viewId === 'environment') ? 'flex' : 'block';
                const btn = document.querySelector(`.options-subtab[onclick*="'${viewId}'"]`);
                if (btn) {
                    btn.classList.add('active');
                    // Update main header to reflect sub-chapter title
                    const header = document.getElementById('options-main-header');
                    if (header) {
                    }
                }
            }
        }

        function switchParserView(viewId) {
            console.log("Switching parser view to:", viewId);
            document.querySelectorAll('.parser-view').forEach(el => el.style.display = 'none');
            document.querySelectorAll('.options-subtab').forEach(el => {
                if (el.id && el.id.startsWith('parser-subtab-')) {
                    el.classList.remove('active');
                }
            });

            const target = document.getElementById('parser-' + viewId + '-view');
            if (target) {
                target.style.display = 'block';
                const btn = document.getElementById('parser-subtab-' + viewId);
                if (btn) btn.classList.add('active');
            }
        }

        // --- Reporting View & SQL Logic ---
        function switchReportingView(view) {
            const views = {
                'dashboard': document.getElementById('reporting-dashboard-view'),
                'database': document.getElementById('reporting-database-view'),
                'video-streaming': document.getElementById('reporting-video-streaming-view'),
                'audio-streaming': document.getElementById('reporting-audio-streaming-view'),
                'parser': document.getElementById('reporting-parser-view'),
                'model-analysis': document.getElementById('reporting-model-analysis-view'),
                'routing-suite': document.getElementById('reporting-routing-suite-view')
            };

            for (const [key, el] of Object.entries(views)) {
                if (el) el.style.display = (view === key) ? 'block' : 'none';
            }

            // Highlighting for new button-based navigation
            document.querySelectorAll('.reporting-subtab').forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('data-view') === view);
            });

            if (view === 'database') loadSqlFiles();
            if (view === 'video-streaming') loadVideoStreamingBenchmarks('video');
            if (view === 'audio-streaming') loadVideoStreamingBenchmarks('audio');
            if (view === 'parser') loadParserPerformance();
            if (view === 'model-analysis') loadModelAnalysis();
            if (view === 'routing-suite') loadRoutingSuiteReport();
        }

        // --- Quality Assurance & Test Suite Logic ---
        function switchTestView(view) {
            document.querySelectorAll('#quality-assurance-regression-suite-panel .test-view-content').forEach(el => {
                el.style.display = 'none';
            });
            document.querySelectorAll('#quality-assurance-regression-suite-panel .options-subtab').forEach(el => {
                el.classList.remove('active');
            });

            const targetView = document.getElementById(`test-${view}-view`);
            if (targetView) targetView.style.display = 'block';

            const btn = document.querySelector(`#quality-assurance-regression-suite-panel .options-subtab[data-view="${view}"]`);
            if (btn) btn.classList.add('active');
            
            if (view === 'suite') {
                loadTestSuites();
            }
        }

        async function runJsErrorScan() {
            const resultsDiv = document.getElementById('js-error-scan-results');
            if (!resultsDiv) return;
            resultsDiv.innerText = "Scanning app.html for potential null-dereferences...";
            resultsDiv.style.color = "#333";
            
            try {
                const res = await eel.scan_js_errors()();
                if (res.status === 'ok') {
                    if (res.findings.length === 0) {
                        resultsDiv.innerText = "✅ No obvious unguarded DOM accesses found.";
                        resultsDiv.style.color = "#2a7";
                    } else {
                        resultsDiv.style.color = "#c62828";
                        let text = `⚠️ Found ${res.findings.length} potential JS null-access issues:\n\n`;
                        res.findings.forEach(f => {
                            text += `Line ${f.line}: ${f.desc}\n   -> ${f.content}\n\n`;
                        });
                        resultsDiv.innerText = text;
                    }
                } else {
                    resultsDiv.innerText = "Error: " + res.message;
                    resultsDiv.style.color = "#c62828";
                }
            } catch (e) {
                resultsDiv.innerText = "System Error: " + e;
                resultsDiv.style.color = "#c62828";
            }
        }

        async function runUiIntegrityCheck() {
            const resultsDiv = document.getElementById('ui-integrity-results');
            if (!resultsDiv) return;
            resultsDiv.innerHTML = "<div style='grid-column: span 2;'>Running integrity checks...</div>";
            
            try {
                const res = await eel.check_ui_integrity()();
                if (res.status === 'ok') {
                    resultsDiv.innerHTML = `
                        <div style="background: white; border: 1px solid #eee; border-radius: 12px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <h4 style="margin: 0 0 10px 0;">Div Tag Balance</h4>
                            <div style="font-size: 1.2em; font-weight: bold; color: ${res.div_balance.balanced ? '#2a7' : '#c62828'};">
                                ${res.div_balance.balanced ? '✅ Balanced' : '❌ Unbalanced'}
                            </div>
                            <div style="font-size: 0.85em; color: #666; margin-top: 5px;">
                                ${res.div_balance.opens} opens / ${res.div_balance.closes} closes
                            </div>
                        </div>
                        <div style="background: white; border: 1px solid #eee; border-radius: 12px; padding: 15px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <h4 style="margin: 0 0 10px 0;">Duplicate Functions</h4>
                            <div style="font-size: 1.2em; font-weight: bold; color: ${res.duplicates.length === 0 ? '#2a7' : '#c62828'};">
                                ${res.duplicates.length === 0 ? '✅ None' : '❌ ' + res.duplicates.length + ' Found'}
                            </div>
                            <div style="font-size: 0.75em; color: #666; margin-top: 5px; max-height: 100px; overflow-y: auto; font-family: monospace;">
                                ${res.duplicates.join(', ') || 'No duplicates detected.'}
                            </div>
                        </div>
                        <div style="background: white; border: 1px solid #eee; border-radius: 12px; padding: 15px; grid-column: span 2; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <h4 style="margin: 0 0 10px 0;">Orphaned Catch Blocks</h4>
                            <div style="font-size: 1.2em; font-weight: bold; color: ${res.orphaned_catches.length === 0 ? '#2a7' : '#c62828'};">
                                ${res.orphaned_catches.length === 0 ? '✅ None' : '❌ ' + res.orphaned_catches.length + ' Found'}
                            </div>
                            <div style="font-size: 0.75em; color: #666; margin-top: 5px; font-family: monospace;">
                                ${res.orphaned_catches.length > 0 ? 'Potentially missing try block at lines: ' + res.orphaned_catches.join(', ') : 'No orphan blocks found.'}
                            </div>
                        </div>
                    `;
                } else {
                    resultsDiv.innerHTML = `<div style='grid-column: span 2; color: #c62828;'>Error: ${res.message}</div>`;
                }
            } catch (e) {
                resultsDiv.innerHTML = `<div style='grid-column: span 2; color: #c62828;'>System Error: ${e}</div>`;
            }
        }

        function refreshTestViews() {
            // Find active subtab
            const activeBtn = document.querySelector('#quality-assurance-regression-suite-panel .options-subtab.active');
            if (!activeBtn) return;
            const view = activeBtn.getAttribute('data-view');
            
            if (view === 'suite') loadTestSuites();
            else if (view === 'jserror') runJsErrorScan();
            else if (view === 'startup') runUiIntegrityCheck();
            else if (view === 'base') runRTTTest('ping');
        }

        async function loadSqlFiles() {
            const list = document.getElementById('sql-file-list');
            if (!list) return;
            const files = await eel.list_sql_files()();
            list.innerHTML = '';
            files.forEach(file => {
                const btn = document.createElement('button');
                btn.className = 'tab-btn';
                btn.style.width = '100.0%';
                btn.style.textAlign = 'left';
                btn.style.marginBottom = '5px';
                btn.style.background = '#fff';
                btn.textContent = file;
                btn.onclick = () => loadSqlContent(file);
                list.appendChild(btn);
            });
        }

        async function loadSqlContent(filename) {
            const content = await eel.get_sql_content(filename)();
            safeHtml('sql-content-renderer', content);
            safeText('selected-sql-filename', filename);
        }

        async function loadVideoStreamingBenchmarks(type = 'all') {
            const container = (type === 'audio') ? document.getElementById('audio-benchmarks-list') : document.getElementById('video-benchmarks-list');
            if (!container) return;

            // Header for Multimedia Analysis (only for video)
            let analysisHtml = '';
            if (type === 'video') {
                const analysis = await eel.get_multimedia_analysis()();
                if (analysis && !analysis.error) {
                    analysisHtml = `<div style="margin-bottom: 30px; background: #fff; border-radius: 12px; border: 1px solid #e0e0e0; padding: 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                        <h4 style="margin: 0 0 15px 0; color: #2c3e50; display: flex; align-items: center; gap: 8px;">
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
                            Multimedia Library Analysis
                        </h4>
                        
                        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 25px;">
                            <div style="background: #e3f2fd; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #bbdefb;">
                                <div style="font-size: 0.75em; color: #1976d2; font-weight: bold; text-transform: uppercase;">Library Health</div>
                                <div style="font-size: 1.6em; font-weight: 800; color: #0d47a1;">${((analysis.stats.native_support_count / (analysis.stats.total_films + analysis.stats.total_dvds || 1)) * 100).toFixed(1)}%</div>
                                <div style="font-size: 0.7em; color: #666;">Chrome Native Ready</div>
                            </div>
                            <div style="background: #f1f8e9; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #c8e6c9;">
                                <div style="font-size: 0.75em; color: #388e3c; font-weight: bold; text-transform: uppercase;">Film Objects</div>
                                <div style="font-size: 1.6em; font-weight: 800; color: #1b5e20;">${analysis.stats.total_films}</div>
                                <div style="font-size: 0.7em; color: #666;">Categorized as Film</div>
                            </div>
                            <div style="background: #fff3e0; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #ffe0b2;">
                                <div style="font-size: 0.75em; color: #e65100; font-weight: bold; text-transform: uppercase;">Disc Images</div>
                                <div style="font-size: 1.6em; font-weight: 800; color: #e65100;">${analysis.stats.total_dvds}</div>
                                <div style="font-size: 0.7em; color: #666;">ISO / BIN / Folder</div>
                            </div>
                            <div style="background: #f3e5f5; padding: 15px; border-radius: 10px; text-align: center; border: 1px solid #e1bee7;">
                                <div style="font-size: 0.75em; color: #7b1fa2; font-weight: bold; text-transform: uppercase;">Incompatible</div>
                                <div style="font-size: 1.6em; font-weight: 800; color: #4a148c;">${analysis.incompatible_videos.length}</div>
                                <div style="font-size: 0.7em; color: #666;">Requires VLC/Transcode</div>
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-top: 20px;">
                            <div>
                                <h5 style="margin: 0 0 10px 0; font-size: 0.9em; color: #555;">Detected DVD & Film Objects</h5>
                                <div style="max-height: 250px; overflow-y: auto; border: 1px solid #eee; border-radius: 6px;">
                                    <table style="width: 100%; border-collapse: collapse; font-size: 0.85em;">
                                        <thead style="background: #f5f5f5; position: sticky; top: 0;">
                                            <tr>
                                                <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Name</th>
                                                <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Type</th>
                                                <th style="padding: 8px; text-align: center; border-bottom: 1px solid #ddd;">Status</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${[...analysis.dvd_objects, ...analysis.film_objects].map(obj => `
                                                <tr style="border-bottom: 1px solid #f0f0f0;">
                                                    <td style="padding: 8px; font-weight: 500;">${obj.name}</td>
                                                    <td style="padding: 8px;"><span style="padding: 2px 6px; background: #eee; border-radius: 4px; font-size: 0.85em;">${obj.type}</span></td>
                                                    <td style="padding: 8px; text-align: center;">
                                                        <span style="color: #4caf50; font-size: 1.1em;">✓</span>
                                                    </td>
                                                </tr>
                                            `).join('') || '<tr><td colspan="3" style="padding: 15px; text-align: center; color: #999;">No objects detected.</td></tr>'}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div>
                                <h5 style="margin: 0 0 10px 0; font-size: 0.9em; color: #d32f2f;">Chrome Incompatible Content</h5>
                                <div style="max-height: 250px; overflow-y: auto; border: 1px solid #eee; border-radius: 6px;">
                                    <table style="width: 100%; border-collapse: collapse; font-size: 0.85em;">
                                        <thead style="background: #fff5f5; position: sticky; top: 0;">
                                            <tr>
                                                <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Name</th>
                                                <th style="padding: 8px; text-align: left; border-bottom: 1px solid #ddd;">Reason</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${analysis.incompatible_videos.map(v => `
                                                <tr style="border-bottom: 1px solid #fff5f5;">
                                                    <td style="padding: 8px; font-weight: 500;">${v.name}</td>
                                                    <td style="padding: 8px; color: #d32f2f;">${v.reason} <small>(${v.codec})</small></td>
                                                </tr>
                                            `).join('') || '<tr><td colspan="2" style="padding: 15px; text-align: center; color: #999;">All good! No incompatible videos found.</td></tr>'}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>

                        <div style="margin-top: 30px;">
                            <h5 style="margin: 0 0 10px 0; font-size: 0.9em; color: #555;">Technical Tool & Mode Matrix</h5>
                            <div style="overflow-x: auto; border: 1px solid #eee; border-radius: 6px;">
                                <table style="width: 100%; border-collapse: collapse; font-size: 0.8em; line-height: 1.4;">
                                    <thead style="background: #f8f9fa;">
                                        <tr>
                                            <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Engine</th>
                                            <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Modes</th>
                                            <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Formats</th>
                                            <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd;">Features</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${(await eel.get_streaming_capability_matrix()()).map(m => `
                                            <tr style="border-bottom: 1px solid #f0f0f0;">
                                                <td style="padding: 10px;"><b>${m.engine}</b></td>
                                                <td style="padding: 10px; color: #666;">${m.modes.join(', ')}</td>
                                                <td style="padding: 10px;">
                                                    ${m.formats.join(', ')} 
                                                    ${m.codecs ? `<br><small style="color:#999;">${m.codecs.join(', ')}</small>` : ''}
                                                </td>
                                                <td style="padding: 10px; color: #444;">
                                                    <div>${m.features.join(' • ')}</div>
                                                    <div style="font-size: 0.9em; color: #888; font-style: italic; margin-top: 4px;">${m.notes || ''}</div>
                                                </td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                        </div>

                        <div style="margin-top: 30px;">
                            <h5 style="margin: 0 0 10px 0; font-size: 0.9em; color: #555;">Item Compatibility Check (By Item / Format)</h5>
                            <div style="margin-bottom: 10px;">
                                <input type="text" id="compatibility-search" placeholder="Filter items..." oninput="filterCompatibilityTable()" 
                                       style="width: 100%; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 0.9em;">
                            </div>
                            <div style="max-height: 400px; overflow-y: auto; border: 1px solid #eee; border-radius: 6px;">
                                <table id="compatibility-table" style="width: 100%; border-collapse: collapse; font-size: 0.85em;">
                                    <thead style="background: #f8f9fa; position: sticky; top: 0; z-index: 10;">
                                        <tr>
                                            <th style="padding: 10px; text-align: left; border-bottom: 1px solid #ddd; width: 40%;">Item</th>
                                            <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">Chrome</th>
                                            <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">MediaMTX</th>
                                            <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">VLC</th>
                                            <th style="padding: 10px; text-align: center; border-bottom: 1px solid #ddd;">FFplay</th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        ${(await eel.get_media_compatibility_report()()).map(item => `
                                            <tr class="comp-row" style="border-bottom: 1px solid #f9f9f9;">
                                                <td style="padding: 10px;">
                                                    <div style="font-weight: 500;">${item.name}</div>
                                                    <div style="font-size: 0.8em; color: #888;">${item.category} | ${item.type} ${item.notes ? `| <span style="color: #e67e22;">${item.notes}</span>` : ''}</div>
                                                </td>
                                                <td style="padding: 10px; text-align: center;">${item.chrome_native ? '<span style="color:#4caf50;">●</span>' : '<span style="color:#f44336;">○</span>'}</td>
                                                <td style="padding: 10px; text-align: center;">${item.mediamtx ? '<span style="color:#4caf50;">●</span>' : '<span style="color:#f44336;">○</span>'}</td>
                                                <td style="padding: 10px; text-align: center;">${item.vlc ? '<span style="color:#4caf50;">●</span>' : '<span style="color:#f44336;">○</span>'}</td>
                                                <td style="padding: 10px; text-align: center;">${item.ffplay ? '<span style="color:#4caf50;">●</span>' : '<span style="color:#f44336;">○</span>'}</td>
                                            </tr>
                                        `).join('')}
                                    </tbody>
                                </table>
                            </div>
                            <div style="margin-top: 10px; font-size: 0.75em; color: #999;">
                                ● Native / Optimal Support | ○ Transcoding Required / Limited Support
                            </div>
                        </div>

                        <script>
                            function filterCompatibilityTable() {
                                const input = document.getElementById('compatibility-search');
                                const filter = input.value.toLowerCase();
                                const rows = document.querySelectorAll('.comp-row');
                                
                                rows.forEach(row => {
                                    const text = row.innerText.toLowerCase();
                                    row.style.display = text.includes(filter) ? '' : 'none';
                                });
                            }
                        <\/script>

                    </div>`;
                }
            }

            const history = await eel.get_benchmark_results()();
            if (!history || (Array.isArray(history) && history.length === 0)) {
                container.innerHTML = analysisHtml + '<p style="color: #999;">Keine Benchmark-Daten vorhanden.</p>';
                return;
            }

            let html = analysisHtml;
            const historyArr = Array.isArray(history) ? [...history] : [history];
            historyArr.reverse().forEach(run => {
                const ts = run.timestamp || (run.results ? (run.results.timestamp || Date.now() / 1000) : Date.now() / 1000);
                const date = new Date(ts * 1000).toLocaleString();

                let runHtml = '';
                const results = run.results || run;
                let foundMatch = false;

                for (const [name, res] of Object.entries(results)) {
                    if (name === "timestamp") continue;
                    if (!res || typeof res !== 'object') continue;

                    const isAudio = name.toLowerCase().includes('audio') || name.toLowerCase().includes('cvlc') || name.toLowerCase().includes('latency');
                    const isVideo = name.toLowerCase().includes('video') || name.toLowerCase().includes('ffplay') || name.toLowerCase().includes('stream');

                    if (type === 'audio' && !isAudio) continue;
                    if (type === 'video' && !isVideo) continue;

                    foundMatch = true;
                    const isOk = res.status === 'ok';
                    const color = isOk ? '#2e7d32' : '#c62828';
                    const icon = isOk ? '✅' : '❌';

                    runHtml += `<div style="padding: 15px; background: #f9f9f9; border-radius: 8px; border-left: 4px solid ${color};">
                                <div style="font-weight: bold; margin-bottom: 5px;">${icon} ${name}</div>
                                <div style="font-size: 0.85em; color: #666;">
                                    Status: <span style="color: ${color}; font-weight: bold;">${(res.status || 'unknown').toUpperCase()}</span><br>
                                    ${res.latency ? `Latency: <b>${res.latency.toFixed(4)}s</b><br>` : ''}
                                    ${res.error ? `<div style="margin-top: 5px; padding: 5px; background: #fee; color: #c33; font-family: monospace; font-size: 0.8em; overflow: auto; max-height: 120px; white-space: pre-wrap;">${res.error}</div>` : ''}
                                </div>
                             </div>`;
                }

                if (foundMatch) {
                    html += `<div style="margin-bottom: 25px; border-bottom: 2px solid #eee; padding-bottom: 15px;">
                                <h4 style="margin: 0 0 10px 0; color: #555;">Run: ${date}</h4>
                                <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 15px;">
                                    ${runHtml}
                                </div>
                             </div>`;
                }
            });
            container.innerHTML = html || '<p style="color: #999;">Keine passenden Benchmarks für diesen Filter gefunden.</p>';
        }

        async function loadModelAnalysis() {
            const stats = await eel.get_model_analysis()();
            const coverReport = await eel.get_cover_extraction_report()();

            // 1. Category Distribution
            const catContent = document.getElementById('cat-dist-content');
            if (catContent && stats.categories) {
                let html = '<div style="display: flex; flex-direction: column; gap: 8px; margin-top: 15px;">';
                const total = stats.total_count || 1;
                for (const [cat, count] of Object.entries(stats.categories)) {
                    const percent = (count / total * 100).toFixed(1);
                    html += `<div>
                        <div style="display: flex; justify-content: space-between; font-size: 0.85em; margin-bottom: 4px;">
                            <span>${cat}</span>
                            <span>${count} (${percent}%)</span>
                        </div>
                        <div style="width: 100%; height: 8px; background: #eee; border-radius: 4px; overflow: hidden;">
                            <div style="width: ${percent}%; height: 100%; background: #2196f3;"></div>
                        </div>
                    </div>`;
                }
                catContent.innerHTML = html + '</div>';
            }

            // 2. Content Type Mapping
            const ctContent = document.getElementById('ct-dist-content');
            if (ctContent && stats.content_types) {
                ctContent.innerHTML = Object.entries(stats.content_types).map(([type, count]) => `
                    <div style="padding: 8px 12px; background: #f5f5f5; border-radius: 6px; border: 1px solid #e0e0e0; display: flex; align-items: center; gap: 10px;">
                        <span style="font-weight: bold; color: #555;">${type}</span>
                        <span style="background: #2196f3; color: white; padding: 2px 6px; border-radius: 4px; font-size: 0.85em;">${count}</span>
                    </div>
                `).join('');
            }

            // 3. Artwork Efficiency
            const artContent = document.getElementById('artwork-stats-content');
            if (artContent && coverReport) {
                const totalArt = coverReport.total || 1;
                const hasArtPct = (coverReport.has_artwork / totalArt * 100).toFixed(1);
                const local = coverReport.sources.local_folder;
                const cache = coverReport.sources.embedded_or_cache;
                const totalSuccess = (local + cache) || 1;
                const localPct = (local / totalSuccess * 100).toFixed(1);
                const cachePct = (cache / totalSuccess * 100).toFixed(1);

                artContent.innerHTML = `
                    <div style="display: flex; flex-direction: column; gap: 20px; margin-top: 15px;">
                        <div style="text-align: center; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                            <div style="font-size: 0.8em; color: #666;">Total Media Hits</div>
                            <div style="font-size: 1.8em; font-weight: bold; color: #4caf50;">${hasArtPct}%</div>
                            <div style="font-size: 0.85em; color: #888;">${coverReport.has_artwork} / ${coverReport.total} items</div>
                        </div>
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                            <div style="padding: 12px; border: 1px solid #eee; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75em; color: #666;">Local Folder</div>
                                <div style="font-weight: bold; color: #ff9800;">${localPct}%</div>
                            </div>
                            <div style="padding: 12px; border: 1px solid #eee; border-radius: 8px; text-align: center;">
                                <div style="font-size: 0.75em; color: #666;">Embedded/Cache</div>
                                <div style="font-weight: bold; color: #2196f3;">${cachePct}%</div>
                            </div>
                        </div>
                    </div>`;
            }

            // 4. Samples
            const samplesContent = document.getElementById('model-samples-content');
            if (samplesContent && stats.samples) {
                samplesContent.innerHTML = `
                    <table style="width: 100%; border-collapse: collapse; font-size: 0.85em; border: 1px solid #eee;">
                        <thead style="background: #f8f8f8;">
                            <tr>
                                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Category</th>
                                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Sample Name</th>
                                <th style="padding: 10px; text-align: left; border-bottom: 2px solid #ddd;">Detected Content Type</th>
                            </tr>
                        </thead>
                        <tbody>
                            ${Object.entries(stats.samples).map(([cat, sample]) => `
                                <tr style="border-bottom: 1px solid #f0f0f0;">
                                    <td style="padding: 10px;"><b>${cat}</b></td>
                                    <td style="padding: 10px; color: #555;">${sample.name}</td>
                                    <td style="padding: 10px;"><span style="padding: 2px 8px; background: #e3f2fd; color: #1565c0; border-radius: 4px;">${sample.content_type}</span></td>
                                </tr>
                            `).join('')}
                        </tbody>
                    </table>`;
            }
        }

        async function loadRoutingSuiteReport() {
            try {
                const report = await eel.get_routing_suite_report()();
                if (!report || report.error) {
                    console.error("Routing report error:", report ? report.error : "No data");
                    return;
                }

                safeText('suite-avg-score', report.avg_quality_score || "0.0");
                safeText('suite-direct-count', (report.modes && report.modes.direct) || 0);
                safeText('suite-vlc-count', (report.modes && report.modes.vlc) || 0);

                const total = report.total_items || 1;
                const incompatiblePct = (((report.incompatible_count || 0) / total) * 100).toFixed(1);
                safeText('suite-incompatible-pct', incompatiblePct + "%");

                // Top Items
                const topBody = document.getElementById('suite-top-items-body');
                if (topBody) {
                    topBody.innerHTML = (report.top_quality_items || []).map(item => `
                        <tr style="border-bottom: 1px solid #f0f0f0;">
                            <td style="padding: 8px;">${item.name}</td>
                            <td style="padding: 8px; text-align: center;"><span style="background:#e8f5e9; color:#2e7d32; padding:2px 6px; border-radius:4px; font-weight:bold;">${item.score}</span></td>
                        </tr>
                    `).join('') || '<tr><td colspan="2" style="padding:10px;text-align:center;">Keine Daten</td></tr>';
                }

                // Complex Items
                const complexBody = document.getElementById('suite-complex-items-body');
                if (complexBody) {
                    complexBody.innerHTML = (report.complex_items || []).map(item => `
                        <tr style="border-bottom: 1px solid #f9f9f9;">
                            <td style="padding: 8px;">${item.name}</td>
                            <td style="padding: 8px; text-align: center;"><span style="background:#fff3e0; color:#e65100; padding:2px 6px; border-radius:4px;">${item.mode ? item.mode.toUpperCase() : 'UNKNOWN'}</span></td>
                        </tr>
                    `).join('') || '<tr><td colspan="2" style="padding:10px;text-align:center;">Keine Daten</td></tr>';
                }
            } catch (e) {
                console.error("Failed to load routing suite report:", e);
            }
        }

        async function loadParserPerformance(containerId = 'parser-reporting-container') {
            const container = document.getElementById(containerId);
            if (!container) return;

            const stats = await eel.get_parser_stats()();
            if (!stats || !stats.averages || Object.keys(stats.averages).length === 0) {
                container.innerHTML = '<p style="color: #999;">Keine Parser-Statistiken vorhanden. Bitte Bibliothek scannen.</p>';
                return;
            }

            let html = `<div style="margin-bottom: 20px;">
                            <strong>Total Items Scanned:</strong> ${stats.total_items}
                        </div>
                        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(${containerId === 'parser-tab-perf-container' ? '180px' : '250px'}, 1fr)); gap: 15px;">`;

            const sorted = Object.entries(stats.averages).sort((a, b) => b[1] - a[1]);
            sorted.forEach(([name, time]) => {
                const color = time > 0.5 ? '#f57c00' : (time > 0.1 ? '#fbc02d' : '#388e3c');
                html += `<div style="padding: 12px; background: #fff; border: 1px solid #eee; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.03);">
                            <div style="font-weight: bold; color: #333; margin-bottom: 5px; font-size: 0.9em; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${name}</div>
                            <div style="font-size: 1.1em; font-weight: 800; color: ${color};">${time.toFixed(4)}s</div>
                            <div style="font-size: 0.7em; color: #999; margin-top: 2px;">avg. extraction time</div>
                         </div>`;
            });
            html += '</div>';

            // Add Last Results Table if in reporting tab
            if (containerId === 'parser-reporting-container' && stats.last_results && stats.last_results.length > 0) {
                html += `<h4 style="margin-top: 30px; margin-bottom: 15px; color: #555; border-bottom: 1px solid #eee; padding-bottom: 8px;">
                            Letzte Parser-Ergebnisse
                         </h4>
                         <div style="overflow-x: auto;">
                            <table style="width: 100%; border-collapse: collapse; font-size: 0.85em; text-align: left;">
                                <thead>
                                    <tr style="background: #f8f9fa; border-bottom: 2px solid #eee;">
                                        <th style="padding: 10px;">Datei</th>
                                        <th style="padding: 10px;">Titel / Artist</th>
                                        <th style="padding: 10px;">Dauer</th>
                                        <th style="padding: 10px;">Parser-Details</th>
                                    </tr>
                                </thead>
                                <tbody>`;

                stats.last_results.forEach(res => {
                    const details = Object.entries(res.parser_times).map(([n, t]) => `${n}: ${t.toFixed(3)}s`).join(', ');
                    html += `<tr style="border-bottom: 1px solid #eee;">
                                <td style="padding: 10px; color: #666; max-width: 250px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-family: monospace;">${res.filename}</td>
                                <td style="padding: 10px;">
                                    <div style="font-weight: 600;">${res.title}</div>
                                    <div style="font-size: 0.9em; color: #888;">${res.artist}</div>
                                </td>
                                <td style="padding: 10px; font-weight: bold; color: #2a7;">${res.total_time.toFixed(3)}s</td>
                                <td style="padding: 10px; color: #999; font-size: 0.8em;">${details}</td>
                            </tr>`;
                });

                html += `</tbody>
                            </table>
                         </div>`;
            }

            container.innerHTML = html;
        }

        // --- Library Folder Browser Logic ---
        async function loadLibraryFolders() {
            const list = document.getElementById('browser-folder-list');
            if (!list) return;
            const folders = await eel.get_library_folders()();
            list.innerHTML = '';
            folders.forEach(folder => {
                const div = document.createElement('div');
                div.style.padding = '12px';
                div.style.background = '#fff';
                div.style.border = '1px solid #ddd';
                div.style.borderRadius = '8px';
                div.style.cursor = 'pointer';
                div.style.display = 'flex';
                div.style.alignItems = 'center';
                div.style.gap = '10px';
                div.style.fontSize = '0.9em';
                div.style.boxShadow = '0 2px 4px rgba(0,0,0,0.02)';
                div.style.transition = 'all 0.2s';

                div.onmouseover = () => {
                    div.style.background = '#f1f8e9';
                    div.style.borderColor = '#2a7';
                };
                div.onmouseout = () => {
                    div.style.background = '#fff';
                    div.style.borderColor = '#ddd';
                };

                div.innerHTML = `<span class="icon-folder" style="color: #666;"></span> <span style="font-family: 'Fira Code', monospace; word-break: break-all; color: #333;">${folder}</span>`;
                div.onclick = () => {
                    const input = document.getElementById('fb-path-input');
                    if (input) {
                        input.value = folder;
                        fbNavigate(folder);
                        // Scroll top pane to top
                        const topPane = document.getElementById('browser-top-pane');
                        if (topPane) topPane.scrollTop = 0;
                    }
                };
                list.appendChild(div);
            });
        }



        function closeLogbookEditor() {
            const modal = document.getElementById('logbuch-editor-modal');
            if (modal) modal.style.display = 'none';
            currentLogbookEditName = null;
            currentLogbookEditFilename = null;
        }

        function getLogbookStatusIcon(status) {
            const normalized = (status || 'ACTIVE').toUpperCase();
            if (normalized === 'COMPLETED') return '<span class="icon-check" style="background-color: #2a7; width: 18px; height: 18px;"></span>';
            if (normalized === 'PLAN') return '<span class="icon-plan" style="background-color: #2980b9; width: 18px; height: 18px;"></span>';
            if (normalized === 'DOCS') return '<span class="icon-doc" style="background-color: #8e44ad; width: 18px; height: 18px;"></span>';
            if (normalized === 'BUG') return '<span class="icon-bug" style="background-color: #c0392b; width: 18px; height: 18px;"></span>';
            return '<span class="icon-dot" style="background-color: #27ae60; width: 18px; height: 18px;"></span>';
        }

        function extractLogbookMeta(markdown) {
            const getTag = (tag, fallback = '') => {
                const re = new RegExp(`<!--\\s*${tag}\\s*:\\s*([^>]+?)\\s*-->`, 'i');
                const m = (markdown || '').match(re);
                return m && m[1] ? m[1].trim() : fallback;
            };

            return {
                category: getTag('Category', 'Planung'),
                titleDe: getTag('Title_DE', ''),
                titleEn: getTag('Title_EN', ''),
                summaryDe: getTag('Summary_DE', ''),
                summaryEn: getTag('Summary_EN', ''),
                status: (getTag('Status', 'ACTIVE') || 'ACTIVE').toUpperCase(),
                date: getTag('Date', new Date().toISOString().slice(0, 10)),
                pinned: getTag('Pinned', 'false').toLowerCase() === 'true'
            };
        }

        function stripLogbookFixedTags(markdown) {
            const keys = ['Category', 'Title_DE', 'Title_EN', 'Summary_DE', 'Summary_EN', 'Status', 'Date', 'Pinned'];
            let cleaned = markdown || '';
            keys.forEach(k => {
                cleaned = cleaned.replace(new RegExp(`^\\s*<!--\\s*${k}\\s*:\\s*.*?-->\\s*\\n?`, 'gim'), '');
            });
            return cleaned.trimStart();
        }

        function buildLogbookFixedTagsBlock(meta) {
            const tags = [
                `<!-- Category: ${meta.category || 'Planung'} -->`,
                `<!-- Title_DE: ${meta.titleDe || ''} -->`,
                `<!-- Title_EN: ${meta.titleEn || ''} -->`,
                `<!-- Summary_DE: ${meta.summaryDe || ''} -->`,
                `<!-- Summary_EN: ${meta.summaryEn || ''} -->`,
                `<!-- Status: ${(meta.status || 'ACTIVE').toUpperCase()} -->`,
                `<!-- Date: ${meta.date || new Date().toISOString().slice(0, 10)} -->`
            ];
            if (meta.pinned) {
                tags.push(`<!-- Pinned: true -->`);
            }
            return tags.join('\n');
        }

        function openLogbookEditor(name, filename, content) {
            currentLogbookEditName = name;
            currentLogbookEditFilename = filename;
            const modal = document.getElementById('logbuch-editor-modal');
            if (!modal) {
                console.error("Modal 'logbuch-editor-modal' not found!");
                return;
            }
            const nameInput = document.getElementById('logbuch-editor-name');
            const contentInput = document.getElementById('logbuch-editor-content');
            const statusInput = document.getElementById('logbuch-editor-status');
            const categoryInput = document.getElementById('logbuch-editor-category');
            const titleDeInput = document.getElementById('logbuch-editor-title-de');
            const titleEnInput = document.getElementById('logbuch-editor-title-en');
            const summaryDeInput = document.getElementById('logbuch-editor-summary-de');
            const summaryEnInput = document.getElementById('logbuch-editor-summary-en');
            const dateInput = document.getElementById('logbuch-editor-date');
            const title = document.getElementById('logbuch-editor-title');

            if (name) {
                const meta = extractLogbookMeta(content || '');
                title.innerText = `${t('logbook_edit_prefix')}${name}`;
                nameInput.value = name;
                contentInput.value = stripLogbookFixedTags(content || '');
                if (statusInput) statusInput.value = meta.status;
                if (categoryInput) categoryInput.value = meta.category;
                if (titleDeInput) titleDeInput.value = meta.titleDe;
                if (titleEnInput) titleEnInput.value = meta.titleEn;
                if (summaryDeInput) summaryDeInput.value = meta.summaryDe;
                if (summaryEnInput) summaryEnInput.value = meta.summaryEn;
                if (dateInput) dateInput.value = meta.date;
                nameInput.disabled = false;
            } else {
                title.innerText = t('logbook_edit_title_new');
                nameInput.value = '';
                contentInput.value = '# Neuer Eintrag\n\n';
                if (statusInput) statusInput.value = 'ACTIVE';
                if (categoryInput) categoryInput.value = 'Planung';
                if (titleDeInput) titleDeInput.value = '';
                if (titleEnInput) titleEnInput.value = '';
                if (summaryDeInput) summaryDeInput.value = '';
                if (summaryEnInput) summaryEnInput.value = '';
                if (dateInput) dateInput.value = new Date().toISOString().slice(0, 10);
                nameInput.disabled = false;
            }

            modal.style.display = 'flex';
            modal.style.zIndex = "4000"; // Ensure it's on top
        }

        async function saveLogbookEntry() {
            const name = readValue('logbuch-editor-name').trim();
            const bodyContent = readValue('logbuch-editor-content');
            const meta = {
                category: readValue('logbuch-editor-category').trim() || 'Planung',
                titleDe: readValue('logbuch-editor-title-de').trim(),
                titleEn: readValue('logbuch-editor-title-en').trim(),
                summaryDe: readValue('logbuch-editor-summary-de').trim(),
                summaryEn: readValue('logbuch-editor-summary-en').trim(),
                status: (readValue('logbuch-editor-status') || 'ACTIVE').toUpperCase(),
                date: readValue('logbuch-editor-date').trim() || new Date().toISOString().slice(0, 10)
            };
            const content = `${buildLogbookFixedTagsBlock(meta)}\n\n${bodyContent.trimStart()}`;
            if (!name) {
                alert(t('test_name_required'));
                return;
            }

            const originalName = (currentLogbookEditFilename || '').replace(/\.md$/i, '');
            const isRename = !!currentLogbookEditFilename && originalName !== name;
            const filenameToSave = name;

            const res = await eel.save_logbook_entry(filenameToSave, content)();
            if (res.status === 'ok') {
                if (isRename) {
                    const delRes = await eel.delete_logbook_entry(currentLogbookEditFilename)();
                    if (delRes.status !== 'ok') {
                        alert((t('common_error') || 'Fehler: ') + (delRes.error || 'Alte Datei konnte nicht gelöscht werden'));
                    }
                }
                closeLogbookEditor();
                await loadLogbuchTab();
                // Refresh content if we were viewing the same file
                if (currentLogbookEditName) {
                    loadLogbuchContent(name, filenameToSave);
                }
                alert(t('logbook_saved'));
            } else {
                alert(t('logbook_error') + res.error);
            }
        }

        async function deleteLogbookEntry(filename) {
            const res = await eel.delete_logbook_entry(filename)();
            if (res.status === 'ok') {
                await loadLogbuchTab();
                // Clear content area
                safeText('logbuch-tab-title', t('logbook_welcome'));
                safeText('logbuch-tab-content', t('logbook_select_entry_text'));
                alert(t('logbook_deleted'));
            } else {
                alert(t('common_error') + res.error);
            }
        }

        async function loadLogbuchTab(retryCount) {
            retryCount = retryCount || 0;
            const list = document.getElementById('logbuch-tab-list');
            if (!list) return;
            if (retryCount === 0) list.innerHTML = `<div style="color:#999;">${t('logbook_loading_items')}</div>`;
            try {
                const entries = await eel.list_logbook_entries()();
                currentLogbuchEntries = entries || [];

                if (!currentLogbuchEntries || currentLogbuchEntries.length === 0) {
                    list.innerHTML = `<div style="color:#999;font-style:italic;">${t('logbook_no_entries_found')}</div>`;
                } else {
                    const categoryFilter = document.getElementById('logbuch-category-filter');
                    const statusFilter = document.getElementById('logbuch-status-filter');
                    if (categoryFilter) {
                        categoryFilter.innerHTML = '';
                        // Always add "All" first
                        const allOpt = document.createElement('option');
                        allOpt.value = 'Alle';
                        allOpt.text = t('logbook_category_all');
                        categoryFilter.appendChild(allOpt);

                        const catMap = new Map(); // Localized Name -> Original Categories
                        currentLogbuchEntries.forEach(e => {
                            const cat = e.category || 'Misc';
                            const catKey = `cat_${cat.toLowerCase()}`;
                            const localizedCat = t(catKey) !== catKey ? t(catKey) : cat;
                            if (!catMap.has(localizedCat)) catMap.set(localizedCat, []);
                            catMap.get(localizedCat).push(cat);
                        });

                        const sortedDisplayCats = Array.from(catMap.keys()).sort();
                        sortedDisplayCats.forEach(displayCat => {
                            const opt = document.createElement('option');
                            opt.value = displayCat; // Use localized name as filter value
                            opt.text = displayCat;
                            categoryFilter.appendChild(opt);
                        });
                    }
                    if (statusFilter) {
                        statusFilter.innerHTML = '';
                        const allStatus = document.createElement('option');
                        allStatus.value = 'ALL';
                        allStatus.text = t('logbook_status_all');
                        statusFilter.appendChild(allStatus);

                        const statuses = Array.from(new Set(currentLogbuchEntries.map(e => (e.status || 'ACTIVE').toUpperCase()))).sort();
                        statuses.forEach(status => {
                            const opt = document.createElement('option');
                            opt.value = status;
                            opt.text = status;
                            statusFilter.appendChild(opt);
                        });
                    }
                    renderLogbuchEntries(currentLogbuchEntries);
                }
            } catch (e) {
                console.error('[loadLogbuchTab] Error:', e);
                if (retryCount < 3) {
                    setTimeout(() => loadLogbuchTab(retryCount + 1), 500);
                } else {
                    list.innerHTML = `<div style="color:#f44;">${t('logbook_error_loading_list')}</div>`;
                }
            }
        }


        async function loadScanDirs() {
            const container = document.getElementById('scan-dirs-list');
            if (!container) return;
            const config = await eel.get_parser_config()();
            const dirs = config.scan_dirs || [];
            const defaultMediaDir = await eel.get_default_media_dir()();

            container.innerHTML = '';
            if (dirs.length === 0) {
                container.innerHTML = `<div style="color: #999; font-style: italic; font-size: 0.9em; padding: 10px; background: #f9f9f9; border-radius: 6px; border: 1px dashed #ddd;">${t('options_no_dirs_configured')}</div>`;
                return;
            }

            dirs.forEach(path => {
                const row = document.createElement('div');
                row.style.cssText = 'display: flex; align-items: center; justify-content: space-between; padding: 10px; background: #f9f9f9; border: 1px solid #eee; border-radius: 6px; font-size: 0.9em;';

                const pathEl = document.createElement('span');
                pathEl.style.cssText = 'font-family: monospace; color: #444; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; flex: 1; margin-right: 10px;';
                pathEl.innerText = path;

                const removeBtn = document.createElement('button');
                removeBtn.innerText = '✕';
                removeBtn.style.cssText = 'background: transparent; border: none; color: #c33; cursor: pointer; font-weight: bold; padding: 5px;';

                const isDefaultDir = path === defaultMediaDir;
                if (isDefaultDir) {
                    removeBtn.disabled = true;
                    removeBtn.style.cssText = 'background: transparent; border: none; color: #aaa; cursor: not-allowed; font-weight: bold; padding: 5px;';
                    removeBtn.title = t('options_default_dir_fixed');
                }

                removeBtn.onclick = async () => {
                    if (isDefaultDir) {
                        return;
                    }
                    const msg = t('options_remove_dir_confirm').replace('{path}', path);
                    if (confirm(msg)) {
                        const res = await eel.remove_scan_dir(path)();
                        if (res.status === 'ok') loadScanDirs();
                    }
                };

                row.appendChild(pathEl);
                row.appendChild(removeBtn);
                container.appendChild(row);
            });
        }

        async function addScanDirUI() {
            const res = await eel.add_scan_dir()();
            if (res.status === 'ok') {
                loadScanDirs();
            }
        }

        async function addDefaultScanDirUI() {
            const res = await eel.ensure_default_scan_dir()();
            if (res.status === 'ok') {
                loadScanDirs();
            }
        }

        function renderLogbuchEntries(entries) {
            const list = document.getElementById('logbuch-tab-list');
            const filter = document.getElementById('logbuch-category-filter');
            const selectedCategory = filter ? filter.value : 'Alle';
            const statusFilter = document.getElementById('logbuch-status-filter');
            const selectedStatus = statusFilter ? statusFilter.value : 'ALL';

            if (list) list.innerHTML = '';
            else return;

            // Filter entries
            const filteredEntries = entries.filter(e => {
                const cat = e.category || 'Misc';
                const catKey = `cat_${cat.toLowerCase()}`;
                const localizedCat = t(catKey) !== catKey ? t(catKey) : cat;

                if (selectedCategory !== 'Alle' && localizedCat !== selectedCategory) return false;
                if (selectedStatus !== 'ALL' && (e.status || 'ACTIVE').toUpperCase() !== selectedStatus) return false;

                return true;
            });

            // Sort: Pinned entries first, then alphanumerically by filename
            filteredEntries.sort((a, b) => {
                // Pinned entries first
                if (a.pinned && !b.pinned) return -1;
                if (!a.pinned && b.pinned) return 1;
                // Then sort alphanumerically by filename
                return (a.filename || a.name || '').localeCompare(b.filename || b.name || '', undefined, { numeric: true, sensitivity: 'base' });
            });

            // Render all entries in flat list
            filteredEntries.forEach(entry => {
                const btn = document.createElement('div');
                btn.style.cssText = 'padding: 10px 12px; background: #f5f5f5; border-radius: 6px; cursor: pointer; transition: all 0.2s; margin-bottom: 4px; position: relative; display: flex; justify-content: space-between; align-items: center;';
                const nameEl = document.createElement('span');
                nameEl.innerText = entry.name;
                nameEl.style.flex = '1';
                btn.appendChild(nameEl);
                // Add pin icon for pinned entries
                if (entry.pinned) {
                    const pinEl = document.createElement('span');
                    pinEl.className = 'icon-pin';
                    pinEl.style.cssText = 'margin-left: 8px; display: flex; align-items: center; background-color: #f1c40f; width: 14px; height: 14px;';
                    pinEl.title = 'Pinned';
                    btn.appendChild(pinEl);
                }
                const iconEl = document.createElement('span');
                iconEl.innerHTML = getLogbookStatusIcon(entry.status || 'ACTIVE');
                iconEl.style.cssText = 'margin-left: 8px; margin-right: 10px; display: flex; align-items: center;';
                iconEl.title = (entry.status || 'ACTIVE').toUpperCase();
                btn.appendChild(iconEl);
                const deleteBtn = document.createElement('button');
                deleteBtn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#c0392b" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>';
                deleteBtn.style.cssText = 'background: transparent; border: none; cursor: pointer; padding: 0; width: 24px; height: 24px; opacity: 0.3; transition: opacity 0.2s; display: flex; align-items: center; justify-content: center;';
                deleteBtn.onclick = (e) => {
                    e.stopPropagation();
                    const msg = t('logbook_delete_confirm').replace('{name}', entry.name);
                    if (confirm(msg)) {
                        deleteLogbookEntry(entry.filename);
                    }
                };
                btn.onmouseenter = () => deleteBtn.style.opacity = '1';
                btn.onmouseleave = () => deleteBtn.style.opacity = '0.3';
                btn.appendChild(deleteBtn);
                btn.onclick = async () => {
                    loadLogbuchContent(entry.name, entry.filename);
                };
                list.appendChild(btn);
            });
        }

        async function loadLogbuchContent(name, filename) {
            safeText('logbuch-tab-title', name);
            safeHtml('logbuch-tab-content', `<div style="color:#999;">${t('edit_loading')}</div>`);

            try {
                const markdown = await eel.get_logbook_entry(name)();
                if (!markdown) {
                    safeHtml('logbuch-tab-content', `<p style="color: #f44;">${t('edit_error_loading')}</p>`);
                    return;
                }
                const meta = extractLogbookMeta(markdown || '');
                const visibleBody = stripLogbookFixedTags(markdown || '');
                const tagsHtml = `
                    <div style="display:flex; flex-wrap:wrap; gap:8px; margin-bottom:14px;">
                        <span style="padding:4px 8px; border-radius:999px; background:#eef2ff; color:#334; font-size:0.8em;"><span class="icon-tag" style="width: 14px; height: 14px;"></span> ${meta.category || '-'}</span>
                        <span style="padding:4px 8px; border-radius:999px; background:#f1f5f9; color:#334; font-size:0.8em;">${getLogbookStatusIcon(meta.status)} ${(meta.status || 'ACTIVE').toUpperCase()}</span>
                    </div>
                    <div style="display: flex; gap: 8px; margin-bottom: 20px; flex-wrap: wrap;">
                        <span style="padding:4px 10px; border-radius:999px; background:#f8fafc; color:#445; font-size:0.8em; display: flex; align-items: center; gap: 6px;"><span class="icon-flag-de" style="width: 14px; height: 14px;"></span> ${meta.titleDe || '-'}</span>
                        <span style="padding:4px 10px; border-radius:999px; background:#f8fafc; color:#445; font-size:0.8em; display: flex; align-items: center; gap: 6px;"><span class="icon-flag-gb" style="width: 14px; height: 14px;"></span> ${meta.titleEn || '-'}</span>
                        <span style="padding:4px 10px; border-radius:999px; background:#f8fafc; color:#445; font-size:0.8em; display: flex; align-items: center; gap: 6px;"><span class="icon-calendar" style="width: 14px; height: 14px;"></span> ${meta.date || '-'}</span>
                    </div>
                `;
                // Use marked.js for proper markdown rendering if available, fallback to simple parsing
                let html;
                if (typeof marked !== 'undefined') {
                    marked.setOptions({
                        breaks: true,
                        gfm: true,
                        headerIds: false,
                        mangle: false
                    });
                    html = marked.parse(visibleBody);
                } else {
                    // Fallback to simple parsing
                    html = visibleBody
                        .replace(/^# (.*$)/gim, '<h1 style="margin-top:0; color: #1a1a1a; font-size: 1.5em;">$1</h1>')
                        .replace(/^## (.*$)/gim, '<h2 style="margin-top:20px; color: #333; font-size: 1.25em; border-bottom: 1px solid #eee; padding-bottom: 5px;">$1</h2>')
                        .replace(/^\- (.*$)/gim, '<li style="margin-left: 20px;">$1</li>')
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\n\n/g, '<br><br>');
                }

                // Wrap content with styling
                const styledHtml = `<div style="line-height: 1.6; color: #333;">${html}</div>`;
                const fullContent = tagsHtml + styledHtml;

                safeHtml('logbuch-tab-content', fullContent);

                // Add edit button
                const contentEl = document.getElementById('logbuch-tab-content');
                if (contentEl) {
                    const editBtn = document.createElement('button');
                    editBtn.innerText = t('edit_btn_edit');
                    editBtn.style.cssText = 'margin-top: 20px; padding: 8px 16px; background: #2a7; color: white; border: none; border-radius: 6px; cursor: pointer; font-weight: bold;';
                    editBtn.onclick = () => openLogbookEditor(name, filename, markdown);
                    contentEl.appendChild(editBtn);
                }
            } catch (e) {
                safeHtml('logbuch-tab-content', `<p style="color: #f44;">${t('edit_error_loading')} ${e}</p>`);
            }
        }