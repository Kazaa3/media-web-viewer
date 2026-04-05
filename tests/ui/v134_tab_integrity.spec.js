const { test, expect } = require('@playwright/test');

/**
 * v1.34 UI Master Integrity Suite
 * Systematically audits all 11 core categories and their internal fragments.
 */

const categories = [
    'player', 'library', 'file', 'edit', 'options', 
    'parser', 'debug', 'tests', 'tools', 'logbuch', 'diagnostics'
];

test.describe('Media Viewer v1.34 UI Master Integrity — Navigation & Fragments', () => {
    
    test.beforeEach(async ({ page }) => {
        // Assume backend is running on local port 8345
        await page.goto('http://127.0.0.1:8345/app.html', { waitUntil: 'networkidle' });
    });

    for (const cat of categories) {
        test(`Tab Integrity: ${cat}`, async ({ page }) => {
            console.log(`[Audit] Checking Category: ${cat}`);

            // 1. Click main sidebar button
            const sidebarBtn = page.locator(`button.nav-item[onclick*="switchMainCategory('${cat}'"]`);
            await expect(sidebarBtn).toBeVisible();
            await sidebarBtn.click();

            // 2. Verify Tab Visibility (wait for .active class)
            // Each category maps to a container ID defined in ui_nav_helpers.js and app.html
            // We use the partial ID match or verify based on visibility
            const tabContent = page.locator('.tab-content.active');
            await expect(tabContent).toBeVisible();

            // 3. Verify Fragment Loading (No "Lade..." hang)
            // Fragments now target internal viewports: #-main-viewport
            const viewport = page.locator('.content-deck-fill:visible, .diagnostics-view:visible, .tools-sub-view:visible, .options-view:visible').first();
            
            // Wait up to 5s for fragment to populate (no longer showing loading-fragment)
            const loadingPlaceholder = page.locator('.loading-fragment:visible');
            await expect(loadingPlaceholder).toBeHidden({ timeout: 5000 });
            
            // 4. Verify Content — check for key UI markers
            const hasContent = await viewport.innerHTML();
            expect(hasContent.length).toBeGreaterThan(50); // Minimal content check

            // 5. Check Sub-Navigation (Internal Sidebar or Pills)
            const internalSidebar = page.locator('.tab-internal-sidebar:visible').first();
            if (await internalSidebar.count() > 0) {
                const subBtns = internalSidebar.locator('.nav-item');
                if (await subBtns.count() > 1) {
                    await subBtns.nth(1).click();
                    await expect(subBtns.nth(1)).toHaveClass(/active/);
                }
            } else {
                // Check for sub-tab pills in fragment
                const subPills = page.locator('.sub-pill-btn:visible, .sub-tab-btn:visible').first();
                if (await subPills.count() > 0) {
                    await subPills.click();
                    await expect(subPills).toHaveClass(/active/);
                }
            }
        });
    }

});
