/**
 * fragment_loader.js - Dynamically loads HTML fragments into the DOM.
 * Supports caching and post-load initialization hooks.
 */

const FragmentLoader = {
    cache: new Map(),

    /**
     * Loads an external HTML fragment into a container.
     * @param {string} targetId - The ID of the container element.
     * @param {string} fragmentPath - The path to the .html fragment.
     * @param {Function} callback - Optional callback after loading.
     */
    async load(targetId, fragmentPath, callback) {
        const container = document.getElementById(targetId);
        if (!container) {
            console.error(`[FragmentLoader] Container #${targetId} not found.`);
            return;
        }

        // Return if already loaded (unless we want to force reload)
        if (container.dataset.loaded === 'true') {
            if (callback) callback();
            return;
        }

        try {
            console.log(`[FragmentLoader] Loading fragment: ${fragmentPath}`);
            let html;

            if (this.cache.has(fragmentPath)) {
                html = this.cache.get(fragmentPath);
            } else {
                const response = await fetch(fragmentPath);
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                html = await response.text();
                this.cache.set(fragmentPath, html);
            }

            container.innerHTML = html;
            container.dataset.loaded = 'true';

            // Trigger translations for the new content
            if (typeof initTranslations === 'function') {
                initTranslations();
            }

            // Trigger splitters if any
            if (typeof initAllSplitters === 'function') {
                initAllSplitters();
            }

            if (callback) callback();
            
            // Dispatch a custom event for module-specific listeners
            const event = new CustomEvent('fragmentLoaded', { 
                detail: { targetId, fragmentPath } 
            });
            document.dispatchEvent(event);

        } catch (error) {
            console.error(`[FragmentLoader] Failed to load ${fragmentPath}:`, error);
            container.innerHTML = `<div class="error-panel">Failed to load module: ${error.message}</div>`;
        }
    }
};

// Global accessor
window.FragmentLoader = FragmentLoader;
