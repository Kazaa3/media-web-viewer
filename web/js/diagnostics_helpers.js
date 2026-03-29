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
        };

        // --- TAB RENDERING: DEBUG DATABASE ---
        window.renderDebugDatabase = async function() {
            const statsEl = document.getElementById('debug-db-info');
            const dictEl = document.getElementById('debug-items-json');
            const pidEl = document.getElementById('debug-python-pid');
            
            if (statsEl) statsEl.innerHTML = '<span style="color: #2a7;">Refresing Database Stats...</span>';
            if (dictEl) dictEl.innerHTML = '<span style="color: #6a1;">Loading Python Dictionary...</span>';

            try {
                const stats = await eel.get_debug_stats()();
                if (statsEl) {
                    statsEl.innerHTML = `
                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                            <div><b>Media Items:</b> ${stats.total_items || 0}</div>
                            <div><b>DB Version:</b> ${stats.db_version || 'v1.0'}</div>
                            <div><b>Last Sync:</b> ${new Date().toLocaleTimeString()}</div>
                            <div><b>Status:</b> <span style="color: #2a7;">Stable</span></div>
                        </div>
                    `;
                }
                
                if (pidEl) pidEl.innerText = stats.pid || 'N/A';

                const dictType = document.getElementById('debug-dict-select')?.value || 'library';
                const dictData = await eel.get_debug_dict(dictType)();
                if (dictEl) dictEl.innerText = JSON.stringify(dictData, null, 2);
            } catch (err) {
                if (statsEl) statsEl.innerHTML = `<span style="color: #f44;">Error: ${err.message}</span>`;
            }
        };

        // --- TAB RENDERING: TOOLS ---
        window.renderToolsDashboard = function() {
            const container = document.getElementById('tools-dashboard-panel');
            if (container) console.log("Tools Dashboard: Initialized");
        };
        
        // Startup health check fallback
        setTimeout(() => { 
            if (typeof eel !== "undefined" && typeof eel.report_spawn === 'function') {
                eel.report_spawn()(() => console.log("Diagnostics: Startup sync complete."));
            }
        }, 5000);
