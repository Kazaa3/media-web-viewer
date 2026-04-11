/**
 * UI Automated Test Suite (Self-Diagnostic)
 * Designed to test all Tabs, Sub-Tabs and Modals without external dependencies.
 */

const UiTestSuite = {
    results: [],
    isRunning: false,
    
    config: {
        categories: ['media', 'management', 'governance', 'diagnostics'],
        subTabs: {
            'media': ['player', 'library', 'playlist', 'video'],
            'management': ['item', 'file', 'edit', 'parser', 'tools'],
            'governance': ['options', 'debug', 'flags'],
            'diagnostics': ['tests', 'reporting', 'logbuch']
        }
    },

    async runAllTests() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.results = [];
        console.log("--- Starting UI Self-Test Suite ---");
        
        try {
            for (const cat of this.config.categories) {
                await this.testCategory(cat);
            }
            this.reportResults();
        } catch (err) {
            console.error("Test Suite Crashed:", err);
        } finally {
            this.isRunning = false;
        }
    },

    async testCategory(cat) {
        console.log(`Testing Category: ${cat}`);
        const btn = document.querySelector(`.tab-btn[data-category="${cat}"]`);
        if (!btn) {
            this.logResult(cat, 'FAIL', `Main category button for ${cat} not found.`);
            return;
        }

        // 1. Test clicking the main category
        btn.click();
        await this.delay(300);
        
        const subNav = document.getElementById('sub-nav-container');
        if (!subNav || subNav.style.display === 'none') {
            this.logResult(cat, 'FAIL', `Sub-navigation bar did not appear for ${cat}.`);
        } else {
            this.logResult(cat, 'PASS', `Main category ${cat} activated.`);
        }

        // 2. Test each sub-tab
        const subTabs = this.config.subTabs[cat] || [];
        for (const sub of subTabs) {
            await this.testSubTab(cat, sub);
        }
    },

    async testSubTab(cat, subId) {
        console.log(`  Testing Sub-Tab: ${subId}`);
        const subBtn = Array.from(document.querySelectorAll('.sub-tab-btn'))
                             .find(b => b.onclick && b.onclick.toString().includes(`'${subId}'`));
        
        if (!subBtn) {
            this.logResult(`${cat}:${subId}`, 'FAIL', `Sub-tab button for ${subId} not found.`);
            return;
        }

        subBtn.click();
        await this.delay(500);

        // Verify content visibility
        const activeContent = document.querySelector('.tab-content.active');
        if (!activeContent) {
            this.logResult(`${cat}:${subId}`, 'FAIL', `No tab-content is active after clicking.`);
            return;
        }

        const isVisible = activeContent.style.display !== 'none' && activeContent.offsetHeight > 0;
        if (!isVisible) {
            this.logResult(`${cat}:${subId}`, 'FAIL', `Tab content for ${subId} is not visible or zero height.`);
        } else {
            // Check for layout shift (simple bound check)
            const rect = activeContent.getBoundingClientRect();
            if (rect.top < 0 || rect.left < 0) {
                this.logResult(`${cat}:${subId}`, 'FAIL', `Content is shifted out of bounds (Top: ${rect.top}, Left: ${rect.left})`);
            } else {
                this.logResult(`${cat}:${subId}`, 'PASS', `Sub-tab ${subId} render OK.`);
            }
        }
    },

    logResult(test, status, message) {
        const result = { test, status, message, time: new Date().toLocaleTimeString() };
        this.results.push(result);
        console.log(`[${status}] ${test}: ${message}`);
        
        // Show in UI if the reporting dashboard is active
        this.updateUiReport(result);
    },

    updateUiReport(result) {
        const container = document.getElementById('test-results-log');
        if (container) {
            const line = document.createElement('div');
            line.className = `test-result-line status-${result.status.toLowerCase()}`;
            line.innerHTML = `<b>${result.test}</b>: ${result.message}`;
            container.prepend(line);
        }
    },

    reportResults() {
        const passCount = this.results.filter(r => r.status === 'PASS').length;
        const failCount = this.results.filter(r => r.status === 'FAIL').length;
        console.log(`--- Test Suite Finished: ${passCount} PASS, ${failCount} FAIL ---`);
        
        if (typeof showToast === 'function') {
            showToast(`Tests Finished: ${passCount} Pass, ${failCount} Fail`, failCount > 0 ? 'error' : 'success');
        }
    },

    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
};

// Expose to window
window.UiTestSuite = UiTestSuite;

// Created with MWV v1.46.00-MASTER
