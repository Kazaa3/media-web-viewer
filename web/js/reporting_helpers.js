/**
 * reporting_helpers.js - Modularized reporting and analytics logic
 * Extracted from app.html and ui_nav_helpers.js
 */

/**
 * Switches between different reporting views.
 * Moved from ui_nav_helpers.js to consolidate reporting logic.
 */
function switchReportingView(view) {
    if (typeof traceUiNav === 'function') {
        traceUiNav('SUBTAB-REPORT', view);
    }
    
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

    document.querySelectorAll('.reporting-subtab').forEach(btn => {
        btn.classList.toggle('active', btn.getAttribute('data-view') === view);
    });

    if (view === 'database' && typeof loadSqlFiles === 'function') {
        loadSqlFiles();
    }
    
    // Auto-update dashboard if switching to it
    if (view === 'dashboard' && typeof updateAnalyticsDashboard === 'function') {
        updateAnalyticsDashboard();
    }
}

/**
 * Hardware & Performance Dashboard Population
 */
function updateDashboardHwInfo(hw) {
    try {
        if (hw) {
            if (typeof safeText === 'function') {
                safeText('report-engine-status', `Bottle / Gevent / Python ${hw.python_version || '3.14.2'}`);
                safeText('report-gpu-status', hw.gpu_type || 'Generic');
                safeText('dash-hw-disk', hw.disk_type || '-');
                safeText('dash-hw-pcie', hw.pcie_gen || '-');
                safeText('dash-hw-gpu', hw.gpu_type || '-');
                const acc = (hw.encoders || []).join(', ').toUpperCase();
                safeText('dash-hw-accel', acc || 'Software (CPU)');
            }
        }
    } catch (e) {
        console.warn('Dashboard HW info fail:', e);
    }
}

/**
 * Analytics logic for Plotly charts
 */
function renderCharts(history) {
    if (typeof Plotly === 'undefined') {
        console.warn('Plotly not loaded, skipping charts.');
        return;
    }

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
    }], { 
        title: (typeof t === 'function') ? t('report_total_status') : 'Total Status', 
        margin: { t: 40, b: 20, l: 20, r: 20 } 
    });

    // Bar Chart (Duration)
    Plotly.newPlot('duration-bar-chart', [{
        x: timestamps,
        y: durations,
        type: 'bar',
        marker: { color: '#2196f3' }
    }], { 
        title: (typeof t === 'function') ? t('report_duration_ms') : 'Duration (ms)', 
        margin: { t: 40 }, 
        xaxis: { visible: false } 
    });

    // Trend Line
    Plotly.newPlot('trend-line-chart', [
        { x: timestamps, y: passes, name: 'Passes', line: { color: '#4caf50' } },
        { x: timestamps, y: fails, name: 'Fails', line: { color: '#f44336' } }
    ], { 
        title: (typeof t === 'function') ? t('report_trend') : 'Trend', 
        margin: { t: 40 } 
    });
}

/**
 * Renders the tabular summary of test history
 */
function renderReportingTable(history) {
    let html = '<table style="width:100%; border-collapse: collapse; margin-top: 15px;">';
    html += '<tr style="background: #f5f5f5;"><th style="padding: 10px; border: 1px solid #ddd;">Datum</th><th style="padding: 10px; border: 1px solid #ddd;">Ergebnis</th><th style="padding: 10px; border: 1px solid #ddd;">Dauer (s)</th></tr>';
    
    [...history].reverse().slice(0, 10).forEach(r => {
        const date = new Date(r.timestamp * 1000).toLocaleString();
        const statusColor = r.fails > 0 ? '#d32f2f' : '#388e3c';
        html += `<tr>
            <td style="padding: 8px; border: 1px solid #ddd;">${date}</td>
            <td style="padding: 8px; border: 1px solid #ddd; color: ${statusColor}; font-weight: bold;">${r.summary}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">${r.duration.toFixed(2)}s</td>
        </tr>`;
    });
    html += '</table>';
    
    if (typeof safeHtml === 'function') {
        safeHtml('report-summary-table', html);
    }
}

/**
 * Main entry point for updating the reporting dashboard
 */
async function updateAnalyticsDashboard() {
    if (typeof eel === 'undefined') return;
    
    try {
        const history = await eel.get_test_history()();
        if (history && history.length > 0) {
            renderCharts(history);
            renderReportingTable(history);
        }
        
        const hw = await eel.get_hardware_info()();
        updateDashboardHwInfo(hw);
    } catch (e) {
        console.error('[Reporting] Dashboard update failed:', e);
    }
}

// Initial call if on reporting tab
document.addEventListener('DOMContentLoaded', () => {
    const activeTab = localStorage.getItem('mwv_active_tab');
    if (activeTab === 'reporting') {
        updateAnalyticsDashboard();
    }
});
