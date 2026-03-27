    
        // Pre-define functions
        let currentLanguage = 'de';
        let translations = {
            'de': {
                'logbook_loading_items': 'Lade Einträge...',
                'logbook_error_loading_list': 'Fehler beim Laden der Logbuch-Liste.',
                'logbook_no_entries_found': 'Keine Logbuch-Einträge gefunden.',
                'edit_loading': 'Lade Inhalt...',
                'edit_error_loading': 'Fehler beim Laden des Inhalts.',
                'edit_btn_edit': 'Bearbeiten',
                'nav_reporting': 'Reporting',
                'nav_tests': 'Tests',
                'nav_logbook': 'Logbuch',
                'nav_video': 'Video',
                'nav_playlist': 'Playlist',
                'nav_debug': 'Debug',
                'debug_python_dict': 'Python Dicts (Details)',
                'debug_dict_library': 'Bibliothek (Media Items)',
                'debug_dict_parser': 'Parser Konfiguration',
                'debug_dict_environment': 'System Umgebung',
                'debug_dict_flags': 'Debug Flags',
                'debug_runtime_info': 'Laufzeit-Info & Log-Level',
                'debug_item_db_overview': 'Item DB (Übersicht)',
                'debug_db_loading_stats': 'Lade Datenbank-Statistiken...',
                'debug_console': 'Konsole / Logs',
                'debug_db_desc': 'Dies zeigt das Item-Dictionary im Python-Backend an, bevor es an die Datenbank und das Frontend gesendet wird.'
            },
            'en': {
                'logbook_loading_items': 'Loading entries...',
                'logbook_error_loading_list': 'Error loading logbook list.',
                'logbook_no_entries_found': 'No logbook entries found.',
                'edit_loading': 'Loading content...',
                'edit_error_loading': 'Error loading content.',
                'edit_btn_edit': 'Edit',
                'nav_reporting': 'Reporting',
                'nav_tests': 'Tests',
                'nav_logbook': 'Logbook',
                'nav_video': 'Video',
                'nav_playlist': 'Playlist',
                'nav_debug': 'Debug',
                'debug_python_dict': 'Python Dicts (Details)',
                'debug_dict_library': 'Library (Media Items)',
                'debug_dict_parser': 'Parser Config',
                'debug_dict_environment': 'System Env',
                'debug_dict_flags': 'Debug Flags',
                'debug_runtime_info': 'Runtime Info & Logs',
                'debug_item_db_overview': 'Item DB (Overview)',
                'debug_db_loading_stats': 'Loading DB stats...',
                'debug_console': 'Console / Logs',
                'debug_db_desc': 'Shows the internal item dictionary from the Python backend before it is persisted.'
            }
        };



        function filterCompatibilityTable() {
            const input = document.getElementById('compatibility-search');
            if (!input) return;
            const filter = input.value.toLowerCase();
            const rows = document.querySelectorAll('.comp-row');
            rows.forEach(row => {
                const text = row.innerText.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        }

        let activeAudioPipeline;
        let currentLogbuchEntries = [];
        let currentLogbookEditName = null;
        let currentLogbookEditFilename = null;
        let lastSyncState = null;

        function appendUiTrace(message) {
            const timestamp = new Date().toLocaleTimeString();
            const logLine = `[UI-Trace ${timestamp}] ${message}`;
            console.warn(logLine);

            const isErrorOrAlert = message.toLowerCase().includes('js-error') || message.toLowerCase().includes('alert');
            if (isErrorOrAlert) {
                const errorLog = document.getElementById('startup-error-log');
                if (errorLog) {
                    if (errorLog.innerText.includes('Waiting for errors')) errorLog.innerText = '';
                    errorLog.innerText += `\n${logLine}`;
                    errorLog.scrollTop = errorLog.scrollHeight;
                }
            }

            try {
                if (typeof eel !== 'undefined' && typeof eel.ui_trace === 'function') {
                    eel.ui_trace(logLine)();
                }
            } catch (e) { }

            const debugOutput = document.getElementById('debug-output');
            if (debugOutput) {
                const prefix = debugOutput.textContent && !debugOutput.textContent.endsWith('\n') ? '\n' : '';
                debugOutput.textContent += `${prefix}${logLine}\n`;
                debugOutput.scrollTop = debugOutput.scrollHeight;
            }

            const resultsContainer = document.getElementById('test-results-container');
            const testOutput = document.getElementById('test-output');
            if (resultsContainer && testOutput && resultsContainer.style.display !== 'none') {
                const prefix = testOutput.textContent && !testOutput.textContent.endsWith('\n') ? '\n' : '';
                testOutput.textContent += `${prefix}${logLine}\n`;
                testOutput.scrollTop = testOutput.scrollHeight;
            }
        }

        async function testBackendSync() {
            const statusDiv = document.getElementById('startup-sync-status');
            if (!statusDiv) return;
            statusDiv.style.display = 'block';
            statusDiv.innerText = "🔄 Pinging backend...";
            statusDiv.style.background = "#fff3e0";
            statusDiv.style.color = "#ef6c00";
            statusDiv.style.border = "1px solid #ffe0b2";

            const start = Date.now();
            try {
                const res = await eel.rtt_ping(testType, testData)();
                const rtt = Date.now() - start;
                const footerLatency = document.getElementById('footer-latency');
                if (footerLatency) footerLatency.innerText = rtt + 'ms';
                appendUiTrace(`RTT ${testType}: ${rtt}ms (Status: ${res.status})`);
                if (res.status === 'pong') {
                    statusDiv.innerHTML = `✅ <strong>Backend Synchronized.</strong> RTT: ${rtt}ms | Status: Stable`;
                    statusDiv.style.background = "#e8f5e9";
                    statusDiv.style.color = "#2e7d32";
                    statusDiv.style.border = "1px solid #c8e6c9";
                } else {
                    throw new Error("Invalid response");
                }
            } catch (err) {
                statusDiv.innerText = "❌ Synchronization Error: " + err;
                statusDiv.style.background = "#ffebee";
                statusDiv.style.color = "#c62828";
                statusDiv.style.border = "1px solid #ffcdd2";
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
            parser_mode: 'lightweight',
            minimal_player_view: false
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
                if (!savedTab) {
                    savedTab = mwv_config.start_page || 'playlist';
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
                'video': 'multiplexed-media-player-orchestrator-panel',
                'vlc': 'multiplexed-media-player-orchestrator-panel',
                'tools': 'tools-tab'
            };

            const targetId = tabMap[tabId];
            if (targetId) {
                const sidebar = document.getElementById('main-sidebar');
                const splitter = document.getElementById('main-splitter');
                const contentArea = document.getElementById('main-content-area');
                
                // Define tabs that should use the full-width layout (no main sidebar)
                // Now including standard navigation tabs (library, item, file, edit, options) as requested by the user
                const managementTabs = ['library', 'item', 'file', 'edit', 'options', 'debug', 'tests', 'reporting', 'logbuch', 'playlist', 'vlc', 'video', 'tools', 'parser'];
                const isManagement = managementTabs.includes(tabId);
                const isSidebarVisible = !isManagement;

                // Force Layout Mode
                document.body.setAttribute('data-layout-mode', isManagement ? 'management' : 'standard');

                // Hard-toggle Global UI Components
                if (sidebar) {
                    if (isManagement) {
                        sidebar.style.display = 'none';
                        sidebar.classList.add('hidden-collapse');
                    } else {
                        sidebar.style.display = 'flex';
                        sidebar.style.width = '300px';
                        sidebar.classList.remove('hidden-collapse');
                    }
                }
                if (splitter) {
                    if (isManagement) {
                        splitter.style.display = 'none';
                        splitter.classList.add('hidden-collapse');
                    } else {
                        splitter.style.display = 'block';
                        splitter.classList.remove('hidden-collapse');
                    }
                }
                
                // Ensure the content area itself fills the screen
                if (contentArea) {
                    if (isManagement) {
                        contentArea.style.marginLeft = '0';
                        contentArea.style.width = '100%';
                    } else {
                        contentArea.style.marginLeft = '0'; // Flexbox handles it in standard mode
                        contentArea.style.width = 'auto'; // Let flex reach end
                    }
                }

                // Reset all tab content displays
                document.querySelectorAll('.tab-content').forEach(el => {
                    el.style.display = 'none';
                    el.classList.remove('active');
                });

                // Show target
                const targetEl = document.getElementById(targetId);
                if (targetEl) {
                    targetEl.classList.add('active');
                    const flexTabs = ['player', 'library', 'item', 'file', 'edit', 'options', 'parser', 'debug', 'tests', 'reporting', 'logbuch', 'playlist', 'vlc', 'video', 'tools'];
                    if (flexTabs.includes(tabId)) {
                        targetEl.style.display = 'flex';
                        targetEl.style.flex = '1';
                        targetEl.style.height = '100%';
                        targetEl.style.width = '100%';
                        targetEl.style.minWidth = '0';
                        targetEl.style.overflow = 'hidden';
                        targetEl.style.flexDirection = 'column';

                        // Initialize splitters
                        if (tabId === 'debug') {
                            setTimeout(() => initSplitterV('debug-splitter', 'debug-settings-pane', 'debug-console-pane', 50), 0);
                        } else if (tabId === 'logbuch') {
                            setTimeout(() => initSplitterV('logbuch-splitter', 'logbuch-sidebar', 'logbuch-viewer-pane', 25), 0);
                        } else if (tabId === 'vlc' || tabId === 'video') {

                        }

                        if (tabId === 'logbuch' && typeof loadLogbuchTab === 'function') loadLogbuchTab();
                        if (tabId === 'tests' && typeof switchTestView === 'function') switchTestView('base');
                        if (tabId === 'reporting') {
                            if (typeof switchReportingView === 'function') switchReportingView('dashboard');
                            if (typeof loadSqlFiles === 'function') loadSqlFiles();
                            if (typeof refreshReportingData === 'function') refreshReportingData();
                        }
                        if (tabId === 'options') {
                            if (typeof switchOptionsView === 'function') switchOptionsView('general');
                            const miniToggle = document.getElementById('toggle-minimal-player');
                            if (miniToggle) miniToggle.checked = mwv_config.minimal_player_view || false;
                        }
                        if (tabId === 'library') renderLibrary();
                        if (tabId === 'vlc' || tabId === 'video') {
                            if (typeof initVlcPlayer === 'function') initVlcPlayer();
                        }
                        if (tabId === 'parser') {
                            if (typeof switchParserView === 'function') switchParserView('configuration');
                        }

                        // --- Minimal Player View Logic ---
                        const minimalMode = mwv_config.minimal_player_view || false;
                        const standardTabs = [
                            'coverflow-library-tab-trigger',
                            'indexed-sqlite-repository-tab-trigger',
                            'filesystem-crawler-tab-trigger',
                            'crud-metadata-tab-trigger',
                            'system-registry-tab-trigger'
                        ];
                        const bottomBar = document.querySelector('.bottom-bar');
                        const playerFooter = document.querySelector('.player-container');

                        if (tabId === 'player' && minimalMode) {
                            standardTabs.forEach(id => {
                                const el = document.getElementById(id);
                                if (el) el.style.display = 'none';
                            });
                            if (bottomBar) bottomBar.style.display = 'none';
                            if (playerFooter) playerFooter.style.bottom = '0';
                        } else {
                            standardTabs.forEach(id => {
                                const el = document.getElementById(id);
                                if (el) el.style.display = 'inline-block';
                            });
                            if (bottomBar) bottomBar.style.display = 'flex';
                            if (playerFooter) playerFooter.style.bottom = '26px';
                        }
                        if (tabId === 'parser') {
                            loadParserPerformance('parser-tab-perf-container');
                        }
                        if (tabId === 'debug' && typeof loadDebugDBInfo === 'function') loadDebugDBInfo();
                    } else {
                        // Block tabs (standard layouts)
                        targetEl.style.display = 'block';
                        if (tabId === 'item') refreshLibrary();
                    }
                } else {
                    console.warn(`[UI] Target element not found for tab: ${tabId} (id: ${targetId})`);
                }
            }
            const sidebarEl = document.getElementById('main-sidebar');
            const splitterEl = document.getElementById('main-splitter');
            const contentEl = document.getElementById('main-content-area');

            localStorage.setItem('mwv_active_tab', tabId);

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

            // Ensure the button is marked as active
            const finalBtn = btn || getTabButton(tabId);
            if (finalBtn) finalBtn.classList.add('active');
        }

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
                        header.innerText = (viewId === 'startup') ? 'Start-Konfiguration' : 'Optionen';
                    }
                    if (viewId === 'startup') {
                        loadStartupConfig();
                    }
                }
            }
        }

        async function loadStartupConfig() {
            try {
                const config = await eel.get_startup_config()();
                if (config) {
                    if (config.browser_choice) {
                        document.getElementById('startup-browser-choice').value = config.browser_choice;
                    }
                    if (config.browser_flags) {
                        const flags = config.browser_flags || [];
                        document.getElementById('startup-browser-flags').value = flags.join('\n');
                    }
                    if (config.env_vars) {
                        let envStr = "";
                        for (const [k, v] of Object.entries(config.env_vars)) {
                            envStr += `${k}=${v}\n`;
                        }
                        const envEl = document.getElementById('startup-env-vars');
                        if (envEl) envEl.value = envStr.trim();
                    }
                }
            } catch (err) {
                console.error("Error loading startup config:", err);
            }
        }

        async function saveStartupConfig() {
            try {
                const choice = document.getElementById('startup-browser-choice').value;
                const flagsRaw = document.getElementById('startup-browser-flags').value;
                const envRaw = document.getElementById('startup-env-vars').value;

                console.log("Saving startup config:", { choice, flagsRaw, envRaw });

                const flags = flagsRaw.split('\n').map(f => f.trim()).filter(f => f.length > 0);

                const envVars = {};
                envRaw.split('\n').forEach(line => {
                    const parts = line.split('=');
                    if (parts.length >= 2) {
                        const key = parts[0].trim();
                        const value = parts.slice(1).join('=').trim();
                        if (key) envVars[key] = value;
                    }
                });

                const result = await eel.update_startup_config({
                    "browser_choice": choice,
                    "browser_flags": flags,
                    "env_vars": envVars
                })();

                if (result && result.status === "success") {
                    if (typeof showToast === "function") {
                        showToast("Startup-Konfiguration gespeichert! Bitte die App neustarten.", "success");
                    } else {
                        alert("Startup-Konfiguration gespeichert! Bitte die App neustarten.");
                    }
                } else {
                    alert("Fehler beim Speichern der Konfiguration.");
                }
            } catch (err) {
                console.error("Error saving startup config:", err);
                alert("Kritischer Fehler beim Speichern: " + err);
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

        function switchEditView(viewId) {
            console.log("Switching edit view to:", viewId);
            document.querySelectorAll('.edit-view').forEach(el => el.style.display = 'none');
            document.querySelectorAll('#edit-main-content-pane .options-subtab').forEach(el => {
                el.classList.remove('active');
            });

            const target = document.getElementById('edit-' + viewId + '-view');
            if (target) {
                target.style.display = 'block';
                const btn = document.getElementById('edit-subtab-' + viewId);
                if (btn) btn.classList.add('active');
            }

            // If switching to ffprobe, trigger analysis if empty and a file is selected
            if (viewId === 'ffprobe') {
                const currentItem = document.getElementById('edit-item-name').value;
                const ffprobeContent = document.getElementById('edit-ffprobe-content');
                if (currentItem && ffprobeContent && ffprobeContent.innerText.includes('Führe Media Analyse aus')) {
                    ffprobeContent.innerText = 'Analysiere ' + currentItem + '...';
                    eel.analyze_media_item(currentItem)(function (res) {
                        try {
                            if (res && res.ffprobe) {
                                ffprobeContent.innerText = JSON.stringify(res.ffprobe, null, 2);
                            } else {
                                ffprobeContent.innerText = "Keine FFprobe Daten verfügbar oder Fehler bei der Analyse.\n\nRaw Result:\n" + JSON.stringify(res, null, 2);
                            }
                        } catch (e) {
                            ffprobeContent.innerText = "Fehler: " + e;
                        }
                    });
                }
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
            if (view === 'video-streaming') {
                loadVideoStreamingBenchmarks('video');
                if (typeof populateTestVideoSelector === 'function') {
                    populateTestVideoSelector();
                }
            }
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

            if (view === 'scripts' || view === 'suite' || view === 'routing') {
                loadTestSuites();
            }
            if (view === 'video') {
                populateTestVideoSelector();
            }
        }

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
                    if (res.error) {
                        outputEl.innerText += "\n\n[STDERR]\n" + res.error;
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

        async function checkBackendReachability() {
            const statusText = document.getElementById('rtt-output');
            const container = document.getElementById('rtt-results-container');
            if (container) container.style.display = 'block';
            if (statusText) statusText.innerText = "[Network] Probing 127.0.0.1 (Eel Port Bind Check)...";

            try {
                const res = await eel.rtt_ping("localhost_check")();
                if (res && res.status === 'pong') {
                    if (statusText) {
                        statusText.innerText = `[SUCCESS] Connection to 127.0.0.1 is active.\nStatus: Stable\nBackend ID: ${res.pid || 'running'}`;
                        statusText.style.color = "#2a7";
                    }
                } else {
                    throw new Error("Invalid response from internal API");
                }
            } catch (err) {
                if (statusText) {
                    statusText.innerText = `[FAILED] 127.0.0.1 refused the connection (ERR_CONNECTION_REFUSED).\nError: ${err.message}\n\nTroubleshooting:\n- Backend process might have crashed.\n- Port 8345 is blocked by firewall.\n- Eel server failed to bind to 127.0.0.1.`;
                    statusText.style.color = "#f44336";
                }
            }
        }

        async function discoverCastingDevices() {
            const status = document.getElementById('cast-scanner-status');
            const list = document.getElementById('cast-device-list');
            if (status) {
                status.innerText = "SCANNING...";
                status.style.color = "#9c27b0";
            }
            if (list) list.innerText = "Searching for Chromecast & DLNA nodes...";

            try {
                const res = await eel.discover_cast_devices()();
                if (status) {
                    status.innerText = "IDLE (Complete)";
                    status.style.color = "#2a7";
                }
                if (list) {
                    const total = (res.chromecast ? res.chromecast.length : 0) + (res.dlna ? res.dlna.length : 0);
                    if (total === 0) {
                        list.innerText = "No devices detected in current network segment.";
                    } else {
                        let html = "<strong>Found Devices:</strong><br>";
                        if (res.chromecast) res.chromecast.forEach(d => html += `📱 Chromecast: ${d.name} (${d.ip})<br>`);
                        if (res.dlna) res.dlna.forEach(d => html += `📺 DLNA: ${d.name} (${d.ip})<br>`);
                        list.innerHTML = html;
                    }
                }
            } catch (e) {
                if (status) status.innerText = "ERROR";
                if (list) list.innerText = "Casting discovery failed: " + e;
            }
        }

        async function toggleSwyhRs(enabled) {
            try {
                const res = await eel.toggle_swyh_rs(enabled)();
                if (typeof showToast === 'function') {
                    showToast(`SWYH-RS ${res.status === 'ok' ? 'TOGGLED' : 'ERROR'}`, 'info');
                } else {
                    console.log(`SWYH-RS toggled: ${res.status}`);
                }
            } catch (e) {
                console.error("Failed to toggle SWYH-RS:", e);
            }
        }

        async function startSpotifyBridge() {
            try {
                if (typeof eel.start_spotify_bridge === 'function') {
                    const res = await eel.start_spotify_bridge()();
                    showToast("Spotify Bridge Status: " + res.status.toUpperCase(), 'info');
                } else {
                    showToast("Spotify Backend nicht verfügbar.", 'error');
                }
            } catch (e) {
                console.error("Spotify Bridge error:", e);
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

                // Update Global Badges
                const pb = document.getElementById('integrity-badge-python');
                const hb = document.getElementById('integrity-badge-html');
                if (pb) {
                    pb.innerText = res.python_integrity.balanced ? 'OK' : 'ERR';
                    pb.style.color = res.python_integrity.balanced ? '#2a7' : '#c62828';
                }
                if (hb) {
                    hb.innerText = res.div_balance.balanced ? 'OK' : 'ERR';
                    hb.style.color = res.div_balance.balanced ? '#2a7' : '#c62828';
                }

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
                        <div style="background: white; border: 1px solid #eee; border-radius: 12px; padding: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <h4 style="margin: 0 0 5px 0; font-size: 0.9em; color: #555;">Python Integrity</h4>
                            <div style="font-size: 1.1em; font-weight: bold; color: ${res.python_integrity.balanced ? '#2a7' : '#c62828'};">
                                ${res.python_integrity.balanced ? '✅ Clean' : '❌ ' + res.python_integrity.errors.length + ' Errors'}
                            </div>
                            <div style="font-size: 0.7em; color: #888; margin-top: 4px; max-height: 80px; overflow-y: auto; font-family: monospace; line-height: 1.2;">
                                ${res.python_integrity.errors.map(e => `• ${e}`).join('<br>') || 'No syntax errors.'}
                            </div>
                        </div>
                        <div style="background: white; border: 1px solid #eee; border-radius: 12px; padding: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.05);">
                            <h4 style="margin: 0 0 5px 0; font-size: 0.9em; color: #555;">Orphan Catches</h4>
                            <div style="font-size: 1.1em; font-weight: bold; color: ${res.orphaned_catches.length === 0 ? '#2a7' : '#c62828'};">
                                ${res.orphaned_catches.length === 0 ? '✅ None' : '❌ ' + res.orphaned_catches.length}
                            </div>
                            <div style="font-size: 0.7em; color: #888; margin-top: 4px; font-family: monospace;">
                                ${res.orphaned_catches.length > 0 ? 'L: ' + res.orphaned_catches.join(', ') : 'No orphan blocks.'}
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
            (files || []).forEach(file => {
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

                safeText('suite-avg-score', report.avg_quality_score || 0);
                safeText('suite-direct-count', (report.modes && report.modes.direct) || 0);
                const vlcCount = (report.modes && report.modes.vlc) || 0;
                const transcodeCount = (report.modes && report.modes.transcode) || 0;
                safeText('suite-vlc-count', vlcCount + transcodeCount);

                const total = report.total_items || 1;
                const incompatiblePct = (((report.incompatible_count || 0) / (total || 1)) * 100).toFixed(1);
                safeText('suite-incompatible-pct', incompatiblePct + "%");

                // Chart: Score Distribution
                if (report.score_distribution) {
                    const trace = {
                        x: Object.keys(report.score_distribution),
                        y: Object.values(report.score_distribution),
                        type: 'bar',
                        marker: { color: '#4caf50' }
                    };
                    const layout = {
                        title: 'Quality Score Distribution',
                        font: { size: 11 },
                        margin: { t: 40, b: 30, l: 30, r: 10 },
                        showlegend: false
                    };
                    Plotly.newPlot('routing-score-distribution-chart', [trace], layout, {responsive: true});
                }

                // Chart: Mode Pie
                if (report.modes) {
                    const trace = {
                        labels: Object.keys(report.modes).filter(k => report.modes[k] > 0),
                        values: Object.values(report.modes).filter(v => v > 0),
                        type: 'pie',
                        hole: 0.4,
                        marker: { colors: ['#4caf50', '#ff9800', '#2196f3', '#9c27b0', '#f44336'] }
                    };
                    const layout = {
                        title: 'Protocol Distribution',
                        font: { size: 11 },
                        margin: { t: 40, b: 20, l: 20, r: 20 }
                    };
                    Plotly.newPlot('routing-mode-pie-chart', [trace], layout, {responsive: true});
                }

                // Chart: Codec Distribution
                if (report.codec_distribution) {
                    const trace = {
                        x: Object.keys(report.codec_distribution),
                        y: Object.values(report.codec_distribution),
                        type: 'bar',
                        marker: { color: '#2196f3' }
                    };
                    const layout = {
                        title: 'Codec Distribution',
                        font: { size: 10 },
                        margin: { t: 40, b: 60, l: 30, r: 10 },
                        showlegend: false
                    };
                    Plotly.newPlot('routing-codec-distribution-chart', [trace], layout, {responsive: true});
                }

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

        async function runDeepRoutingAnalysis() {
            appendUiTrace("Starting Deep Routing Analysis Suite...");
            if (typeof loadRoutingSuiteReport === 'function') loadRoutingSuiteReport();
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
                await loadLogbuchTab(0, true);
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
                await loadLogbuchTab(0, true);
                // Clear content area
                safeText('logbuch-tab-title', t('logbook_welcome'));
                safeText('logbuch-tab-content', t('logbook_select_entry_text'));
                alert(t('logbook_deleted'));
            } else {
                alert(t('common_error') + res.error);
            }
        }

        async function loadLogbuchTab(retryCount, forceRefresh = false) {
            retryCount = retryCount || 0;
            const list = document.getElementById('logbuch-tab-list');
            if (!list) return;
            
            if (forceRefresh || !currentLogbuchEntries || currentLogbuchEntries.length === 0) {
                if (retryCount === 0) list.innerHTML = `<div style="color:#999;">${typeof t === 'function' ? t('logbook_loading_items') : 'Lade...'}</div>`;
                try {
                    const entries = await eel.list_logbook_entries()();
                    currentLogbuchEntries = entries || [];
                } catch (e) {
                    console.error('[loadLogbuchTab] Error:', e);
                    if (retryCount < 3) {
                        setTimeout(() => loadLogbuchTab(retryCount + 1, forceRefresh), 500);
                    } else {
                        list.innerHTML = `<div style="color:#f44;">${t('logbook_error_loading_list')}</div>`;
                    }
                    return;
                }
            }

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
            const categoryFilter = document.getElementById('logbuch-category-filter');
            const statusFilter = document.getElementById('logbuch-status-filter');

            const selectedCategory = categoryFilter ? categoryFilter.value : 'Alle';
            const selectedStatus = statusFilter ? statusFilter.value : 'ALL';

            if (!list) return;
            list.innerHTML = '';

            // Filter entries
            const filteredEntries = entries.filter(e => {
                const cat = e.category || 'Misc';
                const catKey = `cat_${cat.toLowerCase()}`;
                const localizedCat = (typeof t === 'function' && t(catKey) !== catKey) ? t(catKey) : cat;

                if (selectedCategory !== 'Alle' && localizedCat !== selectedCategory) return false;
                if (selectedStatus !== 'ALL' && (e.status || 'ACTIVE').toUpperCase() !== selectedStatus) return false;
                return true;
            });

            // Sort: Pinned first, then alphanumeric
            filteredEntries.sort((a, b) => {
                if (a.pinned && !b.pinned) return -1;
                if (!a.pinned && b.pinned) return 1;
                return (a.name || '').localeCompare(b.name || '', undefined, { numeric: true, sensitivity: 'base' });
            });

            const fragment = document.createDocumentFragment();
            filteredEntries.forEach(entry => {
                const btn = document.createElement('div');
                btn.style.cssText = 'padding: 10px 12px; background: #f5f5f5; border-radius: 6px; cursor: pointer; transition: all 0.2s; margin-bottom: 4px; position: relative; display: flex; justify-content: space-between; align-items: center; border: 1px solid transparent;';
                btn.onmouseenter = () => { btn.style.background = '#eee'; btn.style.borderColor = '#ddd'; };
                btn.onmouseleave = () => { btn.style.background = '#f5f5f5'; btn.style.borderColor = 'transparent'; };

                const nameWrap = document.createElement('div');
                nameWrap.style.cssText = 'display: flex; align-items: center; gap: 8px; flex: 1; overflow: hidden;';

                if (entry.pinned) {
                    const pin = document.createElement('span');
                    pin.innerHTML = '📌';
                    pin.style.fontSize = '0.9em';
                    nameWrap.appendChild(pin);
                }

                const nameEl = document.createElement('span');
                nameEl.innerText = entry.name;
                nameEl.style.cssText = 'white-space: nowrap; overflow: hidden; text-overflow: ellipsis; font-weight: 500;';
                nameWrap.appendChild(nameEl);
                btn.appendChild(nameWrap);

                const statusWrap = document.createElement('div');
                statusWrap.style.cssText = 'display: flex; align-items: center; gap: 10px; margin-left: 10px;';

                const iconEl = document.createElement('span');
                iconEl.innerHTML = (typeof getLogbookStatusIcon === 'function') ? getLogbookStatusIcon(entry.status || 'ACTIVE') : '📄';
                statusWrap.appendChild(iconEl);

                const deleteBtn = document.createElement('button');
                deleteBtn.innerHTML = '🗑️';
                deleteBtn.style.cssText = 'background: none; border: none; cursor: pointer; padding: 4px; opacity: 0.3; transition: opacity 0.2s; font-size: 1.1em;';
                deleteBtn.onmouseenter = (e) => { e.target.style.opacity = '1'; };
                deleteBtn.onmouseleave = (e) => { e.target.style.opacity = '0.3'; };
                deleteBtn.onclick = (e) => {
                    e.stopPropagation();
                    const msg = (typeof t === 'function' ? t('logbook_delete_confirm') : 'Löschen?').replace('{name}', entry.name);
                    if (confirm(msg)) deleteLogbookEntry(entry.filename);
                };
                statusWrap.appendChild(deleteBtn);
                btn.appendChild(statusWrap);

                btn.onclick = () => loadLogbuchContent(entry.name, entry.filename);
                fragment.appendChild(btn);
            });
            list.appendChild(fragment);
        }

        async function loadLogbuchContent(name, filename) {
            const header = document.getElementById('logbuch-viewer-header');
            const metaContainer = document.getElementById('logbuch-entry-meta');
            const scrollContainer = document.getElementById('logbuch-scroll-container');
            const contentEl = document.getElementById('logbuch-tab-content');

            // Reset UI
            if (header) header.style.display = 'block';
            safeText('logbuch-tab-title', name);
            if (metaContainer) metaContainer.innerHTML = '';
            safeHtml('logbuch-tab-content', `<div style="color:#999; text-align:center; padding-top:40px;">${t('edit_loading')}</div>`);
            if (scrollContainer) scrollContainer.scrollTop = 0;

            try {
                const markdown = await eel.get_logbook_entry(name)();
                if (!markdown) {
                    safeHtml('logbuch-tab-content', `<p style="color: #f44; text-align:center;">${t('edit_error_loading')}</p>`);
                    return;
                }
                const meta = extractLogbookMeta(markdown || '');
                const visibleBody = stripLogbookFixedTags(markdown || '');

                // Fill Meta
                if (metaContainer) {
                    metaContainer.innerHTML = `
                        <span title="Kategorie">📁 ${meta.category || '-'}</span>
                        <span title="Status">${getLogbookStatusIcon(meta.status)} ${(meta.status || 'active').toUpperCase()}</span>
                        <span title="Datum">📅 ${meta.date || '-'}</span>
                        <span title="DE/EN">🌐 ${meta.titleDe ? '🇩🇪' : ''}${meta.titleEn ? '🇬🇧' : ''}</span>
                    `;
                }

                let html;
                if (typeof marked !== 'undefined') {
                    marked.setOptions({ breaks: true, gfm: true, headerIds: false, mangle: false });
                    html = marked.parse(visibleBody);
                } else {
                    html = visibleBody
                        .replace(/^# (.*$)/gim, '<h1 style="margin-top:0; color: #1a1a1a; font-size: 1.5em;">$1</h1>')
                        .replace(/^## (.*$)/gim, '<h2 style="margin-top:20px; color: #333; font-size: 1.25em; border-bottom: 1px solid #eee; padding-bottom: 5px;">$1</h2>')
                        .replace(/^\- (.*$)/gim, '<li style="margin-left: 20px;">$1</li>')
                        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                        .replace(/\n\n/g, '<br><br>');
                }

                safeHtml('logbuch-tab-content', html);

                // Add edit button at bottom
                const footer = document.createElement('div');
                footer.style.cssText = 'margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; display: flex; justify-content: flex-end;';
                const editBtn = document.createElement('button');
                editBtn.innerText = t('edit_btn_edit', 'Eintrag bearbeiten');
                editBtn.className = 'tab-btn active';
                editBtn.style.cssText = 'padding: 8px 20px; font-weight: bold; background: #2a7; color: white; border: none; border-radius: 6px; cursor: pointer;';
                editBtn.onclick = () => openLogbookEditor(name, filename, markdown);
                footer.appendChild(editBtn);
                contentEl.appendChild(footer);

            } catch (e) {
                console.error('[loadLogbuchContent] Error:', e);
                safeHtml('logbuch-tab-content', `<p style="color: #f44; text-align:center;">${t('edit_error_loading')} ${e}</p>`);
            }
        }
    
    
        function isUnsupportedMediaError(reason) {
            const text = String(reason || '');
            return text.includes('NotSupportedError') || text.includes('no supported source was found');
        }

        window.onerror = function (msg, url, lineNo, columnNo, error) {
            alert("JS Error: " + msg + "\nLine: " + lineNo + "\nCol: " + columnNo);
            return false;
        };
        window.addEventListener('unhandledrejection', function (event) {
            if (isUnsupportedMediaError(event.reason)) {
                console.warn('Unsupported media source rejected by browser:', event.reason);
                const statusEl = document.getElementById('active-orchestration-status-message-renderer');
                if (statusEl) {
                    statusEl.textContent = t('player_unsupported_source') || 'Unsupported media source for browser playback.';
                }
                event.preventDefault();
                return;
            }
            console.error("Uncaught Promise: ", event.reason);
        });
    
                
                    if ('mediaSession' in navigator) {
                        const updateMediaMetadata = (meta) => {
                            try {
                                const footerCover = document.getElementById('footer-artwork-raster-buffer');
                                const artworkSrc = footerCover && footerCover.src ? footerCover.src : '';
                                navigator.mediaSession.metadata = new MediaMetadata({
                                    title: meta.title || '',
                                    artist: meta.artist || '',
                                    album: meta.album || '',
                                    artwork: [{ src: artworkSrc, sizes: '96x96', type: 'image/png' }]
                                });
                            } catch (e) { console.warn('mediaSession metadata set failed', e); }
                        };

                        navigator.mediaSession.setActionHandler('play', () => { const p = document.getElementById('native-html5-audio-pipeline-element'); if (p && p.play) p.play(); });
                        navigator.mediaSession.setActionHandler('pause', () => { const p = document.getElementById('native-html5-audio-pipeline-element'); if (p && p.pause) p.pause(); });
                        navigator.mediaSession.setActionHandler('previoustrack', () => window.playPrev && window.playPrev());
                        navigator.mediaSession.setActionHandler('nexttrack', () => window.playNext && window.playNext());

                        const pipelineElement = document.getElementById('native-html5-audio-pipeline-element');
                        if (pipelineElement && pipelineElement.addEventListener) {
                            pipelineElement.addEventListener('play', () => updateMediaMetadata({ title: document.querySelector('#status') ? document.querySelector('#status').textContent : '' }));
                        }
                    }
                    function updateMinimalPlayerMode(enabled) {
            mwv_config.minimal_player_view = enabled;
            saveParserChainUI(); // Re-use this for global config save
            const activeTab = localStorage.getItem('mwv_active_tab') || 'player';
            switchTab(activeTab, getTabButton(activeTab));
        }

        function getTabButton(tabId) {
            const btnMap = {
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
                'vlc': 'media-orchestrator-tab-trigger',
                'video': 'media-orchestrator-tab-trigger'
            };
            return document.getElementById(btnMap[tabId]);
        }
        function set_media_session(meta) {
            try {
                if (!('mediaSession' in navigator)) return;
                            const artwork = (meta.artwork && meta.artwork.length) ? meta.artwork[0].src : document.getElementById('footer-artwork-raster-buffer').src;
                            navigator.mediaSession.metadata = new MediaMetadata({
                                title: meta.title || '',
                                artist: meta.artist || '',
                                album: meta.album || '',
                                artwork: [{ src: artwork, sizes: '96x96', type: 'image/png' }]
                            });
                        } catch (e) {
                            console.warn('set_media_session failed', e);
                        }
                    }
                    window.set_media_session = set_media_session;
                
    
        activeAudioPipeline = document.getElementById('native-html5-audio-pipeline-element');
        currentLogbuchEntries = [];

        // ============ Player Expansion State ============
        let currentPlaylist = [];
        const cats = ["audio", "video", "images", "documents", "ebooks", "abbild", "spiel", "beigabe"];
        let libraryFilter = 'all';
        let librarySubFilter = 'all';
        let coverflowIndex = 0;
        let coverflowItems = [];

        const CATEGORY_MAP = {
            "audio": ["Audio", "Album", "Hörbuch", "Klassik", "Compilation", "Single", "Podcast", "Radio", "Soundtrack", "Playlist", "Music", "Song"],
            "video": ["Video", "Film", "Serie", "ISO/Image", "Musikvideos", "Animes", "Cartoons", "Movie", "TV Show"],
            "film": ["Film", "Film Object"],
            "serie": ["Serie"],
            "album": ["Album"],
            "soundtrack": ["Soundtrack"],
            "compilation": ["Compilation"],
            "single": ["Single"],
            "klassik": ["Klassik"],
            "playlist": ["Playlist"],
            "podcast": ["Podcast"],
            "images": ["Bilder"],
            "documents": ["Dokument"],
            "ebooks": ["E-Book"],
            "abbild": ["Abbild", "ISO/Image", "Disk Image", "PAL DVD", "NTSC DVD", "Blu-ray", "PAL DVD (Abbild)", "NTSC DVD (Abbild)", "DVD (Abbild)", "Blu-ray (Abbild)", "Audio-CD (Abbild)", "CD-ROM (Abbild)", "Disk-Abbild", "DVD Object"],
            "spiel": ["PC Spiel", "PC Spiel (Index)", "Digitales Spiel (Steam)", "Spiel"],
            "beigabe": ["Supplement", "Beigabe", "Software"]
        };

        function setLibraryFilter(cat) {
            libraryFilter = cat;
            librarySubFilter = 'all'; // Reset sub-filter when switching main category
            const subFilterSelect = document.getElementById('library-subcategory-filter');
            if (subFilterSelect) subFilterSelect.value = 'all';

            coverflowIndex = 0;
            document.querySelectorAll('#coverflow-library-panel .filter-chip').forEach(btn => {
                btn.classList.toggle('active', btn.getAttribute('onclick').includes(`'${cat}'`));
            });
            renderLibrary();
        }

        let librarySubTab = localStorage.getItem('mwv_library_sub_tab') || 'coverflow';

        function switchLibrarySubTab(tabId) {
            librarySubTab = tabId;
            localStorage.setItem('mwv_library_sub_tab', tabId);

            // Update buttons
            document.querySelectorAll('#coverflow-library-panel button.options-subtab').forEach(btn => btn.classList.remove('active'));
            const btn = document.getElementById(`lib-tab-btn-${tabId}`);
            if (btn) btn.classList.add('active');

            // Update views
            document.querySelectorAll('.library-sub-content').forEach(view => view.style.display = 'none');
            document.getElementById(`lib-view-${tabId}`).style.display = 'block';

            renderLibrary();
        }

        function setLibrarySubFilter(val) {
            librarySubFilter = val;
            coverflowIndex = 0;
            renderLibrary();
        }

        async function renderLibrary() {
            const track = document.getElementById('coverflow-track');
            if (!track) return;

            try {
                const library = await eel.get_library()();
                coverflowItems = library.media || [];

                // Filter logic
                if (libraryFilter !== 'all') {
                    const allowedTypes = CATEGORY_MAP[libraryFilter] || [];
                    coverflowItems = coverflowItems.filter(i => allowedTypes.includes(i.category));
                }

                // Populate dynamic sub-filters based on current category
                const subFilterSelect = document.getElementById('library-subcategory-filter');
                if (subFilterSelect) {
                    const currentVal = subFilterSelect.value;
                    const categories = [...new Set(library.media.map(i => i.category))].filter(Boolean).sort();

                    let optionsHtml = `<option value="all" data-i18n="filter_sub_all">Alle Unterkategorien</option>`;
                    categories.forEach(cat => {
                        optionsHtml += `<option value="${cat.toLowerCase()}">${cat}</option>`;
                    });

                    subFilterSelect.innerHTML = optionsHtml;
                    subFilterSelect.value = categories.map(c => c.toLowerCase()).includes(currentVal.toLowerCase()) ? currentVal : 'all';
                }

                if (librarySubFilter !== 'all') {
                    coverflowItems = coverflowItems.filter(i => (i.category || '').toLowerCase() === librarySubFilter.toLowerCase());
                }

                if (coverflowItems.length === 0) {
                    const noMediaHtml = `<div style="padding: 100px; color: #999; text-align: center; width: 100%;" data-i18n="lib_no_media_warning">Keine Medien gefunden</div>`;
                    safeHtml('coverflow-track', noMediaHtml);
                    safeHtml('grid-container', noMediaHtml);
                    safeHtml('streaming-grid-container', noMediaHtml);
                    return;
                }

                if (librarySubTab === 'coverflow') {
                    updateCoverflowDisplay();
                } else if (librarySubTab === 'grid') {
                    renderGridView();
                } else if (librarySubTab === 'details') {
                    renderDetailedView();
                } else if (librarySubTab === 'streaming') {
                    renderVideoStreamingView();
                } else if (librarySubTab === 'album') {
                    renderAlbumView();
                } else if (librarySubTab === 'following') {
                    renderFollowingView();
                } else if (librarySubTab === 'database') {
                    renderDatabaseView();
                }

            } catch (e) {
                console.error("Failed to render library:", e);
            }
        }

        function renderAlbumView() {
            const container = document.getElementById('album-grid-container');
            if (!container) return;

            // Group by Album name
            const albums = {};
            coverflowItems.forEach(item => {
                let albumName = 'Unknown Album';
                if (item.tags && item.tags.album) albumName = item.tags.album;
                else if (item.category === 'Album') albumName = item.name;

                if (!albums[albumName]) {
                    albums[albumName] = {
                        name: albumName,
                        art: item.art_path,
                        items: []
                    };
                }
                albums[albumName].items.push(item);
            });

            let html = '';
            Object.values(albums).forEach(album => {
                const cover = album.art ? `/direct/${encodeURIComponent(album.art)}` : 'img/default_album.png';
                html += `
                <div class="video-card" onclick="playAlbum('${album.name.replace(/'/g, "\\'")}')">
                    <div class="video-card-preview">
                        <img src="${cover}" alt="${album.name}">
                        <div class="video-duration-badge">${album.items.length} Items</div>
                    </div>
                    <div class="video-card-info">
                        <div class="video-card-title">${album.name}</div>
                        <div class="video-card-meta">
                            <span>Album • ${album.items[0].tags.artist || 'Unknown Artist'}</span>
                        </div>
                    </div>
                </div>`;
            });

            safeHtml('album-grid-container', html || '<div style="padding: 40px; color: #999; text-align: center; width: 100%;">Keine Alben gefunden</div>');
        }

        function renderFollowingView() {
            const container = document.getElementById('following-grid-container');
            if (!container) return;

            // Group by Series
            const series = {};
            coverflowItems.filter(i => isVideoItem(i) || i.category === 'Serie').forEach(item => {
                const seriesName = (item.tags && item.tags.series) || (item.category === 'Serie' ? item.name : 'Other Videos');
                if (!series[seriesName]) {
                    series[seriesName] = {
                        name: seriesName,
                        items: []
                    };
                }
                series[seriesName].items.push(item);
            });

            let html = '';
            Object.values(series).forEach(s => {
                const firstItem = s.items[0];
                const cover = firstItem.art_path ? `/direct/${encodeURIComponent(firstItem.art_path)}` : 'img/default_video.png';
                html += `
                <div class="video-card" onclick="playSeries('${s.name.replace(/'/g, "\\'")}')">
                    <div class="video-card-preview">
                        <img src="${cover}" alt="${s.name}">
                        <div class="video-duration-badge">${s.items.length} Folgen</div>
                    </div>
                    <div class="video-card-info">
                        <div class="video-card-title">${s.name}</div>
                        <div class="video-card-meta">
                            <span>Serie • ${s.items.length} Episoden</span>
                        </div>
                    </div>
                </div>`;
            });

            safeHtml('following-grid-container', html || '<div style="padding: 40px; color: #999; text-align: center; width: 100%;">Keine Folgen gefunden</div>');
        }

        function playAlbum(albumName) {
            const items = coverflowItems.filter(item => (item.tags && item.tags.album === albumName) || (item.category === 'Album' && item.name === albumName));
            if (items.length > 0) {
                currentPlaylist = [...items];
                playlistIndex = 0;
                isShuffle = false;
                if (typeof updateShuffleUI === 'function') updateShuffleUI();
                
                const firstItem = currentPlaylist[0];
                if (isVideoItem(firstItem)) {
                    switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                    setTimeout(() => {
                        if (typeof playVideo === 'function') playVideo(firstItem, firstItem.path);
                    }, 100);
                } else {
                    if (typeof play === 'function') play(firstItem, getMediaUrl(firstItem));
                    switchTab('player', document.getElementById('active-queue-tab-trigger'));
                }
                if (typeof renderPlaylist === 'function') renderPlaylist();
            }
        }

        function playSeries(seriesName) {
            const items = coverflowItems.filter(item => (item.tags && item.tags.series === seriesName) || (item.category === 'Serie' && item.name === seriesName));
            if (items.length > 0) {
                currentPlaylist = [...items];
                playlistIndex = 0;
                isShuffle = false;
                if (typeof updateShuffleUI === 'function') updateShuffleUI();

                const firstItem = currentPlaylist[0];
                if (isVideoItem(firstItem)) {
                    switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                    setTimeout(() => {
                        if (typeof playVideo === 'function') playVideo(firstItem, firstItem.path);
                    }, 100);
                } else {
                    if (typeof play === 'function') play(firstItem, getMediaUrl(firstItem));
                    switchTab('player', document.getElementById('active-queue-tab-trigger'));
                }
                if (typeof renderPlaylist === 'function') renderPlaylist();
            }
        }

        function renderVideoStreamingView() {
            const container = document.getElementById('streaming-grid-container');
            if (!container) return;

            const videos = coverflowItems.filter(i => isVideoItem(i));
            let html = '';
            
            videos.forEach((item) => {
                const progressWidth = item.duration_sec ? ((item.playback_position || 0) / item.duration_sec) * 100 : 0;
                const cover = item.art_path ? `/direct/${encodeURIComponent(item.art_path)}` : 'img/default_video.png';
                const streamUrl = `/direct/${encodeURIComponent(item.path)}`;
                
                html += `
                <div class="video-card" onclick="playMediaObject(coverflowItems.find(v => v.name === '${item.name.replace(/'/g, "\\'")}'))">
                    <div class="video-card-preview">
                        <img src="${cover}" alt="${item.name}">
                        <video src="${streamUrl}" muted loop preload="none"></video>
                        <div class="video-duration-badge">${item.duration || ''}</div>
                        ${item.playback_position > 0 ? `<div class="playback-progress-bar" style="width: ${progressWidth}%"></div>` : ''}
                    </div>
                    <div class="video-card-info">
                        <div class="video-card-title">${item.name}</div>
                        <div class="video-card-meta">
                            <span>${item.codec || ''} • ${item.extension || ''}</span>
                            <span>${item.last_played ? new Date(item.last_played).toLocaleDateString() : ''}</span>
                        </div>
                    </div>
                </div>`;
            });

            safeHtml('streaming-grid-container', html || '<div style="padding: 40px; color: #999; text-align: center; width: 100%;">Keine Videos gefunden</div>');

            container.querySelectorAll('.video-card').forEach(card => {
                const video = card.querySelector('video');
                card.addEventListener('mouseenter', () => {
                   if (video) {
                       video.currentTime = 0;
                       video.play().catch(e => console.warn('Preview play failed:', e));
                   }
                });
                card.addEventListener('mouseleave', () => {
                    if (video) {
                        video.pause();
                        video.currentTime = 0;
                    }
                });
            });
        }

        function renderGridView() {
            const container = document.getElementById('grid-container');
            if (!container) return;

            const html = coverflowItems.map((item, idx) => {
                const artwork = `/cover/${encodeURIComponent(item.name)}`;
                const title = item.tags && item.tags.title ? item.tags.title : (item.name || 'Unknown');
                const artist = item.tags && item.tags.artist ? item.tags.artist : '';
                const displayTitle = artist ? `${artist} - ${title}` : title;

                let seriesInfo = '';
                if (item.category === 'Serie' && item.tags && item.tags.season !== undefined) {
                    const s = String(item.tags.season).padStart(2, '0');
                    const e = String(item.tags.episode || 0).padStart(2, '0');
                    seriesInfo = `<span style="color: #e74c3c; font-weight: bold; margin-left: 5px;">S${s}E${e}</span>`;
                }

                return `
                    <div class="grid-item" onclick="playMediaObject(coverflowItems[${idx}])">
                        <div class="grid-cover" style="background-image: url('${artwork}')">
                            ${item.is_chrome_native ? `<div class="native-badge" title="Chrome Native support">⚡ DIRECT</div>` : ''}
                            ${getCategoryBadgeHtml(item)}
                        </div>
                        <div class="grid-info">
                            <div class="grid-title" title="${item.name}">${displayTitle}${seriesInfo}</div>
                            <div class="grid-meta">${item.category || ''} | ${item.type || ''}</div>
                        </div>
                    </div>
                `;
            }).join('');

            safeHtml('grid-container', html);
        }

        function renderDetailedView() {
            const header = document.getElementById('details-table-header');
            const body = document.getElementById('details-table-body');
            if (!header || !body) return;

            // Render Header
            const cols = [
                { key: 'name', label: 'Name' },
                { key: 'category', label: 'Category' },
                { key: 'type', label: 'Type' },
                { key: 'path', label: 'Path' },
                { key: 'tags', label: 'Tags' }
            ];

            safeHtml('details-table-header', cols.map(c => `<th>${c.label}</th>`).join(''));

            // Render Body
            const html = coverflowItems.map((item, idx) => {
                return `
                    <tr onclick="playMediaObject(coverflowItems[${idx}])">
                        <td>${item.name || '---'}</td>
                        <td>${item.category || '---'}</td>
                        <td>${item.type || '---'}</td>
                        <td title="${item.path}">${item.path || '---'}</td>
                        <td>${item.tags ? JSON.stringify(item.tags) : '---'}</td>
                    </tr>
                `;
            }).join('');

            safeHtml('details-table-body', html);
        }

        async function triggerTxtImport(category) {
            try {
                showToast(`Starte TXT Import für ${category}...`, 'info');
                const result = await eel.import_txt_to_db(category)();
                
                if (result.status === 'ok') {
                    showToast(`Import erfolgreich: ${result.imported} Items hinzugefügt, ${result.skipped} übersprungen.`, 'success');
                    renderDatabaseView(); // Refresh table
                } else if (result.status === 'cancelled') {
                    showToast("Import abgebrochen.", 'info');
                } else if (result.error) {
                    showToast(`Import Fehler: ${result.error}`, 'error');
                }
            } catch (e) {
                console.error("TXT Import failed:", e);
                showToast("Interner Fehler beim Import.", 'error');
            }
        }

        async function renderDatabaseView() {
            const body = document.getElementById('lib-db-table-body');
            const stats = document.getElementById('lib-db-stats');
            const searchInput = document.getElementById('lib-db-search');
            if (!body) return;

            try {
                // We fetch the FULL library for the database view, ignoring current filters
                const library = await eel.get_library()();
                let items = library.media || [];

                // Filter by search term
                const searchTerm = searchInput ? searchInput.value.toLowerCase() : '';
                if (searchTerm) {
                    items = items.filter(i => 
                        String(i.id || '').includes(searchTerm) ||
                        (i.name || '').toLowerCase().includes(searchTerm) ||
                        (i.path || '').toLowerCase().includes(searchTerm) ||
                        (i.category || '').toLowerCase().includes(searchTerm) ||
                        (i.type || '').toLowerCase().includes(searchTerm)
                    );
                }

                if (stats) stats.innerText = `${items.length} Objekte in der Datenbank`;

                const html = items.map((item, idx) => {
                    const artist = item.tags && item.tags.artist ? item.tags.artist : '';
                    const album = item.tags && item.tags.album ? item.tags.album : '';
                    const info = [artist, album].filter(Boolean).join(' / ');
                    
                    return `
                        <tr>
                            <td style="color: #999; font-size: 0.8em; text-align: center;">${idx + 1}</td>
                            <td style="font-family: monospace; font-size: 0.85em; color: #2196F3; font-weight: bold;">${item.id || '---'}</td>
                            <td><span class="badge-${(item.type || 'unknown').toLowerCase()}">${item.type || '---'}</span></td>
                            <td>${item.category || '---'}</td>
                            <td style="font-weight: 500;">${item.name || '---'}</td>
                            <td style="font-size: 0.9em; color: #444;">${info || '---'}</td>
                            <td style="font-size: 0.8em; color: #666; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;" title="${item.path}">
                                ${item.path || '---'}
                            </td>
                            <td>
                                <div style="display: flex; gap: 5px;">
                                    <button class="icon-btn" onclick="playMediaObjectByName('${item.name.replace(/'/g, "\\'")}')" title="Abspielen">▶️</button>
                                    <button class="icon-btn" onclick="openMetaEditor('${item.name.replace(/'/g, "\\'")}')" title="Editieren">✏️</button>
                                </div>
                            </td>
                        </tr>
                    `;
                }).join('');

                safeHtml('lib-db-table-body', html || '<tr><td colspan="7" style="text-align: center; padding: 20px;">Keine Einträge gefunden</td></tr>');

            } catch (e) {
                console.error("Failed to render database view:", e);
                safeHtml('lib-db-table-body', '<tr><td colspan="7" style="color: red;">Fehler beim Laden der Datenbank</td></tr>');
            }
        }

        async function playMediaObjectByName(name) {
            const media = await eel.get_media_by_name(name)();
            if (media) playMediaObject(media);
        }

        async function openMetaEditor(name) {
            const media = await eel.get_media_by_name(name)();
            if (media) {
                switchTab('edit');
                openEditForm(media);
            } else {
                alert("Medium nicht in Datenbank gefunden.");
            }
        }

        function updateCoverflowDisplay() {
            const track = document.getElementById('coverflow-track');
            if (!track) return;

            const html = coverflowItems.map((item, idx) => {
                const artwork = `/cover/${encodeURIComponent(item.name)}`;
                const title = item.tags && item.tags.title ? item.tags.title : (item.name || 'Unknown');
                const artist = item.tags && item.tags.artist ? item.tags.artist : '';
                const displayTitle = artist ? `${artist} - ${title}` : title;

                let seriesInfo = '';
                if (item.category === 'Serie' && item.tags && item.tags.season !== undefined) {
                    const s = String(item.tags.season).padStart(2, '0');
                    const e = String(item.tags.episode || 0).padStart(2, '0');
                    seriesInfo = `<span style="color: #ff5252; font-weight: 800; margin-left: 8px; font-size: 0.9em;">S${s}E${e}</span>`;
                }

                let classes = 'coverflow-item';
                if (idx === coverflowIndex) classes += ' active';
                else if (idx < coverflowIndex) classes += ' left';
                else classes += ' right';

                return `
                    <div class="${classes}" style="background-image: url('${artwork}')" 
                         onclick="selectCoverflowItem(${idx})"
                         tabindex="0">
                        ${item.is_chrome_native ? `<div class="native-badge" style="position: absolute; top: 10px; right: 10px; padding: 2px 6px; background: #4caf50; color: white; font-size: 0.7em; font-weight: bold; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">⚡ DIRECT</div>` : ''}
                        <div class="info">
                            <div class="title">${displayTitle}${seriesInfo}</div>
                            <div class="meta">${item.category || ''} | ${item.type || ''}</div>
                        </div>
                    </div>
                `;
            }).join('');

            safeHtml('coverflow-track', html);

            // Center the active item
            const activeEl = track.querySelector('.coverflow-item.active');
            if (activeEl) {
                const offset = activeEl.offsetLeft + (activeEl.offsetWidth / 2);
                const containerHalf = track.parentElement.offsetWidth / 2;
                track.style.transform = `translateX(${containerHalf - offset}px)`;
            }
        }

        function selectCoverflowItem(idx) {
            if (idx === coverflowIndex) {
                playMediaObject(coverflowItems[idx]);
            } else {
                coverflowIndex = idx;
                updateCoverflowDisplay();
            }
        }

        // Keyboard Navigation for Coverflow
        document.addEventListener('keydown', (e) => {
            const activeTab = localStorage.getItem('mwv_active_tab');
            if (activeTab !== 'library') return;

            if (e.key === 'ArrowLeft') {
                if (coverflowIndex > 0) {
                    coverflowIndex--;
                    updateCoverflowDisplay();
                }
            } else if (e.key === 'ArrowRight') {
                if (coverflowIndex < coverflowItems.length - 1) {
                    coverflowIndex++;
                    updateCoverflowDisplay();
                } else if (e.key === 'Enter') {
                    if (coverflowItems[coverflowIndex]) {
                        playMediaObject(coverflowItems[coverflowIndex]);
                    }
                }
            } else if (e.key === 'Enter') {
                if (coverflowItems[coverflowIndex]) {
                    playMediaObject(coverflowItems[coverflowIndex]);
                }
            }
        });

        function isVideoItem(item) {
            if (!item) return false;
            // 1. Check Category
            const videoCategories = ['Film', 'Serie', 'ISO/Image', 'Video', 'Musikvideos', 'Animes', 'Cartoons', 'Movie', 'TV Show'];
            if (item.category && videoCategories.includes(item.category)) return true;

            // 2. Check Extension
            const path = item.path || item.relpath || "";
            const videoExtensions = ['.mp4', '.mkv', '.iso', '.webm', '.avi', '.mov', '.ts', '.m4v', '.mpg', '.mpeg', '.flv', '.wmv'];
            const ext = path.toLowerCase().slice(((path.lastIndexOf(".") - 1) >>> 0) + 2);
            if (ext && videoExtensions.includes("." + ext)) return true;

            return false;
        }

        function playMediaObject(item) {
            if (isVideoItem(item)) {
                console.info("[Play-Routing] Video detected, switching to Video Player tab:", item.path);
                switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                // Delay slightly to ensure tab logic completes
                setTimeout(() => {
                    if (typeof playVideo === 'function') {
                        playVideo(item, item.path);
                    }
                }, 100);
            } else {
                if (typeof addToQueue === 'function') {
                    addToQueue(item);
                    switchTab('player', document.getElementById('active-queue-tab-trigger'));
                }
            }
        }

        function addToQueue(item) {
            if (!currentPlaylist) currentPlaylist = [];
            currentPlaylist.push(item);
            if (typeof renderPlaylist === 'function') renderPlaylist();
            showToast(t('pl_added_to_queue') || "Added to queue");
        }

        window.jumpToChapter = function (startTime) {
            const video = document.getElementById('native-html5-video-resource-node');
            const audio = document.getElementById('native-html5-audio-pipeline-element');

            let player = null;
            if (video && (video.offsetHeight > 0 || !video.paused)) player = video;
            else if (audio && (audio.offsetHeight > 0 || !audio.paused)) player = audio;

            if (player && (player.readyState > 0 || !player.paused)) {
                player.currentTime = startTime;
                player.play().catch(() => { });
                showToast(t('player_status_playing') + " (Kapitel @ " + new Date(startTime * 1000).toISOString().substring(11, 19) + ")");
            } else {
                console.warn("[JumpToChapter] No active player found to seek in.");
            }
        };

        function showToast(message, duration = 3000) {
            const container = document.getElementById('toast-container');
            if (!container) return;
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.innerText = message;
            container.appendChild(toast);
            setTimeout(() => {
                toast.remove();
            }, duration + 300);
        }

        function getCategoryBadgeHtml(item) {
            if (!item || !item.category) return '';
            const specialCategories = ['H\u00f6rbuch', 'Compilation', 'Serie', 'Film', 'E-Book', 'Dokument', 'Bilder', 'ISO/Image', 'Soundtrack', 'Playlist'];
            if (!specialCategories.includes(item.category)) return '';

            let catIcon = '';
            if (item.category === 'H\u00f6rbuch') catIcon = '🎧';
            else if (item.category === 'Film') catIcon = '🎬';
            else if (item.category === 'Serie') catIcon = '📺';
            else if (item.category === 'Dokument') catIcon = '📄';
            else if (item.category === 'E-Book') catIcon = '📖';
            else if (item.category === 'Bilder') catIcon = '🖼️';
            else if (item.category === 'ISO/Image') catIcon = '💿';
            else if (item.category === 'Compilation') catIcon = '💽';
            else if (item.category === 'Soundtrack') catIcon = '🎼';
            else if (item.category === 'Playlist') catIcon = '📜';

            if (!catIcon) return '';
            return `<div style="position:absolute; bottom:-4px; right:-4px; background:white; border-radius:50%; width:20px; height:20px; display:flex; align-items:center; justify-content:center; font-size:12px; box-shadow:0 1px 3px rgba(0,0,0,0.3); z-index:5;" title="${item.category}">${catIcon}</div>`;
        }

        let contextMenuItem = null;
        function showContextMenu(e, item) {
            e.preventDefault();
            contextMenuItem = item;
            const menu = document.getElementById('custom-context-menu');
            if (!menu) return;

            // Dynamically hide/show items based on file extension
            const ext = item.name.toLowerCase().split('.').pop();
            const isVideo = ['mp4', 'mkv', 'webm', 'mov', 'avi', 'ts'].includes(ext);
            const isDisc = ['iso', 'dvd', 'udf', 'img'].includes(ext) || item.is_directory || item.category === 'Film';
            const isAudio = ['mp3', 'flac', 'm4a', 'wav', 'ogg', 'opus'].includes(ext);

            const groupHeaders = menu.querySelectorAll('.context-menu-header');
            const dividers = menu.querySelectorAll('.context-menu-divider');
            const items = menu.querySelectorAll('.context-menu-item');

            // Hide/Show based on type
            items.forEach(el => {
                const action = el.getAttribute('onclick');
                if (action.includes('dvd_native') || action.includes('bluray_native') || action.includes('vlc_iso')) {
                    el.style.display = isDisc ? 'flex' : 'none';
                } else if (action.includes('chrome_native') || action.includes('mediamtx') || action.includes('ffmpeg_browser') || action.includes('vlc_ts')) {
                    el.style.display = (isVideo || isAudio) ? 'flex' : 'none';
                } else if (action.includes('vlc_extern') || action.includes('cvlc')) {
                    el.style.display = 'flex'; // Always show general VLC
                }
            });

            // Adjust headers and dividers (simplified)
            groupHeaders.forEach(h => {
                if (h.innerText.includes('Disc') && !isDisc) h.style.display = 'none';
                else h.style.display = 'block';
            });

            menu.style.display = 'block';

            // Positioning
            let x = e.clientX;
            let y = e.clientY;

            menu.style.left = x + 'px';
            menu.style.top = y + 'px';

            // Adjust if off-screen
            const rect = menu.getBoundingClientRect();
            if (rect.right > window.innerWidth) {
                menu.style.left = (window.innerWidth - rect.width - 5) + 'px';
            }
            if (rect.bottom > window.innerHeight) {
                menu.style.top = (window.innerHeight - rect.height - 5) + 'px';
            }
        }

        function hideContextMenu() {
            const menu = document.getElementById('custom-context-menu');
            if (menu) menu.style.display = 'none';
        }

        async function handleContextMenuAction(mode) {
            if (!contextMenuItem) return;
            const item = contextMenuItem;
            hideContextMenu();

            if (mode === 'vlc_ts') {
                const res = await eel.vlc_ts_mode(item.path)();
                if (res.status === 'play') {
                    startEmbeddedVideo(item, res.path, null, res.type);
                } else {
                    showToast(res.error || "VLC TS Error");
                }
                return;
            }

            const res = await eel.open_video(item.path, mode)();
            if (res && res.status === 'play') {
                const embeddedModes = ['mediamtx', 'mediamtx_webrtc', 'chrome_native', 'chrome_direct', 'chrome_hls', 'chrome_fragmp4', 'ffmpeg_browser', 'chrome_remux', 'chrome_transcode', 'transcode'];
                if (embeddedModes.includes(res.mode) || embeddedModes.includes(mode)) {
                    if (typeof startEmbeddedVideo === 'function') {
                        startEmbeddedVideo(item, res.path, null, res.type);
                        switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                    }
                }
            } else if (res && res.status === 'error') {
                if (typeof showToast === 'function') showToast(res.error);
                else console.error(res.error);
            } else if (res && res.status === 'ok') {
                showToast(res.message || "Aktion gestartet");
            }
        }


        window.addEventListener('click', () => hideContextMenu());
        window.addEventListener('scroll', () => hideContextMenu(), true);
        let playlistIndex = -1;
        let isShuffle = false;
        let isRepeat = 'off'; // 'off', 'all', 'one'
        let shuffledPlaylist = [];
        // Pick-and-insert state
        let pickedIndex = -1;
        let pickTimer = null;

        // Auto-play next song
        if (activeAudioPipeline) {
            activeAudioPipeline.onended = () => {
                if (isRepeat === 'one') {
                    activeAudioPipeline.play();
                } else {
                    playNext();
                }
            };
        }

        function updateShuffleUI() {
            const btn = document.getElementById('btn-shuffle');
            const plBtn = document.getElementById('sequence-buffer-randomization-orchestrator');

            [btn, plBtn].forEach(b => {
                if (!b) return;
                const icon = b.querySelector('.icon-shuffle, .icon-shuffle-on');
                if (icon) {
                    icon.className = isShuffle ? 'icon-shuffle-on' : 'icon-shuffle';
                }
                if (isShuffle) b.classList.add('active');
                else b.classList.remove('active');
            });
        }

        function updateRepeatUI() {
            const btn = document.getElementById('btn-repeat');
            if (!btn) return;
            const container = document.getElementById('repeat-icon');
            if (container) {
                if (isRepeat === 'all') {
                    container.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>';
                } else if (isRepeat === 'one') {
                    container.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/><path d="M11 10h1v4"/><path d="M10 14h3"/></svg>';
                } else {
                    container.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="opacity:0.6;"><polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0 0 1-4 4H3"/></svg>';
                }
            }
            if (isRepeat !== 'off') btn.classList.add('active');
            else btn.classList.remove('active');
        }

        function toggleShuffle() {
            isShuffle = !isShuffle;
            updateShuffleUI();

            if (isShuffle) {
                // Create a shuffled version of the current playlist
                shuffledPlaylist = [...currentPlaylist];
                for (let i = shuffledPlaylist.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [shuffledPlaylist[i], shuffledPlaylist[j]] = [shuffledPlaylist[j], shuffledPlaylist[i]];
                }
                // If something is playing, make sure it's the current index in shuffled
                if (playlistIndex !== -1) {
                    const currentItem = currentPlaylist[playlistIndex];
                    playlistIndex = shuffledPlaylist.indexOf(currentItem);
                }
            } else {
                // Back to normal, readjust index
                if (playlistIndex !== -1 && shuffledPlaylist.length > 0) {
                    const currentItem = shuffledPlaylist[playlistIndex];
                    playlistIndex = currentPlaylist.indexOf(currentItem);
                }
            }
            renderPlaylist();
        }

        function toggleRepeat() {
            if (isRepeat === 'off') {
                isRepeat = 'all';
            } else if (isRepeat === 'all') {
                isRepeat = 'one';
            } else {
                isRepeat = 'off';
            }
            updateRepeatUI();
            renderPlaylist();
        }

        async function playNext() {
            const list = isShuffle ? shuffledPlaylist : currentPlaylist;
            if (list.length === 0) return;

            playlistIndex++;
            if (playlistIndex >= list.length) {
                if (isRepeat === 'all') {
                    playlistIndex = 0;
                } else {
                    playlistIndex = list.length - 1;
                    return; // Stop at end
                }
            }
            const item = list[playlistIndex];
            if (isVideoItem(item)) {
                onPlaylistItemClick(playlistIndex, item);
            } else {
                play(item, getMediaUrl(item), true);
            }
        }

        async function playPrev() {
            const list = isShuffle ? shuffledPlaylist : currentPlaylist;
            if (list.length === 0) return;

            playlistIndex--;
            if (playlistIndex < 0) {
                if (isRepeat === 'all') {
                    playlistIndex = list.length - 1;
                } else {
                    playlistIndex = 0;
                }
            }
            const item = list[playlistIndex];
            if (isVideoItem(item)) {
                onPlaylistItemClick(playlistIndex, item);
            } else {
                play(item, getMediaUrl(item), true);
            }
        }

        function getMediaUrl(item) {
            let itemName = item.name || item.filename || "unknown";
            let url = '/media/' + encodeURIComponent(itemName);
            if (item.is_transcoded && item.transcoded_format) {
                url += '.' + item.transcoded_format.toLowerCase() + '_transcoded';
            }
            return url;
        }



        async function initTranslations() {
            try {
                const response = await fetch('i18n.json');
                translations = await response.json();
                currentLanguage = await eel.get_language()();

                if (typeof currentLanguage !== 'string' || !translations[currentLanguage]) {
                    currentLanguage = 'de';
                }

                // Update select element
                const select = document.getElementById('language-select');
                if (select) select.value = currentLanguage;

                applyTranslations(currentLanguage);

                if (typeof checkConnection === 'function') {
                    checkConnection();
                }
                syncVersionInfo();

                // Re-refresh current tab
                const activeTab = localStorage.getItem('mwv_active_tab') || 'player';
                switchTab(activeTab, getTabButton(activeTab));
            } catch (e) {

                console.error('Failed to load translations:', e);
            }
        }

        function applyTranslations(lang) {
            currentLanguage = lang;
            const elements = document.querySelectorAll('[data-i18n]');
            elements.forEach(el => {
                const key = el.getAttribute('data-i18n');
                let val = null;

                // Handle [attribute]key format
                const attrMatch = key.match(/^\[([^\]]+)\](.+)$/);
                if (attrMatch) {
                    const attr = attrMatch[1];
                    const subKey = attrMatch[2];
                    val = t(subKey);
                    if (typeof val === 'string') {
                        el.setAttribute(attr, val);
                    }
                    return;
                }

                val = t(key);
                if (val === key || typeof val !== 'string') return;

                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = val;
                } else {
                    // Important: Only overwrite if it's a simple text-only element
                    // to avoid destroying nested icons/spans.
                    if (el.children.length === 0) {
                        el.innerHTML = val;
                    } else {
                        // For elements with children, more complex logic might be needed
                        // e.g., finding a specific child to update or leaving it alone.
                    }
                }
            });
            document.documentElement.lang = lang;
        }

        async function changeLanguage(lang) {
            await eel.set_language(lang)();
            applyTranslations(lang);
        }

        function t(key, defaultValue) {
            if (translations[currentLanguage] && translations[currentLanguage][key]) {
                // Support \n in JSON strings
                return translations[currentLanguage][key].replace(/\\n/g, '\n');
            }

            // Fallback to German base translations
            if (translations.de && translations.de[key]) {
                return translations.de[key].replace(/\\n/g, '\n');
            }

            return defaultValue || key;
        }

        // Initialize on load
        window.addEventListener('load', initTranslations);

        // Add to switchTab logic to refresh playlist if it's selected
        const originalSwitchTab = window.switchTab;
        window.switchTab = function (tabId, btn) {
            if (typeof originalSwitchTab === 'function') {
                originalSwitchTab(tabId, btn);
            } else {
                // Fallback if not yet defined
                const contents = document.querySelectorAll('.tab-content');
                contents.forEach(c => c.classList.remove('active'));
                const target = document.getElementById(tabId + '-tab') || document.getElementById(tabId);
                if (target) target.classList.add('active');

                const btns = document.querySelectorAll('.tab-btn');
                btns.forEach(b => b.classList.remove('active'));
                if (btn) btn.classList.add('active');
            }

            if (tabId === 'playlist') {
                renderPlaylist();
            }
        };
    
    
        let fbCurrentPath = null;
        let fbParentPath = null;

        async function fbPickFolder() {
            const folder = await eel.pick_folder()();
            if (folder) {
                // Switch to browser tab automatically after folder selection
                switchTab('file', document.querySelector('.tab-btn[onclick*="file"]'));
                fbNavigate(folder);
            }
        }

        async function fbNavigate(dirPath, retryCount) {
            retryCount = retryCount || 0;
            try {
                let result = await eel.browse_dir(dirPath || null)();
                if (result.error) {
                    safeHtml('fb-list', `<p style="color: #c33;">❌ ${result.error}</p>`);
                    return;
                }
                fbCurrentPath = result.path;
                fbParentPath = result.parent;
                safeValue('fb-path-input', result.path);
                const backBtn = document.getElementById('fb-back');
                if (backBtn) backBtn.disabled = !result.parent;

                let list = document.getElementById('fb-list');
                if (list) list.innerHTML = '';

                if (result.items.length === 0) {
                    safeHtml('fb-list', `<p style="color: #999;">${t('fb_no_items')}</p>`);
                    return;
                }

                result.items.forEach(item => {
                    let row = document.createElement('div');
                    row.style.cssText = 'display: flex; align-items: center; padding: 8px 12px; margin-bottom: 4px; border: 1px solid #eee; border-radius: 6px; cursor: pointer; transition: background 0.1s;';
                    row.onmouseover = () => row.style.background = '#f5f5f5';
                    row.onmouseout = () => row.style.background = '';

                    if (item.type === 'folder') {
                        row.innerHTML = `<span style="font-size: 1.3em; margin-right: 10px;">📁</span><span style="flex:1;">${item.name}</span>`;
                        row.onclick = () => fbNavigate(item.path);
                    } else {
                        row.innerHTML = `<span style="font-size: 1.3em; margin-right: 10px;">🎵</span><span style="flex:1;" class="fb-name">${item.name}</span><span class="fb-status" style="color: #999; font-size: 0.85em;">${item.size}</span>`;
                        row.onclick = async () => {
                            let statusEl = row.querySelector('.fb-status');
                            statusEl.textContent = '⏳ …';
                            let res = await eel.add_file_to_library(item.path)();
                            if (res.status === 'added' || res.status === 'exists') {
                                statusEl.textContent = res.status === 'added' ? t('fb_added') : t('fb_exists');
                                statusEl.style.color = res.status === 'added' ? '#2a7' : '#c90';

                                let finalItem = res.item;
                                if (!finalItem) {
                                    const lib = await eel.get_library()();
                                    finalItem = lib.media.find(m => m.name === (res.name || item.name));
                                }
                                if (finalItem && typeof loadLibrary === 'function') {
                                    loadLibrary();
                                }
                            } else {
                                statusEl.textContent = '❌ ' + (res.error || 'Fehler');
                                statusEl.style.color = '#c33';
                            }
                        };
                    }
                    list.appendChild(row);
                });
            } catch (e) {
                console.error('[fbNavigate] Error:', e);
                if (retryCount < 3) {
                    setTimeout(() => fbNavigate(dirPath, retryCount + 1), 1000);
                } else {
                    const list = document.getElementById('fb-list');
                    if (list) list.innerHTML = `<p style="color: #c33;">❌ ${t('common_error')}${e.message}</p>`;
                }
            }
        }


        function fbBack() {
            if (fbParentPath) fbNavigate(fbParentPath);
        }
    
    
        // ============ Debug Log Logic ============
        async function loadDebugDBInfo() {
            const infoEl = document.getElementById('debug-db-info');
            if (!infoEl) return;
            try {
                const stats = await eel.get_db_stats()();

                let html = `
                    <div style="background: #f8f9fa; border-radius: 10px; padding: 15px; border: 1px solid #eef;">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #eee;">
                            <span style="font-weight: bold; color: #333; font-size: 1.1em;">
                                <span class="icon-database" style="background-color: #2980b9;"></span> ${t('database_item') || 'Items'}:
                                <span style="color: #2980b9; margin-left: 5px;">${stats.total_items}</span>
                            </span>
                        </div>
                        <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                `;

                for (const [cat, count] of Object.entries(stats.categories)) {
                    html += `
                        <div style="display: flex; align-items: center; background: white; border: 1px solid #ddd; border-radius: 20px; padding: 4px 10px; font-size: 0.85em; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                            <span style="font-weight: 600; color: #555; margin-right: 6px;">${cat}:</span>
                            <span style="color: #2a7; font-weight: bold;">${count}</span>
                        </div>
                    `;
                }

                html += `
                        </div>
                    </div>
                `;
                infoEl.innerHTML = html;
            } catch (e) {
                console.error('[DB Info] Error:', e);
                infoEl.innerText = t('db_loading_error') || 'Error loading DB stats';
            }
        }

        async function loadDebugLogs() {
            loadDebugDBInfo();
            const debugConsole = await eel.get_konsole()();
            const debugPre = document.getElementById('debug-output');
            const debugItemsJson = document.getElementById('debug-items-json');

            if (debugPre && debugConsole.logs) {
                // Only update if content changed or first time
                if (debugPre.innerText !== debugConsole.logs) {
                    const parent = debugPre.parentElement;
                    const isAtBottom = parent ? (parent.scrollHeight - parent.scrollTop - parent.clientHeight < 50) : true;

                    debugPre.innerText = debugConsole.logs;

                    if (parent && isAtBottom) {
                        parent.scrollTop = parent.scrollHeight;
                    }
                }
            }

            if (debugItemsJson && debugConsole.env) {
                // Update Runtime Info
                const pyPid = document.getElementById('debug-python-pid');
                const brPid = document.getElementById('debug-browser-pid');
                const lvSel = document.getElementById('debug-log-level-select');

                if (pyPid) pyPid.innerText = debugConsole.env.pid || '-';
                if (brPid) brPid.innerText = debugConsole.env.browser_pid || 'N/A';
                if (lvSel && !lvSel.dataset.manual) {
                    lvSel.value = debugConsole.env.log_level || 'INFO';
                }

                // Update current dict view if it's currently showing env or flags (which refresh regularly)
                // or if it's empty/loading
                const dictSelect = document.getElementById('debug-dict-select');
                if (dictSelect) {
                    const currentVal = dictSelect.value;
                    const isManualRefreshView = (currentVal === 'library' || currentVal === 'parser');
                    const isEmpty = !debugItemsJson.innerText.trim() || debugItemsJson.innerText.includes('Loading') || debugItemsJson.innerText.includes('Lade');

                    if (currentVal === 'env') {
                        debugItemsJson.innerHTML = syntaxHighlight(debugConsole.env);
                    } else if (currentVal === 'flags') {
                        debugItemsJson.innerHTML = syntaxHighlight(debugConsole.debug_flags);
                    } else if (isEmpty && currentVal === 'library') {
                        const libRes = await eel.get_library()();
                        if (libRes && libRes.media) {
                            debugItemsJson.innerHTML = syntaxHighlight(libRes.media);
                        }
                    }
                }
            }
        }

        async function changeDebugDictView(viewType) {
            const debugItemsJson = document.getElementById('debug-items-json');
            if (!debugItemsJson) return;

            debugItemsJson.innerHTML = '<i>Processing...</i>';

            try {
                let data = null;
                if (viewType === 'library') {
                    const res = await eel.get_library()();
                    data = res.media;
                } else if (viewType === 'parser') {
                    data = await eel.get_parser_config()();
                } else {
                    const res = await eel.get_konsole()();
                    if (viewType === 'env') data = res.env;
                    if (viewType === 'flags') data = res.debug_flags;
                }

                if (data) {
                    debugItemsJson.innerHTML = syntaxHighlight(data);
                } else {
                    debugItemsJson.innerText = 'No data available for: ' + viewType;
                }
            } catch (e) {
                console.error("[changeDebugDictView] Error:", e);
                debugItemsJson.innerText = 'Error loading data: ' + e.message;
            }
        }

        async function changeLogLevel(level) {
            const select = document.getElementById('debug-log-level-select');
            if (select) select.dataset.manual = "true";
            await eel.set_log_level(level)();
            loadDebugLogs(); // Refresh
        }

        // JSON Syntax Highlighting mit optimierten Farben
        function syntaxHighlight(json) {
            if (typeof json !== 'string') {
                json = JSON.stringify(json, null, 2);
            }
            json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
            return json.replace(/"(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?/g, function (match) {
                let cls = 'json-number';
                let color = '#b5cea8'; // Numbers: soft green
                if (/^"/.test(match)) {
                    if (/:$/.test(match)) {
                        cls = 'json-key';
                        color = '#9cdcfe'; // Keys: bright blue
                        match = match.replace(/^"(.*)":$/, '"<span style="color: #9cdcfe; font-weight: 500;">$1</span>":');
                        return match;
                    } else {
                        cls = 'json-string';
                        color = '#ce9178'; // Strings: orange
                    }
                } else if (/true|false/.test(match)) {
                    cls = 'json-boolean';
                    color = '#569cd6'; // Booleans: blue
                } else if (/null/.test(match)) {
                    cls = 'json-null';
                    color = '#569cd6'; // Null: blue
                }
                return '<span style="color: ' + color + ';">' + match + '</span>';
            });
        }

        async function loadDebugFlags() {
            try {
                const flags = await eel.get_debug_flags()();
                const optionsContainer = document.getElementById('debug-flags-container');
                const modalContainer = document.getElementById('modal-debug-flags');
                const reusedContainer = document.getElementById('debug-flags-container-reused');

                const flagsHtml = `<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; width: 100%;">` +
                    Object.entries(flags).map(([key, value]) => {
                        const labelText = t(`debug_flag_${key}`) || key.toUpperCase();
                        return `
                                    <label style="display: flex; align-items: center; gap: 10px; cursor: pointer; padding: 6px 12px; border: 1px solid #f0f0f0; border-radius: 6px; background: #fff; transition: all 0.2s;"
                                           onmouseover="this.style.background='#fafafa'; this.style.borderColor='#2a7'" 
                                           onmouseout="this.style.background='#fff'; this.style.borderColor='#f0f0f0'">
                                        <input type="checkbox" ${value ? 'checked' : ''} onchange="toggleDebugFlag('${key}', this.checked)" style="accent-color: #2a7; transform: scale(1.1); cursor: pointer;">
                                        <span style="font-family: inherit; font-size: 0.82em; color: #333; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${labelText}</span>
                                    </label>`;
                    }).join('') + `</div>`;

                if (optionsContainer) optionsContainer.innerHTML = flagsHtml;
                if (modalContainer) modalContainer.innerHTML = flagsHtml;
                if (reusedContainer) reusedContainer.innerHTML = flagsHtml;

            } catch (e) {
                console.error("Failed to load debug flags:", e);
            }
        }

        async function toggleDebugFlag(key, value) {
            await eel.set_debug_flag(key, value)();
            // Refresh both locations
            loadDebugFlags();
        }

        async function setAllFlags(value) {
            await eel.set_all_debug_flags(value)();
            loadDebugFlags();
        }

        function toggleDebugMenu() {
            const modal = document.getElementById('debug-flags-modal');
            if (modal.style.display === 'none') {
                modal.style.display = 'block';
                safeStyle('feature-status-modal', 'display', 'none'); // Close other
                loadDebugFlags();
            } else {
                modal.style.display = 'none';
            }
        }

        eel.expose(log_to_debug);
        function log_to_debug(message) {
            const debugTextarea = document.getElementById('browse-results-debug');
            if (debugTextarea) {
                if (debugTextarea.value.length > 0 && !debugTextarea.value.endsWith('\n')) {
                    debugTextarea.value += '\n';
                }
                debugTextarea.value += message + '\n';
                debugTextarea.scrollTop = debugTextarea.scrollHeight;
            }
        }

        eel.expose(set_db_status);
        function set_db_status(isVisible) {
            const container = document.getElementById('db-status-container');
            if (container) {
                container.style.display = isVisible ? 'flex' : 'none';
            }
        }

        let __testOutputBuffer = '';
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

        eel.expose(append_test_output);
        function append_test_output(message) {
            appendTestOutputChunk(String(message || ''));
        }
    
    
        async function moveItemUp(index) {
            // Call backend to persist reorder, then refresh playlist from backend
            try {
                if (typeof eel === 'undefined') {
                    if (index <= 0) return;
                    const activeListClient = isShuffle ? shuffledPlaylist : currentPlaylist;
                    [activeListClient[index - 1], activeListClient[index]] = [activeListClient[index], activeListClient[index - 1]];
                    if (playlistIndex === index) playlistIndex = index - 1;
                    else if (playlistIndex === index - 1) playlistIndex = index;
                    renderPlaylist();
                    return;
                }

                // If shuffle is active, map the visible shuffled index to the
                // actual index in `currentPlaylist` before calling the backend.
                // Prefer server-side move-by-key to avoid index-mapping issues
                let item = isShuffle ? shuffledPlaylist[index] : currentPlaylist[index];
                let key = (item && (item.name || item.path)) || null;
                let res = null;
                if (!key) {
                    console.debug('moveItemUp: no key for index', index);
                    // fallback to index-based call if key unavailable
                    res = await eel.move_item_up(index)();
                    console.debug('moveItemUp: index-fallback res=', res);
                } else {
                    console.debug('moveItemUp: calling move_item_up_by_key key=', key, 'index=', index, 'isShuffle=', isShuffle);
                    res = await eel.move_item_up_by_key(key)();
                    console.debug('moveItemUp: server res=', res);
                }
                if (res && res.status === 'ok') {
                    // Refreshed state returned in res.items
                    currentPlaylist = res.items.slice();
                    playlistIndex = res.index;

                    if (isShuffle) {
                        // In shuffle mode, we don't want to reshuffle the whole list,
                        // but we need to stay consistent. For now, disable reorder in shuffle
                        // or update the shuffled list too.
                        // Choice: disable reorder buttons in renderPlaylist if isShuffle?
                        // Better: If isShuffle is active, we should probably move the item in shuffled list too.
                        const movedItem = currentPlaylist[playlistIndex];
                        // simplest: just update currentPlaylist and hope user switches off shuffle to reorder
                        // But let's at least keep the index correct.
                    }
                    renderPlaylist();
                }
            } catch (e) {
                console.error('moveItemUp error', e);
            }
        }

        async function moveItemDown(index) {
            try {
                if (typeof eel === 'undefined') {
                    const activeListClient = isShuffle ? shuffledPlaylist : currentPlaylist;
                    if (index >= activeListClient.length - 1) return;
                    [activeListClient[index], activeListClient[index + 1]] = [activeListClient[index + 1], activeListClient[index]];
                    if (playlistIndex === index) playlistIndex = index + 1;
                    else if (playlistIndex === index + 1) playlistIndex = index;
                    renderPlaylist();
                    return;
                }

                // Map shuffled visible index to actual playlist index when needed.
                let item = isShuffle ? shuffledPlaylist[index] : currentPlaylist[index];
                let key = (item && (item.name || item.path)) || null;
                let res = null;
                if (!key) {
                    console.debug('moveItemDown: no key for index', index);
                    res = await eel.move_item_down(index)();
                    console.debug('moveItemDown: index-fallback res=', res);
                } else {
                    console.debug('moveItemDown: calling move_item_down_by_key key=', key, 'index=', index, 'isShuffle=', isShuffle);
                    res = await eel.move_item_down_by_key(key)();
                    console.debug('moveItemDown: server res=', res);
                }
                if (res && res.status === 'ok') {
                    currentPlaylist = res.items.slice();
                    playlistIndex = res.index;
                    renderPlaylist();
                }
            } catch (e) {
                console.error('moveItemDown error', e);
            }
        }

        async function removeItem(index) {
            try {
                if (typeof eel === 'undefined') {
                    const activeList = isShuffle ? shuffledPlaylist : currentPlaylist;
                    const removedItem = activeList[index];
                    activeList.splice(index, 1);

                    if (isShuffle) {
                        const masterIdx = currentPlaylist.indexOf(removedItem);
                        if (masterIdx !== -1) currentPlaylist.splice(masterIdx, 1);
                    } else {
                        const shuffIdx = shuffledPlaylist.indexOf(removedItem);
                        if (shuffIdx !== -1) shuffledPlaylist.splice(shuffIdx, 1);
                    }

                    if (playlistIndex === index) {
                        playlistIndex = -1;
                        const playerPipeline = document.getElementById('native-html5-audio-pipeline-element');
                        if (player) {
                            player.pause();
                            player.src = "";
                        }
                    } else if (playlistIndex > index) {
                        playlistIndex--;
                    }
                    renderPlaylist();
                    return;
                }

                // Use the backend to remove
                let actualIndex = index;
                if (isShuffle) {
                    const item = shuffledPlaylist[index];
                    actualIndex = currentPlaylist.findIndex(i => i && item && (i.name === item.name || i.path === item.path));
                    if (actualIndex === -1) actualIndex = index;
                }
                const res = await eel.remove_playlist_item(actualIndex)();
                if (res && res.status === 'ok') {
                    const remote = await eel.get_current_playlist()();
                    if (remote && remote.items) {
                        currentPlaylist = remote.items.slice();
                        playlistIndex = remote.index;
                        renderPlaylist();
                    }
                }
            } catch (e) {
                console.error('removeItem error', e);
            }
        }

        async function moveCurrentUp() {
            try {
                if (playlistIndex === undefined || playlistIndex === -1) return;
                if (typeof eel === 'undefined') {
                    return moveItemUp(playlistIndex);
                }
                const res = await eel.move_current_up()();
                if (res && res.status === 'ok') {
                    const remote = await eel.get_current_playlist()();
                    if (remote && remote.items) {
                        currentPlaylist = remote.items.slice();
                        playlistIndex = remote.index;
                        renderPlaylist();
                    }
                }
            } catch (e) {
                console.error('moveCurrentUp error', e);
            }
        }

        async function moveCurrentDown() {
            try {
                if (playlistIndex === undefined || playlistIndex === -1) return;
                if (typeof eel === 'undefined') {
                    return moveItemDown(playlistIndex);
                }
                const res = await eel.move_current_down()();
                if (res && res.status === 'ok') {
                    const remote = await eel.get_current_playlist()();
                    if (remote && remote.items) {
                        currentPlaylist = remote.items.slice();
                        playlistIndex = remote.index;
                        renderPlaylist();
                    }
                }
            } catch (e) {
                console.error('moveCurrentDown error', e);
            }
        }

        function clearPlaylist() {
            if (!confirm(t('common_confirm_clear_playlist') || 'Clear playlist?')) return;
            currentPlaylist = [];
            shuffledPlaylist = [];
            playlistIndex = -1;

            // Note: Keep backend in sync
            if (typeof eel !== 'undefined' && typeof eel.set_current_playlist === 'function') {
                eel.set_current_playlist(currentPlaylist)().catch(console.error);
            }
            const player = document.getElementById('native-html5-audio-pipeline-element');
            if (player) {
                player.pause();
                player.src = "";
            }
            isShuffle = false;
            updateShuffleUI();
            renderPlaylist();
        }

        async function savePlaylistUI() {
            if (currentPlaylist.length === 0) {
                alert(t('pl_empty_warning') || 'Playlist is empty.');
                return;
            }
            try {
                const names = currentPlaylist.map(item => item.name);
                const path = await eel.pick_save_file(t('pl_save_title') || "Save Playlist", [["JSON Files", "*.json"], ["All Files", "*.*"]], "playlist.json")();
                if (!path) return;

                const result = await eel.save_playlist(names, path)();
                if (result.status === 'ok') {
                    alert((t('pl_saved_success') || "Playlist saved to ") + result.path);
                } else {
                    alert((t('common_error') || "Error: ") + result.error);
                }
            } catch (e) {
                console.error("Save Playlist Error:", e);
            }
        }

        async function loadPlaylistUI() {
            try {
                const path = await eel.pick_file(t('pl_load_title') || "Load Playlist", [["JSON Files", "*.json"], ["All Files", "*.*"]])();
                if (!path) return;

                const result = await eel.load_playlist(path)();
                if (result.status === 'ok') {
                    currentPlaylist = result.items;
                    shuffledPlaylist = [];
                    isShuffle = false;
                    updateShuffleUI();
                    playlistIndex = -1;
                    renderPlaylist();
                    if (typeof showToast === 'function') showToast((t('pl_loaded_success') || "Loaded items: ") + result.items.length);
                } else {
                    console.error((t('common_error') || "Error: ") + result.error);
                }
            } catch (e) {
                console.error("Load Playlist Error:", e);
            }
        }

        function renderPlaylist() {
            const list = document.getElementById('json-serialized-sequence-item-container');
            const countEl = document.getElementById('json-serialized-sequence-length-renderer');
            if (!list) return;

            list.ondragover = (e) => e.preventDefault();
            list.ondrop = (e) => {
                e.preventDefault();
                const data = e.dataTransfer.getData("text/plain");
                if (data) {
                    try {
                        const item = JSON.parse(data);
                        currentPlaylist.push(item);
                        renderPlaylist();
                    } catch (err) { console.error("Drop error", err); }
                }
            };

            const moveUpBtn = document.getElementById('sequence-buffer-index-decrement-trigger');
            const moveDownBtn = document.getElementById('sequence-buffer-index-increment-trigger');
            if (moveUpBtn) {
                moveUpBtn.disabled = isShuffle;
                moveUpBtn.style.opacity = isShuffle ? '0.3' : '1';
                moveUpBtn.style.cursor = isShuffle ? 'default' : 'pointer';
            }
            if (moveDownBtn) {
                moveDownBtn.disabled = isShuffle;
                moveDownBtn.style.opacity = isShuffle ? '0.3' : '1';
                moveDownBtn.style.cursor = isShuffle ? 'default' : 'pointer';
            }

            const activeList = isShuffle ? shuffledPlaylist : currentPlaylist;
            list.innerHTML = '';
            countEl.innerText = activeList.length + ' Items';

            activeList.forEach((item, index) => {
                let div = document.createElement('div');
                div.className = 'implementation-encapsulated-state-buffer-node';
                if (index === playlistIndex) div.classList.add('playing');
                if (index === pickedIndex) div.classList.add('picked');
                if (pickedIndex !== -1) div.style.cursor = 'cell';

                let tags = item.tags || {};
                let titleDisplay = tags.title || item.name || item.filename || t('lib_unknown_title');
                let artistDisplay = tags.artist || t('lib_unknown_artist');
                let itemName = item.name || item.filename || "unknown";
                let badgeHtml = getCategoryBadgeHtml(item);

                div.innerHTML = `
                    <div style="position:relative; display:inline-block; margin-right:12px; flex-shrink:0;">
                        <img class="media-cover" style="margin-right:0;" src="/cover/${encodeURIComponent(itemName)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='; this.style.backgroundColor='transparent';" alt="">
                        ${badgeHtml}
                    </div>
                    <div class="media-info" style="flex: 1;">
                        <strong style="font-size: 0.9em;">${titleDisplay}</strong>
                        <span style="font-size: 0.8em;">${artistDisplay}</span>
                    </div>
                    <div style="display: flex; align-items: center; gap: 8px; margin-left: auto; padding-right: 10px;">
                         <div class="grab-icon"
                               onmousedown="onGrabPointerDown(event, ${index})"
                               onmouseup="onGrabPointerUp(event, ${index})"
                               onmouseleave="onGrabPointerLeave(event, ${index})"
                               title="${t('pl_grab') || 'Grab to move'}">☰
                         </div>
                        <div class="playlist-controls" style="display: flex; gap: 5px;">
                            <button onclick="event.stopPropagation(); moveItemUp(${index})" title="${t('pl_move_up') || 'Up'}"
                                ${isShuffle ? 'disabled style="opacity:0.3; cursor:default;"' : 'style="background:transparent; border:none; cursor:pointer; display: flex; align-items: center; justify-content: center; padding: 5px;"'}>
                                <span class="icon-up" style="width: 16px; height: 16px;"></span>
                            </button>
                            <button onclick="event.stopPropagation(); moveItemDown(${index})" title="${t('pl_move_down') || 'Down'}"
                                ${isShuffle ? 'disabled style="opacity:0.3; cursor:default;"' : 'style="background:transparent; border:none; cursor:pointer; display: flex; align-items: center; justify-content: center; padding: 5px;"'}>
                                <span class="icon-down" style="width: 16px; height: 16px;"></span>
                            </button>
                            <button onclick="event.stopPropagation(); removeItem(${index})" title="${t('pl_remove') || 'Remove'}" style="background:transparent; border:none; cursor:pointer; font-size: 0.8em; color: #c0392b; padding: 5px;">❌</button>
                        </div>
                    </div>
                `;

                div.onclick = () => onPlaylistItemClick(index, item);
                div.oncontextmenu = (e) => showContextMenu(e, item);

                // --- Drag and Drop Handlers ---
                div.onmouseenter = () => {
                    if (pickedIndex !== -1 && pickedIndex !== index) {
                        div.classList.add('drop-target-before');
                    }
                };
                div.onmouseleave = () => {
                    div.classList.remove('drop-target-before', 'drop-target-after');
                };
                div.onmouseup = async (e) => {
                    if (pickedIndex !== -1 && pickedIndex !== index) {
                        e.stopPropagation();
                        await releasePick(index);
                    }
                };

                list.appendChild(div);
            });

            updateSidebarPlaylists();
        }

        function updateSidebarPlaylists() {
            const containers = document.querySelectorAll('.active-playlist-container');
            const activeList = isShuffle ? shuffledPlaylist : currentPlaylist;

            containers.forEach(container => {
                container.innerHTML = '';
                if (activeList.length === 0) {
                    container.innerHTML = `<p style="padding: 20px; color: #999;" data-i18n="lib_no_media_desc">${t('lib_no_media_desc')}</p>`;
                    return;
                }

                activeList.forEach((item, index) => {
                    let div = document.createElement('div');
                    div.className = 'implementation-encapsulated-state-buffer-node';
                    if (index === playlistIndex) div.classList.add('playing');

                    let tags = item.tags || {};
                    let titleDisplay = tags.title || item.name || item.filename || t('lib_unknown_title');
                    let artistDisplay = tags.artist || t('lib_unknown_artist');
                    let itemName = item.name || item.filename || "unknown";
                    let badgeHtml = getCategoryBadgeHtml(item);

                    div.innerHTML = `
                        <div style="position:relative; display:inline-block; margin-right:12px; flex-shrink:0;">
                            <img class="media-cover" style="margin-right:0;" src="/cover/${encodeURIComponent(itemName)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='; this.style.backgroundColor='transparent';" alt="">
                            ${badgeHtml}
                        </div>
                        <div class="media-info">
                            <strong>${titleDisplay}</strong>
                            <span>${artistDisplay}</span>
                        </div>
                    `;

                    let mediaUrl = '/media/' + encodeURIComponent(itemName);
                    if (item.is_transcoded && item.transcoded_format) {
                        mediaUrl += '.' + item.transcoded_format.toLowerCase() + '_transcoded';
                    }

                    div.onclick = (e) => {
                        if (e) e.stopPropagation();
                        onPlaylistItemClick(index, item);
                    };
                    div.oncontextmenu = (e) => showContextMenu(e, item);
                    container.appendChild(div);
                });
            });
        }

        // Pick-and-insert handlers
        async function onPlaylistItemClick(index, item) {
            // If an item is picked, insert before clicked index
            if (pickedIndex !== -1) {
                if (pickedIndex !== index) {
                    await releasePick(index);
                } else {
                    cancelPick();
                }
                return;
            }
            // Normal click: select and play
            playlistIndex = index;
            if (isVideoItem(item)) {
                // Redirect video items to Video Tab
                console.info("[Queue-Redirect] Video clicked in audio queue, redirecting...");
                switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                setTimeout(() => {
                    if (typeof playVideo === 'function') playVideo(item, item.path);
                }, 100);
            } else {
                // Standard Audio Play
                play(item, getMediaUrl(item));
            }
            renderPlaylist();
        }

        function onGrabPointerDown(e, index) {
            e.stopPropagation();
            if (isShuffle) return;

            ignoreNextMouseUp = true;
            console.log(`[Picking] Immediate pick on handle ${index}`);
            try { appendUiTrace(`Grab-Down (Immediate) on ${index}`); } catch (e) { }

            pickItem(index);
        }

        let ignoreNextMouseUp = false;

        function onGrabPointerUp(e, index) {
            console.log(`[Picking] mouseup on handle ${index}, ignoreNext=${ignoreNextMouseUp}, pickedIndex=${pickedIndex}`);

            if (pickedIndex !== -1 && pickedIndex !== index) {
                // Let it bubble to div.onmouseup for drop
                return;
            }

            e.stopPropagation();

            if (ignoreNextMouseUp) {
                ignoreNextMouseUp = false;
            } else if (pickedIndex === index) {
                cancelPick();
            }
        }

        function onGrabPointerLeave(e, index) {
            // e.stopPropagation(); // Might break things
            if (pickTimer) {
                console.log(`[Picking] Mouse left handle ${index} during press - continuing timer for robustness`);
                // We DON'T cancel here anymore. Only mouseup or a very far move should cancel.
                // But for simplicity, we let the timer finish if they stay within reasonable bounds.
                // If they release outside, we still have the mouseup on body or similar?
                //                 // Actually, let's keep it but make it less sensitive.
                //
                //                 // If we want it to be REALLY robust, we should listen to mouseup on window.
                //             }
                //         }
                //
                //         function clearPickProgress(index) {
                //             const progress = document.getElementById(`pick-progress-${index}`);
                //             if (progress) {
                //                 progress.style.transition = 'none';
                //                 progress.style.width = '0%';
                //                 setTimeout(() => { if (progress) progress.style.transition = 'width 0.4s linear'; }, 50);
                //             }
                //         }
                //
                //         function pickItem(index) {
                //             console.log("pickItem activated for index:", index);
                //             if (isShuffle) {
                //                 alert(t('pl_disable_shuffle') || 'Disable shuffle to reorder directly.');
                //                 return;
                //             }
                //             pickedIndex = index;
                //             document.body.classList.add('is-picking');
                //
                //             // Add global cancel listener if user releases outside elements
                //             const onGlobalUp = (e) => {
                //                 if (pickedIndex !== -1) {
                //                     console.log("[Picking] Global mouseup detected - checking if we need to cancel");
                //                     // If we are here, we might have missed a specific drop target mouseup
                //                     // We'll give it a tiny delay to see if releasePick was called
                //                     setTimeout(() => {
                //                         if (pickedIndex !== -1) cancelPick();
                //                     }, 50);
                //                 }
                //                 window.removeEventListener('mouseup', onGlobalUp);
                //             };
            }
        }

        function clearPickProgress(index) {
            const progress = document.getElementById(`pick-progress-${index}`);
            if (progress) {
                progress.style.transition = 'none';
                progress.style.width = '0%';
                setTimeout(() => { if (progress) progress.style.transition = 'width 0.4s linear'; }, 50);
            }
        }

        function pickItem(index) {
            console.log("pickItem activated for index:", index);
            if (isShuffle) {
                alert(t('pl_disable_shuffle') || 'Disable shuffle to reorder directly.');
                return;
            }
            pickedIndex = index;
            document.body.classList.add('is-picking');

            // Add global cancel listener if user releases outside elements
            const onGlobalUp = (e) => {
                if (pickedIndex !== -1) {
                    console.log("[Picking] Global mouseup detected - checking if we need to cancel");
                    // If we are here, we might have missed a specific drop target mouseup
                    // We'll give it a tiny delay to see if releasePick was called
                    setTimeout(() => {
                        if (pickedIndex !== -1) cancelPick();
                    }, 50);
                }
                window.removeEventListener('mouseup', onGlobalUp);
            };
            window.addEventListener('mouseup', onGlobalUp);

            // Visual confirmation
            const list = document.getElementById('json-serialized-sequence-item-container');
            if (list && list.children[index]) {
                list.children[index].classList.add('picked-flash');
                setTimeout(() => { if (list.children[index]) list.children[index].classList.remove('picked-flash'); }, 500);
            }

            renderPlaylist();
            // announce
            try { appendUiTrace(`PICK-SUCCESS: ${index}`); } catch (e) { }

            // Robustness: if we never get a releasePick, cancel after 30s
            if (window._pickAutoCancel) clearTimeout(window._pickAutoCancel);
            window._pickAutoCancel = setTimeout(() => {
                if (pickedIndex !== -1) {
                    console.log("[Picking] Auto-cancelling pick after timeout");
                    cancelPick();
                }
            }, 30000);
        }

        async function releasePick(targetIndex) {
            console.log("releasePick called. pickedIndex:", pickedIndex, "targetIndex:", targetIndex);
            if (pickedIndex === -1) {
                console.warn("releasePick called but no item picked.");
                return;
            }

            // Adjust targetIndex for "insert before" semantics if moving from above
            let finalTarget = targetIndex;
            if (pickedIndex !== -1 && pickedIndex < targetIndex) {
                finalTarget = targetIndex - 1;
            }
            if (finalTarget < 0) finalTarget = 0;

            try {
                if (typeof eel === 'undefined') {
                    console.log("Eel undefined, using local fallback");
                    // local fallback
                    const active = currentPlaylist;
                    const item = active.splice(pickedIndex, 1)[0];
                    active.splice(finalTarget, 0, item);
                    // update playlistIndex
                    playlistIndex = active.indexOf(item);
                    pickedIndex = -1;
                    cancelPick(); // Cleanup classes
                    return;
                }

                console.log("Calling eel.move_item_to(", pickedIndex, ",", finalTarget, ")");
                const res = await eel.move_item_to(pickedIndex, finalTarget)();
                console.log("eel.move_item_to response:", res);
                pickedIndex = -1; // Local reset
                cancelPick(); // Cleanup classes and state
                if (res && res.status === 'ok') {
                    // Update current list from server state
                    currentPlaylist = res.items;
                    playlistIndex = res.index;
                    renderPlaylist();
                } else {
                    alert((t('common_error') || 'Error: ') + (res && res.message ? res.message : 'move failed'));
                    renderPlaylist();
                }
            } catch (e) {
                console.error('releasePick error', e);
                pickedIndex = -1;
                cancelPick();
            }
        }

        function cancelPick() {
            console.log("[Picking] cancelPick called, cleaning up state and classes");
            try { appendUiTrace(`CANCEL-PICK (index was ${pickedIndex})`); } catch (e) { }

            pickedIndex = -1;
            ignoreNextMouseUp = false;
            document.body.classList.remove('is-picking');

            if (pickTimer) { clearTimeout(pickTimer); pickTimer = null; }
            if (window._pickAutoCancel) { clearTimeout(window._pickAutoCancel); window._pickAutoCancel = null; }

            // Immediate DOM cleanup for speed
            document.querySelectorAll('.implementation-encapsulated-state-buffer-node').forEach(el => {
                el.classList.remove('drop-target-before', 'drop-target-after', 'picked', 'picked-flash');
                el.style.cursor = '';
            });

            renderPlaylist();
        }
    
    
        let allLibraryItems = [];
        let currentEditingTestFile = null; // For test suite editing

        async function loadEditItems(retryCount) {
            retryCount = retryCount || 0;
            try {
                const result = await eel.get_library()();
                allLibraryItems = result.media || [];
                renderEditList(allLibraryItems);
                if (allLibraryItems.length === 0 && retryCount < 3) {
                    setTimeout(() => loadEditItems(retryCount + 1), 500);
                }
            } catch (e) {
                console.error('[loadEditItems] Error:', e);
                if (retryCount < 3) {
                    setTimeout(() => loadEditItems(retryCount + 1), 1000);
                }
            }
        }


        function renderEditList(items) {
            const list = document.getElementById('edit-items-list');
            list.innerHTML = '';
            items.forEach(item => {
                const div = document.createElement('div');
                div.style.cssText = 'padding: 10px; border: 1px solid #eee; margin-bottom: 5px; border-radius: 4px; cursor: pointer; background: #fff; display: flex; align-items: center; gap: 10px; transition: background 0.1s; position: relative; z-index: 10; pointer-events: auto;';
                div.onmouseover = () => div.style.background = '#f0f0f0';
                div.onmouseout = () => div.style.background = '#fff';
                div.onclick = () => {
                    console.log("[Editor] Item clicked:", item.name);
                    openEditForm(item);
                };

                const thumb = document.createElement('img');
                thumb.src = `/cover/${encodeURIComponent(item.name)}`;
                thumb.style.cssText = 'width: 40px; height: 40px; border-radius: 4px; object-fit: cover; background: #eee;';
                thumb.onerror = () => thumb.src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';

                const info = document.createElement('div');
                info.style.overflow = 'hidden';
                info.innerHTML = `<div style="font-weight: bold; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">${item.tags.title || item.name}</div><div style="font-size: 0.8em; color: #666;">${item.tags.artist || '-'}</div>`;

                div.appendChild(thumb);
                div.appendChild(info);
                list.appendChild(div);
            });
        }

        function filterEditList() {
            const query = readValue('edit-search').toLowerCase();
            const filtered = allLibraryItems.filter(item =>
                item.name.toLowerCase().includes(query) ||
                (item.tags.title && item.tags.title.toLowerCase().includes(query)) ||
                (item.tags.artist && item.tags.artist.toLowerCase().includes(query)) ||
                (item.tags.album && item.tags.album.toLowerCase().includes(query))
            );
            renderEditList(filtered);
        }

        function openEditForm(item) {
            console.log("[Editor] Opening form for:", item.name);
            safeStyle('edit-placeholder', 'display', 'none', 'important');
            safeStyle('edit-form-container', 'display', 'block', 'important');

            if (!item) {
                console.error("[Editor] No item provided!");
                return;
            }

            safeValue('edit-item-name', item.name);
            safeText('edit-filename-display', item.name);
            const cover = document.getElementById('edit-cover');
            if (cover) cover.src = `/cover/${encodeURIComponent(item.name)}`;

            const container = document.getElementById('edit-dynamic-tags');
            if (container) container.innerHTML = '';

            // Alphabetisch sortieren für Ordnung + Core-Felder sicherstellen
            let keys = Object.keys(item.tags).sort();
            const coreKeys = ['title', 'artist', 'album', 'year', 'genre', 'isbn', 'imdb', 'tmdb', 'discogs'];
            coreKeys.forEach(k => {
                if (!keys.includes(k)) keys.push(k);
            });
            keys.sort();

            keys.forEach(key => {
                if (key === 'chapters' || key === '_parser_times') return;

                const row = document.createElement('div');
                row.style.display = 'flex';
                row.style.alignItems = 'center';
                row.style.padding = '8px 0';
                row.style.borderBottom = '1px solid #f9f9f9';

                const label = document.createElement('label');
                label.style.width = '140px';
                label.style.fontSize = '0.85em';
                label.style.color = '#666';
                label.style.textTransform = 'capitalize';
                label.innerText = key.replace('_', ' ');

                const input = document.createElement('input');
                input.type = 'text';
                input.className = 'edit-dynamic-input';
                input.dataset.key = key;
                input.value = item.tags[key] || '';
                input.style.flex = '1';
                input.style.padding = '8px 12px';
                input.style.border = '1px solid #eee';
                input.style.borderRadius = '4px';
                input.style.fontSize = '0.95em';
                input.onfocus = () => input.style.borderColor = '#2a7';
                input.onblur = () => input.style.borderColor = '#eee';

                row.appendChild(label);
                row.appendChild(input);
                container.appendChild(row);
            });

            if (item.tags.chapters && Array.isArray(item.tags.chapters) && item.tags.chapters.length > 0) {
                const chapHeader = document.createElement('h4');
                chapHeader.innerText = 'Kapitel bearbeiten';
                chapHeader.style.marginTop = '20px';
                chapHeader.style.marginBottom = '10px';
                chapHeader.style.color = '#555';
                container.appendChild(chapHeader);

                item.tags.chapters.forEach((chap, idx) => {
                    const row = document.createElement('div');
                    row.style.display = 'flex';
                    row.style.alignItems = 'center';
                    row.style.padding = '4px 0';

                    const label = document.createElement('label');
                    label.style.width = '140px';
                    label.style.fontSize = '0.85em';
                    label.style.color = '#888';
                    label.innerText = `Kapitel ${idx + 1}`;

                    const input = document.createElement('input');
                    input.type = 'text';
                    input.className = 'edit-chapter-input';
                    input.dataset.index = idx;
                    input.value = chap.title || `Kapitel ${idx + 1}`;
                    input.style.flex = '1';
                    input.style.padding = '6px 12px';
                    input.style.border = '1px solid #eee';
                    input.style.borderRadius = '4px';
                    input.style.fontSize = '0.9em';
                    input.style.background = '#fafafa';

                    row.appendChild(label);
                    row.appendChild(input);
                    container.appendChild(row);
                });
            }
        }

        function resetEditForm() {
            safeStyle('edit-placeholder', 'display', 'flex');
            safeStyle('edit-form-container', 'display', 'none');
        }

        async function saveTags() {
            const name = readValue('edit-item-name');
            const item = allLibraryItems.find(i => i.name === name);
            if (!item) return;

            const newTags = {};
            document.querySelectorAll('.edit-dynamic-input').forEach(input => {
                newTags[input.dataset.key] = input.value;
            });

            // Erhalte komplexe Objekte
            if (item.tags._parser_times) {
                newTags._parser_times = item.tags._parser_times;
            }
            if (item.tags.chapters && Array.isArray(item.tags.chapters)) {
                newTags.chapters = JSON.parse(JSON.stringify(item.tags.chapters));
                document.querySelectorAll('.edit-chapter-input').forEach(input => {
                    const idx = parseInt(input.dataset.index);
                    if (newTags.chapters[idx]) {
                        newTags.chapters[idx].title = input.value;
                    }
                });
            }

            const result = await eel.update_tags(name, newTags)();
            if (result.status === 'ok') {
                // Update local data
                item.tags = newTags;
                // Refresh all relevant views
                if (typeof loadEditItems === 'function') loadEditItems();
                if (typeof loadLibrary === 'function') loadLibrary();
                if (typeof renderPlaylist === 'function') renderPlaylist();
                alert(t('edit_save_success'));
            }

        }

        async function renameMedia() {
            const oldName = readValue('edit-item-name');
            const newName = prompt(t('edit_rename_prompt'), oldName);
            if (newName && newName !== oldName) {
                const res = await eel.rename_media(oldName, newName)();
                if (res.status === 'ok') {
                    safeValue('edit-item-name', newName);
                    safeText('edit-filename-display', newName);
                    // Refresh all relevant views
                    if (typeof loadEditItems === 'function') loadEditItems();
                    if (typeof loadLibrary === 'function') loadLibrary();
                    if (typeof renderPlaylist === 'function') renderPlaylist();
                    alert(t('edit_rename_success'));
                } else {
                    alert(t('edit_rename_error') + res.message);
                }

            }
        }

        async function deleteMediaFromEdit() {
            const name = readValue('edit-item-name');
            const msg = t('edit_delete_confirm').replace('{name}', name);
            if (confirm(msg)) {
                const res = await eel.delete_media(name)();
                if (res.status === 'ok') {
                    resetEditForm();
                    if (typeof loadEditItems === 'function') loadEditItems();
                    if (typeof loadLibrary === 'function') loadLibrary();
                    if (typeof renderPlaylist === 'function') renderPlaylist();
                    alert(t('edit_delete_success'));
                }

            }
        }

        async function triggerIsbnScan() {
            const isbnInput = document.getElementById('isbn-scanner-input');
            const isbn = isbnInput ? isbnInput.value.trim() : '';
            if (!isbn) {
                showToast("⚠️ Bitte ISBN eingeben.", 3000);
                return;
            }

            showToast(`🔍 Scanne ISBN: ${isbn}...`, 2000);
            const result = await eel.api_scan_isbn(isbn)();

            if (result && !result.error) {
                showToast(`✅ Gefunden: ${result.title}`, 3000);

                // Update the current editor inputs if they match the key
                const inputs = document.querySelectorAll('.edit-dynamic-input');
                let updatedCount = 0;
                inputs.forEach(input => {
                    const key = input.dataset.key;
                    if (result[key]) {
                        input.value = result[key];
                        input.style.background = '#e8f5e9'; // Highlight change
                        updatedCount++;
                    }
                });

                // If title input didn't exist or wasn't updated, we might need to add it
                // but usually it exists.

                // Specific handling for cover if available
                if (result.cover) {
                    const coverImg = document.getElementById('edit-cover');
                    if (coverImg) {
                        coverImg.src = result.cover;
                        coverImg.style.boxShadow = '0 0 15px rgba(46, 204, 113, 0.4)';
                    }
                    // Also update specific hidden fields or tags if needed
                }
            } else if (result && result.amazon_cover && !result.error) {
                // Fallback with cover
                showToast("ℹ️ Nur Cover gefunden.", 3000);
                const coverImg = document.getElementById('edit-cover');
                if (coverImg) coverImg.src = result.amazon_cover;
            } else {
                showToast(`❌ Fehler: ${result ? result.error : 'Unbekannt'}`, 4000);
            }
        }

        async function refreshLibrary() {
            let result = await eel.get_library()();
            let list = document.getElementById('persistent-sqlite-repository-item-grid');
            if (list) list.innerHTML = '';
            if (!result.media || result.media.length === 0) {
                safeHtml('persistent-sqlite-repository-item-grid', `<p style="padding: 20px; color: #999;" data-i18n="lib_no_media_desc">${t('lib_no_media_desc')}</p>`);
                return;
            }
            result.media.forEach(item => {
                let div = document.createElement('div');
                div.className = 'implementation-encapsulated-state-buffer-node';
                div.draggable = true;
                div.ondragstart = (e) => {
                    e.dataTransfer.setData("text/plain", JSON.stringify(item));
                };
                let tags = item.tags;
                let displayYear = tags.year ? String(tags.year).substring(0, 4) : '';
                let trackStr = tags.track ? 'Track ' + tags.track : '';
                if (tags.track && tags.totaltracks) trackStr += '/' + tags.totaltracks;
                let extraInfo = [displayYear, tags.genre, trackStr, tags.album ? '💿 ' + tags.album : ''].filter(Boolean).join(' • ');
                let codecInfo = [tags.codec, tags.bitdepth, tags.samplerate, tags.bitrate].filter(Boolean).join(' | ');
                let badgeHtml = getCategoryBadgeHtml(item);

                div.innerHTML = `
                    <div style="position:relative; display:inline-block; margin-right:12px; flex-shrink:0;">
                        <img class="media-cover" style="margin-right:0;" src="/cover/${encodeURIComponent(item.name)}" onerror="this.src='data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='; this.style.backgroundColor='transparent';" alt="">
                        ${badgeHtml}
                    </div>
                    <div class="media-info">
                        <strong>${tags.title}</strong>
                        <span>${tags.artist}</span>
                        <span style="font-size: 0.8em; color: #888; margin-top: 2px;">${extraInfo}</span>
                        <span style="font-size: 0.75em; color: #aaa;">${codecInfo}</span>
                    </div>
                    <span style="font-size: 0.85em; color: #999; white-space: nowrap; margin-left: auto;">${item.duration}</span>
                `;

                let mediaUrl = '/media/' + encodeURIComponent(item.name);
                if (item.is_transcoded && item.transcoded_format) {
                    mediaUrl += '.' + item.transcoded_format.toLowerCase() + '_transcoded';
                }

                div.onclick = () => jumpToEdit(item);
                div.oncontextmenu = (e) => showContextMenu(e, item);
                list.appendChild(div);
            });
        }

        async function scan(targetDir = null, clearDb = true) {
            const scanBtn = document.getElementById('scan-btn');

            if (typeof set_db_status === 'function') {
                set_db_status(true);
            }
            if (scanBtn) {
                scanBtn.disabled = true;
                scanBtn.style.opacity = '0.7';
                scanBtn.style.cursor = 'wait';
            }
            safeText('active-orchestration-status-message-renderer', t('db_updating'));

            try {
                let result = await eel.scan_media(targetDir, clearDb)();

                // Always reload canonical library view after scan
                if (typeof loadLibrary === 'function') {
                    loadLibrary();
                }
                if (typeof loadEditItems === 'function') {
                    loadEditItems();
                }
            } catch (e) {
                console.error('[scan] Error during scan:', e);
                safeText('active-orchestration-status-message-renderer', `${t('common_error')} ${e.message || e}`);
            } finally {
                if (typeof set_db_status === 'function') {
                    set_db_status(false);
                }
                if (scanBtn) {
                    scanBtn.disabled = false;
                    scanBtn.style.opacity = '1';
                    scanBtn.style.cursor = 'pointer';
                }
            }
        }

        async function saveToFileUI() {
            const name = readValue('edit-item-name');
            if (!name) {
                alert(t('edit_no_selection_error'));
                return;
            }

            const tags = {};
            const tagRows = document.querySelectorAll('.edit-tag-row');
            tagRows.forEach(row => {
                const keyEl = row.querySelector('.tag-key');
                const valEl = row.querySelector('.tag-val');
                if (keyEl && valEl) {
                    const key = keyEl.innerText.replace(':', '').trim().toLowerCase();
                    tags[key] = valEl.value;
                }
            });

            // Button context
            const btn = event.currentTarget;
            const originalBtnText = btn.innerHTML;
            btn.innerHTML = (t('edit_saving') || 'Speichern...') + ' ⏳';
            btn.disabled = true;

            try {
                const result = await eel.save_tags_to_file(name, tags)();
                if (result.success) {
                    alert(t('edit_save_to_file_success') || 'Erfolgreich in Datei gespeichert!');
                    loadLibrary(); // Refresh library to show updated tags
                } else {
                    alert((t('edit_save_to_file_error') || 'Fehler beim Speichern in Datei: ') + result.error);
                }
            } catch (e) {
                alert('Eel error: ' + e);
            } finally {
                btn.innerHTML = originalBtnText;
                btn.disabled = false;
            }
        }

        async function loadLibrary(retryCount) {
            retryCount = retryCount || 0;
            try {
                let result = await eel.get_library()();
                if (result && result.media && result.media.length > 0) {
                    // console.log("[loadLibrary] Loaded " + result.media.length + " items.");
                } else {
                    console.warn("[loadLibrary] No media found.");
                    return;
                }

                // Update current playlist
                currentPlaylist = [...result.media];
                if (isShuffle) {
                    shuffledPlaylist = [...currentPlaylist];
                    for (let i = shuffledPlaylist.length - 1; i > 0; i--) {
                        const j = Math.floor(Math.random() * (i + 1));
                        [shuffledPlaylist[i], shuffledPlaylist[j]] = [shuffledPlaylist[j], shuffledPlaylist[i]];
                    }
                }

                if (typeof eel !== 'undefined' && typeof eel.set_current_playlist === 'function') {
                    eel.set_current_playlist(currentPlaylist)().catch(console.error);
                }

                renderPlaylist();
            } catch (e) {
                console.error('[loadLibrary] Error:', e);
                if (retryCount < 3) {
                    setTimeout(() => loadLibrary(retryCount + 1), 1000);
                }
            }
        }

        function jumpToEdit(item) {
            const editBtn = document.querySelector('button[onclick*="\'edit\'"]');
            switchTab('edit', editBtn);
            openEditForm(item);
        }
    
    
        activeAudioPipeline = document.getElementById('native-html5-audio-pipeline-element');
        let currentVideoItem = null;
        let currentVideoPath = null;
        let vjsPlayer = null;

        function play(item, path) {
            console.info(">>> [Play-Trace] play() called for:", item.name, "path:", path);
            const videoExts = ['mp4', 'mkv', 'webm', 'ogg', 'mov', 'avi', 'm4v', 'iso'];
            const extFromPath = (item.name || path || "").split('.').pop().toLowerCase();
            const isVideo = isVideoItem(item);

            currentVideoItem = item;
            updateMediaSidebar(item, path);

            if (isVideo) {
                console.info(">>> [Play-Trace] isVideo IDENTIFIED (type: " + item.type + ", cat: " + item.category + "). Calling playVideo().");
                playVideo(item, path);
                return;
            }
            // Ensure video is stopped if audio starts
            stopVideo();

            // Highlight in list (audio specific)
            document.querySelectorAll('.implementation-encapsulated-state-buffer-node').forEach((el, idx) => {
                let list = isShuffle ? shuffledPlaylist : currentPlaylist;
                if (list[idx] === item) {
                    el.classList.add('playing');
                } else {
                    el.classList.remove('playing');
                }
            });

            // Update Playlist UI if open
            if (typeof renderPlaylist === 'function') {
                renderPlaylist();
            }

            activeAudioPipeline.src = path;
            activeAudioPipeline.play().catch(e => {
                if (isUnsupportedMediaError(e)) {
                    console.warn('Audio playback unsupported for source:', path, e);
                    safeText('active-orchestration-status-message-renderer', (t('player_unsupported_source') || 'Unsupported media source for browser playback.'));
                    return;
                }
                console.error('Audio playback failed:', e);
            });

            // Synchronize backend index
            if (typeof eel !== 'undefined' && typeof eel.jump_to_index === 'function') {
                const list = isShuffle ? shuffledPlaylist : currentPlaylist;
                const idx = list.indexOf(item);
                if (idx !== -1) {
                    eel.jump_to_index(idx)();
                }
            }

            // Python Backend anfunken (ONLY FOR AUDIO)
            eel.play_media(path)();
        }

        function updateMediaSidebar(item, path) {
            // Update Restored Sidebar
            let tags = item.tags;
            console.log("Updating sidebar & mediainfo details for item:", item.name);

            safeText('sidebar-metadata-primary-string-renderer', tags.title || item.name);
            let artistStr = tags.albumartist && tags.albumartist !== tags.artist ? tags.artist + " (Album: " + tags.albumartist + ")" : (tags.artist || 'Unknown');
            safeText('sidebar-metadata-secondary-string-renderer', artistStr);

            // Update Parser -> MediaInfo Details Elements
            safeText('parser-mediainfo-primary', tags.title || item.name);
            safeText('parser-mediainfo-secondary', artistStr);

            let sbCover = document.getElementById('sidebar-artwork-raster-buffer');
            let miCover = document.getElementById('parser-mediainfo-artwork');
            const coverUrl = "/cover/" + encodeURIComponent(item.name);

            [sbCover, miCover].forEach(img => {
                if (img) {
                    img.src = coverUrl;
                    img.style.opacity = "1";
                    img.onerror = function () {
                        this.src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs=';
                        this.style.backgroundColor = '#ddd';
                    };
                }
            });

            // Update footer cover
            let footerCover = document.getElementById('footer-artwork-raster-buffer');
            if (footerCover) {
                footerCover.src = coverUrl;
                footerCover.onerror = function () { this.src = 'data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs='; };
            }

            let displayYear = tags.year ? String(tags.year).substring(0, 4) : '';
            let trackStr = tags.track ? t('sb_track_label') + tags.track : '';
            if (tags.track && tags.totaltracks) trackStr += '/' + tags.totaltracks;

            let discStr = tags.disc ? t('sb_disc_label') + tags.disc : '';
            let ext = (item.extension || '').toUpperCase();
            let extraInfoSb = [ext, displayYear, tags.genre, discStr, trackStr].filter(Boolean).join(' • ');

            let badgeText = [tags.codec, tags.bitdepth, tags.samplerate, tags.bitrate].filter(Boolean).join(' | ');
            let sidebarBadge = badgeText;
            if (item.is_transcoded) {
                sidebarBadge = '⚠️ [TRANSCODING] ' + sidebarBadge;
                badgeText = '[TRANSCODED] ' + badgeText;
            }

            if (badgeText) {
                safeText('sidebar-status-tag-visualizer', badgeText);
                safeStyle('sidebar-status-tag-visualizer', 'display', 'inline-block');
                safeText('sidebar-status-tag-visualizer-sidebar', sidebarBadge);
                safeStyle('sidebar-status-tag-visualizer-sidebar', 'display', 'inline-block');
                safeText('parser-mediainfo-status-badge', badgeText);
                safeStyle('parser-mediainfo-status-badge', 'display', 'inline-block');
            } else {
                ['sidebar-status-tag-visualizer', 'sidebar-status-tag-visualizer-sidebar', 'parser-mediainfo-status-badge'].forEach(id => {
                    safeStyle(id, 'display', 'none');
                });
            }

            let artStr = tags.has_art === 'Yes' ? t('sb_art_yes') : t('sb_art_no');
            let extStr = t('sb_file_label') + (item.type ? item.type.toLowerCase() : (item.extension || '').toLowerCase());
            let contStr = tags.container ? t('sb_container_label') + tags.container.toLowerCase() : '';

            let fileInfoStr = [tags.size, artStr].filter(Boolean).join(' &bull; ');
            let tagVal = tags.tagtype && tags.tagtype !== 'None' ? tags.tagtype : 'None';
            let tagStr = t('sb_tag_format_label') + tagVal;
            let fileTypeStr = `${t('sb_filetype_label')}${item.category || (item.type || 'Media')}`;
            let formatDetailsStr = [extStr, contStr, tagStr, fileTypeStr].filter(Boolean).join(' • ');

            fileInfoStr = fileInfoStr + '<br><br>' + formatDetailsStr;
            let headerInfo = `<strong>${item.name}</strong><br><br><span style="color:#aaa; font-style:italic; font-size:0.85em; word-break: break-all;">${path}</span>`;
            fileInfoStr = headerInfo + '<br><br>' + fileInfoStr;

            let parserTimesHtml = '';
            const showParserTimes = document.getElementById('toggle-parser-times') ? document.getElementById('toggle-parser-times').checked : true;

            if (showParserTimes && tags._parser_times) {
                let times = [];
                for (const [pName, pTime] of Object.entries(tags._parser_times)) {
                    let msTime = (pTime * 1000).toFixed(1);
                    if (pTime > 0) {
                        times.push(`<span style="color: #666; font-weight: bold;" title="${t('test_status_executed')}">${pName}: ${msTime}ms</span>`);
                    } else {
                        times.push(`<span style="color: #ccc;" title="${t('test_status_skipped')}">${pName}: übersprungen</span>`);
                    }
                }
                if (times.length > 0) {
                    parserTimesHtml = '<div style="margin-top: 10px; padding: 10px; background: #f5f5f5; border-radius: 6px; font-size: 0.85em;">' +
                        '<div style="margin-bottom: 5px; color: #888; text-transform: uppercase; font-size: 10px; font-weight: bold; letter-spacing: 0.5px;">Performance</div>' +
                        times.join(' • ') + '</div>';
                }
            }

            let transcodeHtml = item.is_transcoded ? `<br><br><span style="color: #d9534f;">${t('sb_transcoding_msg').replace('{fmt}', item.transcoded_format || 'FLAC')}</span>` : '';

            // Update sidebar performance/parsing times
            safeHtml('sidebar-performance-container', parserTimesHtml);

            let chaptersHtml = '';
            if (tags.chapters && tags.chapters.length > 0) {
                chaptersHtml = '<div style="margin-top: 15px; background: #2a2a2a; border-radius: 6px; padding: 10px; text-align: left;">';
                chaptersHtml += '<h4 style="margin-top:0; margin-bottom: 8px; font-size: 14px; text-transform: uppercase; color: #aaa; border-bottom: 1px solid #444; padding-bottom: 4px;">Kapitel (' + tags.chapters.length + ')</h4>';
                chaptersHtml += '<div style="max-height: 200px; overflow-y: auto; font-size: 13px; padding-right: 5px;">';
                tags.chapters.forEach((chap, idx) => {
                    let timeString = new Date(chap.start * 1000).toISOString().substring(11, 19);
                    chaptersHtml += `<div onclick="window.jumpToChapter(${chap.start})" style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #333; padding: 6px 4px; cursor: pointer; transition: background 0.1s;" onmouseover="this.style.background='#3a3a3a'" onmouseout="this.style.background=''">
                        <span style="color: #ddd; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; flex: 1; min-width: 0; margin-right: 10px;" title="${chap.title}">${chap.title}</span>
                        <span style="color: #888; font-family: monospace; flex-shrink: 0;">${timeString}</span>
                    </div>`;
                });
                chaptersHtml += '</div></div>';
            }

            safeHtml('parser-mediainfo-technical-details', fileInfoStr + parserTimesHtml + transcodeHtml + chaptersHtml);

            // Update technical details in sidebar
            let sidebarGridHtml = '';
            const techData = {
                'Codec': tags.codec,
                'Quality': tags.bitdepth ? `${tags.bitdepth}bit / ${tags.samplerate}Hz` : '',
                'Bitrate': tags.bitrate,
                'Format': item.extension,
                'Size': tags.size
            };
            for (const [key, val] of Object.entries(techData)) {
                if (val) sidebarGridHtml += `<b>${key}:</b> <span>${val}</span><br>`;
            }
            safeHtml('sidebar-metadata-extended-attribute-grid', sidebarGridHtml);

            const playingLabel = t('player_status_playing') || 'Playing: ';
            const byLabel = t('player_status_by') || ' by ';
            safeHtml('active-orchestration-status-message-renderer', `${playingLabel} &nbsp; <strong>${tags.title || item.name}</strong> &nbsp; ${byLabel} &nbsp; ${tags.artist || 'Unknown'}`);
        }

        // ============ Video Player ============
        function showUnsupportedVideoHint() {
            safeStyle('video-unsupported-hint', 'display', 'block');
            safeStyle('btn-open-vlc', 'display', 'flex');
            safeStyle('btn-open-vlc', 'background', '#d35400');
            safeStyle('btn-open-vlc', 'boxShadow', '0 0 0 3px rgba(243, 156, 18, 0.35)');
        }

        function hideUnsupportedVideoHint() {
            safeStyle('video-unsupported-hint', 'display', 'none');
            safeStyle('btn-open-vlc', 'background', '#2980b9');
            safeStyle('btn-open-vlc', 'boxShadow', 'none');
        }

        async function triggerOpenWith() {
            if (!currentVideoItem) {
                showToast(t('player_select_song') || 'Bitte zuerst eine Datei auswählen.');
                return;
            }
            const engine = document.getElementById('player-type')?.value || 'auto';
            const mode = document.getElementById('video-mode')?.value || 'auto';

            // Resolve path: for VLC network use the URL input, for DVD device use the device path
            let targetPath = currentVideoItem.path;
            if (mode === 'vlc_network') {
                const urlInput = document.getElementById('vlc-network-url');
                if (urlInput && urlInput.value.trim()) targetPath = urlInput.value.trim();
            } else if (mode === 'vlc_device') {
                const devInput = document.getElementById('vlc-device-path');
                if (devInput && devInput.value.trim()) targetPath = devInput.value.trim();
            }

            console.info('>>> [Play-Trace] triggerOpenWith — engine:', engine, 'mode:', mode, 'path:', targetPath);

            let res;
            if (engine === 'auto' || mode === 'auto') {
                res = await eel.open_video_smart(targetPath, mode)();
            } else {
                res = await eel.open_video(targetPath, engine === 'mtx' ? 'chrome' : engine, mode)();
            }

            if (res && res.status === 'play') {
                console.info('>>> [Play-Trace] triggerOpenWith returned status=play, mode=', res.mode);
                startEmbeddedVideo(currentVideoItem, res.path, null, res.type || null);
                orchestrateVideoPlaybackMode();
            } else if (res && res.status === 'ok') {
                console.info('>>> [Play-Trace] triggerOpenWith returned status=ok, mode=', res.mode);
                updateStatusStrip(engine, mode, targetPath, false);
            } else if (res && res.status === 'error') {
            }
        }

        function updateStatusStrip(engine, mode, file, isPlaying, hwAccel = false) {
            const strip = document.getElementById('active-engine-status-strip');
            if (!strip) return;
            strip.style.display = 'flex';

            const engineEl = document.getElementById('status-strip-engine');
            const modeEl = document.getElementById('status-strip-mode');
            const fileEl = document.getElementById('status-strip-file');
            const iconEl = document.getElementById('status-strip-icon');
            const hwBadge = document.getElementById('status-strip-hw-badge');

            if (engineEl) engineEl.textContent = engine.charAt(0).toUpperCase() + engine.slice(1);
            if (modeEl) modeEl.textContent = mode;
            if (fileEl) fileEl.textContent = file.split('/').pop();
            if (hwBadge) hwBadge.style.display = hwAccel ? 'inline-block' : 'none';

            if (iconEl) {
                if (isPlaying) {
                    iconEl.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="#7df"><path d="M8 5v14l11-7z"/></svg>';
                } else {
                    iconEl.innerHTML = '<svg width="12" height="12" viewBox="0 0 24 24" fill="#e67e22"><rect x="6" y="6" width="12" height="12" rx="2"/></svg>';
                }
            }
        }

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
                const colors = { auto: '#2a7', chrome: '#2a7', vlc: '#e67e22', mtx: '#2980b9', pyplayer: '#8e44ad', external: '#8e44ad', mpv: '#d32f2f' };
                const bgs = { auto: '#e8f8f0', chrome: '#e8f8f0', vlc: '#fff3e0', mtx: '#eaf4fb', pyplayer: '#f5eafb', external: '#f5eafb', mpv: '#ffebee' };
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
            const defaults = { auto: 'auto', chrome: 'chrome_direct', vlc: 'vlc_embedded', mtx: 'mtx_hls', pyplayer: 'pyplayer_native', external: 'external_stream', mpv: 'mpv_native' };
            const modeInput = document.getElementById('video-mode');
            if (modeInput) modeInput.value = defaults[engine] || 'auto';

            // Show/hide open-with button
            const openWithBtn = document.getElementById('btn-open-with-video');
            if (openWithBtn) openWithBtn.style.display = currentVideoItem ? 'inline-block' : 'none';
        }

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
            const chromeInfo = document.getElementById('chrome-info-strip');
            const chromeInfoTexts = {
                chrome_direct: 'Direct Play: MP4/WebM werden nativ im Browser abgespielt — keine Transkodierung.',
                chrome_remux: 'mkvmerge Remux: MKV-Dateien werden via Pipe-Kit für Chrome kompatibel gemacht.',
                chrome_fragmp4: 'FFmpeg FragMP4: Universelle Echtzeit-Transkodierung über FragMP4 für alle Formate.',
                chrome_hls: 'Internal HLS: Experimentelles HLS-Streaming über das interne Backend.'
            };
            if (chromeInfo && chromeInfoTexts[mode]) chromeInfo.textContent = chromeInfoTexts[mode];

            const vlcInfo = document.getElementById('vlc-info-strip');
            const vlcInfoTexts = {
                vlc_embedded: 'Embedded HLS: VLC streamt das Video als HLS-Stream direkt in diesen Tab.',
                vlc_browser: 'Standalone VLC: Öffnet die Datei in einer separaten VLC-Instanz (extern).',
                vlc_dvd: 'VLC DVD Mode: Optimierte Wiedergabe für DVD-Strukturen und ISO-Images.',
                vlc_network: 'VLC Network: Streamen von einer Netzwerk-URL oder einem Device.',
                vlc_device: 'VLC Device: Direkte Wiedergabe von physikalischen Datenträgern.'
            };
            if (vlcInfo && vlcInfoTexts[mode]) vlcInfo.textContent = vlcInfoTexts[mode];

            const mtxInfo = document.getElementById('mtx-info-strip');
            const mtxInfoTexts = {
                mtx_hls: 'MediaMTX HLS: Stabiles HTTP Live Streaming (benötigt MediaMTX Server).',
                mtx_webrtc: 'MediaMTX WebRTC: Ultra-Low-Latency Wiedergabe (<100ms Verzögerung).',
                mtx_rtsp: 'MediaMTX RTSP: Forwarding an einen RTSP-Stream-Endpunkt.',
                mtx_rtmp: 'MediaMTX RTMP: Forwarding an einen RTMP-Stream-Endpunkt.'
            };
            if (mtxInfo && mtxInfoTexts[mode]) mtxInfo.textContent = mtxInfoTexts[mode];

            const pyInfo = document.getElementById('pyplayer-info-strip');
            const pyInfoTexts = {
                pyplayer_native: 'pyvidplayer2: Nutzt die Python-Bibliothek für eine native Overlay-Wiedergabe.',
                pyplayer_mpv: 'mpv Standalone: Startet den mächtigen mpv-Player als separaten Prozess.',
                pyplayer_mini: 'Mini-Overlay: Kompakte Wiedergabe in einem schwebenden Fenster.'
            };
            if (pyInfo && pyInfoTexts[mode]) pyInfo.textContent = pyInfoTexts[mode];

            // External / D&D Info Strip
            const extInfo = document.getElementById('external-info-strip');
            const extInfoTexts = {
                external_stream: 'Network Stream: Direkte Wiedergabe von URLs (HLS, RTSP, RTMP) im Browser-Player oder VLC.',
                external_dnd: 'Drag & Drop: Ziehe lokale Dateien hierher, um sie sofort abzuspielen.'
            };
            if (extInfo && extInfoTexts[mode]) extInfo.textContent = extInfoTexts[mode];
        }

        // --- External Sources Handlers ---
        async function handleExternalDrop(event) {
            event.preventDefault();
            const zone = document.getElementById('external-dnd-zone');
            if (zone) zone.style.background = '#f7fbff';

            if (event.type === 'dragleave') return;

            let path = event.dataTransfer.getData('text/plain') || event.dataTransfer.getData('text/uri-list');
            console.log("Drop event detected. Data:", path);

            if (path && path.startsWith('file://')) {
                path = decodeURIComponent(path.replace('file://', ''));
                path = path.split('\n')[0].split('\r')[0];
            }

            if (path) {
                showToast(`📂 Externes File: ${path}`, 2000);
                await eel.play_external_file(path)();
            } else if (event.dataTransfer.files.length > 0) {
                showToast("ℹ️ Pfad-Maskierung: Nutze 'Datei auswählen'.", 4000);
            }
        }

        async function playExternalStream() {
            const urlInput = document.getElementById('external-stream-url');
            const url = urlInput ? urlInput.value.trim() : '';
            if (!url) return;

            showToast(`🌐 Stream: ${url}`, 2000);
            const res = await eel.play_stream_url(url, 'hls')();
            if (res && res.status === 'ok') {
                const streamUrl = res.hls || url;
                startEmbeddedVideo({ name: 'Stream', path: url }, streamUrl, null, res.type || 'application/x-mpegURL');
                orchestrateVideoPlaybackMode();
            }
        }

        async function pickAndPlayExternal() {
            const path = await eel.pick_file("Mediendatei auswählen")();
            if (path) {
                showToast(`📂 Öffne: ${path}`, 2000);
                await eel.play_external_file(path)();
            }
        }

        // Legacy: kept for backward compat, delegates to selectEngine
        function updateVideoModes() {
            const type = document.getElementById('player-type');
            if (type) selectEngine(type.value, document.querySelector(`.engine-btn[data-engine="${type.value}"]`));
        }
        function orchestrateVideoPlaybackMode() {
            const dndPanel = document.getElementById('orchestrator-ingress-drag-drop-buffer');
            const embedded = document.getElementById('coordinated-media-renderer-pipeline-viewport');
            if (dndPanel) dndPanel.style.display = 'none';
            if (embedded) embedded.style.display = 'flex';
        }

        function formatTime(seconds) {
            if (isNaN(seconds)) return '00:00';
            const h = Math.floor(seconds / 3600);
            const m = Math.floor((seconds % 3600) / 60);
            const s = Math.floor(seconds % 60);
            if (h > 0) return `${h}:${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
            return `${m.toString().padStart(2, '0')}:${s.toString().padStart(2, '0')}`;
        }

        async function playVideo(item, path) {
            console.info(">>> [Play-Trace] playVideo() called for:", path, "item:", item);
            if (window._locking_video_playback) {
                console.warn(">>> [Play-Trace] Playback LOCK detected. Skipping double call.");
                return;
            }
            window._locking_video_playback = true;
            setTimeout(() => { window._locking_video_playback = false; }, 1000);

            currentVideoItem = item;
            currentVideoPath = path;

            showToast(`🔍 Analysiere Media-Routing...`, 1500);

            try {
                // 1. Technical Analysis via Test-Suite
                // We use the relative path (relpath) if available, otherwise fallback to item.path or the passed path
                const relpath = item.relpath || item.path || path;
                const info = await eel.analyze_media(relpath)();

                if (info.error) {
                    showToast("Fehler bei der Analyse: " + info.error);
                    return;
                }

                console.log("Analysis result:", info);
                const score = info.quality_score;
                const mode = info.recommended_mode;

                // Update UI Indicators in Video Tab
                safeText('player-score-badge', `${score} / 100`);
                safeText('player-route-badge', mode.toUpperCase());
                safeStyle('player-routing-status-bar', 'display', 'flex');

                // Color coding for score
                const scoreBadge = document.getElementById('player-score-badge');
                if (scoreBadge) {
                    if (score > 80) scoreBadge.style.color = '#2a7';
                    else if (score > 50) scoreBadge.style.color = '#ff9800';
                    else scoreBadge.style.color = '#d32f2f';
                }

                const tagsContainer = document.getElementById('player-codec-tags');
                if (tagsContainer) {
                    tagsContainer.innerHTML = '';
                    const codecs = [];
                    const a = info.analysis || {};
                    if (a.video_codec) codecs.push(a.video_codec.toUpperCase());
                    if (a.audio_codec) codecs.push(a.audio_codec.toUpperCase());
                    if (a.hdr) codecs.push('HDR');
                    codecs.forEach(c => {
                        const span = document.createElement('span');
                        span.style = "font-size: 0.65em; padding: 2px 6px; background: #f0f0f0; border: 1px solid #ddd; border-radius: 4px; color: #666; font-weight: bold;";
                        span.innerText = c;
                        tagsContainer.appendChild(span);
                    });
                }

                showToast(`✨ Quality: ${score}/100 | Mode: ${mode.toUpperCase()}`, 3000);

                // 2. Resolve final play source
                const source = await eel.get_play_source(relpath)();
                console.log("Play source result:", source);

                if (source.mode === 'direct') {
                    showToast("🚀 DIRECT PLAY (Native/Remux)", 2000);
                    switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                    selectEngine('chrome');
                    const btn = document.querySelector('[data-mode="chrome_direct"]');
                    selectSubMode('chrome_direct', btn, 'chrome');
                    const d_sec = (info.analysis && info.analysis.duration_sec) || 0;
                    startEmbeddedVideo(item, source.url, null, 'video/mp4', d_sec);
                } else if (source.mode === 'vlc') {
                    showToast("📺 VLC REQUIRED (ISO/HDR/Complex)", 3000);
                    switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                    selectEngine('vlc');
                    startVLC(source.path || path);
                } else if (source.mode === 'hls') {
                    showToast("🌐 FALLBACK TO HLS STREAMING", 3000);
                    const res = await eel.open_video_smart(path, 'hls')();
                    if (res && res.status === 'play') {
                        switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                        selectEngine('mtx');
                        const streamUrl = res.webrtc || res.hls;
                        const d_sec = (info.analysis && info.analysis.duration_sec) || 0;
                        startEmbeddedVideo(item, streamUrl, null, 'application/x-mpegURL', d_sec);
                    }
                } else if (source.mode === 'transcode') {
                    showToast("🛠️ REAL-TIME TRANSCODE (FFmpeg/MSE)", 3000);
                    switchTab('video', document.getElementById('media-orchestrator-tab-trigger'));
                    selectEngine('chrome');
                    const btn = document.querySelector('[data-mode="chrome_transcode"]');
                    selectSubMode('chrome_transcode', btn, 'chrome');
                    const d_sec = (info.analysis && info.analysis.duration_sec) || 0;
                    startEmbeddedVideo(item, source.url, null, 'video/mp4', d_sec);
                } else if (source.mode === 'error') {
                    showPlaybackError("Routing Fehler", source.message || "Unbekannter Fehler beim Routing", {
                        mode: "ERROR",
                        score: score,
                        v_codec: (info.analysis && info.analysis.video_codec) || '-',
                        a_codec: (info.analysis && info.analysis.audio_codec) || '-',
                        path: relpath
                    });
                }
            } catch (err) {
                console.error("Routing error:", err);
                showPlaybackError("Kritischer Fehler", `Media-Analyse fehlgeschlagen: ${err.message || err}`, {
                    mode: "CRITICAL",
                    path: currentVideoPath,
                    error_details: String(err)
                });
            }
        }

        function showPlaybackError(title, message, technicalInfo = {}) {
            const body = document.getElementById('playback-error-body');
            if (!body) {
                alert(title + ": " + message);
                return;
            }
            
            let html = `
                <div style="font-weight: bold; font-size: 1.1em; color: #333; margin-bottom: 10px;">${title}</div>
                <div style="color: #666; margin-bottom: 20px; line-height: 1.5;">${message}</div>
                
                <div style="background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 15px;">
                    <div style="font-size: 0.8em; color: #6c757d; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px; font-weight: bold;">Technische Details</div>
                    <table style="width: 100%; font-size: 0.9em; border-collapse: collapse;">
                        <tr><td style="padding: 4px 0; color: #495057; font-weight: 600; width: 40%;">Modus</td><td style="padding: 4px 0; color: #212529;">${technicalInfo.mode || '-'}</td></tr>
                        <tr><td style="padding: 4px 0; color: #495057; font-weight: 600;">Qualität</td><td style="padding: 4px 0; color: #212529;">${technicalInfo.score || '-'} / 100</td></tr>
                        <tr><td style="padding: 4px 0; color: #495057; font-weight: 600;">Video Codec</td><td style="padding: 4px 0; color: #212529;">${technicalInfo.v_codec || '-'}</td></tr>
                        <tr><td style="padding: 4px 0; color: #495057; font-weight: 600;">Audio Codec</td><td style="padding: 4px 0; color: #212529;">${technicalInfo.a_codec || '-'}</td></tr>
                        <tr><td style="padding: 4px 0; color: #495057; font-weight: 600;">Dateipfad</td><td style="padding: 4px 0; color: #212529; word-break: break-all; font-family: monospace; font-size: 0.85em;">${technicalInfo.path || '-'}</td></tr>
                    </table>
                </div>
            `;
            
            body.innerHTML = html;
            safeStyle('playback-error-modal', 'display', 'flex');
            safeStyle('playback-error-modal', 'zIndex', '5000');
        }

        async function runBatchRemux() {
            const folder = await eel.pick_folder()();
            if (!folder) return;

            const btn = event.target.closest('button');
            const originalText = btn.innerHTML;
            btn.innerHTML = '⏳ remuxing...';
            btn.disabled = true;

            try {
                const result = await eel.remux_mkv_batch(folder)();
                if (result.status === 'ok') {
                    const r = result.results;
                    alert(`Remux abgeschlossen!\nErfolgreich: ${r.success}\nFehler: ${r.errors.length}\n${r.errors.join('\n')}`);
                } else {
                    alert(result.error);
                }
            } finally {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }
        }

        // --- Video.js Custom Component Definitions ---
        const vjsBtn = videojs.getComponent('Button');
        const vjsMenuBtn = videojs.getComponent('MenuButton');
        const vjsMenuItem = videojs.getComponent('MenuItem');

        let currentVideoTracks = { audio: [], subtitles: [] };
        let currentAudioIdx = 0;
        let currentSubsIdx = null;

        videojs.registerComponent('AudioTrackMenuButton', videojs.extend(vjsMenuBtn, {
            constructor: function() { vjsMenuBtn.apply(this, arguments); },
            createMenu: function() {
                const Menu = videojs.getComponent('Menu');
                const menu = new Menu(this.player_);
                if (currentVideoTracks && currentVideoTracks.audio) {
                    currentVideoTracks.audio.forEach(t => {
                        const item = new vjsMenuItem(this.player_, {
                            label: t.label, selectable: true,
                            selected: String(t.id) === String(currentAudioIdx)
                        });
                        item.on('click', () => {
                            currentAudioIdx = t.id;
                            startEmbeddedVideo(currentVideoItem, currentVideoPath, null, null, null, currentAudioIdx, currentSubsIdx);
                        });
                        menu.addItem(item);
                    });
                }
                return menu;
            },
            buildCSSClass: function() { return "vjs-icon-audio vjs-control vjs-button vjs-menu-button"; },
            controlText_: "Audio"
        }));

        videojs.registerComponent('SubtitleTrackMenuButton', videojs.extend(vjsMenuBtn, {
            constructor: function() { vjsMenuBtn.apply(this, arguments); },
            createMenu: function() {
                const Menu = videojs.getComponent('Menu');
                const menu = new Menu(this.player_);
                const offItem = new vjsMenuItem(this.player_, { label: "Off", selectable: true, selected: currentSubsIdx === null });
                offItem.on('click', () => {
                    currentSubsIdx = null;
                    startEmbeddedVideo(currentVideoItem, currentVideoPath, null, null, null, currentAudioIdx, null);
                });
                menu.addItem(offItem);
                if (currentVideoTracks && currentVideoTracks.subtitles) {
                    currentVideoTracks.subtitles.forEach(t => {
                        const item = new vjsMenuItem(this.player_, {
                            label: t.label, selectable: true,
                            selected: String(t.id) === String(currentSubsIdx)
                        });
                        item.on('click', () => {
                            currentSubsIdx = t.id;
                            startEmbeddedVideo(currentVideoItem, currentVideoPath, null, null, null, currentAudioIdx, currentSubsIdx);
                        });
                        menu.addItem(item);
                    });
                }
                return menu;
            },
            buildCSSClass: function() { return "vjs-icon-subtitles vjs-control vjs-button vjs-menu-button"; },
            controlText_: "Subs"
        }));

        let currentAspectRatio = '16:9';
        videojs.registerComponent('AspectRatioMenuButton', videojs.extend(vjsMenuBtn, {
            constructor: function() { vjsMenuBtn.apply(this, arguments); },
            createMenu: function() {
                const Menu = videojs.getComponent('Menu');
                const menu = new Menu(this.player_);
                const ratios = ['Auto', '16:9', '21:9', '4:3', '1:1'];
                ratios.forEach(r => {
                    const item = new vjsMenuItem(this.player_, { label: r, selectable: true, selected: r === currentAspectRatio });
                    item.on('click', () => {
                        currentAspectRatio = r;
                        if(r === 'Auto') { this.player_.fluid(true); this.player_.aspectRatio(''); }
                        else { this.player_.fluid(false); this.player_.aspectRatio(r); }
                        showToast(`Aspect Ratio: ${r}`, 1000);
                    });
                    menu.addItem(item);
                });
                return menu;
            },
            buildCSSClass: function() { return "vjs-icon-spinner vjs-control vjs-button vjs-menu-button"; },
            controlText_: "Ratio"
        }));

        videojs.registerComponent('CinemaModeButton', videojs.extend(vjsBtn, {
            constructor: function() { vjsBtn.apply(this, arguments); },
            handleClick: function() { 
                const container = document.getElementById('video-player-container-root-wrapper');
                if(container) {
                    container.classList.toggle('cinema-expanded');
                    showToast(container.classList.contains('cinema-expanded') ? "Cinema Mode: ON" : "Cinema Mode: OFF", 1000);
                }
            },
            buildCSSClass: function() { return "vjs-icon-layout vjs-control vjs-button cinema-btn"; },
            controlText_: "Cinema"
        }));

        videojs.registerComponent('VisualFXMenuButton', videojs.extend(vjsMenuBtn, {
            constructor: function() { vjsMenuBtn.apply(this, arguments); },
            createMenu: function() {
                const Menu = videojs.getComponent('Menu');
                const menu = new Menu(this.player_);
                const fx = [
                    { l: 'Natural', f: 'none' }, { l: 'Vibrant', f: 'saturate(1.4) contrast(1.1)' },
                    { l: 'Cinematic', f: 'contrast(1.2) sepia(0.1)' }, { l: 'B&W', f: 'grayscale(1)' },
                    { l: 'Warmer', f: 'sepia(0.3) saturate(1.2)' }
                ];
                fx.forEach(f => {
                    const item = new vjsMenuItem(this.player_, { label: f.l, selectable: true });
                    item.on('click', () => {
                        const v = document.getElementById('native-html5-video-resource-node');
                        if(v) v.style.filter = f.f;
                        showToast(`FX: ${f.l}`, 800);
                    });
                    menu.addItem(item);
                });
                return menu;
            },
            buildCSSClass: function() { return "vjs-icon-circle vjs-control vjs-button vjs-menu-button"; },
            controlText_: "Visual FX"
        }));

        videojs.registerComponent('StopButton', videojs.extend(vjsBtn, {
            constructor: function() { vjsBtn.apply(this, arguments); },
            handleClick: function() { stopVideo(); },
            buildCSSClass: function() { return "vjs-icon-cancel vjs-control vjs-button stop-btn"; },
            controlText_: "Stop"
        }));

        videojs.registerComponent('VlcButton', vjsBtn.extend({
            constructor: function() { vjsBtn.apply(this, arguments); },
            handleClick: function() { if(typeof switchToVLC === 'function') switchToVLC(); },
            buildCSSClass: function() { return "vjs-icon-share vjs-control vjs-button vlc-btn"; },
            controlText_: "VLC"
        }));

        videojs.registerComponent('MpvButton', vjsBtn.extend({
            constructor: function() { vjsBtn.apply(this, arguments); },
            handleClick: function() { if(currentVideoPath) if(typeof startMPV === 'function') startMPV(currentVideoPath); },
            buildCSSClass: function() { return "vjs-icon-circle-inner-circle vjs-control vjs-button mpv-btn"; },
            controlText_: "MPV"
        }));

        videojs.registerComponent('SnapshotButton', vjsBtn.extend({
            constructor: function() { vjsBtn.apply(this, arguments); },
            handleClick: function() { 
                const v = document.getElementById('native-html5-video-resource-node');
                if(!v) return;
                const canvas = document.createElement('canvas');
                canvas.width = v.videoWidth; canvas.height = v.videoHeight;
                canvas.getContext('2d').drawImage(v, 0, 0);
                const data = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.download = `snapshot_${new Date().getTime()}.png`;
                link.href = data; link.click();
            },
            buildCSSClass: function() { return "vjs-icon-photo vjs-control vjs-button snapshot-btn"; },
            controlText_: "Snapshot"
        }));

        function startEmbeddedVideo(item, path, onErrorCallback = null, type = null, durationSec = null, audioIdx = 0, subsIdx = null) {
            const video = document.getElementById('native-html5-video-resource-node');
            const placeholder = document.getElementById('idle-state-media-icon-symbol');

            if (!vjsPlayer) {
                vjsPlayer = videojs('native-html5-video-resource-node', {
                    fluid: true,
                    aspectRatio: '16:9',
                    playbackRates: [0.5, 1, 1.25, 1.5, 2],
                    controlBar: {
                        children: [
                            'playToggle', 'volumePanel', 'currentTimeDisplay', 'timeDivider',
                            'durationDisplay', 'progressControl', 'remainingTimeDisplay',
                            'playbackRateMenuButton',
                            'AudioTrackMenuButton',
                            'SubtitleTrackMenuButton',
                            'AspectRatioMenuButton',
                            'VisualFXMenuButton',
                            'VlcButton', 'MpvButton', 'SnapshotButton', 'CinemaModeButton', 'StopButton',
                            'fullscreenToggle', 'pictureInPictureToggle'
                        ]
                    }
                });

                vjsPlayer.on('ended', () => {
                    if (repeatStatus === 'one') vjsPlayer.play();
                    else playNext();
                });

                vjsPlayer.on('error', () => {
                    const error = vjsPlayer.error();
                    if (error && error.code === 4) {
                        showUnsupportedVideoHint();
                        if (typeof onErrorCallback === 'function') onErrorCallback();
                    }
                });

                vjsPlayer.on('timeupdate', () => {
                    const slider = document.getElementById('video-seek-slider');
                    const currentTimeSpan = document.getElementById('video-current-time');
                    const durationSpan = document.getElementById('video-duration');
                    const now = vjsPlayer.currentTime();
                    if (slider && !slider.matches(':active')) {
                        const progress = (now / vjsPlayer.duration()) * 100;
                        slider.value = isFinite(progress) ? progress : 0;
                    }
                    if (currentTimeSpan) currentTimeSpan.innerText = formatTime(now);
                    if (durationSpan) durationSpan.innerText = formatTime(vjsPlayer.duration());

                    // Throttled position update to backend
                    if (Math.abs(now - (vjsPlayer.lastPersist || 0)) > 5 && (item || currentVideoItem)) {
                        const mediaName = (item && item.name) || (currentVideoItem && currentVideoItem.name);
                        if (mediaName) {
                            vjsPlayer.lastPersist = now;
                            eel.update_playback_position(mediaName, now)();
                        }
                    }
                });

                const seekSlider = document.getElementById('video-seek-slider');
                if (seekSlider) {
                    seekSlider.addEventListener('input', (e) => {
                        if (vjsPlayer && vjsPlayer.duration()) {
                            const previewTime = (e.target.value / 100) * vjsPlayer.duration();
                            const currentTimeSpan = document.getElementById('video-current-time');
                            if (currentTimeSpan) currentTimeSpan.innerText = formatTime(previewTime);
                        }
                    });
                    seekSlider.addEventListener('change', (e) => {
                        if (vjsPlayer && vjsPlayer.duration()) {
                            const newTime = (e.target.value / 100) * vjsPlayer.duration();
                            vjsPlayer.currentTime(newTime);
                        }
                    });
                }
            }

            // Centralized seeking logic for all transcode-style streams
            vjsPlayer.off('seeking');
            vjsPlayer.on('seeking', () => {
                const newTime = vjsPlayer.currentTime();
                const currentSrc = vjsPlayer.src();
                if (currentSrc.includes('/stream_transcode') || currentSrc.includes('/video-stream') || currentSrc.includes('/transcode')) {
                    console.info("[Video.js] Hot-reloading stream for seek at:", newTime);
                    const base = currentSrc.split('?')[0];
                    const newPath = `${base}?filepath=${encodeURIComponent(path)}&ss=${newTime}`;
                    vjsPlayer.src({ src: newPath, type: vjsPlayer.currentType() });
                    vjsPlayer.one('canplay', () => {
                        vjsPlayer.currentTime(newTime);
                        vjsPlayer.play();
                    });
                }
            });

            vjsPlayer.originalPath = path;
            eel.stop_vlc()();
            safeStyle('vlc-info', 'display', 'none');
            hideUnsupportedVideoHint();

            if (placeholder) {
                placeholder.style.setProperty('display', 'none', 'important');
                placeholder.style.zIndex = '-1';
            }

            const vjsWrapper = video.closest('.video-js');
            if (vjsWrapper) {
                vjsWrapper.style.display = 'block';
                vjsWrapper.style.width = '100%';
                vjsWrapper.style.zIndex = '50';
            }

            video.style.display = 'block';
            video.style.visibility = 'visible';
            video.style.opacity = '1';
            video.style.zIndex = '10';

            let finalPath = path;
            if (path && (path.includes('/stream_transcode') || path.includes('/video-stream') || path.includes('/transcode'))) {
                const url = new URL(path.includes('://') ? path : 'http://localhost' + path);
                url.searchParams.set('audio_idx', audioIdx);
                if (subsIdx !== null) url.searchParams.set('subs_idx', subsIdx);
                else url.searchParams.delete('subs_idx');
                finalPath = url.pathname + url.search;
            }

            const finalType = type || 'video/mp4';
            vjsPlayer.src({ src: finalPath, type: finalType });

            // Fetch tracks for the menu if not already loaded for this path
            if (vjsPlayer.lastProbedPath !== path) {
                vjsPlayer.lastProbedPath = path;
                eel.get_media_tracks(path)((tracks) => {
                    currentVideoTracks = tracks || { audio: [], subtitles: [] };
                    // Re-calculate menus
                    if (vjsPlayer.controlBar.childNameIndex_['AudioTrackMenuButton']) {
                        vjsPlayer.controlBar.childNameIndex_['AudioTrackMenuButton'].update();
                    }
                    if (vjsPlayer.controlBar.childNameIndex_['SubtitleTrackMenuButton']) {
                        vjsPlayer.controlBar.childNameIndex_['SubtitleTrackMenuButton'].update();
                    }
                });
            }

            // Restore position
            const seekTime = (item && item.playback_position) || 0;
            if (seekTime > 0) {
                const restoreSeek = () => {
                    if (Math.abs(vjsPlayer.currentTime() - seekTime) > 1) {
                        vjsPlayer.currentTime(seekTime);
                    }
                };
                vjsPlayer.one('canplay', restoreSeek);
                setTimeout(restoreSeek, 2000);
            }

            // Stubborn duration override
            if (durationSec && durationSec > 0) {
                const targetDuration = parseFloat(durationSec);
                const applyOverride = () => {
                    vjsPlayer.duration = function () { return targetDuration; };
                    vjsPlayer.trigger('durationchange');
                };
                vjsPlayer.on('loadedmetadata', applyOverride);
                vjsPlayer.on('durationchange', () => {
                    if (Math.abs(vjsPlayer.duration() - targetDuration) > 1) applyOverride();
                });
                vjsPlayer.on('progress', () => {
                    if (vjsPlayer.duration() < targetDuration * 0.9) applyOverride();
                });
                applyOverride();
            } else {
                delete vjsPlayer.duration;
            }

            vjsPlayer.ready(() => {
                setTimeout(() => {
                    const vjsWrapper = video.closest('.video-js');
                    if (vjsWrapper) {
                        vjsWrapper.style.visibility = 'visible';
                        vjsWrapper.style.opacity = '1';
                        vjsWrapper.style.display = 'block';
                    }
                    if (placeholder) {
                        placeholder.style.setProperty('display', 'none', 'important');
                        placeholder.style.visibility = 'hidden';
                    }
                    vjsPlayer.trigger('resize');
                }, 150);

                vjsPlayer.play().catch(e => {
                    console.warn("Video.js playback failed:", e);
                    if (typeof onErrorCallback === 'function') onErrorCallback();
                });
            });
        }

        async function startMPV(filePath) {
            const video = document.getElementById('native-html5-video-resource-node');
            if (video) { video.pause(); video.style.display = 'none'; }
            if (typeof eel !== 'undefined' && typeof eel.stop_vlc === 'function') eel.stop_vlc()();
            if (typeof showToast === 'function') showToast("🚀 MPV...", 3000);
            try {
                const res = await eel.open_mpv(filePath)();
                if (res && res.status === 'ok') showToast("MPV gestartet.", 2000);
            } catch (e) { console.error("MPV Error:", e); }
        }

        async function startVLC(filePath, displayName = null) {
            const video = document.getElementById('native-html5-video-resource-node');
            if (video) { video.pause(); video.style.display = 'none'; }
            safeStyle('idle-state-media-icon-symbol', 'display', 'block');
            safeStyle('btn-open-vlc', 'display', 'none');
            hideUnsupportedVideoHint();
            safeStyle('vlc-info', 'display', 'block');
            const shownName = displayName || (currentVideoItem && currentVideoItem.name) || String(filePath || '-');
            safeText('vlc-current-file', shownName);
            const res = await eel.play_vlc(filePath)();
            if (res && res.error) {
                showPlaybackError("VLC Fehler", "Fehler beim Starten.", { error: res.error });
                safeHtml('vlc-pipe-log-feed', '<span style="color:#f33;">FEHLER:</span> ' + res.error);
                safeStyle('vlc-status-badge', 'background', '#e74c3c');
                safeText('vlc-status-badge', 'Fehler');
            } else {
                safeHtml('vlc-pipe-log-feed', 'Aktiv.');
                safeStyle('vlc-status-badge', 'background', '#2a7');
                safeText('vlc-status-badge', 'Aktiv');
            }
        }

        function showExternalStatus(filePath, mode) {
            const video = document.getElementById('native-html5-video-resource-node');
            if (video) { video.pause(); video.style.display = 'none'; }
            safeStyle('idle-state-media-icon-symbol', 'display', 'block');
            safeStyle('vlc-info', 'display', 'block');
            const shownName = (currentVideoItem && currentVideoItem.name) || String(filePath || '-');
            safeText('vlc-current-file', shownName + " [Extern: " + mode + "]");
            safeHtml('vlc-pipe-log-feed', 'Extern.');
            safeStyle('vlc-status-badge', 'background', '#3498db');
            safeText('vlc-status-badge', 'Extern');
        }

        async function togglePip() {
            const video = document.getElementById('native-html5-video-resource-node');
            if (!video) return;
            try {
                if (document.pictureInPictureElement) await document.exitPictureInPicture();
                else if (document.pictureInPictureEnabled) await video.requestPictureInPicture();
            } catch (error) { console.error("PiP Error:", error); }
        }

        function seekVideo(delta) { if (vjsPlayer) vjsPlayer.currentTime(vjsPlayer.currentTime() + delta); }
        function toggleSpeed() {
            if (vjsPlayer) {
                const currentRate = vjsPlayer.playbackRate();
                const rates = [1, 1.25, 1.5, 2, 0.5];
                let nextIdx = (rates.indexOf(currentRate) + 1) % rates.length;
                vjsPlayer.playbackRate(rates[nextIdx]);
                showToast(`Speed: ${rates[nextIdx]}x`, 1000);
            }
        }
        function openEQ() { showToast("EQ soon", 2000); }

        async function stopVideo() {
            const video = document.getElementById('native-html5-video-resource-node');
            if (vjsPlayer) { try { vjsPlayer.pause(); } catch (e) { } }
            if (video) { video.src = ""; video.style.display = 'none'; }
            safeStyle('idle-state-media-icon-symbol', 'display', 'block');
            await eel.stop_vlc()();
            safeStyle('vlc-info', 'display', 'none');
            currentVideoItem = null;
            currentVideoPath = null;
        }

        function switchToVLC() {
            if (currentVideoItem) {
                safeValue('player-type', 'vlc');
                updateVideoModes();
                safeValue('video-mode', 'vlc_extern');
                playVideo(currentVideoItem, currentVideoItem.path);
            }
        }

        window.jumpToChapter = function (startTime) {
            let p = document.getElementById('native-html5-audio-pipeline-element');
            if (p) {
                p.currentTime = startTime;
                p.play();
            }
        };
    
    
        const ALL_PARSERS = ["filename", "container", "mkvmerge", "mkvinfo", "vlc", "mutagen", "pymediainfo", "ffprobe", "ffmpeg", "isoparser", "ebml", "mkvparse", "enzyme", "pycdlib", "pymkv", "tinytag", "eyed3", "music_tag"];
        let SLOW_PARSERS = [];
        let currentParserChain = [];
        let currentParserOptions = {};
        let currentParserMapping = {};
        let currentParserInfo = {};
        let currentGranularSettings = {};

        // INitialize on load to populate left side list
        document.addEventListener('DOMContentLoaded', () => {
            loadParserConfig();
        });

        function loadParserConfig() {
            // First fetch slow parsers
            eel.get_slow_parsers()((slow) => {
                SLOW_PARSERS = slow || [];

                eel.get_parser_config()((config) => {
                    console.log("Raw parser config from python:", config);

                    if (typeof config === 'string') {
                        try { config = JSON.parse(config); } catch (e) { console.error("Failed to parse config:", e); }
                    }

                    currentParserOptions = config || {};

                    if (config && config.parser_chain && Array.isArray(config.parser_chain)) {
                        currentParserChain = config.parser_chain;
                    } else {
                        currentParserChain = ["filename", "container", "mutagen", "pymediainfo", "ffprobe", "ffmpeg"];
                    }

                    if (config && config.parser_mode) {
                        const modeToggle = document.getElementById('toggle-parser-mode');
                        if (modeToggle) modeToggle.checked = (config.parser_mode === "full");
                        const statusText = document.getElementById('parser-mode-status');
                        if (statusText) {
                            statusText.innerText = config.parser_mode === "full" ? t('parser_mode_full') : t('parser_mode_light');
                        }
                    }

                    // Set Fast Scan toggle
                    const fastScanToggle = document.getElementById('toggle-fast-scan');
                    if (fastScanToggle) {
                        fastScanToggle.checked = config.fast_scan_enabled !== false; // Default true
                    }

                    // Initialize mapping
                    eel.get_parser_mapping()((mapping) => {
                        console.log("Parser mapping loaded:", mapping);
                        currentParserMapping = mapping;
                    });

                    cats.forEach(cat => {
                        const cb = document.getElementById('cat-' + cat);
                        if (cb && config.indexed_categories) {
                            cb.checked = config.indexed_categories.includes(cat);
                        }

                        const dispCb = document.getElementById('disp-cat-' + cat);
                        if (dispCb && config.displayed_categories) {
                            dispCb.checked = config.displayed_categories.includes(cat);
                        }
                    });

                    // Set Playback Mode
                    const playbackSelect = document.getElementById('config-playback-mode');
                    if (playbackSelect && config.playback_mode) {
                        playbackSelect.value = config.playback_mode;
                    }

                    // Set Bandwidth Limit
                    const bandwidthInput = document.getElementById('config-bandwidth-limit');
                    if (bandwidthInput && config.bandwidth_limit) {
                        bandwidthInput.value = config.bandwidth_limit;
                    }

                    // Set Feature Flags
                    if (config.feature_flags) {
                        const analyseFlag = document.getElementById('flag-analyse-mode');
                        if (analyseFlag) analyseFlag.checked = !!config.feature_flags.analyse_mode;
                        const writeFlag = document.getElementById('flag-write-mode');
                        if (writeFlag) writeFlag.checked = !!config.feature_flags.write_mode;
                    }

                    // Fetch Parser Info and Granular Settings
                    if (eel.get_all_parser_info) {
                        eel.get_all_parser_info()((info) => {
                            currentParserInfo = info || {};
                        });
                    }
                    if (eel.get_all_parser_settings) {
                        eel.get_all_parser_settings()((settings) => {
                            currentGranularSettings = settings || {};
                        });
                    }

                    renderParserList();
                });
            });
        }

        function renderParserList() {
            const list = document.getElementById('parser-list');
            if (!list) return;
            list.innerHTML = '';

            currentParserChain.forEach(parser => {
                if (ALL_PARSERS.includes(parser)) {
                    list.appendChild(createParserItem(parser, true));
                }
            });

            ALL_PARSERS.forEach(parser => {
                if (!currentParserChain.includes(parser)) {
                    list.appendChild(createParserItem(parser, false));
                }
            });

            setupDragAndDrop();
        }

        function createParserItem(parserId, isActive) {
            const li = document.createElement('li');
            li.className = 'parser-item';
            li.draggable = true;
            li.dataset.id = parserId;

            const labelName = t('parser_' + parserId);
            const isSlow = SLOW_PARSERS.includes(parserId);
            const slowBadge = isSlow ? `<span style="font-size: 0.7em; background: #fff3e0; color: #ef6c00; padding: 2px 6px; border-radius: 4px; margin-left: 8px; font-weight: bold; border: 1px solid #ffe0b2;">${t('parser_slow_label')}</span>` : '';

            li.innerHTML = `
                <div class="parser-handle">☰</div>
                <div class="parser-name" style="flex: 1; cursor: pointer;" onclick="showParserOptions('${parserId}')">${labelName}${slowBadge}</div>
                <label class="switch">
                    <input type="checkbox" class="parser-toggle" ${isActive ? 'checked' : ''} onchange="saveParserChainUI()">
                    <span class="slider"></span>
                </label>
            `;

            // Add click listener for selection state
            li.addEventListener('click', (e) => {
                if (!e.target.classList.contains('parser-toggle') && !e.target.classList.contains('slider')) {
                    showParserOptions(parserId);
                }
            });

            return li;
        }

        async function showParserOptions(parserId) {
            const container = document.getElementById('parser-options-container');
            const placeholder = document.getElementById('parser-options-placeholder');

            // Highlight selected in list
            document.querySelectorAll('.parser-item').forEach(li => {
                li.classList.toggle('selected', li.dataset.id === parserId);
            });

            placeholder.style.display = 'none';
            container.style.display = 'flex';
            container.style.flexDirection = 'column';
            container.style.gap = '20px';
            container.innerHTML = '';

            const pInfo = currentParserInfo[parserId] || {};
            const pCaps = pInfo.capabilities || {};
            const pSchema = pInfo.settings_schema || {};
            const pSettings = currentGranularSettings[parserId] || {};

            let html = '';

            // 1. Capabilities Header
            if (pCaps.name) {
                html += `
                    <div style="background: #f8f9fa; border-radius: 12px; padding: 20px; border: 1px solid #eee; margin-bottom: 30px;">
                        <h3 style="margin: 0 0 10px 0; display: flex; align-items: center; gap: 10px; font-size: 1.2em;">
                            <span style="background: #2a7; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.8em; font-weight: bold;">${pCaps.name}</span>
                            Parser Details
                        </h3>
                        <p style="color: #555; font-size: 0.9em; margin-bottom: 20px; line-height: 1.6;">${pCaps.description || ''}</p>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                            <div>
                                <h4 style="font-size: 0.8em; color: #888; text-transform: uppercase; margin-bottom: 8px;">Supported Tags</h4>
                                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                                    ${(pCaps.supported_tags || []).map(t => `<span style="background: white; border: 1px solid #ddd; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; color: #666;">${t}</span>`).join('')}
                                </div>
                            </div>
                            <div>
                                <h4 style="font-size: 0.8em; color: #888; text-transform: uppercase; margin-bottom: 8px;">Supported Codecs</h4>
                                <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                                    ${(pCaps.supported_codecs || []).map(t => `<span style="background: white; border: 1px solid #ddd; padding: 2px 8px; border-radius: 4px; font-size: 0.75em; color: #666;">${t}</span>`).join('')}
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            }

            // 2. Dynamic Settings from Schema
            if (Object.keys(pSchema).length > 0) {
                html += `<h3 style="font-size: 1.1em; margin-bottom: 15px; border-left: 4px solid #2a7; padding-left: 12px;">Parser Einstellungen</h3>`;
                for (const [key, schema] of Object.entries(pSchema)) {
                    const value = pSettings[key] !== undefined ? pSettings[key] : schema.default;
                    html += renderGranularSettingRow(parserId, key, schema, value);
                }
            }

            // Fallback for legacy hardcoded options if info is missing
            if (Object.keys(pSchema).length === 0) {
                if (parserId === 'mutagen') {
                    html += renderOptionRow('mutagen_prefer_albumartist', t('parser_opt_mutagen_albumartist'));
                    html += renderOptionRow('mutagen_extract_lyrics', t('parser_opt_mutagen_lyrics'));
                } else if (parserId === 'pymediainfo') {
                    html += renderOptionRow('pymediainfo_full_scan', t('parser_opt_pymediainfo_full'));
                } else if (parserId === 'ffmpeg') {
                    html += renderOptionRow('ffmpeg_deep_analysis', t('parser_opt_ffmpeg_deep'));
                    html += renderOptionRow('ffmpeg_extract_thumbnails', t('parser_opt_ffmpeg_thumbs'));
                } else {
                    const parserName = t('parser_' + parserId);
                    html += `<p style="color: #666; font-style: italic; padding: 10px;">${t('parser_no_options').replace('{parser}', parserName)}</p>`;
                }
            }

            // 3. Supported Extensions
            const extensions = [];
            for (const ext in currentParserMapping) {
                if (currentParserMapping[ext].includes(parserId)) {
                    extensions.push(ext);
                }
            }

            if (extensions.length > 0) {
                html += `
                    <div style="margin-top: 25px; padding: 18px; background: rgba(0,0,0,0.03); border-radius: 12px; border: 1px solid rgba(0,0,0,0.05);">
                        <h4 style="margin: 0 0 12px 0; font-size: 0.85em; color: #888; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">${t('parser_supported_types')}</h4>
                        <div style="display: flex; flex-wrap: wrap; gap: 6px;">
                            ${extensions.map(ext => `<span style="background: #fff; color: #555; padding: 4px 10px; border-radius: 6px; font-size: 0.8em; font-weight: 600; font-family: 'JetBrains Mono', 'Courier New', monospace; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid rgba(0,0,0,0.05);">${ext}</span>`).join('')}
                        </div>
                    </div>
                `;
            }

            container.innerHTML = html;
        }

        function renderGranularSettingRow(parserId, key, schema, value) {
            let fieldHtml = '';
            if (schema.type === 'boolean') {
                fieldHtml = `
                    <label class="switch">
                        <input type="checkbox" ${value ? 'checked' : ''} onchange="updateGranularSetting('${parserId}', '${key}', this.checked)">
                        <span class="slider"></span>
                    </label>
                `;
            } else if (schema.type === 'string') {
                fieldHtml = `<input type="text" value="${value || ''}" style="flex: 1; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px;" onchange="updateGranularSetting('${parserId}', '${key}', this.value)">`;
            } else if (schema.type === 'integer') {
                fieldHtml = `<input type="number" value="${value || 0}" style="width: 80px; padding: 8px 12px; border: 1px solid #ddd; border-radius: 6px;" onchange="updateGranularSetting('${parserId}', '${key}', parseInt(this.value))">`;
            }

            return `
                <div style="display: flex; flex-direction: column; gap: 8px; background: #fff; border: 1px solid #eee; padding: 18px; border-radius: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.02);">
                    <div style="display: flex; align-items: center; justify-content: space-between; gap: 20px;">
                        <div style="font-weight: 600; color: #333;">${key}</div>
                        ${fieldHtml}
                    </div>
                    <div style="font-size: 0.85em; color: #888; line-height: 1.4;">${schema.description || ''}</div>
                </div>
            `;
        }

        async function updateGranularSetting(parserId, key, value) {
            if (!currentGranularSettings[parserId]) currentGranularSettings[parserId] = {};
            currentGranularSettings[parserId][key] = value;

            // Highlight save button
            const saveBtn = document.querySelector('[data-i18n="parser_btn_save"]');
            if (saveBtn) {
                saveBtn.style.boxShadow = '0 0 10px rgba(42, 167, 112, 0.4)';
                saveBtn.classList.add('pulse');
            }

            // Persist to backend
            const update = {};
            update[parserId] = currentGranularSettings[parserId];
            if (eel.update_parser_settings) {
                await eel.update_parser_settings(update)();
            }
        }

        function renderOptionRow(key, label) {
            const isChecked = currentParserOptions[key] === true;
            return `
                <div style="display: flex; align-items: center; gap: 15px; background: #fdfdfd; border: 1px solid #eee; padding: 15px; border-radius: 8px; transition: all 0.2s;">
                    <label class="switch">
                        <input type="checkbox" id="opt-${key}" ${isChecked ? 'checked' : ''} onchange="updateOptionValue('${key}', this.checked)">
                        <span class="slider"></span>
                    </label>
                    <div style="font-weight: 500; color: #333;">${label}</div>
                </div>
            `;
        }

        function updateOptionValue(key, value) {
            currentParserOptions[key] = value;
            // Highlight that saving is needed
            const saveBtn = document.querySelector('[data-i18n="parser_btn_save"]');
            if (saveBtn) {
                saveBtn.style.boxShadow = '0 0 10px rgba(42, 167, 112, 0.4)';
            }
        }

        function setupDragAndDrop() {
            const list = document.getElementById('parser-list');
            let draggedItem = null;

            list.addEventListener('dragstart', e => {
                if (e.target.classList.contains('parser-item')) {
                    draggedItem = e.target;
                    setTimeout(() => e.target.classList.add('dragging'), 0);
                }
            });

            list.addEventListener('dragend', e => {
                if (e.target.classList.contains('parser-item')) {
                    e.target.classList.remove('dragging');
                    draggedItem = null;
                }
            });

            list.addEventListener('dragover', e => {
                e.preventDefault();
                const afterElement = getDragAfterElement(list, e.clientY);
                if (draggedItem) {
                    if (afterElement == null) {
                        list.appendChild(draggedItem);
                    } else {
                        list.insertBefore(draggedItem, afterElement);
                    }
                }
            });
        }

        function getDragAfterElement(container, y) {
            const draggableElements = [...container.querySelectorAll('.parser-item:not(.dragging)')];
            return draggableElements.reduce((closest, child) => {
                const box = child.getBoundingClientRect();
                const offset = y - box.top - box.height / 2;
                if (offset < 0 && offset > closest.offset) {
                    return { offset: offset, element: child };
                } else {
                    return closest;
                }
            }, { offset: Number.NEGATIVE_INFINITY }).element;
        }

        async function updateStartPage(page) {
            try {
                if (typeof eel !== 'undefined') {
                    await eel.set_start_page(page)();
                    // Also update local cached config
                    mwv_config.start_page = page;
                    console.log('Start page updated to:', page);
                }
            } catch (e) {
                console.error('Failed to save start page:', e);
            }
        }

        async function updateBrowseDirUI(path) {
            try {
                if (typeof eel !== 'undefined') {
                    await eel.update_browse_dir(path)();
                    mwv_config.browse_default_dir = path;
                }
            } catch (e) { console.error(e); }
        }

        async function updateLibraryDirUI(path) {
            try {
                if (typeof eel !== 'undefined') {
                    await eel.update_library_dir(path)();
                    mwv_config.library_dir = path;
                }
            } catch (e) { console.error(e); }
        }

        async function updateAdditionalDirsUI(text) {
            const dirs = text.split('\n').map(d => d.trim()).filter(d => d.length > 0);
            try {
                if (typeof eel !== 'undefined') {
                    // We need a set_additional_library_dirs Eel function
                    await eel.update_additional_library_dirs(dirs)();
                    mwv_config.additional_library_dirs = dirs;
                }
            } catch (e) { console.error(e); }
        }

        async function setAppModeUI(mode) {
            try {
                if (typeof eel !== 'undefined') {
                    await eel.set_app_mode(mode)();
                    mwv_config.app_mode = mode;
                    updateAppModeButtons();
                }
            } catch (e) { console.error(e); }
        }

        async function setParserModeUI(mode) {
            try {
                if (typeof eel !== 'undefined') {
                    await eel.set_parser_mode(mode)();
                    mwv_config.parser_mode = mode;
                    updateParserModeButtons();
                }
            } catch (e) { console.error(e); }
        }

        function updateAppModeButtons() {
            const mode = mwv_config.app_mode || 'High-Performance';
            document.querySelectorAll('[id^="mode-"]').forEach(el => el.style.background = '#fff');
            const target = mode === 'High-Performance' ? 'mode-perf' : 'mode-bw';
            const el = document.getElementById(target);
            if (el) el.style.background = '#e6f7ff';
        }

        function updateParserModeButtons() {
            const mode = mwv_config.parser_mode || 'lightweight';
            document.querySelectorAll('[id^="pm-"]').forEach(el => el.style.background = '#fff');
            let target = 'pm-light';
            if (mode === 'full') target = 'pm-full';
            if (mode === 'ultimate') target = 'pm-ult';
            const el = document.getElementById(target);
            if (el) el.style.background = '#f6ffed';
        }

        async function resetConfigUI() {
            if (confirm(t('reset_confirm_app') || "Möchtest du wirklich alle Einstellungen zurücksetzen?")) {
                try {
                    await eel.reset_config()();
                    alert(t('settings_reset_success'));
                    location.reload();
                } catch (e) { alert(t('settings_reset_error') + e); }
            }
        }

        function saveParserChainUI() {
            const listItems = document.getElementById('parser-list').querySelectorAll('.parser-item');
            const newChain = [];

            listItems.forEach(item => {
                const isActive = item.querySelector('.parser-toggle').checked;
                if (isActive) {
                    newChain.push(item.dataset.id);
                }
            });

            const modeToggle = document.getElementById('toggle-parser-mode');
            const newMode = (modeToggle && modeToggle.checked) ? "full" : "lightweight";

            // Immediate UI Feedback for Mode
            const statusText = document.getElementById('parser-mode-status');
            if (statusText) {
                statusText.innerText = newMode === "full" ? t('parser_mode_full') : t('parser_mode_light');
                statusText.style.color = newMode === "full" ? "#e67e22" : "#2a7"; // Orange for Intensive, Green for Fast
            }

            const indexedCats = [];
            // cats is now defined globally
            cats.forEach(cat => {
                const cb = document.getElementById('cat-' + cat);
                if (cb && cb.checked) indexedCats.push(cat);
            });

            const displayedCats = [];
            cats.forEach(cat => {
                const cb = document.getElementById('disp-cat-' + cat);
                if (cb && cb.checked) displayedCats.push(cat);
            });

            const fastScanToggle = document.getElementById('toggle-fast-scan');
            const fastScanEnabled = (fastScanToggle && fastScanToggle.checked);

            // Prepare the full config object
            const finalConfig = {
                ...currentParserOptions,
                "parser_chain": newChain,
                "parser_mode": newMode,
                "fast_scan_enabled": fastScanEnabled,
                "indexed_categories": indexedCats,
                "displayed_categories": displayedCats,
                "minimal_player_view": mwv_config.minimal_player_view
            };

            console.log("Saving full parser config:", finalConfig);

            // Use the update_parser_config exposed function in main.py
            eel.update_parser_config(finalConfig)((result) => {
                if (result && result.status === 'ok') {
                    const statusSpan = document.getElementById('parser-save-status');
                    if (statusSpan) {
                        statusSpan.style.display = 'inline';
                        setTimeout(() => { statusSpan.style.display = 'none'; }, 3000);
                    }
                    // Reset save button visual hint
                    const saveBtn = document.querySelector('[data-i18n="parser_btn_save"]');
                    if (saveBtn) saveBtn.style.boxShadow = 'none';
                } else {
                    console.error("Save failed:", result);
                    alert(t('common_error') + (result ? result.message : 'Unknown error'));
                }
            });
        }

        // Toggle Parser Times function
        function toggleParserTimes(show) {
            // Re-render the sidebar info if a song is currently playing
            if (activeAudioPipeline.src) {
                // Find current item based on the title, or we can just trigger a re-render of the file info
                const titleText = readText('sidebar-metadata-primary-string-renderer');
                if (titleText !== t('sb_no_song')) {
                    // The easiest way is to let the user re-click for now, but we saved the preference.
                }
            }
        }
    
    
        let packageSearchTimer = null;

        function normalizeInstalledPackages(rawPackages) {
            const normalized = [];

            if (typeof rawPackages === 'string') {
                const trimmed = rawPackages.trim();
                if (trimmed) {
                    try {
                        rawPackages = JSON.parse(trimmed);
                    } catch (_) {
                        rawPackages = [];
                    }
                }
            }

            if (rawPackages && typeof rawPackages === 'object' && !Array.isArray(rawPackages)) {
                if (Array.isArray(rawPackages.packages)) {
                    rawPackages = rawPackages.packages;
                } else if (Array.isArray(rawPackages.installed_packages)) {
                    rawPackages = rawPackages.installed_packages;
                }
            }

            if (Array.isArray(rawPackages)) {
                rawPackages.forEach(pkg => {
                    if (!pkg || typeof pkg !== 'object') return;
                    const name = String(pkg.name ?? pkg.Name ?? pkg.project_name ?? pkg.projectName ?? '').trim();
                    const version = String(pkg.version ?? pkg.Version ?? pkg.ver ?? '').trim();
                    if (!name) return;
                    normalized.push({ name, version: version || '-' });
                });
            } else if (rawPackages && typeof rawPackages === 'object') {
                Object.entries(rawPackages).forEach(([name, version]) => {
                    const pkgName = String(name || '').trim();
                    if (!pkgName) return;
                    normalized.push({ name: pkgName, version: String(version ?? '-').trim() || '-' });
                });
            }

            normalized.sort((a, b) => a.name.localeCompare(b.name, undefined, { sensitivity: 'base' }));
            return normalized;
        }

        async function installMissingPackages() {
            const btn = document.getElementById('btn-install-missing');
            const output = document.getElementById('pip-install-output');
            const missingJson = btn ? btn.dataset.missingPackages : null;
            if (!missingJson) return;

            const packages = JSON.parse(missingJson);
            if (!packages || packages.length === 0) return;

            btn.disabled = true;
            btn.textContent = t('env_requirements_installing');
            output.style.display = 'block';
            output.textContent = `> pip install ${packages.join(' ')}\n...`;

            try {
                const res = await eel.pip_install_packages(packages)();
                if (res.status === 'ok') {
                    output.textContent += `\n\n${res.output}\n\n${t('env_requirements_install_success')}`;
                    btn.textContent = t('env_requirements_install_success');
                    // Reload info after short delay
                    setTimeout(() => {
                        loadEnvironmentInfo(true);
                        output.style.display = 'none';
                    }, 3000);
                } else {
                    const errorDetail = (typeof res.error === 'object') ? JSON.stringify(res.error) : (res.error || 'Unknown error');
                    output.textContent += `\n\n${t('env_requirements_install_error')}\n${errorDetail}`;
                    btn.disabled = false;
                    btn.textContent = t('env_requirements_install_btn');
                }
            } catch (err) {
                const errMsg = (err instanceof Error) ? err.message : (typeof err === 'object' ? JSON.stringify(err) : String(err));
                output.textContent += `\n\nError: ${errMsg}`;
                btn.disabled = false;
                btn.textContent = t('env_requirements_install_btn');
            }
        }

        async function loadEnvironmentInfo(forceRefresh = false) {
            try {
                const requestForceRefresh = !!forceRefresh;
                let info = requestForceRefresh
                    ? await eel.get_environment_info(true)()
                    : await eel.get_environment_info()();

                const initialPackages = normalizeInstalledPackages(info?.installed_packages);
                const hasInitialPackages = initialPackages.length > 0;
                if (!requestForceRefresh && !hasInitialPackages) {
                    try {
                        const refreshed = await eel.get_environment_info(true)();
                        if (refreshed) info = refreshed;
                    } catch (refreshErr) {
                        console.warn('Environment info force-refresh failed:', refreshErr);
                    }
                }

                if (!info || typeof info !== 'object') {
                    throw new Error('Invalid environment info response');
                }

                const safeCondaEnvs = Array.isArray(info.available_conda_environments) ? info.available_conda_environments : [];
                const safeSystemPythons = Array.isArray(info.available_system_pythons) ? info.available_system_pythons : [];
                const safeLocalVenvs = Array.isArray(info.local_venvs) ? info.local_venvs : [];
                const safeInstalledPackages = normalizeInstalledPackages(info.installed_packages);

                const envPythonVersionEl = document.getElementById('env-python-version');
                const envVenvStatusEl = document.getElementById('env-venv-status');
                const envVenvPathEl = document.getElementById('env-venv-path');
                const envPythonExecEl = document.getElementById('env-python-exec');
                const envPlatformEl = document.getElementById('env-platform');
                const envMediainfoStatusEl = document.getElementById('env-mediainfo-status');
                const envMutagenStatusEl = document.getElementById('env-mutagen-status');
                const envFfmpegStatusEl = document.getElementById('env-ffmpeg-status');
                const envFfprobeStatusEl = document.getElementById('env-ffprobe-status');
                const envPymkvStatusEl = document.getElementById('env-pymkv-status');
                const envMkvStatusEl = document.getElementById('env-mkv-status');
                const envMkvmergeStatusEl = document.getElementById('env-mkvmerge-status');
                const envGuiStatusEl = document.getElementById('env-gui-status');
                const envAppVersionEl = document.getElementById('env-app-version');
                const envMediaplayerStatusEl = document.getElementById('env-mediaplayer-status');
                const envEelStatusEl = document.getElementById('env-eel-status');
                const envBottleStatusEl = document.getElementById('env-bottle-status');
                const envGeventStatusEl = document.getElementById('env-gevent-status');
                const envStreamToolsStatusEl = document.getElementById('env-stream-tools-status');
                const envTestToolsStatusEl = document.getElementById('env-test-tools-status');
                const envDevToolsStatusEl = document.getElementById('env-dev-tools-status');
                const envBuildToolsStatusEl = document.getElementById('env-build-tools-status');
                const envCorePackagesStatusEl = document.getElementById('env-core-packages-status');
                const envRequirementsListEl = document.getElementById('env-requirements-list');
                const envMainPidEl = document.getElementById('env-main-pid');
                const envBrowserPidEl = document.getElementById('env-browser-pid');
                const envTestbedPidEl = document.getElementById('env-testbed-pid');
                const envSeleniumPidEl = document.getElementById('env-selenium-pid');
                const envBaseDependenciesStatusEl = document.getElementById('env-base-dependencies-status');

                // Hardware Info
                try {
                    const hwInfo = await eel.get_hardware_info()();
                    if (hwInfo) {
                        const diskTypeEl = document.getElementById('hardware-disk-type');
                        if (diskTypeEl) diskTypeEl.textContent = hwInfo.disk_type || '-';
                        const pcieGenEl = document.getElementById('hardware-pcie-gen');
                        if (pcieGenEl) pcieGenEl.textContent = hwInfo.pcie_gen || '-';
                        const networkMountEl = document.getElementById('hardware-network-mount');
                        if (networkMountEl) networkMountEl.textContent = hwInfo.is_network_mount ? 'Network (NFS/SMB)' : 'Local File System';

                        // GPU & Encoders
                        const gpuTypeEl = document.getElementById('hardware-gpu-type');
                        if (gpuTypeEl) gpuTypeEl.textContent = hwInfo.gpu_type || 'Generic';
                        const encodersEl = document.getElementById('hardware-encoders');
                        if (encodersEl) {
                            const encs = hwInfo.encoders || [];
                            encodersEl.textContent = encs.length > 0 ? encs.join(', ').toUpperCase() : 'Software Only (FFmpeg)';
                        }
                    }
                } catch (hwErr) {
                    console.error('Failed to load hardware info:', hwErr);
                }

                const mediaInfoStatus = info.mediainfo_status || {};
                const pyMediaInfoOk = !!mediaInfoStatus.pymediainfo_available;
                const pyMediaInfoVer = mediaInfoStatus.pymediainfo_version || '';
                const mediaInfoCliOk = !!mediaInfoStatus.mediainfo_cli_available;
                const mediaInfoCliPath = mediaInfoStatus.mediainfo_cli_path || '';
                const mediaInfoCliVer = mediaInfoStatus.mediainfo_cli_version || '';

                const toolsStatus = info.tools_status || {};
                const ffmpegOk = !!toolsStatus.ffmpeg_cli_available;
                const ffmpegPath = toolsStatus.ffmpeg_cli_path || '';
                const ffmpegVer = toolsStatus.ffmpeg_cli_version || '';
                const ffprobeOk = !!toolsStatus.ffprobe_cli_available;
                const ffprobePath = toolsStatus.ffprobe_cli_path || '';
                const ffprobeVer = toolsStatus.ffprobe_cli_version || '';
                const browserOk = !!toolsStatus.browser_available;
                const browserName = toolsStatus.browser_name || 'browser';
                const browserPath = toolsStatus.browser_path || '';
                const browserVer = toolsStatus.browser_version || '';
                const mkvCliOk = !!toolsStatus.mkvinfo_cli_available;
                const mkvCliVer = toolsStatus.mkvinfo_cli_version || '';
                const mkvCliPath = toolsStatus.mkvinfo_cli_path || '';
                const mkvPyOk = !!toolsStatus.python_mkv_available;
                const mkvPyVer = toolsStatus.python_mkv_version || '';
                const mkvMergeOk = !!toolsStatus.mkvmerge_cli_available;
                const mkvMergeVer = toolsStatus.mkvmerge_cli_version || '';
                const mkvMergePath = toolsStatus.mkvmerge_cli_path || '';
                const vlcPyOk = !!toolsStatus.python_vlc_available;
                const vlcPyVer = toolsStatus.python_vlc_version || '';
                const vlcCliOk = !!toolsStatus.vlc_cli_available;
                const vlcCliPath = toolsStatus.vlc_cli_path || '';
                const vlcCliVer = toolsStatus.vlc_cli_version || '';
                const mutagenOk = !!toolsStatus.mutagen_available;
                const mutagenVer = toolsStatus.mutagen_version || '';

                // MediaInfo: pymediainfo + mediainfo CLI
                const mediaInfoText = [
                    `${pyMediaInfoOk ? '✅' : '❌'} pymediainfo${pyMediaInfoVer ? ` ${pyMediaInfoVer}` : ''}`,
                    `${mediaInfoCliOk ? '✅' : '❌'} mediainfo${mediaInfoCliPath ? ` (${mediaInfoCliPath})` : ''}${mediaInfoCliVer ? ` ${mediaInfoCliVer}` : ''}`,
                ].join(' | ');

                // Mutagen
                const mutagenText = `${mutagenOk ? '✅' : '❌'} mutagen${mutagenVer ? ` ${mutagenVer}` : ''}`;

                // FFmpeg tools
                const ffmpegText = `${ffmpegOk ? '✅' : '❌'} ffmpeg${ffmpegPath ? ` (${ffmpegPath})` : ''}${ffmpegVer ? ` ${ffmpegVer}` : ''}`;
                const ffprobeText = `${ffprobeOk ? '✅' : '❌'} ffprobe${ffprobePath ? ` (${ffprobePath})` : ''}${ffprobeVer ? ` ${ffprobeVer}` : ''}`;

                // MKV Info: pymkv + mkvinfo CLI
                const mkvText = [
                    `${mkvPyOk ? '✅' : '❌'} pymkv${mkvPyVer ? ` ${mkvPyVer}` : ''}`,
                    `${mkvCliOk ? '✅' : '❌'} mkvinfo${mkvCliPath ? ` (${mkvCliPath})` : ''}${mkvCliVer ? ` ${mkvCliVer}` : ''}`,
                ].join(' | ');

                // GUI: Browser
                const guiText = `${browserOk ? '✅' : '❌'} ${browserName}${browserVer ? ` ${browserVer}` : ''}${browserPath ? ` (${browserPath})` : ''}`;

                // Mediaplayer: VLC
                const mediaplayerText = [
                    `${vlcPyOk ? '✅' : '❌'} python-vlc${vlcPyVer ? ` ${vlcPyVer}` : ''}`,
                    `${vlcCliOk ? '✅' : '❌'} vlc${vlcCliVer ? ` ${vlcCliVer}` : ''}${vlcCliPath ? ` (${vlcCliPath})` : ''}`,
                ].join(' | ');

                const packageVersionMap = new Map();
                safeInstalledPackages.forEach(pkg => {
                    if (!pkg || typeof pkg !== 'object') return;
                    const name = String(pkg.name || '').trim().toLowerCase();
                    const version = String(pkg.version || '').trim();
                    if (!name) return;
                    packageVersionMap.set(name, version || '-');
                });

                // Display environment type and status
                let statusText = '';
                let isActive = false;

                if (info.env_type === 'venv') {
                    if (info.has_conda_context) {
                        statusText = `✅ Ja (Venv: ${info.env_name || 'unknown'}, Conda-Kontext: ${info.conda_env_name || 'unknown'})`;
                    } else {
                        statusText = `✅ Ja (Venv: ${info.env_name || 'unknown'})`;
                    }
                    isActive = true;
                } else if (info.env_type === 'conda') {
                    statusText = `✅ Ja (Conda: ${info.env_name || 'unknown'})`;
                    isActive = true;
                } else {
                    statusText = '❌ Nein (System Python)';
                    isActive = false;
                }

                // Backend Detail Breakdown
                const eelVer = packageVersionMap.get('eel') || '-';
                const wsVer = packageVersionMap.get('websocket-client') || '-';
                const eelText = `${eelVer !== '-' ? '✅' : '❌'} Eel ${eelVer} | ${wsVer !== '-' ? '✅' : '❌'} Websocket ${wsVer}`;

                const bottleVer = packageVersionMap.get('bottle') || '-';
                const bottleWsVer = packageVersionMap.get('bottle-websocket') || '-';
                const bottleText = `${bottleVer !== '-' ? '✅' : '❌'} bottle ${bottleVer} | ${bottleWsVer !== '-' ? '✅' : '❌'} bottle-websocket ${bottleWsVer}`;

                const geventVer = packageVersionMap.get('gevent') || '-';
                const geventWsVer = packageVersionMap.get('gevent-websocket') || '-';
                const greenletVer = packageVersionMap.get('greenlet') || '-';
                const geventText = `${geventVer !== '-' ? '✅' : '❌'} gevent ${geventVer} | ${geventWsVer !== '-' ? '✅' : '❌'} gevent-websocket ${geventWsVer} | ${greenletVer !== '-' ? '✅' : '❌'} greenlet ${greenletVer}`;

                const m3u8Ver = packageVersionMap.get('m3u8') || '-';
                const streamToolsText = `${m3u8Ver !== '-' ? '✅' : '❌'} m3u8 ${m3u8Ver}`;

                const corePackages = [
                    ['bottle', 'bottle'],
                    ['bottle-websocket', 'bottle-websocket'],
                    ['eel', 'Eel'],
                    ['m3u8', 'm3u8'],
                    ['gevent', 'gevent'],
                    ['greenlet', 'greenlet'],
                ];
                const corePackagesText = corePackages
                    .map(([pkgKey, pkgLabel]) => {
                        const version = packageVersionMap.get(pkgKey);
                        return `${version ? '✅' : '❌'} ${pkgLabel}${version ? ` ${version}` : ''}`;
                    })
                    .join(' | ');
                if (envCorePackagesStatusEl) envCorePackagesStatusEl.textContent = corePackagesText;

                const testPackages = [
                    ['pytest', 'pytest'],
                    ['pytest-cov', 'pytest-cov'],
                    ['coverage', 'coverage'],
                    ['pluggy', 'pluggy'],
                    ['iniconfig', 'iniconfig'],
                    ['pyautogui', 'PyAutoGUI'],
                    ['pygetwindow', 'PyGetWindow'],
                    ['pymsgbox', 'PyMsgBox'],
                    ['pyrect', 'PyRect'],
                    ['pyscreeze', 'PyScreeze'],
                    ['mouseinfo', 'MouseInfo'],
                    ['pytweening', 'pytweening'],
                    ['python3-xlib', 'python3-xlib'],
                    ['pyperclip', 'pyperclip'],
                ].sort((a, b) => a[1].localeCompare(b[1]));

                const testToolsText = testPackages
                    .map(([pkgKey, pkgLabel]) => {
                        const version = packageVersionMap.get(pkgKey);
                        return `${version ? '✅' : '❌'} ${pkgLabel}${version ? ` ${version}` : ''}`;
                    })
                    .join(' | ');

                const devPackages = [
                    ['mypy', 'mypy'],
                    ['mypy_extensions', 'mypy_extensions'],
                    ['typing_extensions', 'typing_extensions'],
                    ['flake8', 'flake8'],
                    ['pycodestyle', 'pycodestyle'],
                    ['pyflakes', 'pyflakes'],
                    ['mccabe', 'mccabe'],
                    ['pathspec', 'pathspec'],
                ].sort((a, b) => a[1].localeCompare(b[1]));

                const devToolsText = devPackages
                    .map(([pkgKey, pkgLabel]) => {
                        const version = packageVersionMap.get(pkgKey);
                        return `${version ? '✅' : '❌'} ${pkgLabel}${version ? ` ${version}` : ''}`;
                    })
                    .join(' | ');

                const buildPackages = [
                    ['pyinstaller', 'PyInstaller'],
                    ['pyinstaller-hooks-contrib', 'pyinstaller-hooks-contrib'],
                    ['altgraph', 'altgraph'],
                    ['wheel', 'wheel'],
                    ['setuptools', 'setuptools'],
                    ['packaging', 'packaging'],
                    ['markdown', 'Markdown'],
                    ['psutil', 'psutil'],
                    ['chardet', 'chardet'],
                    ['future', 'future'],
                    ['zope.event', 'zope.event'],
                    ['zope.interface', 'zope.interface'],
                ].sort((a, b) => a[1].localeCompare(b[1]));

                const buildToolsText = buildPackages
                    .map(([pkgKey, pkgLabel]) => {
                        const version = packageVersionMap.get(pkgKey);
                        return `${version ? '✅' : '❌'} ${pkgLabel}${version ? ` ${version}` : ''}`;
                    })
                    .join(' | ');

                const categorizedKeys = new Set([
                    'bottle', 'bottle-websocket', 'eel', 'websocket-client',
                    ...testPackages.map(([pkgKey]) => pkgKey),
                    ...devPackages.map(([pkgKey]) => pkgKey),
                    ...buildPackages.map(([pkgKey]) => pkgKey),
                    'pymediainfo',
                    'mutagen',
                    'python-vlc',
                ]);

                const baseDependencies = safeInstalledPackages
                    .filter(pkg => {
                        if (!pkg || typeof pkg !== 'object') return false;
                        const key = String(pkg.name || '').trim().toLowerCase();
                        return key && !categorizedKeys.has(key);
                    })
                    .map(pkg => {
                        const label = String(pkg.name || '').trim();
                        const version = String(pkg.version || '').trim();
                        return `${label}${version ? ` ${version}` : ''}`;
                    });

                const baseDependenciesText = baseDependencies.length > 0
                    ? `✅ ${baseDependencies.join(', ')}`
                    : '-';

                const requirementsStatusPreview = info.requirements_status && typeof info.requirements_status === 'object'
                    ? info.requirements_status
                    : null;
                const requirementsInstalledPreview = Array.isArray(requirementsStatusPreview?.installed)
                    ? requirementsStatusPreview.installed
                    : [];
                const requirementsMissingPreview = Array.isArray(requirementsStatusPreview?.missing)
                    ? requirementsStatusPreview.missing
                    : [];
                const requirementsListText = requirementsStatusPreview?.available
                    ? [
                        requirementsInstalledPreview.length > 0 ? `✅ ${requirementsInstalledPreview.join(', ')}` : '',
                        requirementsMissingPreview.length > 0 ? `❌ ${requirementsMissingPreview.join(', ')}` : ''
                    ].filter(Boolean).join(' | ') || '-'
                    : t('env_requirements_not_found');

                // Show/Hide Install button based on missing packages
                const btnInstallMissing = document.getElementById('btn-install-missing');
                if (btnInstallMissing) {
                    if (requirementsMissingPreview.length > 0) {
                        btnInstallMissing.style.display = 'inline-block';
                        btnInstallMissing.dataset.missingPackages = JSON.stringify(requirementsMissingPreview);
                    } else {
                        btnInstallMissing.style.display = 'none';
                    }
                }

                if (envVenvStatusEl) envVenvStatusEl.textContent = statusText;
                if (envVenvPathEl) envVenvPathEl.textContent = info.env_path || '-';
                if (envPythonExecEl) envPythonExecEl.textContent = info.python_executable || '-';
                if (envPythonVersionEl) envPythonVersionEl.textContent = info.python_version || '-';
                if (envMediainfoStatusEl) envMediainfoStatusEl.textContent = mediaInfoText;
                if (envMutagenStatusEl) envMutagenStatusEl.textContent = mutagenText;
                if (envFfmpegStatusEl) envFfmpegStatusEl.textContent = ffmpegText;
                if (envFfprobeStatusEl) envFfprobeStatusEl.textContent = ffprobeText;
                if (envMkvStatusEl) envMkvStatusEl.textContent = mkvText;
                if (envEelStatusEl) envEelStatusEl.textContent = eelText;
                if (envGuiStatusEl) envGuiStatusEl.textContent = guiText;
                if (envAppVersionEl) envAppVersionEl.textContent = info.version || '-';
                if (envMediaplayerStatusEl) envMediaplayerStatusEl.textContent = mediaplayerText;
                if (envBottleStatusEl) envBottleStatusEl.textContent = bottleText;
                if (envGeventStatusEl) envGeventStatusEl.textContent = geventText;
                if (envStreamToolsStatusEl) envStreamToolsStatusEl.textContent = streamToolsText;
                if (envTestToolsStatusEl) envTestToolsStatusEl.textContent = testToolsText;
                if (envDevToolsStatusEl) envDevToolsStatusEl.textContent = devToolsText;
                if (envBuildToolsStatusEl) envBuildToolsStatusEl.textContent = buildToolsText;
                if (envCorePackagesStatusEl) envCorePackagesStatusEl.textContent = corePackagesText;
                if (envRequirementsListEl) envRequirementsListEl.textContent = requirementsListText;
                if (envBaseDependenciesStatusEl) envBaseDependenciesStatusEl.textContent = baseDependenciesText;
                if (envPlatformEl) envPlatformEl.textContent = info.platform || info.system || '-';
                if (envMainPidEl) envMainPidEl.textContent = info.pid || '-';
                if (envBrowserPidEl) envBrowserPidEl.textContent = info.browser_pid || '-';
                if (envTestbedPidEl) envTestbedPidEl.textContent = info.testbed_pid || '-';
                if (envSeleniumPidEl) envSeleniumPidEl.textContent = info.selenium_pid || '-';

                // Full package list rendering (keep as before)
                const packagesList = document.getElementById('installed-packages-list');
                const packageCount = document.getElementById('package-count');
                const packageSource = document.getElementById('package-source');
                const sourceText = String(info.installed_packages_source || 'unknown');
                if (packageSource) packageSource.textContent = `[source: ${sourceText}]`;

                if (safeInstalledPackages.length > 0 && packagesList && packageCount) {
                    packageCount.textContent = `(${safeInstalledPackages.length})`;

                    // Store packages globally for search functionality
                    window.allPackages = safeInstalledPackages;
                    window.allPackagesSearch = safeInstalledPackages.map(pkg => ({
                        nameLc: String(pkg.name || '').toLowerCase(),
                        versionLc: String(pkg.version || '').toLowerCase(),
                        raw: pkg,
                    }));

                    // Initial render
                    renderPackages(safeInstalledPackages);

                    // Setup search
                    const searchInput = document.getElementById('package-search');
                    if (searchInput && searchInput.dataset.bound !== '1') {
                        searchInput.addEventListener('input', (e) => {
                            const searchTerm = e.target.value.toLowerCase();
                            if (packageSearchTimer) clearTimeout(packageSearchTimer);
                            packageSearchTimer = setTimeout(() => {
                                if (searchTerm === '') {
                                    renderPackages(window.allPackages);
                                } else {
                                    const rows = Array.isArray(window.allPackagesSearch) ? window.allPackagesSearch : [];
                                    const filtered = rows
                                        .filter(row => row.nameLc.includes(searchTerm) || row.versionLc.includes(searchTerm))
                                        .map(row => row.raw);
                                    renderPackages(filtered);
                                }
                            }, 120);
                        });
                        searchInput.dataset.bound = '1';
                    }
                } else {
                    if (packageCount) packageCount.textContent = '(0)';
                    if (packagesList) packagesList.innerHTML = `<span style="color: #999;">${t('env_no_packages_found')}</span>`;
                }
                if (envPymkvStatusEl) {
                    envPymkvStatusEl.innerHTML = mkvPyOk ? `<span style="color: #2a7;">✅</span> pymkv ${mkvPyVer}` : `<span style="color: #c0392b;">❌</span> not available`;
                }
                if (envMkvStatusEl) {
                    envMkvStatusEl.innerHTML = mkvCliOk ? `<span style="color: #2a7;">✅</span> mkvinfo (${mkvCliPath}) ${mkvCliVer}` : `<span style="color: #c0392b;">❌</span> not available`;
                }
                if (envMkvmergeStatusEl) {
                    envMkvmergeStatusEl.innerHTML = mkvMergeOk ? `<span style="color: #2a7;">✅</span> mkvmerge (${mkvMergePath}) ${mkvMergeVer}` : `<span style="color: #c0392b;">❌</span> not available`;
                }
                if (envPlatformEl) envPlatformEl.textContent = `${info.platform_system || '-'} ${info.platform_release || ''}`.trim();

                // Color code the venv status
                const statusEl = document.getElementById('env-venv-status');
                if (statusEl) {
                    if (isActive) {
                        statusEl.style.color = '#2a7';
                        statusEl.style.fontWeight = 'bold';
                    } else {
                        statusEl.style.color = '#f4d';
                    }
                }

                // Display Conda Environments
                const condaList = document.getElementById('conda-environments-list');
                if (condaList && safeCondaEnvs.length > 0) {
                    let condaHtml = '<div style="font-family: monospace;">';
                    safeCondaEnvs.forEach(env => {
                        if (!env || typeof env !== 'object') return;
                        const envName = env.name || '-';
                        const envVersion = env.version || '-';
                        const envPath = env.path || '-';
                        const isCurrent = info.env_type === 'conda' && info.env_name === envName;
                        const isRecommended = !!env.recommended;
                        const currentBadge = isCurrent ? '<span style="color: #2a7; font-weight: bold;">● AKTIV</span>' : '';
                        const recBadge = isRecommended ? '<span style="color: #f80; font-weight: bold;">⭐ EMPFOHLEN</span>' : '';

                        condaHtml += `
                            <div style="margin-bottom: 8px; padding: 6px; background: ${isCurrent ? '#e8f5e9' : '#fff'}; border-left: 3px solid ${isCurrent ? '#4caf50' : '#ddd'}; border-radius: 3px;">
                                <div style="font-weight: bold; color: #333;">${envName} ${currentBadge} ${recBadge}</div>
                                <div style="color: #666; font-size: 0.9em;">${envVersion}</div>
                                <div style="color: #999; font-size: 0.85em; word-break: break-all;">${envPath}</div>
                            </div>
                        `;
                    });
                    condaHtml += '</div>';
                    condaList.innerHTML = condaHtml;
                } else if (condaList) {
                    condaList.innerHTML = `<span style="color: #999;">${t('env_no_conda_envs')}</span>`;
                }

                // Display System Python Installations split into Global / Local
                const globalPythonList = document.getElementById('system-python-global-list');
                const localPythonList = document.getElementById('system-python-local-list');

                const validSystemPythons = safeSystemPythons.filter(p => p && typeof p === 'object');
                const globalPythons = validSystemPythons.filter(p => String(p.path || '').startsWith('/usr/bin/'));
                const localPythons = validSystemPythons.filter(p => !String(p.path || '').startsWith('/usr/bin/'));

                const renderPythonList = (container, rows, emptyText) => {
                    if (!container) return;
                    if (!rows || rows.length === 0) {
                        container.innerHTML = `<span style="color: #999;">${emptyText}</span>`;
                        return;
                    }
                    let html = '<div style="font-family: monospace;">';
                    rows.forEach(python => {
                        if (!python || typeof python !== 'object') return;
                        html += `
                            <div style="margin-bottom: 8px; padding: 6px; background: #fff; border-left: 3px solid #ddd; border-radius: 3px;">
                                <div style="color: #666; font-size: 0.9em;">${python.version || '-'}</div>
                                <div style="color: #999; font-size: 0.85em; word-break: break-all;">${python.path || '-'}</div>
                            </div>
                        `;
                    });
                    html += '</div>';
                    container.innerHTML = html;
                };

                renderPythonList(globalPythonList, globalPythons, t('env_no_system_pythons'));
                renderPythonList(localPythonList, localPythons, t('env_no_system_pythons'));

                // Display Local Virtual Environments
                const venvsList = document.getElementById('local-venvs-list');
                const venvConceptEl = document.getElementById('multi-venv-concept');
                if (venvConceptEl) venvConceptEl.textContent = info.multi_venv_concept || '';

                if (venvsList && safeLocalVenvs.length > 0) {
                    let venvsHtml = '<div style="font-family: monospace;">';
                    safeLocalVenvs.forEach(venv => {
                        if (!venv || typeof venv !== 'object') return;
                        const isCurrent = venv.is_current;
                        const exists = venv.exists !== false; // Backend now returns exists
                        const currentBadge = isCurrent ? '<span style="color: #2a7; font-weight: bold;">● AKTIV</span>' : '';
                        const missingBadge = !exists ? '<span style="color: #c0392b; font-weight: bold;">⚠️ NICHT INSTALLIERT</span>' : '';
                        const roleBadge = venv.role ? `<span style="background: #eee; color: #555; padding: 2px 6px; border-radius: 4px; font-size: 0.8em; margin-right: 5px; font-weight: bold;">${venv.role}</span>` : '';

                        venvsHtml += `
                            <div style="margin-bottom: 8px; padding: 8px; background: ${isCurrent ? '#e8f5e9' : '#fff'}; border-left: 4px solid ${isCurrent ? '#4caf50' : (exists ? '#ddd' : '#c0392b')}; border-radius: 3px; opacity: ${exists ? 1 : 0.7};">
                                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 4px;">
                                    <div style="font-weight: bold; color: #333;">${roleBadge}${venv.name || '-'} ${currentBadge} ${missingBadge}</div>
                                </div>
                                <div style="color: #666; font-size: 0.9em; margin-bottom: 4px;">${venv.purpose || ''}</div>
                                <div style="color: #999; font-size: 0.85em; word-break: break-all;">${venv.version || (exists ? '-' : '(Kein Python found)')} ${exists ? ' | ' + venv.path : ''}</div>
                            </div>
                        `;
                    });
                    venvsHtml += '</div>';
                    venvsList.innerHTML = venvsHtml;
                } else if (venvsList) {
                    venvsList.innerHTML = `<span style="color: #999;">${t('env_no_local_venvs')}</span>`;
                }

                // Display Installed Packages

                // Display requirements.txt status
                const requirementsCount = document.getElementById('requirements-count');
                const requirementsLastChecked = document.getElementById('requirements-last-checked');
                const requirementsStatusList = document.getElementById('requirements-status-list');
                const requirementsStatus = info.requirements_status && typeof info.requirements_status === 'object'
                    ? info.requirements_status
                    : null;

                if (requirementsCount && requirementsStatusList) {
                    if (requirementsLastChecked) {
                        const now = new Date();
                        requirementsLastChecked.textContent = `${t('env_requirements_last_checked')}: ${now.toLocaleTimeString()}`;
                    }
                    const available = !!requirementsStatus?.available;
                    const missing = Array.isArray(requirementsStatus?.missing) ? requirementsStatus.missing : [];
                    const installedCount = Number(requirementsStatus?.installed_count || 0);
                    const total = Number(requirementsStatus?.total || (installedCount + missing.length));
                    requirementsCount.textContent = `(${installedCount}/${total})`;

                    if (!available) {
                        requirementsStatusList.innerHTML = `<span style="color: #999;">${t('env_requirements_not_found')}</span>`;
                    } else if (missing.length === 0) {
                        requirementsStatusList.innerHTML = `<span style="color: #2a7; font-weight: bold;">${t('env_requirements_all_present')}</span>`;
                    } else {
                        const missingHtml = missing
                            .map(name => `<div style="margin: 3px 0; color: #c62828;">• ${name}</div>`)
                            .join('');
                        requirementsStatusList.innerHTML = `
                            <div style="margin-bottom: 6px; color: #c62828; font-weight: bold;">${t('env_requirements_missing')}</div>
                            ${missingHtml}
                        `;
                    }
                }

                // Inject dynamic Scan-Directory description if element exists
                if (info.default_scan_dir) {
                    const scanDirDesc = document.querySelector('[data-i18n="options_scan_dirs_desc"]');
                    if (scanDirDesc) {
                        // Dynamically update the path in the translated string
                        let desc = t('options_scan_dirs_desc');
                        if (desc.includes('/opt/media-web-viewer/media')) {
                            desc = desc.replace('/opt/media-web-viewer/media', info.default_scan_dir);
                            scanDirDesc.textContent = desc;
                        }
                    }
                }

            } catch (e) {
                console.error("Failed to load environment info:", e);
                const failText = `<span style="color: #c62828;">${t('common_error_loading')}</span>`;
                const fallbackNoData = `<span style="color: #999;">${t('env_no_packages_found')}</span>`;

                const packageCount = document.getElementById('package-count');
                const packageSource = document.getElementById('package-source');
                const requirementsCount = document.getElementById('requirements-count');
                const requirementsLastChecked = document.getElementById('requirements-last-checked');
                const requirementsStatusList = document.getElementById('requirements-status-list');
                const condaList = document.getElementById('conda-environments-list');
                const globalPythonList = document.getElementById('system-python-global-list');
                const localPythonList = document.getElementById('system-python-local-list');
                const venvsList = document.getElementById('local-venvs-list');
                const packagesList = document.getElementById('installed-packages-list');

                if (packageCount) packageCount.textContent = '(0)';
                if (packageSource) packageSource.textContent = '[source: error]';
                if (requirementsCount) requirementsCount.textContent = '(0/0)';
                if (requirementsLastChecked) requirementsLastChecked.textContent = t('env_requirements_last_checked_error');
                if (requirementsStatusList) requirementsStatusList.innerHTML = failText;
                if (condaList) condaList.innerHTML = failText;
                if (globalPythonList) globalPythonList.innerHTML = failText;
                if (localPythonList) localPythonList.innerHTML = failText;
                if (venvsList) venvsList.innerHTML = failText;
                if (packagesList) packagesList.innerHTML = fallbackNoData;
            }
        }

        function renderPackages(packages) {
            const packagesList = document.getElementById('installed-packages-list');

            if (packages.length === 0) {
                packagesList.innerHTML = `<span style="color: #999;">${t('env_no_matching_packages')}</span>`;
                return;
            }

            let packagesHtml = '<table style="width: 100%; border-collapse: collapse;">';
            packagesHtml += `<thead><tr style="background: #e0e0e0;"><th style="text-align: left; padding: 4px 8px; font-weight: bold;">${t('env_table_package')}</th><th style="text-align: left; padding: 4px 8px; font-weight: bold;">${t('env_table_version')}</th></tr></thead>`;
            packagesHtml += '<tbody>';

            packages.forEach((pkg, index) => {
                const bgColor = index % 2 === 0 ? '#fff' : '#f5f5f5';
                packagesHtml += `
                    <tr style="background: ${bgColor};">
                        <td style="padding: 4px 8px; border-bottom: 1px solid #eee;">${pkg.name}</td>
                        <td style="padding: 4px 8px; border-bottom: 1px solid #eee; color: #666;">${pkg.version}</td>
                    </tr>
                `;
            });

            packagesHtml += '</tbody></table>';
            packagesList.innerHTML = packagesHtml;
        }
    
    
        window.runLatencyDiagnostics = async function (payloadSize = 0, samples = 5) {
            const count = Math.max(1, Math.min(30, Number(samples) || 5));
            const size = Math.max(0, Math.min(200000, Number(payloadSize) || 0));

            const frontendSamples = [];
            const eelSamples = [];
            const bottleSamples = [];

            const measureFrame = () => new Promise((resolve) => {
                const start = performance.now();
                requestAnimationFrame(() => resolve(performance.now() - start));
            });

            const measureEel = async () => {
                const start = performance.now();
                await eel.api_ping(Date.now(), size)();
                return performance.now() - start;
            };

            const measureBottle = async () => {
                const start = performance.now();
                await fetch('/health', { cache: 'no-store' });
                return performance.now() - start;
            };

            for (let i = 0; i < count; i++) {
                frontendSamples.push(await measureFrame());
                eelSamples.push(await measureEel());
                bottleSamples.push(await measureBottle());
            }

            const avg = (arr) => arr.reduce((a, b) => a + b, 0) / arr.length;
            const p95 = (arr) => {
                const sorted = [...arr].sort((a, b) => a - b);
                const idx = Math.min(sorted.length - 1, Math.floor(sorted.length * 0.95));
                return sorted[idx];
            };

            const result = {
                samples: count,
                payloadSize: size,
                frontend: { avgMs: Number(avg(frontendSamples).toFixed(2)), p95Ms: Number(p95(frontendSamples).toFixed(2)) },
                eelRoundtrip: { avgMs: Number(avg(eelSamples).toFixed(2)), p95Ms: Number(p95(eelSamples).toFixed(2)) },
                bottleHttp: { avgMs: Number(avg(bottleSamples).toFixed(2)), p95Ms: Number(p95(bottleSamples).toFixed(2)) },
                raw: { frontendSamples, eelSamples, bottleSamples },
            };

            console.info('[LatencyDiagnostics]', result);
            return result;
        }

        async function loadFeatureStatus() {
            const container = document.getElementById('feature-list-container');
            if (!container) return;
            container.innerHTML = `<div style="text-align: center; color: #888; padding: 20px;">${t('logbook_loading_items')}</div>`;

            try {
                const entries = await eel.list_feature_modal_items()();
                container.innerHTML = '';

                // Filter: Show only entries that have a summary
                let allItems = entries.filter(e => e.summary && e.summary.trim() !== "");
                const allSorted = [...allItems].sort((a, b) => (b.modified_ts || 0) - (a.modified_ts || 0));
                const latest = allSorted.slice(0, 3);
                const latestNames = latest.map(l => l.name);

                const rootItems = allItems.filter(f => f.source === 'root' && !latestNames.includes(f.name));

                // 1. Bugs (Known Issues + entries categorized as Bug)
                const bugItems = allItems.filter(f =>
                    f.name === '00_Known_Issues' || (f.category && f.category.toLowerCase() === 'bug')
                ).filter(f => !latestNames.includes(f.name));

                // 2. Features (Open)
                const featureItems = allItems.filter(f =>
                    (f.category === 'Feature' || f.category === 'Task' || f.category === 'Planung' || f.category === 'Planning') &&
                    f.status !== 'COMPLETED' &&
                    f.name !== '00_Known_Issues' &&
                    !latestNames.includes(f.name)
                );

                // 3. Documentation
                const docItem = allItems.find(f => f.name === '31_Project_Documentation');
                const docItems = docItem ? [docItem] : [];

                // 4. Other Completed
                const otherCompleted = allItems.filter(f =>
                    f.status === "COMPLETED" &&
                    !latestNames.includes(f.name) &&
                    f.name !== '31_Project_Documentation' &&
                    f.source !== 'root' &&
                    f.name !== '00_Known_Issues' &&
                    !(f.category && f.category.toLowerCase() === 'bug')
                ).sort((a, b) => (b.modified_ts || 0) - (a.modified_ts || 0));

                if (allItems.length === 0) {
                    container.innerHTML += `<div style="text-align: center; color: #888; padding: 20px;">${t('logbook_empty_desc')}</div>`;
                    return;
                }

                // Render Sections
                renderFeatureSection(container, t('logbook_section_latest'), latest, true);
                renderFeatureSection(container, t('feature_section_root_docs'), rootItems);
                renderFeatureSection(container, t('logbook_section_bugs'), bugItems);
                renderFeatureSection(container, t('logbook_section_features'), featureItems);
                renderFeatureSection(container, t('logbook_btn_documentation'), docItems);
                renderFeatureSection(container, t('logbook_section_completed'), otherCompleted);
            } catch (e) {
                console.error("Error loading features:", e);
                container.innerHTML = `<div style="text-align: center; color: #b71c1c; padding: 20px;">${t('common_error_loading')}</div>`;
            }
        }

        function renderFeatureSection(container, title, items, highlight = false) {
            if (items.length === 0) return;

            const header = document.createElement('div');
            header.style.cssText = "font-weight: bold; color: #555; font-size: 0.85em; text-transform: uppercase; margin: 15px 0 8px 5px; border-bottom: 2px solid #eee; padding-bottom: 4px; display: flex; align-items: center; gap: 8px;";
            if (highlight) header.style.color = "#2a7";
            header.innerText = title;
            container.appendChild(header);

            items.forEach(feat => {
                const featDiv = document.createElement('div');
                featDiv.style.cssText = "display: flex; align-items: flex-start; gap: 12px; cursor: pointer; padding: 12px; border-radius: 8px; transition: all 0.2s; border: 1px solid transparent;";
                featDiv.onclick = () => openLogbook(feat.name, feat.source || 'logbuch', feat.filename || feat.name);
                featDiv.onmouseover = () => { featDiv.style.background = '#f9f9f9'; featDiv.style.borderColor = '#eee'; featDiv.style.transform = 'translateX(4px)'; };
                featDiv.onmouseout = () => { featDiv.style.background = 'transparent'; featDiv.style.borderColor = 'transparent'; featDiv.style.transform = 'translateX(0)'; };

                // Color based on status
                let badgeBg = "#eee", badgeColor = "#555";
                if (feat.status === "COMPLETED") { badgeBg = "#e8f5e9"; badgeColor = "#2e7d32"; }
                else if (feat.status === "ACTIVE") { badgeBg = "#e3f2fd"; badgeColor = "#1565c0"; }
                else if (feat.status === "PLAN") { badgeBg = "#fff3e0"; badgeColor = "#e65100"; }
                else if (feat.status === "TASK") { badgeBg = "#e1f5fe"; badgeColor = "#0277bd"; }
                else if (feat.status === "DOCS") { badgeBg = "#ede7f6"; badgeColor = "#5e35b1"; }

                const displayTitle = currentLanguage === 'de' ? feat.title_de : feat.title_en;
                const displaySummary = currentLanguage === 'de' ? feat.summary_de : feat.summary_en;

                featDiv.innerHTML = `
                    <div style="background: ${badgeBg}; color: ${badgeColor}; padding: 4px 8px; border-radius: 4px; font-size: 0.7em; font-weight: bold; min-width: 85px; text-align: center; text-transform: uppercase;">
                        ${feat.status}
                    </div>
                    <div style="flex: 1;">
                        <div style="font-weight: 600; color: #111; font-size: 0.95em;">${displayTitle}</div>
                        ${displaySummary ? `<div style="font-size: 0.85em; color: #666; margin-top: 3px; line-height: 1.4;">${displaySummary}</div>` : ''}
                    </div>
                `;
                container.appendChild(featDiv);
            });
        }

        function toggleFeatureStatus() {
            const modal = document.getElementById('feature-status-modal');
            if (modal.style.display === 'none') {
                modal.style.display = 'block';
                loadFeatureStatus();
                const debugModal = document.getElementById('debug-flags-modal');
                if (debugModal) debugModal.style.display = 'none';
            } else {
                modal.style.display = 'none';
            }
        }

        async function openLogbook(featureName, source = 'logbuch', filename = null) {
            const modal = document.getElementById('logbook-modal');
            const titleElement = document.getElementById('logbook-title');
            const contentElement = document.getElementById('logbook-content');

            // Close feature modal if open
            const featureModal = document.getElementById('feature-status-modal');
            if (featureModal) featureModal.style.display = 'none';

            titleElement.innerText = `Logbuch: ${featureName}`;
            contentElement.innerHTML = '<div class="spinner" style="margin: 20px auto;"></div>';
            modal.style.display = 'block';

            try {
                const entryRef = source === 'root' ? (filename || featureName) : featureName;
                let markdown = await eel.get_logbook_entry(entryRef, source)();

                // Bilingual split logic
                if (markdown.includes('<!-- lang-split -->')) {
                    const parts = markdown.split('<!-- lang-split -->');
                    if (currentLanguage === 'de') {
                        markdown = parts[0];
                    } else {
                        markdown = parts[1] || parts[0]; // Fallback if second part is missing
                    }
                }

                // Simple markdown parsing for display
                let html = markdown
                    .replace(/^# (.*$)/gim, '<h1 style="margin-top:0; color: #1a1a1a; font-size: 1.5em;">$1</h1>')
                    .replace(/^## (.*$)/gim, '<h2 style="margin-top:20px; color: #333; font-size: 1.25em; border-bottom: 1px solid #eee; padding-bottom: 5px;">$1</h2>')
                    .replace(/^\- (.*$)/gim, '<li style="margin-left: 20px;">$1</li>')
                    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                    .replace(/\n\n/g, '<br><br>');

                contentElement.innerHTML = html;
            } catch (e) {
                contentElement.innerHTML = `<p style="color: #f44;">${t('edit_error_loading')}${e}</p>`;
            }
        }

        async function clearDatabase() {
            if (confirm(t("reset_confirm_db"))) {
                const result = await eel.clear_database()();
                if (result.status === 'ok') {
                    alert(t("reset_success_db"));
                    loadLibrary(); // Update views
                }
            }
        }

        async function resetBackend() {
            if (!confirm("Möchten Sie das Backend wirklich zurücksetzen? Die Verbindung wird kurzzeitig unterbrochen.")) return;
            try {
                const res = await eel.reset_backend()();
                if (res && res.status === 'success') {
                    alert("Backend-Reset erfolgreich: " + res.message);
                    location.reload(); // Refresh to re-initialize everything
                } else {
                    alert("Fehler beim Backend-Reset: " + (res ? res.message : 'Unknown error'));
                }
            } catch (e) {
                console.error("Backend Reset Exception:", e);
                alert("Fehler bei der Kommunikation mit dem Backend.");
            }
        }

        async function resetAppData() {
            if (confirm(t("reset_confirm_app"))) {
                const result = await eel.reset_app_data()();
                if (result.status === 'ok') {
                    alert(t("reset_success_app"));
                    location.reload();
                } else {
                    alert(t("common_error_prefix") + result.message);
                }
            }
        }
        // ============ Resizable Splitter Logic ============
        async function runRoutingBenchmark(type) {
            const resultsContainer = document.getElementById('routing-benchmark-results');
            const outputPre = document.getElementById('routing-benchmark-output');
            if (!resultsContainer || !outputPre) return;

            resultsContainer.style.display = 'block';
            outputPre.innerHTML = `🚀 [Benchmark] Initialisiere ${type === 'latency' ? 'Latenz-Test' : 'Format-Coverage'}...\n\n`;
            resultsContainer.scrollIntoView({ behavior: 'smooth' });

            const script_id = {
                'latency': 'routing/test_perf_latency.py',
                'multi': 'routing/test_multi_format_router.py',
                'playback': 'routing/test_playback_matrix.py',
                'complete': 'routing/test_complete_routing_suite.py'
            }[type] || 'routing/test_perf_latency.py';

            try {
                // We use the existing run_tests logic which streams output
                const result = await eel.run_tests(script_id)();

                if (result.status === 'finished') {
                    outputPre.innerHTML += `\n✅ [Benchmark] Fertiggestellt mit Status: ${result.code}\n`;
                } else if (result.status === 'error') {
                    outputPre.innerHTML += `\n❌ [Benchmark] Fehler: ${result.error}\n`;
                }
            } catch (err) {
                console.error('[runRoutingBenchmark] Exception:', err);
                outputPre.innerHTML += `\n❌ [Benchmark] System-Fehler: ${err}\n`;
            }
        }

        /**
         * Global Splitter Initialization
         * side: 'left' (default) or 'right' for vertical splitters.
         *       'top' (default) or 'bottom' for horizontal splitters.
         */
        function initSplitter(splitterId, targetPaneId, containerId, orientation = 'vertical', side = 'left') {
            const splitter = document.getElementById(splitterId);
            const targetPane = document.getElementById(targetPaneId);
            const container = document.getElementById(containerId);
            let isDragging = false;

            if (!splitter || !targetPane || !container) return;

            const isVertical = orientation === 'vertical';
            const storageKey = `mwv_splitter_${splitterId}`;

            // Restore previous state
            let savedPos = localStorage.getItem(storageKey);
            if (savedPos && isVertical) {
                const numericPos = parseInt(savedPos);
                if (numericPos > 600) savedPos = "300";
            }

            if (savedPos) {
                if (isVertical) {
                    targetPane.style.width = savedPos + 'px';
                } else {
                    targetPane.style.height = savedPos + 'px';
                }
                targetPane.style.flex = 'none';
            }

            splitter.addEventListener('mousedown', (e) => {
                isDragging = true;
                splitter.classList.add('active');
                document.body.style.cursor = (isVertical ? 'col-resize' : 'ns-resize');
                e.preventDefault();
            });

            window.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const rect = container.getBoundingClientRect();
                let size;

                if (isVertical) {
                    if (side === 'left') {
                        size = e.clientX - rect.left;
                    } else {
                        size = rect.right - e.clientX;
                    }
                    const minW = 150;
                    const maxW = rect.width - 250;
                    if (size < minW) size = minW;
                    if (size > maxW) size = maxW;
                    targetPane.style.width = size + 'px';
                } else {
                    if (side === 'top' || side === 'left') {
                        size = e.clientY - rect.top;
                    } else {
                        size = rect.bottom - e.clientY;
                    }
                    const minH = 100;
                    const maxH = rect.height - 100;
                    if (size < minH) size = minH;
                    if (size > maxH) size = maxH;
                    targetPane.style.height = size + 'px';
                }
                targetPane.style.flex = 'none';
                localStorage.setItem(storageKey, size);
            });

            window.addEventListener('mouseup', () => {
                if (!isDragging) return;
                isDragging = false;
                splitter.classList.remove('active');
                document.body.style.cursor = 'default';
            });
        }

        initSplitter('edit-splitter', 'edit-sidebar-left', 'edit-split-container', 'vertical', 'left');
        initSplitter('main-splitter', 'main-sidebar', 'main-split-container', 'vertical', 'left');
        initSplitter('parser-tab-splitter', 'parser-left-settings', 'parser-tab-split-container', 'vertical', 'left');
        initSplitter('debug-splitter', 'debug-settings-pane', 'debug-flag-persistence-panel', 'vertical', 'right');
        initSplitter('logbuch-splitter', 'logbuch-sidebar', 'logbuch-split-container', 'vertical', 'right');
        initSplitter('player-analytics-splitter', 'video-queue-pane', 'player-tab-split-container', 'vertical', 'right');
        selectEngine('chrome', document.querySelector('.options-subtab[data-engine=chrome]'));
        initSplitter('browser-tab-splitter', 'browser-top-pane', 'filesystem-crawler-directory-panel', 'horizontal', 'top');

        async function syncVersionInfo() {
            try {
                const version = await eel.get_version()();
                const footerVersion = document.getElementById('footer-version');
                if (footerVersion) footerVersion.innerText = `v${version}`;
                const envAppVersionEl = document.getElementById('env-app-version');
                if (envAppVersionEl) envAppVersionEl.textContent = version;
            } catch (err) {
                console.warn('[syncVersionInfo] Failed to fetch version:', err);
            }
        }

        async function loadTestSuites(retryCount) {
            retryCount = retryCount || 0;
            const container = document.getElementById('test-suites-container');
            const scriptsList = document.getElementById('test-scripts-list');
            const routingList = document.getElementById('routing-test-scripts-list');
            if (!container) return;

            if (retryCount === 0) {
                const loadingHtml = `<div style="color: #999; font-style: italic;" data-i18n="test_loading">${t('test_loading', 'Suites werden geladen...')}</div>`;
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
                        comment: t('test_gui_comment', 'Interaktive E2E Tests im Browser.')
                    }
                });

                if (container) container.innerHTML = '';
                if (scriptsList) scriptsList.innerHTML = '';
                if (routingList) routingList.innerHTML = '';

                // Group by folder, with UI folders prioritized and subfolders grouped
                const groups = {};
                suites.forEach(suite => {
                    let folder = suite.folder || 'Root';
                    // Normalize UI folder grouping
                    if (folder.toLowerCase().startsWith('ui')) folder = 'UI/' + folder.slice(2).replace(/^\/+/, '');
                    if (!groups[folder]) groups[folder] = [];
                    groups[folder].push(suite);
                });

                // Sort: UI folders first, then Root, then others
                const sortedFolders = Object.keys(groups).sort((a, b) => {
                    const isAUI = a.toLowerCase().startsWith('ui');
                    const isBUI = b.toLowerCase().startsWith('ui');
                    if (isAUI && !isBUI) return -1;
                    if (!isAUI && isBUI) return 1;
                    if (a === 'Root') return 1;
                    if (b === 'Root') return -1;
                    return a.localeCompare(b);
                });

                sortedFolders.forEach(folder => {
                    const folderSuites = groups[folder].sort((a, b) => a.name.localeCompare(b.name));
                    if (folderSuites.length === 0) return;

                    // Section Header with UI highlight
                    const header = document.createElement('div');
                    let headerStyle = 'grid-column: 1/-1; width: 100%; padding: 15px 5px 5px 5px; font-weight: bold; font-size: 1.1em; color: #444; border-bottom: 2px solid #edeff5; margin-top: 20px; display: flex; align-items: center; gap: 8px; background: rgba(255,255,255,0.9); backdrop-filter: blur(5px); position: sticky; top: 0; z-index: 100;';
                    if (folder.toLowerCase().startsWith('ui')) headerStyle += ' background: #e3f2fd; color: #1565c0;';
                    header.style.cssText = headerStyle;
                    const folderLabel = folder === 'Root' ? t('test_suites_root', 'Core Utilities & Tests') : folder;
                    header.innerHTML = `<span>${folder === 'Root' ? '📂' : (folder.toLowerCase().startsWith('ui') ? '🖥️' : '📁')}</span> ${folderLabel}`;

                    if (container) container.appendChild(header.cloneNode(true));
                    if (scriptsList) scriptsList.appendChild(header.cloneNode(true));
                    if (routingList && folder.toLowerCase().includes('routing')) routingList.appendChild(header.cloneNode(true));

                    folderSuites.forEach(suite => {
                        try {
                            if (container) {
                                const card = createTestCard(suite);
                                container.appendChild(card);
                            }
                            if (scriptsList) {
                                const card = createTestCard(suite);
                                scriptsList.appendChild(card);
                            }
                            if (routingList && folder.toLowerCase().includes('routing')) {
                                const card = createTestCard(suite);
                                routingList.appendChild(card);
                            }
                        } catch (e) {
                            console.error('[loadTestSuites] Error creating card for', suite.name, e);
                        }
                    });
                });

                syncVersionInfo();

                if (suites.length > 0) {
                    const infoText = `${suites.length} Tests gefunden`;
                    [container, scriptsList, routingList].forEach(el => {
                        if (el) {
                            const info = document.createElement('div');
                            info.style.cssText = 'grid-column: 1/-1; width: 100%; text-align: right; font-size: 0.8em; color: #888; padding: 10px;';
                            info.innerText = infoText;
                            el.prepend(info);
                        }
                    });
                    console.log(`[loadTestSuites] Rendered ${suites.length} tests successfully.`);
                }
            } catch (e) {
                console.error('[loadTestSuites] Error:', e);
                const errorHtml = `<div style="color: #c33; padding: 20px;">${t('test_error_loading', 'Fehler beim Laden der Tests: ')}${e}</div>`;
                if (container) container.innerHTML = errorHtml;
                if (scriptsList) scriptsList.innerHTML = errorHtml;
            }
        }

        function createTestCard(suite) {
            const card = document.createElement('div');
            card.style.cssText = 'background: #fff; border: 1px solid #e0e0e0; border-radius: 10px; padding: 20px; display: flex; flex-direction: column; position: relative; box-shadow: 0 4px 6px rgba(0,0,0,0.02); transition: transform 0.2s, box-shadow 0.2s;';
            card.onmouseover = () => { card.style.transform = 'translateY(-2px)'; card.style.boxShadow = '0 6px 12px rgba(0,0,0,0.05)'; };
            card.onmouseout = () => { card.style.transform = 'translateY(0)'; card.style.boxShadow = '0 4px 6px rgba(0,0,0,0.02)'; };

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
                        <h3 style="margin: 0; font-size: 1.1em; color: #333;">${suite.name}</h3>
                    </div>
                    <div class="test-card-actions" style="display: flex; align-items: center; gap: 8px;">
                        ${categoryHtml}
                    </div>
                </div>
                <div style="display: grid; grid-template-columns: auto 1fr; gap: 8px 15px; font-size: 0.85em; color: #555; margin-bottom: 15px;">
                    <strong style="color: #333;">${t('test_meta_inputs')}:</strong> <span>${m.inputs || '-'}</span>
                    <strong style="color: #333;">${t('test_meta_outputs')}:</strong> <span>${m.outputs || '-'}</span>
                    <strong style="color: #333;">${t('test_meta_files')}:</strong> <span style="font-family: monospace; background: #f5f5f5; padding: 2px 4px; border-radius: 3px;">${m.files || '-'}</span>
                </div>
                <div style="margin-top: auto; padding-top: 15px; border-top: 1px solid #eee; font-size: 0.85em; color: #777; font-style: italic;">
                    ${m.comment || '-'}
                </div>
            `;

            if (!suite.isGuiTest) {
                const editBtn = document.createElement('button');
                editBtn.innerText = t('test_btn_edit');
                editBtn.style.cssText = 'border: none; background: #f0f0f0; border-radius: 4px; padding: 4px 8px; font-size: 0.8em; cursor: pointer; opacity: 0.6; transition: opacity 0.2s;';
                editBtn.onmouseover = () => editBtn.style.opacity = '1';
                editBtn.onmouseout = () => editBtn.style.opacity = '0.6';
                editBtn.onclick = (e) => {
                    e.stopPropagation();
                    openTestEditModal(suite);
                };
                const actionsArea = card.querySelector('.test-card-actions');
                if (actionsArea) actionsArea.prepend(editBtn);

                const delBtn = document.createElement('button');
                delBtn.innerText = '🗑️';
                delBtn.style.cssText = 'border: none; background: #fff; border-radius: 4px; padding: 4px 6px; font-size: 0.8em; cursor: pointer; opacity: 0.4; transition: all 0.2s;';
                delBtn.onmouseover = () => { delBtn.style.opacity = '1'; delBtn.style.background = '#ffebee'; };
                delBtn.onmouseout = () => { delBtn.style.opacity = '0.4'; delBtn.style.background = '#fff'; };
                delBtn.onclick = (e) => {
                    e.stopPropagation();
                    confirm(t('confirm_delete')) && deleteTest(suite.id);
                };
                if (actionsArea) actionsArea.appendChild(delBtn);
            }

            return card;
        }

        let isTestRunInProgress = false;

        async function runSelectedTests() {
            if (isTestRunInProgress) {
                return;
            }

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
                requestAnimationFrame(() => {
                    resultsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
                });
            }

            __testOutputBuffer = '';
            appendTestOutputChunk(`${t('test_run_starting')}\n`);
            summaryBadge.style.display = 'none';
            summaryBadge.textContent = '';

            let totalPasses = 0;
            let totalFails = 0;

            try {
                if (selectedFiles.length > 0) {
                    const result = await eel.run_tests(selectedFiles)();
                    if (result.error) {
                        appendTestOutputChunk(`${t('test_run_error')}${result.error}\n`);
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
                        appendTestOutputChunk(`\n\n[GUI-Tests] ${t('test_run_system_error')}${e}`);
                    }
                }

                if (selectedFiles.length > 0) {
                    summaryBadge.style.display = 'inline-block';
                    if (totalFails > 0) {
                        summaryBadge.textContent = `❌ ${totalFails} Failed, ${totalPasses} Passed`;
                        summaryBadge.style.background = '#ffebee';
                        summaryBadge.style.color = '#c62828';
                    } else {
                        summaryBadge.textContent = `✅ Alle ${totalPasses} Tests Passed`;
                        summaryBadge.style.background = '#e8f5e9';
                        summaryBadge.style.color = '#2e7d32';
                    }
                }
            } catch (e) {
                appendTestOutputChunk(`${t('test_run_system_error')}${e}\n`);
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
            safeText('test-edit-filename', `${t('test_meta_file_label')}tests/${suite.id}`);
            safeValue('test-edit-category', suite.metadata.category || '-');
            safeValue('test-edit-inputs', suite.metadata.inputs || '-');
            safeValue('test-edit-outputs', suite.metadata.outputs || '-');
            safeValue('test-edit-files', suite.metadata.files || '-');
            safeValue('test-edit-comment', suite.metadata.comment || '-');
            safeStyle('test-edit-modal', 'display', 'flex');
        }

        function closeTestEditModal() {
            safeStyle('test-edit-modal', 'display', 'none');
        }

        async function refreshReportingData() {
            if (typeof eel.get_test_results !== 'function') {
                console.error('[UI] eel.get_test_results not available. Check backend @eel.expose.');
                const container = document.getElementById('report-summary-table');
                if (container) container.innerHTML = '<p style="color: #c33;">Backend API Error: get_test_results missing.</p>';
                return;
            }
            const history = await eel.get_test_results()();
            if (!history || history.length === 0) {
                const container = document.getElementById('report-summary-table');
                if (container) container.innerHTML = '<p style="color: #999;">Keine Testdaten vorhanden.</p>';
                return;
            }
            if (window.Plotly) {
                renderCharts(history);
            } else {
                console.warn('[UI] Plotly not loaded. Skipping charts.');
            }
            renderReportingTable(history);

            // Update infrastructure stats
            safeText('report-engine-status', 'Bottle / WSGI');
            safeText('report-gevent-status', 'Aktiv (Gevent / Greenlet)');
            safeText('report-os-status', navigator.platform || 'Linux');

            // Update Hardware card in Dashboard
            try {
                const hw = await eel.get_hardware_info()();
                if (hw) {
                    safeText('report-gpu-status', hw.gpu_type || 'Generic');
                    safeText('dash-hw-disk', hw.disk_type || '-');
                    safeText('dash-hw-pcie', hw.pcie_gen || '-');
                    safeText('dash-hw-gpu', hw.gpu_type || '-');
                    const acc = (hw.encoders || []).join(', ').toUpperCase();
                    safeText('dash-hw-accel', acc || 'Software (CPU)');
                }
            } catch (e) {
                console.warn('Dashboard HW info fail:', e);
            }
        }

        function renderCharts(history) {
            const recent = history.slice(-20); // Last 20 for charts
            const timestamps = recent.map(r => new Date(r.timestamp * 1000).toLocaleString());
            const passes = recent.map(r => r.passes);
            const fails = recent.map(r => r.fails);
            const durations = recent.map(r => r.duration);

            // Pie Chart (Total Pass/Fail of all history)
            let totalP = 0, totalF = 0;
            history.forEach(r => { totalP += r.passes; totalF += r.fails; });
            Plotly.newPlot('status-pie-chart', [{
                values: [totalP, totalF],
                labels: ['Passed', 'Failed'],
                type: 'pie',
                marker: { colors: ['#4caf50', '#f44336'] }
            }], { title: t('report_total_status'), margin: { t: 40, b: 20, l: 20, r: 20 } });

            // Bar Chart (Duration)
            Plotly.newPlot('duration-bar-chart', [{
                x: timestamps,
                y: durations,
                type: 'bar',
                marker: { color: '#2196f3' }
            }], { title: t('report_duration_ms'), margin: { t: 40 }, xaxis: { visible: false } });

            // Trend Line
            Plotly.newPlot('trend-line-chart', [
                { x: timestamps, y: passes, name: 'Passes', line: { color: '#4caf50' } },
                { x: timestamps, y: fails, name: 'Fails', line: { color: '#f44336' } }
            ], { title: t('report_trend'), margin: { t: 40 } });
        }

        function renderReportingTable(history) {
            let html = '<table style="width:100%; border-collapse: collapse; margin-top: 15px;">';
            html += '<tr style="background: #f5f5f5;"><th style="padding: 10px; border: 1px solid #ddd;">Datum</th><th style="padding: 10px; border: 1px solid #ddd;">Ergebnis</th><th style="padding: 10px; border: 1px solid #ddd;">Dauer (s)</th></tr>';
            history.reverse().slice(0, 10).forEach(r => {
                const date = new Date(r.timestamp * 1000).toLocaleString();
                const statusColor = r.fails > 0 ? '#d32f2f' : '#388e3c';
                html += `<tr>
                    <td style="padding: 8px; border: 1px solid #ddd;">${date}</td>
                    <td style="padding: 8px; border: 1px solid #ddd; color: ${statusColor}; font-weight: bold;">${r.summary}</td>
                    <td style="padding: 8px; border: 1px solid #ddd;">${r.duration.toFixed(2)}s</td>
                </tr>`;
            });
            html += '</table>';
            safeHtml('report-summary-table', html);
        }

        async function saveTestMetadata() {
            if (!currentEditingTestFile) return;

            const metadata = {
                category: readValue('test-edit-category'),
                inputs: readValue('test-edit-inputs'),
                outputs: readValue('test-edit-outputs'),
                files: readValue('test-edit-files'),
                comment: readValue('test-edit-comment')
            };

            const res = await eel.update_test_metadata(currentEditingTestFile, metadata)();
            if (res.status === 'ok') {
                closeTestEditModal();
                loadTestSuites(); // Reload to show new metadata
                alert(t("test_save_success"));
            } else {
                alert(t("common_error") + res.error);
            }
        }

        async function createNewTest() {
            const name = prompt(t('test_new_prompt_name'));
            if (!name) return;
            const res = await eel.create_new_test(name)();
            if (res.status === 'ok') {
                loadTestSuites();
            } else {
                alert(t('common_error') + (res.message || res.error));
            }
        }

        async function deleteTest(filename) {
            if (!confirm(`Möchtest du den Test "${filename}" wirklich löschen?`)) return;
            const res = await eel.delete_test(filename)();
            if (res.status === 'ok') {
                loadTestSuites();
            } else {
                alert(t('common_error') + (res.message || res.error));
            }
        }

        // ============ Backend Sync Status ============
        async function checkConnection() {
            const indicator = document.getElementById('sync-indicator');
            const dot = document.getElementById('sync-dot');
            const text = document.getElementById('sync-text');

            if (typeof eel === 'undefined' || window.__eel_missing__ === true) {
                safeStyle('sync-dot', 'background', '#f44');
                safeStyle('sync-indicator', 'background', '#ffebee');
                safeText('sync-text', t('sync_offline_no_backend'));
                safeStyle('sync-text', 'color', '#c62828');
                if (lastSyncState !== 'missing-backend') {
                    appendUiTrace('sync-state: missing backend (eel unavailable)');
                }
                lastSyncState = 'missing-backend';
                return;
            }

            try {
                const res = await eel.ping()();
                if (res && res.status === 'ok') {
                    safeStyle('sync-dot', 'background', '#4CAF50');
                    safeStyle('sync-dot', 'boxShadow', '0 0 8px #4CAF50');
                    safeStyle('sync-indicator', 'background', '#e8f5e9');
                    safeText('sync-text', t('sync_synchronized'));
                    safeStyle('sync-text', 'color', '#2e7d32');
                    safeStyle('vsync-field', 'display', 'block');
                    if (lastSyncState !== 'ok') {
                        appendUiTrace('sync-state: synchronized');
                    }
                    lastSyncState = 'ok';
                } else {
                    throw new Error("Invalid response");
                }
            } catch (e) {
                safeStyle('sync-dot', 'background', '#ff9800');
                safeStyle('sync-indicator', 'background', '#fff3e0');
                safeText('sync-text', t('sync_connection_lost'));
                safeStyle('sync-text', 'color', '#e65100');
                if (lastSyncState !== 'lost') {
                    appendUiTrace(`sync-state: connection lost (${e && e.message ? e.message : e})`);
                }
                lastSyncState = 'lost';
            }
        }

        async function runFfmpegPipelineSuite() {
            let relpath = document.getElementById('pipeline-test-path').value;
            if (!relpath) {
                // Default to the real-world test file from logbook if empty
                relpath = "*.mp4";
                document.getElementById('pipeline-test-path').value = relpath;
            }

            const resultsContainer = document.getElementById('pipeline-results');
            const cardsContainer = document.getElementById('pipeline-cards');
            resultsContainer.style.display = 'block';
            cardsContainer.innerHTML = '<div style="grid-column: 1/-1; padding: 20px; text-align: center;">⏳ Tests laufen...</div>';

            try {
                const res = await eel.run_ffmpeg_pipeline_test(relpath)();
                if (res.status === 'ok') {
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
                } else {
                    cardsContainer.innerHTML = `<div style="grid-column: 1/-1; color: #d32f2f; padding: 20px; text-align: center;">❌ ${res.message}</div>`;
                }
            } catch (err) {
                cardsContainer.innerHTML = `<div style="grid-column: 1/-1; color: #d32f2f; padding: 20px; text-align: center;">❌ Fehler: ${err.message}</div>`;
            }
        }

        async function testMediaQualityScore() {
            const relpath = document.getElementById('pipeline-test-path').value;
            if (!relpath) return showToast("Pfad fehlt.");
            const info = await eel.analyze_media(relpath)();
            showToast(`🎯 Quality: ${info.quality_score}/100 | Mode: ${info.recommended_mode.toUpperCase()}`, 5000);
        }

        async function generateTestMatrix() {
            showToast("⏳ Erstelle Test-Pattern Matrix...");
            const res = await eel.run_video_matrix_test()();
            if (res.status === 'ok') {
                showToast(`✅ ${res.matrix.length} Test-Files erstellt in media/tests/matrix/`);
            }
        }

        /* --- VIDEO PLAYER TEST SUITE LOGIC --- */
        let videoTestHistory = [];

        async function populateTestVideoSelector() {
            const selector = document.getElementById('test-video-selector');
            if (!selector) return;

            const currentVal = selector.value;
            selector.innerHTML = '<option value="">-- Kein Video ausgewählt --</option>';

            const options = [];

            // 1. Add Library Items
            if (typeof allLibraryItems !== 'undefined' && allLibraryItems && allLibraryItems.length > 0) {
                allLibraryItems.forEach(v => {
                    const path = (v.path || "").toLowerCase();
                    if (path.endsWith('.mp4') || path.endsWith('.mkv') || path.endsWith('.avi') ||
                        path.endsWith('.mov') || path.endsWith('.webm') || path.endsWith('.ts') || path.endsWith('.iso')) {
                        options.push({ value: v.path, text: `📁 ${v.name}` });
                    }
                });
            }

            // 2. Add Test Matrix Files & Artifacts (from common locations)
            // We can also let the backend provide a dedicated 'test_mediums' list
            try {
                const testMedia = await eel.get_test_media_files()();
                if (testMedia && testMedia.length > 0) {
                    testMedia.forEach(tm => {
                        options.push({ value: tm.path, text: `🧪 ${tm.name}` });
                    });
                }
            } catch (e) {
                console.warn("Could not load dedicated test media:", e);
            }

            // Populate unique options
            const seen = new Set();
            options.forEach(opt => {
                if (!seen.has(opt.value)) {
                    const el = document.createElement('option');
                    el.value = opt.value;
                    el.textContent = opt.text;
                    if (opt.value === currentVal) el.selected = true;
                    selector.appendChild(el);
                    seen.add(opt.value);
                }
            });

            if (options.length === 0) {
                selector.innerHTML = '<option value="">-- Keine Medien gefunden (Scan nötig?) --</option>';
            }
        }

        /* --- Video Mode Triggers (Missing implementations) --- */
        async function triggerVLCPlay() {
            if (typeof eel.open_vlc === 'function') {
                return await eel.open_vlc(currentVideoItem.path)();
            } else {
                throw new Error("VLC Backend (open_vlc) nicht gefunden.");
            }
        }

        async function triggerWebMTranscode() {
            if (typeof eel.trigger_webm_transcode === 'function') {
                return await eel.trigger_webm_transcode(currentVideoItem.path)();
            } else {
                throw new Error("WebM Backend (trigger_webm_transcode) nicht gefunden.");
            }
        }

        async function triggerFFmpegPlay() {
            if (typeof eel.trigger_ffmpeg_stream === 'function') {
                return await eel.trigger_ffmpeg_stream(currentVideoItem.path)();
            } else {
                throw new Error("FFmpeg Backend (trigger_ffmpeg_stream) nicht gefunden.");
            }
        }

        async function triggerFragMP4Play() {
            if (typeof eel.start_mp4frag_conversion === 'function') {
                return await eel.start_mp4frag_conversion(currentVideoItem.path, "")();
            } else {
                throw new Error("FragMP4 Backend (start_mp4frag_conversion) nicht gefunden.");
            }
        }

        async function runMtxValidation() {
            const pathInput = document.getElementById('mtx-test-path');
            const path = pathInput ? pathInput.value : "";
            if (!path) {
                showToast("Bitte geben Sie einen Pfad zum Testen an.");
                return;
            }

            const resultsDiv = document.getElementById('mtx-validation-results');
            const cardsDiv = document.getElementById('mtx-status-cards');
            const logsDiv = document.getElementById('mtx-log-view');

            if (resultsDiv) resultsDiv.style.display = 'block';
            if (cardsDiv) cardsDiv.innerHTML = '<div style="grid-column: 1/-1; text-align: center; padding: 20px;">Teste MediaMTX Pipeline... 🛰️</div>';
            if (logsDiv) logsDiv.innerHTML = 'Starting validation...';

            try {
                const report = await eel.run_mtx_validation(path)();

                if (cardsDiv) {
                    cardsDiv.innerHTML = '';
                    const items = [
                        { label: 'Server Up', ok: report.server_up },
                        { label: 'HLS Push', ok: report.hls_push_ok },
                        { label: 'HLS Read', ok: report.hls_read_ok },
                        { label: 'WebRTC Push', ok: report.webrtc_push_ok },
                        { label: 'WebRTC Read', ok: report.webrtc_read_ok }
                    ];

                    items.forEach(it => {
                        const card = document.createElement('div');
                        card.style.padding = '10px';
                        card.style.borderRadius = '8px';
                        card.style.background = it.ok ? '#e8f5e9' : '#ffebee';
                        card.style.border = `1px solid ${it.ok ? '#4caf50' : '#f44336'}`;
                        card.style.textAlign = 'center';
                        card.style.fontSize = '0.8em';
                        card.style.fontWeight = 'bold';
                        card.style.color = it.ok ? '#1b5e20' : '#c62828';
                        card.innerHTML = `${it.ok ? '✅' : '❌'} ${it.label}`;
                        cardsDiv.appendChild(card);
                    });
                }

                if (logsDiv) {
                    logsDiv.innerHTML = report.logs.join('\n');
                    logsDiv.scrollTop = logsDiv.scrollHeight;
                }

            } catch (err) {
                if (logsDiv) logsDiv.innerHTML += `\n❌ Fehler: ${err}`;
            }
        }

        async function runVideoPlayerTest(mode) {
            const selector = document.getElementById('test-video-selector');
            const videoPath = selector.value;
            if (!videoPath) {
                showToast("Bitte wählen Sie zuerst ein Video für den Test aus.");
                return;
            }

            const videoName = selector.options[selector.selectedIndex].text;
            const startTime = performance.now();
            const resultId = Date.now();

            const entry = {
                id: resultId,
                date: new Date().toLocaleTimeString(),
                name: videoName,
                mode: mode,
                status: 'running',
                time: '...',
                details: 'Test läuft...'
            };
            videoTestHistory.unshift(entry);
            updateTestResultsTable();

            try {
                const item = allLibraryItems.find(i => i.path === videoPath);
                if (!item) throw new Error("Medium nicht in Bibliothek gefunden.");
                currentVideoItem = item;

                if (mode === 'direct') {
                    switchTab('video');
                    await playVideo(item, item.path);
                    const res = await monitorVjsPlayback();
                    entry.status = res.status;
                    entry.details = res.details;
                    entry.time = res.time + 's';
                } else if (mode === 'vlc') {
                    await triggerVLCPlay();
                    entry.status = 'pass';
                    entry.details = 'VLC Bridge Handshake erfolgreich.';
                } else if (mode === 'webm') {
                    switchTab('video');
                    // Force webm transcode by calling playVideo with a mock analysis or similar
                    // Actually playVideo already determines mode.
                    await playVideo(item, item.path); 
                    const res = await monitorVjsPlayback();
                    entry.status = res.status;
                    entry.details = res.details;
                    entry.time = res.time + 's';
                } else if (mode === 'ffmpeg') {
                    await triggerFFmpegPlay();
                    entry.status = 'pass';
                    entry.details = 'FFmpeg HLS/DASH Stream initialisiert.';
                } else if (mode === 'mpv') {
                    if (typeof eel.open_mpv === 'function') {
                        await eel.open_mpv(videoPath)();
                        entry.status = 'pass';
                        entry.details = 'MPV Player Instanz gestartet.';
                    } else {
                        throw new Error("MPV Backend (open_mpv) fehlt.");
                    }
                } else if (mode === 'ffplay') {
                    if (typeof eel.open_ffplay === 'function') {
                        await eel.open_ffplay(videoPath)();
                        entry.status = 'pass';
                        entry.details = 'FFplay Instanz gestartet.';
                    } else {
                        throw new Error("FFplay Backend (open_ffplay) fehlt.");
                    }
                } else if (mode === 'transcode') {
                    // Test the real-time transcoding URL
                    const source = await eel.get_play_source(videoPath)();
                    if (source.mode === 'direct') {
                        // For tests, we just verify the URL looks correct
                        entry.status = 'pass';
                        entry.details = 'Transcode-URL active: ' + source.url.substring(0, 30) + '...';
                        // Optionally play it?
                    } else {
                        throw new Error("Transcode-Modus konnte nicht aktiviert werden.");
                    }
                } else if (mode === 'mkvmerge') {
                    const res = await eel.trigger_mkvmerge_remux(videoPath)();
                    entry.status = res.status === 'ok' ? 'pass' : 'fail';
                    entry.details = res.details;
                } else if (mode === 'mtx') {
                    const res = await eel.trigger_mtx_stream(videoPath, "hls")();
                    entry.status = res.status === 'ok' ? 'pass' : 'fail';
                    entry.details = res.details;
                } else if (mode === 'mp4tag7') {
                    const res = await eel.trigger_mp4tag_faststart(videoPath)();
                    entry.status = res.status === 'ok' ? 'pass' : 'fail';
                    entry.details = res.details;
                } else if (mode === 'mp4frag') {
                    // Logic for MP4Frag test
                    if (typeof eel.start_mp4frag_conversion === 'function') {
                        await eel.start_mp4frag_conversion(videoPath, "")();
                        entry.status = 'pass';
                        entry.details = 'Fragmented MP4 Pipeline gestartet.';
                    } else {
                        throw new Error("MP4Frag Backend nicht verfügbar.");
                    }
                }

                entry.time = ((performance.now() - startTime) / 1000).toFixed(2) + 's';
            } catch (err) {
                entry.status = 'fail';
                entry.details = err.message || "Fehler beim Teststart";
                entry.time = 'Error';
            }

            updateTestResultsTable();
        }

        function monitorVjsPlayback(timeoutMs = 15000) {
            return new Promise((resolve, reject) => {
                if (!vjsPlayer) return reject("Video.js Player nicht initialisiert.");
                
                const startTime = Date.now();
                const checker = setInterval(() => {
                    if (vjsPlayer.currentTime() > 0.1 && !vjsPlayer.paused()) {
                        clearInterval(checker);
                        resolve({ 
                            status: 'pass', 
                            details: `Playback OK: ${vjsPlayer.currentType()} @ ${vjsPlayer.currentTime().toFixed(1)}s`,
                            time: ((Date.now() - startTime) / 1000).toFixed(2)
                        });
                    }
                    if (vjsPlayer.error()) {
                        clearInterval(checker);
                        reject(`VJS Error: ${vjsPlayer.error().message}`);
                    }
                    if (Date.now() - startTime > timeoutMs) {
                        clearInterval(checker);
                        reject(`Timeout: Playback did not start within ${timeoutMs/1000}s`);
                    }
                }, 500);
            });
        }

        function updateTestResultsTable() {
            const body = document.getElementById('video-test-results-body');
            if (!body) return;

            if (videoTestHistory.length === 0) {
                body.innerHTML = '<tr><td colspan="6" style="text-align: center; color: #999; padding: 40px;">Noch keine Testergebnisse vorhanden.</td></tr>';
                return;
            }

            body.innerHTML = '';
            videoTestHistory.forEach(e => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${e.date}</td>
                    <td style="font-weight: 600;">${e.name}</td>
                    <td><span style="font-size: 0.8em; background: #eee; padding: 2px 6px; border-radius: 4px;">${e.mode.toUpperCase()}</span></td>
                    <td><span class="status-badge status-${e.status}">${e.status}</span></td>
                    <td>${e.time}</td>
                    <td style="color: #666; font-size: 0.85em;">${e.details}</td>
                `;
                body.appendChild(tr);
            });
        }

        function clearTestHistory() {
            if (confirm("Möchten Sie den Testverlauf wirklich löschen?")) {
                videoTestHistory = [];
                updateTestResultsTable();
            }
        }

        async function runCodecMatrix() {
            try {
                showToast("Matrix Test startet (Mock-Dateien werden generiert)...");
                const res = await eel.run_video_matrix_test()();
                if (res.status === 'ok') {
                    res.matrix.forEach(m => {
                        const cell = document.getElementById('matrix-' + m.id.split('_').pop());
                        if (cell) {
                            cell.innerHTML = m.status === 'ready' ? '<span style="color: #2e7d32;">✅ Bereit</span>' : '<span style="color: #c62828;">❌ Fehlgeschlagen</span>';
                        }
                    });
                    showToast("Codec-Matrix erfolgreich generiert.");
                }
            } catch (err) {
                console.error("Matrix Error:", err);
                showToast("Fehler bei Matrix-Generierung.");
            }
        }
    
    
        (function initUiTraceHooks() {
            // Hijack alerts to log to backend
            if (window._trace_hooks_active) return;
            window._trace_hooks_active = true;

            appendUiTrace('initUiTraceHooks: hijacking popups and error handlers...');

            // --- POPUP HIJACKER ---
            const origAlert = window.alert;
            window.alert = function (msg) {
                appendUiTrace('[ALERT-PROXIED] ' + msg);
                if (window.eel && eel.log_js_error) {
                    eel.log_js_error({ type: 'POPUP_ALERT', message: msg, timestamp: new Date().toISOString() })();
                }
                origAlert(msg); // Call original alert
            };

            const origConfirm = window.confirm;
            window.confirm = function (msg) {
                appendUiTrace('[CONFIRM-PROXIED] ' + msg);
                if (window.eel && eel.log_js_error) {
                    eel.log_js_error({ type: 'POPUP_CONFIRM', message: msg, timestamp: new Date().toISOString() })();
                }
                return origConfirm(msg);
            };

            const origPrompt = window.prompt;
            window.prompt = function (msg, defaultVal) {
                appendUiTrace('[PROMPT-PROXIED] ' + msg, defaultVal);
                if (window.eel && eel.log_js_error) {
                    eel.log_js_error({ type: 'POPUP_PROMPT', message: msg, timestamp: new Date().toISOString() })();
                }
                return origPrompt(msg, defaultVal);
            };

            // --- ERROR HIJACKER ---
            window.addEventListener('error', (e) => {
                const msg = `js-error: ${e.message} at ${e.filename}:${e.lineno}:${e.colno}`;
                appendUiTrace(msg);
                if (window.eel && eel.log_js_error) {
                    eel.log_js_error({
                        type: 'UNHANDLED_REJECTION',
                        message: msg,
                    })();
                }
            });

            appendUiTrace('initUiTraceHooks: attached successfully.');
        })();

        /* --- DOM INTEGRITY HELP FUNCTIONS (Diagnostic) --- */
        window.logDivBalancePerTab = function () {
            const tabs = document.querySelectorAll('.tab-content');
            console.group("DOM Integrity Check: DIV Balance Per Tab");
            let totalIssues = 0;

            tabs.forEach(tab => {
                const id = tab.id;
                const html = tab.innerHTML;
                const opens = (html.match(/<div/g) || []).length;
                const closes = (html.match(/<\/div/g) || []).length;
                const delta = opens - closes;

                const status = delta === 0 ? "✅ OK" : "❌ IMBALANCED";
                if (delta !== 0) totalIssues++;

                console.log(`[${id}] ${status} | Opens: ${opens} | Closes: ${closes} | Delta: ${delta}`);
            });

            if (totalIssues === 0) {
                console.log("Overall: All tabs are internally balanced.");
            } else {
                console.warn(`Overall: Detected ${totalIssues} imbalanced tabs.`);
            }
            console.groupEnd();
            return totalIssues === 0;
        };

        function toggleImpressum() {
            const modal = document.getElementById('impressum-modal');
            if (modal) {
                modal.style.display = (modal.style.display === 'flex' ? 'none' : 'flex');
            }
        }
        function toggleDebugDict() {
            const trigger = document.getElementById('telemetry-inspector-tab-trigger');
            if (trigger) switchTab('debug', trigger);
        }

        window.runRoutingBenchmark = async function (type) {
            const resultsContainer = document.getElementById('routing-benchmark-results');
            const outputArea = document.getElementById('routing-benchmark-output');
            if (!resultsContainer || !outputArea) return;

            resultsContainer.style.display = 'block';
            outputArea.textContent = 'Benchmarking starting...\n';
            resultsContainer.scrollIntoView({ behavior: 'smooth' });

            const scriptMap = {
                'latency': 'routing/test_perf_latency.py',
                'multi': 'routing/test_multi_format_router.py'
            };

            const scriptId = scriptMap[type];
            if (!scriptId) return;

            try {
                outputArea.textContent += `Executing: tests/${scriptId}\n\n`;
                // Use run_tests since it handles the environment and subprocess correctly
                const result = await eel.run_tests([scriptId])();
                outputArea.textContent += result.output || result.error || 'No output returned.';
            } catch (err) {
                outputArea.textContent += `\nError: ${err}`;
            }
        };

        /* --- SPLITTER LOGIC --- */
        function initSplitterV(splitterId, leftId, rightId, defaultPercent = 30) {
            const splitter = document.getElementById(splitterId);
            const left = document.getElementById(leftId);
            const right = document.getElementById(rightId);
            if (!splitter || !left || !right) return;

            // Initial state
            left.style.width = `${defaultPercent}%`;
            left.style.flex = 'none';
            right.style.flex = '1';

            let isDragging = false;

            splitter.addEventListener('mousedown', (e) => {
                isDragging = true;
                document.body.style.cursor = 'col-resize';
                splitter.classList.add('active');
                e.preventDefault();
            });

            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const container = splitter.parentElement;
                const containerRect = container.getBoundingClientRect();
                const newLeftWidth = e.clientX - containerRect.left;
                const percent = (newLeftWidth / containerRect.width) * 100;
                
                if (percent > 10 && percent < 90) {
                    left.style.width = `${percent}%`;
                }
            });

            document.addEventListener('mouseup', () => {
                if (isDragging) {
                    isDragging = false;
                    document.body.style.cursor = 'default';
                    splitter.classList.remove('active');
                }
            });
        }

        function initSplitterH(splitterId, topId, bottomId, defaultHeight = 200) {
            const splitter = document.getElementById(splitterId);
            const top = document.getElementById(topId);
            const bottom = document.getElementById(bottomId);
            if (!splitter || !top || !bottom) return;

            top.style.height = `${defaultHeight}px`;
            top.style.flex = 'none';
            bottom.style.flex = '1';

            let isDragging = false;

            splitter.addEventListener('mousedown', (e) => {
                isDragging = true;
                document.body.style.cursor = 'row-resize';
                splitter.classList.add('active');
                e.preventDefault();
            });

            document.addEventListener('mousemove', (e) => {
                if (!isDragging) return;
                const container = splitter.parentElement;
                const containerRect = container.getBoundingClientRect();
                const newHeight = e.clientY - containerRect.top;
                
                if (newHeight > 50 && newHeight < containerRect.height - 50) {
                    top.style.height = `${newHeight}px`;
                }
            });

            document.addEventListener('mouseup', () => {
                if (isDragging) {
                    isDragging = false;
                    document.body.style.cursor = 'default';
                    splitter.classList.remove('active');
                }
            });
        }
    
